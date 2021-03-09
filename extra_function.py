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

def reg_expr(oss_space):

    list_routes = oss_space.list_routes
    list_nodes = oss_space.list_nodes
    initial_node = oss_space.initial_node

    if len(list_nodes) == 0:
        print("No nodes")
        return ''

    list_nodes.remove(initial_node)

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

    while len(list_nodes) > 0:
        list_route_node_auto = []
        list_route_node_input = []
        list_route_node_output = []
        node = random.choice(list_nodes)
        print(node.id)
        
        for route in list_routes:
            if route.start_node == node and route.finish_node == node:
                list_route_node_auto.append(route)
            if route.start_node == node and route.finish_node != node:
                list_route_node_output.append(route) 
            if route.finish_node == node and route.start_node != node:
                list_route_node_input.append(route)
        
        if len(list_route_node_output) > 1:
                
            groups = groupby(list_route_node_output, attrgetter('finish_node')) #o(n)
            for (key, data) in groups:
                routes = list(data)
                if len(routes) > 1: 
                    new_labels_rel = set()
                    for route in routes:
                        if len(route.label_rel) > 2:
                            if route.label_rel[0] == '(' and route.label_rel[-1] == ')' and route.label_rel[-2]!='*':
                                route.label_rel = route.label_rel[1:-1]
                        #print(route.label_rel)
                        new_labels_rel.add(route.label_rel)
                        list_routes.remove(route)
                        list_route_node_output.remove(route)
                    
                    new_label_rel = '|'.join(new_labels_rel)
                    #print(new_label_rel)
                    new_route = Route(node, key, label_rel = "(" + new_label_rel + ")")
                    new_route.set_label_rel = new_labels_rel
                    list_routes.append(new_route)
                    list_route_node_output.append(new_route)

        if len(list_route_node_input) == 1 and len(list_route_node_output) == 1 and len(list_route_node_auto) == 0:
            route_in = list_route_node_input[0]
            route_out = list_route_node_output[0]

            new_label, set_label = clear_label(route_in.label_rel, route_out.label_rel, set_label1=route_in.set_label_rel, set_label2=route_out.set_label_rel)
            
            new_route = Route(route_in.start_node, route_out.finish_node , label_rel = new_label)
            new_route.set_label_rel = set_label
            
            list_routes.append(new_route)
            
            list_routes.remove(route_in)
            list_routes.remove(route_out)
            list_route_node_input.remove(route_in)
            list_route_node_output.remove(route_out)

        
                    
        if len(list_route_node_auto) > 0:
            for auto_route in list_route_node_auto:
                
                for input_route in list_route_node_input:
                    for output_route in list_route_node_output:
                        new_label, set_label = clear_label(input_route.label_rel, output_route.label_rel, autolabel=auto_route.label_rel, set_label1=input_route.set_label_rel, set_label2=output_route.set_label_rel, set_auto=auto_route.set_label_rel)
                        new_route = Route(input_route.start_node, output_route.finish_node, label_rel = new_label)  
                        #print("entrato", auto_route.label_rel)
                        new_route.set_label_rel = set_label
                        #print("uscito", new_route.label_rel)
                        list_routes.append(new_route)
                    list_routes.remove(input_route)   
                list_routes.remove(auto_route)

            for output_route in list_route_node_output:
                list_routes.remove(output_route)

        else:
            for input_route in list_route_node_input:
                for output_route in list_route_node_output:
                    new_label, set_label = clear_label(input_route.label_rel, output_route.label_rel, set_label1=input_route.set_label_rel, set_label2=output_route.set_label_rel)
                    new_route = Route(input_route.start_node, output_route.finish_node, label_rel = new_label)
                    new_route.set_label_rel = set_label
                    list_routes.append(new_route)
                list_routes.remove(input_route)

            for output_route in list_route_node_output:
                list_routes.remove(output_route)
        list_nodes.remove(node)
        '''for route in list_routes:
            print("ROUTE",route.start_node.id, route.finish_node.id)
        '''
    final_labels = set()
    for route in list_routes:
        #new_labels_rel = set()
        if len(route.label_rel) > 2:
            if route.label_rel[0] == '(' and route.label_rel[-1] == ')' and route.label_rel[-2]!='*':
                route.label_rel = route.label_rel[1:-1]
        if len(route.set_label_rel) > 1:
            list_label = route.label_rel.split("|")
            for label in list_label:
                final_labels.add(label)
            '''for label in route.set_label_rel:
                final_labels.add(label)'''
        else:
            final_labels.add(route.label_rel)
    
    final_label = '|'.join(final_labels)
    #new_route = Route(node, key, label_rel = final_label)
        
    return final_label #return regular expression

