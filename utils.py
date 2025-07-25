import json

def load_persona_job(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
