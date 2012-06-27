from flask import Flask, render_template, request
import json
import veritable
from util import get_last_successful_analysis, get_baselines, mean, std


MIN_RATINGS = 100
ITEMS = [it 
    for it in json.loads(open('static/movie_descriptions.json').read())
    if it['num_ratings'] > MIN_RATINGS]
ITEMS.sort(key=lambda x: x['name'])
ITEM_NAMES = dict([(m['id'], m['name']) for m in ITEMS])
TABLE_NAME = 'movielens'

# connect to the Veritable API and perform baseline predictions; this will
# allow us to compute "lift" later
api = veritable.connect()
analysis = get_last_successful_analysis(api, TABLE_NAME)
baselines = get_baselines(analysis, ITEMS)
app = Flask(__name__)


'''
Decides whether an item should be considered for inclusion in the 
recommendations
'''
def item_filter(per_item_preds, baseline_val):
    per_item_mean = mean(per_item_preds)
    per_item_std = std(per_item_preds)
    lift = per_item_mean - baseline_val
    return per_item_mean > 3. and per_item_std < .8 and lift > 0.


def item_sorter(item):
    return item[1]


@app.route('/')
def index():
    return render_template('index.html', items=ITEMS)


@app.route('/predict', methods=['POST'])
def predict():
    # make predictions
    query = request.json
    preds = analysis.predict(query)

    # compute the rating change from baseline for each item
    item_scores = []
    for m in query:
        if query[m] == None:
            per_item_preds = [float(p[m]) for p in preds.distribution]
            if item_filter(per_item_preds, baselines[m]):
                # print ITEM_NAMES[m], lift, per_item_mean, per_item_std
                per_item_mean = mean(per_item_preds)
                lift = per_item_mean - baselines[m]
                item_scores.append((m, lift))
    
    # sort by rating change and return those items with an increase
    item_scores.sort(key=item_sorter, reverse=True)
    result = [(ITEM_NAMES[r[0]], r[1]) for r in item_scores]
    return json.dumps(result)
    

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
