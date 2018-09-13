def makeJsonNotif(kind, doer, date, **kwargs):
    result = {}
    result["kind"] = kind
    result["doer"] = doer
    result["date"] = date
    if kind == 'comment' or kind == 'like':
        result["entity"] = kwargs['entity']
        return result
    if kind == 'request':
        result["target"] = kwargs['target']
        return result
