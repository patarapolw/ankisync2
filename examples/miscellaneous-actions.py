#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# miscellaneous-actions.py : implementation of the Miscellaneous Actions
# Author: sosie <sosie@sos-productions.com> (08.2021)
# Note: this is a direct copy, autogenerated from the fixed API docs found on FooSoft productions website
# using Anᴵkisync2_api.py script. Some examples may not work
# due to the missing test database collections.anki2 in the current user anki directory
# See : https://foosoft.net/projects/anki-connect/#miscellaneous-actions
#
#sudo pip3 install ankisync2
import os

from ankisync2.ankiconnect import  ankiconnect as invoke

        
    {
        "action": "deckNames"
    },
    {
        "action": "browse",
        "params": {
            "query": "deck:current"
        }
    }
]