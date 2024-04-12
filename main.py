import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, \
    OnSiteOrRemoteFilters
import json
import datetime

# Change root logger level (default is WARN)
logging.basicConfig(level=logging.INFO)

current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"{formatted_datetime}_results.json"

def setup():
    with open(f"results/{file_name}", 'a') as f:
        f.write('[\n')

def cleanup():
    with open(f"results/{file_name}", 'a') as f:
        f.seek(f.tell() - 2, 0)  
        f.truncate()
        f.write('\n]')



# Fired once for each successfully processed job
def on_data(data: EventData):
    print('[ON_DATA]', data.title, data.company, data.company_link, data.date, data.link, data.insights,
          len(data.description))
    
    with open(f"results/{file_name}", 'a') as f:
        try:
            job_data = {
            'job_id': data.job_id,
            'title': data.title,
            'company': data.company,
            'company_link': data.company_link,
            'date': data.date,
            'link': data.link,
            'insights': data.insights,
            'description_length': len(data.description),
            'description': data.description,
            'apply_link': data.apply_link if data.apply_link else 'N/A',
            }
        except Exception as e:
            print(f'Error occurred while processing job data: {e}')
            job_data = {}
            
        json.dump(job_data, f)
        f.write(',\n')
    


# Fired once for each page (25 jobs)
def on_metrics(metrics: EventMetrics):
    print('[ON_METRICS]', str(metrics))


def on_error(error):
    print('[ON_ERROR]', error)


def on_end():
    print('[ON_END]')


scraper = LinkedinScraper(
    chrome_executable_path=None,  # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver)
    chrome_binary_location=None,  # Custom path to Chrome/Chromium binary (e.g. /foo/bar/chrome-mac/Chromium.app/Contents/MacOS/Chromium)
    chrome_options=None,  # Custom Chrome options here
    headless=True,  # Overrides headless mode only if chrome_options is None
    max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
    slow_mo=0.5,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
    page_load_timeout=40  # Page load timeout (in seconds)    
)

# Add event listeners
scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

queries = [
    # Query(
    #     options=QueryOptions(
    #         limit=100  # Limit the number of jobs to scrape.            
    #     )
    # ),
    Query(
        query='Software Engineering Manager',
        options=QueryOptions(
            locations=['United States'],
            apply_link=True,  # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page must be navigated. Default to False.
            # skip_promoted_jobs=True,  # Skip promoted jobs. Default to False.
            page_offset=2,  # How many pages to skip
            limit=10,
            filters=QueryFilters(
                relevance=RelevanceFilters.RECENT,
                time=TimeFilters.MONTH,
                type=[TypeFilters.FULL_TIME],
                on_site_or_remote=[OnSiteOrRemoteFilters.REMOTE, OnSiteOrRemoteFilters.ON_SITE, OnSiteOrRemoteFilters.HYBRID],
                experience=[ExperienceLevelFilters.MID_SENIOR, ExperienceLevelFilters.DIRECTOR]
            )
        )
    ),
]




# main 

setup()

scraper.run(queries)

cleanup()