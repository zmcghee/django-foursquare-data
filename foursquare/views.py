import foursquare.models as foursquare
from foursquare.utils import *
from djangofoursquare.views import *

def foursquare_return(request):
    """
	Most of this is lifted from djangofoursquare, but once the
	user is authenticated I'm calling my store_foursquare_user
	method instead of hooking into Auth.
    """
    unauthed_token = request.session.get('unauthed_token', None)
    
    if not unauthed_token:
        request.session['notice'] = "Sorry, we couldn't properly process your authentication. Please try again, and let us know if it consistently fails."
        return HttpResponseRedirect('/?error')
    token = oauth.OAuthToken.from_string(unauthed_token)
    
    if token.key != request.GET.get('oauth_token', 'no-token'):
        request.session['notice'] = "Sorry, we couldn't log you in."
        return HttpResponseRedirect('/?error')
    
    try:
        access_token = exchange_request_token_for_access_token(
                get_consumer(), get_connection(), token)
    except (KeyError, FoursquareError), e:
        request.session['notice'] = "Sorry, we experienced an error logging you in. Please try again."
        return HttpResponseRedirect('/?error')

    request.session['access_token'] = access_token.to_string()
    
    auth = is_authenticated(get_consumer(), get_connection(), access_token)
    if not auth:
        request.session['notice'] = "Sorry, you weren't authenticated by Foursquare."
        return HttpResponseRedirect('/?error')
        
    userdata = auth['user']
    
    try:
        user = store_foursquare_user(foursquare_user_data=userdata, 
                access_token=access_token)
    except FoursquareError, e:
        request.session['notice'] = "Sorry, we experienced an error logging you in. Please try again."
        return HttpResponseRedirect('/?error')
        
    if user is None:
        request.session['notice'] = "Sorry, you weren't authenticated by Foursquare."
        return HttpResponseRedirect('/?error')
                        
    return HttpResponseRedirect('/?success')