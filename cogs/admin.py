import discord
from discord.ext import commands
from discord import app_commands


from database.produtos import (
    adicionar_produto,
    remover_produto,
    listar_produtos
)

from database.kits import (
    adicionar_kit,
    remover_kit
)
ADMIN_ROLE_ID = 1529288668403990599
def eh_admin(interaction: discord.Interaction) -> bool:
    """Verifica se o usuário tem permissões administrativas ou o role definido."""
    try:
        member = interaction.user
        if not isinstance(member, discord.Member):
            return False

        if member.guild_permissions.administrator:
            return True

        return any(role.id == ADMIN_ROLE_ID for role in member.roles)
    except Exception:
        return False
class AddProdutoModal(discord.ui.Modal, title="Adicionar Produto"):

    asset_id = discord.ui.TextInput(
        label="🆔 Asset ID",
        placeholder="123456789",
        required=True
    )

    nome = discord.ui.TextInput(
        label="📝 Nome",
        placeholder="Nome do produto",
        required=True
    )

    categoria = discord.ui.TextInput(
        label="📂 Categoria",
        placeholder="Julietes",
        required=True
    )

    preco = discord.ui.TextInput(
        label="💰 Preço",
        placeholder="250",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        try:
            asset_id = int(self.asset_id.value)
            preco = int(self.preco.value)

        except ValueError:
            await interaction.followup.send(
                "❌ Asset ID ou preço inválido.",
                ephemeral=True
            )
            return

        imagem = (
            f"https://thumbnails.roblox.com/v1/assets"
            f"?assetIds={asset_id}&size=420x420&format=Png"
        )

        link = f"https://www.roblox.com/catalog/{asset_id}"

        try:

            await adicionar_produto(
                asset_id=asset_id,
                nome=self.nome.value,
                categoria=self.categoria.value,
                preco=preco,
                criador="",
                descricao="",
                imagem=imagem,
                link=link
            )

        except Exception as e:

            await interaction.followup.send(
                f"```{e}```",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="✅ Produto adicionado",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Produto",
            value=self.nome.value,
            inline=False
        )

        embed.add_field(
            name="Preço",
            value=f"{preco} Robux",
            inline=False
        )

        embed.add_field(
            name="Asset ID",
            value=str(asset_id),
            inline=False
        )

        embed.set_image(url=imagem)

        await interaction.followup.send(
            embed=embed,
            ephemeral=True
        )


class AddKitModal(discord.ui.Modal, title="Adicionar Kit"):

    nome = discord.ui.TextInput(
        label="🎧 Nome do Kit",
        placeholder="DJ Arana Red",
        required=True
    )

    preco = discord.ui.TextInput(
        label="💰 Preço",
        placeholder="250",
        required=True
    )

    link = discord.ui.TextInput(
        label="🔗 Link do Roblox",
        placeholder="https://www.roblox.com/pt/looks/123456789",
        required=True
    )

    imagem = discord.ui.TextInput(
        label="🖼️ URL da Imagem",
        placeholder="https://...",
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):

        print("1 - Entrou no modal")

        await interaction.response.defer(ephemeral=True)

        print("2 - Defer OK")

        try:
            look_id = int(
                self.link.value.split("/looks/")[1].split("/")[0]
            )

            print("3 - Look ID:", look_id)

        except Exception as e:
            print("ERRO NO LINK:", e)

            await interaction.followup.send(
                "❌ Link do Roblox inválido.",
                ephemeral=True
            )
            return

        print("4 - Antes de adicionar")

        try:
            await adicionar_kit(
                nome=self.nome.value,
                categoria="Kits",
                look_id=look_id,
                preco=int(self.preco.value),
                descricao="",
                imagem=self.imagem.value,
                link=self.link.value
            )

            print("5 - Kit salvo")

        except Exception as e:
            print("ERRO AO SALVAR KIT:")
            print(repr(e))

            await interaction.followup.send(
                f"Erro ao salvar o kit:\n```{e}```",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="✅ Kit adicionado",
            color=discord.Color.green()
        )

        embed.add_field(
            name="🎧 Nome",
            value=self.nome.value,
            inline=False
        )

        embed.add_field(
            name="💰 Preço",
            value=f"{self.preco.value} Robux",
            inline=False
        )

        if self.imagem.value and self.imagem.value.strip():
            embed.set_image(url=self.imagem.value.strip())

        await interaction.followup.send(
            embed=embed,
            ephemeral=True
        )


class RemoverKitModal(discord.ui.Modal, title="Remover Kit"):

    look_id = discord.ui.TextInput(
        label="🆔 Look ID",
        placeholder="123456789",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        try:
            look_id = int(self.look_id.value)

        except ValueError:
            await interaction.followup.send(
                "❌ Look ID inválido.",
                ephemeral=True
            )
            return

        await remover_kit(look_id)

        embed = discord.Embed(
            title="✅ Kit removido",
            description=f"Look ID **{look_id}** removido da loja.",
            color=discord.Color.red()
        )

        await interaction.followup.send(
            embed=embed,
            ephemeral=True
        )


class PainelAdmin(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    async def interaction_check(self, interaction: discord.Interaction):

        if not eh_admin(interaction):
            await interaction.response.send_message(
                "❌ Você não tem permissão para usar este painel.",
                ephemeral=True
            )
            return False

        return True

    @discord.ui.button(
        label="➕ Adicionar Produto",
        style=discord.ButtonStyle.green
    )
    async def adicionar_produto(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_modal(AddProdutoModal())

    @discord.ui.button(
        label="🎧 Adicionar Kit",
        style=discord.ButtonStyle.blurple
    )
    async def adicionar_kit(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_modal(AddKitModal())

    @discord.ui.button(
        label="🗑️ Remover Kit",
        style=discord.ButtonStyle.red
    )
    async def remover_kit(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_modal(RemoverKitModal())

    @discord.ui.button(
        label="📦 Listar Produtos",
        style=discord.ButtonStyle.gray
    )
    async def listar(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        produtos = await listar_produtos()

        if not produtos:
            await interaction.response.send_message(
                "Nenhum produto cadastrado.",
                ephemeral=True
            )
            return

        texto = ""

        for asset_id, nome, categoria in produtos:
            texto += (
                f"**{nome}**\n"
                f"🆔 `{asset_id}`\n"
                f"📂 {categoria}\n\n"
            )

        embed = discord.Embed(
            title="📦 Produtos cadastrados",
            description=texto,
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="painel", description="Abre o painel administrativo.")
    async def painel(self, interaction: discord.Interaction):

        if not eh_admin(interaction):
            await interaction.response.send_message(
                "❌ Você não tem permissão para usar este comando.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="🛠️ Painel Administrativo",
            description="Escolha uma opção abaixo.",
            color=discord.Color.blue()
        )

        await interaction.response.send_message(
            embed=embed,
            view=PainelAdmin(),
            ephemeral=True
        )

    @app_commands.command(
        name="addproduto",
        description="Adicionar um produto."
    )
    async def addproduto(self, interaction: discord.Interaction):

        if not eh_admin(interaction):
            await interaction.response.send_message(
                "❌ Você não tem permissão.",
                ephemeral=True
            )
            return

        await interaction.response.send_modal(AddProdutoModal())

    @app_commands.command(
        name="removerproduto",
        description="Remover um produto."
    )
    @app_commands.describe(asset_id="Asset ID do produto")
    async def removerproduto(
        self,
        interaction: discord.Interaction,
        asset_id: int
    ):

        if not eh_admin(interaction):
            await interaction.response.send_message(
                "❌ Você não tem permissão.",
                ephemeral=True
            )
            return

        await remover_produto(asset_id)

        await interaction.response.send_message(
            f"✅ Produto `{asset_id}` removido.",
            ephemeral=True
        )

    @app_commands.command(
        name="removerkit",
        description="Remover um kit."
    )
    async def removerkit(self, interaction: discord.Interaction):

        if not eh_admin(interaction):
            await interaction.response.send_message(
                "❌ Você não tem permissão.",
                ephemeral=True
            )
            return

        await interaction.response.send_modal(RemoverKitModal())

    @app_commands.command(
        name="listarprodutos",
        description="Lista todos os produtos."
    )
    async def listarprodutos(self, interaction: discord.Interaction):

        if not eh_admin(interaction):
            await interaction.response.send_message(
                "❌ Você não tem permissão.",
                ephemeral=True
            )
            return

        produtos = await listar_produtos()

        if not produtos:
            await interaction.response.send_message(
                "Nenhum produto cadastrado.",
                ephemeral=True
            )
            return

        texto = ""

        for asset_id, nome, categoria in produtos:
            texto += (
                f"**{nome}**\n"
                f"🆔 `{asset_id}`\n"
                f"📂 {categoria}\n\n"
            )

        embed = discord.Embed(
            title="📦 Produtos",
            description=texto,
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Admin(bot))