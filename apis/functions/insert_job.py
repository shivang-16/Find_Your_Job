import os
from dotenv import load_dotenv
from db.db import get_collection
from datetime import datetime

load_dotenv()

collection = get_collection('jobs')

def insert_job(job):
    # Helper function to safely convert to lowercase
    def to_lowercase(value):
        return value.lower() if isinstance(value, str) else 'n/a'

    # Convert all fields to lowercase
    job_document = {
        "title": to_lowercase(job.get('title', 'N/A')),
        "company_name": to_lowercase(job.get('company_name', 'N/A')),
        "job_link": to_lowercase(job.get('job_link', 'N/A')),
        "job_location": to_lowercase(job.get('job_location', 'N/A')),
        "job_salary": to_lowercase(job.get('job_salary', 'N/A')),
        "source": to_lowercase(job.get('source', 'N/A')),
        "posted": job.get('posted', datetime.utcnow()),
        "createdAt": datetime.utcnow()
    }

    # Check for duplicates
    duplicate = collection.find_one({
        "title": job_document['title'],
        "company_name": job_document['company_name'],
        "source": job_document['source']
    })

    if duplicate:
        print(f"Duplicate job found: {job_document['title']} at {job_document['company_name']} from {job_document['source']}. Skipping insertion.")
    else:
        try:
            collection.insert_one(job_document)
            print(f"Inserted job: {job_document['title']}")
        except Exception as e:
            print(f"Error inserting job {job_document['title']}: {e}")
