import oauth2 as oauth
from parseini import consumer_key, consumer_secret
import httplib, urllib

def upload(file_content, file_name, otaku):

    # Dropbox-specific paremeters to be encoded to url
    params = urllib.urlencode({'locale': 'en-US', 'overwrite': 'true'})

    # OAuth Authorization header
    auth_header = 'OAuth oauth_version="1.0",\
            oauth_signature_method="PLAINTEXT",\
            oauth_consumer_key="' + consumer_key + '",\
            oauth_token="' + otaku.access_token + '",\
            oauth_signature="' + consumer_secret + '&' + otaku.access_secret + '"'

    headers = {"Content-type": "image/png",
               "Accept": "text/plain",
               "Authorization": auth_header}

    conn = httplib.HTTPSConnection(
        "api-content.dropbox.com/1/files_put/sandbox/" + file_name
        + "?" + params)

    conn.request("POST", "", file_content, headers)
    response = conn.getresponse()

    data = response.read()
    conn.close()

    return data
