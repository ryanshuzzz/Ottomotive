import tornado.ioloop
import tornado.web
import smartcar
import webbrowser

client_id = '60efb543-adc8-4481-b316-9866110de2b3'
client_secret = '6de37c8e-9edc-4155-b345-7d2c92d91303'
redirect_uri = 'http://localhost:5000/callback'

client = smartcar.AuthClient(client_id, client_secret, redirect_uri, test_mode = True)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        auth_url = client.get_auth_url(force=True)
        webbrowser.open(auth_url)

class CallbackHandler(tornado.web.RequestHandler):
    def get(self):
        actual_code = self.get_argument('code') #get code
        codeStr = str(actual_code)
        global access							#change from global in future
        access = client.exchange_code(actual_code) #get access info
        access_token = access["access_token"]
        vehicle_ids_dict = smartcar.get_vehicle_ids(access_token)
        print(access)
        vehicles_in_list = vehicle_ids_dict['vehicles']

        vehicle_dic = get_cars(vehicles_in_list, access_token)
        self.render('html/index.html', title = "callback", code=codeStr)

class AboutHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('html/about.html')

class RegisterHandler(tornado.web.RequestHandler):	#when *press register* -> pass info into "create_user"
	def get(self):
		self.render('html/register.html')

class ContactHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('html/contact.html')

class LoginHandler(tornado.web.RequestHandler):
	def post(self):
		self.render('html/loggedin.html')

def make_app():
	return tornado.web.Application([
		(r"/static/(.*)", tornado.web.StaticFileHandler,{'path': 'html/static/'}),
		(r"/", MainHandler),
		(r"/callback", CallbackHandler),
		(r"/about", AboutHandler),
		(r"/register", RegisterHandler),
		(r"/contact", ContactHandler),
		(r"/loggedin", LoginHandler),
		])

'''Begin functions for output'''
def get_cars(vehicles_in_list, access_token):
    vehicle_dic = {}
    for vehicle in range(len(vehicles_in_list)):
      vehicle_dic.update({"Vehicle" + str(vehicle + 1): vehicles_in_list[vehicle]})

    vehicle_lst2 = []
    for car in vehicle_dic.keys():
        vehicle_lst2.append(smartcar.Vehicle(vehicle_dic[car], access_token))


# odometer_reading, vehicle_make, vehicle_model, vehicle_year, vehicle_latitude, vehicle_longitude, vehicle_datetime
    odometer_reading = []
    '''Give all of the odometer reading'''
    for odometer in range(len(vehicle_lst2)):
        odometer_reading.append((vehicle_lst2[odometer].odometer()['data']['distance']))

    vehicle_make = []
    '''Give all of the vehical's makes'''
    for car in range(len(vehicle_lst2)):
        vehicle_make.append(vehicle_lst2[car].info()['make'])

    vehicle_model = []
    '''Give all of the vehical's modles'''
    for car in range(len(vehicle_lst2)):
        vehicle_model.append(vehicle_lst2[car].info()['model'])

    vehicle_year = []
    '''Give all of the vehical's years'''
    for car in range(len(vehicle_lst2)):
        vehicle_year.append(vehicle_lst2[car].info()['year'])

    vehicle_latitude = []
    '''Give all of the vehical's latitudes'''
    for car in range(len(vehicle_lst2)):
        vehicle_latitude.append(vehicle_lst2[car].location()['data']['latitude'])

    vehicle_longitude = []
    '''Give all of the vehical's longitude'''
    for car in range(len(vehicle_lst2)):
        vehicle_longitude.append(vehicle_lst2[car].location()['data']['longitude'])

    vehicle_age = []
    '''this is irrelevant'''
    for car in range(len(vehicle_lst2)):  # <- gets the age of data of every car
        vehicle_age.append(vehicle_lst2[car].location()['age'])

    vehicle_datetime = []
    '''Give all of the vehical's ages in a list of 5 tiems
        Ex. vehicle_age[0][0] -> 1st car's year
        Ex. vehicle_age[0][1] -> 1st car's month
        Ex. vehicle_age[0][2] -> 1st car's day
        Ex. vehicle_age[1][0] -> 2nd car's year
        Ex. vehicle_age[2][0] -> 1st car's month
    '''

    for date in vehicle_age: # <- appending each cars entire age into a list

        '''dont worry about this'''
        tt = date.timetuple() # <- formating age to extract information
        print('year ->', tt[0])
        print('month ->', tt[1])
        print('day ->', tt[2])
        print('hour ->', tt[3])
        print('minute ->', tt[4])
        age_info = ''
        for day in range(len(tt[:5])):
            age_info += (str(tt[day])+ ' ')  # <- year
        vehicle_datetime.append(age_info)

    for date in range(len(vehicle_datetime)):
        '''this formats the age
        dnt worry about this'''
        vehicle_datetime[date] = vehicle_datetime[date].strip().split()


    print('vehicle_datetime ->', vehicle_datetime)
    print('vehicle_age ->', vehicle_age)
    print('vehicle_longitude ->', vehicle_longitude)
    print('vehicle_latitude ->', vehicle_latitude)
    print('vehicle_year ->', vehicle_year)
    print('vehicle_model ->', vehicle_model)
    print('vehicle_make ->', vehicle_make)
    print()
    print('vehicle_dic ->', vehicle_dic)
    print('vehicle_lst2 ->', vehicle_lst2)
    print('odometer_reading ->', odometer_reading)
    return vehicle_dic


'''main run '''
if __name__ == "__main__":
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
