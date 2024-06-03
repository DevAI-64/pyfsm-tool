from src.pyfsm_tool.state_behaviour import StateBehaviour
import pytest


class MyBehaviour(StateBehaviour):

    def action(self) -> None:
        self.state_data_store["my_test"] = 50

    def next_transition_id(self) -> str:
        return "my_transition"


@pytest.fixture
def my_behaviour() -> MyBehaviour:
    return MyBehaviour()


def test_action(my_behaviour: MyBehaviour) -> None:
    my_behaviour.action()
    assert(my_behaviour.state_data_store.get("my_test") == 50)


def test_next_transition_id(my_behaviour: MyBehaviour) -> None:
    assert(my_behaviour.next_transition_id() == "my_transition")
