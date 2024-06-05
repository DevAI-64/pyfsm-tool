from typing import Any, Dict, List

from pyfsm_tool.finite_state_machine import FiniteStateMachine
from pyfsm_tool.fsm_exceptions import FSMException
from pyfsm_tool.state_behaviour import StateBehaviour
import pytest


class FirstState(StateBehaviour):
    def action(self) -> None:
        self.state_data_store["first_state"] = (
            f"first_state_ok_{self.state_data_store.get('my_key', '')}"
        )


class IntermediaryState(StateBehaviour):

    def __init__(self, transition_id: str) -> None:
        super().__init__()
        self._transition_id: str = transition_id

    def action(self) -> None:
        self.state_data_store["intermediary_state"] = (
            f"intermediary_state_ok_{self.state_data_store.get('my_key', '')}"
        )
    
    def next_transition_id(self) -> str:
        return self._transition_id


class LastState1(StateBehaviour):
    def action(self) -> None:
        self.state_data_store["last_state_1"] = (
            f"last_state_1_ok_{self.state_data_store.get('my_key', '')}"
        )
        self.state_data_store["last_state_1_with_first_state_data"] = (
            f"last_state_1_ok_{self.state_data_store.get('first_state', '')}"
        )


class LastState2(StateBehaviour):
    def action(self) -> None:
        self.state_data_store["last_state_2"] = (
            f"last_state_2_ok_{self.state_data_store.get('my_key', '')}"
        )
        self.state_data_store["last_state_2_with_intermediary_state_data"] = (
            "last_state_2_ok_"
            f"{self.state_data_store.get('intermediary_state', '')}"
        )


@pytest.fixture
def fsm() -> FiniteStateMachine:
    fsm: FiniteStateMachine = FiniteStateMachine()
    return fsm


@pytest.fixture
def fsm_with_states() -> FiniteStateMachine:
    fsm: FiniteStateMachine = FiniteStateMachine()
    fsm.register_first_state(FirstState(), "first_state")
    fsm.register_state(IntermediaryState("1"), "intermediary_state")
    fsm.register_last_state(LastState1(), "last_state_1")
    fsm.register_last_state(LastState2(), "last_state_2")
    return fsm


@pytest.fixture
def fsm_with_states_and_transitions_1() -> FiniteStateMachine:
    fsm: FiniteStateMachine = FiniteStateMachine()
    fsm.fsm_data_store = {"my_key": 42}
    fsm.register_first_state(FirstState(), "first_state")
    fsm.register_state(IntermediaryState("t1"), "intermediary_state")
    fsm.register_last_state(LastState1(), "last_state_1")
    fsm.register_last_state(LastState2(), "last_state_2")
    fsm.register_default_transition("first_state", "intermediary_state")
    fsm.register_transition("intermediary_state", "last_state_1", "t1")
    fsm.register_transition("intermediary_state", "last_state_2", "t2")
    return fsm


@pytest.fixture
def fsm_with_states_and_transitions_2() -> FiniteStateMachine:
    fsm: FiniteStateMachine = FiniteStateMachine()
    fsm.fsm_data_store = {"my_key": 42}
    fsm.register_first_state(FirstState(), "first_state")
    fsm.register_state(IntermediaryState("t2"), "intermediary_state")
    fsm.register_last_state(LastState1(), "last_state_1")
    fsm.register_last_state(LastState2(), "last_state_2")
    fsm.register_default_transition("first_state", "intermediary_state")
    fsm.register_transition("intermediary_state", "last_state_1", "t1")
    fsm.register_transition("intermediary_state", "last_state_2", "t2")
    return fsm


def test_fsm_data_store(fsm: FiniteStateMachine) -> None:
    data_store: Dict[str, Any] = {
        "thanks_for_all_the_fish": 42,
        "run_for_your_life": "Who"
    }
    fsm.fsm_data_store = data_store
    assert(fsm.fsm_data_store == data_store)


@pytest.mark.parametrize(
    "state_behaviour, id_state, nb_of_instances",
    [
        ("toto", "tata", 1),
        (IntermediaryState("1"), "intermediary_state", 2)
    ]
)
def test_register_state_with_exception(
    fsm: FiniteStateMachine,
    state_behaviour: Any,
    id_state: str,
    nb_of_instances: int
) -> None:
    with pytest.raises(FSMException):
        for _ in range(0, nb_of_instances):
            fsm.register_state(state_behaviour, id_state)


