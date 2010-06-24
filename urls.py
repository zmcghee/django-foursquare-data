from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^foursquare/', include('foursquare.urls')),
    url(r'^load_history/', view='contest.views.history', name='load_user_history'),
    (r'', 'contest.views.homepage'),
)
