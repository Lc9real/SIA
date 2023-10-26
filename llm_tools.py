import os
from langchain.tools import Tool
from langchain.chains import LLMMathChain
import wikipedia
import shutil
import tool_SD
import requests
from googlesearch import search
from bs4 import BeautifulSoup
from datetime import datetime
from duckduckgo_search import DDGS
import asyncio
from geopy.geocoders import Nominatim
from open_meteo import OpenMeteo
from open_meteo.models import DailyParameters, HourlyParameters
import magichue
import keyboard
import win32clipboard




light = magichue.Light("192.168.0.59")

#funktion
def get_path(none: str) -> str:
    """returns the path of this folder"""
    return os.getcwdb()
def Create_file(fullstring):
        """create a file on the path and write the content to it"""
        list = fullstring.split(',')
        path, content = list[0], list[1:]
        content = ",".join(content)
        try:
            f = open(path, "x")
            f.write(content.replace("\\n", "\n"))
            return "Done"
        except:
            return "this file already exists try a different name or place"

def move_file(fullstring):
    """move file from old path to new"""
    list = fullstring.split(',')
    oldpath, newpath = list[0], list[1:]
    shutil.move(oldpath, newpath)

    return "Done"


def search_File(fileToSearch, rootDir="C/User/"):
    for relPath,dirs,files in os.walk(rootDir):
        if(fileToSearch in files):
            fullPath = os.path.join(rootDir,relPath,fileToSearch)
            return fullPath


def copy_file(fullstring):
    """copy file from one path to another path"""
    list = fullstring.split(',')
    oldpath, newpath = list[0], list[1:]
    shutil.copy(oldpath, newpath)

    return "Done"


def delete_file(path):
    if "SIA" in path:
        os.remove(path)
        return "Done"
    else:
        return "You only have permission to delete files in C:/Users/lukac/SIA"



def get_links(searchin):
    list2 = []
    for links in search(searchin, tld="co.in", num=10, stop=10, pause=2):
        list2.append(links)
    return list2


def get_Wiki(searchin):
    try:
        return wikipedia.summary(searchin)
    except:
        return "didn't find a wikipedia page with that name"

def web_scraper(url):
    page = requests.get(url)
    return page.text[:6000]
def web_text_scraper(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.text[:6000]

def get_date(inp):
    return datetime.now()

def console(command):
    return os.system(command)

def ddgos(searchin):
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(searchin, max_results=5)]
        return results

async def get_weather_async(inp):
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(inp)
    async with OpenMeteo() as open_meteo:
        forecast = await open_meteo.forecast(
            latitude=location.latitude,
            longitude=location.longitude,
            current_weather=True,
            past_days=1,
            timezone= "GMT",
            daily=[
                DailyParameters.SUNRISE,
                DailyParameters.SUNSET,
            ],
            hourly=[
                HourlyParameters.TEMPERATURE_2M,
                HourlyParameters.RELATIVE_HUMIDITY_2M,
            ],
        )
        print(forecast)
        return forecast.current_weather

def get_weather(inp):
    return asyncio.run(get_weather_async(inp))

def set_clipboard(data:str):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(data)
    win32clipboard.CloseClipboard()

def get_clipboard(inp:str):
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return data
    except:
        data = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
        win32clipboard.CloseClipboard()
        return data

def light_state(inp:str):
    if inp.lower() == "on" or inp.lower() == "1":
        #light.on = True
        return "Light is turned on"
    elif inp.lower() == "off" or inp.lower() == "0":
        #light.on = False
        return "Light is turned off"
    else:
        return "Wrong key input is on off 1 or 0"
def change_light_color(fullstring:str):

    strlist = fullstring.split(',')
    rgb = strlist[0], strlist[1], strlist[2]
    rgb = list(map(int, rgb))
    #light.rgb = rgb
    return "Color was changed"
def change_light_brightness(bright:int):
    #light.brightness = bright
    return "brighness was changed"


def play_pause(state:str):
    keyboard.press_and_release('play/pause media')
    if state == "pause":
        return "Music is getting paused"
    else:
        return "Music is getting played again"


def start_file(path:str):
    os.startfile(path)
    return f"{path} was opend"



