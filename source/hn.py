import json
import urllib2
import time
from xml.etree import ElementTree as ET


def get_items(uri, query=None):
    items = []
    data = json.loads(urllib2.urlopen(uri).read())
    for item in data['items']:
        if 'id' in item and 'title' in item:
            if query is None or query.lower() in item['title'].lower():
                result = parse_item(item)
                items.append(result)

    xml = generate_xml(items)
    return xml


def generate_xml(items):
    xml_items = ET.Element('items')
    for item in items:
        xml_item = ET.SubElement(xml_items, 'item')
        for key in item.keys():
            if key is 'uid' or key is 'arg':
                xml_item.set(key, item[key])
            else:
                child = ET.SubElement(xml_item, key)
                child.text = item[key]
    print(ET.tostring(xml_items))


def parse_item(item):
    return {
        'uid': '%s%s' % (item['id'], time.time()),
        'arg': item['url'],
        'title': item['title'],
        'subtitle': '%s points | %s comments | %s | %s' % (item['points'], item['commentCount'], item['postedAgo'], item['postedBy']),
        'icon': 'icon.png'
    }