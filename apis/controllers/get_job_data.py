from db.db import get_collection
from pymongo import DESCENDING

collection = get_collection('jobs')

def get_jobs(page=1, source=None, salary_range=None, title=None, limit=100):
    try:
        skip = (page - 1) * limit

        # Build the query dictionary
        query = {}
        if source:
            query['source'] = source
        if salary_range:
            query['job_salary'] = salary_range
        if title:
            # Use $regex for case-insensitive title search
            query['title'] = {'$regex': title, '$options': 'i'}

        # Fetch jobs with filters and pagination
        jobs_cursor = collection.find(query).skip(skip).limit(limit).sort("_id", DESCENDING)
        jobs = list(jobs_cursor)  # Convert cursor to a list

        # Convert ObjectId to string before returning the response
        for job in jobs:
            job['_id'] = str(job['_id'])

        return jobs
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        return None
