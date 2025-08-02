from cryptography.fernet import Fernet

class SiteAuth(object):

    site = ""
    username = ""
    password = ""

    def __init__(self, site, username, password):
        self.site = site
        self.username = username
        self.password = password
    
    def __str__(self):
        return f"Website: {self.site}\nUsername: {self.username}\nPassword: {self.password}"

    def toCSV(self):
        return f"{self.site},{self.username},{self.password},\n"
    
    def decode(self, key):
        try:
            f = Fernet(key)
            self.username = f.decrypt(self.username).decode()
            self.password = f.decrypt(self.password).decode()
        except:
            print("[Exception] Wrong key")

    @staticmethod
    def parseSiteAuth(csv):
        site, username, password, eol = csv.split(",")
        return SiteAuth(site, username, password)


# main
c = ""
while c != "0":
    c = input('''
    1. Login
    2. Register
    ''')
    match c:
        case "1":
            passkey = input("Insert the password:\n")
            passkey = passkey.encode()
            auths = []
            point = open("./.vault", "a")
            point.close()
            point = open("./.vault", "r")
            list = point.readlines()
            for e in list:
                auths.append(SiteAuth.parseSiteAuth(e))
            point.close()
            choice = ""
            while choice != "0":
                choice = input('''
                1. Add a new password
                2. View a site password
                3. Remove a password
                0. Exit
                ''')
                match choice:
                    case "1":
                        site = input("Insert the url:\n")
                        username = input("Insert the username:\n")
                        password = input("Insert the password:\n")
                        f = Fernet(passkey)
                        username = f.encrypt(username.encode())
                        password = f.encrypt(password.encode())
                        for auth in auths:
                            if auth.site == site:
                                print("Password already exists")
                                break
                        else:
                            auths.append(SiteAuth(site, username, password))
                            print("Password added")
                    case "2":
                        site = input("Insert the url:\n")
                        found = False
                        for auth in auths:
                            if auth.site == site:
                                temp = SiteAuth(auth.site, auth.username, auth.password)
                                temp.decode(passkey)
                                found = True
                                print(temp)
                                break                            
                        if not found:
                            print("Site not found")
                    case "3":
                        site = input("Insert the url:\n")
                        for auth in auths:
                            if auth.site == site:
                                auths.remove(auth)
                                print("Password removed")
                                break
                    case "0":
                        point = open("./.vault", "w")
                        for auth in auths:
                            point.write(auth.toCSV())
                        point.close()
                        print("Goodbye!")
                        break
                    case _:
                        print("Invalid choice")
            break
        case "2":
            key = Fernet.generate_key()
            print(f"Your master password: {key.decode()}")
            break
        case _:
            c="0"
            print("Goodbye!")
            break