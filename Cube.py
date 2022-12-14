from cubes import Workspace
from cubes.compat import ConfigParser


class Cube:
    def __init__(self):
        settings = ConfigParser()
        settings.read("./resources/config.ini")
        self.workspace = Workspace(config=settings)
        self.workspace.import_model("resources/covid.json")
        self.browser = self.workspace.browser("facts")
