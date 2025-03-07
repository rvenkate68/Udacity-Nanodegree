"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "NWPortland.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

street_dir_re = re.compile(r'^([a-z]|_)*\b\S+\.?', re.IGNORECASE)

expected = ["Avenue", "Boulevard", "Circle", "Court", "Drive", "Highway", "Lane",
            "Loop", "Parkway", "Place", "Road", "Street", "Terrace",  "Way" ]

expected_dir = ["Northwest", "Southwest"]

#expected = []
# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "Ave": "Avenue",
            "Dr": "Drive",
            "Hwy": "Highway",
            "Rd": "Road",
            "road": "Road",
            "GLN": "Glen Street",
            "Regatta": "Regatta Lane",
            "Blanton": "Blanton Street"
            }

map_dir = { "NW": "Northwest",
            "SW": "Southwest"
            }

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
        n = street_dir_re.search(street_name)
        if n:
            direction = n.group()
            if direction not in expected_dir:
                street_types[direction].add(street_name)


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

    return street_types


def update_name(name, mapping):

    street_name = street_type_re.search(name)
    key = street_name.group()
    new_street = mapping.get(key)
    if new_street:
        name = re.sub(street_type_re, new_street, name)
    return name

def update_dir(name, map_dir):

    street_dir = street_dir_re.search(name)
    key = street_dir.group()
    new_street = map_dir.get(key)
    if new_street:
        name = re.sub(street_dir_re, new_street, name)
    return name


def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))

if __name__ == '__main__':
    test()
