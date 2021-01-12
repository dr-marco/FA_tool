#creare una classe
import uuid

class FA:
	def __init__(self, list_states, list_trans, initial_state, actual_state, alias = ''):
		self.alias = alias

		self.list_states = list_states
		self.list_trans = list_trans
		self.initial_state = initial_state
		self.actual_state = actual_state

class State:
	def __init__(self,  alias = '', active = False, isFinal = False):
		self.alias = alias

		self.active = active  #TODO nel caso togliamo
		self.isFinal = isFinal

class Transition:
	def __init__(self, start_state, finish_state, input_event_func = None, output_events_func = [], label_oss = '', label_rel = '', alias = ''):
		self.alias = alias

		self.start_state = start_state
		self.finish_state = finish_state
		self.input_event_func = input_event_func
		self.output_events_func = output_events_func
		self.label_oss = label_oss
		self.label_rel = label_rel

class EventFunction:
	def __init__(self, event, link):
		self.event = event
		self.link = link

class Event:
	def __init__(self, alias = ''):
		self.alias = alias

class Link:
	def __init__(self, start_FA, finish_FA, alias = '', buffer = ''):
		self.alias = alias

		self.start_FA = start_FA
		self.finish_FA = finish_FA
		self.buffer = buffer

class Net:
	def __init__(self, list_FA, list_link):
		self.list_FA = list_FA
		self.list_link = list_link

class Standard_Space:
	def __init__(self, initial_node, list_nodes, list_routes):
		self.initial_node = initial_node
		self.list_nodes = list_nodes
		self.list_routes = list_routes

class Node:
	def __init__(self, list_states_FA, list_values_link, alias = '', id = 0, final = False, index_Oss = 0):
		self.alias = ':'.join(list_states_FA) + '|' + ':'.join(list_values_link)
		self.id  = id

		self.final = final
		self.list_states_FA = list_states_FA
		self.list_values_link = list_values_link
		self.index_Oss = index_Oss

class Route:
	def __init__(self, transition, start_node, finish_node, label = ''):
		self.transition = transition
		self.start_node = start_node
		self.finish_node = finish_node
		self.label = label #TODO nel caso la togliamo

class Closure_Node:
	def __init__(self, node, label):
		self.node = node
		self.label = label

class Closure:
	def __init__(self, initial_node, list_nodes, list_routes, list_output_routes):
		self.initial_node = initial_node
		self.list_nodes = list_nodes
		self.list_routes = list_routes
		self.list_output_routes = list_output_routes
