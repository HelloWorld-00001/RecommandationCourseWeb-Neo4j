
from Helper.Helper import Helper as hp
from Model.Course import Course
from Model.Job import Job


class CompetencyController():
    competencies = {}
    def __init__(self, programmingLanguage, framework, knowledge, platform, tool):
        self.competencies["ProgrammingLanguage"] = hp.detectStringToList(programmingLanguage)
        self.competencies["Framework"] =  hp.detectStringToList(framework)
        self.competencies["Knowledge"] =  hp.detectStringToList(knowledge)
        self.competencies["Platform"] =  hp.detectStringToList(platform)
        self.competencies["Tool"] =  hp.detectStringToList(tool)

    CompetencyAttr ={"ProgrammingLanguage": ["ProgrammingLanguage", "programmingLanguage", "pl"], 
                     "Framework": ["Framework", "framework", "fw"], 
                     "Knowledge": ["Knowledge", "knowledge", "kl"], 
                     "Platform": ["Platform", "platform", "pf"], 
                     "Tool": ["Tool", "tool", "tl"]}
    
    def getCompetency(self):
        return self.competencies
    
    def getCompetencyList(self):

        return ["ProgrammingLanguage", "Framework", "Knowledge", "Platform", "Tool"]

    def getMatchedCompeLen(data):
        res = 0
        if (data["ProgrammingLanguage"] is not None): res = res + 1
        if (data["Framework"] is not None): res = res + 1
        res = res + len(data["Tool"]) + len(data["Knowledge"]) + len(data["Platform"])

        return res
    

    def getTotalLen(self):
        lenght = 0
        for com in self.CompetencyAttr:
            lenght += len(self.competencies[com])
        return lenght
    
    
    def makeCompetencyCondition(self, CompetencyAttr, sign, CompeValue):
        # Assuming hp.toUpperList is a method from another module or a static method defined elsewhere
        if CompeValue is None or len(CompeValue) < 1:
            return ""
        where = f"where {sign}.{CompetencyAttr} in {hp.toUpperList(CompeValue)}"
        return where
    
    def makeCompetencyConditionSpecial(self, CompetencyAttr, sign, CompeValue):
        # Assuming hp.toUpperList is a method from another module or a static method defined elsewhere
        if CompeValue is None or len(CompeValue) < 1:
            return f'where {sign}.{CompetencyAttr} = \"hahaha\"'
        where = f"where {sign}.{CompetencyAttr} in {hp.toUpperList(CompeValue)}"
        return where

    
    def makeCompetencyConditionAll(self):
        conditions = {}
        # Since makeCompetencyConditon is now a static method, it should be called directly on the class
        for com in self.CompetencyAttr:
            conditions[self.CompetencyAttr[com][0]] = self.makeCompetencyCondition(self.CompetencyAttr[com][1], self.CompetencyAttr[com][2], self.competencies[com])

        return conditions
    
    def makeCompetencyConditionAllSpecial(self):
        conditions = {}
        # Since makeCompetencyConditon is now a static method, it should be called directly on the class
        for com in self.CompetencyAttr:
            conditions[self.CompetencyAttr[com][0]] = self.makeCompetencyConditionSpecial(self.CompetencyAttr[com][1], self.CompetencyAttr[com][2], self.competencies[com])

        return conditions

