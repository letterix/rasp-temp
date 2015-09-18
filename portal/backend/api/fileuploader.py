#import json
#from builtins import print
#import requests
#from requests.api import request
#from common import *


#def get(serial_number):

    #data = {'serial_number' : serial_number}
    #url="http://localhost:1443/upload_log_file"
    #filename = "C:/projekt/esbe/portal/backend/"+ serial_number + ".log"
    #file = open(filename,'rb')
    #request = requests.post(url, data = data, files={'myFile': (filename, file)})
    #file.close()


    #if request:
     #   return OkResponse("Sucess")
    #else:
        #return ErrorResponse("Error")


