# discord-bot
python3  nextcord bot com sqlite start easy with:
```
git clone https://github.com/peccato/discord-bot.git
cd discord-bot
virtualenv discordbot
source discordbot/bin/activate
pip install -r requeriments.txt
```
configure bot prefix,languague and token in config.json file
currently there are 2 languages in the langs/ folder usable to configure in config.json
<br>
. `pt-br` brazilian portuguese languague
<br/>
. `en-us` English languague
<br/>



<br />
and your bot is ready to run with the command:
`python main.py`

the bot already comes with the following commands:<br/>

. `ship` Command for fun, mentioning two people along with the command appears a random percentage of affinity.
<br/>
. `editplay` Edits the bot's current activity in the user list.
<br/>
. `ping` Command to test bot response time.
<br/>
. `give` Command to transfer balance to another user
<br/>
. `daily` Command to redeem the daily gift
<br/>
. `weekly` Command to redeem the weekly gift
<br/>
. `rank` Shows the current rank of coins
<br/>
. `help` Show list of bot commands
