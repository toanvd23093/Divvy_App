import re

class User():
    def __init__(self, userEmail, userPassword, userFirstName, userLastName):
        self.userEmail = userEmail
        self.userPassword = userPassword
        self.userFirstName = userFirstName
        self.userLastName = userLastName

    def __str__(self):
        return f"First Name: {self.userFirstName}. Last Name: {self.userLastName}. Email: {self.userEmail}. Password: {self.userPassword}"

    @property
    def userEmail(self):
        return self._userEmail
    
    @userEmail.setter
    def userEmail(self,userEmail):
        pattern = r'[a-zA-Z0-9_\.\-]+@[a-z]+\.[a-z]+$'

        if not re.match(pattern,userEmail):
            raise ValueError("Email Format is not valid. Valid format should be john-doe@gmail.com")
        
        self._userEmail = userEmail

    @property
    def userPassword(self):
        return self._userPassword
    
    @userPassword.setter
    def userPassword(self,userPassword):
        if len(userPassword) <= 5:
            raise ValueError("Password should have more than 5 letters")
        
        self._userPassword = userPassword

    @property
    def userFirstName(self):
        return self._userFirstName
    
    @userFirstName.setter
    def userFirstName(self,userFirstName):
        pattern = r'^(?!.*  )[a-zA-Z\-\s]+$'

        if not re.match(pattern,userFirstName):
            raise ValueError("There should not be any special character in first name")
 
        self._userFirstName = userFirstName

    @property
    def userLastName(self):
        return self._userLastName
    
    @userLastName.setter
    def userLastName(self,userLastName):
        pattern = r'^(?!.*  )[a-zA-Z\-\s]+$'

        if not re.match(pattern,userLastName):
            raise ValueError("There should not be any special character in last name")
        
        self._userLastName = userLastName