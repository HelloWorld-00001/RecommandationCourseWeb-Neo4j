from Helper.Helper import Helper as hp
from Model.Course import Course
from Model.Job import Job
from Model.User import User
from Controller.CompetencyController import CompetencyController as cc

class LoginController():

    username = "Unknown"
    password = ""
    user = User()

    def __init__(self, username="", password=""):
        self.username = username
        self.password = password
        self.user = User(self.username, self.password)


    def login(self):

        userE = self.user.getUser()
        if userE is None or len(userE) < 1:
            return False
        else:
            return True
        
    def getUserData(self):
        userData = self.user.getUserDataString()
        return userData

    def getUsername(self):
        return self.username
