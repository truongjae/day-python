from selenium import webdriver
from time import sleep as sl
import requests
driver = webdriver.Chrome('chromedriver.exe',service_log_path=None)


def login(username,password,two_fa):
	driver.get("https://fb.com")
	# sl(1)
	input_username = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input")
	# input_username.click()
	input_username.send_keys(username)
	input_password = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/input")
	input_password.send_keys(password)
	btn_login = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button")
	btn_login.click()
	sl(2)

	val_2fa = get_2fa(two_fa)

	input_2fa = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/form/div/div[2]/div[3]/span/input")
	input_2fa.send_keys(val_2fa)
	btn_continue = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/form/div/div[3]/div[1]/button")
	btn_continue.click()
	sl(2)
	btn_continue_save_browser = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/form/div/div[3]/div[1]/button")
	btn_continue_save_browser.click()

	data_cookie = driver.get_cookies()

	print(convert_cookie_to_string(data_cookie))

def get_2fa(two_fa):
	url = "https://2fa.live/tok/"+two_fa
	p = requests.get(url)
	data = p.json()
	return data['token']

# def get_cookie():
# 	data = [{'domain': '.facebook.com', 'expiry': 1673882042, 'httpOnly': True, 'name': 'fr', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '0hg7wFyubwSuYvoOB.AWU68EgCbKK3evokKFjboryezcg.BjTsKi.qf.AAA.0.0.BjTsKw.AWUZJzCEBA4'}, {'domain': '.facebook.com', 'expiry': 1697642038, 'httpOnly': True, 'name': 'xs', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '43%3AcgKYtx3TFS3dzA%3A2%3A1666106031%3A-1%3A-1'}, {'domain': '.facebook.com', 'expiry': 1666710831, 'httpOnly': False, 'name': 'locale', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'en_US'}, {'domain': '.facebook.com', 'expiry': 1697642038, 'httpOnly': False, 'name': 'c_user', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '100086094867180'}, {'domain': '.facebook.com', 'expiry': 1666710843, 'httpOnly': False, 'name': 'wd', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '929x887'}, {'domain': '.facebook.com', 'expiry': 1700666029, 'httpOnly': True, 'name': 'datr', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'osJOY3w5llyFMxfA2pPpXuN6'}, {'domain': '.facebook.com', 'expiry': 1700666042, 'httpOnly': True, 'name': 'sb', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'osJOY6gmf__tDTOy52nIfLcg'}]
# 	cookie = dict()
# 	for d in data:
# 		cookie[d['name']] = d['value']
# 	return cookie
def convert_cookie_to_string(data):
	string_cookie = ""
	for d in data:
		string_cookie += d['name']+"="+d['value']+"; "
	return string_cookie
username = "100086094867180"
password = "Hi8FMoG"
two_fa = "FVKKFMM64EUQVMIBAB2IGTYIAOPWGF45"

login(username,password,two_fa)