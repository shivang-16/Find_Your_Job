import os
from dotenv import load_dotenv
from db import get_collection



load_dotenv()

collection = get_collection('jobs')


def insert_job(job):
    print(job, "here is the job")

    job_document = {
        "title": job.get('title', 'N/A'),  # Default to 'N/A' if None
        "company_name": job.get('company_name', 'N/A'),
        "job_link": job.get('job_link', 'N/A'),
        "job_location": job.get('job_location', 'N/A'),
        "job_salary": job.get('job_salary', 'N/A'),
        "source": job.get('source', 'N/A')
    }

    try:
        collection.insert_one(job_document)
        print(f"Inserted job: {job_document['title']}")
    except Exception as e:
        print(f"Error inserting job {job_document['title']}: {e}")


