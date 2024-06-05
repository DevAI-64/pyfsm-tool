"""State behaviour module"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class StateBehaviour(ABC):
    """Defines the class that creates and manipulates the state for fsm.

    Attributes:
        state_data_store (Dict[str, Any]): Data store.
    """

    def __init__(self) -> None:
        """Build the StateBehaviour instance."""
        super().__init__()
        self._state_data_store: Dict[str, Any] = {}

    @property
    def state_data_store(self) -> Dict[str, Any]:
        """State data store."""
        return self._state_data_store

    @state_data_store.setter
    def state_data_store(self, state_data_store: Dict[str, Any]) -> None:
        self._state_data_store = state_data_store

    @abstractmethod
    def action(self) -> None:
        """Defines action to be performed by the state, to be implemented."""

    def next_transition_id(self) -> str:
        """Defines the identifier of the next transition.

        Returns:
            str: The next transition id. By default returns
            "default-<ClassName>".
        """
        return f"default-{self.__class__.__name__}"
