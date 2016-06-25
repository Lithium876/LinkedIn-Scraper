import timeit, time, os, re
from os import system
from selenium import webdriver
from easygui import passwordbox
from xlwt import Workbook
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

new_tab=webdriver.PhantomJS("C:\Program Files (x86)\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\\bin\phantomjs.exe")
new_tab.set_window_size(1024, 768)

name=[]
size=[]
industry=[]
location=[]
system("title "+"LinkedIn Bot")

a = re.compile('&page_num=\d+')
b = re.compile('&page_num=\d+&')
c = '+ employees'

def write(name,col1, location, col2, size, col3, industry, col4):
    file=input("\nEnter file name: ")
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    sheet1.write(0,0,"Company Name")
    sheet1.write(0,1,"Address")
    sheet1.write(0,2,"Company Size")
    sheet1.write(0,3,"Industry")
    sheet1.col(0).width = 6000
    sheet1.col(1).width = 6000
    sheet1.col(2).width = 6000
    sheet1.col(3).width = 6000

    for i in range(len(name)):
        sheet1.write(i+1,col1,name[i])
        sheet1.write(i+1,col2,location[i])
        sheet1.write(i+1,col3,size[i])
        sheet1.write(i+1,col4,industry[i])
    wb.save(file+'.xls')

def scrape(url):
	new_tab.get(url)
	try:
		new_tab.find_element_by_xpath("""//*[@id="stream-about-section"]/div[2]/button[1]/span""").click()
	except:
		print("Not there")
	try:										
		name1 = new_tab.find_element_by_xpath("""//*[@id="stream-promo-top-bar"]/div[2]/div[1]/div[1]/div/h1/span""")
		name.append(name1.text)
	except:
		name.append("n/a")
		print("Error")
	try:	
		industry1 = new_tab.find_element_by_xpath("""//*[@id="stream-about-section"]/div[2]/div[2]/ul/li[2]/p""")
		industry.append(industry1.text)
	except:
		industry.append("n/a")
		print("Error")
	try:	
		location1 = new_tab.find_element_by_xpath("""//*[@id="stream-about-section"]/div[2]/div[2]/ul/li[4]/p""")
		if c in location1.text:
			location.append("n/a")
		else:
			location.append(location1.text)
	except:
		print("Error")
	try:	
		size1 = new_tab.find_element_by_xpath("""//*[@id="stream-about-section"]/div[2]/div[2]/ul/li[5]/p""")
		if c not in size1.text:
			size.append("n/a")
		else:
			size.append(size1.text)
	except:
		print("Error")

def crawl(curr,max_page,url):
	while True:
		try:
			os.system('cls')
			page = curr
			while page <= max_page:
		  		browser.get(url+"&page_num="+str(page))
		  		print("Page: "+str(page))
		  		print("Scarping...\n")
		  		start=timeit.default_timer()
		  		url_links =[]
		  		for i in range(1,11):
		  			links = browser.find_elements_by_xpath("""//*[@id="results"]/li["""+str(i)+"""]/div/h3/a""")
			  		for link in links:
			  			url_links.append(link.get_attribute('href'))
			  			scrape(url_links[i-1])
			  	estimate=timeit.default_timer() - start
			  	print("\n\n[+]Scarping Page "+str(page)+" Completed\n")
			  	page+=1
			  	print("Estimated Time: "+ str(round(estimate,3)))
			write(name,0, location, 1, size, 2, industry, 3)
			print("Success!")
			input()
			break
		except:
			print("Something went wrong, try again")
			search()

def login(email,passwrd):
	global browser 
	browser=webdriver.PhantomJS("C:\Program Files (x86)\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\\bin\phantomjs.exe")
	browser.set_window_size(1024, 768)
	browser.implicitly_wait(600)
	browser.get("https://linkedin.com/uas/login")
	try:
		browser.find_element_by_id("session_key-login").send_keys(email + Keys.TAB)
		browser.find_element_by_id("session_password-login").send_keys(passwrd + Keys.RETURN)
		print("\n[+] Success! Logged In, Bot Starting!")
		time.sleep(1)
		os.system('cls')
		search()
	except:
		print("[-] Error In Login, Incorrect Email or Password")
		Main()
	
def search():
	while True:
		try:
			url=input("Enter URL: ")
			checkurl=a.search(url)
			checkurl1=b.search(url)
			s=int(input("\nStart Page: "))
			e=int(input("End Page: "))
			try:
				if checkurl.group() in url:
					url = url.replace(checkurl.group(), '')
				elif checkurl1.group() in url:
					url = url.replace(checkurl1.group(), '')
			except:
				break
			break
		except:
			print("\nInvaild Input... Try again")
			time.sleep(2)
	browser.get(url)
	crawl(s,e,url)

def Main():
	email = input("Email: ")
	passwrd = passwordbox("Password: ")
	login(email,passwrd)

if __name__ == '__main__':
	Main()
