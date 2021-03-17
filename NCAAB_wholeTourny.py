import requests
import time
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import urllib3
import re

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = 'https://www.whatifsports.com/ncaab/'
browser = webdriver.Firefox()

rounds = 5
n=1
sims = 3

while n < rounds + 1:
    #Opens the Teams and Results file for reading and writting
    m=n+1
    with open('Teams_'+str(n)+'.txt') as t, open('Teams_'+str(m)+'.txt', 'w') as w, open('Winners', 'w') as r:
        for line in t:
            while True:
                try:
                    browser.get(url)
                    break
                except WebDriverException:
                    print("Website didn't load. Trying again...")

            #Re-initializing Variables
            homeWins = 0
            awayWins = 0
            homeLandslide = 0
            awayLandslide = 0

            away = line.split()
            home = next(t)
            home = home.split()

            if away.__len__()==2:
                away = away[0]+' '+away[1]
            elif away.__len__()==3:
                away = away[0]+' ' +away[1]+ ' ' +away[2]
            else:
                away = away[0]
            if home.__len__()==2:
                home = home[0]+' ' +home[1]
            elif home.__len__()==3:
                home = home[0]+' ' +home[1]+ ' ' +home[2]
            else:
                home = home [0]

            #Num of Simulations per game
            # sims = 2

            r.write(line + "\n") #Writes the text in the results
            split = line.split()

            #To detect headers IE: South, East etc..
            # if split.__len__() == 1:
            #     continue
            # elif split.__len__() > 1:
            #     # re.split('&', line)
            #     home = split[0]
            #     away = split[1]x
            #     print home
            #     print away


            #Finds the home and away team. Doesn't really matter since they are at neutral site

            # if split.__len__() == 3:
            #     home = split[0]
            #     away = split[1] + " " + split[2]
            #
            # elif split.__len__() == 4:
            #     home = split[0] + " " + split[1]
            #     away = split[2] + " " + split[3]
            # else:
            #     home = split[0]
            #     away = split[1]


            #Selects the away teams from the dropdown menus (Maybe could make a function out of these)
            ddAway = Select(browser.find_element_by_id("vname"))
            ddAway.select_by_visible_text(away)
            btnAway = browser.find_element_by_id("visitorbtn")
            btnAway.click()

            time.sleep(.5)

            # Selects the home teams from the dropdown menus
            ddHome = Select(browser.find_element_by_id("hname"))
            ddHome.select_by_visible_text(home)  # Replace Home here
            btnHome = browser.find_element_by_id("homebtn")
            btnHome.click()


            #Clicks the play game button
            playBtn = browser.find_element_by_id("playBtn")
            setHome = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div[2]/div/div/form/div[3]/div/div/div/div/div[2]/input[2]')
            setHome.click()
            playBtn.click()
            time.sleep(2)
            # iframe = browser.find_elements_by_tag_name('iframe')[1]
            # browser.switch_to.frame(iframe)
            
            for i in range(0, sims):
                time.sleep(3)
                # iframe = browser.find_elements_by_tag_name('iframe')[5]
                # browser.switch_to.frame(iframe)
                # print(browser.page_source)
                # f = browser.find_element(By.ID,"fancybox-frame")
                # browser.switch_to.frame(f)
                while True:
                    try:
                        frame = browser.find_element_by_xpath('//*[@id="fancybox-frame"]')
                        browser.switch_to.frame(frame)
                        break
                    except NoSuchElementException:
                        print("Couldn't find iFrame. Trying again...")
                
                # pass1 = browser.find_element_by_id("PASSFIELD1")
                while True:
                    try:
                        awayScore = browser.find_element_by_xpath('/html/body/div[2]/div[1]/table/tbody/tr[2]/td[4]').text
                        homeScore = browser.find_element_by_xpath('/html/body/div[2]/div[1]/table/tbody/tr[3]/td[4]').text
                        break
                    except NoSuchElementException:
                        print("Couldn't find scores. Trying again...")

                homeScore = int(homeScore)
                awayScore = int(awayScore)

                #Determining Winners for each game
                #Landslide determines if they won by 10+ points
                if (homeScore > awayScore):
                    homeWins = homeWins + 1
                    if ((homeScore - awayScore) > 10):
                        homeLandslide = homeLandslide + 1

                else:
                    awayWins = awayWins + 1
                    if ((awayScore - homeScore) > 10):
                        awayLandslide = awayLandslide + 1
                



                #Cleaning up the browser and refreshing to simulate another game
                browser.refresh()
                alert = browser.switch_to.alert
                alert.accept()
                browser.switch_to.default_content()

                #EXTRA STUFF FOR TESTING
                #     fancyClose = browser.find_element_by_id('fancybox-close')
                # fancyClose.click()
                # time.sleep(1)
                # switchHome = browser.find_element_by_id('vswitchlink')
                # switchHome.click()
                # browser.switch_to.default_content()
                # playBtn = browser.find_element_by_id("playBtn")
                # playBtn.click()
                # switch = switch + 1


            #Printing result data
            #With Dominations
            # print(home + ": " + str(homeWins) + "\t\t (by 10+): " + str(homeLandslide))
            # print(away + ": " + str(awayWins) + "\t\t (by 10+): " + str(awayLandslide))
            print(" ")
            #Without Dominations
            print(home + ": " + str(homeWins) + "("+str(homeLandslide)+")")
            print(away + ": " + str(awayWins) + "("+str(awayLandslide)+")")
            print(" ")

            #Writing result data -> Results

            # With Dominations
            # r.write(home + ": " + str(homeWins) + "\t (by 10+): " + str(homeLandslide) + "\n")
            # r.write(away + ": " + str(awayWins) + "\t (by 10+): " + str(awayLandslide) + "\n")
            #No Dominations
            r.write(home + ": " + str(homeWins) + "\n")
            r.write(away + ": " + str(awayWins) + "\n")
            r.write("\n")

            #Determining Winners
            if homeWins > awayWins:
                w.write(home + "\n")
            else:
                w.write(away + "\n")

            #Closes the popup window so next teams can be selected.
            # fancyClose = browser.find_element_by_id('fancybox-close')
            # fancyClose.click()
            # time.sleep(1)
            # visitClear = browser.find_element_by_id('visitorclearbtn')
            # time.sleep(1)
            # visitClear.click()
            # homeClear = browser.find_element_by_id('homeclearbtn')
            # time.sleep(1)
            # homeClear.click()
    n = n+1
    t.close()
    r.close()
    # w.close()
