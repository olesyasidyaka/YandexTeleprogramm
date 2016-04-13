#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import lxml.html as html
import io, json
import datetime
import codecs
import re

json_string = ''
data = dict()

def weekdayToString(weekday):
	return {
		0: u"Пн",
		1: u"Вт",
		2: u"Ср",
		3: u"Чт",
		4: u"Пт",
		5: u"Сб",
		6: u"Вс",
		'today': u"Сегодня"
	}[weekday]

def readDay(ind, link, day, weekday):
	connection = urllib.urlopen(link)
	st = connection.read()
	connection.close()
	page = html.fromstring(st)
	channels = page.cssselect('.tv-channel')
	
	file = codecs.open('page' + str(ind) + '.html', "w")#, "utf-8")
	file.write(st)
	file.close()
	
	global data
	data[ind] = dict()
	data[ind]['date'] = day
	data[ind]['weekday'] = weekdayToString(weekday)
	data[ind]['channels'] = []

	for row in channels:
		item = dict()
		item['channel'] = row.cssselect('.tv-channel-title__text')[0].text_content()
		style = row.cssselect('.b-tv-image__picture')[0].get("style").replace("url(", "url(http:")
		item['icon'] = "http://" + style[style.find("avatars"):-1]
		item['programs'] = []
		if (len(row.cssselect('.tv-channel-events__items')) != 0):
			pr = row.cssselect('.tv-channel-events__items')[0]
			time = pr.cssselect('.tv-event__time-text')
			prog = pr.cssselect('.tv-event__title-inner')
			genre = pr.cssselect('.tv-event')
			for p in range(0, len(time)):
				m = re.match(r'.*"genre":"(.*)"', genre[p].get('data-bem')).group(1)
				item['programs'].append([time[p].text_content(), prog[p].text_content(), m])
		
		data[ind]['channels'].append(item)


	# global json_string
	# json_string += json.dumps({"data":data[day]}, indent=4, ensure_ascii = False).encode('utf-8')

now = datetime.datetime.now()
links = {'today': ["https://tv.yandex.ru/213?grid=main&period=all-day", now.strftime("%d"), now.weekday()]}
one_day = datetime.timedelta(days=1)
for i in range(1, 7):
	now += one_day
	links[i] = ["https://tv.yandex.ru/213?date=" + now.strftime("%Y-%m-%d") + "&grid=main&period=all-day", now.strftime("%d"), now.weekday()]

for k, v in links.iteritems():
	readDay(k, v[0], v[1], v[2])

with open('data_week.json', 'w') as outfile:
	json_string = json.dumps({"data":data}, indent=4, ensure_ascii = False).encode('utf-8')
	outfile.write(json_string)

