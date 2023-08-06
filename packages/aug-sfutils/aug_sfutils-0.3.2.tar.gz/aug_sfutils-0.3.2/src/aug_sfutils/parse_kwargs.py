def parse_kw(lbl_in, kwargs, default=None):
    for key in lbl_in:
        if key in kwargs.keys():
            return kwargs[key]
    return default
