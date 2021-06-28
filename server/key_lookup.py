import gnupg
import os
gpg_dir = os.getcwd()[:os.getcwd().rindex('/')] + '/.gnupg'
gpg = gnupg.GPG(gnupghome = gpg_dir)
gpg.encoding = 'utf-8'

def uids(el):
    return el["uids"]

def get_pk(uid):     
    keys = gpg.list_keys()
    key_uids = list(map(uids, keys))
    
    for index,item in enumerate(key_uids):
        for all_uids in item:
            if uid in all_uids:
                return keys[index]

    return None

def get_sk(uid):
    keys = gpg.list_keys(True)
    key_uids = list(map(uids, keys))

    for index,item in enumerate(key_uids):
        for all_uids in item:
            if uid in all_uids:
                return keys[index]

    c = input(f"""No \'{uid}\' key was found.
Do you want to create a new {uid} key? (y/n)""")

    while c == 'y':
        p1 = input("Key passphrase: ")
        p2 = input("Repeat passphrase: ")
        if p1 == p2:
            create_key(
                name_real=uid,
                passphrase=p1)
            print("Key created.")
        else:
            print("Passphrases do not match. Please try again.")

    return None


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
    key = gpg.gen_key(input_data)
    print(key)
    return key

