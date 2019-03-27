from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [    
    url(r'^home/$', views.home, name = 'home'),
    url(r'^$',views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'profile/(?P<username>\w+)', views.profile, name='profile'),  
    url(r'^edit/',views.edit_profile, name='edit_profile'),
    url(r'^add_neighbourhood/$', views.add_neighbourhood, name="add_neighbourhood"),
    url(r'^neighbourhood/(?P<hood_id>\d+)', views.hood_details, name = 'hood_details'),
    url(r'^add_business/(?P<hood_id>\d+)', views.add_business, name="add_business"),
    url(r'^search/(?P<hood_id>\d+)', views.search, name="search"),

] 
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

        