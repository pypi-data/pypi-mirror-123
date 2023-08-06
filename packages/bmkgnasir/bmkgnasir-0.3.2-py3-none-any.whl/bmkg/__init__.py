import requests
from bs4 import BeautifulSoup

def extract():
    try:
        content = requests.get('https://www.bmkg.go.id')
    except Exception:
        return None

    if content.status_code == 200:
        soup = BeautifulSoup(content.text, "html.parser")

        # Get Datetime
        datetime = soup.find("span", {"class": "waktu"})
        datetime = datetime.text.split(", ")
        date = datetime[0]
        time = datetime[1]

        # Get Magnitude
        result = soup.find("div", {"class": "col-md-6 col-xs-6 gempabumi-detail no-padding"})
        result = result.findChildren("li")
        magnitude = result[1].text
        depth = result[2].text
        latitude = result[3].text.split(' - ')[0]
        latitude2 = latitude.split(' ')[0]
        ls = "LS"
        lu = "LU"
        if latitude.find(ls) != -1:
            latitude2 = "-" + latitude2
        else:
            latitude2 = latitude2
        longitude = result[3].text.split(' - ')[1].split(' ')[0]
        result = dict()
        result["date"] = date
        result["time"] = time
        result["magnitude"] = magnitude
        result["depth"] = depth
        result["latitude"] = latitude2
        result["longitude"] = longitude
        return result

    else:
        return None

def show(result):
    if result is None:
        print("Can't find data")
        return
    print(f"Date : {result['date']}")
    print(f"Magnitude : {result['magnitude']}")
    print(f"Depth : {result['depth']}")
    print(f"latitide : {result['latitude']}")
    print(f"longitude : {result['longitude']}")