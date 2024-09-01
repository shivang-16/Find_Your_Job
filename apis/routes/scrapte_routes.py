from flask import Blueprint, jsonify
from controllers.scrape_job_data import scrapejobsdata

# Create a Blueprint for scrape routes
scrape_blueprint = Blueprint('scrape', __name__)

@scrape_blueprint.route('/api/scrape', methods=['GET'])
def scrape_jobs():
    job_data = scrapejobsdata()
    return jsonify(job_data)
