import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

class room:
    def __init__(self, name, schedule):
        self.name = name
        self.schedule = schedule
    

def weekdays_converter (weeknhour):
    conv_weekday = weeknhour.split(" ")[0]

    if "0" in conv_weekday:
        conv_weekday = "2ª"

    elif "1" in conv_weekday:
        conv_weekday = "3ª"

    elif "2" in conv_weekday:
        conv_weekday = "4ª"
         
    elif "3" in conv_weekday:
        conv_weekday = "5ª"

    elif "4" in conv_weekday:
        conv_weekday = "6ª"

    elif "5" in conv_weekday:
        conv_weekday = "Sáb"

    return conv_weekday

def hours_converter (hours):
    conv_hours = []
    conv_hours[0] , conv_hours[1] = hours.split("-") 
        
room_list = []    
driver = webdriver.Chrome()

rooms_list = ["https://fenix.tecnico.ulisboa.pt/publico/findSpaces.do?spaceID=2448131361679&method=viewSpace&_request_checksum_=74e479d6a0ace5d939df42398cf6cd97f7d6fb71","https://fenix.tecnico.ulisboa.pt/publico/findSpaces.do?spaceID=2448131361680&method=viewSpace&_request_checksum_=0e36f9bdddb51d808dbbbce6a07ecdbd3aa637da","https://fenix.tecnico.ulisboa.pt/publico/findSpaces.do?spaceID=2448131361681&method=viewSpace&_request_checksum_=fbbec68a291a5fbd8630ca894dbbd04b34be368e"]
busy_hours = []
room_number = 0

driver.maximize_window()

for room in rooms_list:
    driver.get(room)
    room_number = room_number + 1
    print("Sala "+str(room_number))
    aux_element = driver.find_element(By.LINK_TEXT, "Horário")
    driver.get(aux_element.get_attribute('href'))

    for busy_hour in driver.find_elements(By.CLASS_NAME , "period-first-slot"):
        hour_converter(busy_hour.get_attribute('headers'),busy_hour.get_attribute('title'))
        #print(busy_hour.get_attribute('headers')+"   "+busy_hour.get_attribute('title'))




    
#aux_element = driver.find_element(By.CLASS_NAME , "period-first-slot")
#print(aux_element.get_attribute('title'))
#print(aux_element.get_attribute('headers'))

