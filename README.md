# 240-Databases-Project
Project Space for CSCI-240: Databases

Proposal:

A database for (mostly) local companies in the IT and Cybersecurity space that can assist in evaluating job prospects, career goals and wage considerations. 

Entity Sets:
- Company: *coID, *name, *contact, *website, *company_size, *glassdoor_rating, *glassdoor_rec, *job_posts
- Job: *jobID, *title, *company, *certifications, *post_date, *cloes_date, *description
  Sub Types:
  - Full Time:
      - Wage/Salary
      - Benefits
      - Schedule
  - Part Time:
      - Wage
      - Schedule
  - Contract:
      - Terms
      - Amount
      - Length
- Contact: contractID*, *name, *phone, *email, *position
  - Leaving empty until after our meeting on Monday. 
- Job Role: *bisID, *job_title, *avg_wage, *description
- Certificatino: *certID, *name, *certifying_body, *cost, *requirements 
        
Questions/Use Cases:
- Which local company has the best glassdoor rating?
- What job role is most in demand locally? 
- Who is a contact for a certain company?
- How does a job postings wage compare to the average wage for such a position?
