📁 Resume Dataset (Candidate Table)
Attribute	Type	Description
CandidateID	Integer (PK)	Unique identifier for each candidate
Name	Text	Full name of the candidate
Email	Text	Candidate’s email address
Phone	Text	Contact phone number
Location	Text	City, State for job matching
Experience	Integer	Total years of experience
Desired Role	Text	The role the candidate is applying for
Hard Skills	Text (comma-separated)	Technical skills (e.g., Python, SQL, Tableau)
Soft Skills	Text (comma-separated)	Non-technical skills (e.g., Leadership, Communication)
Education	Text	Highest degree and field of study
Certifications	Text	Relevant certifications (e.g., Google DA, AWS ML)
Last Job Title	Text	Most recent position held
Resume Text	Long Text	Full resume body (for NLP processing)
Resume Length	Integer	Word count of resume (useful for filtering)
Salary Expectation	Text	Expected salary range (e.g., $80k-$100k)
Availability	Text	When candidate can start (Immediate, 2 weeks, etc.)
Work Authorization	Text	Visa status (OPT, H1B, Green Card, etc.)
Remote Preference	Text	Remote / Hybrid / On-site
LinkedIn	URL	LinkedIn profile link (optional)
GitHub	URL	GitHub link (optional)
📁 Job Descriptions Dataset (Job Table)
Attribute	Type	Description
JobID	Integer (PK)	Unique identifier for each job
Job Title	Text	Name of the position (e.g., Data Analyst)
Company	Text	Hiring company (synthetic data)
Location	Text	City, State for matching candidates
Industry	Text	Industry of the job (Finance, Tech, Healthcare, etc.)
Role Category	Text	Functional category (Data, AI/ML, Ops, etc.)
Job Type	Text	Full-time / Internship / Contract
Work Mode	Text	Remote / Hybrid / On-site
Min Experience	Integer	Minimum experience required (0-5 years)
Required Education	Text	Minimum qualification required
Salary Range	Text	Budgeted salary range
Required Skills	Text (comma-separated)	Key skills needed for the job
Description	Long Text	Full job description
Posted Date	Date	When the job was posted
Urgency	Text	Hiring priority (Immediate, Rolling, etc.)
🔄 Candidate ↔ Job Matching Table (For AI Matching)
Attribute	Type	Description
MatchID	Integer (PK)	Unique match identifier
CandidateID	Integer (FK → Resume Dataset)	Links to a candidate
JobID	Integer (FK → Job Dataset)	Links to a job posting
Match Score	Float (0-100%)	AI-generated match percentage
Skill Overlap	Integer	Number of matching skills
Is Eligible	Boolean	Whether candidate meets min experience, visa, etc.
Match Rank	Integer	Ranking of candidate for that job (1 = Best)
🔗 Relationships & Logic
Each candidate can match with multiple jobs
Each job posting can have multiple matched candidates
The matching table is the core linking dataset where AI calculates rankings
📌 Now:

Open docs/schema.md
Paste this schema inside
Save the file ✅
You're structuring this like an enterprise-level data product 🔥
Let me know when you're done, and we’ll move to the next step! 🚀







You said:

 im here in vs code so how can i paste here
ChatGPT said:
🔥 You’re exactly where you need to be! Now, follow these steps to paste the schema into schema.md inside VS Code:

📌 How to Paste the Schema in VS Code
1️⃣ Click inside schema.md (you already have it open).
2️⃣ Copy the schema tables I gave above.
3️⃣ In VS Code, right-click inside schema.md and click "Paste"
OR press Ctrl + V (Windows) / Cmd + V (Mac).
4️⃣ Press Ctrl + S (Windows) / Cmd + S (Mac) to Save the file.
