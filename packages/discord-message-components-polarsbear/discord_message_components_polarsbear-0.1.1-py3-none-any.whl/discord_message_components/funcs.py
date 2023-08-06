from typing import Union
import requests
import discord
import json
import zlib

from .classes import *
from .utils import removenone


global token


class Config:
    token:str
    _token: str

    def __init__(self):
        self._token = ""

    @property
    def token(self):
        return self._token.replace("Bot ","")

    @token.setter
    def token(self,v, bot=True):
        global token
        if bot:
            self._token = "Bot " + v
        else:
            self._token = v
        token = self._token

config = Config()
msgurl = "https://discord.com/api/channels/{0.id}/messages"
zlib_ = zlib.decompressobj()


async def send_message(channel:discord.TextChannel, content:str = "", embed:[discord.Embed] = None, components:[Component] = None, responds:discord.Message = None):
    url = msgurl.format(channel)
    headers = {"authorization":token,"content-type":"application/json"}
    if responds is not None:
        ref = {"message_id": responds.id, "channel_id": responds.channel.id, "guild_id": responds.guild.id}
    else:
        ref = None
    payload = removenone({"message_reference":ref,"content":content, "embed":embed.to_dict(), "components":[c.dict for c in components] if components.__class__.__name__ == "list" else components.dict if components.__class__.__name__ == "ComponentHelper" else [components.dict] if components is not None else None})
    response = requests.post(url,headers=headers,json=payload)

    return json.loads(response.content)


async def respond(interaction:ComponentInteraction, content:str = None, embed:[discord.Embed] = None, components:[Component] = None):
    url = f"https://discord.com/api/v8/interactions/{interaction.id}/{interaction.token}/callback"
    payload = removenone({"type":4,"data":removenone({"content":content,"embed":embed.to_dict(),"components":[c.dict for c in components] if components.__class__.__name__ == "list" else components.dict if components.__class__.__name__ == "ComponentHelper" else [components.dict] if components is not None else None})})
    headers = {"authorization":token}
    return json.loads(requests.post(url,headers=headers,json=payload).content)


async def websocket_wrap(msg):
    buffer = bytearray()
    buffer.extend(msg)
    _msg = zlib_.decompress(buffer)
    d = json.loads(_msg.decode())
    if d["t"] == "INTERACTION_CREATE" and d["d"]["type"] == 3:
        return ComponentInteraction(d)