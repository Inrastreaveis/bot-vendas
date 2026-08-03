import aiosqlite
from .database import conectar


async def adicionar_kit(
    nome,
    categoria,
    look_id,
    preco,
    descricao,
    imagem,
    link
):
    async with conectar() as db:

        await db.execute(
            """
            INSERT INTO kits
            (
                nome,
                categoria,
                look_id,
                preco,
                descricao,
                imagem,
                link
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                nome,
                categoria,
                look_id,
                preco,
                descricao,
                imagem,
                link
            )
        )

        await db.commit()


async def listar_categoria(categoria):

    async with conectar() as db:

        cursor = await db.execute(
            """
            SELECT
                id,
                nome,
                categoria,
                look_id,
                preco,
                descricao,
                imagem,
                link
            FROM kits
            WHERE categoria = ?
            ORDER BY nome
            """,
            (categoria,)
        )

        return await cursor.fetchall()


async def listar_todos():

    async with conectar() as db:

        cursor = await db.execute(
            """
            SELECT
                id,
                nome,
                categoria,
                look_id,
                preco,
                descricao,
                imagem,
                link
            FROM kits
            ORDER BY nome
            """
        )

        return await cursor.fetchall()


async def remover_kit(look_id):

    async with conectar() as db:

        cursor = await db.execute(
            """
            DELETE FROM kits
            WHERE look_id = ?
            """,
            (look_id,)
        )

        await db.commit()

        return cursor.rowcount > 0
