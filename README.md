# pyfsm-tool

pyfsm-tool is a module to create and manipulate finite states machines (fsm).

## Getting started

### Import modules
FiniteStateMachine module:
```python
from pyfsm_tool import FiniteStateMachine, StateBehaviour
```
Exceptions module:
```python
from pyfsm_tool import FSMException
```

### Create new FSM
The new fsm is empty (No state and no transition).
```python
fsm: FiniteStateMachine = FiniteStateMachine()
```

### Initialize the fsm data store
Initialize fsm data store wit 'message' and 'count' available for all states.
```python
fsm.fsm_data_store = {"message": "", "count": 0}
```

### Create new behaviours
Create new behaviours for fsm states.
- First behaviour: add 'Hello' in fsm data store (key = 'message') and next transition is 't1'
```python
class Behaviour1(StateBehaviour):
    def action(self) -> None:
        self.state_data_store["message"] += "Hello"

    def next_transition_id(self) -> str:
        return "t1"
```
- Second behaviour: add ' ' in fsm data store (key = 'message') and next transition is 't2'
```python
class Behaviour2(StateBehaviour):
    def action(self) -> None:
        self.state_data_store["message"] += " "

    def next_transition_id(self) -> str:
        return "t2"
```
- Third behaviour: add 'world' in fsm data store (key = 'message') and next transition is 't3'
```python
class Behaviour3(StateBehaviour):
    def action(self) -> None:
        self.state_data_store["message"] += "world"

    def next_transition_id(self) -> str:
        return "t3"
```
- Fourth behaviour: add '!' in fsm data store (key = 'message') and next transition is 't4' (itself) if the key 'count' in fsm data store is less than 2 (there is incrementation of fsm data store for key 'count'), else next transition is 't5' 
```python
class Behaviour4(StateBehaviour):
    def action(self) -> None:
        self.state_data_store["message"] += "!"

    def next_transition_id(self) -> str:
        if self.state_data_store.get("count") < 2:
            self.state_data_store["count"] += 1
            return "t4"
        return "t5"
```
- Fifth behaviour: display fsm data store (key = 'message') and finish fsm. 
```python
class Behaviour5(StateBehaviour):
    def action(self) -> None:
        print(self.state_data_store.get("message"))
```

### Register all states
- Register first state with first behaviour
```python
fsm.register_first_state(Behaviour1(), "b1")
```
- Register next states with next behaviours
```python
fsm.register_state(Behaviour2(), "b2")
fsm.register_state(Behaviour3(), "b3")
fsm.register_state(Behaviour4(), "b4")
```
- Register last state with last behaviour
```python
fsm.register_last_state(Behaviour5(), "b5")
```
If state behaviour not inherits `StateBehaviour` class or if state already 
exists(same id) or if an argument is `None`, then `FSMException` is raise.
```python
try:
    fsm.register_state(Behaviour2(), "b2")
except FSMException as error:
    pass  # or do something...
```

### Register all transitions
```python
fsm.register_transition("b1", "b2", "t1")
fsm.register_transition("b2", "b3", "t2")
fsm.register_transition("b3", "b4", "t3")
fsm.register_transition("b4", "b4", "t4")
fsm.register_transition("b4", "b5", "t5")
```
If transition already exists(same id) or if an argument is `None`, then `FSMException` is raise.
```python
try:
    fsm.register_transition("b1", "b2", "t1")
except FSMException as error:
    pass  # or do something...
```

### Run FSM
```python
fsm.run()
```

## Author
If you have any questions or suggestions, please don't hesitate to contact me : <belaich.david@outlook.fr>.
