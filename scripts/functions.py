from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging


class Instagram_post_automation():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
    
    def login_page(self,username,password,title_post,image):
        self.driver.get("https://www.instagram.com/")
        login_username = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="loginForm"]/div[1]/div[1]/div/label/input')))
        login_password = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="loginForm"]/div[1]/div[2]/div/label/input')))
        login_submit = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="loginForm"]/div[1]/div[3]')))

        login_username.send_keys(username)
        login_password.send_keys(password)
        login_submit.click()

class LinkedIn_post_automation():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
    
    def login_page(self,username,password,title_post,image):
        self.driver.get("https://www.linkedin.com/")

        sign_in_button = self.wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/nav/div/a[2]')))
        sign_in_button.click()

        login_username = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="username"]')))
        login_password = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="password"]')))
        login_submit = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="organic-div"]/form/div[4]/button')))

        login_username.send_keys(username)
        login_password.send_keys(password)
        login_submit.click()
class X_post_automation():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
    
    def login_page(self,username,password):
            self.driver.get("https://x.com/")
            button_enter =  self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[4]/a/div')))
            button_enter.click()

            username_field = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')))
            username_field.send_keys(username)

            button_next = self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div')))
            button_next.click()

            password_field = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')))
            password_field.send_keys(password)

            button_advance = self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button')))
            button_advance.click()

    def create_post(self,content,image_path):
            print(image_path)
            if image_path == None:
                entry_content = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div')))
                post_button = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button')))
                entry_content.send_keys(content)
                post_button.click()
            else:
                entry_content = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div')))
                entry_content.send_keys(content)
                
                entry_image_path_button = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/button')))
                #entry_image_path_button.click()
                entry_image_path_button.send_keys(image_path)

                post_button = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button')))
                post_button.click()
