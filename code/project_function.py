import pickle
import copy
import time
from memory_profiler import profile

from user_class import *
import extra_function as fn

import jsonpickle
import os
import sys


text_to_file = ""

#COMPITO 1
def generate_behavior_space(net):
	global text_to_file
	list_space_nodes = []
	list_routes = []
	tail_nodes = []

	list_states_FA = []
	list_values_link = []

	for FA in net.list_FA:
		list_states_FA.append(FA.initial_state.alias)

	for link in net.list_link:
		list_values_link.append(link.buffer)

	initial_node = Node(list_states_FA = list_states_FA, list_values_link = list_values_link)
	initial_node.final = True

	list_space_nodes.append(initial_node)
	tail_nodes.append(initial_node)
	#id = 1
	while tail_nodes:
		node_temp = tail_nodes[0]
		#print("node in uso", node_temp.id, "alias", node_temp.alias)
		FA_index = 0

		for state_alias in node_temp.list_states_FA:
			FA = net.list_FA[FA_index]
			for transition in FA.list_trans:
				if transition.start_state.alias == state_alias:
					node_to_add = fn.change_state(transition, FA_index, state_alias, net.list_link, node_temp)
					if node_to_add is not None:
						if not any(node_to_add := node for node in list_space_nodes if node.alias == node_to_add.alias):
							#node_to_add.id = id
							#id = id +1
							#print("\t nodo in aggiunta", node_to_add.id)
							list_space_nodes.append(node_to_add)
							tail_nodes.append(node_to_add)
							node_to_add.final = all(value == '' for value in node_to_add.list_values_link)
						route_to_add = Route(node_temp, node_to_add, alias = transition.alias, label_oss = transition.label_oss, label_rel = transition.label_rel)
						#print("\t ROUTE: aggiunta", route_to_add.finish_node.id, "alias", route_to_add.finish_node.alias, route_to_add.alias)
						list_routes.append(route_to_add)

			FA_index += 1
		tail_nodes.remove(node_temp)

	list_final_nodes = [node for node in list_space_nodes if node.final == True]
	bad_nodes = set(list_space_nodes)
	for node in list_final_nodes:
		bad_nodes = fn.BFS(list_routes, bad_nodes, node)

	for node in bad_nodes:
		list_space_nodes.remove(node)

	for route in list_routes:
		if route.start_node not in list_space_nodes or route.finish_node not in list_space_nodes:
			list_routes.remove(route)

	id = 0
	for node in list_space_nodes:
		node.id = id
		id = id + 1
	
	text_to_file += "\t" + str(len(list_space_nodes)) + " Nodes\n"
	for node in list_space_nodes:
		text_to_file += "\t ID: " + str(node.id) + " ALIAS: " + node.alias + "\n"
	text_to_file += "\t" + str(len(list_routes)) + " Routes\n"
	for route in list_routes:
		text_to_file += "\tROUTE: <" + str(route.start_node.id) + ":" + route.alias + ":" + str(route.finish_node.id)+ "> with oss: " + route.label_oss + " and rel:" + route.label_rel + "\n"
	
	return Behavior_Space(initial_node, list_space_nodes, list_routes)


