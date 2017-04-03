#!/usr/bin/python3

# https://pypi.python.org/pypi/websocket-client
import websocket
import wsHelper as wsh
import json
import igraph as ig

selected_knowbase = None
know_base_dic = {}


def add_node_type(node_type):
    global know_base_dic
    know_base_dic[selected_knowbase]["node_types"].add(node_type)  
    print (selected_knowbase)
    return 'Node type added:' + node_type

def add_relation_type(relation_type):
    global know_base_dic
    know_base_dic[selected_knowbase]["relation_types"].add(relation_type)  
    print (selected_knowbase)
    return 'Relation type added:' + relation_type

def add_node(node_str):
    node = json.loads(node_str)
    if node["type"] in know_base_dic[selected_knowbase]["node_types"]:
        know_base_dic[selected_knowbase]["graph"].add_vertex(**node)    
        return "Node added"
    return "Unknown node type"

def add_relation():
    g = know_base_dic[selected_knowbase]["graph"]
    v0 = g.find(**{"id":node.pop("fromId")})
    v1 = g.find(**{"id":node.pop("toId")})
    g.add_relation(v0,v1,**node)

def get_node_types():
    return "Node types:" + wsh.format_set_to_arr_str(know_base_dic[selected_knowbase]["node_types"])

def get_node_count():
    return len(know_base_dic[selected_knowbase]["graph"].vs)

def get_relation_types():
    return "Relation types:" + wsh.format_set_to_arr_str(know_base_dic[selected_knowbase]["relation_types"])

def handle_knowbase(message):

    global selected_knowbase
    selected_knowbase = message.split(":")[1].strip()

    if selected_knowbase == '':
        raise ValueError(wsh.INVALID_KBASE)
        
    if selected_knowbase in know_base_dic:
        # TODO populate the knbase dic on startup
        return "Knowledge base has been selected"

    else:
        know_base_dic[selected_knowbase] = { 
                "node_types" : set(), 
                "relation_types" : set(),
                "graph" : ig.Graph()
            }
        return "Knowledge base has been created" 



add_commands = {

    'Add node type' : add_node_type,
    'Add relation type' : add_relation_type,
    'Add node' : add_node,
    'Add relation' : add_relation,

}

get_commands = {

    'Get node types' : get_node_types,
    'Get relation types' : get_relation_types,
    'Get node count' : get_node_count

}

myfile = open('myfile.dc', 'w')

def handle_message(ws,message):
    
    global myfile
    myfile.write(message + "\n")
     
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
        myfile.close()
        print ("file closed")
        exit()

    wsh.send(ws,res)

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
