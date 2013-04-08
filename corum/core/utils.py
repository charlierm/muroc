from django.contrib.admin.util import NestedObjects
import pprint


def to_dic(lst):
    result = {}
    for item in iter(lst):
        next = item.next()
        if type(item) is list:
            result[item.id] = to_dic(item)
        else:
            result[item.id] = item
        if type(item.next()) is list:
            result[item.id] = to_dic(item.next())
    return result


def get_relationships(object):
    collector = NestedObjects(using='default')
    collector.collect([object])
    test = collector.nested()
    pprint.pprint(to_dic(test))




