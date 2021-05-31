from annotation.typed import AnyType, only, optional, options, predicate, typechecked, union


typed = lambda x: x
number = union(int, float)


def derives(base_class):
    return predicate(lambda x: issubclass(x, base_class))


def enable():
    global typed
    typed = typechecked
