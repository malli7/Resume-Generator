import os
from openai import OpenAI
from prompts import cover_letter_prompt
from resume import CoverLetter
from prompt_templates import cover_letter_template




API_KEY = os.getenv("API_KEY") 
client = OpenAI(api_key=API_KEY) 


class GPTCoverLetter:
    def __init__(self, job_description, resume_data):
        self.job_description = job_description
        self.resume_data = resume_data
        
    def generate_cover_letter_text(self):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": cover_letter_prompt},
                {"role": "user", "content": f"Here’s the candidate’s resume skills: {self.resume_data}"},
                {"role": "user", "content": f"Here’s the job description: {self.job_description}"},
            ]
        )
        return response.choices[0].message.content
    

    def generate_cover_letter(self):
        cover_letter = self.generate_cover_letter_text()
        linkedin = self.resume_data["personal_information"].get("linkedin", "")
        github = self.resume_data["personal_information"].get("github", "")
        portfolio = self.resume_data["personal_information"].get("portfolio", "") 
        linkedin_link = f'| <a href="{linkedin}">LinkedIn</a>' if linkedin else ""
        github_link = f'| <a href="{github}">GitHub</a>' if github else ""
        portfolio_link = f'| <a href="{portfolio}">Portfolio</a>' if portfolio else ""
        
        return  CoverLetter(cover_letter_template.format(
                name=self.resume_data["personal_information"]["name"],
                email=self.resume_data["personal_information"]["email"],
                phone=self.resume_data["personal_information"]["phone"],
                location=self.resume_data["personal_information"]["city"],
                linkedin=linkedin_link,
                github=github_link,
                portfolio=portfolio_link,
                cover_letter = cover_letter,
            ))