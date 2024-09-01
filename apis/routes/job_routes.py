from flask import Blueprint, jsonify, request
from controllers.get_job_data import get_jobs
from middleware.check_auth import check_auth

# Create a Blueprint for job-related routes
job_blueprint = Blueprint('job', __name__)

@job_blueprint.route('/api/jobs/get', methods=['GET'])
def fetch_jobs():
    # Get the 'page' parameter from the query string, defaulting to 1 if not provided
    page = int(request.args.get('page', 1))

    # Get optional query parameters
    source = request.args.get('source')
    salary_range = request.args.get('salary_range')
    title = request.args.get('title')

    # Fetch jobs with filters and pagination
    jobs = get_jobs(page, source=source, salary_range=salary_range, title=title)

    if jobs is not None:
        return jsonify(jobs)
    else:
        return jsonify({"error": "Error fetching jobs"}), 500
