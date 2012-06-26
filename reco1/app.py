from flask import Flask, render_template, request
import json
import veritable
from util import get_last_successful_analysis, get_baselines, mean


MIN_RATINGS = 100
ITEMS = [it 
    for it in json.loads(open('static/item_descriptions.json').read())
    if it['num_ratings'] > MIN_RATINGS]
ITEMS.sort(key=lambda x: x['name'])
ITEM_NAMES = dict([(m['id'], m['name']) for m in ITEMS])
TABLE_NAME = 'movielens'

# connect to the Veritable API and perform baseline predictions; this will
# allow us to compute "lift" later
api = veritable.connect()
analysis = get_last_successful_analysis(api, TABLE_NAME)
baselines = get_baselines(analysis)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', items=ITEMS)


@app.route('/predict', methods=['POST'])
def predict():
    # make predictions
    query = request.json
    preds = analysis.predict(query)

    # compute the rating change from baseline for each item
    rating_lifts = []
    for m in query:
        if query[m] == None:
            per_item_preds = [int(p[m]) for p in preds.distribution]
            per_item_mean = float(sum(per_item_preds)) / len(per_item_preds)
            rating_lifts.append((m, per_item_mean - baselines[m]))
    
    # sort by rating change and return those items with an increase
    rating_lifts.sort(key=lambda r: r[1], reverse=True)
    result = [(ITEM_NAMES[r[0]], r[1]) for r in rating_lifts if r[1] > 0.]
    return json.dumps(result)
    

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
