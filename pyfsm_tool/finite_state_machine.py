from typing import Any, Dict, Optional

from pyfsm_tool.fsm_exceptions import FSMException
from pygraph_tool.exceptions import (
    EdgeException, GraphException, NodeException
)
from pygraph_tool.graph import Graph
from pyfsm_tool.state_behaviour import StateBehaviour


class FiniteStateMachine:
    def __init__(self) -> None:
        self._graph: Graph = Graph()
        self._id_first_state: Optional[str] = None
        self._id_last_state: Optional[str] = None
        self._fsm_data_store: Dict[str, Any]

    @property
    def graph(self) -> Graph:
        return self._graph

    @graph.setter
    def graph(self, graph: Graph) -> None:
        self._graph = graph

    @property
    def id_first_state(self) -> Optional[str]:
        return self._id_first_state

    @id_first_state.setter
    def id_first_state(self, id_first_state: Optional[str]) -> None:
        self._id_first_state = id_first_state

    @property
    def id_last_state(self) -> Optional[str]:
        return self._id_last_state

    @id_last_state.setter
    def id_last_state(self, id_last_state: Optional[str]) -> None:
        self._id_last_state = id_last_state

    @property
    def fsm_data_store(self) -> Dict[str, Any]:
        return self._fsm_data_store

    @fsm_data_store.setter
    def fsm_data_store(self, fsm_data_store: Dict[str, Any]) -> None:
        self._fsm_data_store = fsm_data_store

    def register_state(
        self,
        state_behaviour: StateBehaviour,
        id_state: str
    ) -> None:
        try:
            self._graph.add_node(
                node_content=state_behaviour,
                node_id=id_state
            )
        except (NodeException, GraphException) as error:
            raise FSMException(
                f"State {id_state} is impossible to register: {error}"
            )

    def register_first_state(
        self,
        state_behaviour: StateBehaviour,
        id_first_state: str
    ) -> None:
        self._id_first_state = id_first_state
        self.register_state(
            state_behaviour=state_behaviour,
            id_state=id_first_state
        )

    def register_last_state(
        self,
        state_behaviour: StateBehaviour,
        id_last_state: str
    ) -> None:
        self._id_last_state = id_last_state
        self.register_state(
            state_behaviour=state_behaviour,
            id_state=id_last_state
        )

    def register_transition(
        self,
        id_state_start: str,
        id_state_end: str,
        id_transition: str
    ) -> None:
        try:
            self._graph.add_unidirectional_edge(
                node_id_start=id_state_start,
                node_id_end=id_state_end,
                edge_id=id_transition
            )
        except (EdgeException, GraphException) as error:
            raise FSMException(
                f"Transition {id_transition} is impossible to register: "
                f"{error}"
            )

    def register_default_transition(
        self,
        id_state_start: str,
        id_state_end: str
    ) -> None:
        self.register_transition(
            id_state_start=id_state_start,
            id_state_end=id_state_end,
            id_transition="default"
        )

    def _get_state_content(self, id_state: str) -> StateBehaviour:
        for state in self._graph.nodes:
            if state.node_id == id_state:
                return state.node_content

    def _get_next_state_id(self, id_transition: str) -> str:
        for transition in self._graph.edges:
            if transition.edge_id == id_transition:
                return transition.node_end.node_id

    def _state_process(self, id_state: str) -> None:

        behaviour: StateBehaviour = self._get_state_content(id_state=id_state)
        behaviour.action()

        if id_state == self._id_last_state:
            return

        next_state_id: str = self._get_next_state_id(
            behaviour.next_transition_id()
        )

        self._state_process(id_state=next_state_id)

    def run(self) -> None:
        self._state_process(id_state=self.id_first_state)
