import veritable
import json
import sys
import time


TABLE_NAME = 'movielens'


def main(data_file, schema_file):
    rows = json.loads(open(data_file).read())
    schema = json.loads(open(schema_file).read())
    
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