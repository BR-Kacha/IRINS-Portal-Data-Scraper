from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
from bs4 import BeautifulSoup

username = "librarian@atmiyauni.ac.in"
password = "AUirins@123"

driver = webdriver.Chrome("D:\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe")
driver.get("https://atmiyauni.irins.org/dashboard")
content = driver.page_source
soup = BeautifulSoup(content)

uname = driver.find_element(By.XPATH, '//*[@id="loginform"]/fieldset[1]/input')
pword = driver.find_element(By.XPATH, '//*[@id="loginform"]/fieldset[2]/input')
uname.send_keys(username)
pword.send_keys(password)

login=driver.find_element(By.XPATH, '//*[@id="login"]')
login.click()
time.sleep(6)
try:
    sucess=driver.find_element(By.XPATH, '/html/body/nav/div/div')
    print("Login successful")
    driver.get("https://atmiyauni.irins.org/dashboard/stats")
    print("Collecting data ...")
    time.sleep(7)
    cit_mtrx_pg = driver.page_source
    cit_soup = BeautifulSoup(cit_mtrx_pg)
    try:
        other_data = []
        for i in cit_soup.find_all('div',class_="col-md-3 col-lg-3 col-sm-12 col-xs-12"):
            for j in i.find_all('div',class_="card-body card-dashboard"):
                for k in j.find_all('div',class_="table-responsive"):
                    tbl= k.find('table')
                    for l in tbl.find_all('td'):
                           print(l.text)
                           other_data.append(l.text)
        metadata = []
        data = []
        
        
        
        
        for x in range(0,len(other_data),2):
              metadata.append(other_data[x])
        for y in range(1,len(other_data),2):
              data.append(other_data[y])
        
        altmetrics_data = []
        for m in cit_soup.find_all('div',class_="col-md-12 col-lg-12 col-sm-12 col-xs-12"):
            for n in m.find_all('div',class_="card-body card-dashboard"):
                for o in n.find_all('div',class_="table-responsive"):
                    tbl= o.find('table')
                    for p in tbl.find_all('td'):
                        print(p.text)
                        altmetrics_data.append(p.text)
        data_dict = {}
        for z in range(0,len(metadata)):
            data_dict[metadata[z]] = data[z]
        data_dict["Altmetrics"] = altmetrics_data[0]
        data_dict["Facebook"] = altmetrics_data[1]
        data_dict["Twiter"] = altmetrics_data[2]
        data_dict["Altmetrics Crossref"] = altmetrics_data[3]
        data_dict["Google Plus"] = altmetrics_data[4]
        dataframe = pd.DataFrame(data=data_dict,index=[0])
        dataframe.T.to_excel("AU_IRINS_Data_through_Python.xlsx", index=True)
        # finaltoexcel = pd.ExcelWriter('AU_IRINS_Data_through_Python.xlsx')
        # finaltoexcel.save()   
    except Exception as e:
        print(e)
except:
    print("Login failed : \n Check the username and password or \n Check your network connection ")

driver.close()