## LLM microservice

Versatile REST API for the local LLM model.

### client

Dynamic client API docs: http://metroplex:5100

### testing frontend

http://metroplex:5100/cloud

### install

mit Cuda support:

```bash
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python
```

ohne Cuda support:

```bash
pip install -e .
```

### self deployment

```bash
python main.py
```

development deploy:

```bash 
python main 8080
```

### run test

```bash
python test/*.py
```

### deployed

deployed through service@metroplex tmux session

### development

add pre-commit hook:

[.git/hooks/pre-commit]
```bash
#!/bin/sh
python3 -m pytest test/*.py
```

For testing functions and prompt engeneering: edit functions.py as interactive or script.
It will dynamically connect to remote LLM model or host its own if required.

To add new endpoints simply add a static method to LLMFunctions. Don't forget to add a docstring. For dynamic API docs.

Backend development: server.py imports LLMFunctions from functions.py and serves it as REST API.
dynamically generates API documentation from LLMFunctions docstrings.