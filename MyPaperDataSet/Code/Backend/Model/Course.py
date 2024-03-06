from Model.BaseModel import BaseModel
from Helper.Helper import Helper as hp
from Model.Competency import Competency as cpt


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
        
        condition = Competency.makeCompetencyConditionAll()
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
            pf.platform as Platform
        '''

        courseList = self.queryToDataFrame(query)
        for col in ['Knowledge', 'Tool', 'Platform', 'Framework', 'ProgrammingLanguage']:
            courseList[col] = courseList[col].apply(lambda x: None if x == [] else x)
            
            
        courseList['Matched'] = 5 - courseList[hp.COMPETENCIES_LIST].isnull().sum(axis=1)
        courseList = courseList.fillna("-")

        sorted_result = courseList.sort_values(by=['Matched', 'Enroll', 'Rate'], ascending=[False, False, False]).reset_index()
        sorted_result = sorted_result.drop("index", axis=1)

        return sorted_result

    pass