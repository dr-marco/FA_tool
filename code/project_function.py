import pickle
import copy

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

    while tail_nodes:
        node_temp = tail_nodes[0]

        FA_index = 0

        for state_alias in node_temp.list_states_FA:
            FA = net.list_FA[FA_index]
            for transition in FA.list_trans:
                if transition.start_state.alias == state_alias:
                    node_to_add = fn.change_state(transition, FA_index, state_alias, net.list_link, node_temp)
                    if node_to_add is not None:

                        if not any(node_to_add := node for node in list_space_nodes if node.alias == node_to_add.alias):
                            list_space_nodes.append(node_to_add)
                            tail_nodes.append(node_to_add)
                            node_to_add.final = all(value == '' for value in node_to_add.list_values_link)

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
                            list_space_nodes.append(node_to_add)
                            tail_nodes.append(node_to_add)
                            node_to_add.final = all(value == '' for value in node_to_add.list_values_link) and node_to_add.index_oss == len(osservation)

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
        print("ROUTE: <" + str(route.start_node.id) + ":" + route.alias + ":" + str(route.finish_node.id)+ ">")

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

                    if clousure_node_temp not in list_closure_nodes:
                        list_closure_nodes.append(clousure_node_temp)
                        tail_nodes.append(clousure_node_temp)
                    
                else:
                    list_output_routes.append(route)
        tail_nodes.remove(closure_node)
    
    closure = Closure(initial_node, list_closure_nodes, list_closure_routes,list_output_routes)
    return closure

def generator_closures_space(behavior_space):
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
            print("\t", closure_node.node.id)
        for route in closure.list_routes:
            print("\t ROUTE: <" + str(route.start_node.id) + ":" + route.alias + ":" + str(route.finish_node.id)+ ">")

        routes_closure = fn.reg_expr_closing(copy.deepcopy(closure))
        delta = ''
        save_delta = False
        
        for route in routes_closure:
            if route.rif_node.final:
                save_delta = True
            delta += route.label_rel + '|'
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
                        new_label = route_out.label_rel + route.label_rel
                    
                    new_route.label_rel = new_label
                    #list_routes_diagnostic.append(new_route)
                    print("\t ROUTEOUT: <" + str(new_route.start_node.id) + ":" + new_route.label_rel + ":" + str(new_route.finish_node.id)+ ">")
        
        delta = delta[:-1]
        if save_delta:
            print('DELTA', delta)
            state.delta = delta

    for state in list_states:
        print(state.alias, state.delta)
        for route in state.list_routes:
            print(route.label_rel, route.start_state.alias, route.finish_state.alias)
    
    diagnosticator_space = Diagnosticator_Space(initial_state, list_states)
    return closure_space, diagnosticator_space

import time
def main():
    
    start_time = time.time()
    with open("net.pickle", "rb") as f:
        net = pickle.load(f)
    print("Generazione spazio comportamentale")
    behavior_space = generate_behavior_space(net)
    print("Generazione spazio comportamentale da osservazione")
    oss_space = generate_behavior_space_from_osservation(net, ["o3", "o2"])
    diagnosis_space(oss_space)
    closure_space, diagnosticator_space = generator_closures_space(behavior_space)
    fn.linear_diagnostic(diagnosticator_space, ["o3", "o2", "o3", "o2"])
    
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
