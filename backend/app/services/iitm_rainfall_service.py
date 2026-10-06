import time
import json
import httpx


IITM_BASE_URL = (
    "https://mumbairain.tropmet.res.in/json/map_file"
)


async def get_iitm_rainfall(period: str):
    endpoint_map = {
        "15min": ("read_map_15.php", 15),
        "1hr": ("read_map_1.php", 1),
        "3hr": ("read_map_3.php", 3),
    }

    if period not in endpoint_map:
        raise ValueError(
            "Invalid rainfall period"
        )

    endpoint, type_value = endpoint_map[period]

    url = f"{IITM_BASE_URL}/{endpoint}"

    params = {
        "type": type_value,
        "_": int(time.time() * 1000)
    }

    async with httpx.AsyncClient(
        verify=False
    ) as client:

        response = await client.get(
            url,
            params=params,
            timeout=20.0
        )

        response.raise_for_status()


        import json

        json_start = response.text.find("[")

        if json_start == -1:
            raise ValueError(
                "IITM response does not contain JSON data"
            )

        json_text = response.text[json_start:]

        return json.loads(json_text)


if __name__ == "__main__":
    import asyncio

    async def test():
        for period in ["15min", "1hr", "3hr"]:
            try:
                data = await get_iitm_rainfall(period)

                print(
                    f"{period}: {len(data)} stations"
                )

                print(
                    "First station:",
                    data[0]
                )

            except Exception as e:
                print(
                    f"{period}: ERROR -> {e}"
                )

    asyncio.run(test())