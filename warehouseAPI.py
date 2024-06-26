import requests as req

def checkWalmart(query):
    url = "http://leonsnet.cc:8443/getWalmartInventory"
    res = req.get(url)
    jsonRes = res.json()
    for i in jsonRes:
        if query.lower() in (i["Name"]).lower():
            return ("Walmart"), (i["Name"]).replace(" ", ""), (i["Price"]).replace(" $", "")
    return ("Walmart"), (query), ("Not found.")

def checkShoprite(query):
    url = "http://leonsnet.cc:8443/getShopriteInventory"
    res = req.get(url)
    jsonRes = res.json()
    for i in jsonRes:
        if query.lower() in (i["Name"]).lower():
            return ("Walmart"), (i["Name"]).replace(" ", ""), (i["Price"]).replace(" $", "")
    return ("Shoprite"), (query), ("Not found.")

        
def checkTarget(query):
    url = "http://leonsnet.cc:8443/getTargetInventory"
    res = req.get(url)
    jsonRes = res.json()
    for i in jsonRes:
        if query.lower() in (i["Name"]).lower():
            return ("Target"), (i["Name"]).replace(" ", ""), (i["Price"]).replace(" $", "")
    return ("Target"), (query), ("Not found.")
            