# by pubins.taylor
# ESPN-FBB-DraftRoomScraper
# main.py v0.12
# init 02APR2022
# last update 03APR2022

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

myMemberId = '{3D596368-E046-4194-8C20-C0CB4F2E8BBD}'  # constant
leagueId = '725581429'  # changes with league
teamId = '4'  # changes with league
baseUrl = 'https://fantasy.espn.com/baseball/draft?leagueId=' + leagueId + '&seasonId=2022&teamId=' + teamId + '&memberId=' + myMemberId
url = ''
bidCSSPath = 'div.current-amount'
summaryButtonXPath = '//*[@id="fitt-analytics"]/div/div[3]/div[2]/div[3]/div/nav/ul/li[2]'
pickTableCSSPath = 'div.pick-history-tables'
# this element is produced if the player does not have a mug shot
# fitt-analytics > div > div.draft-columns > div.draft-column.raised.flex.flex-column > div.jsx-2898375982.pickArea.bb.brdr-clr-gray-06 > div > div.jsx-2649155106.pro-team-container.dib > div > img.jsx-3743397412.fallback
playerPath = '#fitt-analytics > div > div.draft-columns > div.draft-column.raised.flex.flex-column > ' \
             'div.jsx-2898375982.pickArea.bb.brdr-clr-gray-06 > div > div.jsx-2649155106.pro-team-container.dib > div ' \
             '> img:nth-child(1) '
draftedPlayersPath = '#fitt-analytics > div > div.draft-columns > div:nth-child(3) > div > ' \
                     'div.jsx-553213854.container.overflow-hidden > div > ul '
# this element is located under the player's Name and bidding buttons
highestBidderPath = '#fitt-analytics > div > div.draft-columns > div.draft-column.raised.flex.flex-column > ' \
                    'div.jsx-2007536929.bid-history__container.clr-gray-05.brdr-clr-gray-06.bb > ul > li:nth-child(1) '


def sesh():
    cOptions = Options()
    # cOptions.headless = True
    driver = webdriver.Chrome(options=cOptions)
    driver.get(baseUrl)
    driver.implicitly_wait(25)
    while True:
        try:
            # when a final bid is placed, the clock resets to a 9-second count down
            time.sleep(8)
            # grab the current bid
            currentBid = driver.find_element(By.CSS_SELECTOR, bidCSSPath).text
            # grab the player's mugshot link w/ the player's id embedded then slice string to get playerid.
            # 2 splits taking the 2nd index and then first index produces the playerid.
            player = driver.find_element(By.CSS_SELECTOR, playerPath).get_attribute('src') \
                .rsplit("full/")[1].rsplit('.png')[0]
            # splitting the text after the first space breaks the bid and team apart
            highestBidder = driver.find_element(By.CSS_SELECTOR, highestBidderPath).text.split(' ', 1)

            # deprecated v0.12
            #   draftedPlayersDiv = driver.find_element(By.CSS_SELECTOR, draftedPlayersPath)
            #   draftedPlayers = draftedPlayersDiv.find_elements(By.TAG_NAME, 'li')
            #
            # TODO click on Draft Summary Tab.  Scrape pick history tables.
            #  The precipitating circumstance should be when the bid value is lower than the previous bid.
            #  for i in draftedPlayers:
            #  print(i.text)
            # TODO click back on Players.
            print(player, highestBidder)
        # important to catch the error inside the while loop so the program can continue when elements are not present
        except Exception as e:
            if e == NoSuchWindowException:
                break
            template = "Error caught! {0} occurred.\nDetails: {1!r}"
            message = template.format(type(e).__name__, e.args[0])
            print(message)

    driver.close()


if __name__ == '__main__':
    sesh()
