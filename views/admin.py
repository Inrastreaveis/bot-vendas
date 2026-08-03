import discord


class PainelAdmin(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)


    @discord.ui.button(
        label="Adicionar Produto",
        emoji="➕",
        style=discord.ButtonStyle.green,
        custom_id="admin_add"
    )
    async def adicionar(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        from cogs.admin import AddProdutoModal

        await interaction.response.send_modal(
            AddProdutoModal()
        )


    @discord.ui.button(
        label="Remover Produto",
        emoji="🗑️",
        style=discord.ButtonStyle.red,
        custom_id="admin_remove"
    )
    async def remover(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            "Em breve...",
            ephemeral=True
        )


    @discord.ui.button(
        label="Listar Produtos",
        emoji="📦",
        style=discord.ButtonStyle.blurple,
        custom_id="admin_listar"
    )
    async def listar(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            "Em breve...",
            ephemeral=True
        )