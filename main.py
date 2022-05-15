from bs4 import BeautifulSoup
import requests
#import BS/requests



#first for loop goes through a few pages of games. htmlText requests for the url then passed into soup(all the html). For loops to find names and prices and then add to lists
def soupActivation():
    gameNames = []
    gamePrices = []
    pages = [3]
    for page in pages:
        htmlText = requests.get('https://www.varle.lt/kompiuteriniai-zaidimai/?p={}'.format(page)).text
        soup = BeautifulSoup(htmlText, 'lxml')
        for gameName in soup.find_all('span', class_='inner'):
            gameNames.append(gameName.text.replace(' ', ''))
        for gamePrice in soup.find_all('span', class_='price'):
            gamePrice = str(gamePrice.text)
            charToCheck = "€"
            if charToCheck in gamePrice:
                gamePrice = gamePrice[:-3]
                gamePrices.append(gamePrice.replace(',', '.'))
    return gameNames,gamePrices


#gameNames, gamePrices = soupActivation()












