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

def gen_random_short_unique_id():
    u_id = shortuuid.uuid()
    
    return u_id

generate_short_unique_id(a)
generate_short_unique_id(b)
generate_short_unique_id(c)

u_list = []

for i in range(1000):
    u_list.append(gen_random_short_unique_id())

#https://stackoverflow.com/questions/14134237/writing-data-from-a-python-list-to-csv-row-wise
import csv
file = 'unique_ids.csv'
with open(file, 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     for u in u_list:
         #print(u)
         wr.writerow([u])

'''
Needs for unique system id's
Requirements:
We would like the IDs to be:
    1. short
    2. readable
    3. unique
    4. reproducible

For unique id's, we use UUIDs which are ISO standardized unique identifiers.

Short:
    Maulik found a useful, shorter version of the UUID called shortuuid.
    These reduce 36 character uuids into (roughly) 8 characters for shortuuids in length.
Readability:
    we can limit the alphabet used in the shortuuids, however, this will reduce the
    amount of possible permutations and thus uniqueness. To keep the number of
    permutations large, limiting the alphabet makes the shortuuids longer
    in character length. If we limit the types of characters
    (ie lower case only or no 'l's) then the uuids grow in length
Unique:
    we want to make sure the id's created are unique so that there are no "collisions".
    The id must be of appropriate length, and the hashing method we use to convert
    strings to ids must be robust enough to limit collisions.
Reproducible:
    What if we lose one of the unique id's? We want these id's to be reproducable so that
    if we need/try to generate the unique id of the system again, it will always have the same id. 
    Therefore, we cannot use randomly generated uuids, but make them off of a
    certain string value, like the site name or address.
   
AI
    use shortuuids
    create alphabet
    make ids long enough to guarantee uniqueness    
    [need NCS] determine which piece of information to generate the shortuuid off of (address, sitename, something unique)

'''