#COMPITO 2
def generate_behavior_space_from_osservation(net, osservation):
	global text_to_file
	list_space_nodes = []
	list_routes = []
	tail_nodes = []

	list_states_FA = []
	list_values_link = []

	for FA in net.list_FA:
		list_states_FA.append(FA.initial_state.alias)

	for link in net.list_link:
		list_values_link.append(link.buffer)

	initial_node = Node(list_states_FA = list_states_FA, list_values_link = list_values_link)
	initial_node.index_oss = 0

	list_space_nodes.append(initial_node)
	tail_nodes.append(initial_node)

	while tail_nodes:
		node_temp = tail_nodes[0]
		FA_index = 0

		for state_alias in node_temp.list_states_FA:
			FA = net.list_FA[FA_index]
			for transition in FA.list_trans:
				if transition.start_state.alias == state_alias:
					#print(osservation)
					node_to_add = fn.change_state(transition, FA_index, state_alias, net.list_link, node_temp, osservation)
					if node_to_add is not None:
						if not any(node_to_add := node for node in list_space_nodes if node.alias == node_to_add.alias and node.index_oss == node_to_add.index_oss):
							#print(transition.alias)
							#print(node_to_add.alias)
							list_space_nodes.append(node_to_add)
							tail_nodes.append(node_to_add)
							node_to_add.final = all(value == '' for value in node_to_add.list_values_link) and node_to_add.index_oss == len(osservation)
							#print("nodo da aggiungere",node_to_add.final)
						route_to_add = Route(node_temp, node_to_add, alias = transition.alias, label_oss = transition.label_oss, label_rel = transition.label_rel)
						list_routes.append(route_to_add)

			FA_index += 1
		tail_nodes.remove(node_temp)

	list_final_nodes = [node for node in list_space_nodes if node.final == True]
	bad_nodes = set(list_space_nodes)
	for node in list_final_nodes:
		bad_nodes = fn.BFS(list_routes, bad_nodes, node)

	for node in bad_nodes:
		list_space_nodes.remove(node)

	for route in list_routes:
		if route.start_node not in list_space_nodes or route.finish_node not in list_space_nodes:
			list_routes.remove(route)

	id = 0
	for node in list_space_nodes:
		node.id = id
		id = id + 1

	text_to_file += "\t" + str(len(list_space_nodes)) + " Nodes\n"
	for node in list_space_nodes:
		text_to_file += "\t ID: " + str(node.id) + " ALIAS: " + node.alias + " and OSS.INDEX: " + str(node.index_oss) + "\n"
	text_to_file += "\t" + str(len(list_routes)) + " Routes\n"
	for route in list_routes:
		text_to_file += "\tROUTE: <" + str(route.start_node.id) + ":" + route.alias + ":" + str(route.finish_node.id)+ "> with oss: " + route.label_oss + " and rel:" + route.label_rel + "\n"
	return Behavior_Space(initial_node, list_space_nodes, list_routes)

#COMPITO 3
def diagnosis_space(oss_space):
	global text_to_file
	oss_space_temp = copy.deepcopy(oss_space) # copia del spazio delle osservazioni utile come oggetto modificabile da parte di fn.reg_expr()
	reg_expr = fn.reg_expr(oss_space_temp)
	text_to_file += "\t" + reg_expr + "\n"
	return reg_expr
#COMPITO 4

def generator_silence_closure(behavior_space, start_node):
	list_closure_nodes = []
	list_closure_routes = []
	list_output_routes = [] # can be remove
	tail_nodes = []

	if start_node not in behavior_space.list_nodes:
		raise Exception("ERROR the stard node is not in behavior space's list nodes")

	
	initial_node = Closure_Node(start_node)
	list_closure_nodes.append(initial_node)
	tail_nodes.append(initial_node)

	while tail_nodes:
		closure_node = tail_nodes[0]
		for route in behavior_space.list_routes:
			if route.start_node.id == closure_node.node.id:
				if route.label_oss == '\u03b5':
					clousure_node_temp = Closure_Node(route.finish_node)
					list_closure_routes.append(route)
					not_to_add = False
					for clousure_node in list_closure_nodes:
						if clousure_node_temp.node.id == clousure_node.node.id:
							not_to_add = True
							break
					
					if not not_to_add:
						list_closure_nodes.append(clousure_node_temp)
						tail_nodes.append(clousure_node_temp)
					
				else:
					list_output_routes.append(route)
		tail_nodes.remove(closure_node)
	
	closure = Closure(initial_node, list_closure_nodes, list_closure_routes,list_output_routes)
	return closure

