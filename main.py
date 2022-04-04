from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

url = 'https://fantasy.espn.com/baseball/draft?leagueId=964815732&seasonId=2022&teamId=8&memberId={3D596368-E046-4194-8C20-C0CB4F2E8BBD}'
selPath = 'div.current-amount'
# fitt-analytics > div > div.draft-columns > div.draft-column.raised.flex.flex-column > div.jsx-2898375982.pickArea.bb.brdr-clr-gray-06 > div > div.jsx-2649155106.pro-team-container.dib > div > img.jsx-3743397412.fallback
playerPath = '#fitt-analytics > div > div.draft-columns > div.draft-column.raised.flex.flex-column > div.jsx-2898375982.pickArea.bb.brdr-clr-gray-06 > div > div.jsx-2649155106.pro-team-container.dib > div > img:nth-child(1)'


def sesh():
    cOptions = Options()
    # cOptions.headless = True
    driver = webdriver.Chrome(options=cOptions)
    driver.get(url)
    driver.implicitly_wait(25)
    while (True):
        try:
            time.sleep(5)
            # grab the current bid
            currentBid = driver.find_element(By.CSS_SELECTOR, selPath).text
            # grab the player's headshot link w/ the player's id embedded
            # then slice to string to get playerid
            player = driver.find_element(By.CSS_SELECTOR, playerPath).get_attribute('src').

            print(player, currentBid)
        # important to catch the error inside the while loop so the program can continue when elements are not present
        except Exception as e:
            template = "Error caught! {0} occurred.\nDetails: {1!r}"
            message = template.format(type(e).__name__, e.args[0])
            print(message)

    driver.close()


if __name__ == '__main__':
    sesh()
