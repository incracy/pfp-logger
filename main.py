import discord
import requests
import os
import time
import json
from datetime import datetime

with open("settings.json", "r") as f:
    settings = json.load(f)

token = settings.get("token")
userIDs = settings.get("userIDs")
serverID = settings.get("serverID")
channelID = settings.get("channelID")

scrapeEveryone = settings.get("scrapeEveryone")
saveDir = settings.get("saveDir")
saveUsernameWithUnix = settings.get("saveUsernameWithUnix")

def countByWalk(dir):
    total = 0

    for root, dirs, files in os.walk(dir):
        total += len(files)

    return total

print(f"\n", 
      f"User ID(s): {userIDs}\n", 
      f"Server ID :{serverID}\n", 
      f"Channel ID: {channelID}\n", 
      f"Scrape Everyone: {scrapeEveryone}\n", 
      f"Save Directory: {saveDir}\n", 
      f"Save Username with Unix Timestamp: {saveUsernameWithUnix}\n\n")

class Client(discord.Client):
    async def on_ready(self):
        current_time = datetime.now()
        formatted_time = current_time.strftime("[%Y-%m-%d %H:%M:%S]")  
        print(f'{formatted_time} [INFO    ] Logged in as {self.user}')

    async def on_user_update(self, before, after):
        if scrapeEveryone == "true":
            total = countByWalk(saveDir)
            current_time = datetime.now()
            formatted_time = current_time.strftime("[%Y-%m-%d %H:%M:%S]")     
            
            server = self.get_guild(serverID)
            channel = server.get_channel(channelID)

            avatar_url = str(after.avatar.url)

            save_directory = os.path.join(saveDir, str(after.id))
            os.makedirs(save_directory, exist_ok=True)

            current_time = int(time.time())
            if saveUsernameWithUnix == "true":
                save_path = os.path.join(save_directory, f'{before.name}_{current_time}.png')
            else:
                save_path = os.path.join(save_directory, f'{before}_{current_time}.png')

            response = requests.get(avatar_url)
            with open(save_path, 'wb') as file:
                file.write(response.content)

            num_files = len([file for file in os.listdir(save_directory) if os.path.isfile(os.path.join(save_directory, file))])

            print(f'{formatted_time} [INFO    ] {before} changed their profile picture')
            await channel.send(f'{before} (<@{before.id}>) updated their profile picture ({num_files}/{str(total)})', file=discord.File(save_path))
        else:
            total = countByWalk(saveDir)
            if after.id in userIDs and before.avatar != after.avatar:
                current_time = datetime.now()
                formatted_time = current_time.strftime("[%Y-%m-%d %H:%M:%S]") 

                server = self.get_guild(serverID)
                channel = server.get_channel(channelID)

                avatar_url = str(after.avatar.url)

                save_directory = os.path.join(saveDir, str(after.id))
                os.makedirs(save_directory, exist_ok=True)

                current_time = int(time.time())
                if saveUsernameWithUnix == "true":
                    save_path = os.path.join(save_directory, f'{before.name}_{current_time}.png')
                else:
                    save_path = os.path.join(save_directory, f'{before}_{current_time}.png')

                response = requests.get(avatar_url)
                with open(save_path, 'wb') as file:
                    file.write(response.content)

                num_files = len([file for file in os.listdir(save_directory) if os.path.isfile(os.path.join(save_directory, file))])

                print(f'{formatted_time} [INFO    ] {before} changed their profile picture')
                await channel.send(f'{before} (<@{before.id}>) updated their profile picture ({num_files}/{str(total)})', file=discord.File(save_path))

client = Client()
client.run(token)