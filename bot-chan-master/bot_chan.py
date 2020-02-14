#!/usr/local/bin/python3

import discord
import asyncio
from check_rss import getRelease
import tinify

tinify.key = "key"

client = discord.Client()

channel = discord.Object(id='ID') #id of the moderators channel
channel2 = discord.Object(id='ID2') #id of the general channel
bans = []

async def my_background_task():
    await client.wait_until_ready()
    while not client.is_closed:
        release = getRelease()
        if release!=None:
            await client.send_message(channel2, release)
        await asyncio.sleep(120)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.channel.is_private:
        mp = await client.send_message(message.channel, 'hello')
        await client.edit_message(tmp, 'Hello.')
    elif message.content.startswith('!crop') and len(message.attachments)>0:
        source = tinify.from_url(message.attachments[0]['url'])
        resized = source.resize(
            method="cover",
            width=128,
            height=128
        )
        resized.to_file("img.png")
        await client.send_file(message.channel, "img.png")
    elif message.content.startswith('!crop') and len(message.embeds)>0:
        source = tinify.from_url(message.embeds[0]['url'])
        resized = source.resize(
            method="cover",
            width=128,
            height=128
        )
        resized.to_file("img.png")
        await client.send_file(message.channel, "img.png")

@client.event
async def on_member_ban(server):
	global bans
	bans.append(client.user)
	msg = '**{0.name}** was banned from the server.'.format(server)
	await client.send_message(channel, msg)

@client.event
async def on_member_remove(server):
    if (client.user not in bans):
        msg = '**{0.name}** left or was kicked from the server.'.format(server)
        await client.send_message(channel, msg)

@client.event
async def on_member_join(server):
    msg = '**{0.name}** has joined the server.'.format(server)
    await client.send_message(channel, msg)

@client.event
async def on_member_unban(server, user):
    msg = '**{0.name}** was unbanned.'.format(user)
    await client.send_message(channel, msg)
    global bans
    if (client.user in bans):
        bans.remove(client.user)

loop = asyncio.get_event_loop()

try:
    loop.create_task(my_background_task())
    loop.run_until_complete(client.login('token'))
    loop.run_until_complete(client.connect())
except Exception:
    loop.run_until_complete(client.close())
finally:
    loop.close()
