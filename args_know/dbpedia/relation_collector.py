from args_know.utils.nif_parser import NIFParser
from args_know.utils import data_utils
import re
import sys
import rdflib

def read_relations(language_link_path):
    resource_count = 0
    for statements in NIFParser(language_link_path):
        for s, v, o in statements:
            resource_count += 1
            sys.stdout.write("\r%d resources found." % resource_count)

            # yield from_resource, v, target_resource
            yield s, v, o


def write_relations(relation_file, output_path):
    resource_prefix = "http://dbpedia.org/resource/"

    data_utils.ensure_parent_dir(output_path)

    source_regex = re.compile("^" + resource_prefix)
    target_regex = re.compile("^" + resource_prefix)

    with open(output_path, 'w') as out:
        for s, v, o in read_relations(relation_file):
            from_resource = re.sub(source_regex, "", s)
            target_resource = re.sub(target_regex, "", o)

            if isinstance(o, rdflib.term.Literal) and o.datatype:
                out.write("%s\t%s\t%s\t%s\n" % (from_resource, v, target_resource, o.datatype))
            else:
                out.write("%s\t%s\t%s\n" % (from_resource, v, target_resource))
