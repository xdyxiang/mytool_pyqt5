from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from myapp.gtcode import CrackGeetest
import time
import os
from myapp.db_func import DB


def do_signup(email,username):
    # 无界面运行配置
    chrome_options = Options()
    prefs = {"download.default_directory": "./"}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path="res/chromedriver.exe", options=chrome_options)

    wait = WebDriverWait(driver, 5)
    try:
        driver.get("http://host/signup")
        #  输入注册邮箱
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="l-sign-layout"]/main/div/div[2]/form/div[1]/div/div[1]/input'))).send_keys(email)
        # 点击获取验证码按钮
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="l-sign-layout"]/main/div/div[2]/form/div[2]/div/div[1]/div[2]/button'))).click()
        crack = CrackGeetest(driver, wait)
        crack.crack()
        time.sleep(2)
        #  输入验证码
        sqlstr = "select * from email_captcha where email = '{0}' order by create_time desc".format(email)
        code = DB().execute_sql(sqlstr)[0][2]
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="l-sign-layout"]/main/div/div[2]/form/div[2]/div/div[1]/div[1]/div/input'))).send_keys(code)
        # 勾选同意
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="l-sign-layout"]/main/div/div[2]/form/div[4]/div/div/div/label/span[1]/span'))).click()
        # 点击注册
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="l-sign-layout"]/main/div/div[2]/form/div[5]/div/button'))).click()
        time.sleep(2)
        # 注册页面------
        # 输入账号名
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="l-sign-layout"]/main/div/div[2]/form/div[1]/div/div/input'))).send_keys(username)
        # 输入密码
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="l-sign-layout"]/main/div/div[2]/form/div[2]/div/div[1]/input'))).send_keys("123456")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="l-sign-layout"]/main/div/div[2]/form/div[3]/div/div[1]/input'))).send_keys("123456")
        time.sleep(1)
        # 点击确认
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="l-sign-layout"]/main/div/div[2]/form/div[4]/div/button'))).click()
        time.sleep(3)
        if driver.title =="*** | 注册成功":
            print("注册成功！！")
            return "注册成功！！"
        else:
            print("注册失败")
            return "注册失败"

    except:
        print("注册失败")
        return "注册失败"
    finally:
        driver.close()

# do_signup("dengyouxin001+097@gmail.com","gg097")
