# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 13:31:07 2022

@author: micha
"""

import json

dictionary = {
    "keywords": ["Fullstack",
                 "Full Sack",
                 "Full-Stack",
                 "Frontend",
                 "Front End",
                 "Backend",
                 "Back End",
                 "Linux",
                 "DevOps",
                 "Devops",
                 "Web",
                 "Mobile",
                 "Android",
                 "iOS",
                 "Java",
                 "Embedded",
                 "SOC",
                 "SQL",
                 "Sql",
                 "UX",
                 "Senior",
                 "Architect",
                 "Cloud", 
                 "Cyber",
                 "Security Researcher",
                 "Recovery Analyst",
                 "Hardware",
                 "Shift work",
                 "Tier 3 Support",
                 "Risk investigation",
                 "Technical Writer",
                 "Project Manager",
                 "Controller",
                 "Bookkeeper",
                 "Help Desk",
                 "Administration",
                 "Planner",
                 "Marketing",
                 "Media",
                 "Creative",
                 "Content Writer",
                 "Brand Manager",
                 "Sales",
                 "Purchasing",
                 "Business",
                 "Salesforce",
                 "Product",
                 "Social Media",
                 "Logistics",
                 "Legal Counsel",
                 "eCommerce",
                 "Attorney",
                 "Financial",
                 "Finance",
                 "Talent Acquisition",
                 "Commercial",
                 "Treasury",
                 "CEO",
                 "Chief",
                 "Head Of",
                 "Specialist",
                 "Customer",
                 "Director",
                 "Affairs",
                 "Regulatory Affair",
                 "Doctoral",
                 "Thesis",
                 "PhD",
                 "Assistant", 
                 "Postdoctoral"],
     "cities": ["Haifa",
                "Yokneam",
               "Migdal Ha'Emeq",
               "Beersheba"
               ]}


with open("unwanted_jobs.json", "w") as outfile:
    json.dump(dictionary, outfile)
    

