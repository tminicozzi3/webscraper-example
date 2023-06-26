import json
import requests
from bs4 import BeautifulSoup

#import schedule
#import time

def createTheJson() :
    def toJson(url) :
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        })
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        list = []
        game_elements = soup.find_all("div", class_="game")
        sport = soup.find("h2", class_= "h4-style team-name").text.strip()
        if "boys" in sport.lower() :
            gender = "Boys" 
        elif "girls" in sport.lower() :
            gender = "Girls"
        else :
            gender = ""
        for game in game_elements :
            team = 'The Rivers School'
            if isinstance(game.find("div", class_="schedule-opponent"), type(None)) == False:
                opp = str(game.find("div", class_="schedule-opponent").text.strip())
            else :
                opp = ""
            timeList = []
            time_elements = game.find_all("span", class_="schedule-date")
            for x in time_elements :
                timeList.append(x)
            x1 = timeList[0].text.strip().find(",")
            date = timeList[0].text.strip()[x1 + 2:].strip()
            x2 = timeList[1].text.strip().find("-")
            time = timeList[1].text.strip()[:x2].strip()
            if isinstance(game.find("span", class_="winloss"), type(None)) == False :
                wL = str(game.find("span", class_="winloss").text.strip())
            else :
                wL = ""
            if isinstance(game.find("span", class_="score"), type(None)) == False :
                score = str(game.find("span", class_="score").text.strip())
            else :
                score = ""
            if isinstance(game.find("span", class_="schedule-location"), type(None)) == False :
                location = str(game.find("span", class_="schedule-location").text.strip())
            else :
                location = ""
            data = {
                "team" : team,
                "boys/girls" : gender,
                "sport" : sport,
                "opponent" : opp,
                "date" : date,
                "location" : location,
                "time" : time,
                "win/loss" : wL,
                "score" : score
            }
            list.append(data)

        return list 

    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    })

    riversURL = "https://www.rivers.org/athletics/teams"
    page2 = requests.get(riversURL, headers=headers)
    soup2 = BeautifulSoup(page2.content, "html.parser")

    listLinks = []
    for option in soup2.find_all("option"):
        if isinstance(option, type(None)) == False :
            if "varsity" in option.text.strip().lower() and "junior varsity" not in option.text.strip().lower() :
                id = option["value"].strip()
                listLinks.append("https://www.rivers.org/team-detail?fromId=249644&Team={}&SeasonLabel=2021%20-%202022&siteId=720".format(id))
    #LEAVES OUT SKIING - BUT NO RESULTS POSTED FOR SKIING...

    bigList = []
    for link in listLinks :
        list = toJson(link)
        bigList.extend(list)

    with open('rivers.json', 'w', encoding='utf-8') as f:
        json.dump(bigList, f, indent=9, ensure_ascii=False)

createTheJson()