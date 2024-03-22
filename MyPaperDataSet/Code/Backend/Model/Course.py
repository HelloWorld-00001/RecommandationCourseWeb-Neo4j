from Model.BaseModel import BaseModel
from Helper.Helper import Helper as hp
from Helper.CompetencyHelper import CompetencyHelper as chp
import pandas as pd

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

    def findCourseByCompetencyController(self, Competency, filterCondition=None):
        
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


    
    def findCourseByCompetency(self, Competency: pd.DataFrame(), level ="BASIC"):

        plCondition = chp.makeCompetencyConditionStatic("programmingLanguage", "pl", Competency["ProgrammingLanguage"])
        klCondition = chp.makeCompetencyConditionStatic("knowledge", "kl", Competency["Knowledge"])
        pfCondition = chp.makeCompetencyConditionStatic("platform", "pf", Competency["Platform"])
        tlCondition = chp.makeCompetencyConditionStatic("tool", "tl", Competency["Tool"])
        fwCondition = chp.makeCompetencyConditionStatic("framework", "fw", Competency["Framework"])

        levelCondition = f"where toUpper(c.level) = \"{level.upper()}\""

        # Tìm tất cả khoá học có liên quan tới kỹ năng
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
        
        # Tính toán số kỹ năng mà người dùng có mà match với yêu cầu
        courseList[["MatchedCol", "MatchedSkill"]] = courseList.apply(lambda x: chp.getMatchedSkill(Competency, x), axis=1, result_type="expand")

        sortCourse = courseList.sort_values(by=['MatchedCol','MatchedSkill' ,'Enroll', 'Rate'], ascending=[False, False,False, False]).reset_index().head(10).drop("index", axis=1)

        courseListUnique = sortCourse["ID"].unique().tolist()
        # Tìm tất cả những kỹ năng mà những khoá học đó giảng dạy

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

    ## Ưu tiên những khoá học mà có kỹ năng người dùng đã có
    ## ưu tiên những khoá học có dạy kỹ năng cấp độ cao cho người dùng 
    ## khoá học cần phải liên quan đến nghề nghiệp
    ## Nếu người dùng chưa có skill -> làm all

    # top đại diện cho số lượng lộ trình gợi ý

    # cấu trúc gợi ý
    '''
    - CareerName:
        - Required 1: loại yêu cầu

            - Course Path 1:
                - CoursePath: Course1 -> end
                - CoursePathLength
            - Course Path 2:
                - ...
        - Required 2: loại yêu cầu

            - Course Path 1:
                - CoursePath: Course1 -> end
                - CoursePathLength
            - Course Path 2:
                - ...


    '''

    def generateRecommandCoursePath(self, skillToLearn, top=3):

        skill = skillToLearn.head(top)
        # skill to learn thường là top 5 bộ kỹ năng yêu cầu
        recommandCourse = []

        # ứng với mỗi bộ kỹ năng được yêu cầu, tìm lộ trình học tương ứng
        for index, row in skill.iterrows():
            recommand = {}
            recommand["Require"] = row
            recommand["CoursePath"] = []
            recommand["CoursePathInfor"] = []

            # tạo lộ trình học rỗng
            for i in range(top):
                recommand["CoursePath"].append([])
                recommand["CoursePathInfor"].append({"TotalDuration": 0, "TotalPrice": 0, "TotalLength": 0})
            
            # Tư vấn các khoá học lớn hơn cấp độ kỹ năng hiện tại
            level = hp.getUpperLevel(row["Level"])

            # Gợi ý lộ trình học theo thứ tự của level -> basic -> advanced
            # Ứng với mỗi yêu cầu thì sẽ tạo top (mặc định là 4) lộ trình học tương ứng

            while (level != "OK"):
                rowData = self.findCourseByCompetency(row, level)
                rowSize = len(rowData)

                for i in range(top):
                    recommand["CoursePath"][i].append(rowData.iloc[i%rowSize])
                    rowVal = rowData.iloc[i%rowSize]
                    hp.printEntity(type(rowVal), "Row Value Type", "Course.py")
                    recommand["CoursePathInfor"][i]["TotalDuration"] += rowVal["Duration"]
                    recommand["CoursePathInfor"][i]["TotalPrice"] += rowVal["Price"]
                    recommand["CoursePathInfor"][i]["TotalLength"] += 1


                level = hp.getUpperLevel(level)
            
            
            
            recommandCourse.append(recommand)

        # -> 5 yêu cầu * 4 lộ trình học = 20 lộ trình học
            

        return recommandCourse

