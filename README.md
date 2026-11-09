# Local Ollama LLM Agent

A small command-line agent for solving general reasoning problems using a model served by **Ollama on the local machine**. It makes one Ollama chat call per problem and requests only the final answer. It does not use cloud model APIs or guarantee a particular accuracy.

## Files

- `main.py` — CLI, JSON input validation, local Ollama calls, and JSON output.
- `requirements.txt` — Python dependency (`ollama`).
- `README.md` — setup and usage instructions.

## Setup

1. Install Ollama for your operating system and start its local service.
2. Install the Python dependency:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Pull the model before running the program. The default configured model is `qwen3:8b`:

   ```bash
   ollama pull qwen3:8b
   ```

   If the instructor specifies a different model name, pull that exact model and set `OLLAMA_MODEL` to the exact same name. For example:

   ```bash
   ollama pull <instructor-model-name>
   ```

   Linux/macOS:

   ```bash
   export OLLAMA_MODEL='<instructor-model-name>'
   ```

   Windows PowerShell:

   ```powershell
   $env:OLLAMA_MODEL = '<instructor-model-name>'
   ```

   If `OLLAMA_MODEL` is unset, the program uses `qwen3:8b`.

## Input and run

The input JSON can be either one object or a list of objects. Every object must have `id` and string-valued `problem` fields. Run:

```bash
python main.py --input input.json --output output.json
```

The output is always a JSON list of objects with `id` and `answer`; `answer` contains the model's requested final response only.

## Local/offline inference

All inference goes through the local Ollama Python library and the Ollama service on your machine. There are no cloud API integrations. After installing the dependency and pulling the chosen model, inference can run without internet access, provided Ollama and the model are available locally.
