# by pubins.taylor
# ESPN-FBB-DraftRoomScraper
# main.py v0.51
# init 02APR2022
# last update 05APR2022

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.chrome.options import Options
import time

myMemberId = '{3D596368-E046-4194-8C20-C0CB4F2E8BBD}'  # constant
leagueId = '1856747168'  # changes with league
teamId = '7'  # changes with league
baseUrl = 'https://fantasy.espn.com/baseball/draft?leagueId=' + leagueId + '&seasonId=2022&teamId=' + teamId + \
          '&memberId=' + myMemberId

bidCSSPath = 'div.current-amount' # deprecated as of v0.12
playerButtonXPath = '//*[@id="fitt-analytics"]/div/div[3]/div[2]/div[3]/div/nav/ul/li[1]/button'
draftSummaryButtonXPath = '//*[@id="fitt-analytics"]/div/div[3]/div[2]/div[3]/div/nav/ul/li[2]/button'
pickTableCSS = 'div.pick-history-tables'
draftedPlayerRowCSS = 'div.fixedDataTableCellGroupLayout_cellGroup'
draftedPlayerColCSS = 'div.player-column'
# TODO this element is produced if the player does not have a mug shot. Will need to get player data alternatively
#  when this element produces.
#  #fitt-analytics > div > div.draft-columns > div.draft-column.raised.flex.flex-column >
#  div.jsx-2898375982.pickArea.bb.brdr-clr-gray-06 > div > div.jsx-2649155106.pro-team-container.dib > div >
#  img.jsx-3743397412.fallback
playerCSS = '#fitt-analytics > div > div.draft-columns > div.draft-column.raised.flex.flex-column > ' \
             'div.jsx-2898375982.pickArea.bb.brdr-clr-gray-06 > div > div.jsx-2649155106.pro-team-container.dib > div ' \
             '> img:nth-child(1) '
draftedPlayersCSS = '#fitt-analytics > div > div.draft-columns > div:nth-child(3) > div > ' \
                     'div.jsx-553213854.container.overflow-hidden > div > ul '
# this element is located under the player's Name and bidding buttons
highestBidderCSS = '#fitt-analytics > div > div.draft-columns > div.draft-column.raised.flex.flex-column > ' \
                    'div.jsx-2007536929.bid-history__container.clr-gray-05.brdr-clr-gray-06.bb > ul > li:nth-child(1) '



def sesh():
    driver = webdriver.Chrome()
    options = Options().add_argument('usr-data-dir=/tmp/tarun')
    driver.get(baseUrl)
    driver.implicitly_wait(25)
    lastPlayerOnBlock = ''
    # provide default value
    currentPlayerOnBlock = 'trp'

    while True:
        try:
            # when a final bid is placed, the clock resets to a 9-second count down
            time.sleep(8)
            # grab the player's mugshot link w/ the player's id embedded then slice string to get playerid.
            # player id value is nested between //full/ & //.png hyperlink elements.
            # 2 splits taking the 2nd index and then first index produces the playerid.
            currentPlayerOnBlock = driver.find_element(By.CSS_SELECTOR, playerCSS).get_attribute('src') \
                .rsplit("full/")[1].rsplit('.png')[0]
            # splitting the text after the first space breaks the bid and team apart. postfixes below will generate a
            # list of 2 elements; bid value and bidder
            highestBidderElement = driver.find_element(By.CSS_SELECTOR, highestBidderCSS).text.split(' ', 1)
            print('player on block ', currentPlayerOnBlock, highestBidderElement)
            # if a new player is queued up; need to flip open the pick history table.
            if currentPlayerOnBlock != lastPlayerOnBlock:
                # click on the 'Draft Summary' tab
                driver.find_element(By.XPATH, draftSummaryButtonXPath).click()
                # wait for past picks to load
                driver.implicitly_wait(1)
                pickTables = driver.find_element(By.CSS_SELECTOR, pickTableCSS)
                # gets all the player columns in the pick tables.
                draftedPlayerCols = pickTables.find_elements(By.CSS_SELECTOR, draftedPlayerColCSS)
                # print(f'player rows has {len(draftedPlayerRows)} elements')
                # print(f'first element is {draftedPlayerRows[0].text}')
                for i in draftedPlayerCols:
                    draftedPlayerId = i.find_element(By.CSS_SELECTOR, 'div.jsx-3743397412.player-headshot > '
                                                                      'img.jsx-3743397412') \
                        .get_attribute('src').rsplit("full/")[1].rsplit('.png')[0]
                    winningTeam = driver.find_element(locate_with(By.CSS_SELECTOR, 'div.public_fixedDataTableCell_cellContent').to_right_of(i))
                    winningBid = driver.find_element(locate_with(By.CSS_SELECTOR, 'div.public_fixedDataTableCell_cellContent').to_right_of(winningTeam))
                    print(f'{draftedPlayerId} drafted by {winningTeam.text} for {winningBid.text}')
                # click back on the 'Players' tab
                driver.find_element(By.XPATH, playerButtonXPath).click()

            # updates decision parameters
            lastPlayerOnBlock = currentPlayerOnBlock

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