from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Location, Neighbourhood, Business
from django.db import models
# Create your tests here.
class ProfileTestCase(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username='user1')
        self.anum = Profile.objects.create(user=self.u1)

    def tearDown(self):
        self.anum.delete()
        self.u1.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.anum, Profile))

    def test_save_profile(self):
        self.anum.save_profile()
        profiles=Profile.objects.all()
        self.assertTrue(len(profiles)>0)

    def test_search_profile(self):
        self.anum.save_profile()
        profile= Profile.search_profile(self.anum)
        self.assertTrue(len(profile)>0)

    def test_get_by_id(self):
        self.anum.save_profile()
        profile=Profile.get_by_id(self.anum)
        self.assertTrue(profile!=None)

# Create your tests here.
class NeighbourhoodTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create(username='user1')
        self.location=Location.objects.create(name='Nairobi')
        self.neighbourhood=Neighbourhood.objects.create(name="Lavington",occupants_count=2000,admin=self.admin,location=self.location) 
        
    def tearDown(self):    
        self.admin.delete()
        
    def test_instance(self):
        self.assertTrue(isinstance(self.neighbourhood, Neighbourhood)) 

    def test_save_hood(self):
        self.neighbourhood.save()
        hoods=Neighbourhood.objects.all()
        self.assertTrue(len(hoods)>0)

    def test_delete_neighbourhood(self):
        self.neighbourhood.save()
        Neighbourhood.delete_neighbourhood(self.neighbourhood.id)
        hood=Neighbourhood.objects.filter(id=self.neighbourhood.id).first()
        self.assertTrue(hood==None)        

    def test_update_occupants(self):
        self.neighbourhood.save()
        Neighbourhood.update_occupants(self.neighbourhood.id, 1800)
        hood=Neighbourhood.objects.filter(id=self.neighbourhood.id).first()
        self.assertTrue(hood.occupants_count==1800)
     
     
class BusinessTestCase(TestCase):
    def setUp(self):
        self.owner = User.objects.create(username='user1')
        self.location=Location.objects.create(name='Nairobi')
        self.neighbourhood=Neighbourhood.objects.create(name="Lavington",occupants_count=2000,admin=self.owner,location=self.location) 
        self.business=Business.objects.create(name='Barber', owner=self.owner,neighbourhood=self.neighbourhood, email="anum@yahoo.com")

    
    def tearDown(self):    
        self.owner.delete()
        self.location.delete()
        self.neighbourhood.delete()
        self.business.delete()
        
    def test_instance(self):
        self.assertTrue(isinstance(self.business, Business)) 

    def test_save_busioness(self):
        self.business.save_business()
        business=Business.objects.all()
        self.assertTrue(len(business)>0)
    