def test_register_state_without_exception(fsm: FiniteStateMachine) -> None:
    fsm.register_state(IntermediaryState("1"), "intermediary_state")
    assert(fsm.nodes[0].node_id == "intermediary_state")


def test_register_first_state(fsm: FiniteStateMachine) -> None:
    fsm.register_first_state(FirstState(), "first_state")
    assert(fsm.id_first_state == "first_state")


def test_register_last_state(fsm: FiniteStateMachine) -> None:
    fsm.register_last_state(LastState1(), "last_state_1")
    fsm.register_last_state(LastState2(), "last_state_2")
    assert(fsm.ids_last_states == ["last_state_1", "last_state_2"])


def test_register_transition_with_exception(
    fsm_with_states: FiniteStateMachine
) -> None:
    with pytest.raises(FSMException):
        for _ in range(0, 2):
            fsm_with_states.register_transition(
                "first_state", "intermediary_state", "t1"
            )


def test_register_transition_without_exception(
    fsm_with_states: FiniteStateMachine
) -> None:
    fsm_with_states.register_transition(
        "first_state", "intermediary_state", "t1"
    )
    results: List[str] = [
        fsm_with_states.edges[0].edge_id,
        fsm_with_states.edges[0].node_start.node_id,
        fsm_with_states.edges[0].node_end.node_id
    ]
    assert(results == ["t1", "first_state", "intermediary_state"])


def test_register_default_transition(
    fsm_with_states: FiniteStateMachine
) -> None:
    fsm_with_states.register_default_transition(
        "first_state", "intermediary_state"
    )
    fsm_with_states.register_default_transition(
        "intermediary_state", "last_state_1"
    )
    node_content_fs: Any = fsm_with_states.get_node("first_state").node_content
    node_content_intermediary: Any = fsm_with_states.get_node(
        "intermediary_state"
    ).node_content
    results: List[str] = [
        f"default-{node_content_fs.__class__.__name__}",
        f"default-{node_content_intermediary.__class__.__name__}"
    ]
    assert(
        results == [edge.edge_id for edge in fsm_with_states.edges]
    )


def test_get_state_content_with_exception(
    fsm_with_states: FiniteStateMachine
) -> None:
    with pytest.raises(FSMException):
        fsm_with_states._get_state_content("toto")


def test_get_state_content_without_exception(
    fsm_with_states: FiniteStateMachine
) -> None:
    assert(
        isinstance(
            fsm_with_states._get_state_content("first_state"),
            FirstState
        )
    )


def test_get_next_state_id_with_exception(
    fsm_with_states: FiniteStateMachine
) -> None:
    with pytest.raises(FSMException):
        fsm_with_states._get_next_state_id("toto")


def test_get_next_state_id_without_exception(
    fsm_with_states: FiniteStateMachine
) -> None:
    fsm_with_states.register_transition(
        "first_state", "intermediary_state", "t1"
    )
    assert(fsm_with_states._get_next_state_id("t1") == "intermediary_state")


def test_state_process_last_state_1(
    fsm_with_states_and_transitions_1: FiniteStateMachine
) -> None:
    results: Dict[str, Any] = {
        "my_key": 42,
        "first_state": "first_state_ok_42",
        "intermediary_state": "intermediary_state_ok_42",
        "last_state_1": "last_state_1_ok_42",
        "last_state_1_with_first_state_data": (
            "last_state_1_ok_first_state_ok_42"
        )
    }
    fsm_with_states_and_transitions_1._state_process("first_state")
    assert(results == fsm_with_states_and_transitions_1.fsm_data_store)
    


def test_state_process_last_state_2(
    fsm_with_states_and_transitions_2: FiniteStateMachine
) -> None:
    results: Dict[str, Any] = {
        "my_key": 42,
        "first_state": "first_state_ok_42",
        "intermediary_state": "intermediary_state_ok_42",
        "last_state_2": "last_state_2_ok_42",
        "last_state_2_with_intermediary_state_data": (
            "last_state_2_ok_intermediary_state_ok_42"
        )
    }
    fsm_with_states_and_transitions_2._state_process("first_state")
    assert(results == fsm_with_states_and_transitions_2.fsm_data_store)


def test_attributes(
    fsm_with_states_and_transitions_1: FiniteStateMachine
) -> None:
    results: List[str] = [
        fsm_with_states_and_transitions_1.id_first_state,
        *fsm_with_states_and_transitions_1.ids_last_states
    ]
    assert(results == ["first_state", "last_state_1", "last_state_2"])
