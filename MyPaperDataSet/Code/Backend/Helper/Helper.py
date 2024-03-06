uri = "bolt://localhost:7687"  # Adjust the URI based on your Neo4j server configuration
username = "neo4j"
password = "12345678"

class Helper():

    def toUpperList(list):
        upperList =  '[' + ', '.join(f'"{item.strip().upper()}"' for item in list) + ']'

        return upperList
    def emptyProcess(data, column):
        for col in column:
            data[col] = data[col].apply(lambda x: None if x == [] else x)
        
    def detectStringToList(string):
        data = string.split(",")
        return data
    

    def emptyProcess(data, column):
        for col in column:
            data[col] = data[col].apply(lambda x: None if x == [] else x)
        return data
    
    def printString(string):

        print("\n-------------------------------------------")
        print("|")
        print(">>> " + string + " <<<")
        print("|")
        print("-------------------------------------------")
    
    def printEntity(entity):

        print("\n-------------------------------------------")
        print("|")
        print(entity)
        print("|")
        print("-------------------------------------------")

    
    COMPETENCIES_LIST = ["Knowledge", "Platform", "Framework", "ProgrammingLanguage", "Tool"]

    
    
            
