import discord
from discord.ext import commands, tasks
import os
from random import choice
import aiohttp
from random import randint
import wikipedia
import time
import datetime
import asyncio
import random
import typing

intents = discord.Intents.all()
prefixes = [";"]
client = commands.Bot(command_prefix=prefixes, intents=intents)

status = ['Listening to ;help', 'Make sure to read the rules!']

client.remove_command("help")

#ready
@client.event
async def on_ready():
    change_status.start()
    print('Bot is ready.')

#status
@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))

#ping command
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

#welcome message
@client.event
async def on_member_join:

#clear command
@client.command(aliases=["cls", "purge"])
@commands.has_permissions(manage_messages=True, administrator=True)
async def clear(ctx, ammount: int):
    await ctx.channel.purge(limit=ammount + 1)
    await ctx.send(f'I have deleted {ammount} of messages', delete_after=5)
    return

#8ball command
@client.command(aliases=['8ball'])
async def _8ball(ctx, question):
    import random
    responses = [
        "It is certain.",
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
        "Very doubtful.",]
    await ctx.send(f'{random.choice(responses)}')

#verify command
@client.command()
@commands.has_role("Not verified")
async def verify(ctx):
  verifiedrole = discord.utils.get(ctx.guild.roles, name='Verified')
  await ctx.author.add_roles(verifiedrole)
  verify = discord.Embed(title="Verification",description="Congrats! You have been verified!", color=ctx.author.color)
  await ctx.send(embed=verify)
  await ctx.author.send(embed=verify)
  u = discord.utils.get(ctx.guild.roles, name='Not verified')
  await ctx.author.remove_roles(u)

#auto role
@client.command
async def test(member):
  notrole=discord.utils.get(member.guild.roles, name='Not verified')
  await member.add_roles(notrole)
  em = discord.Embed(title="Welcome  To 𝓢𝓭॥乛|SoundDute|•|™", color=discord.Color.blue())
  em.add_field(name="◆━━━━━━━━━◆❃◆━━━━━━━━━◆", value=f"Hello, {member}", inline=False)
  em.add_field(name="◆━━━━━━━━━◆❃◆━━━━━━━━━◆", value=f"◈  WELCOME TO OUR SEVER", inline=False)
  em.add_field(name="◆━━━━━━━━━◆❃◆━━━━━━━━━◆", value=f"◈  READ THE SEVER RULES IN #📜〡𝖱ules", inline=False)
  em.add_field(name="◆━━━━━━━━━◆❃◆━━━━━━━━━◆", value=f"◈  TAKE YOUR ROLES IN #🔰〡𝖲elf-𝖱oles", inline=False)
  em.add_field(name="◆━━━━━━━━━◆❃◆━━━━━━━━━◆", value=f"◈ Choose Your Favorite Colour In  #🎨〡𝖢olour-𝖱oles", inline=False)
  em.add_field(name="◆━━━━━━━━━◆❃◆━━━━━━━━━◆", value=f"◈ Always Check #📣〡𝖠nnouncements", inline=False)
  em.add_field(name="◆━━━━━━━━━◆❃◆━━━━━━━━━◆", value=f"◈  BE ACTIVE IN #🗨️〡𝖦eneral-𝖢hat\n◆━━━━━━━━━◆❃◆━━━━━━━━━◆", inline=False)
  em.set_thumbnail(url=member.avatar_url)
  chl = client.get_channel(786589900609945674)
  await chl.send(embed=em)

#verify error
@verify.error
async def verify_error(ctx, error):
    em=discord.Embed(title="Error", description="You are already verified!", color=discord.Color.red())
    await ctx.send(embed=em, delete_after=5)

#help command
@client.command(aliases=['h'])
async def help(ctx):
    helpEmbed = discord.Embed(tittle="Help Menu", color=ctx.author.color)
    helpEmbed.set_author(name="Help Menu:\nPrefix = ';'")
    helpEmbed.add_field(name="Moderation Command Menu", value="```Type ;modHelp to open that```", inline=True)
    helpEmbed.add_field(name="Miscellaneous Command Menu", value="```Type ;miscHelp to open that```", inline=True)
    helpEmbed.set_image(url="https://media.giphy.com/media/f7k6TfAFkiAqKVcJGH/giphy.gif")

    await ctx.send(embed=helpEmbed)

#modHelp
@client.command()
async def modHelp(ctx):
    mod = discord.Embed(tittle="mod", color=ctx.author.color)

    mod.add_field(name="Moderation Command Menu", value="```;clear (ammount) : Deletes the specified ammount of messages from the channel```\n```;ban (user) (reasion) : Bans the specified user from the server```\n```;kick (user) (reason) : Kicks the specified user from the server```\n```;mute (user) (time) (reason) : Mutes the specified user from the server```\n```;unmute (user) : Unmutes the specified user```\n```;unban (user) : Unbans a banned user from the server```\n")

    mod.set_footer(text="More moderation commands will be added soon")

    await ctx.send(embed=mod)


#miscHelp
@client.command()
async def miscHelp(ctx):
    misc = discord.Embed(tittle="misc", color=ctx.author.color)

    misc.add_field(name="Miscellaneous Command Menu", value="```;ping : Tells the bot's latency```\n```;8ball (question) : Tells the answer of the asked question in a random yes/no answer```\n```;meme : Send a hot meme from reddit```\n```;define (querry) : Sends a definition of your querry from wikipedia```\n")

    misc.set_footer(text="More miscellaneous commands will be added soon")

    await ctx.send(embed=misc)

#meme command
@client.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(
                'https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed = discord.Embed(title="Memes", color=discord.Color.orange())
            embed.set_image(url=res['data']['children'][random.randint(0, 25)]
                            ['data']['url'])
            await ctx.send(embed=embed)

#define command
@client.command()
async def define(ctx,*, ask):
    definition = wikipedia.summary(ask, sentences=3, chars=1000, auto_suggest=False, redirect=True)
    search = discord.Embed(color=ctx.author.color)
    search.add_field(name=ask, value=definition, inline=False)
    await ctx.send(embed=search)

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

#unban command
@client.command(aliases=['ub'])
@commands.has_permissions(ban_members=True, administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name,member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
            return

    await ctx.send(member+" was not found")

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

#run event
client.run(os.environ['DISCORD_TOKEN'])
