import veritable
import veritable.utils
import json
import sys
import time


TABLE_NAME = 'movielens'

'''
Perform analysis on the given data file and and schema, creating the 
table first if needed and uploading the data.
'''
def main(data_file, schema_file):
    rows = json.loads(open(data_file).read())
    schema = json.loads(open(schema_file).read())
    # veritable.utils.validate_data(rows, schema)
    
    api = veritable.connect()
    
    if not api.table_exists(TABLE_NAME):
        print 'Creating table'
        table = api.create_table(TABLE_NAME)
    else:
        print 'Getting table'
        table = api.get_table(TABLE_NAME)
    
    print 'Uploading rows'
    table.batch_upload_rows(rows)
    print 'Creating analysis'
    analysis = table.create_analysis(schema)
    
    while True:
        time.sleep(2)
        analysis.update()
        if analysis.state == 'failed':
            print analysis.error
        elif analysis.state == 'running':
            print 'Running'


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])