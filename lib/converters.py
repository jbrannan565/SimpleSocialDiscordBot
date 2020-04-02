def convert_arg_to_dict(args):
    ret = {}

    args = " ".join(args)
    args = args.split(', ')

    for a in args:
        a = a.split('=')
        ret[a[0]] = a[1]
    
    return ret

def dict_to_string(resource):
    _resource = ""
    for (key,val) in resource.items():
        if key == "_id" or key == "last_update":
            continue
        if type(val) is list:
            _resource += f"\t{key}:\n"
            for v in val:
                _resource += f"\t\t- {v}\n"
            continue
        _resource += f"\t{key}: {val}\n"
    return _resource

def cursor_to_string(cursor):
    _ret = ""
    for c in cursor:
        if type(c) is dict:
            _ret += dict_to_string(c)
            _ret += "\n"
    return _ret


