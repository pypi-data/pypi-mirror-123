def arg_to_bool(var, default=False):
    res = default

    if default == True:
        if var in ['false', 'False', 0, False]:
            res = False
    else:
        if var in ['true', 'True', 1, True]:
            res = True

    return res
