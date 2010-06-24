from django.db import models

class User(models.Model):
	id = models.IntegerField(primary_key=True)
	firstname = models.CharField(max_length=45)
	lastname = models.CharField(max_length=45, blank=True)
	photo = models.URLField()
	gender = models.CharField(max_length=6)
	email = models.EmailField()
	phone = models.CharField(max_length=10,blank=True,null=True)
	access_token = models.TextField(blank=True)
	
	def __unicode__(self):
		return "%s %s" % (self.firstname, self.lastname)

class Category(models.Model):
	id = models.IntegerField(primary_key=True)
	fullpathname = models.TextField()
	nodename = models.TextField()
	iconurl = models.URLField()
	
	def __unicode__(self):
		return "%s" % (self.fullpathname)
	
	class Meta:
		verbose_name_plural = "Categories"

class Venue(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100)
	primarycategory = models.ForeignKey(Category)
	address = models.CharField(max_length=150)
	crossstreet = models.CharField(max_length=150)
	city = models.CharField(max_length=150)
	state = models.CharField(max_length=2)
	zip = models.IntegerField(max_length=5)
	geolat = models.CharField(max_length=20)
	geolong = models.CharField(max_length=20)
	phone = models.IntegerField(blank=True,null=True)
	
	def __unicode__(self):
		return "%s" % (self.name)

class CheckIn(models.Model):
	id = models.IntegerField(primary_key=True)
	user = models.ForeignKey(User)
	venue = models.ForeignKey(Venue)
	shout = models.TextField(blank=True)
	created = models.DateTimeField()
	
	def __unicode__(self):
		return "%s at %s" % (self.id, self.venue)
	
	class Meta:
		verbose_name_plural = "Check-ins"