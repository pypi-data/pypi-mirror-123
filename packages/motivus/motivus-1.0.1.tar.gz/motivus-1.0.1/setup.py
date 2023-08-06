import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="motivus",
    version="1.0.1",
    description="Motivus client library",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://motivus.cl",
    author="Motivus SpA",
    author_email="info@motivus.cl",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=setuptools.find_packages(),
    install_requires=["websockets", "asyncio"],
    include_package_data=True,
    python_requires='>=3.6',
)
