import sqlite3
import sys
from pysafepass.paths import PASSWORD_DB, USER_DB


def add_user(usrname:str, password_hash:str)->bool:
    '''
    adds username and its password hash to the password db.
    '''
    try:
        pass_con = sqlite3.connect(PASSWORD_DB)
        pass_cur = pass_con.cursor()
        pass_cur.execute('CREATE TABLE IF NOT EXISTS password_hashes (NAME TEXT, KEY TEXT)')
        pass_cur.execute("INSERT INTO password_hashes VALUES (?,?)",(usrname, password_hash))
        pass_con.commit()
        pass_con.close()
        # print(f'[*] Successfully added password hash to db of user {usrname}')
        return True
    except Exception as e:
        # print('[-] Exception : ', e) 
        return False


def get_pass_hash(usrname:str)->str:
    '''
    searches for password hash in the password db for specific usrname 
    and returns passwd_hash as string
    '''
    try:
        pass_con = sqlite3.connect(PASSWORD_DB)
        pass_cur = pass_con.cursor()

        # fetch password hash for usrname from password_hashes table
        pass_cur.execute('SELECT KEY FROM password_hashes WHERE NAME=?', (usrname,))
        passwd_hash = pass_cur.fetchone()

        if passwd_hash is not None:
            # if row is not none then acc is found and fetched the password hash
            # print('[*] Password hash fetched successfully from password db for user ' + usrname)
            return passwd_hash[0]
        else :
            # return empty string if acc not found
            # print('[!] No Account Found.')
            # print('[!] No Account Found.')
            return ''
    except sqlite3.OperationalError as e:
        # print('[!] Trying to fetch without creating user.')
        # print('[!] Trying to fetch without creating user.')
        pass
    except Exception as e:
        # print('[-] Exception : ', e) 
        pass


def get_saved_users():
    '''
    returns list of user names stored in password database.
    '''
    try:
        pass_con = sqlite3.connect(PASSWORD_DB)
        pass_cur = pass_con.cursor()
        pass_cur.execute('SELECT NAME FROM password_hashes')
        usernames = pass_cur.fetchall()
        
        # extract user names
        users = []
        for username in usernames:
            users.append(username[0])

        return users
    except Exception as e:
        # print('[!] Try creating user before logging in.')
        # print(f'[-] Exception in get_save_users: {e}')
        # print(f'[-] Exception in get_save_users: {e}. Exiting program')
        # print('[-] Closing SafePass')
        sys.exit()



def dump_user_data(data:dict, name:str)->bool:
    '''
    dumps user data to the database.
    takes encrypted data(dict) and name(str) 
    '''
    # print('[*] Starting to dump user data into database.')
    # extracting information from the data dictionary if data is encrypted:
    if data['encrypted']:
        usernames = data['usernames']
        websites = data['websites']
        passwords = data['passwords']
        max_count = len(usernames)

        # creating user.db
        user_con = sqlite3.connect(USER_DB)
        user_cur = user_con.cursor()
        user_cur.execute(f'DROP TABLE IF EXISTS {name}')
        user_cur.execute(f'CREATE TABLE IF NOT EXISTS {name} (USERNAMES TEXT, WEBSITES TEXT, PASSWORDS TEXT)')

        # insert values to users database
        for pos in range(max_count):
            user_con.execute(f'INSERT INTO {name}(USERNAMES, WEBSITES, PASSWORDS) VALUES(?,?,?)', (usernames[pos], websites[pos], passwords[pos], ) )

        user_con.commit()
        user_con.close()
        # print(f'[*] {name} data successfully dumped to user database.')
        return True
        
    else:
        # print('[!] Encrypt data before saving.')
        # print('[!] Encrypt data before saving.')

        return False


def get_dumped_user_data(name:str)->dict:
    '''
    get dumped user data from users database. 
    takes encrypted name(str
    ).
    '''
    # print('[*] Fetching dumped user data')
    try:
        # connect to db and create cursor
        user_con = sqlite3.connect(USER_DB)
        user_cur = user_con.cursor()
        
        # extracting information from the users database.
        user_cur.execute(f'SELECT * FROM {name}')

        # raw data = [(username, website, password), ....]
        raw_data = user_cur.fetchall()

        if raw_data:
            max_count = len(raw_data)

            # create empty list to save encrypted data
            data = {
            'encrypted': True,
            'passwords': [],
            'usernames': [],
            'websites': []
            }

            # append raw data to data
            for pos in range(max_count):
                data['usernames'].append(raw_data[pos][0])
                data['websites'].append(raw_data[pos][1])
                data['passwords'].append(raw_data[pos][2])

            user_con.close()

            return data
        else :
            # returning empty string if no data is available
            # print(f'[!] No saved data available for {name}')
            # print('[*] Save passwords before fetching them.')

            # print(f'[!] No saved data available for {name}')
            return dict()
    except sqlite3.OperationalError:
         # returning empty string if no data is available
        # print(f'[!] No saved data available for {name}')
        # print('[*] Save information before fetching them.')

        # print(f'[!] No saved data available for {name}')
        return dict()
