"""Finite state machine module"""

from typing import Any, Dict, List

from pygraph_tool import EdgeException, GraphException, NodeException, Graph
from .fsm_exceptions import FSMException
from .state_behaviour import StateBehaviour


class FiniteStateMachine(Graph):
    """Defines the class that creates and manipulates finite states machine.

    Inherits from Graph.

    Attributes:
        id_first_state (str): Id for first state of fsm.
        ids_last_states (List[str]): Ids for last states of fsm.
        fsm_data_store (Dict[str, Any]): The data store for fsm.
    """

    def __init__(self) -> None:
        """Build the FiniteStateMachine instance."""
        super().__init__()
        self._id_first_state: str = ""
        self._ids_last_states: List[str] = []
        self._fsm_data_store: Dict[str, Any] = {}

    @property
    def id_first_state(self) -> str:
        """Id for first state of fsm."""
        return self._id_first_state

    @id_first_state.setter
    def id_first_state(self, id_first_state: str) -> None:
        self._id_first_state = id_first_state

    @property
    def ids_last_states(self) -> List[str]:
        """Ids for last states of fsm."""
        return self._ids_last_states

    @ids_last_states.setter
    def ids_last_states(self, ids_last_states: List[str]) -> None:
        self._ids_last_states = ids_last_states

    @property
    def fsm_data_store(self) -> Dict[str, Any]:
        """The data store for fsm."""
        return self._fsm_data_store

    @fsm_data_store.setter
    def fsm_data_store(self, fsm_data_store: Dict[str, Any]) -> None:
        self._fsm_data_store = fsm_data_store

    def add_bidirectional_edge(self) -> None:
        pass

    def register_state(
        self, state_behaviour: StateBehaviour, id_state: str
    ) -> None:
        """Register a state.

        Args:
            state_behaviour (StateBehaviour): State behaviour.
            id_state (str): State identifier.

        Raises:
            FSMException: If state behaviour not inherits to StateBehaviour or
                if state is impossible to register.
        """
        if not isinstance(state_behaviour, StateBehaviour):
            raise FSMException(
                "Parameter 'state_behaviour' must be StateBehaviour instance."
                f"State {id_state} is impossible to register."
            )
        try:
            self.add_node(node_content=state_behaviour, node_id=id_state)
        except (NodeException, GraphException) as error:
            raise FSMException(
                f"State {id_state} is impossible to register: {error}"
            ) from error

    def register_first_state(
        self, state_behaviour: StateBehaviour, id_first_state: str
    ) -> None:
        """Register first state, state to start fsm.

        Args:
            state_behaviour (StateBehaviour): State behaviour.
            id_first_state (str): State identifier for first state.
        """
        self._id_first_state = id_first_state
        self.register_state(
            state_behaviour=state_behaviour, id_state=id_first_state
        )

    def register_last_state(
        self, state_behaviour: StateBehaviour, id_last_state: str
    ) -> None:
        """Register last state, state to end fsm.

        Args:
            state_behaviour (StateBehaviour): State behaviour.
            id_last_state (str): State identifier for last state.
        """
        self._ids_last_states = [*self._ids_last_states, id_last_state]
        self.register_state(
            state_behaviour=state_behaviour, id_state=id_last_state
        )

    def register_transition(
        self, id_state_start: str, id_state_end: str, id_transition: str
    ) -> None:
        """Register transition between two states.

        Args:
            id_state_start (str): State identifier for start transition.
            id_state_end (str): State identifier for end transition.
            id_transition (str): Transition identifier.

        Raises:
            FSMException: If transition is impossible to register.
        """
        try:
            self.add_unidirectional_edge(
                node_id_start=id_state_start,
                node_id_end=id_state_end,
                edge_id=self._normalize_transition_id(
                    self._get_state_content(id_state_start), id_transition
                ),
            )
        except (EdgeException, GraphException) as error:
            raise FSMException(
                f"Transition {id_transition} is impossible to register: "
                f"{error}"
            ) from error

    def register_default_transition(
        self, id_state_start: str, id_state_end: str
    ) -> None:
        """Register default transition between two states.

        Transition identifier is "default-<StartNodeClassName>".

        Args:
            id_state_start (str): State identifier for start transition.
            id_state_end (str): State identifier for end transition.
        """
        behaviour: StateBehaviour = self._get_state_content(id_state_start)
        self.register_transition(
            id_state_start=id_state_start,
            id_state_end=id_state_end,
            id_transition=f"default-{behaviour.__class__.__name__}",
        )

    def _get_state_content(self, id_state: str) -> StateBehaviour:
        """Get the current state content.

        Args:
            id_state (str): State identifier to get content.

        Raises:
            FSMException: If state not found.

        Returns:
            StateBehaviour: The current state content.
        """
        for state in self.nodes:
            if state.node_id == id_state:
                return state.node_content
        raise FSMException(f"State id {id_state} not found.")

    def _get_next_state_id(self, id_transition: str) -> str:
        """Get the next state identifier.

        Args:
            id_transition (str): Transition identifier to find state target.

        Raises:
            FSMException: If transition not found.

        Returns:
            str: Next state identifier.
        """
        for transition in self.edges:
            if transition.edge_id == id_transition:
                return transition.node_end.node_id
        raise FSMException(f"Transition id {id_transition} not found.")

    def _state_process(self, id_state: str) -> None:
        """Run the current state.

        Args:
            id_state (str): State identifier to run.
        """
        behaviour: StateBehaviour = self._get_state_content(id_state=id_state)
        behaviour.state_data_store = {
            **behaviour.state_data_store,
            **self._fsm_data_store,
        }
        behaviour.action()
        self._fsm_data_store = {
            **self._fsm_data_store,
            **behaviour.state_data_store,
        }

        if id_state in self._ids_last_states:
            return

        next_state_id: str = self._get_next_state_id(
            id_transition=self._normalize_transition_id(
                behaviour, behaviour.next_transition_id()
            )
        )

        self._state_process(id_state=next_state_id)

    def _normalize_transition_id(
        self, behaviour: StateBehaviour, id_transition: str
    ) -> str:
        """Normalize transition id (lower case and add class name).

        Args:
            behaviour (StateBehaviour): The behaviour (node content).
            id_transition (str): The transition id before normalization.

        Returns:
            str: The transition id normalized.
        """
        class_name: str = behaviour.__class__.__name__
        if id_transition != f"default-{class_name}":
            id_transition = f"{id_transition.lower()}-{class_name}"
        return id_transition

    def run(self) -> None:
        """Run the finite states machine."""
        self._state_process(id_state=self.id_first_state)
