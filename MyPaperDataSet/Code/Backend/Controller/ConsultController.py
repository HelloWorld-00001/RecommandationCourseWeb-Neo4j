from Helper.Helper import Helper as hp
from Model.Course import Course
from Model.Job import Job
from Model.User import User
from Controller.CompetencyController import CompetencyController as cc

class ConsultController():



    def eliminateKnownCompetencies(self, userSkill, jobSkill):
        # Flatten the list of lists in userSkill["Knowledge"] to make comparison easier
        
        deleteCol = ["Knowledge", "Platform"]

        for col in deleteCol:
            jobSkill[col] = jobSkill[col].apply(lambda x: hp.removeFromList(hp, x,  userSkill[col].tolist()))
        
        for col in ["ProgrammingLanguage", "Framework"]:
            jobSkill[col + "Level"] = jobSkill[col].apply(lambda x: hp.getLevel(hp, x,  userSkill[col]))

        jobSkill["Tool"] = jobSkill["Tool"].apply(lambda x: x if x not in userSkill["Tool"].tolist() else None)
        return jobSkill
    

    def consultCareerByJob(self, username, jobName, top=5):
        user = User(username)
        job = Job()
        course = Course()

        userSkill = user.getSkill()

        # need to change userSkill to competency 
        jobSkill = job.findJobCompetency(jobName, top)

        needSkill = self.eliminateKnownCompetencies(userSkill, jobSkill).head(top).reset_index().drop("index", axis=1)

        recommandCourse = course.printCoursePath(needSkill)
        return recommandCourse
    

    def consultCareerByJobCompe(self, competency, jobName, top=5):
        job = Job()
        course = Course()

        jobSkill = job.findJobCompetency(jobName, top)

        needSkill = self.eliminateKnownCompetencies(competency, jobSkill).head(top).reset_index().drop("index", axis=1)

        recommandCourse = course.printCoursePath(recommandCourse)

    

