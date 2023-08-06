import os, json

def open_json(json_file):
    with open(json_file) as data:
        return json.load(data)

def write_dotenv(env, file=".env"):
    """
    python-dotenv dont have any function to overwrite .env file
    write_dotenv is just a write variables in text file
    """
    with open(".env", "w") as f:
        for i in env:
            f.write(f'{i}={env[i]}\n')

def to_print_dict(dic:dict):
    """
    @ make the dict a key: value table string
    """
    ret = ''
    for i in dic:
        ret = ret + f"""\n {i}: {dic[i]}"""
    return ret

def print_dict(dic:dict):
    """
    @ just print to_print_dict
    """
    print(to_print_dict(dic))