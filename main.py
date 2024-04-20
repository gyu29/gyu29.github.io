import discord
from discord.ext import commands
import random
import time
from discord import app_commands
import traceback
import json
import datetime
from discord import app_commands
from keep_alive import keep_alive

keep_alive()

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

BOOST_CHANNEL_ID = 1230861934526595092
boost_role_id = 1230863985453043743
BLACKLISTED_ROLES = ["Staff", "Admin", "Dulltive", "Creators"]
STAFF_CHANNEL_ID = 1230001582180139089
CHANNEL_TO_MODERATE_ID = 1228202556828946443

@bot.event
async def on_ready():
  print('Logged in as {0.user}'.format(bot))
  await bot.change_presence(activity=discord.Activity(
      type=discord.ActivityType.playing, name="Minecraft"))
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands")
  except Exception as e:
    print(e)

@bot.event
async def on_message(message):
    if message.channel.id == CHANNEL_TO_MODERATE_ID:
        has_whitelisted_role = any(role.name in BLACKLISTED_ROLES for role in message.author.roles)
        if any(word.startswith('http://') or word.startswith('https://') or word.startswith('discord.gg') or word.endswith('.gg') or word.endswith('.com') or word.endswith('.shop') for word in message.content.split()):
            staff_channel = bot.get_channel(STAFF_CHANNEL_ID)
            await staff_channel.send(f"{message.author.mention} sent a link in {message.channel.mention}:\n{message.content}")
            if not has_whitelisted_role:
                await message.delete()
                await staff_channel.send(f"{message.author.mention}'s message has been deleted")
    
@bot.tree.command(name='rules', description="Shows the rules of this server.")
@app_commands.checks.has_permissions(administrator=True)
async def rules(interaction: discord.Interaction):
    current_time = datetime.datetime.now()
    embed = discord.Embed(title="Rules", description="""
[1]: You MUST follow Discord's Terms of Service at all times within this server.
[2]: Use common sense
[3]: Spamming, spam pinging, or sending multiple messages that hold 90%+ similarity in any way, is prohibited.
[4]: Offensive slurs are prohibited if directed towards someone.
[5]: Racial slurs are prohibited.
[6]: Verbally attacking, accosting, or harassing other members is prohibited.
[7]: If a member of the discord is involved in, threatened by, or could potentially be involved in a situation that is violent in any way (self-harm or harm to others), this includes suicide, child abuse, violence, or murder, ALL GROUP MEMBERS are responsible for immediately reporting it and the person shall face immediate ban.
[8]: Ban evasion is strictly prohibited. If you are caught ban evading, you will permanently be banned from our server on all accounts. Mute evasion will result in a temporary ban.
[9]: HARASSING or THREATENING other members, even in DMs, is prohibited. This includes hate speech, bullying and sexual connotations.
[10]: English is to be spoken in this server at all times.
[11]: Do not advertise your server or products here. Breaking any of these rules can and will potentially result in a ban or a blacklist, or both.
""", color=discord.Color.red(), timestamp=current_time)
    await interaction.response.send_message(embed=embed)

@bot.event
async def guild_boost(guild, member):
  channel = bot.get_channel(BOOST_CHANNEL_ID)
  await channel.send(f"Thank you for boosting **{guild.name}**! Your support is greatly appreciated.")
  boost_role = member.guild.get_role(boost_role_id)
  await member.add_roles(boost_role)
  print(f'{member.name} has boosted the server')
  
bot.run('MTIzMDg2NDI1ODU2OTYwNTEzMA.GhC_mj.XHB8MaFsv3TMyK_CPBeKTs_wgtzFAw1sufSkLk')
