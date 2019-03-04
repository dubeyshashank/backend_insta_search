import csv
import os
import pandas as pd
import pandasql as ps

from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

FILE = os.environ.get("FILE", "test_data_sample.csv")


# with open(FILE) as f:
#     reader = csv.reader(f)
#     terms = [row[0] for row in reader]
#     print(terms)

df = pd.read_csv(FILE, skiprows=1, index_col=False, names=['name'])
print(df.columns)
pysql = lambda q: ps.sqldf(q, globals())


@app.route('/process_search')
def gen_search_json():
    query = request.args.get("q", '')
    df1 = pysql("Select name as id from (select name,length(name) as len_name from "
                "df where name like '%{}%' order by len_name asc, name desc) as n".format(query))

    results = df1.to_dict(orient='records')
    #must be list of dicts: [{"name": "foo"}, {"name": "bar"}]

    resp = jsonify(results=results[:10])  # top 10 results
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

