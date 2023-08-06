"""
Steamid OpenIdConnect:
"""
from social_core.backends.open_id_connect import OpenIdConnectAuth


class SteamIdOpenIdConnect(OpenIdConnectAuth):
    name = 'steamid-oidc'
    AUTHORIZATION_URL= 'https://steamid.steamforvietnam.net/oidc/auth'
    OIDC_ENDPOINT = 'http://steamid.steamid.svc.cluster.local/oidc'
    ID_TOKEN_ISSUER = 'https://steamid.steamforvietnam.net/oidc'

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Google API"""
        return self.get_json(
            'http://steamid.steamid.svc.cluster.local/oidc/me',
            params={'access_token': access_token, 'alt': 'json'}
        )
        
    def get_user_details(self, response):
        """Return user details from SteamId API account"""
        if 'email' in response:
            email = response['email']
        else:
            email = ''

        fullname = response.get('fullName', '')

        return {'username': email.split('@', 1)[0],
                'email': email,
                'fullname': fullname}