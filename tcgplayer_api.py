import requests
import json

def as_currency(amount):
    if amount >= 0:
        return '${:,.2f}'.format(amount)
    else:
        return '-${:,.2f}'.format(-amount)

def price(data: str):
    """
    <quantity> <set-code-cardnumber> <card_name>
    Example: "2 OP01-001 Luffy"
    """

    data_split = data.split(" ")
    if len(data_split) < 3:
        return -1, "Invalid input format (expected: quantity set-code-cardnumber card_name)"
    quantity = data_split[0]

    try:
        set_part = data_split[1]
        setdata = set_part.split("-")[0]
        number = set_part.split("-")[1]

    except IndexError:
        return -1, "Invalid set-cardnumber format"

    card_name = data_split[2]

    match setdata:
        case "OP01":
            set_name = "romance-dawn"
        case "OP02":
            set_name = "paramount-war"
        case "OP03":
            set_name = "pillars-of-strength"
        case "OP04":
            set_name = "kingdoms-of-intrigue"
        case "OP05":
            set_name = "awakening-of-the-new-era"
        case "OP06":
            set_name = "wings-of-the-captain"
        case "OP07":
            set_name = "500-years-in-the-future"
        case "OP08":
            set_name = "two-legends"
        case "OP09":
            set_name = "emperors-in-the-new-world"
        case "OP10":
            set_name = "royal-blood"
        case "OP11":
            set_name = "a-fist-of-divine-speed"
        case "EB01":
            set_name = "extra-booster-memorial-collection"
        case "EB02":
            set_name = "premium-booster-the-best"
        case "ST01":
            set_name = "starter-deck-1-straw-hat-crew"
        case "ST02":
            set_name = "starter-deck-2-worst-generation"
        case "ST03":
            set_name = "starter-deck-3-the-seven-warlords-of-the-sea"
        case "ST04":
            set_name = "starter-deck-4-animal-kingdom-pirates"
        case "ST05":
            set_name = "starter-deck-5-film-edition"
        case "ST06":
            set_name = "starter-deck-6-absolute-justice"
        case "ST07":
            set_name = "starter-deck-7-big-mom-pirates"
        case "ST08":
            set_name = "starter-deck-8-monkeydluffy"
        case "ST09":
            set_name = "starter-deck-9-yamato"
        case "ST10":
            set_name = "ultra-deck-the-three-captains"
        case "ST11":
            set_name = "starter-deck-11-uta"
        case "ST12":
            set_name = "starter-deck-12-zoro-and-sanji"
        case "ST13":
            set_name = "ultra-deck-the-three-brothers"
        case "ST14":
            set_name = "starter-deck-14-3d2y"
        case "ST15":
            set_name = "starter-deck-15-red-edwardnewgate"
        case "ST16":
            set_name = "starter-deck-16-green-uta"
        case "ST17":
            set_name = "starter-deck-17-blue-donquixote-doflamingo"
        case "ST18":
            set_name = "starter-deck-18-purple-monkeydluffy"
        case "ST19":
            set_name = "starter-deck-19-black-smoker"
        case "ST20":
            set_name = "starter-deck-20-yellow-charlotte-katakuri"
        case "ST21":
            set_name = "starter-deck-ex-gear-5"
        case _:
            print(f"[Bug] No hard coded set name for \"{setdata}\"")
            set_name = ""

    url = f"https://mp-search-api.tcgplayer.com/v1/search/request?isList=false&q={card_name}"
    payload = json.dumps({
        "algorithm": "sales_dismax",
        "from": 0,
        "size": 24,
        "filters": {
            "term": {
                "productLineName": [
                    "one-piece-card-game"
                ],
                "setName": [
                    f"{set_name}"
                ],
                "productTypeName": [
                    "Cards"
                ]
            },
            "range": {},
            "match": {}
        },
        "listingSearch": {
            "context": {
                "cart": {}
            },
            "filters": {
                "term": {
                    "sellerStatus": "Live",
                    "channelId": 0
                },
                "range": {
                    "quantity": {
                        "gte": 1
                    }
                },
                "exclude": {
                    "channelExclusion": 0
                }
            }
        },
        "context": {
            "cart": {},
            "shippingCountry": "US",
            "userProfile": {}
        },
        "settings": {
            "useFuzzySearch": True,
            "didYouMean": {}
        },
        "sort": {}
    })
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, headers=headers, data=payload).json()

    except Exception as e:
        return -1, f"Request error: {e}"

    if response["results"][0]["results"]:
        market_price = -1

        for result in response["results"][0]["results"]:
            found_card = result["customAttributes"]["number"]
            found_card_name = result["productName"]

            if "Parallel" in found_card_name or "Alternate Art" in found_card_name or "Manga" in found_card_name:
                continue

            if found_card == data_split[1]:
                try:
                    market_price = float(result["marketPrice"]) * int(quantity)

                except Exception as e:
                    return -1, f"Error processing price: {e}"
                break

        if market_price == -1:
            return -1, "Matching card not found"

        return market_price, None

    else:
        return -1, "No results found"

def analyze(deck_lines):
    total = 0
    errors = []
    for line in deck_lines:
        line = line.strip()
        if not line:
            continue
        mp, error = price(line)
        if mp == -1:
            errors.append(f"Could not find price for \"{line}\": {error}")
        else:
            total += mp
            
    return total, errors
