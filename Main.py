from selenium import webdriver
from time import sleep
import urllib.request
from selenium.webdriver.common.keys import Keys
import requests
import bs4
import webbrowser
from selenium.webdriver.common.by import By
import random
import datetime as dt
import newyork as NY
import base64


class Tripadvisor():

	def __init__(self):

		print('START TIME: ', dt.datetime.now())
		print('LIST SIZE: ',len(NY.newyork))
		chrome_options = webdriver.ChromeOptions()
		#chrome_options.add_argument("--headless")  
		self.driver = webdriver.Chrome(executable_path=r'chromedriver_win32/chromedriver.exe', chrome_options=chrome_options)
		self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0)'}
		url = self.driver.get('https://www.tripadvisor.com/Restaurants/')
		self.res = requests.get(self.driver.current_url, headers=self.headers)
		self.res.raise_for_status()
		self.soup = bs4.BeautifulSoup(self.res.text, 'html.parser')
		self.Linklist = []

	def get_urls(self,places):
		print('GETTING THE URLS')
		if self.driver.get(self.driver.current_url) != 'https://www.tripadvisor.com/':
			self.driver.get('https://www.tripadvisor.com/')
		#-------------------------------------------------------------click resteraunt button------------------------------------------------------------- 
		CRSST = self.driver.find_element_by_xpath('//*[@id="lithium-root"]/main/div[1]/div[1]/div/div/div[4]/a')
		CRSST.click()	
		sleep(2)

		#-------------------------------------------------------------selectwords to type over-------------------------------------------------------------
		try:
			STWI = self.driver.find_element_by_xpath('/html/body/div[2]/div/form/input[1]')
			STWII.click()
		except:
			pass
		sleep(2)
		#-------------------------------------------------------------type where you are looking for-------------------------------------------------------------
		location = places

		try:
			self.driver.find_element_by_xpath('/html/body/div[2]/div/form/input[1]').send_keys(location)
			sleep(2)
		except:
			print('THIS ONE BROKE: '+str(location))
			
		#-------------------------------------------------------------search-------------------------------------------------------------
		try:
			self.driver.find_element_by_xpath('/html/body/div[2]/div/form/div/a[1]').click()
			sleep(3)		
		except:
			print('This city sucks ass nun here.')
			pass

		counter = 1
		#-------------------------------------------------------------this part gets urls-------------------------------------------------------------
		next_page_link = self.driver.current_url
		going = True
		while going == True:
			
			self.res = requests.get(next_page_link)
			self.res.raise_for_status()
			self.soup = bs4.BeautifulSoup(self.res.text, 'html.parser')
			for a in self.soup.find_all("a", {'_15_ydu6b'}):
				href = a.get('href')
				self.Linklist.append(href[:-5])
				with open("newyork_urls.txt", "a") as chk:
					chk.write(str(href[:-5])+'\n')

			#-------------------------------------------------------------hits next button-------------------------------------------------------------
			try:
				nextbutton = self.soup.find("a", {"class":"nav next rndBtn ui_button primary taLnk"})
				nextbuttonhref = nextbutton.get('href')
				next_page_link = 'https://www.tripadvisor.com'+str(nextbuttonhref)
			except:
				going = False
			#-------------------------------------------------------------done-------------------------------------------------------------
		print('LINKS SO FAR: ',len(self.Linklist))
		print('FINNISHED WITH '+str(location))


	def get_data(self):

		textfile =  open("newyork_urls.txt", "r")
		for line in textfile:
			self.Linklist.append(line)

		self.Linklist = set(self.Linklist)

		print('LEN OF LINKS: ',len(self.Linklist))
		print('STARTING THE SCRAPING THIS MAY TAKE SOMETIME TIME...')
		new_list = []
		for i in self.Linklist:
			new_list.append(i)
		

		counter = 0
		for i in new_list:
			try:
				counter+=1
				self.driver.get('https://www.tripadvisor.com'+str(i))
				self.res = requests.get(self.driver.current_url)
				self.res.raise_for_status()
				self.soup = bs4.BeautifulSoup(self.res.text, 'html.parser')
	
				#-------------------------------------------------------------name-------------------------------------------------------------
				name = 'N/A'
				try:
					h1 = self.soup.find('h1',{'class':'_3a1XQ88S'})
					h1 = h1.text
					name = h1
				except:
					pass
				#-------------------------------------------------------------email and phone-------------------------------------------------------------
				try:
					email = 'N/A'
					phone = 'N/A'
					for div in self.soup.find_all('div',{'class':'_36TL14Jn'}):
						a = div.find('a')
						if a.get('href') == None:
							pass
						elif a.get('href')[:3].lower() == "tel":
							phone = a.get('href')[4:]
						elif a.get('href')[:4].lower() == "mail":
							email = a.get('href')[7:]
				except:
					pass
				#-------------------------------------------------------------website-------------------------------------------------------------
				try:
					website = 'N/A'
					for div in self.soup.find_all('div',{'class':'_36TL14Jn _3jdfbxG0'}):
						x = div.find('a')
						if x.get('data-encoded-url') is not None:
							decoded = base64.b64decode(x.get('data-encoded-url'))
							website = str(decoded[4:])
							#print(decoded[4:])
				except:
					pass
				#-------------------------------------------------------------rating-------------------------------------------------------------
				try:
					rating = self.soup.find('span',{'class':'r2Cf69qf'})
					rating = rating.text
					#print(rating.text)
				except:
					pass

				with open("newyork_data.txt", "a") as chkc:
					chkc.write(str(name)+','+str(email)+','+str(phone)+','+str(website)+','+str(i)+'\n')
				print("TASK "+str(counter)+"/"+str(len(new_list)))
			except:
				print('THERE WAS A PROBLEM CONNECTING TAKING A BREAK')
				sleep(500)
				#cali_data.write('THIS GOT MESSED UP'+','+'N/A'+','+'N/A'+','+'N/A'+','+i+'\n')
			

		self.driver.quit()

Bot = Tripadvisor()
list_length = len(NY.newyork)
for The_local in range(list_length):
	Bot.get_urls(NY.newyork[The_local])

Bot.get_data()
#you have to do a special bot for los angeles
#https://www.tripadvisor.com/RestaurantSearch-g55197-oa30-Memphis_Tennessee.html#EATERY_LIST_CONTENTS