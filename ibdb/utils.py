from itertools import chain


def make_difference_list_from_key(target, source, key):
    target_key = set(chain.from_iterable(target))
    source_key = {x[key] for x in source}
    diff = source_key - target_key
    return [x for x in source if x[key] in diff]
