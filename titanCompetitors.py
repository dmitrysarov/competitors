# -*- coding: utf-8 -*-

import re
import urllib2
import selenium.webdriver as webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

inputFile = urllib2.urlopen('https://titan-race.ru/starts/2016-08-07/list')
inputFileContent = inputFile.read()
inputFileContent = re.findall(r'Спринт.+?(<table.+</table>).+?Эстафеты',inputFileContent,re.DOTALL)[0].decode('utf-8')
inputFile.close()
names = re.findall(r'<tr.+?<td>.*?</td><td>.*?</td><td>(\w*?)</td><td>(\w*?)</td>',inputFileContent,re.DOTALL|re.U)
names_list = [' '.join(list(n)) for n in names]
names_sub = [n.replace(' ', '%20') for n in names_list]
browser = webdriver.Firefox()
iron = []
halfIron = []
olimpic = []
for i in xrange(len(names)-1):
    browser.get('http://tristats.ru/profile.html?name=' + names_sub[i])
    try:
        WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH,'//a[contains(., ":")]')))
        page_source = browser.page_source.encode('utf8')
        iron.append(''.join(re.findall(r'best.IronmanResultId.+?result.+?(\d\d:\d\d:\d\d).+?best.IronmanResultId', page_source,re.DOTALL)))
        halfIron.append(''.join(re.findall(r'best.HalfIronmanResultId.+?result.+?(\d\d:\d\d:\d\d).+?best.HalfIronmanResultId', page_source,re.DOTALL)))
        olimpic.append(''.join(re.findall(r'best.OlympicResultId.+?result.+?(\d\d:\d\d:\d\d).+?best.OlympicResultId', page_source,re.DOTALL)))
    except:
        iron.append('')
        halfIron.append('')
        olimpic.append('')
    str1 = re.compile('(?P<a><td>' + names[i][0] + '</td><td>' + names[i][1] + '</td><td>.*?</td><td>.*?</td>)', re.DOTALL|re.U)
    inputFileContent = re.sub(str1, '\g<a><td> ir ' + iron[i] + '</td><td> hi' + halfIron[i] + '</td><td> ol ' + olimpic[i] + '</td>', inputFileContent)
browser.close()
with open('page_content.html', 'w') as fid:
    fid.write(inputFileContent.encode('windows-1251'))