from bs4 import BeautifulSoup
import requests
import sqlite3
import time

url = "https://www.lyngsat.com/"
conn = sqlite3.connect("TvSat.db")
cur = conn.cursor()


def main_page():
    """opens lyngsat.com and returns the urls for the sattelite servers, packages, and trackers"""
    load = False
    while not load:
        try:
            response = requests.get(url).text
            load = True
        except:
            sec = 5
            print("Connection Error, retrying in " + str(sec) + " Minutes")
            time.sleep(sec * 60)

    html_text = BeautifulSoup(response, "lxml")
    satellite_urls = []
    package_urls = []
    tracker_urls = []

    trs = html_text.find_all("tr")

    for tr in trs:
        if tr.td != None:
            if tr.td.font != None:
                if tr.td.font.text == "Satellites:":
                    satellites = tr.find_all("a")
                    for satellite in satellites:
                        satellite_urls.append(url + satellite["href"])
                elif tr.td.font.text == "Packages:":
                    packages = tr.find_all("a")
                    for package in packages:
                        package_urls.append(url + package["href"])
                elif tr.td.font.text == "SatTracker:":
                    trackers = tr.find_all("a")
                    for tracker in trackers:
                        tracker_urls.append(url + tracker["href"])

    return satellite_urls, package_urls, tracker_urls


def satellites_page(satellite_server_url):
    """opens the satellite page and returns the names, position, and urls for the sattelites"""
    load = False
    while not load:
        try:
            response = requests.get(satellite_server_url).text
            load = True
        except:
            sec = 5
            print("Connection Error, retrying in " + str(sec) + " Minutes")
            time.sleep(sec * 60)
    html_text = BeautifulSoup(response, "lxml")
    satellite_urls = []
    satellite_positions = []
    sattelite_names = []
    region_ = satellite_server_url[24:-5]
    print(region_)
    big_table = html_text.find("table", width=720, align="center")
    if big_table != None:
        trs = big_table.find_all("tr")
        for j, tr in enumerate(trs[1::]):
            if tr.td != None:
                if tr.td.a != None:
                    if (url + tr.td.a["href"]) not in satellite_urls:
                        satellite_urls.append(url + tr.td.a["href"])
                        if "°" in tr.td.find("font").text:
                            satellite_positions.append(str(tr.td.find("font").text))
                        else:
                            satellite_positions.append(satellite_positions[-1])
                tds = tr.find_all("td")
                if len(tds) == 3:
                    tds.insert(0, satellite_positions[j])
                for i, td in enumerate(tds):

                    if i == 1:

                        temp = td.find_all("a")

                        temp = temp[0].text

                        sattelite_names.append(temp)
                        try:
                            cur.execute(
                                "INSERT INTO satellite (name, region, pos) VALUES (?, ?, ?);",
                                (temp, region_, satellite_positions[j]),
                            )
                            print(temp, region_, satellite_positions[j])
                            conn.commit()
                        except:
                            pass

    for satellite_url in satellite_urls:
        satellite_page(satellite_url)

    return sattelite_names, satellite_positions, satellite_urls


def satellite_page(sattelite_url):
    """opens a sattelite page and return the channel names and urls"""
    print(sattelite_url)
    load = False
    while not load:
        try:
            response = requests.get(sattelite_url).text
            load = True
        except:
            sec = 5
            print("Connection Error, retrying in " + str(sec) + " Minutes")
            time.sleep(sec * 60)

    html_text = BeautifulSoup(response, "lxml")
    # lists
    channel_urls = []
    channel_names = []

    big_table = html_text.find(
        "table", width=720, border="", cellspacing=0, cellpadding=0
    )
    if big_table != None:
        trs = big_table.find_all("tr")
        for tr in trs:
            if tr != None:
                tds = tr.find_all("td")
                while len(tds) > 7:
                    tds = tds[1::]
                if tds[0] != None:
                    if tds[0].i == None and tds[0].a != None:
                        channel_names.append(tds[0].a.text)
                        try:
                            cur.execute(
                                "INSERT INTO channels (name) VALUES (?);",
                                (tds[0].a.text,),
                            )
                            conn.commit()
                            print(tds[0].a.text)
                        except:
                            pass
                        channel_urls.append(tds[0].a["href"])

    for i, channel_url in enumerate(channel_urls):
        channel_page(channel_url, channel_names[i])

    return channel_names, channel_urls


