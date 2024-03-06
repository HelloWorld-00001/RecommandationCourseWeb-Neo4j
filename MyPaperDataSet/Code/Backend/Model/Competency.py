from Model.BaseModel import BaseModel
from Helper.Helper import Helper as hp

class Competency(BaseModel):

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
    
    @staticmethod
    def makeCompetencyConditonStatic(CompetencyAttr, sign, CompeValue):
        # Assuming hp.toUpperList is a method from another module or a static method defined elsewhere
        if CompeValue is None or len(CompeValue) < 1:
            return ""
        where = f"where {sign}.{CompetencyAttr} in {hp.toUpperList(CompeValue)}"
        return where
    
    def makeCompetencyConditon(self, CompetencyAttr, sign, CompeValue):
        # Assuming hp.toUpperList is a method from another module or a static method defined elsewhere
        if CompeValue is None or len(CompeValue) < 1:
            return ""
        where = f"where {sign}.{CompetencyAttr} in {hp.toUpperList(CompeValue)}"
        return where

    @staticmethod
    def makeCompetencyConditionAllStatic(CompetencyVal):

        # Since makeCompetencyConditon is now a static method, it should be called directly on the class
        plCondition = Competency.makeCompetencyConditonStatic("programmingLanguage", "pl", CompetencyVal["ProgrammingLanguage"])
        klCondition = Competency.makeCompetencyConditonStatic("knowledge", "kl", CompetencyVal["Knowledge"])
        pfCondition = Competency.makeCompetencyConditonStatic("platform", "pf", CompetencyVal["Platform"])
        tlCondition = Competency.makeCompetencyConditonStatic("tool", "tl", CompetencyVal["Tool"])
        fwCondition = Competency.makeCompetencyConditonStatic("framework", "fw", CompetencyVal["Framework"])
        return plCondition, fwCondition, klCondition, pfCondition, tlCondition
    
    def makeCompetencyConditionAll(self):
        conditions = {}
        # Since makeCompetencyConditon is now a static method, it should be called directly on the class
        for com in self.CompetencyAttr:
            conditions[com[0]] = self.makeCompetencyCondition(com[1], com[2], self.competencies[com[0]])

        return conditions
