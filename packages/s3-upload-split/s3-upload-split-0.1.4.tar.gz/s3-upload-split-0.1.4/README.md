# Python S3 Upload Split

S3 Upload Split is used to stream the content of an iterator to multiple S3 objects based on a provided regular 
expression. The iterator must be a list of dictionary, typically the resulset of a SQL query. Files will be called 
`data-{pattern}.json` where `{pattern}` is the match found using your regex.

## Install
`pip install s3-upload-split`

## Usage

### Import
```python
import re
from sqlalchemy import create_engine
from s3_upload_split import SplitUploadS3

bucket = 'YOUR_BUCKET_NAME' # ex: my-bucket
prefix = 'OUTPUT_PATH' # ex: db1/output/dev/
regex = re.compile(r'YOUR_REGEX') # ex: \\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}\\D+(\\d{4}-\\d{2})-\\d{2}
engine = create_engine('sqlite:///bookstore.db') # https://github.com/pranaymethuku/bookstore-database/blob/master/database/bookstore.db

with engine.connect() as con:

    iterator = con.execute('SELECT * FROM book')
    SplitUploadS3(bucket, prefix, regex, iterator).handle_content()
```

## Limitations
It creates one thread per matched pattern using your regex, so take it into account when you use that module. This is 
typically useful if your regex matches months in the input iterator. 