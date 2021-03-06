# -*- coding: utf-8 -*-

import re
import urllib2
import selenium.webdriver as webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


inputFile = urllib2.urlopen('http://iron-star.com/event/ironstar_113_kazan/')
inputFileContent = inputFile.read()
inputFileContent = re.findall(r'<table class="competitors__table uchastnik_estafet".+?</table>\s*\n\s*<h3',inputFileContent,re.DOTALL)[0]
inputFile.close()
names = re.findall(r'<td class="competitors__name">([\w\s]+)</td>',inputFileContent,re.DOTALL)
names_sub = [n.replace(' ', '%20') for n in names]
browser = webdriver.Firefox()
iron = []
halfIron = []
olimpic = []
for i in xrange(len(names)-1):
    browser.get('http://tristats.ru/profile.html?name=' + names_sub[i])
    try:
        WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH,'//a[contains(., ":")]')))
        page_source = browser.page_source.encode('utf8')
        iron.append(''.join(re.findall(r'best.IronmanResultUrl.+?result.+?(\d\d:\d\d:\d\d)</a>.+?best.IronmanResultUrl', page_source,re.DOTALL)))
        halfIron.append(''.join(re.findall(r'best.HalfIronmanResultUrl.+?result.+?(\d\d:\d\d:\d\d)</a>.+?best.HalfIronmanResultUrl', page_source,re.DOTALL)))
        olimpic.append(''.join(re.findall(r'best.OlympicResultUrl.+?result.+?(\d\d:\d\d:\d\d)</a>.+?best.OlympicResultUrl', page_source,re.DOTALL)))
    except:
        iron.append('')
        halfIron.append('')
        olimpic.append('')
    str1 = re.compile('(?P<a><td.*?>' + names[i] + '</td>.*?<td.*?>.*?</td>)', re.DOTALL)
    inputFileContent = re.sub(str1, '\g<a><td> ir ' + iron[i] + '</td><td> hi' + halfIron[i] + '</td><td> ol ' + olimpic[i] + '</td>', inputFileContent)
browser.close()
with open('ironStarRelay.html', 'w') as fid:
    fid.write(inputFileContent.decode('utf-8').encode('windows-1251'))