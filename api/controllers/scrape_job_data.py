import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from model.job_model import insert_job

load_dotenv()

searchKeyword = 'Web developer'

jobPortals = {
    "simplyhired": f"https://www.simplyhired.co.in/search?q={searchKeyword}",
    "indeed": f"https://in.indeed.com/jobs?q={searchKeyword}",
    "foundit": f"https://www.foundit.in/srp/results?query={searchKeyword}",
    "linkedin": f"https://www.linkedin.com/jobs/search?keywords={searchKeyword}",
    "naukri": f"https://www.naukri.com/{searchKeyword}-jobs?k={searchKeyword}",
    "internshala": f"https://internshala.com/jobs/{searchKeyword}-jobs/",
    "ycombinator": f"https://www.workatastartup.com/companies?query={searchKeyword}&sortBy=keyword",
    "upwork": f"https://www.upwork.com/nx/search/jobs/?q={searchKeyword}",
    "freelancer": f"https://www.freelancer.com/search/projects?q={searchKeyword}",
    "glassdoor": f"https://www.glassdoor.co.in/Job/{searchKeyword}-jobs-SRCH_KO0,16.htm",
}

scraperapi_key = os.getenv('SCRAPER_API')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def createFile(file, title, company_name, job_link, job_location, job_salary=None, source=None):
    if title and company_name and job_link and job_location:
        file.write(f"Job Title: {title}\n")
        file.write(f"Company Name: {company_name}\n")
        file.write(f"Job Link: {job_link}\n")
        file.write(f"Job Location: {job_location}\n")
        if job_salary:
            file.write(f"Job Salary: {job_salary}\n")
        if source:
            file.write(f"Source: {source}\n")
        file.write("\n")

