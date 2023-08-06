from . import encrypt
from . import db
from . import hash


class User:
    '''
    class User generates a user, stores data with the help of encryption.
    '''

    def __init__(self, new_usr:bool, usrname:str, passwd:str)->None:
        '''
        create User
        takes new_user (bool) as parameter 
        '''
        self.usrname = usrname
        self.__password = passwd

        # create dictionary with lists to store information
        self.data = {
                'usernames': [],
                'passwords': [],
                'websites': [],
                'encrypted' : False 
        }

        if new_usr:
            # print('[*] Generating new user...')
            # print('[*] Calculating password hash')
            pass_hash = hash.hashdata(self.__password)
            # print('[*] Adding password hash to db')
            db.add_user(usrname=self.usrname, password_hash=pass_hash)   
            # print('[*] User created with username {}'.format(self.usrname))        


    def add_info(self, username, password, website)->bool:
        '''
        add user entered information to the lists.
        returns bool.
        '''
        # print('[*] Adding Information to the lists')
        # if any parameter is empty, print error
        if bool(username) and bool(password) and bool(website):
            self.data['usernames'].append(username)
            self.data['websites'].append(website)
            self.data['passwords'].append(password)
            self.encrypt_info()
            # print('[*] Information added to list successfully.')
            db.dump_user_data(self.data, self.usrname)
            return True
        else:
            # print('[-] Please enter valid information. All parameters should be non empty.')
            return False
            

    def encrypt_info(self)->bool:
        '''
        encrypts all the data (information) in the user dict. 
        '''
        # check if data is not encrypted
        if not self.data['encrypted']:
            KEY = encrypt.gen_key_from_pass(self.__password)
            length = len(self.data['usernames'])

            # encrypt data into a new list
            usernames = [ encrypt.encrypt_data( KEY, self.data['usernames'][pos] ).decode('utf-8') for pos in range(length) ]
            passwords = [ encrypt.encrypt_data( KEY, self.data['passwords'][pos] ).decode('utf-8') for pos in range(length) ]
            websites = [ encrypt.encrypt_data( KEY, self.data['websites'][pos] ).decode('utf-8') for pos in range(length) ]
            
            # update data values
            self.data['usernames'] = usernames
            self.data['passwords'] = passwords
            self.data['websites'] = websites
            self.data['encrypted'] = True

            # print('[*] Encrypted Data successfully')
            return True

        else : 
            # print('[*] Data is already encrypted.')
            return False


    def __get_usr_pass_hash(self)->str:
        '''
        returns stored user password hash from saved password hash database.
        '''
        return db.get_pass_hash(self.usrname)


    def authenticate_user(self)->bool:
        '''
        Autenticates user before viewing their passwords.
        returns: bool
        '''
        entered_pass = self.__password
        pass_hash = hash.hashdata(entered_pass)

        usr_pass_hash = self.__get_usr_pass_hash()

        if pass_hash == usr_pass_hash and usr_pass_hash != '':
            # print(f'[*] {self.usrname} Authenticated.')
            return True           

        # print(f'[!] {self.usrname} unsuccessfull login attempt!')
        return False


    def decrypt_info(self)->bool:
            '''
            decrypts all the data (information) in the user dict. 
            '''
            # check if data is encrypted
            if self.data['encrypted']:
                
                KEY = encrypt.gen_key_from_pass(self.__password)
                length = len(self.data['usernames'])

                # decrypt data into a new list
                usernames = [ encrypt.decrypt_data( KEY, self.data['usernames'][pos] ).decode('utf-8') for pos in range(length) ]
                passwords = [ encrypt.decrypt_data( KEY, self.data['passwords'][pos] ).decode('utf-8') for pos in range(length) ]
                websites = [ encrypt.decrypt_data( KEY, self.data['websites'][pos] ).decode('utf-8') for pos in range(length) ]
                
                # update data values
                self.data['usernames'] = usernames
                self.data['passwords'] = passwords
                self.data['websites'] = websites
                self.data['encrypted'] = False

                # print('[*] Decrypted Data successfully')

            else : 
                # print('[*] Data is already decrypted.')
                pass
            return True

    def get_user_pass(self):
        '''
        saves user password and other information to the database.
        This function is written for functions.py 
        '''
        data = db.get_dumped_user_data(self.usrname)
        if data:
            self.data = data
            return self.decrypt_info()

        # print(f'[!] Save some passwords for the user {self.usrname}')
        return False