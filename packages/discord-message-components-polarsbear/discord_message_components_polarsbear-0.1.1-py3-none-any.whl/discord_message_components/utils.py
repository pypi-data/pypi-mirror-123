def removenone(d):
    tmp = d
    broken = True
    while broken:
        broken = False
        for k in tmp:
            if tmp[k] is None:
                tmp.__delitem__(k)
                broken = True
                break

    return tmp



def valueparse(v):
    if isinstance(v, list):
        tmp = []
        for i in v:
            tmp.append(valueparse(i))
        return tmp

    elif v.__class__.__module__ == "discord_message_components.classes":
        return removenone(todict(v))

    else:
        return v


def todict(obj):
    tmp = {}
    d = removenone(obj.__dict__)
    for k,v in d.items():
        tmp[k] = valueparse(v)

    return tmp