# User-based Recommendation Reference Design

This reference design demonstrates how to use the [Veritable API](https://dev.priorknowledge.com) to generate recommendations based on the ratings that a user has given other items.

See [this page](https://dev.priorknowledge.com/docs/examples/example_user_recs.html) on the [Veritable developer docs](https://dev.priorknowledge.com/docs) for a more complete introduction and discussion of recommendation systems, and the architecture and implementation of this example.

# Installation

This example is implemented in python, and uses the [Veritable python client](https://dev.priorknowledge.com/docs/client/python) ([github](github.com/priorknowledge/veritable-python)).

To download and install:

    $ git clone https://github.com/priorknowledge/user-recs-example.git
    $ cd user-recs-example
    $ pip install -r requirements.txt

To upload data and start an analysis:

    $ export VERITABLE_KEY=<your Veritable API key>
    $ python util/run_analysis.py data/movielens_data.json data/movielens_schema.json

The app will not work until this analysis is complete, which you can check on the [Veritable dashboard](https://dev.priorknowledge.com/dashboard).

Once the analysis is done, run the app:

    $ python recs/app.py

Then point your browser at [http://localhost:5000](http://localhost:5000)

# Important files

- [`recs/app.py`](https://github.com/priorknowledge/user-recs-example/blob/master/recs/app.py) The Flask application that make ratings predictions and uses them to generate item recommendations.
- [`recs/static/main.js`](https://github.com/priorknowledge/user-recs-example/blob/master/recs/static/main.js) The Javascript that collects the user ratings, asks the server for recommendations, and then populates the page with the results.
- [`recs/templates/index.html`](https://github.com/priorknowledge/user-recs-example/blob/master/recs/templates/index.html) The jinja template for the app's only page.
- [`util/run_analysis.py`](https://github.com/priorknowledge/user-recs-example/blob/master/util/run_analysis.py) A command-line script that uploads rating data to Veritable and starts an analysis.

# Support

If you have any problems with or questions about this example, please let us know in our public [chat room](https://dev.priorknowledge.com/campfire), or at support@priorknowledge.com.
