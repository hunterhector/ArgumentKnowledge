from args_know.utils import nif_utils
from args_know.utils.nif_utils import NifRelationCollector
from args_know.utils.nif_parser import NIFParser
from args_know.utils import data_utils
import re
import sys


def read_interlingual_links(language_link_path, target_lang):
    target_relation = "http://www.w3.org/2002/07/owl#sameAs"
    source_prefix = "http://dbpedia.org/resource/"
    target_prefix = "http://<lang>.dbpedia.org/resource/".replace("<lang>", target_lang)

    collector = NifRelationCollector(
        target_relation
    )

    line_count = 0
    resource_count = 0

    source_regex = re.compile("^" + source_prefix)
    target_regex = re.compile("^" + target_prefix)

    for statements in NIFParser(language_link_path):
        for s, v, o in statements:
            ready = collector.add_arg(s, v, o)

            if ready:
                line_count += 1
                from_resource = re.sub(source_regex, "", s)
                target_url = collector.pop(s)[target_relation]

                if target_url.startswith(target_prefix):
                    resource_count += 1
                    target_resource = re.sub(target_regex, "", target_url)
                    sys.stdout.write("\r%d %s resources found in %d lines." % (resource_count, target_lang, line_count))
                    yield from_resource, target_resource


def write_interlingual_resources(language_link_path, target_lang, output_path):
    data_utils.ensure_parent_dir(output_path)
    with open(output_path, 'w') as out:
        for from_resource, target_resource in read_interlingual_links(language_link_path, target_lang):
            out.write("%s\t%s\n" % (from_resource, target_resource))
