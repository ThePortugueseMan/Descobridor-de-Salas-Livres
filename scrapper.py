import selenium
import time
from array import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

class room:
    def __init__(self,name :str):
        self.name = name
        self.schedule = ini_schedule()


    

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

def hours_converter (hours):
    start_hour , end_hour = hours.split("-")
    start_hour_int = int(start_hour.replace(':',''))
    end_hour_int = int(end_hour.replace(':',''))
    #print(str(start_hour_int)+" até "+str(end_hour_int))

    return [start_hour_int,end_hour_int]

def ini_schedule():
    _schedule = [[],[],[],[],[],[]]
    div = 27

    for _weekday in _schedule:
        i = 0
        while i <= div:
            _weekday.append(0)
            i = i+1
    return _schedule
        
def index_from_hour (_hour :int):
    i = 0
    first_hour = 800
    #print("Hour is: "+str(_hour))

    while _hour != first_hour:
        first_hour = first_hour + 30
        
        if first_hour%100 == 60:
            first_hour = first_hour +40
        i = i+1
        #print(str(i)+": "+str(first_hour))
    #print(str(i))
    return i


def add_To_schedule (_room :room, _day, _hours):
    #print("Add")
    conv_weekday = weekdays_converter(_day)
    conv_hours = hours_converter(_hours)

    start_time = index_from_hour(conv_hours[0])
    end_time = index_from_hour(conv_hours[1])-1

    #print_schedule(_room.schedule)
    #print("Add: Day "+str(conv_weekday)+" - from" + str(start_time)+" to "+str(end_time))
    while start_time != end_time+1:
        _room.schedule[conv_weekday][start_time] = 1
        start_time = start_time+1


def print_schedule(_schedule):
    i=0
    for _weekday in _schedule:
        print("Day "+str(i))
        i = i+1

        for hour in _weekday:
            print(str(hour))




driver = webdriver.Chrome()

rooms_list = ["https://fenix.tecnico.ulisboa.pt/publico/findSpaces.do?spaceID=2448131361679&method=viewSpace&_request_checksum_=74e479d6a0ace5d939df42398cf6cd97f7d6fb71","https://fenix.tecnico.ulisboa.pt/publico/findSpaces.do?spaceID=2448131361680&method=viewSpace&_request_checksum_=0e36f9bdddb51d808dbbbce6a07ecdbd3aa637da","https://fenix.tecnico.ulisboa.pt/publico/findSpaces.do?spaceID=2448131361681&method=viewSpace&_request_checksum_=fbbec68a291a5fbd8630ca894dbbd04b34be368e"]
rooms = []
busy_hours = []
room_number = 0

driver.maximize_window()

for room_it in rooms_list:
    driver.get(room_it)

    aux_element = driver.find_element(By.LINK_TEXT, "Horário")
    driver.get(aux_element.get_attribute('href'))

    room_aux = room(str(room_number))
    rooms.append(room_aux)

    for busy_hour in driver.find_elements(By.CLASS_NAME , "period-first-slot"):
        add_To_schedule(room_aux,busy_hour.get_attribute('headers'),busy_hour.get_attribute('title'))

#print_schedule(rooms[0].schedule)


    
#aux_element = driver.find_element(By.CLASS_NAME , "period-first-slot")
#print(aux_element.get_attribute('title'))
#print(aux_element.get_attribute('headers'))

