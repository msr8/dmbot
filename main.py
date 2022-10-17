from   discord.ext import commands
import discord

import funcs

import json





# Loads the config
with open('config.json') as f:
    config:dict = json.load(f)
# Defines the ongoing events var
events = []

intents = discord.Intents.default()
bot     = commands.Bot(intents=intents)
# bot     = commands.Bot(guild_ids=[1028742298563002490, 1029927181327007815], intents=intents)







class Dropdown(discord.ui.Select):
    def __init__(self, bot_: discord.Bot, msg:discord.Message):
        self.bot = bot_
        self.msg = msg
        # Set the options that will be presented inside the dropdown:
        options = [discord.SelectOption(label=i) for i in funcs.get_events()]

        super().__init__(
            placeholder="Choose the event",
            min_values=1,
            max_values=1,
            options=options,
        )

    # When the user selects an option, submit the message for that event
    async def callback(self, interaction: discord.Interaction):
        event = self.values[0]
        await funcs.save_submission(self.msg, event, interaction)



class MyView(discord.ui.View):

    def __init__(self, bot_: discord.Bot, msg:discord.Message ):
        self.bot = bot_
        self.msg = msg
        super().__init__()

        # Adds the dropdown to our View object
        self.add_item(Dropdown(self.bot, self.msg))




















@bot.event
async def on_connect():
    print('I am up!\n')

    if bot.auto_sync_commands:
        await bot.sync_commands()




    
    






@bot.slash_command(name='event',  description='Start an event')
@discord.option(name='action',    choices=['list', 'start', 'stop'], description='Wether you want to start/stop an event or list all the ongoing events')
@discord.option(name='name',      default='', description='Name of the event to start/stop')
async def _(ctx:discord.ApplicationContext, action:str, name:str):
    events      = funcs.get_events()
    orig_events = events.copy()

    # If user wants to see the ongoing events
    if action == 'list':
        text = '\n'.join(events) if events else 'There are no ongoing events'

    # If a mod wants to start an event
    elif action == 'start':
        # Checks if event name is given
        if not name:
            text = 'No event name given'
        else:
            events.append(name)
            text = f'{name} has been started'
    
    # If a mod wants to stop an event
    elif action == 'stop':
        # Checks if event name is given
        if not name:
            text = 'No event name given'
        else:
            # Checks if the event is ongoing or not
            if not name in events:
                text = f'There is no ongoing event named {name}'
            # Stops the event
            else:
                events.remove(name)
                text = f'{name} has been stopped'

    await ctx.respond(text)

    # Saves the events if there was any change
    if len(events) != len(orig_events):
        funcs.save_events(events)



@bot.message_command(name='Submit')
async def _(ctx:discord.ApplicationContext, msg:discord.Message):
    # Checks if its a DM
    if not isinstance(msg.channel, discord.DMChannel):
        await ctx.respond('Please DM me the submission'); return
    # Checks if its not by a bot
    if msg.author.bot:
        await ctx.respond('Unfortunately, bots cannot participate'); return

    events = funcs.get_events()
    # Checks if no event is going on
    if not events:
        await ctx.respond('No events are currently going on')

    # Checks if only one event is going on
    elif len(events) == 1:
        event = events[0]
        await funcs.save_submission(msg, event, ctx.interaction)
    
    # Otherwise, shows the dropdown
    else:
        await ctx.respond(view=MyView(bot, msg))








@bot.slash_command(name='test',  description='tests smth')
async def _(ctx:discord.ApplicationContext):
    events = funcs.get_events()
    events.append('1')
    events.append('3')
    funcs.save_events(events)
    await ctx.respond('Done')












bot.run(config['token'])








'''
-> Help Command

'''

