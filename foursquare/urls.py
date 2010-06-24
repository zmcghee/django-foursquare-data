from django.conf.urls.defaults import *

from foursquare.views import *

urlpatterns = patterns('foursquare.views',    
    url(r'^auth/$',
        view=auth,
        name='foursquare_oauth_auth'),
    url(r'^return/$',
        view=foursquare_return,
        name='foursquare_oauth_return'),
)