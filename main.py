"""
An open-source Discord Bot for crypto prices.

Discord: Renax#6191
Instagram: renax.official

"""

#----- LIBS -----#

import discord
from discord.ext import commands
import json
import psutil
import re
import requests
import os
import asyncio
import time

#--------------#

#----- Bot Settings -----#
token = "YOUR-TOKEN"
client = commands.Bot(command_prefix=";", help_command=None)

async def changing_presence():
    while True:
        await client.change_presence(activity=discord.Game(name="Support me on Instagram: @renax.official"))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Game(name="v0.1 | ;help"))
        await asyncio.sleep(10)

@client.event
async def on_ready():
    print("Bot ready: CryptoChecker")
    print("v0.1 | By Renax#0187")
    print("______________________________")
    client.loop.create_task(changing_presence())

#------------------------#

#----- Commands -----#
@client.command()
async def help(ctx, area = None):
    if area is None:
        embed=discord.Embed(title=f"**Help Menu**", color=0x0080c0)
        embed.add_field(name="Prefix: ;", value=" ‎‎‎", inline=False)
        embed.add_field(name=f"**📢Commands**", value=f"```;help cmd```", inline=True) 
        embed.add_field(name=f"**👨‍💻Tech**", value=f"```;help tech```", inline=True)
        embed.set_footer(text="CryptoChecker | 2021")
        await ctx.send(embed=embed)

    if area == "tech":
        await ctx.message.delete()
        embed = discord.Embed(title=f"**👨‍💻Tech Help Menu👨‍💻**", color=0x0080c0)
        embed.add_field(name=f"**🔧 - ;stats**", value="Shows Information about the Host-Server")
        embed.add_field(name=f"**📭 - ;invite**", value="Sends the Invite Link of the bot")
        await ctx.send(embed=embed)

    if area == "cmd":
        await ctx.message.delete()
        embed = discord.Embed(title=f"**📢Commands Help Menu📢**", color=0x0080c0)
        embed.add_field(name=f"**💲 - ;price **", value="Shows the price of Bitcoin")
        embed.add_field(name=f"**💰 - ;donate**", value="Sends a BTC/DOGE Adress where you can support me with a little donation.")
        await ctx.send(embed=embed)

@client.command()
async def price(ctx):
        url = f"https://api.coindesk.com/v1/bpi/currentprice.json"
        r = requests.get(url)
        re = r.json()
        price_usd = re["bpi"]["USD"]["rate"]
        price_eur = re["bpi"]["EUR"]["rate"]
        disclaimer = re["disclaimer"]
        update = re["time"]["updated"]
        embed = discord.Embed(title=f"Price of **Bitcoin**", description=disclaimer, color=0xffff00)
        embed.add_field(name="USD", value=f"** {price_usd} $**")
        embed.add_field(name="EUR", value=f"** {price_eur} €**")
        embed.set_footer(text=f"Updated: {update}")
        await ctx.send(embed=embed)


@client.command()
async def stats(ctx):
    p = psutil.Process(os.getpid())
    p.create_time()
    uptime = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(p.create_time()))
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    server = len(client.guilds)
    embed=discord.Embed(title="Server Info", color=0x061fff)
    embed.set_thumbnail(url="https://www.freeiconspng.com/thumbs/server-icons/virtual-server-icon-7.png")
    embed.add_field(name=f"**🌍Server**", value=f"On ```{server}``` Servers", inline=False)
    embed.add_field(name=f"**💻CPU**", value=str(cpu) + " % used", inline=True)
    embed.add_field(name=f"**💾RAM**", value=str(ram) + " % used", inline=True)
    embed.add_field(name=f"**📡Ping**", value=f"{round(client.latency * 1000)}ms", inline=True)
    embed.add_field(name=f"**⏰Uptime**", value=f"Online since ```{uptime}```")
    embed.set_footer(text="CryptoChecker | 2021")
    await ctx.send(embed=embed)

async def donate(ctx):
    embed=discord.Embed(title="Donate me here", description="You can support me with a little donation.", color=0x05cc00)
    embed.add_field(name="Bitcoin", value="Adress: bc1q39ywxw9avvqrflx3mrz66w7sf36wqaw4q5hqjd9g5s20cpz7sdeqmxpdav", inline=True)
    embed.add_field(name="Dogecoin", value="Adress: D9HkUKKvUNT99jmms1m4htnFdScnqGAzxjv", inline=True)
    await ctx.send(embed=embed)

@client.command()
async def invite(ctx):
        embed=discord.Embed(title="Add to your Server.", url="https://discord.com/api/oauth2/authorize?client_id=831438438775128084&permissions=0&scope=bot", description="Click the button to add the bot to your server", color=0xffff00)
        embed.set_footer(text="CryptoChecker | 2021 ")
        await ctx.channel.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.channel.send(f"Invalid Command. Try using ```;help``` for the Help Menu")



client.run(token)
