#!/usr/bin/python3


# https://pypi.python.org/pypi/websocket-client
import websocket
import json

import wsHelper as wsh
import igraph as ig


selected_kb = None
kb_dic = {}


def add_node_type(node_type):

    kb_dic[selected_kb]["node_types"].add(node_type)
    print (selected_kb)

    return wsh.N_T_A + node_type


def add_relation_type(relation_type):

    kb_dic[selected_kb]["relation_types"].add(relation_type)
    print (selected_kb)

    return wsh.R_T_A +  relation_type


def add_node(node_str):

    node = json.loads(node_str)

    if node["type"] in kb_dic[selected_kb]["node_types"]:

        kb_dic[selected_kb]["graph"].add_vertex(**node)
        return wsh.N_ADDED 

    return wsh.UNK_N_T 


def add_relation(relation_str):

    g = kb_dic[selected_kb]["graph"]
    relation = json.loads(relation_str)

    if relation["type"] in kb_dic[selected_kb]["relation_types"]:

        v0 = g.vs.find(**{"id" : relation.pop("fromId")}).index
        v1 = g.vs.find(**{"id" : relation.pop("toId")}).index
        g.add_edge(v0,v1,**relation)

        return wsh.R_ADDED
    print ("----------------------------------------\n" + relation["type"])
    exit()
    return wsh.UNK_R_T

def get_node_types():
    return wsh.N_TYPES + wsh.fmt_arr_str(kb_dic[selected_kb]["node_types"])


def get_node_count():
    return wsh.N_COUNT + str(len(kb_dic[selected_kb]["graph"].vs))


def get_relation_types():
    return wsh.R_TYPES + wsh.fmt_arr_str(kb_dic[selected_kb]["relation_types"])


def get_relation_count():
    return wsh.R_COUNT + str(len(kb_dic[selected_kb]["graph"].es))

def get_engines():
    return "Engines:" +  json.dumps(wsh.engines)


par_cmds = {

    'Add node type' : add_node_type,
    'Add relation type' : add_relation_type,
    'Add node' : add_node,
    'Add relation' : add_relation,

}


get_cmds = {

    'Get node types' : get_node_types,
    'Get relation types' : get_relation_types,
    'Get node count' : get_node_count,
    'Get relation count' : get_relation_count,
    'Get engines' : get_engines

}

"""
recommender = { 

    'Get rating estimation:' : rs.get_rating_estimation,
    'Recommendations:' : rs.get_recommendations

}
"""

def handle_knowbase(msg):

    global selected_kb

    if selected_kb and not kb_dic[selected_kb]["persisted"]:
        if wsh.persist(kb_dic[selected_kb]["graph"],selected_kb + "_graph.pkl"):
            kb_dic[selected_kb]["persisted"] = True

    selected_kb = msg.split(":")[1].strip()

    if selected_kb == '':
        raise ValueError(wsh.INV_KB)

    if selected_kb in kb_dic:
        return wsh.KB_SELECTED

    else:

        graph = wsh.load(selected_kb + "_graph.pkl")

        if graph:

            kb_dic[selected_kb] = {
                        "node_types" : set(graph.vs["type"]),
                        "relation_types" : set(graph.es["type"]),
                        "graph" : graph,
                        "persisted" : True
                    }
            
            return wsh.KB_SELECTED

        else:

            kb_dic[selected_kb] = {
                        "node_types" : set(),
                        "relation_types" : set(),
                        "graph" : ig.Graph(),
                        "persisted" : False
                    }           
            
            return wsh.KB_CREATED


def handle_message(ws,msg):

    global my_log_file
    my_log_file.write(msg + "\n")

    print ("Received message: " + msg)

    if msg in wsh.AUTH_DIC:
        res = msg + ":" + wsh.AUTH_DIC[msg]

    elif msg.startswith(wsh.SELECT_KB):
        res = handle_knowbase(msg)

    elif msg.split(':',1)[0] in par_cmds:
        splitted = msg.split(':',1)
        res = par_cmds[splitted[0]] (splitted[1])

    elif msg in get_cmds:
        res = get_cmds[msg]()

#    elif msg.split(':',1)[0] in recommender:
#        splitted = msg.split(':',1)
#        res = recommender[splitted[0]] (splitted[1], kb_dic[selected_kb])

    else:

        print ("Unexpected Message: " + msg)
        print (kb_dic)

        my_log_file.close()
        wsh.persist(kb_dic[selected_kb]["graph"], selected_kb + "_graph.pkl")
        print ("file closed")
        exit()

    wsh.send(ws,res)


my_log_file = open('myfile.dc', 'w')


def main():

    ws = websocket.WebSocket()
    ws.connect(wsh.END_POINT)

    print ("CONNECTED to " + wsh.END_POINT)

    while (True):
        handle_message(ws, ws.recv())

    ws.close()
    print("WebSocket closed\nexit\n")


if __name__ == "__main__":
    main()
