import sys
# sys.path.append("..Helper.Helper")
# sys.path.append("..Model.Course")

from Helper.Helper import Helper as hp
from Model.Course import Course
from Model.Job import Job
from Controller.CompetencyController import CompetencyController as cc


class SearchController():

    def makeCourseFilterCondition(self, level, price, duration):
        condition = " where "

        if (level == "None"):
            levelCondition = ""
        else:
            condition += f" toUpper(c.level) = \"{level.upper()}\" and "

        if price == "Free":
            condition += f"c.price = 0"
        else:
            condition += f"c.price != 0"
        
        condition += f" and c.duration < {int(duration) + 1}"


        return condition
    
    def compactList(self, list, size=7):
        list = list[:size]
        return list
    
    def list2string(self, listz):

        if len(listz) < 1: return "-"
        
        if type(listz) == list:
            listz = [str(item) for item in listz]
            s = ",".join(listz)
            return s
        return listz

    def findCourse(self, Competencies, level=None, price=None, duration=None):

        filterCondition = None
        if level is not None:
            filterCondition = self.makeCourseFilterCondition(level, price, duration)
        
        courseModel = Course()
        data = courseModel.findCourseByCompetencyController(Competencies, filterCondition)
        data["Knowledge"] = data["Knowledge"].apply(lambda x: self.compactList(x))

        for col in hp.COMPETENCIES_LIST:
            data[col] = data[col].apply(lambda x: self.list2string(x))
        return data
    
    def findJob(self,Competencies):
        
        job = Job()
        data = job.findJob(Competencies)
        data["Knowledge"] = data["Knowledge"].apply(lambda x: self.compactList(x))

        return data
    
    
    

    def filterCourseData(self, data, level, price, duration):

        if level != "None":
            data = data[(data["Level"] == level.upper())]

        if duration != "unLimit":
            data = data[(data["Duration"] < int(duration))]

        if price == "Free":
            data = data[(data["Price"] == 0)]
        elif price == "Fee":
            data = data[(data["Price"] != 0)]
        
        return data
    
    def filterJobData(self, data, frequency, sortBy):

        data = data[(data["Frequency"] > int(frequency))]

        data = data.sort_values(sortBy, ascending= False) #ascending
        
        return data






    
        