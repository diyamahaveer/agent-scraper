# Data Directory
#
# This directory is used to store the results of therapist scraping tasks.
# - 'results.json' will contain the list of therapist objects once a scrape is completed.
# - The format is a JSON array of objects as defined in 'config/models.py' and serialized by 'config/schemas.py'.
#
# You may add task-specific results or logs here in the future.
#
#
#
# How to Use
# POST to /scrape_therapists with JSON:
# { "website": "<target_url>", "zipcode": "12345" }
# Poll /task_status/<task_id> to check when your scrape is done; results will be in data/results.json.