#tools
def load_tools(llm):
    tools = [
        Tool(
            name="FileCreator",
            func=Create_file,
            description="useful for when you need to Create a File at a Directory. The input to this tool should be a comma separated list of the path to the file and the content like this: [the path to the file you want to create], [the content of the file]. For example: C:/Users/lukac/Desktop/newFile.txt,ABCD, would be the input if you wanted to Create a file on the Desktop named newFile.txt with the content 'ABCD'.",
        )
    ]

    llm_math_chain = LLMMathChain(llm=llm)
    tools.append(
        Tool.from_function(
            func=llm_math_chain.run,
            name="Calculator",
            description="useful for when you need to answer questions about math",

        )
    )

    tools.append(
        Tool.from_function(
            func=get_path,
            name="getPath",
            description="useful for when you need to get the path of this folder",

        )
    )



    tools.append(
        Tool(
            name="FileMover",
            func=move_file,
            description="useful for when you need to Move a File from one path to another. The input to this tool should be a comma separated list of the old path to the file and the new path like this: '[the path to the file you want to move], [the new path of the file]'. For example, 'C:/Users/lukac/Desktop/newFile.txt,C:/Users/lukac/Desktop/random shit/newFile.txt', would be the input if you wanted to move a file from the Desktop to a folder on the desktop called random shit.",
        ))

    tools.append(
        Tool.from_function(
            func=tool_SD.generate_image,
            name="generateImage",
            description="useful for when you need to generate an image input is a prompt like 'realistic futuristic city-downtown with short buildings, sunset' wich will create a beatifull futuristic city",

        )
    )

    tools.append(
        Tool(
            name="FileCopier",
            func=copy_file,
            description="useful for when you need to copy a File from one path to another. The input to this tool should be a comma separated list of the path to the file and the new path like this: '[the path to the file you want to copy], [the new path of the file]'. For example, 'C:/Users/lukac/Desktop/newFile.txt,C:/Users/lukac/Desktop/random shit/newFile.txt', would be the input if you wanted to move a file form the Desktop to a folder on the desktop called random shit.",
        ))

    tools.append(
        Tool(
            name="FileDeleter",
            func=delete_file,
            description="useful for when you need to delete a File. The input to this tool should be the path to the file you want to delet. For example, 'C:/Users/lukac/SIA/Files/New_File.txt', would be the input if you wanted to delet a file called New_File.txt.",
        ))

    tools.append(
        Tool.from_function(
            func=get_links,
            name="get_link",
            description="useful for when you need to search for links on google input is search word, returns first 10 links",

        )
    )

    tools.append(
        Tool.from_function(
            func=get_Wiki,
            name="wikipedia",
            description="useful for when you need to search wikipedia for information will return a summery of the article",

        )
    )

    tools.append(
        Tool.from_function(
            func=web_scraper,
            name="website_scraper",
            description="useful for when you need to get the html code of an url",

        )
    )

    tools.append(
        Tool.from_function(
            func=web_text_scraper,
            name="website_text_scraper",
            description="useful for when you need to get the text content thats on an website input is a url",

        )
    )
    tools.append(
        Tool.from_function(
            func=get_date,
            name="time",
            description="useful for when you need to now the time or date input is 'now'",

        )
    )
    tools.append(
        Tool.from_function(
            func=console,
            name="console",
            description="useful for when you need to run cmd or console commands",

        )
    )

    tools.append(
        Tool.from_function(
            func=ddgos,
            name="ddgo_search",
            description="useful for when you need to search something on duck duck go or get current data",

        )
    )

    tools.append(
        Tool.from_function(
            func=get_weather,
            name="weather",
            description="useful for when you need to know the weather conditions of a city input is the city name",


        )
    )

    tools.append(
        Tool.from_function(
            func=light_state,
            name="light",
            description="useful for when you need to turn the light on or off. the input is on, 1, off or 0",

        )
    )
    tools.append(
        Tool(
            name="light_color",
            func=change_light_color,
            description="useful for when you need to change the color of the light. The input to this tool should be a comma separated list of the rgb color code: '[red 0-256],[green 0-256],[blue 0-256]'. For example: '0,256,256', would be the input if you wanted to change the color of the light to cyan.",
        ))
    tools.append(
        Tool.from_function(
            func=change_light_brightness,
            name="brightness",
            description="useful for when you need to change the brightness of the light. the input is a number from 0 to 256",

        )
    )

    tools.append(
        Tool.from_function(
            func=play_pause,
            name="music",
            description="useful for when you need to pause the music input is pause or play",

        )
    )

    tools.append(
        Tool.from_function(
            func=start_file,
            name="start_file",
            description="useful for when you need to open a file on the users screen",

        )
    )

    tools.append(
        Tool.from_function(
            func=set_clipboard,
            name="set_clipboard",
            description="useful for when you need to copy something into the clipboard of the user",

        )
    )

    tools.append(
        Tool.from_function(
            func=get_clipboard,
            name="get_clipboard",
            description="useful for when you need to get something out of the clipboard of the user",

        )
    )






    return tools