def generator_closures_space_and_diagnosticator(behavior_space):
	global text_to_file
	list_closures = []
	list_routes_diagnostic = []
	list_states = []
	tail_closures = []

	initial_closure = generator_silence_closure(behavior_space, behavior_space.initial_node)
	initial_closure.id = 0
	
	initial_state = State_Diagnostic("x0")
	initial_state.id = 0
	list_states.append(initial_state)
	list_closures.append(initial_closure)
	tail_closures.append(initial_closure)
	id = 1
	
	while tail_closures:
		closure = tail_closures[0]
		state_temp = list_states[closure.id]
		for output_routes in closure.list_output_routes:
			closure_to_add = next((closure_temp for closure_temp in list_closures if closure_temp.initial_node.node == output_routes.finish_node), None)
			if closure_to_add == None:
				
				closure_to_add = generator_silence_closure(behavior_space, output_routes.finish_node)
				closure_to_add.id = id

				state = State_Diagnostic("x"+str(id))
				state.id = id
				state.list_routes = []
				list_states.append(state)

				id += 1
				list_closures.append(closure_to_add)
				tail_closures.append(closure_to_add)

				new_route = Route_Diagnostic(output_routes)
				new_route.start_state = state_temp
				new_route.finish_state = state
			else:
				new_route = Route_Diagnostic(output_routes)
				new_route.start_state = state_temp
				new_route.finish_state = list_states[closure_to_add.id]
			state_temp.list_routes.append(new_route)
		tail_closures.remove(closure)
	closure_space = Closure_Space(list_closures, list_routes_diagnostic) 

	for closure in closure_space.list_closures:
		state = list_states[closure.id]
		text_to_file += "\t x" + str(closure.id) + "\n"
		for closure_node in closure.list_nodes:
			text_to_file += "\t\t ID: " + str(closure_node.node.id) + "\n"
		for route in closure.list_routes:
			text_to_file += "\t\t ROUTE: <" + str(route.start_node.id) + ":" + route.alias + ":" + str(route.finish_node.id)+ "> with rel: " + route.label_rel + "\n"
		routes_closure = fn.reg_expr_closing(copy.deepcopy(closure))
		
		delta_set = set()
		save_delta = False
		for route in routes_closure:
			if route.rif_node.final:
				save_delta = True
				delta_set.add(route.label_rel)
			for route_out in state.list_routes:
				if route_out.start_node.id == route.rif_node.id and route_out.start_state.id == closure.id:
					new_route = route_out
					new_label, set_label = fn.clear_label(route_out.label_rel, route.label_rel, set_label1=route_out.set_label_rel, set_label2=route.set_label_rel )
				
					'''new_label = ''
					if route_out.label_rel ==  '\u03b5' and route.label_rel == '\u03b5':
					   new_label = '\u03b5'
					elif route_out.label_rel ==  '\u03b5':
						new_label = route.label_rel
					elif route.label_rel ==  '\u03b5':
						new_label = route_out.label_rel
					else:
						#print(route_out.alias, route.alias)
						new_label = route.label_rel + route_out.label_rel'''
					
					new_route.label_rel = new_label
					new_route.set_label_rel = set_label
					text_to_file += "\t\t ROUTEOUT: <" + str(new_route.start_node.id) + ":" + new_route.label_rel + ":" + str(new_route.finish_node.id)+ "> with rel: " + new_route.label_rel + "\n"
		
		
		if save_delta:
			delta = "|".join(delta_set)
			text_to_file += '\t\t DELTA: ' + delta + "\n"
			state.delta = delta
			closure.delta = delta
	text_to_file += "Generation Diagnosticator\n"
	diagnosticator_space = Diagnosticator_Space(initial_state, list_states)
	for state in list_states:
		text_to_file += "\t STATE: " + str(state.id) + "\n"
		for route in state.list_routes:
			text_to_file += "\t\t ROUTE OUT: <" + str(route.start_node.id) + ":" + route.alias + ":" + str(route.finish_node.id)+ "> with rel: " + route.label_rel + "\n"
		if state.delta:
			text_to_file += '\t\t DELTA: ' + state.delta + "\n"
	diagnosticator_space = Diagnosticator_Space(list_states[0], list_states)
	return closure_space, diagnosticator_space

