from flask import Flask, jsonify, request
from flask_cors import CORS
from controllers.get_job_data import get_jobs
from controllers.scrape_job_data import scrapejobsdata

app = Flask(__name__)
CORS(app)


@app.route('/')
def test():
    return "Server is working"


@app.route('/api/scrape', methods=['GET'])
def scrape_jobs():
    job_data = scrapejobsdata()
    return jsonify(job_data)


@app.route('/api/jobs/get', methods=['GET'])
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


if __name__ == '__main__':
    app.run(debug=True)
