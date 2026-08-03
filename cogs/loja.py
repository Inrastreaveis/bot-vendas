from discord.ext import commands
from discord import app_commands
from views.categorias import CategoriaView
import discord

from views.categorias import CategoriaView


class Loja(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="loja",
        description="Abrir a Company Store"
    )
    async def loja(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🛍️ Company Store",
            description=(
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "**Bem-vindo à Company Store!**\n\n"
                "Escolha uma categoria no menu abaixo.\n\n"
                "🕶️ Julietes\n"
                "🧢 Bonés\n"
                "🥷 Tocas\n"
                "👑 Chapéus\n"
                "🎭 Máscaras\n"
                "🎧 Kits DJ Arana\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━"
            ),
            color=0x5865F2
        )
        embed.set_footer(text="Company Store • Roblox")
        await interaction.response.send_message(embed=embed, view=CategoriaView())


async def setup(bot):
    await bot.add_cog(Loja(bot))