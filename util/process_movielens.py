import json
import sys
from os.path import join

'''
Read movielens data into Veritable-ready json
'''

def main(input_file, output_dir):
    data = {}
    columns = set()
    with open(input_file) as fd:
        for line in fd:
            tokens = line.split('\t')
            user_id = 'U{}'.format(tokens[0]).decode()
            movie_id = 'M{}'.format(tokens[1]).decode()
            rating = tokens[2]
            if user_id not in data:
                data[user_id] = { '_id': user_id }
            data[user_id][movie_id] = rating
            columns.add(movie_id)
    
    # Add dummy data to ensure that each possible rating is observed at 
    # least once for each movie
    for i in range(5):
        user_id = 'FU{}'.format(i)
        data[user_id] = dict([(m, str(i+1)) for m in columns])
        data[user_id]['_id'] = user_id

    rows = data.values()
    schema = dict([(c, { 'type': 'categorical' }) for c in columns])
    
    open(join(output_dir, 'movielens_data.json'), 'wb').write(
        json.dumps(rows, indent=2))
    open(join(output_dir, 'movielens_schema.json'), 'wb').write(
        json.dumps(schema, indent=2))
    

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
