from Model.BaseModel import BaseModel
from Helper.Helper import Helper as hp


class Course(BaseModel): 
    

    def __init__(self, courseName="", courseLink="", courseDescription="", price=0, duration=0.0, enroll=0, rating=0.0, level=""):
        self.courseName = courseName
        self.courseLink = courseLink
        self.courseDescription = courseDescription
        self.price = price
        self.duration = duration
        self.enroll = enroll
        self.rating = rating
        self.level = level

    def findCourseByCompetency(self, Competency, filterCondition=None):
        
        condition = Competency.makeCompetencyConditionAllSpecial()
        if filterCondition is None: filterCondition = ""

        
        query = f''' match(f:FactCourse)-[:Belong_to_course]->(c:Course) {filterCondition}
        match(f)-[:Taught_programmingLanguage]->(pl : ProgrammingLanguage) {condition["ProgrammingLanguage"]}
        optional match(f)-[:Taught_knowledge]->(kl: Knowledge) {condition["Knowledge"]}
        optional match(f)-[:Taught_platform]->(pf: Platform) {condition["Platform"]}
        optional match(f)-[:Taught_tool]->(tl: Tool) {condition["Tool"]}
        optional match(f)-[:Taught_framework]->(fw: Framework) {condition["Framework"]}
        return c.name as CourseName, c.link as Link, c.level as Level, c.duration as Duration, c.price as Price, f.enroll as Enroll, f.rating as Rate,
            pl.programmingLanguage as ProgrammingLanguage,
            kl.knowledge as Knowledge, fw.framework as Framework,  tl.tool as Tool, 
            pf.platform as Platform, id(f) as ID
        '''

        courseList = self.queryToDataFrame(query)
        for col in ['Knowledge', 'Tool', 'Platform', 'Framework', 'ProgrammingLanguage']:
            courseList[col] = courseList[col].apply(lambda x: None if x == [] else x)
            
            
        courseList['Matched'] = 5 - courseList[hp.COMPETENCIES_LIST].isnull().sum(axis=1)
        courseList = courseList.fillna("-")

        sorted_result = courseList.sort_values(by=['Matched', 'Enroll', 'Rate'], ascending=[False, False, False]).reset_index()
        sorted_result = sorted_result.drop("index", axis=1)

        courseListUnique = sorted_result["ID"].unique().tolist()

        query2 = f''' match(f:FactCourse)-[:Taught_programmingLanguage]->(pl : ProgrammingLanguage)
        where id(f) in {str(courseListUnique)}
        optional match(f)-[:Taught_knowledge]->(kl: Knowledge) 
        optional match(f)-[:Taught_platform]->(pf: Platform) 
        optional match(f)-[:Taught_tool]->(tl: Tool)
        optional match(f)-[:Taught_framework]->(fw: Framework)
        return id(f) as ID,
            collect(distinct pl.programmingLanguage) as ProgrammingLanguage,
            collect(distinct kl.knowledge) as Knowledge, collect(distinct fw.framework) as Framework, 
            collect(distinct tl.tool) as Tool, collect(distinct pf.platform) as Platform
        '''
        sortCourseClean = sorted_result.drop(hp.COMPETENCIES_LIST, axis=1)
        courseData = self.queryToDataFrame(query2)
        res = sortCourseClean.merge(courseData, on="ID")
        res = res.drop_duplicates(subset=["ID"])
        return res.drop("ID", axis=1)


    
    def consultCourseByCompetency(self, Competency, level ="BASIC"):

        plCondition = hp.makeCompetencyConditon("programmingLanguage", "pl", Competency["ProgrammingLanguage"])
        klCondition = hp.makeCompetencyConditon("knowledge", "kl", Competency["Knowledge"])
        pfCondition = hp.makeCompetencyConditon("platform", "pf", Competency["Platform"])
        tlCondition = hp.makeCompetencyConditon("tool", "tl", Competency["Tool"])
        fwCondition = hp.makeCompetencyConditon("framework", "fw", Competency["Framework"])

        levelCondition = f"where toUpper(c.level) = \"{level.upper()}\""

        query = f''' match(f:FactCourse)-[:Belong_to_course]->(c:Course) {levelCondition}
        optional match(f)-[:Taught_programmingLanguage]->(pl : ProgrammingLanguage) {plCondition}
        optional match(f)-[:Taught_knowledge]->(kl: Knowledge) {klCondition}
        optional match(f)-[:Taught_platform]->(pf: Platform) {pfCondition}
        optional match(f)-[:Taught_tool]->(tl: Tool) {tlCondition}
        optional match(f)-[:Taught_framework]->(fw: Framework) {fwCondition}
        return c.name as CourseName, c.link as Link, c.level as Level, c.duration as Duration, 
            c.price as Price, f.enroll as Enroll, f.rating as Rate, id(f) as ID,
            collect(distinct pl.programmingLanguage) as ProgrammingLanguage,
            collect(distinct kl.knowledge) as Knowledge, collect(distinct fw.framework) as Framework, 
            collect(distinct tl.tool) as Tool, collect(distinct pf.platform) as Platform
        '''

        courseList = self.queryToDataFrame(query)
        for col in ['Knowledge', 'Tool', 'Platform', 'Framework', 'ProgrammingLanguage']:
            courseList[col] = courseList[col].apply(lambda x: None if x == [] else x)
        

        courseList[["MatchedCol", "MatchedSkill"]] = courseList.apply(lambda x: hp.getMatchedSkill(Competency, x), axis=1, result_type="expand")

        sortCourse = courseList.sort_values(by=['MatchedCol','MatchedSkill' ,'Enroll', 'Rate'], ascending=[False, False,False, False]).reset_index().head(5).drop("index", axis=1)

        courseListUnique = sortCourse["ID"].unique().tolist()

        query2 = f''' match(f:FactCourse)-[:Taught_programmingLanguage]->(pl : ProgrammingLanguage)
        where id(f) in {str(courseListUnique)}
        optional match(f)-[:Taught_knowledge]->(kl: Knowledge) 
        optional match(f)-[:Taught_platform]->(pf: Platform) 
        optional match(f)-[:Taught_tool]->(tl: Tool)
        optional match(f)-[:Taught_framework]->(fw: Framework)
        return id(f) as ID,
            collect(distinct pl.programmingLanguage) as ProgrammingLanguage,
            collect(distinct kl.knowledge) as Knowledge, collect(distinct fw.framework) as Framework, 
            collect(distinct tl.tool) as Tool, collect(distinct pf.platform) as Platform
        '''
        sortCourseClean = sortCourse.drop(hp.COMPETENCIES_LIST, axis=1)
        courseData = self.queryToDataFrame(query2)
        res = sortCourseClean.merge(courseData, on="ID")
        return res

    def getListRecommandCourse(self, skillToLearn):
        
        recommand = {}
        recommandCourse = []

        for index, row in skillToLearn.iterrows():
            recommand["Require"] = row
            recommand["CoursePath"] = [[], [], [], []]
            level = hp.getLowerLevel(row["ProgrammingLanguageLevel"], row["FrameworkLevel"])
            while (level != "OK"):
                rowData = self.consultCourseByCompetency(row, level)
                rowSize = len(rowData)
                if (rowSize < 1): break

                for i in range(0, 4):
                    recommand["CoursePath"][i].append(rowData.iloc[i%rowSize])

                level = hp.getUpperLevel(level)

            recommandCourse.append(recommand)
            
        
        return recommandCourse

    def printCoursePath(self, skillToLearn):
        recommandCourse = self.getListRecommandCourse(skillToLearn)
        for coursePath in recommandCourse:
            print("\n--------------------------------")
            print("Require: ")
            print(coursePath["Require"]["CareerName"])
            print("\n---- Start Course Path ----")
            for course in coursePath["CoursePath"]:
                print(f"CoursePath: ")

                for subCourse in course:
                    print(subCourse["CourseName"] + "Level: " + subCourse["Level"])
                    print("-->")
            
                print("---- End Path ----\n")

            print("--------------------------------\n")
        return recommandCourse

