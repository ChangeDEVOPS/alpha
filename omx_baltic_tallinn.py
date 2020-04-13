import http.client
import json
import time

conn = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "9e6671c14dmsh184f85db4beeef6p13be69jsn6d38bfd5852e"
}
list = ["ARC1T",
        "BLT1T",
        "CPA1T",
        "EEG1T",
        "EFT1T",
        "HAE1T",
        "LHV1T",
        "MRK1T",
        "NCN1T",
        "PKG1T",
        "PRF1T",
        "SFG1T",
        "TAL1T",
        "TKM1T",
        "TSM1T",
        "TVEAT"
        ]


def get_response(stock):
    request = f"/stock/get-detail?region=US&lang=en&symbol={stock}.TL"
    conn.request("GET", request, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


for stock in list:
    result = get_response(stock)
    while "defaultKeyStatistics" not in result:
        result = get_response(stock)
    json_result = json.loads(result)
    PE = None # 0-10+10% = 0-11
    PB = None # 0-2 = 0 - 2.2
    ROE = None # >10%
    profitability = None # > 20%
    try:
        PE = json_result["summaryDetail"]["trailingPE"]["raw"]
        PB = json_result["defaultKeyStatistics"]["priceToBook"]["raw"]
        ROE = json_result["financialData"]["returnOnEquity"]["raw"]
        profitability = json_result["defaultKeyStatistics"]["profitMargins"]["raw"]
    except:
        continue
    if PE is not None and PE >= 0 and PE <= 12:
        if PB is not None and PB >= 0 and PB <= 2.2:
            if ROE is not None and ROE >= 0.2:
                if profitability is not None and profitability >= 0:
                    print(stock, PE, PB, ROE, profitability)