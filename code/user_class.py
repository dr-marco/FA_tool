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
	def __init__(self, start_state, finish_state, input_event_func = None, output_events_func = [], label_oss = '\u03b5', label_rel = '\u03b5', alias = ''):
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

class Behavior_Space:
	def __init__(self, initial_node, list_nodes, list_routes):
		self.initial_node = initial_node
		self.list_nodes = list_nodes
		self.list_routes = list_routes

class Node:
	def __init__(self, list_states_FA, list_values_link, alias = '', id = 0, final = False, index_oss = 0):
		self.alias = ':'.join(list_states_FA) + '|' + ':'.join(list_values_link)
		self.id  = id

		self.final = final
		self.list_states_FA = list_states_FA
		self.list_values_link = list_values_link
		self.index_oss = index_oss

class Route:
	def __init__(self, start_node, finish_node, alias = '', label_oss = '\u03b5', label_rel = '\u03b5'):
		self.alias = alias

		self.start_node = start_node
		self.finish_node = finish_node
		self.label_oss = label_oss #TODO nel caso la togliamo
		self.label_rel = label_rel #TODO nel caso la togliamo
		
		#per regex
		self.set_label_rel = {label_rel}
		self.rif_node = None

class Route_Diagnostic(Route):
	def __init__(self, parent):
		super().__init__(parent.start_node, parent.finish_node, parent.alias, parent.label_oss, parent.label_rel)
		self.start_state = None
		self.finish_state = None

class Closure_Node:
	def __init__(self, node, label = ""):
		self.node = node
		self.label = label

class Closure:
	def __init__(self, initial_node, list_nodes, list_routes, list_output_routes, id = 0):
		self.id = id
		
		self.initial_node = initial_node
		self.list_nodes = list_nodes
		self.list_routes = list_routes
		self.list_output_routes = list_output_routes
		
		self.delta = ''
		self.list_diagnostic_output_route = []

class Closure_Space:
	def __init__(self, list_closures, list_routes):
		self.list_closures = list_closures
		self.list_routes = list_routes

class State_Diagnostic:
	def __init__(self, alias, list_routes = [], delta = '', id = 0):
		self.id = id
		self.alias = alias
		self.delta = delta
		self.list_routes = list_routes

class Diagnosticator_Space:
	def __init__(self, initial_state, list_states):
		self.list_states = list_states
		self.initial_state = initial_state
