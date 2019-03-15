import requests
import time
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import urllib3
import re

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = 'https://www.whatifsports.com/ncaab/'
browser = webdriver.Firefox()


#Opens the Teams and Results file for reading and writting
with open('Teams_64.txt') as t, open('Results_64.txt', 'w') as r, open('Winners_64.txt', 'w') as w:
    for line in t:
        browser.get(url)
        #Re-initializing Variables
        homeWins = 0
        awayWins = 0
        homeLandslide = 0
        awayLandslide = 0

        #Num of Simulations per game
        sims = 10

        r.write(line + "\n") #Writes the text in the results
        split = line.split()

        #To detect headers IE: South, East etc..
        if split.__len__() == 1:
            continue
        # elif split.__len__() > 1:
        #     # re.split('&', line)
        #     home = split[0]
        #     away = split[1]
        #     print home
        #     print away


        #Finds the home and away team. Doesn't really matter since they are at neutral site

        if split.__len__() == 3:
            home = split[0]
            away = split[1] + " " + split[2]

        elif split.__len__() == 4:
            home = split[0] + " " + split[1]
            away = split[2] + " " + split[3]
        else:
            home = split[0]
            away = split[1]


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
        setHome = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div/form/div[3]/div/div/div/div/div[2]/input[2]')
        setHome.click()
        playBtn.click()

        time.sleep(1)

        iframe = browser.find_elements_by_tag_name('iframe')

        for i in range(0, sims):
            time.sleep(3)
            f = browser.find_elements_by_tag_name('iframe')[0]
            browser.switch_to.frame(0)
            awayScore = browser.find_element_by_xpath('/html/body/div[2]/div[1]/table/tbody/tr[2]/td[4]').text
            homeScore = browser.find_element_by_xpath('/html/body/div[2]/div[1]/table/tbody/tr[3]/td[4]').text

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
        print(home + ": " + str(homeWins))
        print(away + ": " + str(awayWins))
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


t.close()
r.close()
w.close()
