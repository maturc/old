"""Calls rss_parser and checks if the last release was already posted or now, by writing to a file."""

from rss_parser import getRss

def getRelease():
    try:
        with open('last_release.txt', 'r+') as f:
            title, link = getRss()
            release = title + " " + link
            r = f.read()
            if(r!=release):
                f.seek(0)
                f.truncate()
                f.write(release)
                return release
    except Exception as e:
        print(str(e))