def generator_closures_space(behavior_space):
	global text_to_file
	list_closures = []
	list_routes_diagnostic = []
	list_states = []
	tail_closures = []

	initial_closure = generator_silence_closure(behavior_space, behavior_space.initial_node)
	initial_closure.id = 0
	
	initial_state = State_Diagnostic("x0")
	initial_state.id = 0
	list_states.append(initial_state)
	list_closures.append(initial_closure)
	tail_closures.append(initial_closure)
	id = 1
	
	while tail_closures:
		closure = tail_closures[0]
		state_temp = list_states[closure.id]
		for output_routes in closure.list_output_routes:
			closure_to_add = next((closure_temp for closure_temp in list_closures if closure_temp.initial_node.node == output_routes.finish_node), None)
			if closure_to_add == None:
				
				closure_to_add = generator_silence_closure(behavior_space, output_routes.finish_node)
				closure_to_add.id = id

				state = State_Diagnostic("x"+str(id))
				state.id = id
				state.list_routes = []
				list_states.append(state)

				id += 1
				list_closures.append(closure_to_add)
				tail_closures.append(closure_to_add)

				new_route = Route_Diagnostic(output_routes)
				new_route.start_state = state_temp
				new_route.finish_state = state
			else:
				new_route = Route_Diagnostic(output_routes)
				new_route.start_state = state_temp
				new_route.finish_state = list_states[closure_to_add.id]
			state_temp.list_routes.append(new_route)
		tail_closures.remove(closure)
	closure_space = Closure_Space(list_closures, list_routes_diagnostic) 

	for closure in closure_space.list_closures:
		state = list_states[closure.id]
		text_to_file += "\t x" + str(closure.id) + "\n"
		for closure_node in closure.list_nodes:
			text_to_file += "\t\t ID: " + str(closure_node.node.id) + "\n"
		for route in closure.list_routes:
			text_to_file += "\t\t ROUTE: <" + str(route.start_node.id) + ":" + route.alias + ":" + str(route.finish_node.id)+ "> with rel: " + route.label_rel + "\n"
		routes_closure = fn.reg_expr_closing(copy.deepcopy(closure))
		
		delta_set = set()
		save_delta = False
		for route in routes_closure:
			if route.rif_node.final:
				save_delta = True
				delta_set.add(route.label_rel)
			for route_out in state.list_routes:
				if route_out.start_node.id == route.rif_node.id and route_out.start_state.id == closure.id:
					new_route = route_out
					new_label, set_label = fn.clear_label(route_out.label_rel, route.label_rel, set_label1=route_out.set_label_rel, set_label2=route.set_label_rel )
					'''new_label = ''
					if route_out.label_rel ==  '\u03b5' and route.label_rel == '\u03b5':
					   new_label = '\u03b5'
					elif route_out.label_rel ==  '\u03b5':
						new_label = route.label_rel
					elif route.label_rel ==  '\u03b5':
						new_label = route_out.label_rel
					else:
						#print(route_out.alias, route.alias)
						new_label = route.label_rel + route_out.label_rel'''
					
					new_route.label_rel = new_label
					new_route.set_label_rel = set_label
					text_to_file += "\t\t ROUTEOUT: <" + str(new_route.start_node.id) + ":" + new_route.label_rel + ":" + str(new_route.finish_node.id)+ "> with rel: " + new_route.label_rel + "\n"
		
		
		if save_delta:
			delta = "|".join(delta_set)
			text_to_file += '\t\t DELTA: ' + delta + "\n"
			state.delta = delta
			closure.delta = delta
	text_to_file += "Generation Diagnosticator\n"
	diagnosticator_space = Diagnosticator_Space(initial_state, list_states)
	for state in list_states:
		text_to_file += "\t STATE: " + str(state.id) + "\n"
		for route in state.list_routes:
			text_to_file += "\t\t ROUTE OUT: <" + str(route.start_node.id) + ":" + route.alias + ":" + str(route.finish_node.id)+ "> with rel: " + new_route.label_rel + "\n"
		if state.delta:
			text_to_file += '\t\t DELTA: ' + state.delta + "\n"
	for i in range(0, len(list_states)):
		closure_space.list_closures[i].list_output_routes =  list_states[i].list_routes
	return closure_space

def generator_diagnosticator(closure_space):
	global text_to_file
	list_closures = []
	list_states = []
	
	for closure in closure_space.list_closures:
		state = State_Diagnostic("x"+str(closure.id), list_routes=[])
		state.id = closure.id
		list_states.append(state)
		state.delta = closure.delta
	
	for closure in closure_space.list_closures:
		for output_routes in closure.list_output_routes:
			#print(closure.id, output_routes.label_rel, output_routes.label_oss)
			
			new_route = Route_Diagnostic(output_routes)
			new_route.start_state = list_states[closure.id]
			
			search_closure_init_node_id = output_routes.finish_node.id
			for closure_temp in closure_space.list_closures:
				if closure_temp.initial_node.node.id == search_closure_init_node_id:
					new_route.finish_state = list_states[closure_temp.id]
					break
			list_states[closure.id].list_routes.append(new_route)
			
	
	text_to_file += "Generation Diagnosticator\n"
	diagnosticator_space = Diagnosticator_Space(list_states[0], list_states)
	for state in list_states:
		text_to_file += "\t STATE: " + str(state.id) + "\n"
		for route in state.list_routes:
			text_to_file += "\t\t ROUTE OUT: <" + str(route.start_node.id) + ":" + route.alias + ":" + str(route.finish_node.id)+ "> with rel: " + new_route.label_rel + "\n"
		if state.delta:
			text_to_file += '\t\t DELTA: ' + state.delta + "\n"
	for i in range(0, len(list_states)):
		closure_space.list_closures[i].list_output_routes =  list_states[i].list_routes
	return diagnosticator_space

