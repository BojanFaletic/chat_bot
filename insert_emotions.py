from selenium import webdriver
from bs4 import BeautifulSoup
from emotions import Emotions
import re
import time
import random

URL = 'https://relatedwords.org/relatedto/'


def get_common_words():
    with open('top_1000_words.txt', 'r') as file:
        d = file.readlines()
    return [x.replace('\n', '') for x in d]

# starts browser
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# emotion structure
em = Emotions()

words = get_common_words()

for k, word in enumerate(words):
    driver.get(URL+word)
    # detection bypass
    time.sleep(random.randrange(1, 100)/1e3)

    d = driver.page_source
    soup = BeautifulSoup(d)

    s = soup.find_all(class_='item')

    # parse webpage for emotion and prob
    names = []
    for i in s:
        try:
            name = re.findall(r'">(.*)</', str(i))[0]
            prob = re.findall(r'rgb\((.*),', str(i))[0].split(',')[0]
            names.append({name: 1-int(prob)/255})
        except:
            break
    # insert word to dictionary
    for w in names:
        for key in list(em.emotions):
            if key in w:
                em.add_word(word, key, w[key])
                print('Adding: ', w)

    print("progress: ", k/len(words)*100, '%')

# end browser
em.save_dictionary('emotions.json')
driver.close()

print('Finshed!')