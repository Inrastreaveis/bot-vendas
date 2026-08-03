import os
import shutil
from pathlib import Path

import aiosqlite

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUNDLED_DATABASE = PROJECT_ROOT / "database.db"
DATABASE = Path(os.getenv("DB_PATH", str(BUNDLED_DATABASE)))


def preparar_banco():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    if DATABASE != BUNDLED_DATABASE and not DATABASE.exists() and BUNDLED_DATABASE.exists():
        shutil.copy2(BUNDLED_DATABASE, DATABASE)


def conectar():
    preparar_banco()
    return aiosqlite.connect(DATABASE)


async def criar_tabelas():
    preparar_banco()
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER UNIQUE,
            nome TEXT,
            categoria TEXT,
            preco INTEGER,
            criador TEXT,
            descricao TEXT,
            imagem TEXT,
            link TEXT
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS kits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            look_id INTEGER UNIQUE NOT NULL,
            preco INTEGER NOT NULL,
            descricao TEXT,
            imagem TEXT,
            link TEXT
        )
        """)

        await db.commit()
