import gnupg
import os
import json

gpg_dir = os.getcwd()[:os.getcwd().rindex('/')] + '/.gnupg'
gpg = gnupg.GPG(gnupghome = gpg_dir)
gpg.encoding = 'utf-8'

def fps(el):
    return el["fingerprint"]

def get_key(fin, secret = False):
    keys = gpg.list_keys(secret)
    key_fps = list(map(fps, keys))
    
    for index,item in enumerate(key_fps):
        if fin in item:
            return keys[index]

    return None

def get_key_data(fin):
    ret = {}

    ret["sec"] = get_key(fin, secret = True)
    ret["pub"] = get_key(fin)
    ret["exp"] = gpg.export_keys(fin)

    return ret

def write_key_to_file(fin):
    with open("keys.json", "r+") as keys:
        kinfo = json.loads(keys.read())
        kinfo["keys"].append(fin)
        keys.seek(0)
        keys.write(json.dumps(kinfo))
        keys.close()

    pass

def create_key(
    name_real,
    passphrase,
    name_comment='',
    name_email='',
    key_type='RSA',
    key_length=1024,
    no_protection=False):
    input_data = gpg.gen_key_input(
        name_real=name_real,
        passphrase=passphrase,
        name_comment=name_comment,
        name_email=name_email,
        key_type=key_type,
        key_length=key_length,
        no_protection=no_protection)
    fin = gpg.gen_key(input_data)
 
    return fin