def benchmark(net, oss_list, oss_list2):
	start_time = time.time()
	behavior_space = generate_behavior_space(net)
	print("--- %s seconds ---" % (time.time() - start_time))
	
	start_time_temp = time.time()
	oss_space = generate_behavior_space_from_osservation(net, oss_list)
	print("--- %s seconds ---" % (time.time() - start_time_temp))
	
	start_time_temp = time.time()
	reg_expr = diagnosis_space(oss_space)
	#print(reg_expr)
	print("--- %s seconds ---" % (time.time() - start_time_temp))
	
	start_time_temp = time.time()
	#closure_space, diagnosticator = generator_closures_space_and_diagnosticator(copy.deepcopy(behavior_space))
	closure_space = generator_closures_space(behavior_space)
	print("--- %s seconds ---" % (time.time() - start_time_temp))
	
	start_time_temp = time.time()
	diagnosticator = generator_diagnosticator(closure_space)
	print("--- %s seconds ---" % (time.time() - start_time_temp))
	
	start_time_temp = time.time()
	labels = fn.linear_diagnostic(diagnosticator, oss_list2)
	print("--- %s seconds ---" % (time.time() - start_time_temp))

	print("--- %s seconds ---" % (time.time() - start_time))
	#print(text_to_file)


def steps(net=None, behavior_space=None, oss_space = None, closing_space = None, diagnosticator = None, gen_bs=True, gen_bs_from_o=False, diagnosis=False, gen_closing=False, gen_diagnosticator=False, linear_diagnostic=False, oss_list = None, oss_list2 = None):
	global text_to_file
	start_time = time.time()
	if net and gen_bs:
		text_to_file += "Generation Behavior Space\n"
		behavior_space = generate_behavior_space(net)

		behavior_space_json = jsonpickle.encode(behavior_space)
		with open("behavior_space.json", "w") as f:
			f.write(behavior_space_json)
	
	if net and oss_list and gen_bs_from_o: 
		text_to_file += "Generation Behavior Space from osservation\n"
		oss_space = generate_behavior_space_from_osservation(net, oss_list)

		oss_space_json = jsonpickle.encode(oss_space)
		with open("oss_space.json", "w") as f:
			f.write(oss_space_json)
	if oss_space and diagnosis:
		text_to_file += "Generation diagnosis in osservation space\n"
		reg_expr = diagnosis_space(oss_space)
		with open("diagnosis.txt", "w") as f:
			f.write(reg_expr)
	
	if behavior_space and gen_closing and gen_diagnosticator:
		text_to_file += "Generation Closing Space\n"
		closure_space, diagnosticator = generator_closures_space_and_diagnosticator(behavior_space)
		
		closure_space_json = jsonpickle.encode(closure_space)
		with open("closure_space.json", "w") as f:
			f.write(closure_space_json)
		
		diagnosticator_json = jsonpickle.encode(diagnosticator)
		with open("diagnosticator.json", "w") as f:
			f.write(diagnosticator_json)
	elif behavior_space and gen_closing:
		text_to_file += "Generation Closing Space\n"
		closure_space = generator_closures_space(behavior_space)

		closure_space_json = jsonpickle.encode(closure_space)
		with open("closure_space.json", "w") as f:
			f.write(closure_space_json)
	elif closing_space and gen_diagnosticator:
		text_to_file += "Generation Diagnosticator\n"
		diagnosticator = generator_diagnosticator(closing_space)
		
		diagnosticator_json = jsonpickle.encode(diagnosticator)
		with open("diagnosticator.json", "w") as f:
			f.write(diagnosticator_json)

		   
	if diagnosticator and linear_diagnostic and oss_list2:
		text_to_file += "Generation linear diagnostic\n"
		labels = fn.linear_diagnostic(diagnosticator, oss_list2)
		for label in labels:

			text_to_file += "\t" + label + "\n"
		with open("linear_diagnostic.txt", "w") as f:
			for label in labels:
				f.write(label + "\n")
	
	text_to_file += "--- %s seconds ---" % (time.time() - start_time)
	#print("--- %s seconds ---" % (time.time() - start_time))

	print(text_to_file)

