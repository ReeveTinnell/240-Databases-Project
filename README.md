# 240-Databases-Project
Project Space for CSCI-240: Databases

Proposal:

A database for local companies in the IT and Cybersecurity space. 

Entity Sets:
- Company: C01, C02, etc: *name, *contact, *website, *company_size, *glassdoor_rating, *glassdoor_rec, *number_job_postings_24m
  - ELM
  - Providence
  - University of Montana
  - OnX
- Industry: I01, I02, etc: *industry, *description 
  - Service Provider
  - Government
  - Non-profit
  - Healthcare
  - Education
- Job Roles: R01, R02, etc: *title, *wage_range, *desired_certs, *industries, *number_posted_jobs
  - Support Technician/Help Desk
  - Sys Admin
  - Security Analyst
- Company Contact: CC01, CC02, etc: *name, *company, *phone, *email, *title
  - Leaving empty until after our meeting on Monday. 

        
Questions/Use Cases:
- Which local company has the best glassdoor rating?
- What job role is most in demand locally? 
- Who is a contact for a certain company?
