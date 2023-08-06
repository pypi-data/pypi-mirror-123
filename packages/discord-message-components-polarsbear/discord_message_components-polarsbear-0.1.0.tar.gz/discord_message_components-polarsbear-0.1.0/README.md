# Discord Message Components
A python library that adds message component support to discord bots
 

## Usage
### I will add proper documentation very soon
```python
from discord_message_components import *
from discord.ext.commands import Bot
import discord

bot = Bot("prefix")

components = ComponentHelper()
button = Button("visible label", 1, "custom_id")
components.addComponent(button)

@bot.event
async def on_socket_raw_receive(msg):
    interaction = await websocket_wrap(msg)
    if interaction is not None: # Making sure the interaction actually happened and was for message components
        await respond(interaction,f"{interaction.member_data.username} clicked button {components.getFirstComponent(interaction.data.custom_id)}") # This acts just like discord_message_components.send_message, except it requires an interaction, and cannot have a message reference
```