def main():
	global text_to_file
	args = fn.parse_arguments()
	if args.bk:
		if not args.net:
			raise Exception("[Error] -net is required")
			return 1
		else:
			doc = fn.json_to_obj(args.net)
			'''with open('../pickle/net3.pickle', 'rb') as f:
				doc = pickle.load(f)'''
			#steps(net=doc, gen_bs=True, gen_bs_from_o=True, diagnosis=True, gen_closing=True, gen_diagnosticator=True, linear_diagnostic=True, oss_list=args.ol, oss_list2=args.ol2)
			benchmark(doc, oss_list=args.ol, oss_list2=args.ol2)
			return 0
	if args.step:
		
		if  args.step == 'gbo' and not args.ol:
			raise Exception("[Error] -gbo and -ol must both be supplied or omitted")
		elif args.step == 'do' and not args.ol2:
			raise Exception("[Error] -do and -ol2 must both be supplied or omitted")
		if args.step == 'all':
			
			if not args.ol or not args.ol2:
				raise Exception("[Error] -ol and -ol2 must be supplied")
			else:
				if not args.net:
					raise Exception("[Error] -net is required")
				doc = fn.json_to_obj(args.net)
				text_to_file += fn.format_net_to_text(doc,text_to_file)
				steps(net=doc, gen_bs=True, gen_bs_from_o=True, diagnosis=True, gen_closing=True, gen_diagnosticator=True, linear_diagnostic=True, oss_list=args.ol, oss_list2=args.ol2)
		elif args.step == 'gb':
			if not args.net:
				raise Exception("[Error] -net is required")
			else:
				doc = fn.json_to_obj(args.net)
				text_to_file += fn.format_net_to_text(doc,text_to_file)
				steps(net=doc, gen_bs=True)
		elif args.step == 'go':
			if not args.ol:
				raise Exception("[Error] -go and -ol must both be supplied or omitted")
			if not args.net:
				raise Exception("[Error] -net is required")
			else:
				doc = fn.json_to_obj(args.net)
				text_to_file += fn.format_net_to_text(doc,text_to_file)
				steps(net=doc, oss_list=args.ol, gen_bs_from_o=True)
		elif args.step == 'd':
			if not args.o:
				raise Exception("[Error] -o is required")
			else:
				with open(args.o, "r") as f:
					doc = jsonpickle.decode(f.read())
				steps(oss_space=doc, diagnosis=True)
		elif args.step == 'gcs':
			if not args.b:
				raise Exception("[Error] -b is required")
			else:
				with open(args.b, "r") as f:
					doc = jsonpickle.decode(f.read())
				steps(behavior_space=doc, gen_closing=True)
		elif args.step == 'gd':
			if not args.cs:
				raise Exception("[Error] -cs is required")
			else:
				with open(args.cs, "r") as f:
					doc = jsonpickle.decode(f.read())
				steps(closing_space=doc, gen_diagnosticator=True)
		elif args.step == 'do':
			if  not args.ol2:
				raise Exception("[Error] -do and -ol must both be supplied or omitted")
			if not args.dgn:
				raise Exception("[Error] -dgn is required")
			else:
				with open(args.dgn, "r") as f:
					doc = jsonpickle.decode(f.read())
				steps(diagnosticator=doc, oss_list2=args.ol2, linear_diagnostic=True)
	else:
		if not args.net:
			raise Exception("[Error] -net is required")
		else:
			if not args.ol or not args.ol2:
				raise Exception("[Error] -ol and -ol2 must be supplied")
			else:
				doc = fn.json_to_obj(args.net)
				text_to_file += fn.format_net_to_text(doc,text_to_file)
				steps(net=doc, gen_bs=True, gen_bs_from_o=True, diagnosis=True, gen_closing=True, gen_diagnosticator=True, linear_diagnostic=True, oss_list=args.ol, oss_list2=args.ol2)

	return 0

import traceback
if __name__ == "__main__":
	try:
		ret_code = main()
		with open("summary.txt", "w") as f:
			f.write(text_to_file)
		
		exit(ret_code)
	except KeyboardInterrupt:
		print("[#] CTRL-C, aborting...")
		with open("summary.txt", "w") as f:
			f.write(text_to_file)
		exit(0)
	except Exception as e:
		
		traceback.format_exc()
		print("[E] Exception", e)
		print("\t LINE: ", traceback.format_exc())
		exit(-1)
