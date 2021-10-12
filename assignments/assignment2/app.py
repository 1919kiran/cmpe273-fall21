from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, g, json
from HashUtil import encode
from database import init_db, insert, get_clicks, retrive_url, update_link
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
    data = request.get_json()
    long_url = data.get('long_url')
    domain = data.get('domain')
    group_guid = data.get('group_guid')
    tags = data.get('tags')
    deeplinks = data.get('deeplinks')
    title = data.get('title')

    short_url = encode(long_url)
    url_data = (long_url, short_url, domain, datetime.datetime.now(), datetime.datetime.now(),
                'admin', 'admin', group_guid, tags, deeplinks, title)

    result = insert(url_data, short_url, domain)
    return jsonify(result)


@app.route('/rest/api/v1/bitlinks/<domain>/<bitlink>/clicks', methods=['GET'])
def count_clicks(domain, bitlink):
    unit = request.args.get('unit')
    units = int(request.args.get('units'))
    unit_reference = unquote(request.args.get('unit_reference'))

    try:
        unit_reference = datetime.datetime.strptime(unit_reference, "%Y-%m-%dT%H:%M:%S%z")
    except Exception as e:
        print('Exception occurred while converting str to date; taking current time as reference', e)
        unit_reference = datetime.datetime.now().isoformat()

    link_clicks = get_clicks(bitlink, domain, unit, units, unit_reference)
    return jsonify({
        'link_clicks': link_clicks,
        'units': units,
        'unit': unit,
        'unit_reference': unit_reference
    })


@app.route('/rest/api/v1/bitlinks/<domain>/<bitlink>', methods=['GET'])
def retrieve(domain, bitlink):
    return jsonify(retrive_url(domain, bitlink, update_clicks=True))


@app.route('/rest/api/v1/bitlinks', methods=['POST'])
def create():
    data = request.get_json()
    long_url = data.get('long_url')
    domain = data.get('domain')
    group_guid = data.get('group_guid')
    tags = data.get('tags')
    deeplinks = data.get('deeplinks')
    title = data.get('title')

    short_url = encode(long_url)
    time = datetime.datetime.now()
    url_data = (long_url, short_url, domain, time, time, 'admin', 'admin', group_guid, str(tags), str(deeplinks), title)
    insert(url_data, short_url, domain)

    return jsonify({
        'link': long_url,
        'bitlink': domain + '/' + short_url,
        'title': title,
        'created_by': 'admin',
        'created_at': time,
        'tags': tags,
        'deeplinks': deeplinks
    })


@app.route('/rest/api/v1/bitlinks/<domain>/<bitlink>', methods=['PATCH'])
def update(domain, bitlink):
    data = request.get_json()
    title = data.get('title')
    tags = data.get('tags')
    deeplinks = data.get('deeplinks')
    updated_by = data.get('updated_by')
    group_guid = data.get('group_guid')
    result = update_link(domain, bitlink, title, tags, deeplinks, updated_by, group_guid)
    result['short_url'] = domain + '/' + bitlink
    return result


if __name__ == 'app':
    init_db()
