uri = "bolt://localhost:7687"  # Adjust the URI based on your Neo4j server configuration
username = "neo4j"
password = "12345678"
import numpy
import pandas as pd

class Helper():

    def getLevelList():

        return ["Basic", "Intermediate", "Advanced"]

    def toUpperList(list):
        upperList =  '[' + ', '.join(f'"{item.strip().upper()}"' for item in list) + ']'

        return upperList
    def emptyProcess(data, column):
        for col in column:
            data[col] = data[col].apply(lambda x: None if x == [] else x)
        
    def detectStringToList(string):
        if string == '': return []
        data = string.split(",")
        return data
    
    def getUpperLevel(level):
        if level == "BASIC": return "INTERMEDIATE"
        elif level == "INTERMEDIATE": return "ADVANCED"
        else: return "OK"

    def emptyProcess(data, column):
        for col in column:
            data[col] = data[col].apply(lambda x: None if x == [] else x)
        return data
    
    def getMatchedCompeLen(data):
        res = 0
        if (data["ProgrammingLanguage"] is not None): res = res + 1
        if (data["Framework"] is not None): res = res + 1
        if data["Tool"] is not None: res = res + len(data["Tool"])
        if (data["Knowledge"] is not None): res = res + len(data["Knowledge"])
        if (data["Platform"] is not None): res = res + len(data["Platform"])

        return res
    
    def makeCompetencyConditon(CompetencyAttr, sign, CompeValue):
        if (CompeValue is None or len(CompeValue) < 1):
            return ""
        
        equaration = "in"
        if type(CompeValue) == str:
            return ""
    
        st = '[' + ', '.join(f'"{item.strip().upper()}"' for item in CompeValue) + ']'
        where = f"where {sign}.{CompetencyAttr} {equaration} {st}"

        return where
    
    def removeFromList(self, row, deleteList):
        if row is None: return None
        if len(deleteList) == 0: return row
        return [item for item in row if item not in deleteList]

    def getLevel(self, lang, skill):
        if lang is None: return None
        level = skill.get(lang.upper(), 'NEW')
        if level == 'NEW': return "BASIC"
        elif level.upper() == 'BASIC': return "INTERMEDIATE"
        elif level.upper() == 'INTERMEDIATE': return "ADVANCED"
        else: return "OK"

    def list2String(listVal):
        if type(listVal) == str: return listVal
        if type(listVal) == list or type(listVal) == numpy.ndarray:
            return ",".join(listVal)
        return str(listVal)

    def getLowerLevel(level1, level2):
        # Dictionary to map string levels to numeric values
        level_mapping = {
            'BASIC': 1,
            'INTERMEDIATE': 2,
            'ADVANCED': 3,
            'OK': 4
        }
        
        # Convert the level strings to their corresponding numeric values
        value1 = level_mapping.get(level1.lower(), 0)  # Use None for not found
        value2 = level_mapping.get(level2.lower(), 0)
        
        # Determine and return the lower level
        if value1 < value2:
            return level1
        elif value1 > value2:
            return level2
        else:
            return level1

    def getLowerLevelOfPandasRow(row):
        level1 = row["ProgrammingLanguageLevel"]
        level2 = row["FrameworkLevel"]
        # Dictionary to map string levels to numeric values
        level_mapping = {
            'BASIC': 1,
            'INTERMEDIATE': 2,
            'ADVANCED': 3,
            'OK': 4
        }
        
        # Convert the level strings to their corresponding numeric values
        value1 = level_mapping.get(level1, 0)  # Use None for not found
        value2 = level_mapping.get(level2, 0)
        
        # Determine and return the lower level
        if value1 < value2:
            return pd.Series([level1, value1])
        else:
            return pd.Series([level2, value2])
        


    def getUpperLevel(level):
        if level == "BASIC": return "INTERMEDIATE"
        elif level == "INTERMEDIATE": return "ADVANCED"
        else: return "OK"

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
    
    
    def printString(string):

        print("\n-------------------------------------------")
        print("|")
        print(">>> " + string + " <<<")
        print("|")
        print("-------------------------------------------")
    
    def printEntity(entity, title="Nope", location="Nope"):

        print("\n-------------------------------------------")
        print(">> Title: " + title + " <<<")
        print(">> Location: " + location + " <<<")
        print("| \t <<<  content  >>>\t |")
        print(entity)
        print("|")
        print("-------------------------------------------")

    
    COMPETENCIES_LIST = ["Knowledge", "Platform", "Framework", "ProgrammingLanguage", "Tool"]

    
    
            
