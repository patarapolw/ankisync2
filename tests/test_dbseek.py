#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
#  Experimental way to access to Notes matching model id, Field name and value
#-------------------------------------------------------------------------------

#sudo pip3 install ankisync2
import os

from anki.storage import Collection
from ankisync2.apkg import Apkg


import pprint

from ankisync2.anki20 import db  
from ankisync2.dir import AnkiPath  # pylint: disable=import-error
#from anki.storage import Collection 

#========== SETTINGS =============================================
db_name="example1"

#.anki20 has extra models and templates useful tables
# I guess it was produced from dconf of 'col' tables
db_anki_format='anki20'
#db_anki_format='anki2'

DECK_DEFAULT='Default'

#Model id to filter the notes
MODEL_ID=0
# if 0 it will use MODEL_DEFAULT. 
# ATTENTION , the name is language dependent
MODEL_DEFAULT='Basic'

FIELD_NAME= 'Chinese_Character'
FIELD_VALUE= '爬上'

#==================================================================

script_dir = os.path.dirname(__file__)
anki_collection_path = os.path.join(script_dir, db_name)

# 0. Load the anki package
apkg = Apkg(anki_collection_path+".apkg")

if(db_anki_format== 'anki2'):
    col = Collection(anki_collection_path+"/collection.anki2", log=True)
    
    # Optional Set the deck
    deck = col.decks.byName(DECK_DEFAULT)
    col.decks.select(deck['id'])
    #pprint(col)
    db=col.db

    modelType = col.models.byName(MODEL_DEFAULT)
    if(MODEL_ID == 0):
        MODEL_ID=modelType.id

    SQL="""SELECT conf, models, decks, dconf
       FROM col"""

    SQL_FILTER=""
    PARAMS=""
    cursor=db.database.execute_sql(SQL+SQL_FILTER, PARAMS)

    import json
    for row in cursor.fetchall():
        #chinese_word=str(row[0])
        conf =json.loads(row[0]) 
        models= json.loads(row[1])
        decks= json.loads(row[2])
        dconf=json.loads(row[3])
        #json.dumps(row[2], ensure_ascii=False)
        #response= str(response.encode('utf8'))
       
        model=models[str(MODEL_ID)]
        
        #card_templates=model['tmpls']
        flds=model['flds']
        card_field_names=[]
        for fld in flds:
            card_field_names.append(fld['name'])

elif(db_anki_format== 'anki20'):
    #NOTE: Not SURE ABOUT if returns col, I am lazy to check
    col=db.database.init(anki_collection_path+"/collection."+db_anki_format)
    SQL="""SELECT flds
       FROM models"""

    if(MODEL_ID == 0): 
        modelType = col.models.byName(MODEL_DEFAULT)
        MODEL_ID=modelType.id

    SQL_FILTER=" WHERE id = "+str(MODEL_ID)+" ;"
    PARAMS=""
    cursor=db.database.execute_sql(SQL+SQL_FILTER, PARAMS)
    for row in cursor:
        #chinese_word=str(row[0])
        separator = "\x1f"
        card_field_names=row[0].split(separator)
else:
    raise("Unsupported anki database format '"+db_anki_format+"'")

"""       

Seek the note that has the matching name field and value

SQL_FILTER="WHERE fields LIKE '%"+FIELD_VALUE+"%'" is not safe, as many fields can has this value so we use our sqlite custom 'field_contains' extension defined in "anki20/db.py" to check it is the good field. Fields data are separated by "\x1f"
This provides a db way that may be faster than
  for n in db.Notes.filter(db.Notes.data["FIELD_NAME"] == "FIELD_VALUE"):  
bur we loose the Note Object wrapping.  
"""  

SQL="""SELECT note_id, fields_names || "\x1f" || fields_values as fields
from(SELECT notes.id as note_id, REPLACE(notes.flds,'@','\\@') as fields_values, REPLACE(models.flds," ","_")  as fields_names
       FROM models, notes ) """       
SQL_FILTER="WHERE fields LIKE '%"+FIELD_VALUE+"%' AND field_contains(fields,'"+FIELD_NAME+"','"+FIELD_VALUE+"')"

PARAMS=""
cursor=db.database.execute_sql(SQL+SQL_FILTER, PARAMS)
for row in cursor.fetchall():
    card_fields=row[1].split("\x1f")
    field_names=card_fields[:len(card_fields)//2]
    field_values=card_fields[len(card_fields)//2:]
    card_fields = {key:value for key, value in zip(field_names, field_values)}

print(card_fields)

apkg.close()
