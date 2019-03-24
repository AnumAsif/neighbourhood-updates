from django.db import models
from django.contrib.auth.models import User
from pyuploadcare.dj.models import ImageField


class Location(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def save_location(self):
        self.save() 
        
class Neighbourhood(models.Model):
    '''
    contain user's neighbourhood information
    '''
    name=models.CharField(max_length=50)
    occupants_count=models.IntegerField(null=True)
    admin=models.ForeignKey(User, on_delete=models.CASCADE)
    location=models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering=('name',)

    def save_neighbourhood(self):
        self.save()

    
    @classmethod
    def delete_neighbourhood(cls, neighbourhood_id):
        hood = Neighbourhood.objects.filter(id=neighbourhood_id).first()
        hood.delete()
    @classmethod
    def find_neighbourhood(cls,neighbourhood_id):
        hood = Neighbourhood.objects.filter(id=neighbourhood_id).first()
        return hood

    @classmethod
    def update_occupants(cls, neighbourhood_id, occupants):
        hood = Neighbourhood.objects.filter(id=neighbourhood_id).first()
        hood.occupants_count=occupants
        hood.save() 

    # def update_    
class Profile(models.Model):
    '''
    Extend django user authentication model
    '''
    user=models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name=models.CharField(max_length=30,null=True)
    last_name=models.CharField(max_length=30,null=True)
    profile_pic=ImageField(blank=True, manual_crop='200x200')
    bio=models.TextField(max_length=200,null=True)
    contact_no=models.IntegerField(null=True)
    email=models.EmailField(null=True)
    neighbourhood=models.ForeignKey('Neighbourhood', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

    def save_profile(self):
        self.save()

    @classmethod
    def search_profile(cls, name):
        profile=Profile.objects.filter(user__username__icontains=name)
        return profile 

    @classmethod
    def get_by_id(cls, id):
        profile=Profile.objects.get(user=id)
        return profile 

    @classmethod
    def filter_by_id(cls, id): 
        profile=Profile.objects.filter(user=id).first()
        return profile    

class Business(models.Model):
    name=models.CharField(max_length=50)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    neighbourhood=models.ForeignKey('Neighbourhood',on_delete=models.CASCADE)
    email=models.EmailField(blank=True)
    
    def __str__(self):
        return self.title

    def save_business(self):
        self.save()    

    @classmethod
    def delete_business(cls,name):
        business=Business.objects.filter(name=name)
        business.delete()
    
    @classmethod
    def find_business(cls, name):    
        businesses=Business.objects.filter(name__icontains=name)
        return businesses

    @classmethod
    def update_details(cls, id, name, email, neighbourhood):
        business=Business.objects.filter(id=id)
        business.email=email
        business.name=name
        business.neighbourhood=neighbourhood
        business.save()


           
# class Category(models.Model):
#     name=models.CharField(max_length=50)    
