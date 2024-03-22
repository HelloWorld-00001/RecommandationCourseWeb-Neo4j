from Helper.Helper import Helper as hp


class CompetencyDtos:

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

    def __init__(self,
                 knowledge="", platform="", tool="",
                 BASICPL="", INTERMEDIATEPL="", ADVANCEDPL="",
                 BASICFW="", INTERMEDIATEFW="", ADVANCEDFW=""):
        self.knowledge = knowledge
        self.platform = platform
        self.tool = tool
        self.BASICPL = BASICPL
        self.INTERMEDIATEPL = INTERMEDIATEPL
        self.ADVANCEDPL = ADVANCEDPL
        self.BASICFW = BASICFW
        self.INTERMEDIATEFW = INTERMEDIATEFW
        self.ADVANCEDFW = ADVANCEDFW

    def getCompetency(self, compeName, level = None):
        if compeName == "Knowledge": return self.knowledge
        elif compeName == "Platform": return self.platform
        elif compeName == "Tool": return self.tool
        elif compeName == "Framework":
            if level.upper() == "BASIC": return self.BASICFW
            elif level.upper() == "INTERMEDIATE": return self.INTERMEDIATEFW
            else: return self.ADVANCEDFW
        elif compeName == "ProgrammingLanguage":
            if level.upper() == "BASIC": return self.BASICPL
            elif level.upper() == "INTERMEDIATE": return self.INTERMEDIATEPL
            else: return self.ADVANCEDPL

        return "Undefined"
    
    def multiDictToSingleDict(self, dict):
        unique_values = set()
        for key in dict:
            unique_values.update(dict[key])

        return list(unique_values)
    

    def getCompetencyOriginal(self):
        competency = self.getCompetencyDtos()

        for com in ["ProgrammingLanguage", "Framework"]:
            competency[com] = self.multiDictToSingleDict(competency[com])
        
        return competency

    def getCompetencyDtos(self):
        competency = {}
        for com in hp.COMPETENCIES_LIST:
            if com in ["ProgrammingLanguage", "Framework"]:
                skill = {}
                for level in hp.getLevelList():
                    skill[level] = hp.detectStringToList(self.getCompetency(com, level))
                competency[com] = skill
            else:
                competency[com] = hp.detectStringToList(self.getCompetency(com))

        return competency
    
    def getCompetencyDtosFromUser(self, userDict):
        self.knowledge = userDict["Knowledge"]
        self.platform = userDict["Platform"]
        self.tool = userDict["Tool"]
        self.BASICPL = userDict["ProgrammingLanguage"]["BASIC"]
        self.INTERMEDIATEPL = userDict["ProgrammingLanguage"]["INTERMEDIATE"]
        self.ADVANCEDPL = userDict["ProgrammingLanguage"]["ADVANCED"]
        self.BASICFW = userDict["Framework"]["BASIC"]
        self.INTERMEDIATEFW = userDict["Framework"]["INTERMEDIATE"]
        self.ADVANCEDFW = userDict["Framework"]["ADVANCED"]

        return self
    
    def getTotalLen(self):
        lenght = 0
        Competency = self.getCompetencyOriginal()
        for com in Competency.keys():
            lenght += len(Competency[com])
        return lenght