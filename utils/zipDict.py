def zipDict(*dicts:dict):
    r={}
    [r.update(i) for i in dicts]
    return r