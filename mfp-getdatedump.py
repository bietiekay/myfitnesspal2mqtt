import myfitnesspal
import sys, getopt
import json
from dateutil import parser
from datetime import datetime,date,time,timedelta

#enddate = date.today()
day = timedelta(days=1)
#startdate = enddate - day
#enddate = startdate
def main(argv):
    try:
      opts, args = getopt.getopt(argv,"h:s:e:u:p:",["sdate=","startdate=","user=","password="])
    except getopt.GetoptError:
      print 'mfp-getdatedump.py -s <startdate> -e <enddate> -u <username> -p <password>'
      sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'mfp-getdatedump.py -s <startdate> -e <enddate> -u <username> -p <password>'
            sys.exit()
        elif opt in ("-s", "--sdate"):
            startdate = parser.parse(arg).date()
        elif opt in ("-e", "--edate"):
            enddate = parser.parse(arg).date()
        elif opt in ("-u", "--user"):
            user = arg
        elif opt in ("-p", "--password"):
            password = arg

#    print("User: "+user)
#    print("PW:   "+password)
#    print("Start: "+startdate.strftime('%Y-%m-%d'))
#    print("End:   "+enddate.strftime('%Y-%m-%d'))

    #sys.stdout.write('connecting...')
    client = myfitnesspal.Client(user,password)
    #sys.stdout.write('connected')

    #sys.stdout.write('Weight...')
    mfpweight = client.get_measurements("Weight",startdate)
    #sys.stdout.write('Body Fat...')
    mfpbodyfat = client.get_measurements("Body Fat %",startdate)

    #sys.stdout.write('{')
    while startdate <= enddate:
        sys.stdout.write('{')
        mfpexercise = client.get_exercise(startdate.year, startdate.month, startdate.day)
        mfpday = client.get_date(startdate.year,startdate.month,startdate.day)
    # ----------- Output as JSON to STDOUT
    #    sys.stdout.write('{ \"'+startdate.strftime('%Y-%m-%d')+'\": {')
        #if allprevious:
        #    sys.stdout.write(',')
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
        mprevious = False;
        for meal in mfpday.meals:
            if bool(meal.entries):
                if mprevious:
                    sys.stdout.write(',')
                sys.stdout.write('{') # opening meal
                sys.stdout.write('\"name\": \"'+meal.name.title().encode('utf-8').replace('\"',"").replace('\"',"")+'\",')
                previous = False;
                for entry in meal.entries:
                    if previous:
                        sys.stdout.write(',')
                    sys.stdout.write('\"'+entry.name.encode('utf-8').replace('\"',"").replace('\"',"")+'\": '+str(entry.nutrition_information).replace('\'','\"'))
                    previous = True;
                mprevious = True;
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
        #sys.stdout.write('}') # closing day
        print("}")
        #allprevious = True;
        #input("Press Enter to continue...")
        startdate = startdate + day
    #sys.stdout.write('}') # closing document
    sys.stdout.flush()
    #print("")
    #    print("}\n")
    #startdate = startdate + day



if __name__ == "__main__":
   main(sys.argv[1:])
