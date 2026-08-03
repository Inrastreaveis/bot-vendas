import discord
from views.produtos import VoltarCategoria


class KitSelect(discord.ui.Select):

    def __init__(self, kits):

        self.kits = kits

        options = []

        for kit in kits:
            options.append(
                discord.SelectOption(
                    label=kit[1],                  # nome
                    description=f"{kit[4]} Robux", # preço
                    value=str(kit[3])             # look_id
                )
            )

        super().__init__(
            placeholder="Escolha um Kit...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        look_id = int(self.values[0])

        kit = next(
            (k for k in self.kits if k[3] == look_id),
            None
        )

        if kit is None:
            await interaction.response.send_message(
                "❌ Kit não encontrado.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="🎧 Kit",
            color=discord.Color.green()
        )

        embed.add_field(
            name="🎧 Nome",
            value=kit[1],
            inline=False
        )

        embed.add_field(
            name="💰 Preço",
            value=f"{kit[4]} Robux",
            inline=False
        )

        if kit[6]:
            embed.set_image(url=kit[6])

        embed.set_footer(
            text="Company Store"
        )

        view = discord.ui.View(timeout=None)

        if kit[7]:
            view.add_item(
                discord.ui.Button(
                    label="🛒 Comprar",
                    style=discord.ButtonStyle.link,
                    url=kit[7]
                )
            )

        view.add_item(VoltarCategoria())

        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True
        )


class KitView(discord.ui.View):

    def __init__(self, kits):
        super().__init__(timeout=180)
        self.add_item(KitSelect(kits))