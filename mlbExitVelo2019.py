from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tweepy
import time

consumer_key = 'ze32oehd7WwH9KTVghHxf43jK'
consumer_secret = 'T49JzKc7ChzjgPYfAGjoQJfWUfUL3GZTbBX33p2VKoFb2Ob1hI'
access_token = '1051201677959843841-NUw4Z8JJpApsWABdfh116Gm7GWXkGl'
access_token_secret = '593a7i8njo1FKfFBd6DZWwUWj8UcNW4slgJ9RpizO4zVY'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
 
def finalizeBIP ():
    driver = webdriver.Safari()
    driver.get('https://baseballsavant.mlb.com/gamefeed?game_pk=599371&game_date=2019-10-22&type=exit_velocity&chart_view=pitch&chart_type=sbp&inning=&count=&batter_hand=&pitcher_hand=&filter=&player=home-pitchers_543037&view=Umpire&coloring=Pitch%20Type')
    
    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.ID, "exitVelocity-tr_2")))
    
    data = driver.page_source
    
    
    soup = BeautifulSoup(data, "html.parser")
    
    allExits = soup.find('div', id='exitVelocity')
    allScore = soup.find('div', id='scoreboard-element')
    score = allScore.findAll('div')
    scoreN = score[6].text
    scoreA = score[15].text

    individualBIP = allExits.findAll('tr')
    individualBIP = individualBIP [:]
    count = 0
    finalResult = []
    
    for BIP in individualBIP: 
        status = False
        hitData = []
        spans = BIP.findAll('span')
        tempResult = []
        for i in range(len(spans)):
            hitData.append(spans[i].text)
        
        if (count > 1):
            result = str(hitData[6]).lower()
            
            if (result == 'undefined'):
                continue
            elif (result == 'lineout'):
                result = ' lined out off of '
            elif (result == 'single'):
                result = ' singled off of '
            elif (result == 'double'):
                result = ' doubled off of '
            elif (result == 'triple'):
                result = ' tripled off of '
            elif (result == 'home run'):
                result = ' homered off of '
            elif (result == 'flyout'):
                result = ' flied out off of '
            elif (result == 'sac bunt'):
                result = ' sac bunted off of '   
            elif (result == 'groundout'):
                result = ' grounded out off of '
            elif (result == 'forceout'):
                result = ' hit into a fielders choice off of '
            elif (result == 'pop out'):
                result = ' popped out off of '
            elif (result == 'field error'):
                result = ' reached on an error off of '
            elif (result == 'gidp'):
                result = ' grounded into a double play off of '
            elif (result == 'fan interference'): 
                result = ' hit into a fan interference off of '
            
            if (result != ''): 
                status = True
        
            tempResult.append(str(hitData[1]) + result + str(hitData[3]) + '.')
            tempResult.append('Pitch Velocity: ' + str(hitData[10]) + ' MPH.')
            tempResult.append('Exit Velocity: ' + str(hitData[7]) + ' MPH.')
            tempResult.append('Launch Angle: ' + str(hitData[8]) + ' deg.')
            tempResult.append('Distance: ' + str(hitData[9]) + ' ft.')
            tempResult.append(' #Nationals: ' + str(scoreN))
            tempResult.append(' #Astros: ' + str(scoreA))
#            tempResult.append('Hit Probability: ' + str(hitData[11]))
            tempResult.append(' #WorldSeries')
            tempResult.append(status)
            finalResult.append(tempResult)
  
        count += 1
    driver.close()
    scoreCurr = [scoreN, scoreA]
            
    return finalResult, scoreCurr

def runProgram (): 
    prev = ''
    wayback = ''
    third = ''
    scorePrev = ['0', '0']
    startTime = time.time()
    elapsedTime = time.time() - startTime
    
    while (elapsedTime < 15300):
        elapsedTime = time.time() - startTime
        status, scoreCurr = finalizeBIP ()
        time.sleep(10)
        print('\n')
        print(status)
        
        last = status[0]
        if (last[-1] == False): 
            continue
        tweet = ''
        
        if (scoreCurr != scorePrev): 
            tweet = ('Score Update: #Nationals: ' + str(scoreCurr[0]) + ' #Astros: ' + str(scoreCurr[1]) + ' #WorldSeries')
            scorePrev = scoreCurr
            third = wayback
            wayback = prev
            prev = last
        
            print('\n')
            print(tweet)
            api.update_status(tweet)
        
        else: 
            if (last != prev and last != wayback and last != third):
                for element in last[:-1]: 
                    tweet += element
                    tweet += ' '
                print('\n')
                print(tweet)
                api.update_status(tweet)
                third = wayback
                wayback = prev
                prev = last
            
                
runProgram()