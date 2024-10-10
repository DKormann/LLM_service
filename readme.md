
## LLM microservice

Mimimaler LLM microservice, der eine Frage im text - zu - text Modus beantwortet.

### client

Client API docs: http://metroplex:5100

### install

mit Cuda support:

```bash
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python
```

ohne Cuda support:

```bash
pip install -r requirements.txt
```

### self deployment

```bash
python server.py
```

### deployed
deployed through service@metroplex tmux session