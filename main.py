#!/usr/bin/env python
# global imports
import sys, argparse, time 
from configparser import SafeConfigParser
from splinter import Browser
from worgen import randomword

class Colors:

    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

blue = Colors.BLUE
green = Colors.GREEN
yellow = Colors.YELLOW
red = Colors.RED
end = Colors.END

# config parser
parser = SafeConfigParser()
parser.read('maggie.config')

if parser.has_option('credentials', 'username') and parser.has_option('credentials', 'password') and \
        parser.has_option('portus', 'version'):
    username = parser.get('credentials', 'username')
    password = parser.get('credentials', 'password')
    version = parser.get('portus', 'version')
    repaddr = parser.get('portus', 'repaddress')
else:
    print('You need to configure maggie.config first')
    sys.exit(1)

# argument parser
parser = argparse.ArgumentParser(description="Portus autotestsuite, run it via 'maggie -a <address> -p <port>'")
parser.add_argument('address',
        help = "portus address, for example 192.168.0.2")
parser.add_argument('port',
        help = "portus port, for example 80, 3000")
args = parser.parse_args()
user_address = args.address
user_port = args.port

startTime = time.time()

## test browser
# browser = Browser('chrome')
## prodcution browser
browser = Browser('phantomjs', service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
browser.driver.set_window_size(1920 ,1080)
url = "https://" + user_address + ":" + user_port 
browser.visit(url)
browser.find_by_id('user_username').first.fill(username)
browser.find_by_id('user_password').first.fill(password)
browser.find_by_name('button').first.click()

# main class
class Checker(object):

    def __init__(self, browser):
        
        self.browser = browser
        self.errors = 0
        self.success = 0

    def chktext(self, text):
        """ check if text is present and visible on the page """ 
        if self.browser.is_text_present(text):
            print("%-55s %s" % (text, green + 'PASSED' + end))
            self.success += 1
        else:
            print("%-55s %s" % (text, red + 'FAILED' + end))
            self.errors += 1
    
    def openpage(self, link, text):
        """ open a new page in the same window, and check if some text 
        exists """ 
        self.browser.click_link_by_partial_href(link)
        self.chktext(text)
    
    def clicklink(self, link):
        """ click on the particular link on the web page """
        self.browser.click_link_by_partial_href(link)
    
    def clickid(self, id):
        """ click on the particular link (by id) on the web page """
        self.browser.find_by_id(id).first.click()
    
    def clickname(self, name):
        """ click on the particular link (by name) on the web page """ 
        self.browser.find_by_name(name).first.click()

    def findlink(self, link):
        """ find particular element on the page """
        if  self.browser.find_link_by_partial_href(link):
            print("%-55s %s" % (link, green + 'PASSED' + end))
            self.success += 1
        else:
            print("%-55s %s" % (link, red + 'FAILED' + end))
            self.errors += 1
    
def section_output(uline, title): 
    """ print the name of the section plus divided line """ 
    print()
    print(title)
    print(len(title) * uline)

### test runners
ck = Checker(browser)

# 1) check if version of portus is correct (see .conf file for more info
section_output('*', 'Portus version')
ck.chktext(version)

# 2) - 5)  check every available section on the left side of the main page 
section_output('*', 'Main page tests')
time.sleep(1)
ck.chktext(username)
for i,k in (('/', 'Recent activities'), 
        ('/namespaces', 'Special namespaces'),
        ('/teams', 'Teams you are member of'), 
        ('/admin/dashboard', 'Recent activities')):
    try:
        ck.openpage(i, k)
    except:
        browser.driver.save_screenshot('screenshot.png')
# go back to the main page
ck.clicklink('/')

# 6) - 8) check Repositories section on the main page
section_output('-', 'Repositories section tests')
time.sleep(1)
ck.chktext('Repositories')
time.sleep(1)
for link in ('#all', '#starred', '#personal'):
    ck.findlink(link)

# 9) Team section tests
section_output('*', 'Team section tests')
time.sleep(1)
ck.clicklink('/teams')
ck.clickid('add_team_btn')
time.sleep(1)
browser.find_by_id('team_name').first.fill(randomword)
time.sleep(1)
browser.find_by_id('team_description').first.fill('QAM team')
ck.clickname('commit')
time.sleep(1)
ck.chktext(randomword)
# 10) check that our acitivity is visible on the main page
time.sleep(1)
ck.openpage('/', username + ' created team ' + randomword)

# 11) Namespaces section test
section_output('*', 'Namespaces section tests')
time.sleep(1)
ck.clicklink('/namespaces')
time.sleep(1)
ck.clickid('add_namespace_btn')
time.sleep(1)
browser.find_by_id('namespace_namespace').first.fill(randomword)
time.sleep(1)
browser.find_by_id('namespace_team').first.fill(randomword)
time.sleep(1)
browser.find_by_id('namespace_description').first.fill('Qam test ' + randomword)
ck.clickname('commit')
time.sleep(1)
ck.chktext(randomword)
# 12) check that our activity is visible on the main page
time.sleep(1)
ck.openpage('/', username + ' created the ' + randomword + ' namespace under the ' + randomword + ' team')

# 13) Namespace section: check Private - Public namespace functionality
section_output('-', 'Check private-public button functionality')
time.sleep(2)
ck.clicklink('/namespaces')
time.sleep(1)
browser.find_link_by_partial_href('/namespaces/').last.click()
# 14) check that our activity is visible on the main page
time.sleep(1)
ck.openpage('/', username + ' set the ' + randomword + ' namespace as public')

# 15) Namespace section check Public - Private namespace functionality
section_output('-', 'Check Public-private button functionality')
time.sleep(1)
ck.clicklink('/namespaces')
time.sleep(1)
browser.find_link_by_partial_href('/namespaces/').last.click()
# check that our activity is visible on the main page
time.sleep(1)
ck.openpage('/', username + ' set the ' + randomword + ' namespace as private')

section_output('*', 'Summary')
print(blue + 'Ran: ' + str(ck.errors + ck.success) + ' tests' + end)
print(green + 'Successes: ' + str(ck.success) + end)
print(red + 'Errors: ' + str(ck.errors) + end)
print(yellow + 'It took: {0:0.1f} seconds'.format(time.time() - startTime) + end) 

