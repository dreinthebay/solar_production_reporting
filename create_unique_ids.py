# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 22:37:00 2020

@author: slin2
"""

import uuid

import shortuuid

#alphabet = 'abcdefghijklmnopqrstuvwxyz123456789'
#shortuuid.set_alphabet(alphabet)

def generate_short_unique_id(string):
    sunique_id = None
    sunique_id = shortuuid.uuid(name=string)
    #shortuuid.ShortUUID().random(length=8)
    return sunique_id
def generate_unique_id(string):
    unique_id = None
    unique_id = uuid.uuid3(uuid.NAMESPACE_DNS, string)
    return unique_id


a = 'bob'

print(generate_unique_id(a))
b = 'Bob'
print(generate_unique_id(b))
c = 'BoB'
print(str(generate_unique_id(c))[:8])
c = 'bob'
string = c
str(uuid.uuid4())[:8]

generate_short_unique_id(a)
generate_short_unique_id(b)
generate_short_unique_id(c)
