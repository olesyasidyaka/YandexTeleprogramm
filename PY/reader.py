import urllib
import lxml.html as html
import io, json

link = "https://tv.yandex.ru/213?grid=main&period=all-day"
page = html.fromstring(urllib.urlopen(link).read())
channels = page.cssselect('.tv-channel')

data = []

for row in channels:
	item = dict()
	item['channel'] = row.cssselect('.tv-channel-title__text')[0].text_content()
	style = row.cssselect('.b-tv-image__picture')[0].get("style").replace("url(", "url(http:")
	item['icon'] = "http://" + style[style.find("avatars"):-1]
	pr = row.cssselect('.tv-channel-events__items')[0]
	time = pr.cssselect('.tv-event__time-text')
	prog = pr.cssselect('.tv-event__title-inner')
	item['programs'] = []
	for p in range(0, len(time)):
	 	item['programs'].append([time[p].text_content(), prog[p].text_content()])
	data.append(item)

with open('data.json', 'w') as outfile:
	json_string = json.dumps({'channels':data}, indent=4, ensure_ascii = False).encode('utf-8')
	outfile.write(json_string)

