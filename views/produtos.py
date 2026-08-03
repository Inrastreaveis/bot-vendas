import discord
import aiohttp


class ProdutoSelect(discord.ui.Select):
    def __init__(self, produtos):
        self.produtos = produtos

        options = [
            discord.SelectOption(
                label=produto[2],
                description=f"{produto[4]} Robux",
                value=str(produto[1])
            )
            for produto in produtos
        ]

        super().__init__(
            placeholder="Escolha um produto...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        asset_id = int(self.values[0])

        produto = next(
            (p for p in self.produtos if p[1] == asset_id),
            None
        )

        if produto is None:
            await interaction.response.send_message(
                "Produto não encontrado.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="📦 Produto",
            color=discord.Color.green()
        )

        embed.add_field(
            name="📦 Nome",
            value=produto[2],
            inline=False
        )

        embed.add_field(
            name="💰 Preço",
            value=f"{produto[4]} Robux",
            inline=True
        )

        embed.add_field(
            name="👤 Criador",
            value=produto[5] or "Desconhecido",
            inline=True
        )
        embed.add_field(
    name="🆔 Asset ID",
    value=str(asset_id),
    inline=False
)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://thumbnails.roblox.com/v1/assets?assetIds={asset_id}&size=420x420&format=Png"
                ) as resp:

                    if resp.status == 200:
                        data = await resp.json()

                        if data["data"]:
                            embed.set_image(
                                url=data["data"][0]["imageUrl"]
                            )
        except Exception as e:
            print("Erro ao carregar thumbnail:", e)

        view = discord.ui.View(timeout=None)

        if produto[8]:
            view.add_item(
                discord.ui.Button(
                    label="🛒 Comprar Agora",
                    style=discord.ButtonStyle.link,
                    url=produto[8]
                )
            )

        view.add_item(VoltarCategoria())

        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True
        )


class VoltarCategoria(discord.ui.Button):

    def __init__(self):
        super().__init__(
            label="⬅️ Voltar categorias",
            style=discord.ButtonStyle.secondary,
            custom_id="voltar_categoria"
        )

    async def callback(self, interaction: discord.Interaction):
        from views.categorias import CategoriaView

        embed = discord.Embed(
            title="🛍️ Loja",
            description="Escolha uma categoria.",
            color=0x5865F2
        )

        await interaction.response.edit_message(
            embed=embed,
            view=CategoriaView()
        )


class ProdutoView(discord.ui.View):
    def __init__(self, produtos):
        super().__init__(timeout=180)
        self.add_item(ProdutoSelect(produtos))