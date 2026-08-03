import aiosqlite
from .database import DATABASE, preparar_banco


async def adicionar_produto(
    asset_id,
    nome,
    categoria,
    preco,
    criador,
    descricao,
    imagem,
    link
):
    preparar_banco()
    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            INSERT INTO produtos
(
    asset_id,
    nome,
    categoria,
    preco,
    criador,
    descricao,
    imagem,
    link
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(asset_id) DO UPDATE SET
nome=excluded.nome,
categoria=excluded.categoria,
preco=excluded.preco,
criador=excluded.criador,
descricao=excluded.descricao,
imagem=excluded.imagem,
link=excluded.link

            """,
            (
                asset_id,
                nome,
                categoria,
                preco,
                criador,
                descricao,
                imagem,
                link,
            ),
        )

        await db.commit()


async def listar_categoria(categoria):

    preparar_banco()
    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            "SELECT * FROM produtos WHERE categoria = ?",
            (categoria,)
        )

        return await cursor.fetchall()


async def remover_produto(asset_id: int):

    preparar_banco()
    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            "DELETE FROM produtos WHERE asset_id = ?",
            (asset_id,)
        )

        await db.commit()


async def listar_produtos():
    preparar_banco()
    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
            SELECT asset_id, nome, categoria
            FROM produtos
            ORDER BY categoria, nome
        """)

        return await cursor.fetchall()