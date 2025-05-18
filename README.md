# DiscordBot
The following code, is for a 30-minutes fun proyect for a personal, funtional discord bot that can do play, skip, and add a reproduction list, also add a funtion to stop when needed

## Features 

- Play music from YouTube (search or URL)
- Queue system for playback
- Skip current song
- Stop playback and clear queue
- Display queued songs
- Auto-disconnect after 1 minute of inactivity

## Prerequisites 

- Python 3.10 or higher
- FFmpeg installed ([Installation Guide](https://ffmpeg.org/download.html))
- Discord Developer Account
- Discord Bot Token

/ To clone this repository:

bash git clone https://github.com/LowProfile9/DiscordBot.git cd DiscordBot

/ Install dependencies:

pip install -r requirements.txt

/ Create a .env file and add your token:

DiscordToken=YOUR_TOKEN_HERE

/How to configure? 
1.Get Discord Token:
Create an application at Discord Developer Portal
Go to "Bot" > "Token" > "Copy"

2.Configure FFmpeg:
Update path in FFMPEG_OPTIONS according to your system
for Windows: 'executable': r'path\to\ffmpeg.exe

3.Bot Prefix(this is important):
Change if you want, but default is: command_prefix="!" 

/ How to command this bot in discord?
Command	Description	Example
!play <query>	Play or add to queue 
!skip	Skip current song	
!stop	Stop bot and clear queue
!queue_list	Show queued songs	
