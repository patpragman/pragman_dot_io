# get a metar from the national weather service
# we'll use this to display a status board
# Pat Pragman
# Ciego Services
# January 31, 2018
# this script was guided by some of the of the code in
# get_report.py from the Python-Metar module, I wrote a more helpful module
# for the web app that displays the metar data

from urllib.request import urlopen


def get_metar(station):
    base_url = "http://tgftp.nws.noaa.gov/data/observations/metar/stations"
    # the NWS stores their metars in the following format:
    # http://tgftp.nws.noaa.gov/data/observations/metar/stations/<station>.TXT

    if isinstance(station, str):
        # if it's a string, then we'll try to work with it
        # and ideally return a tuple of the following form:
        #  (BOOL, STRING) where the bool gives the status of the request
        # and the string contains the text of a report
        # if it's not a string, return a tuple
        try:
            # If the input is a string, we need to try to open the URL with the
            # title of the station, then parse it as a METAR
            target_url = f"{base_url}/{station}.TXT"
            url_hypertext = urlopen(target_url)  # try to open the URL
            return_string = ''  # this is what I will return from the URL I have opened

            # iterate through the lines in url_hypertext and look for metars
            for line in url_hypertext:
                if not isinstance(line, str):
                    # convert from Bytes to str
                    line = line.decode()

                if line.startswith(station):
                    # check if the station is the first thing on the line
                    # if it is, strip it and return it as a bool
                    return_string = line.strip()
                    return (True, return_string)

            if not return_string:
                return (False, f'No data returned from the NWS for {station}')

        except Exception as err:
            print(err)
            return (False, f'{station} {err}')

    else:
        return (False, "Unable to parse non-string imputs")
