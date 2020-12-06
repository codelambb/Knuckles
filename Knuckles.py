import discord
from discord.ext import commands, tasks
import os
from random import choice
import aiohttp
from random import randint
import time
import datetime
import asyncio
import random
import typing

intents = discord.Intents.all()
prefixes = ["!"]
client = commands.Bot(command_prefix=list(prefixes),intents = intents)

client = commands.Bot(command_prefix = prefixes)

status = ['Listening to !help', 'Make sure to read the rules!']

client.remove_command("help")

@client.event
async def on_ready():
	change_status.start()
	print('Bot is ready.')

@tasks.loop(seconds=20)
async def change_status():
	await client.change_presence(activity=discord.Game(choice(status)))

#ping command
@client.command()
async def ping(ctx):
	await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

#clear command
@client.command(aliases=["cls", "purge"])
@commands.has_permissions(manage_messages=True, administrator=True)
async def clear(ctx, ammount:int):
	await ctx.channel.purge(limit=ammount+1)
	await ctx.send(f'I have deleted {ammount} of messages', delete_after=5)
	return

#8ball command
@client.command(aliases=['8ball'])
async def _8ball(ctx, question):
	import random
	responses = ["It is certain.",
				"It is decidedly so.",
				"Without a doubt.",
				"Yes - definitely.",
				"You may rely on it.",
				"As I see it, yes.",
				"Most likely.",
				"Outlook good.",
				"Yes.",
				"Signs point to yes.",
				"Reply hazy, try again.",
				"Ask again later.",
				"Better not tell you now.",
				"Cannot predict now.",
				"Concentrate and ask again.",
				"Don't count on it.",
				"My reply is no.",
				"My sources say no.",
				"Outlook not so good.",
				"Very doubtful."]
	await ctx.send(f'{random.choice(responses)}')

#help command
@client.command(aliases=['h'])
async def help(ctx):
	helpEmbed = discord.Embed(tittle="Help Menu", color=ctx.author.color)
	helpEmbed.set_author(name="Help Menu:\nPrefix = '!'")
	helpEmbed.add_field(name="Moderation Command Menu", value="```Type !modHelp to open that```", inline=True)
	helpEmbed.add_field(name="Miscellaneous Command Menu", value="```Type !miscHelp to open that```", inline=True)

	await ctx.send(embed=helpEmbed)

#modHelp
@client.command(aliases=['mocd'])
async def modHelp(ctx):
	mod = discord.Embed(tittle="mod", color=ctx.author.color)
	mod.add_field(name="Moderation Command Menu", value="```!clear (ammount) : Deletes the specified ammount of messages from the channel```\n```!ban (user) (reasion) : Bans the specified user from the server```\n```!kick (user) (reason) : Kicks the specified user from the server```\n```!mute (user) (reason) : Mutes the specified user from the server```\n```!unmute (user) : Unmutes the specified user```\n```!announce (message) : Sends a announcemnt in the server with and embed style```\n")
	mod.set_footer(text="More moderation commands will be added soon")
	await ctx.send(embed=mod)

#miscHelp
@client.command(aliases=['micd'])
async def miscHelp(ctx):
	misc = discord.Embed(tittle="misc", color=ctx.author.color)
	misc.add_field(name="Miscellaneous Command Menu", value="```!ping : Tells the bot's latency```\n```!8ball (question) : Tells the answer of the asked question in a random yes/no answer```\n```!meme : Send a hot meme from reddit```\n")
	misc.set_footer(text="More miscellaneous commands will be added soon")
	await ctx.send(embed=misc)

#ban command
@client.command(aliases=['b'])
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
	await ctx.send(f'Banned {member} from the server.')
	await member.ban(reason=reason)

#kick command
@client.command(aliases=['k'])
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
	await ctx.send(f'Kicked {member} from the server.')
	await member.kick(reason=reason)

#mute command
@client.command(aliases=['m'])
@commands.has_permissions(manage_roles=True, administrator=True)
async def mute(ctx, member: discord.Member, *, reason="No reason provided"):
	await ctx.send(f'Muted {member}.')
	await member.send(f'You have been muted in the server {guild.name} for {reason}')
	muted_role = discord.utils.find(ctx.guild.roles, name="Muted")
	await member.add_role(muted_role, reason=reason)

#unmute command
@client.command()
@commands.has_permissions(manage_roles=True, administrator=True)
async def unmute(ctx, member: discord.Member):
	mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
	await member.remove_roles(mutedRole)
	await ctx.send(f'Unmuted {members.mention}')
	await member.send(f'You have been unmuted from the server {guild.name}')

#meme command 
@client.command()
async def meme(ctx):
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://www.reddit.com/r/dankmemes/new.json?sort=hot,") as r:
                res = await r.json()
                embed = discord.Embed(title="Here is a meme", color=0x00FFFF)
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)

#announcemnt command
@client.command(aliases=["ann"])
@commands.has_permissions(administrator=True, manage_messages=True, manage_roles=True, ban_members=True, kick_members=True)
async def announce(ctx, message ):
	anno = discord.Embed(tittle="ann", color=ctx.author.color)
	anno.add_field(name="Announcement", value=message)
	anno.set_footer(text=f'Announcement by {ctx.author.mention}')
	await ctx.send(embed=anno) 

client.run(os.environ['DISCORD_TOKEN'])