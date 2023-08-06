from typing import Optional

from jsonargparse import ArgumentParser

from classy.cli import BaseCommand


class ServeCommand(BaseCommand):
    name = "serve"

    def parser(self) -> Optional[ArgumentParser]:
        parser = ArgumentParser(self.name, self.description)

    def run(self, config):
        pass
