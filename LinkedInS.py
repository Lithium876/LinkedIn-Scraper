import timeit, time, os, re
from tkinter import *
from os import system
from selenium import webdriver
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
		location.append(location1.text)
	except:
		location.append("n/a")
		print("Error")
	try:	
		size1 = new_tab.find_element_by_xpath("""//*[@id="stream-about-section"]/div[2]/div[2]/ul/li[5]/p""")
		size.append(size1.text)
	except:
		size.append("n/a")
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
		  		for i in range(1,11):
		  			links = browser.find_elements_by_xpath("""//*[@id="results"]/li["""+str(i)+"""]/div/h3/a""")
			  		for link in links:
			  			scrape(link.get_attribute('href'))
			  	print("\n\n[+]Scarping Page "+str(page)+" Completed\n")
			  	page+=1
			estimate=timeit.default_timer() - start
			print("Estimated Time: "+ str(round(estimate,3)))
			write(name,0, location, 1, size, 2, industry, 3)
			print("Success!")
			input()
			break
		except:
			print("Something went wrong, try again")
			search()
	
def search():
	url=GetURL.get()
	while True:
		try:
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
	urlWin.destroy()
	crawl(s,e,url)

def login():
	global browser 
	browser=webdriver.PhantomJS("C:\Program Files (x86)\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\\bin\phantomjs.exe")
	browser.set_window_size(1024, 768)
	browser.implicitly_wait(600)
	browser.get("https://linkedin.com/uas/login")	
	browser.find_element_by_id("session_key-login").send_keys(username.get() + Keys.TAB)
	browser.find_element_by_id("session_password-login").send_keys(password.get() + Keys.RETURN)
	time.sleep(1)
	if browser.current_url == "https://www.linkedin.com/uas/login":
		print("[-] Error In Login, Incorrect Email or Password\n")
		Main()
	else:
		root.destroy()
		print("\n[+] Success! Logged In, Bot Starting!")
		time.sleep(1)
		os.system('cls')
		GetURL()

def GetURL():
	print("1. Copy the link you wish to scrap from LinkedIn")
	print("2. Use ctrl+v to paste in the URL in the box")
	print("3. Click Search")
	print("4. If you wish to scrape multiple pages, please\n   specify the page you wish to begin and the last\n   page you want scraped.If you only need one page")
	print("   then use the page number for both start and end.")
	print("\n\nNB: ONLY NUMBERS ARE ALLOWED FOR START AND END PAGE.\nWHITESPACES, LETTERS OR SYMBOLS ARE INVALID INPUT")
	global urlWin
	urlWin = Tk()
	global GetURL
	#======Initalize window=====
	urlWin.wm_title("Search")
	urlWin.resizable(width=False, height=False)
	urlWin.geometry("450x60")
	urlWin.withdraw()
	urlWin.update_idletasks()  # Update "requested size" from geometry manager
	x = (urlWin.winfo_screenwidth() - urlWin.winfo_reqwidth()) / 2
	y = (urlWin.winfo_screenheight() - urlWin.winfo_reqheight()) / 2
	urlWin.geometry("+%d+%d" % (x, y))
	urlWin.deiconify()
	#===========================
	urlLabel = Label(urlWin, text="URL:")
	urlLabel.grid(row=0, column=0, pady=3)
	GetURL=Entry(urlWin,width=68)
	GetURL.grid(row=0, column=1)
	GetURLbtn=Button(urlWin,text="Search",command=search, width=20)
	GetURLbtn.grid(columnspan=2)
	urlWin.mainloop()

def Main():
	global root
	root = Tk()
	print("Please enter your LinkedIn email and password")
	global username, password
	#======Initalize window=====
	root.wm_title("LinkedIn Login")
	root.iconbitmap(r'icon.ico')
	root.resizable(width=False, height=False)
	root.geometry("250x90")
	root.withdraw()
	root.update_idletasks()  # Update "requested size" from geometry manager
	x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
	y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
	root.geometry("+%d+%d" % (x, y))
	root.deiconify()
	#===========================
	user = Label(root, text="Email:")
	user.grid(row=0, column=0, pady=3, sticky=E)
	username=Entry(root,width=30)
	username.grid(row=0, column=1)
	passwrd=Label(root,text="Password:")
	passwrd.grid(row=1, column=0, pady=5)
	password=Entry(root, width=30, show="*")
	password.grid(row=1, column=1)
	Login=Button(root,text="Login",command=login, width=20)
	Login.grid(columnspan=2)
	root.mainloop()

if __name__ == '__main__':
	Main()