def channel_page(channel_url, name):
    """takes a channel_url and returns the
    systems, encryptions, languages, video encodes, fecs, srs, frequencies, packages of the channel, and
    the beams and EIRPs of the sattelite it is on."""
    load = False
    while not load:
        try:
            response = requests.get(channel_url).text
            load = True
        except:
            sec = 5
            print("Connection Error, retrying in " + str(sec) + " Minutes")
            time.sleep(sec * 60)

    html_text = BeautifulSoup(response, "lxml")
    # lists
    systems = []
    encryptions = []
    langs = []
    vide_encodes = []
    fecs = []
    srs = []
    freqs = []
    packs = []
    beams = []
    erips = []

    big_table = html_text.find(
        "table", width=700, border=1, cellspacing=0, cellpadding=0
    )
    print(channel_url)
    if big_table != None:
        trs = big_table.find_all("tr")
        for tr in trs[2::]:
            if tr != None:
                tds = tr.find_all("td")
                temp_sat = ""
                for i, td in enumerate(tds):
                    if td != None:
                        if i == 0:
                            pass
                        elif i == 1:
                            temp_sat = str(td.text)
                            pass
                        elif i == 2:
                            temp = td.text
                            try:
                                e = str(td).split("<br/>")[1][
                                    : str(td).split("<br/>")[1].index("<")
                                ]
                                b = str(td.text).split(e)[0]
                            except:
                                e = None
                                b = str(td.text)
                                pass

                            beams.append((temp_sat, b))
                            erips.append((temp_sat, e))
                            try:
                                print(
                                    'UPDATE satellite SET beam = "'
                                    + b
                                    + '", EIRP = "'
                                    + e
                                    + '" WHERE name = "'
                                    + temp_sat
                                    + '";'
                                )
                                cur.execute(
                                    'UPDATE satellite SET beam = "'
                                    + b
                                    + '", EIRP = "'
                                    + e
                                    + '" WHERE name = "'
                                    + temp_sat
                                    + '";'
                                )
                            except:
                                print(
                                    'UPDATE satellite SET beam = "'
                                    + b
                                    + '" WHERE name = "'
                                    + temp_sat
                                    + '";'
                                )
                                cur.execute(
                                    'UPDATE satellite SET beam = "'
                                    + b
                                    + '" WHERE name = "'
                                    + temp_sat
                                    + '";'
                                )

                        elif i == 3:
                            freqs.append((temp_sat, name, td.text))
                            try:
                                cur.execute(
                                    "INSERT INTO chan_sat (channel_name, sat_name, frequency) VALUES (?, ?, ?);",
                                    (name, temp_sat, td.text),
                                )
                            except:
                                pass
                        elif i == 4:
                            systems.append((temp_sat, name, td.text))
                            cur.execute(
                                'UPDATE satellite SET sys = "'
                                + td.text
                                + '" WHERE name = "'
                                + temp_sat
                                + '";'
                            )
                        elif i == 5:
                            s = str(td).split("<br/>")[0].split(">")[-1]
                            f = str(td).split("<br/>")[1].split("<")[0]
                            srs.append((temp_sat, name, s))
                            fecs.append((temp_sat, name, f))
                            print(
                                'UPDATE channels SET SR = "'
                                + s
                                + '", FEC = "'
                                + f
                                + '" WHERE name = "'
                                + name
                                + '";'
                            )
                            cur.execute(
                                'UPDATE channels SET SR = "'
                                + s
                                + '", FEC = "'
                                + f
                                + '" WHERE name = "'
                                + name
                                + '";'
                            )
                        elif i == 6:
                            vide_encodes.append((temp_sat, name, td.text))
                            cur.execute(
                                'UPDATE channels SET vid_encode = "'
                                + td.text
                                + '" WHERE name = "'
                                + name
                                + '";'
                            )
                        elif i == 7:
                            flag = False
                            temp = ""
                            for c in td.text:
                                if c.isalpha() == False:
                                    break
                                if c.isupper() and not flag:
                                    temp = temp + c
                                    flag = True
                                elif c.isupper() and flag:
                                    langs.append((temp_sat, name, temp))
                                    try:
                                        cur.execute(
                                            """INSERT INTO chan_lang (name, lang) VALUES (?, ?);""",
                                            (name, temp),
                                        )
                                    except:
                                        pass
                                    temp = c
                                else:
                                    temp = temp + c
                        elif i == 8:
                            encryptions.append((temp_sat, name, td.text))
                            cur.execute(
                                'UPDATE channels SET encryption = "'
                                + td.text
                                + '" WHERE name = "'
                                + name
                                + '";'
                            )
                        elif i == 9:
                            if td.text != "":
                                packs.append((temp_sat, name, td.text))
                                cur.execute(
                                    'UPDATE chan_sat SET prov_pack = "'
                                    + td.text
                                    + '" WHERE channel_name = "'
                                    + name
                                    + '" AND sat_name = "'
                                    + temp_sat
                                    + '";'
                                )
                            else:
                                packs.append((temp_sat, name, None))
                        print("update lists")
                        conn.commit()

    return (
        systems,
        encryptions,
        langs,
        vide_encodes,
        fecs,
        srs,
        freqs,
        packs,
        beams,
        erips,
    )


