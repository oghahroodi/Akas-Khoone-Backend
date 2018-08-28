import re

def extractHashtags(s):
    return re.findall(r"#(\w+)", s)
    #return set(part[1:] for part in s.split() if part.startswith('#'))