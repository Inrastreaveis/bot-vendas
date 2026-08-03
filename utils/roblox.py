import aiohttp

print("ROBLOX UTILS CARREGADO")


async def buscar_produto(asset_id: int):
    url = f"https://apis.roblox.com/marketplace-items/v1/items/details?itemIds={asset_id}&itemType=Asset"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:

            print("STATUS:", resp.status)

            if resp.status != 200:
                print(await resp.text())
                return None

            data = await resp.json()
            print(data)

            if not data.get("data"):
                return None

            item = data["data"][0]

            return {
                "asset_id": asset_id,
                "nome": item.get("name", "Sem nome"),
                "criador": item.get("creatorName", "Desconhecido"),
                "descricao": item.get("description", ""),
                "imagem": f"https://thumbnails.roblox.com/v1/assets?assetIds={asset_id}&size=420x420&format=Png",
                "link": f"https://www.roblox.com/catalog/{asset_id}"
            }


async def buscar_kit(look_id: int):
    return {
        "look_id": look_id,
        "nome": "Teste",
        "descricao": "",
        "imagem": None,
        "link": f"https://www.roblox.com/pt/looks/{look_id}"
    }