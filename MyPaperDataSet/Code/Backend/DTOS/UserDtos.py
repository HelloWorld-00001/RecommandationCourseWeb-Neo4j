from Helper.Helper import Helper as hp


class UserDtos:


    username = "Unknown"
    fullName = ""
    email = ""
    phone = ""

    def __init__(self, username="Unknown", fullName="", email="", phone=""):
        self.username = username
        self.fullName = fullName
        self.email = email
        self.phone = phone

    
    def getUserDtos(self):
        return {"Username": self.username, "FullName": self.fullName, 
                "Email": self.email, "Phone": self.phone}