import urllib2
from csv import reader
import datetime

def downloadData(url):
    response = urllib2.urlopen(url)
    fh = open("assignment2.csv", "w")
    fh.write(response.read())
    fh.close()
    return "assignment2.csv"


def processData(data):
    with open(data, 'r') as read_obj:
        csv_reader = reader(read_obj)
        rowNumber = 1
        people = {}

        for row in csv_reader:
            rowNumber += 1
            birthday = extractDate(row, rowNumber)
            if birthday != -1:
                people[row[0]] = (row[1], birthday)

    return people


def extractDate(row, rowNumber):
    date = row[2]

    fileName = "errors.log"

    count = 0

    for i in range(len(date)):

        if date[i] == "/":

            count += 1

            if count > 2:
                break

    # counting the forward slashes

    if count != 2:
        loggerError(row, fileName, rowNumber)

        return -1

    # checking the number of digits and slashes as a whole

    if len(date) != 10:
        loggerError(row, fileName, rowNumber)

        return -1

    date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')

    return date_time_obj.date()


def loggerError(row, fileName, rowNumber):
    # “Error processing line #<linenum> for ID #<id>”

    loggerFile = open(fileName, 'a')

    loggerFile.write("Error processing line #" + rowNumber + "for #" + row[0] + "\n")

    loggerFile.close()


def displayPerson(id, db):
    if db[id] == None:
        print("No user found with that id")
    else:
        print("Person #" + id + " is " + db[id][0] + " with a birthday of " + db[id][1])


url = input("Please enter the url of the specified source: ")

if len(url) == 0:

    print("Please run the application again and type the url")

else:

    csvData = downloadData(url)

    personData = processData()

    person_id = int(input("Please insert the ID here: "))

    while person_id > 0:
        displayPerson(person_id, personData)
        person_id = int(input("Please isnert the ID here: "))