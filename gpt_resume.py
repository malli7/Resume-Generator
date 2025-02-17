import os
from openai import OpenAI
from resume import Resume
import re
from prompt_templates import prompt_template
from prompts import summary_prompt, skills_prompt, experience_prompt,projects_prompt,cert_prompt


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 

client = OpenAI(api_key=OPENAI_API_KEY)

class GPTResume:
    def __init__(self, job_description, resume_data):
        self.job_description = job_description
        self.resume_data = resume_data
    
    def generate_summary(self):        
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
        {"role": "system", "content": "You are a professional resume writer with deep expertise in AI-driven hiring trends, recruiter psychology, and ATS optimization."},
        {"role": "user", "content": summary_prompt},
        {"role": "user", "content": f"Here’s the candidate’s resume data: {self.resume_data}"},
        {"role": "user", "content": f"Here’s the job description: {self.job_description}"},
        ],)
        return response.choices[0].message.content
    
    def generate_education(self):
        return "\n".join([
                f"<div class='entry'><p class='education'><b>{edu['education_level']} {'in'} {edu['field_of_study']} | {edu['start_date']} - {edu['year_of_completion']} | {"GPA: "} {edu['GPA']}</b></p> <p class='education'>{edu['institution']}, {edu['location']} </p> </div>"
                for edu in self.resume_data["education_details"]
            ])

    def generate_skills(self):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI-powered ATS and hiring expert, specializing in skill matching for high-impact job applications."},
                {"role": "user", "content": skills_prompt},
                {"role": "user", "content": f"Here’s the candidate’s resume skills: {self.resume_data["skills"]}"},
                {"role": "user", "content": f"Here’s the job description: {self.job_description}"},
            ]
        )
        return response.choices[0].message.content
    
    def generate_experience(self):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI-powered ATS optimization expert specializing in rewriting and enhancing professional experience for job applications."},
                {"role": "user", "content": experience_prompt},
                {"role": "user", "content": f"Here’s the candidate’s work experience: {self.resume_data["experience_details"]}"},
                {"role": "user", "content": f"Here’s the job description: {self.job_description}"},
            ]
        )
        formatted_experience = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', response.choices[0].message.content)
        return formatted_experience
    
    def generate_projects(self):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI-powered ATS optimization expert specializing in crafting job-winning project descriptions that impress recruiters at all levels."},
                {"role": "user", "content": projects_prompt},
                {"role": "user", "content": f"Here’s the candidate’s projects: {self.resume_data['projects']}"},
                {"role": "user", "content": f"Here’s the job description: {self.job_description}"},
            ]
        )
        formatted_projects = response.choices[0].message.content
        formatted_projects = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_projects)
        return formatted_projects
    
    def format_certifications_and_achievements(self):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI-powered ATS optimization expert specializing in selecting, enhancing, and generating relevant certifications and achievements for job applications."},
                {"role": "user", "content":cert_prompt},
                {"role": "user", "content": f"Here’s the candidate’s certifications: {self.resume_data['certifications']}"},
                {"role": "user", "content": f"Here’s the candidate’s achievements: {self.resume_data['achievements']}"},
                {"role": "user", "content": f"Here’s the job description: {self.job_description}"},
            ]
        )
        formatted_certifications = response.choices[0].message.content
        formatted_certifications = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_certifications)
        return formatted_certifications

            
    def generate_resume(self):
        return Resume(prompt_template.format(
            name=self.resume_data["personal_information"]["name"],
            email=self.resume_data["personal_information"]["email"],
            phone=self.resume_data["personal_information"]["phone"],
            location=self.resume_data["personal_information"]["city"],
            linkedin=self.resume_data["personal_information"]["linkedin"],
            github=self.resume_data["personal_information"]["github"],
            portfolio=self.resume_data["personal_information"]["portfolio"],
            summary=self.generate_summary(), 
            education = self.generate_education(),
            skills=self.generate_skills(),
            experience=self.generate_experience(),
            projects=self.generate_projects(),
            certifications=self.format_certifications_and_achievements()
        ))
