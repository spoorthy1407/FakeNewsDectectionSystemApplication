import json

FILE = "data/trusted_sources.json"


def load_sources():

    with open(FILE) as f:
        return json.load(f)


def is_trusted(source):

    sources = load_sources()

    return source in sources


def add_source(source):

    sources = load_sources()

    if source not in sources:
        sources.append(source)

    with open(FILE, "w") as f:
        json.dump(sources, f)