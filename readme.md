
## LLM microservice

Mimimaler LLM microservice, der eine Frage im text - zu - text Modus beantwortet.

### client

post request an http://metroplex:5100/answer

mit Params:
```json
{
  "question": "Was ist die Hauptstadt von Frankreich?",
}
```

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