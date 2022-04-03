from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
#https://fantasy.espn.com/baseball/waitingroom?leagueId=1786659526
#https://fantasy.espn.com/baseball/draft?leagueId=1786659526&seasonId=2022&teamId=8&memberId={3D596368-E046-4194-8C20-C0CB4F2E8BBD}
url = 'https://fantasy.espn.com/baseball/draft?leagueId=1786659526&seasonId=2022&teamId=8&memberId={3D596368-E046-4194-8C20-C0CB4F2E8BBD}'
selPath = 'div.current-amount'
# this element is produced if the player does not have a mug shot
# fitt-analytics > div > div.draft-columns > div.draft-column.raised.flex.flex-column > div.jsx-2898375982.pickArea.bb.brdr-clr-gray-06 > div > div.jsx-2649155106.pro-team-container.dib > div > img.jsx-3743397412.fallback
playerPath = '#fitt-analytics > div > div.draft-columns > div.draft-column.raised.flex.flex-column > div.jsx-2898375982.pickArea.bb.brdr-clr-gray-06 > div > div.jsx-2649155106.pro-team-container.dib > div > img:nth-child(1)'
draftedPlayersPath = '#fitt-analytics > div > div.draft-columns > div:nth-child(3) > div > div.jsx-553213854.container.overflow-hidden > div > ul'
# this element is located under the player's Name and bidding buttons
highestBidderPath = '#fitt-analytics > div > div.draft-columns > div.draft-column.raised.flex.flex-column > div.jsx-2007536929.bid-history__container.clr-gray-05.brdr-clr-gray-06.bb > ul > li:nth-child(1)'

def sesh():
    cOptions = Options()
    # cOptions.headless = True
    driver = webdriver.Chrome(options=cOptions)
    driver.get(url)
    driver.implicitly_wait(25)
    while True:
        try:
            # when a final bid is placed, the clock resets to a 9 second count down
            time.sleep(8)
            # grab the current bid
            currentBid = driver.find_element(By.CSS_SELECTOR, selPath).text
            # grab the player's headshot link w/ the player's id embedded then slice to string to get playerid.
            # 2 splits taking the 2nd index and then first index produces the playerid.
            player = driver.find_element(By.CSS_SELECTOR, playerPath).get_attribute('src').rsplit("full/")[1].rsplit('.png')[0]
            highestBidder = driver.find_element(By.CSS_SELECTOR, highestBidderPath).text
            draftedPlayers = driver.find_elements(By.CSS_SELECTOR, draftedPlayersPath)
            # TODO for loop for draftedPlayers...place them into a list that does not need to get printed.
            print(player, currentBid, highestBidder)
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
