import json
import requests

class geocoder:


    def __init__(self): 
        self.url_search1 = "https://nominatim.openstreetmap.org/search/?city={city}&format=json"
        self.url_search2 = "https://nominatim.openstreetmap.org/search/?city={city}&countrycodes={countrycode}&format=json"
        self.RESULT_LIST=[]
        self.place_types=["city","village","town","hamlet","isolated_dwelling","borough","suburb","quarter","neighbourhood"]

    
    def getQueryResults(self,*args):#city[0]  countrycode[1]
        if len(args)==2:
            self.url_search = self.url_search2.replace("{city}", str(args[0])).replace("{countrycode}", str(args[1]))
        elif len(args)==1:
            self.url_search = self.url_search1.replace("{city}", str(args[0]))
        else:
            return -3
        #print("URL: "+self.url_search)

        try:
            r = requests.get(self.url_search)

            if r.status_code == 200:
                res = r.text
                J = json.loads(res)

                for row in J:   
                    #print("     TYPE="+row["type"]+":"+row["display_name"])
                    if(row["type"] in self.place_types):
                        self.RESULT_LIST.append(row)

                return len( self.RESULT_LIST )
            else:
                return -1
        except:
            print("Unknown error...")
            return -2


    def listResults(self):
        num=1
        for row in self.RESULT_LIST:
            print("  "+str(num)+". "+row["display_name"])
            num=num+1


    def getCoordindates(self,choice):
        try:
            lon = self.RESULT_LIST[choice]["lon"]
            lat = self.RESULT_LIST[choice]["lat"]
            coordinates = {'lat':lat,'lon':lon}
            return coordinates
        except:
            return False







