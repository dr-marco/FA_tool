import pickle
from user_class import *

state0s = State(alias = '0')
state1s = State(alias = '1')

state0b = State(alias = '0')
state1b = State(alias = '1')

s1 = Transition(state0s, state1s, label_oss = 'act', alias = 's1')
s2 = Transition(state1s, state0s, label_oss = 'sby', alias = 's2')
s3 = Transition(state0s, state0s, label_rel = 'f1', alias = 's3')
s4 = Transition(state1s, state1s, label_rel = 'f2', alias = 's4')

b1 = Transition(state0b, state1b, label_oss = 'opn', alias = 'b1')
b2 = Transition(state1b, state0b, label_oss = 'cls', alias = 'b2')
b3 = Transition(state0b, state0b, label_rel = 'f3', alias = 'b3')
b4 = Transition(state1b, state1b, label_rel = 'f4', alias = 'b4')
b5 = Transition(state0b, state0b, label_oss = 'nop', alias = 'b5')
b6 = Transition(state1b, state1b, label_oss = 'nop', alias = 'b6')
b7 = Transition(state0b, state1b, label_rel = 'f5', label_oss = 'opn', alias = 'b7')
b8 = Transition(state1b, state0b, label_rel = 'f6', label_oss = 'cls', alias = 'b8')



list_state_S = [state0s, state1s]
list_transition_S = [s1, s2, s3, s4]

S = FA(list_state_S, list_transition_S, initial_state = state0s, actual_state = state0s, alias = 'S')

list_state_B = [state0b, state1b]
list_transition_B = [b1, b2, b3, b4, b5, b6, b7, b8]

B = FA(list_state_B, list_transition_B, initial_state = state0b, actual_state = state0b, alias = 'B')


L = Link(S.alias, B.alias, alias = 'L')

op = Event(alias = 'op')
cl = Event(alias = 'cl')

function_opL = EventFunction(op, L)
function_clL = EventFunction(cl, L)

s1.output_events_func = [function_opL]
s2.output_events_func = [function_clL]
s3.output_events_func = [function_clL]
s4.output_events_func = [function_opL]

b1.input_event_func = function_opL
b2.input_event_func = function_clL
b3.input_event_func = function_opL
b4.input_event_func = function_clL
b5.input_event_func = function_clL
b6.input_event_func = function_opL
b7.input_event_func = function_clL
b8.input_event_func = function_opL



net = Net([S, B], [L])

with open("net_alt.pickle", "wb") as f:
    pickle.dump(net, f)
