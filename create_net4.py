import pickle
from user_class import *

state20 = State(alias = '20')
state21 = State(alias = '21')

state10 = State(alias = '10')
state11 = State(alias = '11')
state12 = State(alias = '12')

t2a = Transition(state20, state21, alias = 't2a')
t2b = Transition(state21, state20, label_rel = 'r', alias = 't2b')
t2c = Transition(state20, state20, label_rel = 'f', alias = 't2c')

t1a = Transition(state10, state11, label_oss = 'o1', alias = 't3a')
t1b = Transition(state11, state12, alias = 't3b')
t1c = Transition(state12, state10, alias = 't3c')
t1d = Transition(state10, state12, label_oss = 'o2', alias = 't3c')


list_state_C2 = [state20, state21]
list_transition_C2 = [t2a, t2b]

C2 = FA(list_state_C2, list_transition_C2, initial_state = state20, actual_state = state20, alias = 'C2')

list_state_C1 = [state10, state11, state12]
list_transition_C1 = [t1a, t1b, t1c, t1d]

C1 = FA(list_state_C1, list_transition_C1, initial_state = state10, actual_state = state10, alias = 'C1')


L2 = Link(C2.alias, C1.alias, alias = 'L2')
L1 = Link(C1.alias, C2.alias, alias = 'L1')

e2 = Event(alias = 'e2')
e1 = Event(alias = 'e1')

function_e1L2 = EventFunction(e1, L2)
function_e2L1 = EventFunction(e2, L1)

t1d.input_event_func = function_e1L2
t1b.output_events_func = [function_e2L1]

t2c.input_event_func = function_e2L1
t2b.output_events_func = [function_e1L2]



net = Net([C1, C2], [L1, L2])

with open("net4.pickle", "wb") as f:
    pickle.dump(net, f)
