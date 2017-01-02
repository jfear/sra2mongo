"""Some small helpers for dealing with xml."""
from sramongo.logger import logger


class AmbiguousElementException(Exception):
    pass


def valid_path(func):
    """Validates that a XML path exists.

    A decorator function that makes sure a XML path (i.e.
    xml.etree.ElementTree.ElemenTree.Element) exists. If the path does not
    exists then return an empty dictionary.

    """
    def new_func(*args, **kwargs):
        # If the current path is present
        if args[1] is None:
            logger.debug(('Not valid path.', func, args))
            return {}
        else:
            return func(*args, **kwargs)

    return new_func


@valid_path
def parse_tree_from_dict(node, locs):
    """Processes key locations.

    node: xml.etree.ElementTree.ElementTree.element
        Current node.
    locs: dict
        A dictionary mapping key to a tuple. The tuple can either be 2 or 3
        elements long. The first element maps to the location in the
        current node. The second element given a processing hint. Possible
        values are:

            * 'text': assumes the wanted is the text element of the path.
            * 'child': assumes that the child of the given path is wanted.
            * str: Any other string will be treated as an attribute lookup
                   of the path.

        If 'child' is given, then a third element needs to be given
        indicating the type of processing. Possible values are:

            * 'text': assumes the wanted is the text element of the path.
            * 'tag': assumes the wanted is the class tag of the path.
            * str: Any other string will be treated as an attribute lookup
                   of the path.

    """
    d = dict()
    for n, l in locs.items():
        try:
            if l[1] == 'text':
                d[n] = node.find(l[0]).text
            elif l[1] == 'child':
                child = node.find(l[0]).getchildren()

                if len(child) > 1:
                    raise AmbiguousElementException(
                            'There are too many elements')
                elif l[2] == 'text':
                    d[n] = child[0].text
                elif l[2] == 'tag':
                    d[n] = child[0].tag
            else:
                d[n] = node.find(l[0]).get(l[1])
        except:
            pass

    return d
