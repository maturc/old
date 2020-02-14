"""Gets the RSS and parses it."""

import re
import requests
import html

def getRss():
    try:
        feed = requests.get('rss_adress')
        text = html.unescape(feed.text)

        try:
            titles=re.findall(r'<title>(.*?)</title>', text)
            links=re.findall(r'<link>(.*?)</link>', text)
			return (titles[0], links[1])
			
		except Exception as e:
			print(str(e))	
		
	except Exception as e:
		print(str(e))
