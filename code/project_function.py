from user_class import *
import pickle
import copy

with open("net.pickle", "rb") as f:
    net = pickle.load(f)

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
                    node_to_add = change_state(transition, FA_index, state_alias, net.list_link, node_temp)
                    if node_to_add is not None:

                        if not any(node_to_add := node for node in list_space_nodes if node.alias == node_to_add.alias):
                            list_space_nodes.append(node_to_add)
                            tail_nodes.append(node_to_add)
                            node_to_add.final = all(value == '' for value in node_to_add.list_values_link)

                        route_to_add = Route(transition, node_temp, node_to_add)
                        list_routes.append(route_to_add)

            FA_index += 1
        tail_nodes.remove(node_temp)

    list_final_nodes = [node for node in list_space_nodes if node.final == True]
    bad_nodes = set(list_space_nodes)
    for node in list_final_nodes:
        bad_nodes = BFS(list_routes, bad_nodes, node)

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
        print("ROUTE: <" + str(route.start_node.id) + ":" + route.transition.alias + ":" + str(route.finish_node.id)+ ">")

    return Behavior_Space(initial_node, list_space_nodes, list_routes)
    
def change_state(transition, index_FA, state_alias, list_link, node):
    new_list_values_link = node.list_values_link.copy()
    new_list_states_FA = node.list_states_FA.copy()

    func = transition.input_event_func
    if func is not None:
        func_link = func.link
        func_event = func.event
        index_link = list_link.index(func_link)
        if new_list_values_link[index_link] != func_event.alias:
            return None
        else:
            new_list_values_link[index_link] = ''

    funcs = transition.output_events_func
    for func in funcs:
        func_link = func.link
        func_event = func.event

        index_link = list_link.index(func_link)
        if new_list_values_link[index_link] != '':
            return None
        else:
            new_list_values_link[index_link] = func_event.alias

    new_state_alias = transition.finish_state.alias
    new_list_states_FA[index_FA] = new_state_alias

    return Node(list_states_FA = new_list_states_FA, list_values_link = new_list_values_link)


def BFS(list_routes, list_space_nodes, final_node):
    grey = []
    good_nodes = set([])

    grey.append(final_node)

    q = []
    q.append(final_node)

    while q:
        node = q.pop(0)
        for route in list_routes:
            if route.finish_node == node:
                if route.start_node not in grey and route.start_node not in good_nodes:
                    q.append(route.start_node)
                    grey.append(route.start_node)
        good_nodes.add(node)
        grey.remove(node)

    return list_space_nodes - good_nodes



generate_behavior_space(net)
