import pickle
import copy
import time
from memory_profiler import profile

from user_class import *
import extra_function as fn


#COMPITO 1

def generate_behavior_space(net):
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

    for node in list_space_nodes:
        print(node.id, node.alias)
    for route in list_routes:
        print("ROUTE: <" + str(route.start_node.id) + ":" + route.alias + ":" + str(route.finish_node.id)+ ">")

    return Behavior_Space(initial_node, list_space_nodes, list_routes)


#COMPITO 2
def generate_behavior_space_from_osservation(net, osservation):
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
                    node_to_add = fn.change_state(transition, FA_index, state_alias, net.list_link, node_temp, osservation)
                    if node_to_add is not None:
                        if not any(node_to_add := node for node in list_space_nodes if node.alias == node_to_add.alias and node.index_oss == node_to_add.index_oss):
                            #print(transition.label_oss)
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

    for node in list_space_nodes:
        print(node.id, node.alias, node.index_oss, node.final)
    for route in list_routes:
        print("ROUTE: <" + str(route.start_node.id) + ":" + route.alias + ":" + str(route.finish_node.id)+ ">", route.label_oss, route.label_rel)

    return Behavior_Space(initial_node, list_space_nodes, list_routes)

#COMPITO 3
def diagnosis_space(oss_space):
    oss_space_temp = copy.deepcopy(oss_space) # copia del spazio delle osservazioni utile come oggetto modificabile da parte di fn.reg_expr()
    reg_expr = fn.reg_expr(oss_space_temp)
    print(reg_expr)

#COMPITO 4
def generator_silence_closure(behavior_space, start_node):
    list_closure_nodes = []
    list_closure_routes = []
    list_output_routes = [] # can be remove
    tail_nodes = []

    if start_node not in behavior_space.list_nodes:
        print("Errore", start_node.id)
        return None

    
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
        print("x" + str(closure.id))
        for closure_node in closure.list_nodes:
            print("\t", closure_node.node.id, closure_node.node.final)
        for route in closure.list_routes:
            print("\t ROUTE: <" + str(route.start_node.id) + ":" + route.alias + ":" + str(route.finish_node.id)+ ">", route.label_rel)

        routes_closure = fn.reg_expr_closing(copy.deepcopy(closure))
        
        '''for route in routes_closure:
            print("\t FNROUTE: <" + str(route.start_node.id) + ":" + route.alias + ":" + str(route.finish_node.id)+ ">", route.label_rel)
        '''
        delta_set = set()
        save_delta = False
        for route in routes_closure:
            if route.rif_node.final:
                save_delta = True
                delta_set.add(route.label_rel)
            '''else:
                print("NON FINAL", route.label_rel, route.start_node.id)'''
            for route_out in state.list_routes:
                if route_out.start_node.id == route.rif_node.id and route_out.start_state.id == closure.id:
                    new_route = route_out
                    #new_route = copy.deepcopy(route_out)
                    new_label = ''
                    if route_out.label_rel ==  '\u03b5' and route.label_rel == '\u03b5':
                       new_label = '\u03b5'
                    elif route_out.label_rel ==  '\u03b5':
                        new_label = route.label_rel
                    elif route.label_rel ==  '\u03b5':
                        new_label = route_out.label_rel
                    else:
                        #print(route_out.alias, route.alias)
                        new_label = route.label_rel + route_out.label_rel
                    
                    new_route.label_rel = new_label
                    #list_routes_diagnostic.append(new_route)
                    print("\t ROUTEOUT: <" + str(new_route.start_node.id) + ":" + new_route.label_rel + ":" + str(new_route.finish_node.id)+ ">")
        
        
        if save_delta:
            delta = "|".join(delta_set)
            print('DELTA', delta)
            state.delta = delta
            closure.delta = delta

    diagnosticator_space = Diagnosticator_Space(initial_state, list_states)
    return closure_space, diagnosticator_space

