import myfitnesspal, sys, json
from datetime import datetime,date,time,timedelta
client = myfitnesspal.Client('$username','$password')

enddate = date.today()
day = timedelta(days=1)
startdate = enddate - day
enddate = startdate

# Bodyfat and Weight...
mfpweight = client.get_measurements("Weight",startdate)
mfpbodyfat = client.get_measurements("Body Fat %",startdate)

allprevious = False
sys.stdout.write('{')
while startdate <= enddate:
    mfpday = client.get_date(startdate.year,startdate.month,startdate.day)
    mfpexercise = mfpday.exercises
    
# ----------- Output as JSON to STDOUT
#    sys.stdout.write('{ \"'+startdate.strftime('%Y-%m-%d')+'\": {')
    if allprevious:
        sys.stdout.write(',')
    sys.stdout.write('\"'+startdate.strftime('%Y-%m-%d')+'\" : {') # opening day
    sys.stdout.write('\"complete\": \"'+str(mfpday.complete).replace('\'','\"')+'\",')
    sys.stdout.write('\"totals\": '+str(mfpday.totals).replace('\'','\"')+',')
    sys.stdout.write('\"measurements\": {') # opening measurements
    #sys.stdout.write('\"')
    if bool(mfpweight.get(startdate)):
        sys.stdout.write('\"weight\": \"'+str(mfpweight[startdate])+'\"')
        if bool(mfpbodyfat.get(startdate)):
            sys.stdout.write(',')
    if bool(mfpbodyfat.get(startdate)):
        sys.stdout.write('\"bodyfat\": \"'+str(mfpbodyfat[startdate])+'\"')
    sys.stdout.write('},') # closing measurements
    sys.stdout.write('\"notes\": \"'+mfpday.notes.encode('utf-8').replace('\"',"").replace('\"',"")+'\",')
    sys.stdout.write('\"meals\": [') # opening meals
    mprevious = False
    for meal in mfpday.meals:
        if bool(meal.entries):
            if mprevious:
                sys.stdout.write(',')
            sys.stdout.write('{') # opening meal
            sys.stdout.write('\"name\": \"'+meal.name.title().encode('utf-8').replace('\"',"").replace('\"',"")+'\",')
            previous = False
            for entry in meal.entries:
                if previous:
                    sys.stdout.write(',')
                sys.stdout.write('\"'+entry.name.encode('utf-8').replace('\"',"").replace('\"',"")+'\": '+str(entry.nutrition_information).replace('\'','\"'))
                previous = True
            mprevious = True
            sys.stdout.write('}') # closing meal
    sys.stdout.write('],') # closing meals
    sys.stdout.write('\"goals\": '+str(mfpday.goals).replace('\'','\"'))
    sys.stdout.write(',') # closing goals
    sys.stdout.write('\"exercises\": [')
    exprevious = False
    for exercise in mfpexercise:
        if exprevious:
            sys.stdout.write(',')
        sys.stdout.write('{ \"type\": \"'+str(exercise.name)+'\", \"activities\": [')
        exactivity = False
        for activity in exercise.get_as_list():
            if exactivity:
                sys.stdout.write(',')
            sys.stdout.write('{ \"name\": \"'+str(activity['name'])+'\",')
            sys.stdout.write(str(activity['nutrition_information']).replace('nutrition_information','activities').replace('\'','\"').replace('{','').replace('}','').replace('None','0'))
            exactivity = True
            sys.stdout.write('}')
        sys.stdout.write(']}')
        exprevious = True
    sys.stdout.write(']}') # closing exercises
    allprevious = True
    #input("Press Enter to continue...")
    startdate = startdate + day
#sys.stdout.write('}') # closing document
sys.stdout.flush()
print(" }")
