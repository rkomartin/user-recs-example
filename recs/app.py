from flask import Flask, render_template, request
import json
import veritable
from util import get_last_successful_analysis, get_baselines, mean, std


MIN_RATINGS = 100
TABLE_NAME = 'movielens'

# load the item metadata from a static file; in a production system this
# information would likely come from a database
ITEMS = [it 
    for it in json.loads(open('static/movie_descriptions.json').read())
    if it['num_ratings'] > MIN_RATINGS]
ITEMS.sort(key=lambda x: x['name'])
ITEM_NAMES = dict([(m['id'], m['name']) for m in ITEMS])

# connect to the Veritable API and perform baseline predictions; this will
# allow us to compute rating "lift" later
api = veritable.connect()
analysis = get_last_successful_analysis(api, TABLE_NAME)
baselines = get_baselines(analysis, ITEMS)
app = Flask(__name__)


def item_filter(per_item_preds, baseline_val):
    '''
    Decides whether an item should be considered for inclusion in the 
    recommendations. This version requires that three conditions be met:
    
    1. The item must have a reasonably high predicted rating (per_item_mean > 3.)
    2. The predictions must indicate that the user will rate the item higher than
       its baseline rating (lift > .2)
    3. The predictions must not be too uncertain regarding the positive 
       lift (conf > .75)
    '''
    N = len(per_item_preds)
    mn = mean(per_item_preds)
    conf = float(sum([1 for p in per_item_preds if p - baseline_val > 0.])) / N
    lift = mn - baseline_val
    return mn > 3. and lift > .2 and conf > .75


def item_sorter(item):
    return item[1]


@app.route('/')
def index():
    return render_template('index.html', items=ITEMS)


@app.route('/recommend', methods=['POST'])
def recommend():
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