def reg_expr_closing(closing_space):
    list_routes = closing_space.list_routes
    list_nodes = [node.node for node in closing_space.list_nodes]
    initial_node = closing_space.initial_node
    list_output_routes = closing_space.list_output_routes
    list_final_output_nodes = []
    list_output_nodes = []
    #list_final_routes = []
    list_nodes_not_final = []
    ex_initial_node_id = -2
    
    if len(list_nodes) == 1:
        new_route = Route(initial_node.node, initial_node.node)
        new_route.label_rel = '\u03b5'
        new_route.rif_node = initial_node.node 
        return [new_route]  

    
    if any(route for route in list_routes if route.finish_node.id == initial_node.node.id):
        place_holder_node = Node([],[])
        new_route = Route(place_holder_node, initial_node.node)
        list_routes.append(new_route)
        list_nodes_not_final.append(place_holder_node)
        ex_initial_node_id = initial_node.node.id
        initial_node.node = place_holder_node
        place_holder_node.id = -1
    
    final_node =  Node([],[])
    final_node.id = -99

    
    for node in list_nodes:
        if node.final:
            list_final_output_nodes.append(node)
            new_route = Route(node, final_node)
            list_routes.append(new_route)
        else:
            list_nodes_not_final.append(node)

    for route in list_output_routes:
        if not route.start_node.final:
            if not route.start_node in list_output_nodes:
                list_output_nodes.append(route.start_node)
                list_final_output_nodes.append(route.start_node)
                new_route = Route(route.start_node, final_node)
                list_routes.append(new_route)
                list_nodes_not_final.remove(route.start_node)

    number_expr_nodes = len(list_final_output_nodes)
    #print(initial_node.node.id)
    if initial_node.node in list_nodes_not_final:
        list_nodes_not_final.remove(initial_node.node)

    while len(list_nodes_not_final) > 0:
        list_route_node_auto = []
        list_route_node_input = []
        list_route_node_output = []
        node = random.choice(list_nodes_not_final)
        
        for route in list_routes:
            if route.start_node == node and route.finish_node == node:
                list_route_node_auto.append(route)
            if route.start_node == node and route.finish_node != node:
                list_route_node_output.append(route) 
            if route.finish_node == node and route.start_node != node:
                list_route_node_input.append(route)
        
        if len(list_route_node_output) > 1:      
            groups = groupby(list_route_node_output, attrgetter('finish_node')) #o(n)
            for (key, data) in groups:
                routes = list(data)
                if len(routes) > 1:
                    new_labels_rel = set()
                    for route in routes:
                        if len(route.label_rel) > 2:
                            if route.label_rel[0] == '(' and route.label_rel[-1] == ')':
                                route.label_rel = route.label_rel[1:-1]
                        new_labels_rel.add(route.label_rel)
                        list_routes.remove(route)
                        list_route_node_output.remove(route)
                    
                    new_label_rel = '|'.join(new_labels_rel)
                    new_route = Route(node, key, label_rel = "(" + new_label_rel + ")")
                    new_route.set_label_rel = new_labels_rel
                    list_routes.append(new_route)
                    list_route_node_output.append(new_route)


        if len(list_route_node_input) == 1 and len(list_route_node_output) == 1 and len(list_route_node_auto) == 0:
            route_in = list_route_node_input[0]
            route_out = list_route_node_output[0]

            new_label, set_label = clear_label(route_in.label_rel, route_out.label_rel, set_label1=route_in.set_label_rel, set_label2=route_out.set_label_rel)
            
            new_route = Route(route_in.start_node, route_out.finish_node , label_rel = new_label)
            new_route.set_label_rel = set_label
            
            list_routes.append(new_route)

            list_routes.remove(route_in)
            list_routes.remove(route_out)
            list_route_node_input.remove(route_in)
            list_route_node_output.remove(route_out)

        
                    
        if len(list_route_node_auto) > 0:
            for auto_route in list_route_node_auto:
                for input_route in list_route_node_input:
                    for output_route in list_route_node_output:
                        new_label, set_label = clear_label(input_route.label_rel, output_route.label_rel, autolabel=auto_route.label_rel, set_label1=input_route.set_label_rel, set_label2=output_route.set_label_rel, set_auto=auto_route.set_label_rel)
                        new_route = Route(input_route.start_node, output_route.finish_node, label_rel = new_label)  
                        
                        new_route.set_label_rel = set_label
                        list_routes.append(new_route)
                    list_routes.remove(input_route)   
                list_routes.remove(auto_route)
                    
            for output_route in list_route_node_output:
                list_routes.remove(output_route)
        else:
            for input_route in list_route_node_input:
                for output_route in list_route_node_output:
                    new_label, set_label = clear_label(input_route.label_rel, output_route.label_rel, set_label1=input_route.set_label_rel, set_label2=output_route.set_label_rel)
                    new_route = Route(input_route.start_node, output_route.finish_node, label_rel = new_label)
                    new_route.set_label_rel = set_label
                    list_routes.append(new_route)
                list_routes.remove(input_route)

            for output_route in list_route_node_output:
                list_routes.remove(output_route)
        list_nodes_not_final.remove(node)
    
    #### QUA####
    
    while len(list_final_output_nodes) > 0:
        list_route_node_auto = []
        list_route_node_input = []
        list_route_node_output = []
        node = random.choice(list_final_output_nodes)
        #print("node id", node.id)
        '''for route in list_routes:
            print("route", route.start_node.id, route.finish_node.id, route.label_rel)
        '''
        for route in list_routes:
            if route.start_node == node and route.finish_node == node:
                list_route_node_auto.append(route)
            if route.start_node == node and route.finish_node != node:
                list_route_node_output.append(route) 
            if route.finish_node == node and route.start_node != node:
                list_route_node_input.append(route)
        

        if len(list_route_node_input) == 1 and len(list_route_node_output) == 1 and len(list_route_node_auto) == 0:
            route_in = list_route_node_input[0]
            route_out = list_route_node_output[0]
            new_label, set_label = clear_label(route_in.label_rel, route_out.label_rel, set_label1=route_in.set_label_rel, set_label2=route_out.set_label_rel)
            
            new_route = Route(route_in.start_node, route_out.finish_node , label_rel = new_label)
            new_route.set_label_rel = set_label
            
            if route_out.rif_node != None:
                new_route.rif_node = route_out.rif_node
            elif route_out.finish_node == final_node:
                new_route.rif_node = node
            
            list_routes.append(new_route)
            
            list_routes.remove(route_in)
            list_routes.remove(route_out)
            list_route_node_input.remove(route_in)
            list_route_node_output.remove(route_out)
                    
        if len(list_route_node_auto) > 0:
            remove = False
            for auto_route in list_route_node_auto:
                for input_route in list_route_node_input:
                    remove = True
                    for output_route in list_route_node_output:
                        new_label, set_label = clear_label(input_route.label_rel, output_route.label_rel, autolabel=auto_route.label_rel, set_label1=input_route.set_label_rel, set_label2=output_route.set_label_rel, set_auto=auto_route.set_label_rel)
                        new_route = Route(input_route.start_node, output_route.finish_node, label_rel = new_label)  
                        
                        new_route.set_label_rel = set_label
                        list_routes.append(new_route)
                        if output_route.rif_node != None:
                            new_route.rif_node = output_route.rif_node
                        elif output_route.finish_node == final_node:
                            new_route.rif_node = node
                    list_routes.remove(input_route)   
                list_routes.remove(auto_route)

            
            if remove:
                for output_route in list_route_node_output:
                    list_routes.remove(output_route)

            if len(list_route_node_input) == 0:
                for output_route in list_route_node_output:                 
                    if output_route.rif_node != None:
                        output_route.rif_node = output_route.rif_node
                    elif output_route.finish_node == final_node:
                        output_route.rif_node = node         
        else:
            #print("cacca", len(list_routes), len(list_route_node_input), len(list_route_node_output))
            remove = False
            for input_route in list_route_node_input:
                remove = True
                #print("qua", input_route.label_rel)
                for output_route in list_route_node_output:
                    if input_route.start_node.id == -1 and output_route.finish_node.id == -99:
                        #print("rimosso")
                        continue
                    new_label, set_label = clear_label(input_route.label_rel, output_route.label_rel, set_label1=input_route.set_label_rel, set_label2=output_route.set_label_rel)
                    new_route = Route(input_route.start_node, output_route.finish_node, label_rel = new_label)
                    new_route.set_label_rel = set_label
                    #print("nuova rotta", new_route.label_rel, new_route.start_node.id, new_route.finish_node.id)
                    list_routes.append(new_route)
                    
                    if output_route.rif_node != None:
                        new_route.rif_node = output_route.rif_node
                    elif output_route.finish_node == final_node:
                        new_route.rif_node = node
                list_routes.remove(input_route)
            if remove:
                for output_route in list_route_node_output:
                    list_routes.remove(output_route)

            if len(list_route_node_input) == 0:
                for output_route in list_route_node_output:                 
                    if output_route.rif_node != None:
                        output_route.rif_node = output_route.rif_node
                    elif output_route.finish_node == final_node:
                        output_route.rif_node = node
        list_final_output_nodes.remove(node)

    return list_routes

