from typing import Protocol

from irispy2 import ChatContext


class ICommand(Protocol):
    invoke: str
    help: str
    type: str | None

    def handle(self, event:ChatContext) -> None:
        ...