def scrapejobsdata():
    job_data = []
    for portal, url in jobPortals.items():
        print(f"Scraping {portal}: {url}")

        try:
            if portal == 'linkedin':
                response = requests.get(url, headers=headers)
            else:
                proxy_url = f"http://api.scraperapi.com?api_key={scraperapi_key}&url={url}"
                response = requests.get(proxy_url, headers=headers)

            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            with open(f"{portal}.html", "w", encoding="utf-8") as file:
                file.write(soup.prettify())

            if portal == 'linkedin':
                job_list = soup.find('ul', class_='jobs-search__results-list')
                if job_list:
                    jobs = job_list.find_all('li')
                    with open(f"{portal}_jobs.txt", "w", encoding="utf-8") as file:
                        for job in jobs:
                            title = job.find('h3', class_='base-search-card__title')
                            company_name = job.find('h4', class_='base-search-card__subtitle')
                            job_link = job.find('a', class_='base-card__full-link')
                            job_location = job.find('span', class_='job-search-card__location')

                            createFile(file, title, company_name, job_link, job_location)

                            if title and company_name and job_link and job_location:
                                job_info = {
                                    "title": title.text.strip(),
                                    "company_name": company_name.text.strip(),
                                    "job_link": job_link['href'].strip(),
                                    "job_location": job_location.text.strip(),
                                    "job_salary": None,
                                    "source": portal
                                }
                                job_data.append(job_info)
                                insert_job(job_info)

            elif portal == 'glassdoor':
                job_list = soup.find('ul', class_='JobsList_jobsList__lqjTr')
                if job_list:
                    jobs = job_list.find_all('li')
                    with open(f"{portal}_jobs.txt", "w", encoding="utf-8") as file:

                        for job in jobs:
                            title = job.find('a', class_='JobCard_jobTitle___7I6y')
                            company_name = job.find('span', class_='EmployerProfile_compactEmployerName__LE242')
                            job_link = title['href'] if title else None
                            job_location = job.find('div', class_='JobCard_location__rCz3x')
                            job_salary = job.find('div', class_='JobCard_salaryEstimate__arV5J')

                            createFile(file, title, company_name, job_link, job_location, job_salary)


                            if title and company_name and job_link and job_location:
                                job_info = {
                                    "title": title.text.strip(),
                                    "company_name": company_name.text.strip(),
                                    "job_link": f"https://www.glassdoor.co.in{job_link}",
                                    "job_location": job_location.text.strip(),
                                    "job_salary": job_salary.text.strip() if job_salary else None,
                                    "source": portal
                                }
                                job_data.append(job_info)
                                insert_job(job_info)

            elif portal == 'indeed':
                job_list = soup.find('ul', class_='css-zu9cdh eu4oa1w0')
                if job_list:
                    jobs = job_list.find_all('li')
                    with open(f"{portal}_jobs.txt", "w", encoding="utf-8") as file:

                        for job in jobs:
                            job_link_element = job.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0')
                            if job_link_element:
                                job_link = f"https://in.indeed.com{job_link_element['href']}"
                                title_element = job_link_element.find('span')
                                company_name_element = job.find('span', class_='css-63koeb eu4oa1w0')
                                job_location_element = job.find('div', class_='css-1p0sjhy eu4oa1w0')
                                job_salary_element = job.find('div', class_='JobCard_salaryEstimate__arV5J')

                                # createFile(file, title_element.text.strip(), company_name_element.text.strip(), job_link, job_location_element.text.strip(), job_salary_element.text.strip())

                                if title_element and company_name_element and job_location_element:
                                    job_info = {
                                        "title": title_element.text.strip(),
                                        "company_name": company_name_element.text.strip(),
                                        "job_link": job_link,
                                        "job_location": job_location_element.text.strip(),
                                        "job_salary": job_salary_element.text.strip() if job_salary_element else None,
                                        "source": portal
                                    }
                                    job_data.append(job_info)
                                    insert_job(job_info)

            elif portal == 'internshala':
                job_list = soup.find('div', id='list_container')
                if job_list:
                    jobs = job_list.find_all('div', class_='internship_meta')
                    for job in jobs:
                        title = job.find('h3', class_='job-internship-name')
                        company_name = job.find('p', class_='company-name')
                        job_link = job.find_parent('div', class_='individual_internship')['data-href'] if job.find_parent('div', class_='individual_internship') else None
                        job_location = job.find('div', class_='individual_internship_details').find('a')

                        if title and company_name and job_link and job_location:
                            job_info = {
                                "title": title.text.strip(),
                                "company_name": company_name.text.strip(),
                                "job_link": f"https://internshala.com{job_link}",
                                "job_location": job_location.text.strip(),
                                "job_salary": None,
                                "source": portal
                            }
                            job_data.append(job_info)
                            insert_job(job_info)

            elif portal == 'simplyhired':
                job_list = soup.find('ul', id='job-list')
                if job_list:
                    jobs = job_list.find_all('li')
                    for job in jobs:
                        title_element = job.find('a', class_='chakra-button css-1djbb1k')
                        company_name_element = job.find('span', class_='css-lvyu5j').find('span')
                        job_link_element = title_element['href']
                        job_location_element = job.find('span', class_='css-1t92pv').find('span')
                        job_salary_element = job.find('p', class_='chakra-text css-1g1y608')

                        title = title_element.text.strip() if title_element else "N/A"
                        company_name = company_name_element.text.strip() if company_name_element else "N/A"
                        job_link = "https://www.simplyhired.co.in" + job_link_element if job_link_element else "N/A"
                        job_location = job_location_element.text.strip() if job_location_element else "N/A"
                        job_salary = job_salary_element.text.strip() if job_salary_element else "N/A"

                        job_info = {
                            "title": title,
                            "company_name": company_name,
                            "job_link": job_link,
                            "job_location": job_location,
                            "job_salary": job_salary,
                            "source": portal
                        }
                        job_data.append(job_info)
                        insert_job(job_info)

            elif portal == 'upwork':
                job_list = soup.find('section', attrs={'data-ev-label': 'search_result_impression'})
                if job_list:
                    jobs = job_list.find_all('article')

                    with open(f"{portal}_jobs.txt", "w", encoding="utf-8") as file:
                        for job in jobs:
                            title_element = job.find('h2', class_='job-tile-title').find('a')
                            title = title_element.text.strip() if title_element else "No title"
                            job_link = title_element['href'] if title_element else "No link"
                            job_location = "Remote"

                            job_info = {
                                "title": title,
                                "job_link": f"https://www.upwork.com{job_link}",
                                "job_location": job_location,
                                "job_salary": None,
                                "source": portal
                            }
                            job_data.append(job_info)
                            insert_job(job_info)

                            createFile(file, title, None, f"https://www.upwork.com{job_link}", job_location)

            elif portal == 'freelancer':
                print(portal, "inside this")
                job_list = soup.find('div', id='project-list')
                if job_list:
                    jobs = job_list.find_all('div', class_="JobSearchCard-item")

                    with open(f"{portal}_jobs.txt", "w", encoding="utf-8") as file:
                        for job in jobs:
                            title_element = job.find('a', class_='JobSearchCard-primary-heading-link')
                            title = title_element.text.strip() if title_element else "No title"
                            job_link = title_element['href'] if title_element else "No link"
                            job_location = "Remote"

                            job_info = {
                                "title": title,
                                "job_link": f"https://www.freelancer.com{job_link}",
                                "job_location": job_location,
                                "job_salary": None,
                                "source": portal
                            }
                            job_data.append(job_info)
                            insert_job(job_info)

                            print(title, job_link, job_location)
                            createFile(file, title, None, f"https://www.freelancer.com{job_link}", job_location)

        except requests.exceptions.RequestException as e:
            print(f"Failed to scrape {portal}: {e}")

    return job_data
