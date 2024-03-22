from Model.BaseModel import BaseModel
from Helper.Helper import Helper as hp
from Helper.CompetencyHelper import CompetencyHelper as chp
import pandas as pd

class User(BaseModel): 
    username = ""
    password = ""
    email = ""
    phone = ""
    DOB = ""
    fullName = ""

    def __init__(self, username=None, password=None, email=None, phone=None, fullName=None, DOB=None):
        super().__init__()
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.fullName = fullName
        self.DOB = DOB


    def getListCol(self):

        return ["Username", "FullName", "Email", "Phone", "ProgrammingLanguage", "Tool", "Knowledge", "Platform", "Framework"]



    # convert user skill to list
    def getSkillList(self, userSkill, skillName, level=None):
        # if skill have no level, separate it to list
        if level is None or level == "No":
            if (type(userSkill[skillName]) == list):
                skill = userSkill[skillName].explode().unique()
                return [] if len(skill) < 1 else skill
            else:
                return userSkill[skillName]
        
        # else 
        skill = userSkill[(userSkill[skillName + "Level"] == level.upper())][skillName]
        skill = []  if len(skill) < 1 else skill.explode().unique()
        return skill
    
    def getUniqueData(self, data, column):
        # if skill have no level, separate it to list

        if data[column] is None or len(data[column]) < 1: return []

        if type(data[column].iloc[0]) == list:
            skill = data[column].dropna().explode().unique()
        else:
            skill = data[column].dropna().astype(str).explode().unique()
        return [] if len(skill) < 1 else skill


    def getUserSkill(self):

        query = f''' match(u:User)
        where toUpper(u.username) = \"{self.username.upper()}\"
        match(u)-[:Known_programmingLanguage]->(pl : ProgrammingLanguage)
        optional match(u)-[:Known_knowledge]->(kl: Knowledge)
        optional match(u)-[:Known_platform]->(pf: Platform)
        optional match(u)-[:Known_tool]->(tl: Tool)
        return u.username as Username, pl.programmingLanguage as ProgrammingLanguage, pl.level as ProgrammingLanguageLevel,
            collect(distinct kl.knowledge) as Knowledge, collect(distinct tl.tool) as Tool, 
            collect(distinct pf.platform) as Platform
        '''
        query2 = f''' match(u:User)
        where toUpper(u.username) = \"{self.username.upper()}\"
        match(u)-[:Known_framework]->(fw: Framework)
        return u.name as FullName, u.email as Email, u.phone as Phone , fw.framework as Framework, fw.level as FrameworkLevel
        '''
        userSkill = self.queryToDataFrame(query)
        userSkill2 = self.queryToDataFrame(query2)



        return pd.concat([userSkill, userSkill2], axis=1)
    

    # convert the return value of query to a dict with level: [list of programming languages]    
    def convertDict(self, skill):
        new_structure = {"BASIC": [], "INTERMEDIATE": [], "ADVANCED": []}

        # Iterating through the original dictionary
        for language, level in skill.items():
            # If the level is already a key in the new structure, append the language to its list
            new_structure[level.upper()].append(language)
        
        # convert a list of programings to a string (to display on the page)
        for col in new_structure.keys():
            new_structure[col] = ",".join(new_structure[col])

        # return the new dictionary

        return new_structure

    # convert the dict level: [list of programming languages]  to orginal programming languages: level

    def convertDictBack(self, dict, column):
        original_structure = {}
        for level, languages in dict[column].items():
            for language in languages:
                original_structure[language] = level

        return original_structure


    def getFullInfor(self):
        userSkill = self.getUserSkill()
        hp.printEntity(userSkill, "UserSkill", "User.py")

        userSkill["ProgrammingLanguageLevel"] = userSkill["ProgrammingLanguageLevel"].str.upper()
        userSkill['FrameworkLevel'] = userSkill['FrameworkLevel'].str.upper()

        userSkilldict = {}
        for com in self.getListCol():
            if (com == "ProgrammingLanguage" or com == "Framework"):
                skill={}
                for index, row in userSkill.iterrows():
                    if (pd.isna(row[com])): continue
                    level = row[com + "Level"] if row[com + "Level"] is not None else "Basic"
                    if row[com] in skill.keys():
                        rowLevel = skill[row[com]]
                        lowLevel = hp.getLowerLevel(level.upper(), rowLevel)
                        skill[row[com]] = level.upper() if rowLevel == lowLevel else rowLevel
                    else:
                        skill[row[com]] = level.upper()
                
                userSkilldict[com] = self.convertDict(skill)
            else:
                userSkilldict[com] = self.getUniqueData(userSkill, com)
        
        return userSkilldict
    
    def getUserDataString(self):
        userData = self.getFullInfor()
        for col in userData.keys():
            if (col == "ProgrammingLanguage" or col == "Framework"):
                for level in hp.getLevelList():
                    userData[col][level.upper()] = hp.list2String(userData[col][level.upper()])
                
            else:
                userData[col] = hp.list2String(userData[col])
        
        return userData

    
    def getUser(self):
        query = f''' match(u:User)
        where toUpper(u.username) = \"{self.username.upper()}\"
        
        return u.username as Username
        '''
        user = self.queryToDataFrame(query)
        return user
    
    # convert all competency to condition in neo4j
    def toNeo4jCondition(self, data, competencyColumn, sign):
        
        attrCol = competencyColumn[:1].lower() + competencyColumn[1:]

        if (type(data[competencyColumn]) != dict):
            if not data[competencyColumn] or len(data[competencyColumn]) > 0:
                return f"where {sign}.{attrCol} in {str( [item.upper() for item in data[competencyColumn]])}"  
        # Initialize an empty list to hold condition parts
        conditions = []

        # Iterate through the dictionary
        for level, languages in data[competencyColumn].items():
            # Skip levels with empty language lists
            if not languages:
                continue
            languages =    [item.upper() for item in languages]
            # Format the condition part for the current level and add it to the list
            condition = f"(toUpper({sign}.level) = '{level}' and {sign}.{attrCol} in {str(languages)})"
            conditions.append(condition)

        # Join all condition parts with ' or '
        final_condition = ' or '.join(conditions)

        # Wrap the entire condition in 'where' clause if it's not empty
        if final_condition:
            final_condition = 'where ' + final_condition

        return final_condition



    def updateUser(self, Competency):
        query = f''' match(u:User)
        where toUpper(u.username) = \"{self.username.upper()}\"
        optional match(pl : ProgrammingLanguage)  {self.toNeo4jCondition(Competency, "ProgrammingLanguage", "pl")} 
        optional match(kl: Knowledge)  {self.toNeo4jCondition(Competency, "Knowledge", "kl")}
        optional match(pf: Platform)  {self.toNeo4jCondition(Competency, "Platform", "pf")}
        optional match(tl: Tool)  {self.toNeo4jCondition(Competency, "Tool", "tl")}
        optional match(fw: Framework)  {self.toNeo4jCondition(Competency, "Framework", "fw")}
        set  u.name = \"{self.fullName}\", u.email = \"{self.email}\", u.phone = \"{self.phone}\"
        merge(u)-[:Known_knowledge]->(kl)
        merge(u)-[:Known_programmingLanguage]->(pl)
        merge(u)-[:Known_platform]->(pf)
        merge(u)-[:Known_tool]->(tl)
        merge(u)-[:Known_framework]->(fw)
        '''
        a = self.queryToDataFrame(query)
        return True
    



    

            
