import re
import ast

def read(code:str):
    """Reads Silicon code and returns a dictionary"""

    valid = [" ","=",";","\n","\t","$","\"","\\","#","{","}","%","!","[","]"]
    definitions = ["True","False","None"]
    
    key = ""
    value = ""
    keyword = ""
    found = False
    invar = False
    isvar = False
    inval = False
    inescape = False
    incomment = False
    indict = False
    inarray = False
    isfunction = False
    inkeyword = False

    values = {}

    for c in code:
        if incomment:
            if c == "\n":
                incomment = False
        elif inkeyword:
            if c != "!":
                keyword += c
            else:
                inkeyword = False
        elif c not in valid:
            if not found:
                key += c
            else:
                value += c
                if invar:
                    isvar = True
        elif c == "\\":
            inescape = True
        elif c == "{":
            indict = True
            value += c
        elif c == "}":
            indict = False
            value += c
        elif c == "[":
            inarray = True
            value += c
        elif c == "]":
            inarray = False
            value += c
        elif c == "%":
            isfunction = True
            value += c
        elif c == "!":
            inkeyword = True
        elif c == "\"":
            if inescape == False and not indict and not inarray and not isfunction and not inkeyword:
                inval = not inval
            elif inkeyword:
                inkeyword = False
            else:
                value += "\""
                inescape = False
        elif c == "#":
            if not inval and not isfunction:
                incomment = True
            else:
                value += c
        elif c == "=":
            if not inval and not isfunction:
                found = True
            else:
                value += c
        elif c == "$":
            if not inval and not isfunction:
                invar = True
            else:
                value += c
        elif c == " " and inval:
            value += c
        elif c == ";":
            if not inval and not inescape and keyword == "":
                if isvar:
                    values[key] = values[value]
                elif isfunction:
                    values[key] = eval("__sf_" + value.replace("%",""))
                elif value.isdigit():
                    v = float(value)
                    
                    if v.is_integer():
                        values[key] = int(v)
                    else:
                        values[key] = v
                elif value in definitions:
                    if value == "True":
                        values[key] = True
                    elif value == "False":
                        values[key] = False
                    elif value == "None":
                        values[key] = None
                elif (value.startswith("[") and value.endswith("]")) or (value.startswith("{") and value.endswith("}")):
                    values[key] = ast.literal_eval(value)
                else:
                    values[key] = value

                key = ""
                value = ""
                keyword = ""
                found = False
                invar = False
                isvar = False
                inescape = False
                isfunction = False
            elif keyword != "":
                if keyword.startswith("merge"):
                    kv = keyword.replace("merge","")
                    kv = re.findall('"([^"]*)"',kv)[0]
                    imported = read(open(kv,"r").read())
                    values.update(imported)

                key = ""
                value = ""
                keyword = ""
                found = False
                invar = False
                isvar = False
                inescape = False
                isfunction = False
                inarray = False
            else:
                value += c

    return values

def convert(dictionary:dict={},beautify:bool=False):
    """Returns the Silicon code of dictionary"""

    d = dictionary
    content = ""

    for k in d:
        v = d[k]

        if type(v) == str:
            if beautify:
                content += k + " = \"" + v + "\";\n"
            else:
                content += k + "=\"" + v + "\";"
        elif type(v) == int:
            if beautify:
                content += k + " = " + v + ";\n"
            else:
                content += k + "=" + v + ";"
        elif type(v) == list:
            if beautify:
                content += k + " = " + str(v).replace("'","\"") + ";\n"
            else:
                content += k + "=" + str(v).replace("'","\"") + ";"
        elif type(v) == dict:
            if beautify:
                content += k + " = " + str(v).replace("'","\"") + ";\n"
            else:
                content += k + "=" + str(v).replace("'","\"") + ";"
        elif type(v) == bool:
            if beautify:
                content += k + " = " + str(v).lower() + ";\n"
            else:
                content += k + "=" + str(v).lower() + ";"

    return content

def __sf_read(file):
    return open(file,"r").read()

def __sf_int(value):
    return int(value)

def __sf_string(value):
    return str(value)

def __sf_float(value):
    return float(value)

def __sf_array(value):
    return list(value)

def __sf_dictionary(value):
    return dict(value)

def __sf_bool(value):
    return bool(value)

def __sf_replace(string,old,new):
    return string.replace(old,new)

def __sf_split(string,value):
    return string.split(value)

def __sf_join(string,array):
    return string.join(array)

def __sf_startswith(string,value):
    return string.startswith(value)

def __sf_endswith(string,value):
    return string.endswith(value)

def __sf_strip(string):
    return string.strip()

def __sf_swapcase(string):
    return string.swapcase()

def __sf_title(string):
    return string.title()

def __sf_capitalize(string):
    return string.capitalize()

def __sf_lower(string):
    return string.lower()

def __sf_eval(string):
    return eval(string)

def __sf_import(file):
    return read(open(file,"r"))

def __sf_get_from_dictionary(dictionary,key):
    return dictionary[key]

def __sf_get_from_array(array,index):
    return array[index]

def __sf_is_valid(value):
    if not value:
        return True
    else:
        return False

def __sf_if(value1,operator,value2):
    return eval(str(value1) + " " + str(operator) + " " + str(value2))