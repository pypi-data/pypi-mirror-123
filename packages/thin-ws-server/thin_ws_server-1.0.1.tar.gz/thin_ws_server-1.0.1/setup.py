from setuptools import setup, find_packages


with open("Readme.md", "r", encoding="utf8") as f:
    long_description = f.read()


options = {
    "name": "thin_ws_server",
    "version": "1.0.1",
    "author": "atoy322",
    "description": "small implementation of websocket server.",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "url": "https://github.com/atoy322/ws_server",
    "packages": find_packages()
}

setup(**options)

