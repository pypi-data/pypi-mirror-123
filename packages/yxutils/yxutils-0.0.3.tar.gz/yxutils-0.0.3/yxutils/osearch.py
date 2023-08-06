import re
import json

def osearch(ds,pattern=".*") :
    if type(ds) is lst :
        return [i for i in lst if re.search(r"{}".format(pattern),json.dumps(i))]
    if type(ds) is dict :
        if "=" not in pattern : 
            tgtds = ds
        if "=" in pattern : 
            key,val = pattern.split("=",1)
            tgtds = dict()
            for k, dv in ds.items() if re.search(r"{}".format(key),k) and re.search(r"{}".format(val),dv) :
                tgtds[k] = dv
        return tgtds




