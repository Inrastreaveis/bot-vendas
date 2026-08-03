import discord

from database.produtos import listar_categoria
from database.kits import listar_categoria as listar_kits_categoria

from views.produtos import ProdutoView
from views.kits import KitView


class CategoriaSelect(discord.ui.Select):

    def __init__(self):

        options = [

            discord.SelectOption(
                label="Oculos",
                description="Ver todos os Oculos",
                emoji="🕶️"
            ),

            discord.SelectOption(
                label="Bonés",
                description="Ver todos os Bonés",
                emoji="🧢"
            ),

            discord.SelectOption(
                label="Tocas",
                description="Ver todas as Tocas",
                emoji="🥷"
            ),

            discord.SelectOption(
                label="Chapéus",
                description="Ver todos os Chapéus",
                emoji="👑"
            ),

            discord.SelectOption(
                label="Máscaras",
                description="Ver todas as Máscaras",
                emoji="🎭"
            ),

            discord.SelectOption(
                label="Kits",
                description="Kits DJ Arana",
                emoji="🎧"
            )

        ]

        super().__init__(
            placeholder="Escolha uma categoria...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        categoria = self.values[0]

        # =========================
        # KITS
        # =========================

        if categoria == "Kits":

            kits = await listar_kits_categoria("Kits")

            if len(kits) == 0:

                await interaction.response.send_message(
                    "❌ Nenhum kit cadastrado.",
                    ephemeral=True
                )

                return

            embed = discord.Embed(
                title="🎧 Kits DJ Arana",
                description="Escolha um kit no menu abaixo.",
                color=discord.Color.green()
            )

            await interaction.response.send_message(
                embed=embed,
                view=KitView(kits),
                ephemeral=True
            )

            return

        # =========================
        # PRODUTOS
        # =========================

        produtos = await listar_categoria(categoria)

        if len(produtos) == 0:

            await interaction.response.send_message(
                "❌ Nenhum produto cadastrado.",
                ephemeral=True
            )

            return

        embed = discord.Embed(
            title=f"📦 {categoria}",
            description="Escolha um produto no menu abaixo.",
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            view=ProdutoView(produtos),
            ephemeral=True
        )


class CategoriaView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CategoriaSelect())