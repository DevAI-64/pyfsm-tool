from abc import ABC, abstractmethod
from typing import Any, Dict


class StateBehaviour(ABC):

    def __init__(self) -> None:
        super().__init__()
        self._state_data_store: Dict[str, Any]

    @abstractmethod
    def action(self) -> None:
        pass

    def next_transition_id(self) -> str:
        return "default"
