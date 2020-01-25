To obtain access token, use this page
https://developer.spotify.com/console/get-search-item/?q=U2&type=artist
OR do this programmatically, see login() below

```
client_id = '819baee8c39046b9938001576dd1f294'
client_secret = 'hidden'
pgiles:tmp$ echo -n '819baee8c39046b9938001576dd1f294:$client_secret' | base64
    HIDDEN...NmFkNzI2YmIxYWIxZThmMjU=
pgiles:tmp$ curl -X "POST" -H "Authorization: Basic HIDDEN...NmFkNzI2YmIxYWIxZThmMjU=" -d grant_type=client_credentials https://accounts.spotify.com/api/token
    {"access_token":"BQAq3Gwj7aT8ftRSILtGG...","token_type":"Bearer","expires_in":3600,"scope":""}
```