#!/usr/bin/env python3

import sys
import time
import random
import argparse
from tqdm import tqdm
from datetime import datetime
from googlesearch import search


colors = True
machine = sys.platform # Detecting the os of current system
if machine.lower().startswith(('os', 'win', 'darwin', 'ios')):
    colors = False # Colors will not be displayed in mac & windows
if not colors:
    end = red = white = green = yellow = ""
else:
    white = "\x1b[97m"
    green = "\x1b[92m"
    red = "\x1b[91m"
    end = "\x1b[0m"
    yellow = "\x1b[93m"


banner = f"""{red}
╭━━━╮╱╱╭╮╱╱╱╭╮
┃╭━╮┣┳┳╯┣━┳┳┫┣╮
┃┃┃┃┣┃┫╋┃╋┃╭┫━┫
┃┃┃┃┣┻┻━┻━┻╯╰┻╯
┃╰━╯┃
Disclaimer{white}:
This tool was developed for educational purposes and should not be used in environments
without {red}legal authorization{white}.
Therefore, the author shall {red}not{white} be responsible for the damages that might be done with it.{end}
"""


user_agents = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
                           "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4091.2 Safari/537.36",
                           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                           "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
                           "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.90 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                           "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                           "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
                           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71",
                           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
                           "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
                           "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36,gzip(gfe)",
                           "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
                           "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/7.0.185.1002 Safari/537.36",
                           "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36 OPR/52.0.2871.99",
                           "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
                           "Mozilla/5.0 (Linux; Android 11; SM-M115F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
                           "Mozilla/5.0 (Linux; Android 8.0.0; SM-A750GN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
                           "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) GSA/169.1.385914506 Mobile/15E148 Safari/604.1",
                           "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1",
                           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
                           "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36/swoLZb83-26")
                           

def dork():
    start = datetime.now()
    parser = argparse.ArgumentParser(description=f"""{red}ox{white}Dork (Google dorking tool) : OXDORK uses Google dorking techniques and Google dorks to find security holes and misconfigurations in web servers. || {red}https://github.com/{white}rlyonheart{end}""")
    parser.add_argument("query", help=f"{white}search query{end}")
    parser.add_argument("-c","--count",help=f"{white}number of results to return ({yellow}default is 50{white}){end}",dest="count", metavar="NUMBER", default=50)
    parser.add_argument("-o","--outfile",help=f"{white}write results to a file{end}",dest="output", metavar="FILENAME")
    parser.add_argument("-v", "--verbose", help=f"{white}run {red}oxdork{white} in verbose mode{end}", dest="verbose", action="store_true")
    args = parser.parse_args()
    number = 0
    counter = 0
    if args.verbose:
    	print(banner)
    	print(f"{white}* Fetching dorks [query={green}{args.query}{white}] [dorks_count={red}{args.count}{end}{white}]...{end}")
    while True:
        try:
        	google_search = search(args.query, num=int(args.count),start=0,stop=None,lang="en",tld="com", pause=2.5,
        	user_agent=f"{random.choice(user_agents)}")
        	for result in tqdm(google_search):
        		counter+=1
        		print(f"{white}[{counter}] oxdork:: [query={green}{args.query}{white}] {green}{result}{end}")
        		if args.output:
        			output(args,result)
        			
        		time.sleep(0.05)
        		number += 1
        		if number >= int(args.count):
        		    break
        	if args.verbose:
        		exit(f"{white}* Stopped [seconds={red}{datetime.now()-start}{white}]{end}")
        	break
        except KeyboardInterrupt:
        	if args.verbose:
        		exit(f"{white}* Process interrupted [{red}Ctrl{white}+{red}C{white}].{end}")
        	break
        
        except Exception as e:
        	if args.verbose:
        		print(f"{white}* Error [query={red}{args.query}{white}]: {red}{e}{end}")
        		print(f"{white}* Retrying [query={green}{args.query}{white}]...{end}")
        		
        		
def output(args,result):
    with open(args.output, "a") as file:
    	file.write(f"{result}\n")
    	file.close()
    	if args.verbose:
    		print(f"{white}* result(s) written to ./{red}{args.output}{end}")		

if __name__ == "__main__":
	dork()