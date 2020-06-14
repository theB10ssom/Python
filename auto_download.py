from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib import parse
import time

options = Options()
options.add_argument('--start-fullscreen')
options.add_experimental_option("prefs", {
	"profile.default_content_setting_values.automatic_downloads" : 1
	})
driver = webdriver.Chrome(executable_path="c:/chromedriver_win32/chromedriver.exe", chrome_options=options)
url = "https://data.kma.go.kr/cmmn/main.do"


try:
	driver.get(url)
	#로그인
	login_path = '//*[@id="loginBtn"]'
	login_btn  = driver.find_element_by_xpath(login_path)
	driver.execute_script("arguments[0].click();", login_btn)

	id_path = '//*[@id="loginId"]'
	id_in   = driver.find_element_by_xpath(id_path)
	id_in.send_keys("yongmin990821@gmail.com")
	pw_path = '//*[@id="passwordNo"]'
	pw_in   = driver.find_element_by_xpath(pw_path)
	pw_in.send_keys("dydals0821!")
	time.sleep(1)

	btn_path= '//*[@id="loginbtn"]'
	btn_ = driver.find_element_by_xpath(btn_path)
	driver.execute_script("arguments[0].click();", btn_)

	time.sleep(2)

	#자료 검색
	css_ = "#mwrap > div.mgnb-wrap > div > ul > li:nth-child(2) > a"
	obs = driver.find_element_by_css_selector(css_)
	obs.click()
    

	d_css_ = "#content > div.content-body > div:nth-child(13) > div > ul > li:nth-child(2) > a"
	dataset_menu = driver.find_element_by_css_selector(d_css_)
	driver.execute_script("arguments[0].click();", dataset_menu)
	time.sleep(2)

	def select_freq(data_freq):
		freq = driver.find_element_by_xpath('//*[@id="dataFormCd"]/option[' + str(data_freq) + ']')
		freq.click()

		time.sleep(2)

	select_freq(6)
	#2 : 시간자료 3 : 일 자료 4 : 월 자료 5 : 년 자료 6: 분 자료  

	def select_date(start_year, end_year):
		start_path = '//*[@id="startDt"]/option['
		end_path   = '//*[@id="endDt"]/option['

		start = driver.find_element_by_xpath(start_path + str(start_year) + ']')
		start.click()
		end   = driver.find_element_by_xpath(end_path + str(end_year) + ']')
		end.click()

		time.sleep(1)

	def select_asos(asos_loc):
		expand_path = '//*[@id="ztree_26_switch"]'
		expand = driver.find_element_by_xpath(expand_path)
		expand.click()

		#loc_path = '//*[@id="ztree_' + str(asos_loc) + '_check"]'
		loc_path = '//*[@id="ztree_27_check"]'
		loc = driver.find_element_by_xpath(loc_path)
		driver.execute_script("arguments[0].click();", loc)
		#if loc.get_attribute('checked'):
		#loc.click()

		time.sleep(1)


	select_date(13, 2)
	#13 : 2009, 2 : 2020
	select_asos(27)
	#27 : 강릉
	search_btn_path = '//*[@id="dsForm"]/div[2]/a'
	search_btn = driver.find_element_by_xpath(search_btn_path)
	driver.execute_script("arguments[0].click();", search_btn)

	time.sleep(2)

	for i in range(2,15):
		select_all_path = '//*[@id="checkAll"]'
		select_all_btn = driver.find_element_by_xpath(select_all_path)
		driver.execute_script("arguments[0].click();", select_all_btn)

		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		down_path = '//*[@id="content"]/div[3]/div[6]/div/div[2]/a'
		down_btn  = driver.find_element_by_xpath(down_path)
		driver.execute_script("arguments[0].click();", down_btn)
		time.sleep(2)

		reqst_path = '//*[@id="reqstPurposeCd10"]'
		reqst_btn  = driver.find_element_by_xpath(reqst_path)
		driver.execute_script("arguments[0].click();", reqst_btn)

		get_path = '//*[@id="btnArea"]/input[2]'
		get_btn  = driver.find_element_by_xpath(get_path)
		driver.execute_script('fnRequest();', get_btn)

		#time.sleep(10)
		driver.execute_script("goPage(%s);" % i)

	time.sleep(5)



except Exception as e:
    print(e)
finally:
    driver.quit()
