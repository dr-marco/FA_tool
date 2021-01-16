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
    reg_expr = fn.reg_expr(oss_space)
    print()

def main():
    with open("net.pickle", "rb") as f:
        net = pickle.load(f)
    #print("Generazione spazio comportamentale")
    #generate_behavior_space(net)
    print("Generazione spazio comportamentale da osservazione")
    oss_space = generate_behavior_space_from_osservation(net, ["o3", "o2"])

    diagnosis_space(oss_space)

if __name__ == "__main__":
    main()
