

'''
//
//                       _oo0oo_
//                      o8888888o
//                      88" . "88
//                      (| -_- |)
//                      0\  =  /0
//                    ___/`---'\___
//                  .' \\|     |// '.
//                 / \\|||  :  |||// \
//                / _||||| -:- |||||- \
//               |   | \\\  -  /// |   |
//               | \_|  ''\---/''  |_/ |
//               \  .-\__  '-'  ___/-. /
//             ___'. .'  /--.--\  `. .'___
//          ."" '<  `.___\_<|>_/___.' >' "".
//         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
//         \  \ `_.   \_ __\ /__ _/   .-` /  /
//     =====`-.____`.___ \_____/___.-`___.-'=====
//                       `=---='
//
//
//     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//               佛祖保佑         永无BUG
//          Đức phật phù hộ  Code không bị lỗi
'''
'''
cd Courses/DataGen/MyPaperDataSet/Code/Backend/

conda activate spark2
'''

from flask import Flask, render_template, request, redirect, jsonify
import os
import pandas as pd
from Controller.SearchController import SearchController as scl
from Helper.Helper import Helper as hp
from Controller.CompetencyController import CompetencyController as ccl
# Assuming your Flask app is located at the root of "Backend" directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FE_PATH = os.path.join(os.path.dirname(BASE_DIR), 'Frontend')

app = Flask(__name__, template_folder="../Frontend", static_folder="../Frontend")


@app.route('/')
def index():
    return render_template( 'index.html')


##----------------------------------------------------------------
# >>> Error handling
##----------------------------------------------------------------

@app.errorhandler(404)
def handle_404_error(error):

    app.logger.error('404 error: %s', error)  # Log the error
    return render_template("error.html", error_code=404, error_message="Resource not found"), 404

@app.errorhandler(ValueError)
def handle_value_error(error):

    app.logger.error('ValueError: %s', error)  # Log the error
    return render_template("error.html", error_code=500, error_message=str(error)), 500

@app.errorhandler(Exception)
def handle_exception(error):
    # Log the error here if you want
    app.logger.exception('Unhandled Exception: %s', error)
    return render_template("error.html", error_code=500, error_message="An unexpected error occurred"), 500

@app.errorhandler(400)
def handle_404_error(error):

    app.logger.error('404 error: %s', error)  # Log the error
    return render_template("error.html", error_code=400, error_message="Bad Request"), 400
##----------------------------------------------------------------
# >>> Search Course Area
##----------------------------------------------------------------

# delcare local variable
courseData = pd.DataFrame()
jobData = pd.DataFrame()
Competency = {}

sc = scl()

@app.route('/search')
def navigate():
    return render_template( 'searchPage.html')


# take input from user to query
@app.route('/searchData', methods=['POST'])
def getForm():

    pl = request.form['inputProgrammingLanguage']
    fw = request.form['inputFramework']
    kl = request.form['inputKnowledge']
    pf = request.form['inputPlatform']
    tl = request.form['inputTool']

    comptencies = ccl(pl, fw, kl, pf, tl)
    global Competency
    Competency = comptencies

    typeButton = request.form['option']
    entity = "Course"
    data = pd.DataFrame()
    if (typeButton == "findJob"):
        data = sc.findJob(comptencies)
        global jobData
        jobData = data
        entity = "Job"
    else:
        data = sc.findCourse(comptencies)
        global courseData 
        courseData = data
    
    # Redirect or respond after processing the data
    return searchResult(data.head(10), entity)
   #redirect("/search")

@app.route('/searchResult')
def searchResult(tableData=pd.DataFrame(), entity="Course"):
    return render_template( 'searchResult.html', tableData = tableData, entity = entity)


@app.route('/filterSearch', methods=['POST'])
def filterSearch():

    global jobData
    global courseData 


    typeFilter = request.form['option']
    if typeFilter != "":
        data = pd.DataFrame()
        global Competency
        if typeFilter == "Job":
            data = sc.findJob(Competency)
            jobData = data
        else:
            data = sc.findCourse(Competency)
            courseData = data
        return searchResult(data.head(10), typeFilter)



    tableData = pd.DataFrame()
    level = request.form.get('levelDropdown')
    if level is None:
        frequency = request.form.get('frequencyDropdown')
        sortBy = request.form.get('sortByDropdown')
        tableData = sc.filterJobData(jobData, frequency, sortBy)
    
    else:
        level = request.form.get('levelDropdown')
        price = request.form.get('priceDropdown')
        duration = request.form.get('durationDropdown')
        tableData = sc.filterCourseData(courseData, level, price, duration)

    

    response = {
        'data': tableData.to_dict(orient='records'),  # Data in records format
        'column': tableData.columns.tolist()  # List of column names
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(port=8000, debug=True)

