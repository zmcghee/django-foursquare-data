from djangofoursquare.utils import *
from djangofoursquare.views import *
import models as foursquare

def get_history(consumer, connection, access_token):
    return make_request(consumer, connection, access_token, 
            'http://api.foursquare.com/v1/history.json')

def store_foursquare_user(foursquare_user_data, access_token): 
	foursquare_user_id = foursquare_user_data['id']
	first_name = foursquare_user_data.get('firstname', '')
	last_name = foursquare_user_data.get('lastname', '')
	photo = foursquare_user_data.get('photo', '')
	gender = foursquare_user_data.get('gender', '')
	phone = foursquare_user_data.get('phone', '')
	email = foursquare_user_data.get('email', '')
	try:
		user = foursquare.User.objects.get(id=foursquare_user_id)
		user.delete()
		user = foursquare.User.objects.get(id=foursquare_user_id)
	except foursquare.User.DoesNotExist:
		user = foursquare.User(id=foursquare_user_id, firstname=first_name, lastname=last_name,
					photo=photo, gender=gender, email=email, phone=phone,
					access_token=access_token)
		user.save()
	return user

def save_history_to_database(users):
	for user in users:
		token = oauth.OAuthToken.from_string(user.access_token)
		json = get_history(get_consumer(), get_connection(), token)
		for checkin in json['checkins']:
			# Add primary category to database
			try:
				category = foursquare.Category.objects.get(id=checkin['venue']['primarycategory']['id'])
			except NameError:
				continue
			except:
				category = foursquare.Category(id=checkin['venue']['primarycategory']['id'])
			category.fullpathname = checkin['venue']['primarycategory']['fullpathname']
			category.nodename = checkin['venue']['primarycategory']['nodename']
			category.iconurl = checkin['venue']['primarycategory']['iconurl']
			category.save()
			# Add venue to database
			try:
				venue = foursquare.Venue.objects.get(id=checkin['venue']['id'])
			except foursquare.Venue.DoesNotExist:
				venue = foursquare.Venue(id=checkin['venue']['id'])
			venue.name = checkin['venue']['name']
			venue.primarycategory = category
			venue.address = checkin['venue']['address']
			try:
				venue.crossstreet = checkin['venue']['crossstreet']
			except:
				venue.crossstreet = "N/A"
			venue.city = checkin['venue']['city']
			venue.state = checkin['venue']['state']
			try:
				venue.zip = checkin['venue']['zip']
			except:
				venue.zip = 0
			venue.geolat = checkin['venue']['geolat']
			venue.geolong = checkin['venue']['geolong']
			try:
				venue.phone = checkin['venue']['phone']
			except:
				pass # phone is not a required field
			venue.save()
			# Add check-in to database
			try:
				checkinrecord = foursquare.CheckIn.objects.get(id=checkin['id'])
			except foursquare.CheckIn.DoesNotExist:
				checkinrecord = foursquare.CheckIn(id=checkin['id'])
			checkinrecord.user = user
			checkinrecord.venue = venue
			try:
				checkinrecord.shout = checkin['shout']
			except:
				pass # shout is not a required field
				#Thu, 21 May 09 18:09:22 +0000
			checkinrecord.created = datetime.datetime.strptime(checkin['created'], "%a, %d %b %y %H:%M:%S +0000")
			checkinrecord.save()