import selenium
import time
import xml.etree.cElementTree as ET
from array import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

#room is defied by its name and schedule
class room:
    def __init__(self,name :str):
        self.name = name
        self.schedule = ini_schedule()


    
# Converts "weekdayx" into x :int
def weekdays_converter (weeknhour):
    conv_weekday = weeknhour.split(" ")[0]

    if "0" in conv_weekday:
        conv_weekday = 0

    elif "1" in conv_weekday:
        conv_weekday = 1

    elif "2" in conv_weekday:
        conv_weekday = 2
         
    elif "3" in conv_weekday:
        conv_weekday = 3

    elif "4" in conv_weekday:
        conv_weekday = 4

    elif "5" in conv_weekday:
        conv_weekday = 5

    return conv_weekday

#Converts "hh:mm-hh:mm" to hhmm start and end times 
def hours_converter (hours):
    start_hour , end_hour = hours.split("-")
    start_hour_int = int(start_hour.replace(':',''))
    end_hour_int = int(end_hour.replace(':',''))

    return [start_hour_int,end_hour_int]

#Initializes schedule
#schedule[] is the week day (0=Monday,5=Saturday)
#schedule[][] is the 30min time slot (0=8:00-8:30;27=21:00-21:30)
    # 0 means its free, 1 means its occupied
def ini_schedule():
    _schedule = [[],[],[],[],[],[]]
    div = 27

    for _weekday in _schedule:
        i = 0
        while i <= div:
            _weekday.append(0)
            i = i+1
    return _schedule


#converts a given hour into its corresponding index (0-27)
#_hour works as starthour
def index_from_hour (_hour :int):
    i = 0
    first_hour = 800

    while _hour != first_hour:
        first_hour = first_hour + 30
        
        if first_hour%100 == 60:
            first_hour = first_hour +40
        i = i+1

    return i

#occupies schedule according to weekday and start and end hours
def add_To_schedule (_room :room, _day, _hours):
    conv_weekday = weekdays_converter(_day)
    conv_hours = hours_converter(_hours)

    start_time = index_from_hour(conv_hours[0])
    end_time = index_from_hour(conv_hours[1])-1


    while start_time != end_time+1:
        _room.schedule[conv_weekday][start_time] = 1
        start_time = start_time+1

#prints a schedule
def print_schedule(_room :room):
    print(_room.name)
    i=0
    for _weekday in _room.schedule:
        print("Day "+str(i))
        i = i+1

        for hour in _weekday:
            print(str(hour))

def highlight(element):
  driver = element._parent
  def apply_style(s):
     driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",element, s)
  original_style = element.get_attribute('style')
  apply_style("background: yellow; border: 2px solid red;")

def writeToXml (_rooms :room):

    list = ET.Element("list")    

    for room in _rooms:
        #roomName = ET.SubElement(list, room.name)
        roomName = ET.SubElement(list, str(room.name))
        i=0
        for weekday in room.schedule:
            
            #day = ET.SubElement(roomName, weekday)
            day = ET.SubElement(roomName, "Day "+str(i))
            i = i+1
            j=0
            for hour in weekday:
                #timeSlot = ET.SubElement(day, j)
                timeSlot = ET.SubElement(day, str(j))

                #occupy_value = ET.SubElement(timeSlot, hour)
                occupy_value = ET.SubElement(timeSlot, str(hour))
                j = j+1

    tree = ET.ElementTree(list)
    ET.dump(tree)
    tree.write("out.xml")




        

#main
driver = webdriver.Chrome()

roomsNames = ["V1.23","V1.24","V1.25","V1.31","V1.32"]
rooms = []
busy_hours = []

driver.maximize_window()

for room_it in roomsNames:
    driver.get("https://fenix.tecnico.ulisboa.pt/publico/findSpaces.do?spaceID=2448131361047&method=viewSpace&_request_checksum_=1d2ff4b392cfcf539414fe8b7eb6e1f960d3d010")
    
    xpath_aux = "//*[contains(text(), '{}')]".format(room_it)
    aux_element = driver.find_element(By.XPATH, xpath_aux)
    aux_element = aux_element.find_element(By.XPATH, "..")
    highlight(aux_element)
    aux_element = aux_element.find_element(By.XPATH, "td[3]/span/a")

    driver.get(aux_element.get_attribute("href"))
    aux_element = driver.find_element(By.LINK_TEXT, "Horário")
    driver.get(aux_element.get_attribute('href'))

    room_aux = room(str(room_it))
    rooms.append(room_aux)

    for busy_hour in driver.find_elements(By.CLASS_NAME , "period-first-slot"):
        add_To_schedule(room_aux,busy_hour.get_attribute('headers'),busy_hour.get_attribute('title'))

    #print_schedule(room_aux)
    writeToXml(rooms)