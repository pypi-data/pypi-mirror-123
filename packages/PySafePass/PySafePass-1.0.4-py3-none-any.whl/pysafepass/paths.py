from os.path import join, dirname


root = dirname(__file__)

PASSWORD_DB = join(root,'db','passwords.db')
USER_DB = join(root,'db','users.db')

log_file = join(root,'logs','SafePass.log')

icon = join(root, '.images', 'safepass.png')
login_ui = join(root,'UI','login.ui')
create_acc_ui = join(root,'UI','CreateAccount.ui')
pass_table_ui = join(root,'UI','PasswordsTable.ui')
save_info_ui = join(root,'UI','SaveInfo.ui')

if __name__ == "__main__":
    print(root)
    print(log_file)