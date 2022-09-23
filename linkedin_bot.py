# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 02:07:00 2022

@author: micha
"""
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json
# measure time
t = time.time()

browser = webdriver.Chrome("chromedriver.exe")

def login(browser, username, password): 
    browser.get("https://www.linkedin.com")
    username_key = browser.find_element(By.ID,"session_key")
    username_key.send_keys(username)
    password_key = browser.find_element(By.ID,"session_password")
    password_key.send_keys(password)
    login_button = browser.find_element(By.CLASS_NAME, "sign-in-form__submit-button")
    login_button.click()

def infiniteScroll(browser):
    # infinte scroll
    time.sleep(3)
    previous_height = browser.execute_script('return document.body.scrollHeight')
    
    while True:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        new_height = browser.execute_script('return document.body.scrollHeight')
        if new_height == previous_height:
            break
    
        previous_height = new_height
        
def getCompaniesJobLink(browser):
    
    # companies I follow on Linkedin
    browser.get("https://www.linkedin.com/in/michallevin25/details/interests/?detailScreenTabIndex=1")
    infiniteScroll(browser)
    
    # find all company links
    time.sleep(3)
    company_page = browser.find_elements(By.XPATH,"//a[contains(@href,'https://www.linkedin.com/company/')]")
    
    # create link for the job page for each company
    # TODO: company_page returns two times the same link. check if possible to remove one of them and then remove if statement
    companies_jobpages = []
    prev_page = company_page[0].get_attribute("href") + 'jobs/'
    for x in range (1,len(company_page)):
        jobs_page = company_page[x].get_attribute("href") + 'jobs/'
        if jobs_page != prev_page:
            companies_jobpages.append(jobs_page)
        prev_page = jobs_page
    
        
    return companies_jobpages
def noJobs(browser):
        # case where there are no jobs
        job_company = browser.find_elements(By.XPATH,'//h1')
        job_company = job_company[0].text
        data = {'Company name': [job_company],
                                 'Job Title': 'no jobs'}
        job_info = pd.DataFrame(data)
        return job_info
    
def createDataFrame(job_company, job_titles, job_locations):
    # create DataFrame      
    data = {'Company name': job_company,
            'Job Title':job_titles,
            'Job Location': job_locations}
    
    job_info = pd.DataFrame(data)
    return job_info



def jobFinder(curr_jobpage):
    browser.get(curr_jobpage)
    time.sleep(3)
        
    try:
        # wont find this element if there are no job boxes
        all_jobs = browser.find_element(By.CLASS_NAME, "org-jobs-recently-posted-jobs-module__show-all-jobs-btn")
    except:
        job_info = noJobs(browser)
    else:    
        time.sleep(3)
        if all_jobs.is_displayed():
            all_jobs.click()
        else:
            print('im here')
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            all_jobs.click()

            
        time.sleep(3)
        job_text = browser.find_elements(By.CLASS_NAME,"occludable-update")
        job_company, job_titles, job_locations = [], [], []
        time.sleep(3)
        unwanted_text = 'See more jobs with these suggestions:'
        for i in range(len(job_text)):
            curr_job = job_text[i].text
        
            # TODO: remove if statement and create scrolling 
            # TODO: create class job
            if len(curr_job) > 1:
                if unwanted_text not in curr_job:
                    if 'Israel' in curr_job:
                        curr_job = curr_job.split('\n')
                        job_titles.append(curr_job[0])
                        job_company.append(curr_job[1])
                        job_locations.append(curr_job[2].replace('Israel', ' '))

                        
        # create DataFrame      
        job_info = createDataFrame(job_company, job_titles, job_locations)
        
        return job_info


def cleanData(companies_df):
    
    # remove job titles with unwanted keywords
    with open('unwanted_jobs.json', 'r') as openfile:
        unwanted_jobs_dict= json.load(openfile)
    keywords = unwanted_jobs_dict['keywords']
    for i in range(0,len(keywords)):
        word = keywords[i]
        companies_df = companies_df[companies_df["Job Title"].str.contains(word) == False]
    
    # remove Nan
    companies_df.dropna(subset=['Job Title'])
    
    # reset index
    companies_df = companies_df.reset_index(drop = True)
    
    return companies_df
    

# main
with open('login_data.json', 'r') as openfile:
    json_data = json.load(openfile)
    
browser = webdriver.Chrome("chromedriver.exe")
login(browser, json_data['email'], json_data['password'])
companies_jobpages = getCompaniesJobLink(browser)
companies_df = jobFinder(companies_jobpages[0])
for curr_jobpage in companies_jobpages[1:]:
    job_info = jobFinder(curr_jobpage)
    companies_df = pd.concat([companies_df, job_info])
    
companies_df = cleanData(companies_df)
print(companies_df)

elapsed = time.time() - t
print("running time", elapsed)

# write to excel
companies_df.to_excel("companies.xlsx")