def clear_label(label1, label2, autolabel = None, set_label1 = None, set_label2 = None, set_auto = None):
    new_label = ''
    new_label_set = {new_label}
    #print("clear_label", label1, label2, set_label1, set_label2, autolabel, set_auto)
    if autolabel and autolabel != '\u03b5':
        #print("autolabel", autolabel, "merda", set_auto)
        autolabel = "(" + autolabel + ")"
        autolabel, set_auto = clear_label(autolabel, '*', set_label1={autolabel}, set_label2={'*'})
    if label1 ==  '\u03b5' and label2 == '\u03b5':
        if autolabel:
            if autolabel == '\u03b5':
                new_label = '\u03b5'
            else:
                new_label = autolabel
                new_label_set = set_auto
        else:
            new_label = '\u03b5'
            new_label_set = {new_label}
    elif label1 ==  '\u03b5':
        if autolabel:
            if autolabel == '\u03b5':
                new_label = label2
                new_label_set = set_label2
            else:
                new_label, new_label_set = clear_label(autolabel, label2, set_label1=set_auto, set_label2=set_label2)
        else:
            new_label = label2
            new_label_set = set_label2
    elif label2 ==  '\u03b5':
        if autolabel:
            if autolabel == '\u03b5':
                new_label = label1
                new_label_set = set_label1
            else:
                new_label, new_label_set = clear_label(label1, autolabel, set_label1=set_label1, set_label2=set_auto)
        else:
            new_label = label1
            new_label_set = set_label1
    else:
        if autolabel:
            if autolabel == '\u03b5':
                new_label, new_label_set = clear_label(label1, label2, set_label1=set_label1, set_label2=set_label2)
            else:
                new_label, new_label_set = clear_label(label1, autolabel, set_label1=set_label1, set_label2=set_auto)
                new_label, new_label_set = clear_label(new_label, label2, set_label1=new_label_set, set_label2=set_label2)
        elif set_label1:
            labels = set()
            #new_label_set = set()
            for label_temp in set_label1:
                for label_temp2 in set_label2:
                    new_label_temp, new_label_set_temp  = clear_label(label_temp, label_temp2)
                    labels.add(new_label_temp)
            
            new_label = '|'.join(labels)
            new_label_set = labels
            #print("sono qua",new_label, "merda", new_label_set)
            
        else:
            
            new_label = label1 + label2
            new_label_set = {label1, label2}
            
    #print("sono qua",new_label, new_label_set )
    return new_label, new_label_set

