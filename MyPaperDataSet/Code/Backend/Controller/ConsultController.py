from Helper.Helper import Helper as hp
from Helper.CompetencyHelper import CompetencyHelper
from Model.Course import Course
from Model.Job import Job
from Model.User import User
from Controller.CompetencyController import CompetencyController as cc
from DTOS.CompetencyDtos import CompetencyDtos


class ConsultController():


    def eliminateKnownCompetencies(self, userSkill, jobSkill):
        # Flatten the list of lists in userSkill["Knowledge"] to make comparison easier
        if userSkill is None or len(userSkill) < 1: return jobSkill
        if jobSkill.empty: return jobSkill 
        deleteCol = ["Knowledge", "Platform", "Tool"]

        for col in deleteCol:
            jobSkill[col] = jobSkill[col].apply(lambda x: hp.removeFromList(hp, x,  userSkill[col].tolist()))
        
        for col in ["ProgrammingLanguage", "Framework"]:
            jobSkill[col + "Level"] = jobSkill[col].apply(lambda x: hp.getLevel(hp, x,  userSkill[col]))

        return jobSkill
    

    def orderSkill(sefl,  jobSkill, order = ["LevelNumber", "MatchedColumn", "Frequency"], orderAsc = [False, False, False], top=5):
        jobSkill[["Level", "LevelNumber"]] = jobSkill.apply(lambda x: hp.getLowerLevelOfPandasRow(x), axis=1, result_type="expand")
        skillToLearn = jobSkill.sort_values(order, ascending=orderAsc)
        skillToLearn = skillToLearn.drop(["LevelNumber", "ProgrammingLanguageLevel", "FrameworkLevel"], axis=1)
        return skillToLearn.head(top).reset_index().drop("index", axis=1)
    

    def consultCourseByJob(self,jobName, username=None, userSkill=None, top=4, mode="user"):

        if mode == "user":
            user = User(username)
            userSkill = user.getFullInfor()

        job = Job()
        course = Course()

        # need to change userSkill to competency 
        jobSkill = job.findJobCompetency(jobName, top, "course")
        jobRequired = job.getJobCompetencyRequired(jobName) # get all job requirements
        hp.printEntity(userSkill, "UserSkill", "ConsultController")
        hp.printEntity(jobRequired["CareerName"].to_string(index=False), "jobRequired", "ConsultController")


        needSkill = self.eliminateKnownCompetencies(userSkill, jobSkill).head(top).reset_index().drop("index", axis=1)
        skillRequired = self.orderSkill(needSkill)
    
        recommandCourse = course.generateRecommandCoursePath(skillRequired, 3)
        #self.printCoursePath(recommandCourse, top)

        return recommandCourse, jobRequired
    
    def printCoursePath(self, recommandCourse, top):
       
        for k in range(top):
            for coursePath in recommandCourse:
                print(coursePath["Require"]["CareerName"])
                print("\n--------------------------------")
                print("Require: ")
                print(coursePath["Require"])
                print("\n--------------- End Require -----------------")
                print(f"CoursePath: {k}")
                print("Course Path Length: ", len(coursePath["CoursePath"][k]))
                print("\n---- Start Course Path ----")

                for subCourse in coursePath["CoursePath"][k]:
                    print(subCourse["CourseName"] + "Level: " + subCourse["Level"])
                    print("-->")
            
                print("---- End Path ----\n")

                print("--------------------------------\n")


    def consultCareerByJobCompe(self, competency, jobName, top=5):
        job = Job()
        course = Course()

        jobSkill = job.findJobCompetency(jobName, top)

        needSkill = self.eliminateKnownCompetencies(competency, jobSkill).head(top).reset_index().drop("index", axis=1)

        recommandCourse = course.printCoursePath(recommandCourse)


    def jobConsulting(self,Competencies:CompetencyDtos):
        
        job = Job()
        comptency = Competencies.getCompetencyOriginal()

        # hp.printEntity(comptency, "Competency Input", "ConsultController")
        data = job.jobConsulting(comptency)

        return data
    
    def jobConsultingByUser(self, username):
        
        job = Job()
        user = User(username)

        userSkill = user.getUserDataString()

        competency = CompetencyDtos()
        competency.getCompetencyDtosFromUser(userSkill)
        compe = {"len": competency.getTotalLen(), "competency": CompetencyHelper.getCompetencyList()}

        return self.jobConsulting(competency), compe
    

    def getListOfCareer(self):
        job = Job()
        return job.getAllJobName()

    

