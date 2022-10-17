from discord import Message
from discord.interactions import Interaction
from discord.errors import InteractionResponded

import os




async def save_submission(msg:Message, event:str, interaction:Interaction):
    print(event, msg.author, msg.content)

    # try:
    #     await interaction.response.send_message(f'Your submission has been accepted for {event}')
    # # If its already been responded to
    # except InteractionResponded:
    #     pass

    await interaction.response.send_message(f'Your submission has been accepted for {event}')



def save_events(events:list):
    text = '\n'.join(events)
    with open('events.txt', 'w') as f:
        f.write(text)



def get_events():
    # Checks if the file doesnt exist
    if not os.path.exists('events.txt'):    return []
    with open('events.txt') as f:
        events = f.read().splitlines()

    return events




