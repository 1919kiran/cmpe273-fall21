from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, g, json
from HashUtil import encode
from database import init_db, insert, get_clicks
import datetime
from urllib.parse import unquote


app = Flask(__name__)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/rest/api/v1/shorten', methods=['POST'])
def shorten():
    print(__name__)
    try:
        data = request.get_json()
        long_url = data.get('long_url')
        domain = data.get('domain')
        group_guid = data.get('group_guid')

        short_url = encode(long_url)
        url_data = (long_url, short_url, domain, datetime.datetime.now(), datetime.datetime.now(),
                    group_guid, group_guid)
        insert(url_data, short_url, domain)

    except Exception as e:
        print('Exception occured: ', e)
    return jsonify({'response': encode(long_url)})


@app.route('/rest/api/v1/bitlinks', methods=['PATCH'])
def update():
    pass


@app.route('/rest/api/v1/bitlinks/<domain>/<bitlink>/clicks', methods=['GET'])
def count_clicks(domain, bitlink):
    try:
        unit = request.args.get('unit')
        units = int(request.args.get('units'))
        unit_reference = unquote(request.args.get('unit_reference'))

        try:
            unit_reference = datetime.datetime.strptime(unit_reference, "%Y-%m-%dT%H:%M:%S%z")
        except Exception as e:
            print('Exception occurred while converting str to date; taking current time as reference', e)
            unit_reference = datetime.datetime.now().isoformat()

        link_clicks = get_clicks(bitlink, unit, units, unit_reference)
        return jsonify({
            'link_clicks': link_clicks,
            'units': units,
            'unit': unit,
            'unit_reference': unit_reference
        })

    except Exception as e:
        data = {
            "message": "Exception occurred",
            "description": str(e),
            "error_code": 500
        }
        response = app.response_class(response=json.dumps(data),
                                      status=500,
                                      mimetype='application/json')
        return response


@app.route('/rest/api/v1/bitlinks/<domain>/<bitlink>', methods=['GET'])
def retrieve(domain, bitlink):
    pass

if __name__ == 'app':
    init_db()