def generator_closures_space(behavior_space):
    list_closures = []
    list_routes_diagnostic = []
    tail_closures = []

    initial_closure = generator_silence_closure(behavior_space, behavior_space.initial_node)
    initial_closure.id = 0
    
    list_closures.append(initial_closure)
    tail_closures.append(initial_closure)
    id = 1
    
    while tail_closures:
        closure = tail_closures[0]
        for output_routes in closure.list_output_routes:
            closure_to_add = next((closure_temp for closure_temp in list_closures if closure_temp.initial_node.node == output_routes.finish_node), None)
            if closure_to_add == None:
                
                closure_to_add = generator_silence_closure(behavior_space, output_routes.finish_node)
                closure_to_add.id = id

                id += 1
                list_closures.append(closure_to_add)
                tail_closures.append(closure_to_add)
        tail_closures.remove(closure)
    
    closure_space = Closure_Space(list_closures, list_routes_diagnostic)

    for closure in closure_space.list_closures:
        print("x" + str(closure.id))
        for closure_node in closure.list_nodes:
            print("\t", closure_node.node.id, closure_node.node.final)
        for route in closure.list_routes:
            print("\t ROUTE: <" + str(route.start_node.id) + ":" + route.alias + ":" + str(route.finish_node.id)+ ">", route.label_rel)

        routes_closure = fn.reg_expr_closing(copy.deepcopy(closure))
        
        delta_set = set()
        save_delta = False
        for route in routes_closure:
            if route.rif_node.final:
                save_delta = True
                delta_set.add(route.label_rel)
            for route_out in closure.list_output_routes:
                if route_out.start_node.id == route.rif_node.id:
                    new_route = route_out
                    #new_route = copy.deepcopy(route_out)
                    new_label = ''
                    if route_out.label_rel ==  '\u03b5' and route.label_rel == '\u03b5':
                       new_label = '\u03b5'
                    elif route_out.label_rel ==  '\u03b5':
                        new_label = route.label_rel
                    elif route.label_rel ==  '\u03b5':
                        new_label = route_out.label_rel
                    else:
                        #print(route_out.alias, route.alias)
                        new_label = route.label_rel + route_out.label_rel
                    
                    new_route.label_rel = new_label
                    #list_routes_diagnostic.append(new_route)
                    print("\t ROUTEOUT: <" + str(new_route.start_node.id) + ":" + new_route.label_rel + ":" + str(new_route.finish_node.id)+ ">")
        
        if save_delta:
            delta = "|".join(delta_set)
            print('DELTA', delta)
            closure.delta = delta
    
    return closure_space

def generator_diagnosticator(closure_space):
    list_closures = []
    list_states = []

    for closure in closure_space.closure_list:
        state = State_Diagnostic("x"+str(closure.id))
        state.id = closure.id
        list_states.append(state)
        state.delta = closure.delta

    for closure in closure_space.closure_list:
        for output_routes in closure.list_output_routes:
            new_route = Route_Diagnostic(output_routes)
            new_route.start_state = list_states[closure.id]
            
            search_closure_init_node_id = output_routes.finish_node.node.id
            for closure_temp in closure_space.closure_list:
                if closure_temp.initial_node.id == search_closure_init_node_id:
                    new_route.finish_state = list_states[closure_temp.id]
                    break
            state.list_routes.append(new_route)
    
    
    for state in list_states:
        print("STATE", state.id)
        for route in state.list_routes:
            print("\t ROUTE OUT: <" + str(route.start_state.id) + ":" + route.label_rel + ":" + str(route.finish_state.id)+ ">")
        if state.delta:
            print("DELTA", state.delta)
    diagnosticator_space = Diagnosticator_Space(list_states[0], list_states)
    return closure_space, diagnosticator_space



def steps(net=None, behavior_space=None, oss_space = None, closing_space = None, diagnosticator = None, gen_bs=True, gen_bs_from_o=False, diagnosis=False, gen_closing=False, gen_diagnosticator=False, linear_diagnostic=False, oss_list = None, oss_list2 = None):
    start_time = time.time()
    if net and gen_bs:
        print("Generation Behavior Space")
        behavior_space = generate_behavior_space(net)
        with open("behavior_space.pickle", "wb") as f:
            pickle.dump(behavior_space, f)
    
    if net and oss_list and gen_bs_from_o: 
        print("Generation Behavior Space from osservation")
        oss_space = generate_behavior_space_from_osservation(net, oss_list)
        with open("oss_space.pickle", "wb") as f:
            pickle.dump(oss_space, f)
    if oss_space and diagnosis:
        print("Generation diagnosis in osservation space")
        diagnosis_space(oss_space)
    
    if behavior_space and gen_closing and gen_diagnosticator:
        print("Generation Closing Space and Diagnosticator")
        closure_space, diagnosticator = generator_closures_space_and_diagnosticator(behavior_space)
        with open("closure_space.pickle", "wb") as f:
            pickle.dump(closure_space, f)  
        with open("diagnosticator_space.pickle", "wb") as f:
            pickle.dump(diagnosticator, f)  
    elif behavior_space and gen_closing:
        print("Generation Closing Space")
        closure_space = generator_closures_space(behavior_space)
        with open("closure_space.pickle", "wb") as f:
            pickle.dump(closure_space, f)  
    elif closing_space and gen_diagnosticator:
        print("Generation Diagnosticator")
        diagnosticator = generator_diagnosticator(closing_space)
        with open("diagnosticator_space.pickle", "wb") as f:
            pickle.dump(diagnosticator, f)  

           
    if diagnosticator and linear_diagnostic and oss_list2:
        print("Generation linear diagnostic")
        fn.linear_diagnostic(diagnosticator, oss_list2)
    print("--- %s seconds ---" % (time.time() - start_time))
      

