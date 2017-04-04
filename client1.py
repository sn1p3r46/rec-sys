#!/usr/bin/python3

# https://pypi.python.org/pypi/websocket-client
import websocket
import wsHelper as wsh
import json
import igraph as ig
import pickle as pkl


selected_knowbase = None
know_base_dic = {}


def add_node_type(node_type):

    know_base_dic[selected_knowbase]["node_types"].add(node_type)  
    print (selected_knowbase)

    return 'Node type added:' + node_type


def add_relation_type(relation_type):

    know_base_dic[selected_knowbase]["relation_types"].add(relation_type)  
    print (selected_knowbase)

    return 'Relation type added:' + relation_type


def add_node(node_str):

    node = json.loads(node_str)

    if node["type"] in know_base_dic[selected_knowbase]["node_types"]:

        know_base_dic[selected_knowbase]["graph"].add_vertex(**node)    
        return "Node added"

    return "Unknown node type"


def add_relation(relation_str):

    g = know_base_dic[selected_knowbase]["graph"]
    relation = json.loads(relation_str)

    if relation["type"] in know_base_dic[selected_knowbase]["relation_types"]:

        v0 = g.vs.find(**{"id":relation.pop("fromId")})
        v1 = g.vs.find(**{"id":relation.pop("toId")})
        g.add_edge(v0,v1,**relation)

        return "Relation added"

    return "Unknown relation type"


def get_node_types():
    return "Node types:" + wsh.format_set_to_arr_str(know_base_dic[selected_knowbase]["node_types"])


def get_node_count():
    return "Node count:" + str(len(know_base_dic[selected_knowbase]["graph"].vs))


def get_relation_types():
    return "Relation types:" + wsh.format_set_to_arr_str(know_base_dic[selected_knowbase]["relation_types"])


def get_relation_count():
    return "Relation count:" + str(len(know_base_dic[selected_knowbase]["graph"].es))


add_commands = {

    'Add node type' : add_node_type,
    'Add relation type' : add_relation_type,
    'Add node' : add_node,
    'Add relation' : add_relation,

}


get_commands = {

    'Get node types' : get_node_types,
    'Get relation types' : get_relation_types,
    'Get node count' : get_node_count,
    'Get relation count' : get_relation_count

}


def handle_knowbase(message):

    global selected_knowbase

    if selected_knowbase and not know_base_dic[selected_knowbase]["persisted"]:       

        db_file = open (selected_knowbase + "_graph.pkl", "wb")
        pkl.dump(know_base_dic[selected_knowbase]["graph"], db_file)
        db_file.close()
        know_base_dic[selected_knowbase]["persisted"] = True

    selected_knowbase = message.split(":")[1].strip()

    if selected_knowbase == '':
        raise ValueError(wsh.INVALID_KBASE)

    if selected_knowbase in know_base_dic:
        return "Knowledge base has been selected"

    else:

        try:

            db_file = open(selected_knowbase + "_graph.pkl", "rb")
            pkl.load(file=db_file)
            db_file.close()
            know_base_dic[selected_knowbase] = {
                    "node_types" : set(db_file.vs["type"]),
                    "relation_types" : set(db_file.es["type"]),
                    "graph" : db_file,
                    "persisted" : True 
                }

            return "Knowledge base has been selected"

        except FileNotFoundError:

            know_base_dic[selected_knowbase] = { 
                    "node_types" : set(), 
                    "relation_types" : set(),
                    "graph" : ig.Graph(),
                    "persisted" : False
                }

            return "Knowledge base has been created" 


def handle_message(ws,message):
    
    global my_log_file
    my_log_file.write(message + "\n")
     
    print ("Received message: " + message)

    if message in wsh.AUTH_DIC:
        res = message + ":" + wsh.AUTH_DIC[message]

    elif message.startswith("Select knowledge base:"):
        res = handle_knowbase(message)
        
    elif message.split(':',1)[0] in add_commands:
        splitted = message.split(':',1)
        res = add_commands[splitted[0]] (splitted[1])

    elif message in get_commands:
        res = get_commands[message]()

    else:

        print ("Unexpected Message: " + message)
        print (know_base_dic)

        my_log_file.close()

        if selected_knowbase != None:

            gfile = open(selected_knowbase+"_graph.pkl", 'wb')
            pkl.dump(know_base_dic[selected_knowbase]["graph"],gfile)
            gfile.close()

        print ("file closed")
        exit()

    wsh.send(ws,res)


my_log_file = open('myfile.dc', 'w')


def main():

    ws = websocket.WebSocket()
    ws.connect(wsh.END_POINT)


    print ("CONNECTED to " + wsh.END_POINT)
    #i = 0 

    while (True):
        handle_message(ws,ws.recv())
        #i+=1

    ws.close()
    print("WebSocket closed\nexit\n")


if __name__ == "__main__":
    main()
