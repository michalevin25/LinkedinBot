# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 13:31:07 2022

@author: micha
"""

import json

dictionary = {
    "keywords": ["Fullstack",
                 "Full Stack",
                 "Full-Stack",
                 "Full-stack",
                 "Frontend",
                 "Front End",
                 "Backend",
                 "Back End",
                 "BackEnd",
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
                 "NOC",
                 "SQL",
                 "Sql",
                 "UX",
                 "Tableau",
                 "Dotnet",
                 "Senior",
                 "Sr.",
                 "Architect",
                 "Cloud", 
                 "Cyber",
                 "Security Researcher",
                 "Recovery Analyst",
                 "Hardware",
                 "FPGA",
                 "Industrial Engineering",
                 "Shift work",
                 "Technitian",
                 "Chemical",
                 "QA Manual",
                 "Tier 3 Support",
                 #"Risk investigation",
                 #"Technical Writer",
                 #"Project Manager",
                 #"Team Lead",
                 #"Team Manager",
                 #"Team Leader",
                 "Controller",
                 "Bookkeeper",
                 #"Help Desk",
                 #"Administration",
                 #"Administrator",
                 "Planner",
                 "Marketing",
                 "Buyer",
                 "Media",
                 "Creative",
                 "Content",
                 "Brand Manager",
                 "Sales",
                 "Presales",
                 "Purchasing",
                 "Business",
                 "Salesforce",
                 "CRM",
                 #"Product",
                 "Social Media",
                 "Logistics",
                 "Ramp Support",
                 "Legal Counsel",
                 "eCommerce",
                 "Compliance",
                 "Attorney",
                 "Financial",
                 "Finance",
                 "Talent Acquisition",
                 "User Acquisition",
                 "Commercial",
                 "Treasury",
                 "CEO",
                 "Vice President",
                 "Chief",
                 "Head of",
                 "Lead",
                 "Specialist",
                 "Customer",
                 "Director",
                 "Executive",
                 "Principal",
                 "Human Resources",
                 "Recruitment Coordinator",
                 "Growth",
                 "Affairs",
                 "Operations Manager",
                 "NPI",
                 "Regulatory Affair",
                 "Lecturer",
                 "Doctoral",
                 "Thesis",
                 "PhD",
                 "Assistant", 
                 "Postdoctoral",
                 "Physicist"],
     "cities": ["Haifa",
                "Yokneam",
                "Yoqneam Illit",
               "Migdal Ha'Emeq",
               "Beersheba"
               ]}


with open("unwanted_jobs.json", "w") as outfile:
    json.dump(dictionary, outfile)
    

