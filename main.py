"""Local Ollama reasoning agent with a JSON command-line interface."""
import argparse
import json
import os
import re
import sys
from pathlib import Path

import ollama

SYSTEM_PROMPT = """You are a careful, general-purpose problem-solving assistant. Solve the
user's problem using whatever reasoning is appropriate. Return only the final
answer requested by the problem: no explanation, analysis, preamble, markdown,
or labels. Preserve any requested answer format exactly. If the problem asks
for a concise value or choice, output only that value or choice."""


def final_answer(text):
    """Keep only the answer, excluding any explicitly tagged reasoning."""
    text = str(text).strip()
    # Some reasoning models may include an explicit private-thought section.
    if "</think>" in text:
        text = text.rsplit("</think>", 1)[-1].strip()
    text = re.sub(r"^<think>.*?</think>\s*", "", text, flags=re.DOTALL).strip()
    return text


def solve(problem, model):
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": problem},
        ],
    )
    content = response["message"]["content"]
    answer = final_answer(content)
    if not answer:
        raise RuntimeError("Ollama returned an empty answer")
    return answer


def load_problems(path):
    with open(path, "r", encoding="utf-8") as source:
        data = json.load(source)
    problems = [data] if isinstance(data, dict) else data
    if not isinstance(problems, list):
        raise ValueError("Input JSON must be one object or a list of objects")
    for index, item in enumerate(problems):
        if not isinstance(item, dict) or "id" not in item or "problem" not in item:
            raise ValueError(f"Item {index} must be an object with 'id' and 'problem' fields")
        if not isinstance(item["problem"], str):
            raise ValueError(f"Item {index} field 'problem' must be a string")
    return problems


def main():
    parser = argparse.ArgumentParser(description="Solve JSON problems with a local Ollama model.")
    parser.add_argument("--input", required=True, help="Path to input JSON")
    parser.add_argument("--output", required=True, help="Path for output JSON")
    args = parser.parse_args()
    model = os.environ.get("OLLAMA_MODEL", "qwen3:8b")

    try:
        problems = load_problems(args.input)
        results = []
        for item in problems:
            results.append({"id": item["id"], "answer": solve(item["problem"], model)})
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as destination:
            json.dump(results, destination, ensure_ascii=False, indent=2)
            destination.write("\n")
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
