import requests
import csv

def get_metars():
    #first, we're going to get all the data in the state for current metars
    #this gives us the most
    metar_source_url = "https://aviationweather.gov/adds/dataserver_current/current/metars.cache.csv"
    csv_metars = requests.get(metar_source_url)


    if csv_metars.status_code == 200:
        #if you get a 200 response
        #then parse the data into a dictionary

        data = csv_metars.content.decode()

        cr = csv.reader(data.splitlines(), delimiter=',')
        list_data = list(cr)


        #now let's clean this data up so we can use it
        metars = {}

        metars['Errors'] = list_data.pop(0)
        metars['Warnings'] = list_data.pop(0)
        metars['Response_Time'] = list_data.pop(0)
        metars['Data_Type'] = list_data.pop(0)
        metars['Results_Count'] = list_data.pop(0)
        metars['Headers'] = list_data.pop(0)

        #now we need to clean up the headers a bit.  There are duplicate headers here, and we don't want that
        metars['Headers'][24] = metars['Headers'][24] + "_" + str(2)
        metars['Headers'][25] = metars['Headers'][25] + "_" + str(2)
        metars['Headers'][26] = metars['Headers'][26] + "_" + str(3)
        metars['Headers'][27] = metars['Headers'][27] + "_" + str(3)
        metars['Headers'][28] = metars['Headers'][28] + "_" + str(4)
        metars['Headers'][29] = metars['Headers'][29] + "_" + str(4)


        for entry in list_data:
            #iterate through the data, apply a metar
            #to every 4-letter ICAO code

            metars[entry[1]] = {}

            #there are duplicate
            i = 0
            for header in metars['Headers']:
                if header in metars[entry[1]]:
                    pass
                else:
                    metars[entry[1]][header] = entry[i]

                i += 1


        return metars

def get_tafs():
    #first, we're going to get all the data in the state for current metars
    #this gives us the most
    metar_source_url = "https://aviationweather.gov/adds/dataserver_current/current/tafs.cache.csv"
    csv_metars = requests.get(metar_source_url)


    if csv_metars.status_code == 200:
        #if you get a 200 response
        #then parse the data into a dictionary

        data = csv_metars.content.decode('utf-8')

        cr = csv.reader(data.splitlines(), delimiter=',')
        list_data = list(cr)


        #now let's clean this data up so we can use it
        metars = {}

        metars['Errors'] = list_data.pop(0)
        metars['Warnings'] = list_data.pop(0)
        metars['Response_Time'] = list_data.pop(0)
        metars['Data_Type'] = list_data.pop(0)
        metars['Results_Count'] = list_data.pop(0)
        metars['Headers'] = list_data.pop(0)

        #now we need to clean up the headers a bit.  There are duplicate headers here, and we don't want that
        metars['Headers'][24] = metars['Headers'][24] + "_" + str(2)
        metars['Headers'][25] = metars['Headers'][25] + "_" + str(2)
        metars['Headers'][26] = metars['Headers'][26] + "_" + str(3)
        metars['Headers'][27] = metars['Headers'][27] + "_" + str(3)
        metars['Headers'][28] = metars['Headers'][28] + "_" + str(4)
        metars['Headers'][29] = metars['Headers'][29] + "_" + str(4)


        for entry in list_data:
            #iterate through the data, apply a metar
            #to every 4-letter ICAO code

            metars[entry[1]] = {}

            #there are duplicate
            i = 0
            for header in metars['Headers']:
                if header in metars[entry[1]]:
                    pass
                else:
                    metars[entry[1]][header] = entry[i]

                i += 1


        return metars
