# Replace "link" value with the downoald link from the tor site, and "file name" value with the name you want the file to be called on your computer
# Instantiate scraper with cloudscraper to bypass cloudflare protections, check to make sure safety protocols are active, download file with status bar

import json
import cloudscraper
import sys

# Initiate Scraper instance through tor with masked headers
class Instantiate_scraper:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper(interpreter='nodejs')
        self.scraper.proxies = {}
        self.scraper.proxies['http'] = 'socks5h://localhost:9050'
        self.scraper.proxies['https'] = 'socks5h://localhost:9050'
        self.headers = {}
        self.headers['User-agent'] = "Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0"

# Check to make sure tor is on, headers are set, and cookies are blocked
    def safety_check(self):
        self.request = self.scraper.get('http://httpbin.org/ip')
        self.on_tor = json.loads(self.request.text)
        self.request = self.scraper.get('http://httpbin.org/user-agent', headers=self.headers)
        self.headers = json.loads(self.request.text)


        self.safe = False
        if self.on_tor == {'origin': '207.237.138.82'}:
            self.safe = False
            print("you are not on Tor")
        elif self.on_tor == {'origin': '69.121.108.201'}:
            self.safe = False
            print("you are not on Tor")
        else:
            if self.headers != {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}:
                self.safe = False
                print("you do not have anonymized headers")
            else:
                self.safe = True
        return self.safe

def start_download():
    link = 'Tor link of file to get here'
    file_name = "name you want for the file you're downloading"
    with open(file_name, "wb") as f:
        print("Downloading %s, Status:" % file_name)
        scraper = Instantiate_scraper()
        scraper = scraper.scraper
        response = scraper.get(link, stream=True, headers=scraper.headers)
        total_length = response.headers.get('content-length')
        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                sys.stdout.flush()


# Execute script
scraper = Instantiate_scraper()
if scraper.safety_check() == True:
    print("You are on Tor, connecting to Maze.")
    print("Beginning file download, please wait, this may take a while.")
    start_download()
    print("Download is complete")



