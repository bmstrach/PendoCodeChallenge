#!/usr/bin/python
# Coding Challenge

# Python version
# Python 2.7.10

# This script is with pip and selenium webdriver already installed
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import sys
import time
import traceback

# Note:
# Versions this script was developed on
# Python - 2.7.10
# Selenium - 3.4.2
# Command used: sudo easy_install --record=selenium_installed_files selenium
# Chrome Webdriver - ChromeDriver 2.29
# Source for webdriver: https://chromedriver.storage.googleapis.com/index.html?path=2.29/

# To run this script:
# First I ran
# sudo easy_install --record=selenium_installed_files selenium
# Then I downloaded the Chrome WebDriver
# I unzip'd the file and placed the chromedriver executable in the same directory as my script
# chromedriver.exe
# Command used to run script:
# In directory of script
# python HackySack2.py


# Max wait time for elements to appear on page
MAX_WAIT = 60


if __name__ == '__main__':
    
    # First get PATH and save it in it's current state
    orig_PATH = os.environ["PATH"]
    
    # The chromedriver executeable is set to be located in the
    # same path as the script
    chrome_exe_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    
    # We add the path of the chrome executeable to the PATH environment
    # variable so that the selenium web driver can find it.
    os.environ["PATH"] = orig_PATH + ":" + chrome_exe_path
    
    try:
        browser = webdriver.Chrome()
        print 'Let\'s Google'
        browser.get("http://www.google.com")
        
        print 'Status: Querying for hacky sack'
        # Found search text box element:
        # <input class="gsfi" id="lst-ib" maxlength="2048" name="q" autocomplete="off" title="Search" type="text" value="" aria-label="Search" aria-haspopup="false" role="combobox" aria-autocomplete="both" style="border: none; padding: 0px; margin: 0px; height: auto; width: 100%; background: url(&quot;data:image/gif;base64,R0lGODlhAQABAID/AMDAwAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw%3D%3D&quot;) transparent; position: absolute; z-index: 6; left: 0px; outline: none;" dir="ltr" spellcheck="false">
        
        search = WebDriverWait(browser, MAX_WAIT).until(EC.presence_of_element_located((By.NAME, "q")))
        
        search.send_keys("hacky sack\n")
        
        print 'Status: Waiting for Shopping link'
        # Example of element for 'Shopping' link
        #<div class="hdtb-mitem hdtb-imb"><a class="q qs" href="/search?q=hacky+sack&amp;biw=582&amp;bih=767&amp;source=lnms&amp;tbm=shop&amp;sa=X&amp;ved=0ahUKEwj_qMHs3YrUAhUHJCYKHeDaDuoQ_AUIBigB">Shopping</a></div>
        
        shopping = WebDriverWait(browser, MAX_WAIT).until(EC.presence_of_element_located((By.XPATH, "//*[@id='hdtb-msb-vis']/div[2]/a")))
        
        # Click shopping
        shopping.click()
        print 'Status: On Shopping page'
        print 'Status: Waiting to pick fourth element'


        # Get the 4th shopping result
        # //*[@id="rso"]/div[1]/div/div[4]/div[1]/div[1]/a
        fourth_element = WebDriverWait(browser, MAX_WAIT).until(EC.presence_of_element_located((By.XPATH, "//*[@id='rso']/div[1]/div/div[4]/div[1]/div[1]/a")))
        
        # TODO: I understand that my try-except will catch exceptions such as element not found.
        # But ideally, I would have had an error check for elementNotFound to indicate a fourth shopping result was
        # not found
        
        # Change the other thing to do this
        fourth_element.click()
        print 'Status: Clicked fourth element'
        
        print 'Status: Waiting for \'Save to Shortlist\' button now!'
        
        
        # <div class="pspo-popout pspo-gpop" data-docid="2585490548763619672"><div class=""><div class="sh-dp__arrow" >
        # //*[@id="rso"]/div[1]/div/div[7]
        # //*[@id="rso"]/div[1]/div/div[7]/div/div[2]/div/div[2]/div[3]/div[4]/div[2]/div - button
        
        # Here is where I got stuck. I checked the xpath for the 'Save to Shortlist' button and this is the XPATH I found.
        # I even compared a session I had while signed in with the session from the test run, both buttons had this xpath
        # I understand using this method, there are times the DOM could not be fully loaded, so you should wait before looking
        # for element. I have played around with multiple timeouts, and the document seems to time out before finding the
        # element. I also used class to look for this element "div.gko-a.ksb.gko-add".
        # I also checked to make sure the driver was not expecting to search on a different window.
        # Was unable to pinpoint my error in allotted time.
        # Example of div element found:
        # <div class="gko-a ksb gko-add" data-cid="11534225610171718711" data-country="US" data-docid="" data-lang="en" data-mid="105495024" data-rmoid="woocommerce_gpf_4138" data-tmo="2060768686429941555,10187121746673456822,6699567025630811168" data-ved="0ahUKEwjBwdfN84rUAhUJbiYKHScZAlYQpi0IJw" jsaction="gksp.ti;keydown:gksp.so" role="button" tabindex="0"><div class="_-5"></div><div class="gko-a-lbl">Save to Shortlist</div></div>
        # save_to_shortlist = WebDriverWait(browser, 240).until(EC.presence_of_element_located((By.XPATH, "//*[@id='rso']/div[1]/div/div[7]/div/div[2]/div/div[2]/div[3]/div[4]/div[2]/div")))
        # save_to_shortlist.click()
        
        # I even tried to do the nearest parent and it cannot seem to find that element either.
        # So I was unable to pinpoint exactly what was happening to where the element could not be located
        save_to_shortlist = WebDriverWait(browser, 240).until(EC.presence_of_element_located((By.XPATH, "//*[@id='rso']/div[1]/div/div[7]/div/div[2]/div/div[2]")))
        
        list = save_to_shortlist.find_elements_by_xpath("//*[@role = 'button']")
        # Also not sure if Save to Shortlist button is last element
        list[-1].click()
        
        print 'Status: ShortList button clicked!'
        
        # Seems that Add note is only for people who are signed in
        # Not sure if this was suppose to be a user signed in or not
        # Found xpath for the Add Note button, but it seems to change bubble ids
        # so needed to sort out how to find this element. For instance, I ran the workflow twice
        # and got the following xpath values:
        # //*[@id="bubble-20"]/div[2]/div[2]/div[2]/div[2]/div[1]
        # //*[@id='bubble-11']/div[2]/div[2]/div[2]/div[2]/div[1]
        # Here is also an example of the div element found:
        # <div class="sh-gc__c-sa" jsaction="gksp.csca" tabindex="0">Add note</div>
        
        # Here was the possible code:
        # add_note = browser.find_element_by_xpath("//*[@id='bubble-11']/div[2]/div[2]/div[2]/div[2]/div[1]")
        # add_note.click()
        # print 'Status: add note clicked!'
        
        # Give some time to see status of page
        time.sleep(10)
        
    except:
        # We catch the exception so that we can continue if any exceptions occur.
        traceback.print_exc()

    # Exit browser here to conclude test
    browser.close()
    # Before we exit - update PATH to original value
    os.environ["PATH"] = orig_PATH
