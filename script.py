from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import urllib
import re

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


driver = webdriver.Firefox()					#firefox chosen as browser for selenium
driver.implicitly_wait(5)    					#will wait for 5 sec

isnextdisabled=0    							#flag to check if next link in the url is disabled or not

website_url="http://trai.gov.in"				#url of website to be scraped
check_anchor_url="/Content/PressDetails"		
next_id = "ctl00_ContentPlaceHolder1_lbtnNext"	#value of id attribute needed for scraping
no_of_documents_downloaded=0					#counter to count no of files downloaded

driver.get('http://trai.gov.in/Content/PressReleases.aspx')	
html = driver.page_source
source_code_1 = BeautifulSoup(html)

while source_code_1.find(id=re.compile(next_id)) and isnextdisabled==0 :	#loop will run until my next vutton will be there on html page should not be disabled

	for a in source_code_1.find_all('a'):					
		if a.has_attr("href"):
			if check_anchor_url in a['href']:
				print("selected href value is",a['href'])
				
				try:
					driver.find_element_by_xpath('//a[@href="'+a['href']+'"]').click()
				except NoSuchElementException:
					print("exception")
				
				driver_back_flag=1
				source_code_2 = BeautifulSoup(driver.page_source)
					

				for b in source_code_2.find_all('a', href=True):
					if b.has_attr("title"):
						if(b['title']=='Click here to download'):					#downloading the pdf
	  						full_url_2=website_url+b['href']
	  						print ("Found the URL:", full_url_2)
	  						
	  						split_array=[]
	  						split_array=b['href'].split('/')
	  						
	  						print("pdf name:",split_array[4])
	  						urllib2.urlretrieve(full_url_2,split_array[4])
	  						no_of_documents_downloaded=no_of_documents_downloaded+1;
	  						print("No of Documents Downloaded:",no_of_documents_downloaded)
	  						print("\n")
	  						driver.back()
	  						driver_back_flag=0
	  						break
				
				if(driver_back_flag==1):		#if pdf was not downloaded, go back to previous page
	  				driver.back()
	  				print("pdf not downloaded")			
		
		if a.has_attr("disabled"):				#if link is disabled update the flag value so that loop can be stopped
			if(a['id']==next_id):
				#driver.close()
				isnextdisabled=1


	driver.find_element_by_id(next_id).click()
	html = html + driver.page_source
	source_code_1 = BeautifulSoup(driver.page_source)
driver.close()		