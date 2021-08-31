#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#sudo pip3 install ankisync2
import os

from ankisync2.ankiconnect import  ankiconnect as invoke

#https://foosoft.net/projects/anki-connect/#card-actions

#Gets the complete list of deck names for the current user.
result = invoke('deckNames')
print('got list of decks: {}'.format(result))

#Gets the complete list of deck names and their respective IDs for the current user.
result = invoke('deckNamesAndIds')
print('got list of decks: {}'.format(result))

#Accepts an array of card IDs and returns an object with each deck name 
#as a key, and its value an array of the given cards which belong to it.
cards=[1502298036657, 1502298033753, 1502032366472]
result = invoke('getDecks',  cards=cards)
print('got list of decks: {}'.format(result))

#reate a new empty deck. Will not overwrite a deck that exists 
#with the same name.
deck="Japanese::Tokyo"
result = invoke('createDeck',  deck=deck)
print('got list of decks: {}'.format(result))

#Deletes decks with the given names. If cardsToo is true
#(defaults to false if unspecified), the cards within the deleted decks
#will also be deleted; otherwise they will be moved to the default deck.
decks=["Japanese::Tokyo"]
cardsToo=True
result = invoke("deleteDecks",  decks=decks , cardsToo=cardsToo)
print('got list of decks: {}'.format(result))

#Gets the configuration group object for the given deck.
deck="Japanese::Tokyo"
result = invoke("getDeckConfig",  deck=deck)
print('got list of decks: {}'.format(result))

#

#Saves the given configuration group, returning true on success or false 
#if the ID of the configuration group is invalid (such as when it does not exist).
deck="Japanese::Tokyo"
config={
            "lapse": {
                "leechFails": 8,
                "delays": [10],
                "minInt": 1,
                "leechAction": 0,
                "mult": 0
            },
            "dyn": False,
            "autoplay": True,
            "mod": 1502970872,
            "id": 1,
            "maxTaken": 60,
            "new": {
                "bury": True,
                "order": 1,
                "initialFactor": 2500,
                "perDay": 20,
                "delays": [1, 10],
                "separate": True,
                "ints": [1, 4, 7]
            },
            "name": "Default",
            "rev": {
                "bury": True,
                "ivlFct": 1,
                "ease4": 1.3,
                "maxIvl": 36500,
                "perDay": 100,
                "minSpace": 1,
                "fuzz": 0.05
            },
            "timer": 0,
            "replayq": True,
            "usn": -1
        }
result = invoke("saveDeckConfig",  config=config)
print('got list of decks: {}'.format(result))
