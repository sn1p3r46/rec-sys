#!/usr/bin/python3

import pickle as pkl

END_POINT               = "ws://service.recommender-system.com/recsys2-course/engine"

RELATION_COUNT          = R_COUNT       = "Relation count:"
RELATION_ADDED          = R_ADDED       = "Relation added"
RELATION_TYPES          = R_TYPES       = "Relation types:"
REL_TYPE_ADDED          = R_T_A         = "Relation type added:"
UNKNOWN_RELATION_TYPE   = UNK_R_T       = "Unknown relation type"

NODE_COUNT              = N_COUNT       = "Node count:"
NODE_ADDED              = N_ADDED       = "Node added"
NODE_TYPES              = N_TYPES       = "Node types:"
NODE_TYPE_ADDED         = N_T_A         = "Node type added:"
UNKNOWN_NODE_TYPE       = UNK_N_T       = "Unknown node type"


INVALID_KBASE           = INV_KB        = "Received Invalid Knowledge Base"
SELECT_KNOWLEDGE_BASE   = SELECT_KB     = "Select knowledge base:"
KNOWLEDGE_BASE_CREATED  = KB_CREATED    = "Knowledge base has been created"
KNOWLEDGE_BASE_SELECTED = KB_SELECTED   = "Knowledge base has been selected" 


AUTH_DIC = {

    'Author name'       : 'Andrea Galloni', 
    'Author email'      : 'andreagalloni[92][at]gmail[dot]com',
    'Author id'         : 'JGNBMW',
    'Token'             : '4lvos7hd1a',

}


engines = [
    
    { "name" : "Item_average", "providesRatingEstimations" : True },
    { "name" : "User_average", "providesRatingEstimations" : True }
    
    ]


def persist(obj,fpath):
    try:
        with open(fpath,"wb") as fobj:
            pkl.dump(obj,fobj)
            return True
    
    except:
        print("Error while persisting.")
        return False


def load(fpath):
    try:
        with open(fpath,"rb") as fobj:
            return pkl.load(fobj)
    except:
        print("Errors while loading.")
        return None 


def send(ws,msg):
    print ("Sending: \"" + msg + "\"")
    ws.send(msg)

# Format to string array of strings
def fmt_arr_str(i):
    return "[\""+'","'.join([x for x in i ])+"\"]"
