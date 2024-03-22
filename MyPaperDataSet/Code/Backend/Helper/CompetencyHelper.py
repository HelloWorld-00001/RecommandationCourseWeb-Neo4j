
from Helper.Helper import Helper as hp


class CompetencyHelper():
   
    CompetencyAttr ={"ProgrammingLanguage": ["ProgrammingLanguage", "programmingLanguage", "pl"], 
                     "Framework": ["Framework", "framework", "fw"], 
                     "Knowledge": ["Knowledge", "knowledge", "kl"], 
                     "Platform": ["Platform", "platform", "pf"], 
                     "Tool": ["Tool", "tool", "tl"]}
    
    
    
    def getCompetencyList():

        return ["ProgrammingLanguage", "Framework", "Knowledge", "Platform", "Tool"]

    def getMatchedCompeLen(data):
        res = 0
        if (data["ProgrammingLanguage"] is not None): res = res + 1
        if (data["Framework"] is not None): res = res + 1
        res = res + len(data["Tool"]) + len(data["Knowledge"]) + len(data["Platform"])

        return res
    

    def getTotalLen(Competency: dict):
        lenght = 0
        for com in Competency.keys():
            lenght += len(Competency[com])
        return lenght
    
    
    def makeCompetencyCondition(self, CompetencyAttr, sign, CompeValue):
        # Assuming hp.toUpperList is a method from another module or a static method defined elsewhere
        if CompeValue is None or len(CompeValue) < 1:
            return ""
        where = f"where {sign}.{CompetencyAttr} in {hp.toUpperList(CompeValue)}"
        return where
    
    def makeCompetencyConditionStatic(CompetencyAttr, sign, CompeValue):
        # Assuming hp.toUpperList is a method from another module or a static method defined elsewhere
        if CompeValue is None or len(CompeValue) < 1:
            return ""
        where = f"where {sign}.{CompetencyAttr} in {hp.toUpperList(CompeValue)}"
        return where
    
    def makeCompetencyConditionSpecial(CompetencyAttr, sign, CompeValue):
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
    
    # process comptency dict for dict like {key: [list]}
    def makeCompetencyConditionAllSpecial(CompetencyDict:dict):
        hp.printEntity(CompetencyDict, "CompetencyDict", "CompetencyHelper.py")

        conditions = {}

        CompetencyAttr ={"ProgrammingLanguage": ["ProgrammingLanguage", "programmingLanguage", "pl"], 
                     "Framework": ["Framework", "framework", "fw"], 
                     "Knowledge": ["Knowledge", "knowledge", "kl"], 
                     "Platform": ["Platform", "platform", "pf"], 
                     "Tool": ["Tool", "tool", "tl"]}

        # Since makeCompetencyConditon is now a static method, it should be called directly on the class
        for com in CompetencyDict.keys():
            sign = CompetencyAttr[com][2]
            attr = CompetencyAttr[com][1]
            
            if CompetencyDict[com] is None or len(CompetencyDict[com]) < 1:
                conditions[com] =  "" #f'where {sign}.{attr} = \"hahaha\"'
            else:
                conditions[com] = f"where {sign}.{attr} in {hp.toUpperList(CompetencyDict[com])}"

        
        return conditions

   

    def getMatchedSkill(skill, data):
        res = 0
        for com in ["ProgrammingLanguage", "Framework", "Tool"]:
            if skill[com] is None or data[com] is None: continue

            if skill[com] in data[com]: res = res + 1

        matchedSkill = res

        for com in ["Knowledge", "Platform"]:
            if skill[com] is None or data[com] is None: continue
            l = len(set(skill[com]) & set(data[com])) 
            if l > 0:
                res = res + 1
                matchedSkill += l
        return res, matchedSkill
