# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 02:07:00 2022

@author: michal
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import pandas as pd
import json



def login(browser): 
    # json file with user info
    with open('login_data.json', 'r') as openfile:
        json_data = json.load(openfile)
        
    browser.get("https://www.linkedin.com")
    username_key = browser.find_element(By.ID,"session_key")
    username_key.send_keys(json_data['email'])
    password_key = browser.find_element(By.ID,"session_password")
    password_key.send_keys(json_data['password'])
    login_button = browser.find_element(By.CLASS_NAME, "sign-in-form__submit-button")
    # TODO: remove sleep
    time.sleep(3)
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
    time.sleep(5)
    WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH,"//a[contains(@href,'https://www.linkedin.com/company/')]")))
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

def noJobs(browser, curr_jobpage = '', jobstatus = 'global'):
        if jobstatus == 'local':
            # only if there are no jobs in israel. 
            browser.get(curr_jobpage)
            
        WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH,'//h1')))
        job_company = browser.find_elements(By.XPATH,'//h1')
        job_company = job_company[0].text
        
        # I filled the data so the cleanData function doesnt remove stuff
        data = {'Company name': [job_company],
                'Job Title': 'no jobs',
                'Job Location': 'none',
                'Job Link': 'none',
                'Other Info': 'none'}
        job_info = pd.DataFrame(data)
        return job_info


    
    
def createDataFrame(job_company, job_titles, job_locations,job_link,other_info):
    # create DataFrame      
    data = {'Company name': job_company,
            'Job Title':job_titles,
            'Job Location': job_locations,
            'Job Link': job_link,
            'Other Info': other_info}
    
    job_info = pd.DataFrame(data)
    return job_info

def searchLocation(location):
        time.sleep(5)   
        # job location - israel
        search_bars = browser.find_elements(By.CLASS_NAME, 'jobs-search-box__text-input')
        search_location = search_bars[3]
        search_location.clear()
        search_location.send_keys(location)
        search_location.send_keys(Keys.RETURN)
        time.sleep(5)

def noJobsinLocation(browser, curr_jobpage):
    try:
        browser.find_element(By.CLASS_NAME,"jobs-search-no-results-banner")
        job_info = noJobs(browser, curr_jobpage, jobstatus = 'local')
        return job_info
    except:
        pass

def foundJobs(browser):
    job_text = browser.find_elements(By.CLASS_NAME,"occludable-update")
    job_company, job_titles, job_locations, other_info = [], [], [], []
    unwanted_text = 'See more jobs with these suggestions:'
    
    for i in range(len(job_text)):
        curr_job = job_text[i].text
    
        # TODO: remove if statement and create scrolling 
        # TODO: create class job
        if len(curr_job) > 1:
            if unwanted_text not in curr_job:
                curr_job = curr_job.split('\n')
                job_titles.append(curr_job[0])
                job_company.append(curr_job[1])
                job_locations.append(curr_job[2].replace(', Israel', ' '))
                other_info.append(', '.join(e for e in curr_job[3:]))
    return job_company, job_titles, job_locations, other_info 
 
def jobFinder(browser,curr_jobpage):
    browser.get(curr_jobpage)
    
    try:
        # wont find this element if there are no job boxes
        WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "org-jobs-recently-posted-jobs-module__show-all-jobs-btn")))
        all_jobs = browser.find_element(By.CLASS_NAME, "org-jobs-recently-posted-jobs-module__show-all-jobs-btn")
        
    except:
        job_info = noJobs(browser)
    else:  
        time.sleep(3)
        # sometimes there is an additional banner on the page - scrolling is needed to show the "show all jobs" button 
       
        if all_jobs.is_displayed():
            all_jobs.click()
        else:
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            all_jobs.click()
        
        # enter location in search box
        searchLocation('israel')
        
        # a banner pops up if as a result of changing location there are no jobs 
        job_info = noJobsinLocation(browser, curr_jobpage)
        
        # in the case that there are jobs at the location
        job_company, job_titles, job_locations, other_info  = foundJobs(browser)
                      
        # create DataFrame   
        job_link = [curr_jobpage] * len(other_info)
        job_info = createDataFrame(job_company, job_titles, job_locations,job_link, other_info)
    return job_info
    
def printProgressBar(index, total, label):
    n_bar = 50  # Progress bar width
    progress = index / total
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(n_bar * progress):{n_bar}s}] {int(100 * progress)}%  {label}")
    sys.stdout.flush()
    
def concatDFs(browser,companies_jobpages):
    companies_df = jobFinder(browser,companies_jobpages[0])
    L = len(companies_jobpages)-1
    
    for index, curr_jobpage in enumerate(companies_jobpages[1:]):
        job_info = jobFinder(browser,curr_jobpage)
        companies_df = pd.concat([companies_df, job_info])
        printProgressBar(index, L, "complete")
    
    return companies_df
    
    
def cleanData(companies_df):
    # remove job titles with unwanted keywords
    with open('unwanted_jobs.json', 'r') as openfile:
        unwanted_jobs_dict= json.load(openfile)
    keywords = unwanted_jobs_dict['keywords']
    
    for i in range(0,len(keywords)):
        word = keywords[i]
        companies_df = companies_df[companies_df["Job Title"].str.contains(word) == False]

       
    cities = unwanted_jobs_dict['cities']
    for i in range(0,len(cities)):
        city = cities[i]
        companies_df = companies_df[companies_df["Job Location"].str.contains(city) == False]
    # remove Nan
    companies_df.dropna(subset=['Job Title'])
    
    # reset index
    companies_df = companies_df.reset_index(drop = True)
    return companies_df
    

#def main():
    # measure time
t = time.time()

chrome_executable = Service(executable_path='chromedriver.exe', log_path='NUL')
browser = webdriver.Chrome(service=chrome_executable)

login(browser)
companies_jobpages = getCompaniesJobLink(browser)
companies_df = concatDFs(browser,companies_jobpages)
companies_df_clean = cleanData(companies_df)


# write to excel
companies_df_clean.to_excel("companies.xlsx")
elapsed = time.time() - t
sys.stdout.write('\r')

"""    
if __name__ == "__main__":
    main()
    
"""

