import serial
import time
import httplib, urllib, base64
import json

s = serial.Serial("/dev/cu.usbmodem1411", 9600)

headers = {
    # Request headers...Key not included in GitHub because I don't want to get in trouble
    'Ocp-Apim-Subscription-Key': '',
}

params = urllib.urlencode({
})

# get the connecting for both API's we need
connTeams = httplib.HTTPSConnection('api.fantasydata.net')
connGames = httplib.HTTPSConnection('api.fantasydata.net')

# Make the request
connTeams.request("GET", "/mlb/v2/json/teams?%s" % params, "{body}", headers)
connGames.request("GET", "/mlb/v2/json/GamesByDate/2017-MAY-04?%s" % params, "{body}", headers)

# Get the responses
teamsResponse = connTeams.getresponse()
gamesResponse = connGames.getresponse()

# Read the responses
teams = teamsResponse.read()
games = gamesResponse.read()

# Read them as JSON...because thats better
teamsObject = json.loads(teams)
gamesObject = json.loads(games)

# Sleep a little to make it more legit...I guess
time.sleep(2)
string = raw_input('Enter your team to get their score!: ')
string = str.strip(string)

for x in range(0 , 30):
    # Getting each team name to check
    teamName = teamsObject[x]["Name"]
    if string == teamName:
        # We got the team they entered so lets get the key (So if they entered in Phillies the key would be PHI)
        teamKey = teamsObject[x]["Key"]
        for i in range(0, len(gamesObject)):
            # We need both home and away key to check (we don't know if the team is playing home or away)
            awayKey = gamesObject[i]["AwayTeam"]
            homeKey = gamesObject[i]["HomeTeam"]
            if teamKey == awayKey or homeKey == teamKey:
                # Found the teams...lets get the correct keys and scores
                print("Found teams playing...")
                newAwayKey = gamesObject[i]["AwayTeam"] # Python is weird because I had grab the key again
                newHomeKey = gamesObject[i]["HomeTeam"]

                # Getting the scores
                scoreAway = gamesObject[i]["AwayTeamRuns"]
                scoreHome = gamesObject[i]["HomeTeamRuns"]
                print("Got scores!")

# If we got the score
try:
    s.write(newAwayKey.encode() + ": " + str(scoreAway) + " " + newHomeKey.encode() + ": " + str(scoreHome))
# If we didn't get the score...The games API call only includes the games played on the specified date
except NameError:
    s.write ("Team not playing today!")

connTeams.close()
connGames.close()
