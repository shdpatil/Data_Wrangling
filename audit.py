
# coding: utf-8

# In[9]:

import xml.etree.cElementTree as ET
from collections import defaultdict
import re

def get_element(file_name):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = ET.iterparse(file_name, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end':
            yield elem
            root.clear()

#define a function to count all types of tags in the file
def count_tags(file_name):
    tag_dict = defaultdict(int)
    for i, elem in enumerate(get_element(file_name)):
        tag_dict[elem.tag] += 1
    return tag_dict
count_tags("sample.osm")
    
        


# In[ ]:

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
osm_file = open("miami_florida.osm", "r")
street_type_re = re.compile(r'\S+.?$', re.IGNORECASE)
street_types = defaultdict(int)
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_types[street_type] += 1
def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 
def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")
def audit():
    for event, elem in ET.iterparse(osm_file):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v']) 
            print_sorted_dict(street_types) 
            
if __name__ == '__main__':
    audit()


# In[7]:

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "miami_florida.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive","Circle" "Court", "Place", "Square", "Lane", "Road", 
            "Trail","Terrace", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "st": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "ave": "Avenue",
            "Pkwy": "Parkway",
            "Blvd": "Boulevard",
            "Cir": "Circle",
            "Ct": "Court",
            "Trl": "Trail",
            "Ter": "Terrace",
            "Ln": "Lane",
            "Pl": "Place",
            "Hwy": "Highway",
            "Dr": "Drive",
            "Rd": "Road",
            "Rd.": "Road",
            "Com": "Commons",
            "Ct": "Court"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):

    m = street_type_re.search(name)
    other_street_types = []
    if m:
        street_type = m.group()
        if street_type in mapping.keys():
            name = re.sub(street_type_re,mapping[street_type],name)
        else:
            other_street_types.append(street_type)

    return name


def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
        print name, "=>", better_name
if __name__ == '__main__':
    test()


# In[4]:

import xml.etree.cElementTree as ET

from collections import defaultdict

import re

import pprint



OSMFILE = "miami_florida.osm"

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
# create the dict to put zipcodes into
def add_to_dict(data_dict, item):
    data_dict[item] += 1

# find the zipcodes
def get_postcode(element):
    for tag in element:
        if (tag.attrib['k'] == "addr:postcode"):
            postcode = tag.attrib['v']
            return postcode


# update zipcodes
def update_postal(postcode):
    postal_code = re.search(r'^\D*(\d{5}).*',postcode)
    #postal_code.groups()
    if postal_code:
        clean_postcode = postal_code.group(1)
        return clean_postcode
        

    #return postcode


# output the list of zipcodes into dict
def audit(osmfile):
    osm_file = open(OSMFILE, "r")
    data_dict = defaultdict(int)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if get_postcode(elem.iter("tag")):
                    postcode = get_postcode(elem.iter("tag"))
                    postcode = update_postal(postcode)
                    add_to_dict(data_dict, postcode)
    return data_dict

# test the zipcode audit and dict creation
def test():
    cleanzips = audit(OSMFILE)
    pprint.pprint(dict(cleanzips))



if __name__ == '__main__':

    test()


# In[3]:

import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    if element.tag == 'node' or element.tag == 'way' or element.tag == 'relation':
        uid = element.get('uid')
        
    return uid


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        #print element.tag
        if element.get('uid'):
            users.add(element.get('uid'))
        pass

    return users


def test():

    users = process_map('miami_florida.osm')
    pprint.pprint(users)
    #assert len(users) == 6



if __name__ == "__main__":
    test()


# In[ ]:




# In[ ]:



