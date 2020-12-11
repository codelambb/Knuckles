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
client = commands.Bot(command_prefix=prefixes, intents=intents)

status = ['Listening to !help', 'Make sure to read the rules!']

client.remove_command("help")

filter_words = ["fuck","bitch","pussy","chutiya","sala","arse"]

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
async def clear(ctx, ammount: int):
    await ctx.channel.purge(limit=ammount + 1)
    await ctx.send(f'I have deleted {ammount} of messages', delete_after=5)
    return

#reaction roles    
@client.event
async def on_reaction_add(ctx, reaction, user):
    channel = client.get_channel(784259046533365801)
    if reaction.channel.id == channel:
      if reaction.emoji == "🏃":
        Role = discord.utils.get(ctx.guild.roles, name="Blue")
        await user.add_roles(Role)

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
	helpEmbed.add_field(name="Moderation Command Menu", value="```Type !modhelp to open that```", inline=True)
	helpEmbed.add_field(name="Miscellaneous Command Menu", value="```Type !mischelp to open that```", inline=True)

	await ctx.send(embed=helpEmbed)

#modHelp
@client.command()
async def modhelp(ctx):
	mod = discord.Embed(tittle="mod", color=ctx.author.color)
	mod.add_field(name="Moderation Command Menu", value="```!clear (ammount) : Deletes the specified ammount of messages from the channel```\n```!ban (user) (reasion) : Bans the specified user from the server```\n```!kick (user) (reason) : Kicks the specified user from the server```\n```!mute (user) (reason) : Mutes the specified user from the server```\n```!unmute (user) : Unmutes the specified user```\n```!announce (message) : Makes an announcemnt with sylish embed style```\n")
	mod.set_footer(text="More moderation commands will be added soon")
	await ctx.send(embed=mod)

#miscHelp
@client.command()
async def mischelp(ctx):
	misc = discord.Embed(tittle="misc", color=ctx.author.color)
	misc.add_field(name="Miscellaneous Command Menu", value="```!ping : Tells the bot's latency```\n```!8ball (question) : Tells the answer of the asked question in a random yes/no answer```\n```!meme : Send a hot meme from reddit```\n```!serverinfo : Send info about server```\n```!userinfo (user) : Send info about specified user```\n")
	misc.set_footer(text="More miscellaneous commands will be added soon")
	await ctx.send(embed=misc)

#ban command
@client.command(aliases=['b'])
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
	await ctx.send(f'Banned {member} from the server. BOOM!')
	await member.ban(reason=reason)

#kick command
@client.command(aliases=['k'])
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
	await ctx.send(f'Kicked {member} from the server.')
	await member.kick(reason=reason)

#mute command
@client.command()
@commands.has_permissions(kick_members=True, manage_messages=True, administrator=True, manage_roles=True)
async def mute(ctx, member: discord.Member, mute_time, *, reason=None):
    if not member:
        await ctx.send("Who do you want me to mute?")
        return
    role = discord.utils.get(ctx.guild.roles, name="Muted")

    if not role:
        await ctx.guild.create_role(name='Muted')

    for channel in ctx.guild.channels:
            await channel.set_permissions(role, speak=False, send_messages=False, read_message_history=True, read_messages=True)

    await member.add_roles(role)
    await ctx.send(f"{member.mention} was muted for {reason}")

    if mute_time[-1] == 's':
    	x = int(mute_time[0:-1])
    	await asyncio.sleep(x)
    	await member.remove_roles(role)
    	await ctx.send(f"{member.mention} was unmuted")

    elif mute_time[-1] == 'm':
    	x = int(mute_time[0:-1]) * 60
    	await asyncio.sleep(x)
    	await member.remove_roles(role)
    	await ctx.send(f"{member.mention} was unmuted")
    

    elif mute_time[-1] == 'h':
    	x = int(mute_time[0:-1]) * 3600
    	await asyncio.sleep(x)
    	await member.remove_roles(role)
    	await ctx.send(f"{member.mention} was unmuted")

    elif mute_time[-1] == 'd':
    	x = int(mute_time[0:-1] * 86400)
    	await asyncio.sleep(x)
    	await member.remove_roles(role)
    	await ctx.send(f"{member.mention} was unmuted")

#unmute command
@client.command()
@commands.has_permissions(manage_roles=True, administrator=True)
async def unmute(ctx, member: discord.Member):
	mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
	await member.remove_roles(mutedRole)
	await ctx.send(f'Unmuted {member}')

#meme command
@client.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get ('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed = discord.Embed(title = "Memes", color = discord.Color.orange())
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)
            
#kill command
@client.command()
async def kill(ctx, user):
	k = random.randint(0,5)
	if k == 0:
		await ctx.send(f'You challenged {user} to a fist fight to the death. You won.')
	if k == 2:
		await ctx.send(f'{user} had a mid air collision with nyan-cat')
	if k == 3:
		await ctx.send(f'{user} fell down a cliff while playing Pokemon Go. Good job on keeping your nose in that puny phone. :iphone:')
	if k == 4:
		await ctx.send(f"{user} presses a random button and is teleported to the height of 100m, allowing them to fall to their inevitable death.\nMoral of the story: Don't go around pressing random buttons.")
	if k == 5:
		await ctx.send(f'{user} is sucked into Minecraft. {user}, being a noob at the so called Real-Life Minecraft faces the Game Over screen.')



#announcemnt command
@client.command(aliases=["ann"])
@commands.has_permissions(administrator=True, manage_messages=True, manage_roles=True, ban_members=True, kick_members=True)
async def announce(ctx,*,message):
	anno = discord.Embed(tittle="ann", color=ctx.author.color)
	anno.add_field(name="Announcement", value=message)
	anno.set_footer(text=f"Announcement by {ctx.author.name}")
	await ctx.channel.purge(limit=1)
	await ctx.send(embed=anno)
	await ctx.send("@Announcements", delete_after=3)

#swear stopper
@client.event
async def on_message(msg):
  for word in filter_words:
    if word in msg.content:
      await msg.delete()
      await msg.channel.send(f"{msg.author.mention}, Swearing is not allowed in this server")
  
  #Good night message
  if msg == 'gn' or msg == 'good night':
    await msg.channel.send("Good Night!")

  #Good morning message
  if msg == 'gm' or msg == 'good morning':
    await msg.channel.send("Good Morning")

  await client.process_commands(msg)

#verify command
@client.command()
@commands.has_role("Not Verified")
async def verify(ctx):
  verifiedrole = discord.utils.get(ctx.guild.roles, name='Members')
  await ctx.author.add_roles(verifiedrole)
  verify = discord.Embed(title="Verification",description="Congrats! You have been verified!", color=ctx.author.color)
  await ctx.author.send(embed=verify)
  await ctx.send(embed=verify)
  u = discord.utils.get(ctx.guild.roles, name='Not Verified')
  e = discord.utils.get(ctx.guild.roles, name='⁣  ⁣    ⁣     About Me⁣  ⁣    ⁣')
  x = discord.utils.get(ctx.guild.roles, name='⁣  ⁣    ⁣    Games I play ⁣   ⁣      ⁣ ⁣')
  y = discord.utils.get(ctx.guild.roles, name='⁣   ⁣ ⁣   ⁣ ⁣     Pings         ⁣  ⁣ ⁣ ⁣')
  await ctx.author.remove_roles(u)
  await ctx.author.add_roles(e)
  await ctx.author.add_roles(x)
  await ctx.author.add_roles(y)
  wel = discord.Embed(title=f"Welcome {ctx.author.name} to 𝗕𝗿𝘂𝘁𝗲 𝗙𝗼𝗿𝗰𝗲 𝗢𝗻𝗹𝘆 ™", color=discord.Color.red())
  wel.add_field(name="Here you can find:",value="🎮》Gaming and game chat\n🎮》Game nights (coming soon)\n🎮》Music\n🎮》Fun bots to entertain you :)\n", inline=False)
  wel.add_field(name="Check out these channels!!!", value="#🏡》about-us - to know about us\n#📜》rules - make sure to follow them\n#📊》self-roles - give yourself some cool roles\n", inline=False)
  wel.set_thumbnail(url=ctx.author.avatar_url)
  wel.set_image(url='https://images-ext-2.discordapp.net/external/bv_iH_uxZrUrqYi4Sn6sQJg70dGllmRNPMELNCzudlU/%3Fwidth%3D627%26height%3D390/https/media.discordapp.net/attachments/775232813510426694/782935786470899772/Presentation1.png')
  chl = client.get_channel(771251330920480788)
  await chl.send(embed=wel)

#server info command
@client.command(aliases=['si'])
async def serverinfo(ctx):
  guild=ctx.guild

  em=discord.Embed(title=f"{guild.name} info", color=ctx.author.color)
  em.set_footer(text=f'Requested by {ctx.author.name}')
  em.add_field(name='Total members', value=f"{guild.member_count}")
  em.add_field(name="Owner", value="DarkStalker.GG#6909")
  em.add_field(name="Server created on:", value=guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

  await ctx.send(embed=em)

#userinfo command
@client.command(aliases=["ui"])
async def userinfo(ctx, member: discord.Member):
  
  em=discord.Embed(color=member.color)

  em.set_author(name=f"{member.name}'s info")
  em.set_thumbnail(url=member.avatar_url)
  em.set_footer(text=f"Requested by {ctx.author.name}")

  em.add_field(name='Member Name', value=member.name)
  em.add_field(name="Member name in guild", value=member.display_name)

  em.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

  await ctx.send(embed=em)

#eval command
@client.command()
async def eval(ctx):
	await ctx.send('Type !add (1st number) (2nd number)')
	await ctx.send('Type !sub (1st number) (2nd number)')
	await ctx.send('Type !multi (1st number) (2nd number)')
	await ctx.send('Type !div (1st number) (2nd number)')

#sub command
@client.command()
async def add(ctx, x, y):
	u = int(x) - int(y)
	await ctx.send(f'Sum after adding {x} and {y} is {u}')

#sub command
@client.command()
async def sum(ctx, x, y):
	u = int(x) - int(y)
	await ctx.send(f'Difference after subtracting {y} from {x} is {u}')

#multi command
@client.command()
async def multi(ctx, x, y):
	u = int(x) * int(y)
	await ctx.send(f'Product after multiplying {x} and {y} is {u}')

#div command
@client.command()
async def div(ctx, x, y):
	u = int(x) / int(y)
	await ctx.send(f'Quotient after dividing {y} from {x} is {u}')

#Blue command add
@client.command()
async def add_Blue(ctx):
	b = discord.utils.get(ctx.guild.roles, name='Blue')
	await ctx.channel.purge(limit=1)
	await ctx.author.add_roles(b)
	await ctx.author.send(f'You have been given the Blue color role!')

#Blue command remove
@client.command()
async def remove_Blue(ctx):
	b = discord.utils.get(ctx.guild.roles, name='Blue')
	await ctx.channel.purge(limit=1)
	await ctx.author.remove_roles(b)
	await ctx.author.send(f'Sucessfully removed the Blue role from you!')

#Red command add
@client.command()
async def add_Red(ctx):
	b = discord.utils.get(ctx.guild.roles, name='Red')
	await ctx.channel.purge(limit=1)
	await ctx.author.add_roles(b)
	await ctx.author.send(f'You have been given the Red color role!')

#Red command remove
@client.command()
async def remove_Red(ctx):
	b = discord.utils.get(ctx.guild.roles, name='Red')
	await ctx.channel.purge(limit=1)
	await ctx.author.remove_roles(b)
	await ctx.author.send(f'Sucessfully removed the Red role from you!')

#Yellow command add
@client.command()
async def add_Yellow(ctx):
  b = discord.utils.get(ctx.guild.roles, name='Yellow')
  await ctx.channel.purge(limit=1)
  await ctx.author.add_roles(b)
  await ctx.author.send(f'You have been given the Yellow color role!')

#Yellow command remove
@client.command()
async def remove_Yellow(ctx):
  b = discord.utils.get(ctx.guild.roles, name='Yellow')
  await ctx.channel.purge(limit=1)
  await ctx.author.remove_roles(b)
  await ctx.author.send(f'Sucessfully removed the Yellow role from you!')

#Black command add
@client.command()
async def add_Black(ctx):
  b = discord.utils.get(ctx.guild.roles, name='Black')
  await ctx.channel.purge(limit=1)
  await ctx.author.add_roles(b)
  await ctx.author.send(f'You have been given the Black color role!')

#Black command remove
@client.command()
async def remove_Black(ctx):
  b = discord.utils.get(ctx.guild.roles, name='Black')
  await ctx.channel.purge(limit=1)
  await ctx.author.remove_roles(b)
  await ctx.author.send(f'Sucessfully removed the Black role from you!')

#Pink command add
@client.command()
async def add_Pink(ctx):
  b = discord.utils.get(ctx.guild.roles, name='Pink')
  await ctx.channel.purge(limit=1)
  await ctx.author.add_roles(b)
  await ctx.author.send(f'You have been given the Pink color role!')

#Pink command remove
@client.command()
async def remove_Pink(ctx):
  b = discord.utils.get(ctx.guild.roles, name='Pink')
  await ctx.channel.purge(limit=1)
  await ctx.author.remove_roles(b)
  await ctx.author.send(f'Sucessfully removed the Pink role from you!')

#Orange command add
@client.command()
async def add_Orange(ctx):
  b = discord.utils.get(ctx.guild.roles, name='Orange')
  await ctx.channel.purge(limit=1)
  await ctx.author.add_roles(b)
  await ctx.author.send(f'You have been given the Orange color role!')

#Orange command remove
@client.command()
async def remove_Orange(ctx):
  b = discord.utils.get(ctx.guild.roles, name='Orange')
  await ctx.channel.purge(limit=1)
  await ctx.author.remove_roles(b)
  await ctx.author.send(f'Sucessfully removed the Orange role from you!')

#Purple command add
@client.command()
async def add_Purple(ctx):
  b = discord.utils.get(ctx.guild.roles, name='Purple')
  await ctx.channel.purge(limit=1)
  await ctx.author.add_roles(b)
  await ctx.author.send(f'You have been given the Purple color role!')

#Purple command remove
@client.command()
async def remove_Purple(ctx):
  b = discord.utils.get(ctx.guild.roles, name='Purple')
  await ctx.channel.purge(limit=1)
  await ctx.author.remove_roles(b)
  await ctx.author.send(f'Sucessfully removed the Purple role from you!')

#Green command add
@client.command()
async def add_Green(ctx):
  b = discord.utils.get(ctx.guild.roles, name='Green')
  await ctx.channel.purge(limit=1)
  await ctx.author.add_roles(b)
  await ctx.author.send(f'You have been given the Green color role!')

#Green command remove
@client.command()
async def remove_Green(ctx):
  b = discord.utils.get(ctx.guild.roles, name='Green')
  await ctx.channel.purge(limit=1)
  await ctx.author.remove_roles(b)
  await ctx.author.send(f'Sucessfully removed the Green role from you!')

#Brown command add
@client.command()
async def add_Brown(ctx):
  b = discord.utils.get(ctx.guild.roles, name='Brown')
  await ctx.channel.purge(limit=1)
  await ctx.author.add_roles(b)
  await ctx.author.send(f'You have been given the Brown color role!')

#Brown command remove
@client.command()
async def remove_Brown(ctx):
  b = discord.utils.get(ctx.guild.roles, name='Brown')
  await ctx.channel.purge(limit=1)
  await ctx.author.remove_roles(b)
  await ctx.author.send(f'Sucessfully removed the Brown role from you!')

#White command add
@client.command()
async def add_White(ctx):
  b = discord.utils.get(ctx.guild.roles, name='White')
  await ctx.channel.purge(limit=1)
  await ctx.author.add_roles(b)
  await ctx.author.send(f'You have been given the White color role!')

#White command remove
@client.command()
async def remove_White(ctx):
  b = discord.utils.get(ctx.guild.roles, name='White')
  await ctx.channel.purge(limit=1)
  await ctx.author.remove_roles(b)
  await ctx.author.send(f'Sucessfully removed the White role from you!')

#auto role
@client.event
async def on_member_join(member):
  notrole=discord.utils.get(member.guild.roles, name='Not Verified')
  await member.add_roles(notrole)

#all the errors

#userinfo error
@userinfo.error
async def userinfo_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):

        em = discord.Embed(title = "Error", description = "Please pass all required arguments", color = discord.Color.red())

        await ctx.send(embed=em, delete_after=5)

client.run(os.environ['DISCORD_TOKEN'])