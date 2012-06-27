import veritable
import veritable.utils
import json
import sys


TABLE_NAME = 'movielens'


'''
Perform analysis on the given data file and and schema, creating the 
table first if needed and uploading the data.
'''
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


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
