import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def gen_key_from_pass(passwd:str)->bytes:
    '''
    Generates key from password.
    '''
    passwd = passwd.encode() 
    salt = b'_50M3s3c43tK3Y!'  
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(passwd))
    # print(key)
    return key


def generate_key()->bool:
    '''
    Generates random key and saves it in key file.
    '''
    with open('keys.txt', 'wb') as key_file:
        KEY = Fernet.generate_key()
        key_file.write(KEY)
        return True


def get_key()->bytes:
    '''
    Extracts key from the key file.
    '''
    with open('keys.txt', 'r') as key_file:
        KEY = key_file.read()
        return KEY


def encrypt_data(KEY:bytes, data:str)->bytes:
    '''
    encrypts data which is passed with the help of key as
    another parameter and returns encrypted data in form 
    of bytes
    '''
    data = data.encode('utf-8')
    encrypter = Fernet(KEY)
    enc_data = encrypter.encrypt(data)
    return enc_data


def decrypt_data(KEY:bytes, data:str)->bytes:
    '''
    decrypts data which is passed with the help of key as
    another parameter and returns decrypted data in form 
    of bytes
    '''
    data = data.encode('utf-8')
    decrypter = Fernet(KEY)
    dec_data = decrypter.decrypt(data)
    return dec_data
