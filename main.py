import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import database.database as db

print(db.__file__)
print(dir(db))

from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Variável TOKEN não configurada.")


intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print("=" * 50)
    print(f"Bot conectado como {bot.user}")
    print(f"ID: {bot.user.id}")

    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} Slash Commands sincronizados.")

        print("Comandos registrados:")
        for cmd in bot.tree.get_commands():
            print("-", cmd.name)

    except Exception as e:
        print(e)

    print("=" * 50)


async def load_cogs():
    for arquivo in os.listdir("./cogs"):
        if arquivo.endswith(".py"):
            print(f"Carregando: cogs.{arquivo[:-3]}")
            await bot.load_extension(f"cogs.{arquivo[:-3]}")
            print(f"✔ {arquivo} carregado")


async def main():
    async with bot:

        await db.criar_tabelas()      # <- Aqui

        await load_cogs()
        await bot.start(TOKEN)


import asyncio
asyncio.run(main())