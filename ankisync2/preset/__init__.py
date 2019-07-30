from pathlib import Path
import json


class Preset:
    path: Path

    def __init__(self, name: str):
        self.path = Path(__file__).parent.joinpath(f"{name}.json")

    @property
    def data(self):
        return json.loads(self.path.read_text())
