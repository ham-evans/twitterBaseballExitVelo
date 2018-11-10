from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
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

driver = webdriver.Chrome("/Users/hamevans/Downloads/chromedriver")

def runPrimer (driver):
    driver.get("https://baseballsavant.mlb.com/gamefeed?game_pk=563396&type=exit_velocity&chart_view=pitch&chart_type=sbp&inning=&count=&batter_hand=&pitcher_hand=&filter=")
    
    # waiting for the page to load - TODO: change
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "pitchVelocity-tr_4")))
    
    data = driver.page_source
    driver.close()
    
    soup = BeautifulSoup(data, "html.parser")
    
    allPitches = soup.find('div', id='pitchVelocity')
    individualPitches = allPitches.findAll('tr')
    totalPitchData = []
    
    for pitch in individualPitches:
        num = 0
        pitchData = []
        spans = pitch.findAll('span')
    
        for i in range(len(spans)):
            pitchData.append(spans[i].text) 
            if (spans[i] == spans[-1]):
                num += 1
                if (num == 3):
                    for information in pitchData: 
                        if ('In play' in information):
                            totalPitchData.append(pitchData)
                    break
    return totalPitchData 
    
 
def finalizeBIP (): 
    driver = webdriver.Chrome("/Users/hamevans/Downloads/chromedriver")
    driver.get('https://baseballsavant.mlb.com/gamefeed?game_pk=563411&type=exit_velocity&chart_view=pitch&chart_type=sbp&inning=&count=&batter_hand=&pitcher_hand=&filter=')
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "exitVelocity-tr_2")))
    
    data = driver.page_source
    driver.close()
    
    soup = BeautifulSoup(data, "html.parser")
    
    allExits = soup.find('div', id='exitVelocity')
    individualBIP = allExits.findAll('tr')
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
            
            if (result == 'lineout'):
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
            elif (result == ' sac fly '): 
                result = ' hit a sac fly off of '
            
            if (result != ''): 
                status = True
            tempResult.append(str(hitData[1]) + result + str(hitData[3]) + '.')
            tempResult.append('Pitch Velocity: ' + str(hitData[10]) + ' MPH.')
            tempResult.append('Exit Velocity: ' + str(hitData[7]) + ' MPH.')
            tempResult.append('Launch Angle: ' + str(hitData[8]) + ' deg.')
            tempResult.append('Distance: ' + str(hitData[9]) + ' ft.')
            tempResult.append('Hit Probability: ' + str(hitData[11]) + '%.')
            tempResult.append(status)
            finalResult.append(tempResult)
            
        count += 1
    return finalResult
        

def runProgram (): 
    prev = ''
    wayback = ''
    third = ''
    while True: 
        status = finalizeBIP ()
        time.sleep(10)
        print('\n')
        print(status)
        
        last = status[0]
        if (last[-1] == False): 
            continue
        tweet = ''
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
            
                
        