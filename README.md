# 240-Databases-Project
Project Space for CSCI-240: Databases

Proposal:

A database for local companies in the IT and Cybersecurity space. 

Entity Sets:
- Company: C01, C02, etc: *name, *contact, *website, *company_size, *glassdoor_rating, *glassdoor_rec, *job_posts
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
- Job Postings: R01, R02, etc: *title, *company, *wage, *desired_certs, *industries, *number_posted_jobs, *position_type
  - Support Technician/Help Desk
  - Sys Admin
  - Security Analyst
- Company Contact: CC01, CC02, etc: *name, *company, *phone, *email, *title
  - Leaving empty until after our meeting on Monday. 
- Position Type:
  - Full-time
  - Part-time
  - Contract
        
Questions/Use Cases:
- Which local company has the best glassdoor rating?
- What job role is most in demand locally? 
- Who is a contact for a certain company?
