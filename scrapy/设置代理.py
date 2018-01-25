from selenium import webdriver
chromeOptions = webdriver.ChromeOptions()

# 设置代理
chromeOptions.add_argument("--proxy-server=183.186.86.171:80")
browser = webdriver.Chrome(chrome_options = chromeOptions)
# 查看本机ip，查看代理是否起作用
browser.get("http://httpbin.org/ip")
print(browser.page_source)

# 退出，清除浏览器缓存
browser.quit()
