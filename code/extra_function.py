from user_class import *
import copy
import random

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

def change_state(transition, index_FA, state_alias, list_link, node, osservation = None):
    new_list_values_link = node.list_values_link.copy()
    new_list_states_FA = node.list_states_FA.copy()
    index_oss = node.index_oss

    if osservation != None:
        if transition.label_oss in osservation and index_oss < len(osservation):
            if transition.label_oss != osservation[index_oss]:
                return None
            else:
                index_oss += 1
        else:
            if transition.label_oss != '\u03b5':
                return None

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

    return Node(list_states_FA = new_list_states_FA, list_values_link = new_list_values_link, index_oss = index_oss)

from operator import attrgetter
from itertools import groupby

def reg_expr(oss_space, multiple_output = False):
    list_routes = oss_space.list_routes
    list_nodes = oss_space.list_nodes
    initial_node = oss_space.initial_node
    if any(route for route in list_routes if route.finish_node == initial_node):
        place_holder_node = Node([],[])
        new_route = Route(place_holder_node, initial_node)
        list_routes.append(new_route)

        initial_node = place_holder_node
    final_node =  Node([],[])

    for node in list_nodes:
        if node.final:
            new_route = Route(node, final_node)
            list_routes.append(new_route)

    while len(list_routes) > 1:
        list_route_node_auto = []
        list_route_node_input = []
        list_route_node_output = []
        node = random.choice(list_nodes)

        for route in list_routes:
            if route.start_node == node and route.finish_node == node:
                list_route_node_auto.append(route)
            if route.start_node == node:
                list_route_node_output.append(route)
            if route.finish_node == node:
                list_route_node_input.append(route)

        #list_route_node_output.sort(key = attrgetter('finish_node'))
        if len(list_route_node_input) == 1 and len(list_route_node_output) == 1:
            route_in = list_route_node_input[0]
            route_out = list_route_node_output[0]
            new_route = Route(route_in.start_node, route_out.finish_node , label_rel = "(" + route_in.label_rel + route_out.label_rel + ")")
            list_routes.append(new_route)
            list_routes.remove(route_in)
            list_routes.remove(route_out)
            list_nodes.remove(node)
        elif len(list_route_node_output) > 1:
            groups = groupby(list_route_node_output, attrgetter('finish_node')) #o(n)
            for (key, data) in groups:
                routes = list(data)
                if len(routes) > 1:
                    new_labels_rel = []
                    for route in routes:
                        new_labels_rel.append(route.label_rel)
                        list_routes.remove(route)
                    new_label_rel = '|'.join(new_labels_rel)
                    new_route = Route(node, key, label_rel = "(" + new_label_rel + ")")
                    list_routes.append(new_route)
        else:
            if len(list_route_node_auto) > 0:
                for auto_route in list_route_node_auto:
                    for input_route in list_route_node_input:
                        input_route.label_rel += auto_route.label_rel + '*'
                    for output_route in list_route_node_output:
                        output_route.label_rel += auto_route.label_rel + '*'
                    list_routes.remove(auto_route)
            else:
                for output_route in list_route_node_output:
                    for input_route in list_route_node_input:
                        new_route = Route(input_route.start_node, output_route.finish_node, label_rel = "(" + input_route.label_rel + output_route.label_rel + ")")
                        list_routes.append(new_route)
                    list_routes.remove(output_route)

                for input_route in list_route_node_input:
                    list_routes.remove(input_route)
            list_nodes.remove(node)
    for e in list_routes:
        print(e.label_rel)
        #if for route in list_route_node_auto:
            # * trans
