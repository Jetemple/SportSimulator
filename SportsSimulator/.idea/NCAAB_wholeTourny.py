import requests
import time
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import urllib3

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = 'https://www.whatifsports.com/ncaab/'
browser = webdriver.Firefox()
browser.get(url)

#Opens the Teams and Results file for reading and writting
with open('Teams_64.txt') as t, open('Results_64.txt', 'w') as r:
    for line in t:
        #Re-initializing Variables
        homeWins = 0
        awayWins = 0
        homeLandslide = 0
        awayLandslide = 0

        #Num of Simulations per game
        sims = 2

        r.write(line + "\n") #Writes the text in the results
        split = line.split()

        #To detect headers IE: South, East etc..
        if split.__len__() == 1:
            continue

        #Finds the home and away team. Doesn't really matter since they are at neutral site
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
            time.sleep(2)
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
        print(home + ": " + str(homeWins) + " - (by 10+): " + str(homeLandslide))
        print(away + ": " + str(awayWins) + " - (by 10+): " + str(awayLandslide))
        print(" ")

        #Writing result data -> Results
        r.write(home + ": " + str(homeWins) + " - (by 10+): " + str(homeLandslide) + "\n")
        r.write(away + ": " + str(awayWins) + " - (by 10+): " + str(awayLandslide) + "\n")
        r.write("\n")

        #Closes the popup window so next teams can be selected.
        fancyClose = browser.find_element_by_id('fancybox-close')
        fancyClose.click()
        visitClear = browser.find_element_by_id('visitorclearbtn')
        time.sleep(.5)
        visitClear.click()
        homeClear = browser.find_element_by_id('homeclearbtn')
        time.sleep(.5)
        homeClear.click()


t.close()
r.close()
