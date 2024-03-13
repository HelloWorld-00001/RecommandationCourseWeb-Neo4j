from Model.BaseModel import BaseModel
from Helper.Helper import Helper as hp


class Job(BaseModel):

    def getAllRecruitment(self):
        query = "match(f: FactJobPosting)-[:Belong_to_career]->(c: Career) \
                return c.name as CareerName, sum(f.totalJobPost) as `Number of Job`"
        listOfRecruitment = self.queryToDataFrame(query)

        return listOfRecruitment

    def findJob(self, Competency):
        
        condition = Competency.makeCompetencyConditionAllSpecial()
        
        query = f''' match(f: FactJobPosting)-[:Belong_to_career]->(c: Career)
                match(f)-[:Required_programmingLanguage]->(pl : ProgrammingLanguage) {condition["ProgrammingLanguage"]}
                optional match(f)-[:Required_knowledge]->(kl: Knowledge) {condition["Knowledge"]}
                optional match(f)-[:Required_tool]->(tl: Tool)<-[:Use_tool]-(pl) {condition["Tool"]}
                optional match(f)-[:Required_framework]->(fw: Framework)<-[:Have_framework]-(pl) {condition["Framework"]}
                optional match(f)-[:Required_platform]->(pf: Platform)-[Deploy_on_framework]->(fw) {condition["Platform"]}

                return c.name as CareerName,
                    pl.programmingLanguage as ProgrammingLanguage,
                    collect(distinct kl.knowledge) as Knowledge,  fw.framework as Framework, tl.tool as Tool, 
                    collect(distinct pf.platform) as Platform,
                    sum(f.totalJobPost) as `Number of Job` 
                '''
        
        careerInfor = self.getAllRecruitment()

        data = self.queryToDataFrame(query)

        data = data.merge(careerInfor, on="CareerName", how="inner")
        data["Frequency"] = round((data['Number of Job_x']/ data['Number of Job_y'])*100, 2)
        data = hp.emptyProcess(data, hp.COMPETENCIES_LIST)
        data["MatchedColumn"] = 5 - data.isnull().sum(axis=1)

        dataSort = data.sort_values(["Frequency", "MatchedColumn"], ascending=[False, False])
        dataSort = dataSort.rename(columns={"Number of Job_x": "Total job by skill", "Number of Job_y": "Total job by career"})



        dataSort = dataSort.fillna("-")
        return  dataSort.reset_index().drop(["index"], axis=1)
    
    def findJobByCompetency(self, Competency=None, careerName = ""):


        if Competency is None: return self.findJobByName(careerName)

        condition = Competency.makeCompetencyConditionAllSpecial()

        careerCondition = ""
        if careerName != "":
            careerCondition =  f"where c.name = \"{careerName}\""

        query = f''' match(f: FactJobPosting)-[:Belong_to_career]->(c: Career) {careerCondition}
                match(f)-[:Required_programmingLanguage]->(pl : ProgrammingLanguage) {condition["ProgrammingLanguage"]}
                optional match(f)-[:Required_knowledge]->(kl: Knowledge) {condition["Knowledge"]}
                optional match(f)-[:Required_tool]->(tl: Tool)<-[:Use_tool]-(pl) {condition["Tool"]}
                optional match(f)-[:Required_framework]->(fw: Framework)<-[:Have_framework]-(pl) {condition["Framework"]}
                optional match(f)-[:Required_platform]->(pf: Platform)-[Deploy_on_framework]->(fw) {condition["Platform"]}

                return c.name as CareerName,
                    pl.programmingLanguage as ProgrammingLanguage,
                    collect(distinct kl.knowledge) as Knowledge,  fw.framework as Framework, collect(distinct tl.tool) as Tool, 
                    collect(distinct pf.platform) as Platform,
                    sum(f.totalJobPost) as `Number of Job`
                '''
        
        data = self.queryToDataFrame(query)
        return data

    def findJobByName(self, careerCondition=""):

        if careerCondition != "":
            careerCondition =  f"where c.name = \"{careerCondition}\""

        query = f''' match(f: FactJobPosting)-[:Belong_to_career]->(c: Career) {careerCondition}
            match(f)-[:Required_programmingLanguage]->(pl : ProgrammingLanguage) 
            optional match(f)-[:Required_knowledge]->(kl: Knowledge)<-[:Relate_to_knowledge]-(pl)
            optional match(f)-[:Required_framework]->(fw: Framework)<-[:Have_framework]-(pl)
            optional match(f)-[:Required_platform]->(pf: Platform) <-[:Deploy_to_platform]-(pl)
            optional match(f)-[:Required_tool]->(tl: Tool)<-[:Use_tool]-(pl)
            return c.name as CareerName,
                pl.programmingLanguage as ProgrammingLanguage,
                collect(distinct kl.knowledge) as Knowledge, fw.framework as Framework, tl.tool as Tool, 
                collect(distinct pf.platform) as Platform,
                sum(f.totalJobPost) as `Number of Job`  order by `Number of Job` desc
            '''
        
        data = self.queryToDataFrame(query)
        return data
    
    def jobConsulting(self, userSkill=None, careerName = ""):
        data = self.findJobByCompetency(userSkill, careerName)
        for career in data['CareerName'].unique():
            queC = f"match(f:FactJobPosting)-[:Belong_to_career]->(c:Career) where c.name = \"{career}\"  return  sum(f.totalJobPost) as numJob"
            totalJob = self.queryToDataFrame(queC)
            totalJobCount = totalJob['numJob'][0]
            data.loc[data['CareerName'] == career, 'Job Count'] = totalJobCount
            data['Frequency'] = round(data['Number of Job']/data['Job Count'] * 100, 2)
        
        data["Matched"] = data.apply(hp.getMatchedCompeLen, axis=1)
        hp.emptyProcess(data, hp.COMPETENCIES_LIST)
        data = data.sort_values(by=['Matched', 'Frequency'], ascending=[ False, False]).reset_index()
        data = data.drop("index", axis=1)
        return data

    

    def findJobCompetency(self, jobName, top=10):
        jobDF = self.jobConsulting(None, jobName)
        jobCompe = jobDF.sort_values("Frequency", ascending=False)
        jobCompe["MatchedColumn"] = 5 - jobCompe.isnull().sum(axis=1)

        jobSkill = jobCompe.sort_values(["MatchedColumn", "Frequency"], ascending=[False, False])   
        return jobSkill.head(top)

    def formatJobSkill(jobCompetency):
        skill ={}
        for com in hp.COMPETENCIES_LIST:
            if (com == "ProgrammingLanguage" or com == "Framework"):
                skill[com] = jobCompetency[com].explode().unique()
            else:
                unique_values = set(val for sublist in jobCompetency[com] for val in sublist)
                # If you need the result as a list
                unique_values_list = list(unique_values)
                skill[com] = unique_values_list
            
        return skill
