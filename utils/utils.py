crimson = 0xDC143C


def flatten(d, inval, outval):
    for k, v in d.items():
        if isinstance(v, dict):
            flatten(d[k], inval, outval)
        else:
            if v == "":
                d[k] = None
    return d