def linear_diagnostic(diagnosticator_space, osservation):
    X = set()
    X.add((diagnosticator_space.initial_state.id,'\u03b5'))
    X_final = set()
    X_final.update(X)
    list_states = diagnosticator_space.list_states
    for o in osservation:
        Xnew = set()
        #print("osservazione", o)
        for (state_id, p) in X:
            groups = groupby(list_states[state_id].list_routes, attrgetter('finish_state')) #o(n)
            #print("STATO", state_id, list_states[state_id].delta)
            for (key, data) in groups:
                routes = list(data)
                for route in routes:
                    if route.label_oss == o:
                        new_p, temp = clear_label(p, route.label_rel)
                        add = True
                        
                        for e_tuple_temp in Xnew:
                            if e_tuple_temp[0] == route.finish_state.id and sorted(e_tuple_temp[1]) != sorted(new_p):
                                #c'è un errore
                                lst = list(e_tuple_temp)
                                #print("stato aggiunto", route.finish_state.id, e_tuple_temp[1])
                                add = False
                                lst[1] = e_tuple_temp[1] + '|' + new_p
                                e_tuple_temp = tuple(lst)
                                break
                        if add:
                            #print("stato aggiunto", route.finish_state.id)
                            Xnew.add((route.finish_state.id, new_p))
        X = copy.deepcopy(Xnew)
        X_final.update(Xnew)
    final_diagnosis = []
    for e in Xnew:
        state = list_states[e[0]]
        if state.delta != '':
            list_delta = set(state.delta.split('|'))
            label, temp = clear_label(e[1], state.delta, set_label1={e[1]}, set_label2=list_delta)
            print(label)



    

    

