from Model.BaseModel import BaseModel
from Helper.Helper import Helper as hp
from Model.Competency import Competency as cpt


class Job(BaseModel):

    def getAllRecruitment(self):
        query = "match(f: FactJobPosting)-[:Belong_to_career]->(c: Career) \
                return c.name as CareerName, sum(f.totalJobPost) as `Number of Job`"
        listOfRecruitment = self.queryToDataFrame(query)

        return listOfRecruitment

    def findJob(self, Competency):
        
        condition = Competency.makeCompetencyConditionAll()
        
        query = f''' match(f: FactJobPosting)-[:Belong_to_career]->(c: Career)
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
        
        careerInfor = self.getAllRecruitment()

        data = self.queryToDataFrame(query)

        data = data.merge(careerInfor, on="CareerName", how="inner")
        data["Frequency"] = round((data['Number of Job_x']/ data['Number of Job_y'])*100, 2)
        dataSort = data.sort_values("Frequency", ascending=False)
        dataSort = dataSort.rename(columns={"Number of Job_x": "Total job by skill", "Number of Job_y": "Total job by career"})
        dataSort = hp.emptyProcess(dataSort, hp.COMPETENCIES_LIST)
        dataSort = dataSort.fillna("-")
        return  dataSort.reset_index().drop(["index"], axis=1)
    

    def calcJobFrequency(self, userSkill):
        data = self.findJob(userSkill)
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
        return data.fillna("-")

