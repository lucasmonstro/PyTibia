from src.repositories.inventory.core import images
from src.utils.core import locate
from src.utils.mouse import rightClick
from ...typings import Context
from .common.base import BaseTask


class OpenDepotTask(BaseTask):
    def __init__(self):
        super().__init__()
        self.name = 'openDepot'
        self.delayBeforeStart = 1
        self.delayAfterComplete = 1

    # TODO: add unit tests
    def do(self, context: Context) -> Context:
        depotPosition = locate(context['screenshot'], images['slots']['depot'])
        rightClick((depotPosition[0] + 5, depotPosition[1] + 5))
        return context

    # TODO: add unit tests
    # TODO: check if depot is opened
    def did(self, _: Context) -> bool:
        return True