def main():
    args = fn.parse_arguments()

    if args.step:
        
        if  args.step == 'gbo' and not args.ol:
            print('Error: -gbo and -ol must both be supplied or omitted')
            return 1
        elif args.step == 'do' and not args.ol2:
            print('Error: -do and -ol2 must both be supplied or omitted')
            return 1
        if args.step == 'all':
            
            if not args.ol or not args.ol2:
                print('Error: -ol and -ol2 must be supplied')
                return 1
            else:
                if not args.net:
                    print('Error: -net is required')
                    return 1 
                with open(args.net, "rb") as f:
                    doc = pickle.load(f)
                steps(net=doc, gen_bs=True, gen_bs_from_o=True, diagnosis=True, gen_closing=True, gen_diagnosticator=True, linear_diagnostic=True, oss_list=args.ol, oss_list2=args.ol2)
        elif args.step == 'gb':
            if not args.net:
                print('Error: -net is required')
                return 1
            else:
                with open(args.net, "rb") as f:
                    doc = pickle.load(f)
                steps(net=doc, gen_bs=True)
        elif args.step == 'go':
            if not args.ol:
                print('Error: -go and -ol must both be supplied or omitted')
                return 1
            if not args.net:
                print('Error: -net is required')
                return 1
            else:
                with open(args.net, "rb") as f:
                    doc = pickle.load(f)
                steps(net=doc, oss_list=args.ol, gen_bs_from_o=True)
        elif args.step == 'd':
            if not args.o:
                print('Error: -o is required')
                return 1
            else:
                with open(args.o, "rb") as f:
                    doc = pickle.load(f)
                steps(oss_space=doc, diagnosis=True)
        elif args.step == 'gcs':
            if not args.b:
                print('Error: -b is required')
                return 1
            else:
                with open(args.b, "rb") as f:
                    doc = pickle.load(f)
                steps(behavior_space=doc, gen_closing=True)
        elif args.step == 'gd':
            if not args.cs:
                print('Error: -cs is required')
                return 1
            else:
                with open(args.cs, "rb") as f:
                    doc = pickle.load(f)
                steps(closing_space=doc, gen_diagnosticator=True)
        elif args.step == 'do':
            if  not args.ol2:
                print('Error: -do and -ol must both be supplied or omitted')
                return 1
            if not args.dgn:
                print('Error: -dgn is required')
                return 1
            else:
                with open(args.dgn, "rb") as f:
                    doc = pickle.load(f)
                steps(diagnosticator=doc, oss_list2=args.ol2, linear_diagnostic=True)
    else:
        if not args.net:
            print('Error: -net is required')
            return 1 
        else:
            if not args.ol or not args.ol2:
                print('Error: -ol and -ol2 must be supplied')
                return 1
            else:
                with open(args.net, "rb") as f:
                    doc = pickle.load(f)
                steps(net=doc, gen_bs=True, gen_bs_from_o=True, diagnosis=True, gen_closing=True, gen_diagnosticator=True, linear_diagnostic=True, oss_list=args.ol, oss_list2=args.ol2)

    

    return 0


if __name__ == "__main__":
	try:
		ret_code = main()
		exit(ret_code)
	except KeyboardInterrupt:
		print("[#] CTRL-C, aborting...")
		exit(0)
	except Exception as e:
		print("[E] Exception", e)
		exit(-1)
