# PleaseExplain

Ever tried reading a Discord conversation before asking yourself, 'What the hell do these words even mean? What are they saying? Is this communication?"  

PleaseExplain is a Discord bot which offers a solution to this mayhem by allowing you to define certain words or phrases.  

Now you don't need to be versed in seven layers of irony and inside jokes to participate in a regular conversion!

## Running the Bot

The bot is currently hosted on DigitalOcean, and you can invite it to your server through this link:  
https://discord.com/oauth2/authorize?client_id=1128976599677665411  
However, note that I'm not planning to host it forever, and your data could be lost.  

Instead, feel free to clone this project, create an application and bot on the Discord Developer Portal, and paste the token in a .env file under the label TOKEN=  
Make sure to install the dependencies in requirements.txt.  
You may also need to create a directory called database/ under which an SQLite database file will be created.  
Finally, just run main.py, and optionally set it as a system process to keep the bot operational.  


## App Commands

`/pleaseexplain [term]`  
Displays a beautiful, succinct explanation of a term, given that it has been defined by somebody.

`/define [term] [definition]`  
Simple as it sounds. Associates a term, which could be a word or phrase, with a specific definition. Feel free to include examples.  

`/undefine [term]`  
Removes that term from the dictionary.  

`/dictionary`  
Displays all of the terms in your server.  

`/random`  
Displays a random definition. Go crazy, learn some new vocabulary.  

`/usage_counting [on/off]`  
Controls whether the bot reads messages to count the amount of times a term has been used.  

`/clear_data [type]`  
Permenantly removes certain type of data (usage, dictionary, etc.) held by the bot.  

`/view_config`  
Displays the current configs you have saved for your server.  

## 

<div align="center">
  <a href="https://shipwrecked.hackclub.com/?t=ghrm" target="_blank">
    <img src="https://hc-cdn.hel1.your-objectstorage.com/s/v3/739361f1d440b17fc9e2f74e49fc185d86cbec14_badge.png" 
         alt="This project is part of Shipwrecked, the world's first hackathon on an island!" 
         style="width: 35%;">
  </a>
</div>
