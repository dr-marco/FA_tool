import pickle
from user_class import *


state10 = State(alias = '10')
state11 = State(alias = '11')

state20 = State(alias = '20')
state21 = State(alias = '21')

state30 = State(alias = '30')
state31 = State(alias = '31')

t1a = Transition(state10, state11, alias = 't1a')
t1b = Transition(state11, state10, alias = 't1b')
t1c = Transition(state10, state11, label_rel = 'f1', alias = 't1c')

t2a = Transition(state20, state21, label_oss = 'o1', alias = 't2a')
t2b = Transition(state21, state20, label_oss = 'o2', alias = 't2b')

t3a = Transition(state30, state31, alias = 't3a')
t3b = Transition(state31, state30, alias = 't3b')
t3c = Transition(state31, state31, label_rel = 'f3', alias = 't3c')

list_state_C1 = [state10, state11]
list_transition_C1 = [t1a, t1b, t1c]

C1 = FA(list_state_C1, list_transition_C1, initial_state = state10, actual_state = state10, alias = 'C1')

list_state_C2 = [state20, state21]
list_transition_C2 = [t2a, t2b]

C2 = FA(list_state_C2, list_transition_C2, initial_state = state20, actual_state = state20, alias = 'C2')

list_state_C3 = [state30, state31]
list_transition_C3 = [t3a, t3b, t3c]

C3 = FA(list_state_C3, list_transition_C3, initial_state = state30, actual_state = state30, alias = 'C3')

L1 = Link(C2.alias, C1.alias, alias = 'L1')
L2 = Link(C2.alias, C3.alias, alias = 'L2')
L3 = Link(C3.alias, C1.alias, alias = 'L3')

e1 = Event(alias = 'e1')
e2 = Event(alias = 'e2')
e3 = Event(alias = 'e3')

function_e1L1 = EventFunction(e1, L1)
function_e2L3 = EventFunction(e2, L3)
function_e3L2 = EventFunction(e3, L2)

t1a.input_event_func = function_e1L1
t1b.input_event_func = function_e2L3

t2a.output_events_func = [function_e1L1,function_e3L2]

t2b.output_events_func = [function_e1L1]

t3a.output_events_func = [function_e2L3]

t3b.input_event_func = function_e3L2

t3c.input_event_func = function_e3L2

net = Net([C1, C2, C3], [L1, L2, L3])

with open("net2.pickle", "wb") as f:
    pickle.dump(net, f)