def trackers_page(tracker_url):
    """takes a tracker server url and returns the list of tracker urls"""
    load = False
    while not load:
        try:
            response = requests.get(tracker_url).text
            load = True
        except:
            sec = 5
            print("Connection Error, retrying in " + str(sec) + " Minutes")
            time.sleep(sec * 60)
    html_text = BeautifulSoup(response, "lxml")
    tracker_urls = []
    satellite_positions = []
    tracker_names = []

    big_table = html_text.find("table", width=720, align="center")
    if big_table != None:
        trs = big_table.find_all("tr")
        for j, tr in enumerate(trs[1::]):
            if tr.td != None:
                if tr.td.a != None:
                    if (tr.td.a["href"]) not in tracker_urls:
                        tracker_urls.append(tr.td.a["href"])
                        print(tr.td.a["href"])
                tds = tr.find_all("td")
                if len(tds) == 3:
                    tds.insert(0, satellite_positions[j])
                for i, td in enumerate(tds):

                    if i == 1:

                        temp = td.find_all("a")

                        temp = temp[0].text

                        tracker_names.append(temp)
                        print(temp)

    for i, tracker_url in enumerate(tracker_urls):
        tracker_page(tracker_url, tracker_names[i])
    return tracker_names, tracker_urls


def tracker_page(tracker_url, name):
    """takes a tracker url and returns the launching rocket and launching time of the sattelite"""
    load = False
    while not load:
        try:
            response = requests.get(tracker_url).text
            load = True
        except:
            sec = 5
            print("Connection Error, retrying in " + str(sec) + " Minutes")
            time.sleep(sec * 60)

    html_text = BeautifulSoup(response, "lxml")

    for font in html_text.find_all("font"):
        if "launched" in font.text:
            launch_date = str(font.text).split("\n")[1][-11:-1]
            launching_rkt = (
                str(font.text).split("\n")[1].split("was launched with ")[1][0:-12]
            )
            cur.execute(
                'UPDATE satellite SET launch_date = "'
                + launch_date
                + '", launch_rkt = "'
                + launching_rkt
                + '" WHERE name = "'
                + name
                + '";'
            )
            print(launch_date, launching_rkt)
            conn.commit()

            return launch_date, launching_rkt
    return "None", "None"


def main():
    """main function"""
    start = time.time()
    satellite_urls, package_urls, tracker_urls = main_page()
    for satellite_url in satellite_urls:
        satellites_page(satellite_url)
    for tracker_url_ in tracker_urls:
        trackers_page(tracker_url_)
    conn.commit()
    conn.close()
    end = time.time()
    taken_s = end - start
    taken_m = taken_s / 60
    time_s = taken_s % 60
    taken_h = taken_m / 60
    time_m = taken_m % 60

    print(
        "Time taken: "
        + str(int(taken_h))
        + " hours "
        + str(int(time_m))
        + " minutes "
        + str(int(time_s))
        + " seconds"
    )


main()
