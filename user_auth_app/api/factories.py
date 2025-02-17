class RegistrationData:
    def __init__(self,token, username, first_name, last_name, is_staff, email ):
        self.token = token
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.is_staff = is_staff
        self.email = email 
        

class LoginData:
    def __init__(self, token, username, first_name, last_name, user_id, email):
       self.token = token
       self.username = username
       self.first_name = first_name
       self.last_name = last_name
       self.user_id = user_id
       self.email = email 
    