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


def get_baselines(analysis):
    # Get baseline ratings for all of the movies
    query = dict([(m['id'], None) for m in ITEMS])
    preds = analysis.predict(query, count=40)
    baselines = {}
    for m in query:
        per_movie_preds = [int(p[m]) for p in preds.distribution]
        baselines[m] = float(sum(per_movie_preds)) / len(per_movie_preds)
    return baselines


def mean(x):
    if len(x) == 0:
        return float('nan')
    else:
        return float(sum(x)) / len(x)
