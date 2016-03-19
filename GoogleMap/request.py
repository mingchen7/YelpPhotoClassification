import json
import time
import urllib
import urllib2
import pymongo
import csv

class GooglePlaces:
    MAPS_KEY = 'AIzaSyD5PRJPguFUMtpE-Z_ABzfY5nS5JvfSCrM'
    BASE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    
    def run(self, radius, types):                                    
        curPage = 1
        numPages = 3
        count = 1
        firstline = True

        with open('Dataset_Business_Phoenix.csv', 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if firstline: 
                    firstline = False
                    continue                
                business_id = row[15]
                longitude = float(row[69])
                latitude = float(row[66])

                results = []
                curPage = 1
                for place_type in types:
                    # initial query url                    
                    url = self.BASE_URL + '?' + urllib.urlencode({
                                                         'location': "%s,%s" % (latitude, longitude),
                                                         'radius': radius,
                                                         'key': self.MAPS_KEY,
                                                         'type': place_type,
                                                         })
                    
                    while curPage <= numPages:        
                        response = self.Request(url)                        
                        results.extend(response['results'])                                                
                        print "Row: %s, place: %s, page: %s, # of places found: %d" % (count, place_type, curPage, len(results)) 
                        if response.has_key('next_page_token'):
                            time.sleep(5)
                            # updating url with next_page_token
                            url = self.BASE_URL + '?' + urllib.urlencode({        
                                                         'pagetoken': response['next_page_token'],
                                                         'key': self.MAPS_KEY,                                                     
                                                         })                                                    
                            curPage = curPage + 1
                        else:
                            break
                    
                    # insert into MongoDB                                    
                
                count = count + 1
                if(count >= 10):
                    break
                
    # single request
    def Request(self, url):
        current_delay = 0.1
        max_delay = 3600

        while True:
            try:
                # Get the API response.
                response = str(urllib2.urlopen(url).read())                
            except IOError:
                pass  # Fall through the to the retry loop.
            else:
                # If we didn't get an IOError then parse the result.
                response = json.loads(response.replace('\\n', ''))
                if response['status'] == 'OK':
                    return response
                elif response['status'] != 'UNKNOWN_ERROR':
                    # Many API errors cannot be fixed by a retry, e.g. INVALID_REQUEST or
                    # ZERO_RESULTS. There is no point retrying these requests.
                    raise Exception(response['error_message'])

            if current_delay > max_delay:
                raise Exception('Too many retry attempts.')
            print 'Waiting', current_delay, 'seconds before retrying.'
            time.sleep(current_delay)
            current_delay *= 2  # Increase the delay each time we retry.
        
            
    def parseJson(self, content):
        print json.dumps([s for s in content['results']], indent=2)
        

if __name__ == "__main__":
    # types = ('bakery','bar','book_store','bus_station','cafe','gas_station','grocery_or_supermarket','gym','library', \
    #      'movie_theater','lodging','night_club','park','parking','restaurant','school','store','subway_station','university') 
    types = ["restaurant"]
    GooglePlaces().run(500, types)


        
        
            
    
    