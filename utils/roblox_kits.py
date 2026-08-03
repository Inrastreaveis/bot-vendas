import aiohttp


async def buscar_kit(look_id: int):

    url = f"https://avatar.roblox.com/v1/outfits/{look_id}/details"

    async with aiohttp.ClientSession() as session:

        async with session.get(url) as resp:

            if resp.status != 200:
                return None

            data = await resp.json()

    imagem = (
        f"https://thumbnails.roblox.com/v1/users/avatar"
    )

    return {
        "look_id": look_id,
        "nome": data.get("name", "Sem nome"),
        "descricao": data.get("description", ""),
        "imagem": None,
        "link": f"https://www.roblox.com/pt/looks/{look_id}"
    }