_registry = {}


def register(classname, cls):
    """Add a class to the registry of serializer classes. When a class is
    registered, an entry for both its classname and its full, module-qualified
    path are added to the registry.

    Example: ::

        class MyClass:
            pass

        register('MyClass', MyClass)
        # Registry:
        # {
        #   'MyClass': [path.to.MyClass],
        #   'path.to.MyClass': [path.to.MyClass],
        # }

    """
    # Module where the class is located
    module = cls.__module__
    # Full module path to the class
    # e.g. user.schemas.UserSchema
    fullpath = '.'.join([module, classname])
    # If the class is already registered; need to check if the entries are
    # in the same module as cls to avoid having multiple instances of the same
    # class in the registry
    if classname in _registry and not \
            any(each.__module__ == module for each in _registry[classname]):
        _registry[classname].append(cls)
    else:
        _registry[classname] = [cls]

    # Also register the full path
    _registry.setdefault(fullpath, []).append(cls)
    return None


def get_class(classname):
    """Retrieve a class from the registry."""

    try:
        classes = _registry[classname]
    except KeyError:
        raise NameError(
            'Class with name {0!r} was not found. You may need '
            'to import the class.'.format(classname))
    if len(classes) > 1:
        raise RuntimeError(
            'Multiple classes with name {0!r} '
            'were found. Please use the full, '
            'module-qualified path.'.format(classname))
    else:
        return _registry[classname][0]
