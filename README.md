# Python-Rootkit
## Discord profile picture logger
#### Configuration:
```json
{
    "token": "Discord Token",
    "userIDs": ["userID", "userID2"],
    "serverID": serverID,
    "channelID": channelID,
    "scrapeEveryone": "false",
    "saveDir": "C:\\Users\\User\\Pictures\\ProfilePictures",
    "saveUsernameWithUnix": "true"
}
```
Make sure to rename settings-example.json to settings.json
Server and Channel ID are saved as an integer, bool values are stored in a string and directory needs the double backslash "\\"
#### To run:
```
py main.py
```
