from flask import Flask, request, jsonify
from scraper.therapist_scraper import scrape_therapists
from scraper.enrichment_agent import enrich_therapists
from scraper.utils import save_to_json
import threading
import uuid
from collections import defaultdict

app = Flask(__name__)
task_results = defaultdict(dict)
task_lock = threading.Lock()

def process_therapist_scrape(task_id, website, zipcode):
    from time import sleep
    try:
        with task_lock:
            task_results[task_id] = {'status': 'processing'}

        therapists = scrape_therapists(website, zipcode, max_results=50)
        enriched = enrich_therapists(therapists)
        save_to_json(enriched, 'data/results.json')

        with task_lock:
            task_results[task_id] = {'status': 'completed', 'data': enriched}
    except Exception as e:
        with task_lock:
            task_results[task_id] = {'status': 'failed', 'error': str(e)}

@app.route('/scrape_therapists', methods=['POST'])
def scrape_therapists_route():
    data = request.get_json()
    website = data.get('website')
    zipcode = data.get('zipcode')
    if not website or not zipcode:
        return jsonify({'error': 'Provide website and zipcode'}), 400

    task_id = str(uuid.uuid4())
    with task_lock:
        task_results[task_id] = {'status': 'pending'}

    thread = threading.Thread(target=process_therapist_scrape, args=(task_id, website, zipcode), daemon=True)
    thread.start()
    return jsonify({'task_id': task_id, 'status': 'pending'})

@app.route('/task_status/<task_id>', methods=['GET'])
def get_status(task_id):
    with task_lock:
        result = task_results.get(task_id)
    if not result:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)