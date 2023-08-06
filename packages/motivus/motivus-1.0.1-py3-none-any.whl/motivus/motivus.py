#!/usr/bin/env python

import asyncio
import websockets
import json
import uuid
import base64
import os
import nest_asyncio
import sys
from websockets.client import WebSocketClientProtocol
nest_asyncio.apply()

default_uri = os.environ["WEBSOCKET_URI"] if "WEBSOCKET_URI" in os.environ else "ws://localhost:4000/client_socket/websocket"
default_token = os.environ["APPLICATION_TOKEN"] if "APPLICATION_TOKEN" in os.environ else "MWBatxipDHG4daX3hemGO4nXZEgAvOTbBPyWDj36AsWqbOJc="


class Client:
    def __init__(self):
        self.uri = default_uri
        self.token = default_token
        self.tasks = {}
        self.loop = asyncio.get_event_loop()
        self.id = 0
        self.channel_id = ""
        self.user_uuid = ""
        self.websocket: WebSocketClientProtocol = WebSocketClientProtocol()

    @classmethod
    async def connect(cls):
        """Sets up the client connection to the worker network. Must be called prior to task scheduling"""

        self = Client()
        self.websocket = await websockets.connect(f'{self.uri}?token={self.token}')
        await self.fetch_channel_id()
        await self.join_channel()

        asyncio.get_event_loop().create_task(self.heartbeat())
        asyncio.get_event_loop().create_task(self.message_listener())
        return self

    async def fetch_channel_id(self):
        """Ask for user_uuid of current associated token and generate a new channel id"""

        join_msg = dict(topic="room:client?", event="phx_join",
                        payload={}, ref="uuid")
        await self.websocket.send(json.dumps(join_msg))
        message = await self.websocket.recv()

        response = json.loads(message)
        if response["ref"] == "uuid" and "uuid" in response["payload"]["response"]:
            self.user_uuid = response["payload"]["response"]["uuid"]
            self.channel_id = f'{response["payload"]["response"]["uuid"]}:{str(uuid.uuid4())}'

            leave_msg = dict(topic="room:client?",
                             event="phx_leave", payload={}, ref=None)
            await self.websocket.send(json.dumps(leave_msg))
            await self.websocket.recv()

        else:
            sys.exit("Internal server error")

    async def join_channel(self):
        """Sets up channel communication"""

        join_msg = dict(topic="room:client:" + self.channel_id,
                        event="phx_join", payload={}, ref="join")
        await self.websocket.send(json.dumps(join_msg))
        message = await self.websocket.recv()

        response = json.loads(message)
        if response["ref"] == "join" and "status" in response["payload"] and response["payload"]["status"] == "error" and "reason" in response["payload"]["response"] and response["payload"]["response"]["reason"] == "unauthorized":
            sys.exit("Unauthorized connection. Check your APPLICATION_TOKEN")
        else:
            pass

    async def message_listener(self):
        """docstring for m"""
        async for message in self.websocket:
            response = json.loads(message)
            if response["event"] == "result":
                ref = response["payload"]["ref"]
                result = response["payload"]["body"]
                if ref in self.tasks:
                    self.tasks[ref].set_result(result)
            else:
                # print(response)
                pass

    async def heartbeat(self):
        data = dict(topic="phoenix", event="heartbeat", payload={}, ref=0)
        try:
            await self.websocket.send(json.dumps(data))

        except websockets.exceptions.ConnectionClosed:
            print('Connection with server closed')
        else:
            await asyncio.sleep(3)
            self.loop.create_task(self.heartbeat())

    def read_file(self, file_path):
        # Open a file: file
        file = open(file_path, mode='rb')
        # Read all lines at once
        all_of_it = file.read()
        # Encode
        encoded = base64.b64encode(all_of_it)
        all_of_it = encoded.decode('ascii')
        # close the file
        file.close()
        return all_of_it

    def empty_task(self):
        self.tasks = {}

    def call_async(self, metadata):
        ref = str(uuid.uuid4())
        # Get the current event loop.
        loop = asyncio.get_running_loop()
        # Create a new Future object.
        fut = loop.create_future()

        self.tasks[ref] = fut

        self.loop.create_task(self.call(metadata.copy(), ref))
        return ref

    def select_task(self, id):
        return self.tasks[id]

    def barrier(self, indexs=[]):
        buffer_task = [self.select_task(k) for k in indexs]
        task = asyncio.ensure_future(asyncio.gather(*buffer_task))
        return task

    async def reply_result(self, task_id, is_valid):
        data = dict(topic="room:client:" + self.channel_id,
                    event="phx_join", payload={}, ref=None)
        await self.websocket.send(json.dumps(data))
        payload = {"body": {"is_valid": is_valid}, "type": "validation",
                   "task_id": task_id, "client_id": self.user_uuid}
        msg = dict(
            topic="room:client:" + self.channel_id,
            payload=payload,
            event="set_validation",
            ref=None)
        msg = json.dumps(msg)
        await self.websocket.send(msg)
        return 1

    async def call(self, metadata, ref):
        if (metadata['run_type'] == 'wasm'):
            payload = {"body": {
                "wasm": self.read_file(metadata['wasm_path']),
                "loader": self.read_file(metadata['loader_path']),
                "params": metadata['arguments'],
                "run_type": metadata['run_type'],
                "processing_base_time": metadata['processing_base_time'],
                "flops": metadata['flops'],
                "flop": metadata['flop']
            },
                "type": "work",
                "ref": ref,
                "client_id": self.user_uuid
            }
        elif (metadata['run_type'] == 'js'):
            payload = {"body": {
                "loader": self.read_file(metadata['loader_path']),
                "params": metadata['arguments'],
                "run_type": metadata['run_type']
            },
                "type": "work",
                "ref": ref,
                "client_id": self.user_uuid
            }

        msg = dict(
            topic="room:client:" + self.channel_id,
            payload=payload,
            event="task",
            ref=None)
        msg = json.dumps(msg)
        await self.websocket.send(msg)
