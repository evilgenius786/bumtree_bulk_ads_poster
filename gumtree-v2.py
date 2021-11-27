import json
import os
import pickle
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

t = 1
timeout = 5

debug = False

headless = False
images = True
max = True

incognito = False


def postAd(driver, file):
    with open(file) as json_file:
        print("Loading config from " + file)
        config = json.load(json_file)
    print(json.dumps(config, indent=4))
    time.sleep(t)
    driver.get("https://my.gumtree.com/postad")
    time.sleep(t)
    try:
        driver.find_element_by_xpath('//*[@id="is-being-refined"]/div[2]/div/div[1]/div/input[2]').click()
    except:
        pass
    click(driver, '//button[@class="btn-link set-left form-row-label space-mts"]')
    print("Category: ", end="")
    print(f"{config['cat'][0]}", end="")
    click(driver, f"//span[contains(text(),'{config['cat'][0]}')]")
    for cat in config['cat'][1:]:
        print(f" -> {cat}", end="")
        time.sleep(t)
        click(driver, f"//*[contains(text(),'{cat}')]", True)
    click(driver, '//*[@id="continueButton"]')
    click(driver, '//*[contains(text(),"Select your location instead")]')
    print("\nLocation: ", end="")
    print(f" {config['loc'][0]}", end="")
    click(driver, f"//*[contains(text(),'{config['loc'][0]}')]")
    for loc in config['loc'][1:]:
        print(f" -> {loc}", end="")
        click(driver, f"//*[contains(text(),'{loc}')]", True)
    click(driver, '//*[@id="locationIdBtn"]')
    time.sleep(t)
    print()
    for data in config['data']:
        print(f"{data} : {str(config['data'][data]).splitlines()}")
        sendkeys(driver, f'//*[@id="{data}"]', config['data'][data])
    print("\nSelecting: ", end="")
    for check in config['check']:
        print(f", {check}", end="")
        click(driver, f"//*[contains(text(),'{check}')]")
    files = [os.path.abspath(os.path.join(config['dir'], p)) for p in os.listdir(config['dir'])]
    print(f"\nUploading files in {config['dir']}: ")
    for file in files:
        print("\t" + file)
        driver.find_element_by_xpath("//input[@type='file']").send_keys(file)
    if len(config["post-ad_usePhone"]) > 1:
        click(driver, "//label[@for='post-ad_usePhone']")
        sendkeys(driver, '//*[@id="post-ad_contactTelephone"]', config["post-ad_usePhone"])
    print("Submitting ad...")
    click(driver, '//*[@id="submit-button-2"]')
    time.sleep(t)


def main():
    driver = getChromeDriver()
    driver.delete_all_cookies()
    try:
        with open("login.json") as file:
            login = json.load(file)
        email = login['email']
        password = login['pass']
    except:
        print("Error: Missing login.json")
        email = "786hassan777@gmail.com"
        password = "Hassan786"
    driver.get("https://my.gumtree.com/postad")
    time.sleep(t)
    # click(driver, '//input[@value="No thanks"]')
    try:
        driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
    except:
        pass
    click(driver, '//*[contains(text(),"I have an account")]')
    try:
        driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
    except:
        pass
    if driver.current_url == "https://my.gumtree.com/login/postad":
        try:
            print("Logging in from cookies...")
            for cookie in pickle.load(open("cookies.pkl", "rb")):
                driver.add_cookie(cookie)
        except:
            try:
                print("Cookies not found! Logging in from username/password...")
                sendkeys(driver, '//*[@id="email"]', email)
                sendkeys(driver, '//*[@id="fld-password"]', password + "\n")
                pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
            except:
                print("Error in logging in...")
    else:
        print("Already logged in!")
    files = [os.path.abspath(os.path.join("configs", p)) for p in os.listdir("configs")]
    for file in files:
        postAd(driver, file)


print("""
           _____                 _                 
          / ____|               | |                
         | |  __ _   _ _ __ ___ | |_ _ __ ___  ___ 
         | | |_ | | | | '_ ` _ \| __| '__/ _ \/ _ \\
         | |__| | |_| | | | | | | |_| | |  __/  __/
          \_____|\__,_|_| |_| |_|\__|_|  \___|\___|

=============================================================
    Developed by : https://www.fiverr.com/muhammadhassan7/
                    © Muhammad Hassan.
=============================================================

                                           """)


def getChromeDriver(proxy=None):
    options = webdriver.ChromeOptions()
    if debug:
        # print("Connecting existing Chrome for debugging...")
        options.debugger_address = "127.0.0.1:9222"
    if not images:
        # print("Turning off images to save bandwidth")
        options.add_argument("--blink-settings=imagesEnabled=false")
    if headless:
        # print("Going headless")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
    if max:
        # print("Maximizing Chrome ")
        options.add_argument("--start-maximized")
    if proxy:
        # print(f"Adding proxy: {proxy}")
        options.add_argument(f"--proxy-server={proxy}")
    if incognito:
        # print("Going incognito")
        options.add_argument("--incognito")
    return webdriver.Chrome(options=options)


def getFirefoxDriver():
    options = webdriver.FirefoxOptions()
    if not images:
        # print("Turning off images to save bandwidth")
        options.set_preference("permissions.default.image", 2)
    if incognito:
        # print("Enabling incognito mode")
        options.set_preference("browser.privatebrowsing.autostart", True)
    if headless:
        # print("Hiding Firefox")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
    return webdriver.Firefox(options)


def click(driver, xpath, js=False):
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    # if js:
    #     driver.execute_script("arguments[0].click();", element)
    ActionChains(driver).move_to_element(element).perform()
    element.click()


def sendkeys(driver, xpath, keys):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(keys)


def getElement(driver, xpath):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))


if __name__ == "__main__":
    main()
