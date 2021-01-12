import pickle
from user_class import *

state20 = State(alias = '20')
state21 = State(alias = '21')

state30 = State(alias = '30')
state31 = State(alias = '31')

t2a = Transition(state20, state21, label_oss = 'o2', alias = 't2a')
t2b = Transition(state21, state20, label_rel = 'r', alias = 't2b')

t3a = Transition(state30, state31, label_oss = 'o3', alias = 't3a')
t3b = Transition(state31, state30, alias = 't3b')
t3c = Transition(state31, state31, label_rel = 'f', alias = 't3c')


list_state_C2 = [state20, state21]
list_transition_C2 = [t2a, t2b]

C2 = FA(list_state_C2, list_transition_C2, initial_state = state20, actual_state = state20, alias = 'C2')

list_state_C3 = [state30, state31]
list_transition_C3 = [t3a, t3b, t3c]

C3 = FA(list_state_C3, list_transition_C3, initial_state = state30, actual_state = state30, alias = 'C3')


L2 = Link(C3.alias, C2.alias, alias = 'L2')
L3 = Link(C2.alias, C3.alias, alias = 'L3')

e2 = Event(alias = 'e2')
e3 = Event(alias = 'e3')

function_e2L2 = EventFunction(e2, L2)
function_e3L3 = EventFunction(e3, L3)

t2a.input_event_func = function_e2L2
t2a.output_events_func = [function_e3L3]

t2b.output_events_func = [function_e3L3]

t3a.output_events_func = [function_e2L2]


t3b.input_event_func = function_e3L3

t3c.input_event_func = function_e3L3

net = Net([C2, C3], [L2, L3])

with open("net.pickle", "wb") as f:
    pickle.dump(net, f)
