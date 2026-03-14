import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "data", "trusted_sources.json")


def load_sources():
    if not os.path.exists(FILE):
        return []
    with open(FILE) as f:
        return json.load(f)


def is_trusted(source):
    if not source:
        return False
    sources = load_sources()
    return source.strip() in sources

def add_source(source):
    sources = load_sources()
    if source not in sources:
        sources.append(source)
        with open(FILE, "w") as f:
            json.dump(sources, f, indent=2)