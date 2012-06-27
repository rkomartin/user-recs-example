from math import sqrt

def get_last_successful_analysis(api, table_name):
    # Get the most recent analysis for the table that ended successfully
    table = api.get_table(table_name)
    analyses = table.get_analyses()
    last_successful_analysis = None
    for analysis in analyses:
        if analysis.state == 'succeeded':
            if last_successful_analysis == None or \
                  analysis.created_at > last_successful_analysis.created_at:
                last_successful_analysis = analysis
    return last_successful_analysis


def get_baselines(analysis, items):
    # Get baseline ratings for all of the movies
    query = dict([(item['id'], None) for item in items])
    preds = analysis.predict(query)
    baselines = {}
    for it in query:
        per_item_preds = [float(p[it]) for p in preds.distribution]
        baselines[it] = mean(per_item_preds)
    return baselines


def mean(x):
    if len(x) == 0:
        return float('nan')
    else:
        return float(sum(x)) / len(x)

def std(x):
    N = len(x)
    sumsq = sum([a * a for a in x])
    mn = mean(x)
    return sqrt(sumsq / N - mn * mn)