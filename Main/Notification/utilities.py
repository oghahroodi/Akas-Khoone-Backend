def makeJsonNotif(kind, doer, entity, date):
    result = {}
    result["kind"] = kind
    result["doer"] = doer
    result["entity"] = entity
    result["date"] = date
    return result
