#creare una classe
import uuid 
class FA:
	def __init__(self, alias = '', list_states, list_trans, initial_state, actual_state):
		self.id = uuid.uuid1()
		self.alias = alias
		
		self.list_states = list_states
		self.list_trans = list_trans
		self.initial_state = initial_state
		self.actual_state = actual_state
		
class State:
	def __init__(self, alias = '', active = False, isFinal = False):
		self.id = uuid.uuid1()
		self.alias = alias
		
		self.active = active
		self.isFinal = isFinal
		
class Transitions:
	def __init__(self, alias = '', start_state, finish_state, input_event_func, output_events_func, label_oss, label_rel):
		self.id = uuid.uuid1()
		self.alias = alias
		
		self.start_state = start_state
		self.finish_state = finish_state
		self.input_event_func = input_event_func
		self.output_events_func = output_events_func
		self.label_oss = label_oss
		self.label_rel = label_rel
			
def EventFunction:
	def __init__(self, event, link):
		self.id = uuid.uuid1()
		
		self.event = event
		self.link = link
		
def Event:
	def __init__(self, alias = ''):
		self.id = uuid.uuid1()
		self.alias = alias
		
def Link:
	def __init__(self, alias = '', start_FA, finish_FA, value = ''):
		self.id = uuid.uuid1()
		self.alias = alias
		
		self.start_FA = start_FA
		self.finish_FA = finish_FA
		self.value = value
		
def Net:
	def __init__(self, alias = '', list_FA, list_link):
		self.id = uuid.uuid1()
		self.alias = alias
		
		self.list_FA = list_FA
		self.list_link = list_link
		
def Standard_Space:
	def __init__(self, initial_node, list_nodes, list_routes):
		self.id = uuid.uuid1()
		
		self.initial_node = initial_node
		self.list_nodes = list_nodes
		self.list_routes = list_routes
		
def Node:
	def __init__(self, alias = '', isFinal = False, list_status_link, list_status_FA, index_Oss = None):
		self.id = uuid.uuid1()
		self.alias = alias
		
		self.isFinal = isFinal
		self.list_status_link = list_status_link
		self.list_status_FA = list_status_FA
		self.index_Oss = index_Oss
		
def Route:
	def __init__(self, transition, start_node, finish_node):
		self.id = uuid.uuid1()
		
		self.transition = transition
		self.start_node = start_node
		self.finish_node = finish_node
		
def Closing_Node:
	def __init__(self, node, label):
		self.id = uuid.uuid1()

		self.node = node
		self.label = label

def Closing:
	def __init__(self, initial_node, list_nodes, list_routes, list_output_routes):
		self.id = uuid.uuid1()
		
		self.initial_node = initial_node
		self.list_nodes = list_nodes
		self.list_routes = list_routes
		self.list_output_routes = list_output_routes
		
