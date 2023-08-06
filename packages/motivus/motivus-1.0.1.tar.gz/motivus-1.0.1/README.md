# Motivus Client Library

## Basic task execution example
Set your application token as an environment value as follows:
```environ
APPLICATION_TOKEN=MWBatxipDHG4daX3hemGO4nXZEgAvOTbBPyWDj36AsWqbOJc=
```
Execute some tasks
```python
from motivus.client import Client

conn = await Client.connect()

task_def = {"run_type": "wasm",
            "wasm_path": "./function.wasm",
            "loader_path": "./loader.js",
            "processing_base_time": 30,
            "flops": 45.0,
            "flop": 1.0,
            "arguments": [1, 3]
            }
task_id = conn.call_async(task_def)
task = conn.select_task(task_id)
result = await task
```

## Getting help
You can contact us anytime using our [contact form](https://motivus.cl/contact/).
