# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3_upload_split']

package_data = \
{'': ['*']}

install_requires = \
['anypubsub>=0.6,<0.7', 'boto3>=1.15.18,<2.0.0']

setup_kwargs = {
    'name': 's3-upload-split',
    'version': '0.1.3',
    'description': 'Streams the content of an iterator to multiple S3 objects based on a regular expression',
    'long_description': "# Python S3 Upload Split\n\nS3 Upload Split is used to stream the content of an iterator to multiple S3 objects based on a provided regular \nexpression. The iterator must be a list of dictionary, typically the resulset of a SQL query. Files will be called \n`data-{pattern}.json` where `{pattern}` is the match found using your regex.\n\n## Install\n`pip install s3-upload-split`\n\n## Usage\n\n### Import\n```python\nimport re\nfrom sqlalchemy import create_engine\nfrom s3_upload_split import SplitUploadS3\n\nbucket = 'YOUR_BUCKET_NAME' # ex: my-bucket\nprefix = 'OUTPUT_PATH' # ex: db1/output/dev/\nregex = re.compile(r'YOUR_REGEX') # ex: \\\\d{4}-\\\\d{2}-\\\\d{2} \\\\d{2}:\\\\d{2}:\\\\d{2}\\\\D+(\\\\d{4}-\\\\d{2})-\\\\d{2}\nengine = create_engine('sqlite:///bookstore.db') # https://github.com/pranaymethuku/bookstore-database/blob/master/database/bookstore.db\n\nwith engine.connect() as con:\n\n    iterator = con.execute('SELECT * FROM book')\n    SplitUploadS3(bucket, prefix, regex, iterator).handle_content()\n```\n\n## Limitations\nIt creates one thread per matched pattern using your regex, so take it into account when you use that module. This is \ntypically useful if your regex matches months in the input iterator. ",
    'author': 'Cyril Scetbon',
    'author_email': 'cscetbon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cscetbon/s3-upload-split',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
