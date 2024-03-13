from Helper.Helper import Helper as hp
from Model.Course import Course
from Model.Job import Job
from Model.User import User
from Controller.CompetencyController import CompetencyController as cc

class ProfileController():

    username = ""
    fullName = ""
    email = ""
    phone = ""

    # competency getter
    knowlege = ""
    platform = ""
    tool = ""

    # special comptency
    BASICPL = ""
    INTERMEDIATEPL = ""
    ADVANCEDPL = ""

    BASICFW = ""
    INTERMEDIATEFW = ""
    ADVANCEDFW = ""

    def __init__(self, username="", email="", phone="", fullname="",
                 knowledge="", platform="", tool="",
                 BASICPL="", INTERMEDIATEPL="", ADVANCEDPL="",
                 BASICFW="", INTERMEDIATEFW="", ADVANCEDFW=""):
        self.username = username
        self.email = email
        self.phone = phone
        self.fullName = fullname
        self.knowledge = knowledge
        self.platform = platform
        self.tool = tool
        self.BASICPL = BASICPL
        self.INTERMEDIATEPL = INTERMEDIATEPL
        self.ADVANCEDPL = ADVANCEDPL
        self.BASICFW = BASICFW
        self.INTERMEDIATEFW = INTERMEDIATEFW
        self.ADVANCEDFW = ADVANCEDFW


    def toUserSkill(self):
        userDict = {}
        userDict["Knowledge"] = hp.detectStringToList(self.knowledge)
        userDict["Platform"] = hp.detectStringToList(self.platform)
        userDict["Tool"] = hp.detectStringToList(self.tool)

        plDict = {}
        fwDict = {}
        
        plDict["BASIC"] = hp.detectStringToList(self.BASICPL)
        plDict["INTERMEDIATE"] = hp.detectStringToList(self.INTERMEDIATEPL)
        plDict["ADVANCED"] = hp.detectStringToList(self.ADVANCEDPL)

        fwDict["BASIC"] = hp.detectStringToList(self.BASICFW)
        fwDict["INTERMEDIATE"] = hp.detectStringToList(self.INTERMEDIATEFW)
        fwDict["ADVANCED"] = hp.detectStringToList(self.ADVANCEDFW)
        userDict["ProgrammingLanguage"] = plDict
        userDict["Framework"] = fwDict
        self.removeDuplicatesBasedOnHierarchy(userDict)
        return userDict

    def removeDuplicatesBasedOnHierarchy(self, data):
        # Define the hierarchy order
        hierarchy = ['ADVANCED', 'INTERMEDIATE', 'BASIC']
        
        for key in data.keys():
            if (key not in ["ProgrammingLanguage", "Framework"]): continue
            # Temporarily store items in a set for comparison, to avoid duplicates
            seen = set()
            
            # Iterate according to the hierarchy (from highest to lowest)
            for level in hierarchy:
                current_level_items = data[key][level]
                
                # If the current level items are not in a list form (e.g., empty string), skip
                if not isinstance(current_level_items, list):
                    continue
                
                # Add current level items to the seen set (since they have the highest precedence)
                new_items = []
                for item in current_level_items:
                    if item not in seen:
                        seen.add(item)
                        new_items.append(item)
                        
                # Update the current level with items not previously seen in higher levels
                data[key][level] = new_items
                
                # For lower levels, remove any items that have been seen in higher levels
                for lower_level in hierarchy[hierarchy.index(level)+1:]:
                    lower_level_items = data[key][lower_level]
                    # Skip if not in list form
                    if not isinstance(lower_level_items, list):
                        continue
                    data[key][lower_level] = [item for item in lower_level_items if item not in seen]
        

    def updateProfile(self):
        user = User(self.username, None, self.email, self.phone, self.fullName)
        userSkill = self.toUserSkill()
        user.updateUser(userSkill)
        return True
