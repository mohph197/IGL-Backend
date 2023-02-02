from flask.testing import FlaskClient

def test_paginate(client: FlaskClient):
    response = client.get('announcements/all')
    result = response.get_json()
    total_count = 0
    assert response.status_code == 200

    for page in range(1, result['num_pages']):
        response = client.get(f'announcements/all?page={page}')
        result = response.get_json()
        total_count += len(result['annonces'])
        assert response.status_code == 200
        assert len(result['annonces']) == result['per_page']
        assert result['page'] == page

    response = client.get(f'announcements/all?page={result["num_pages"]}')
    result = response.get_json()
    total_count += len(result['annonces'])
    assert response.status_code == 200
    assert len(result['annonces']) == result['total_count'] % result['per_page'] or len(result['annonces']) == result['per_page']
    assert result['page'] == result['num_pages']
    assert total_count == result['total_count']

def test_filter(client: FlaskClient):
    q = 'villa'
    type = 'Vente'
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    start_price = 10000
    end_price = 1000000
    wilaya = 'Alger'
    commune = 'Alger'
    request_args = f'q={q}&type={type}&start_date={start_date}&end_date={end_date}&start_price={start_price}&end_price={end_price}&wilaya={wilaya}&commune={commune}'
    response = client.get(f'announcements/all?{request_args}')
    result = response.get_json()
    assert response.status_code == 200

    for page in range(1, result['num_pages'] + 1):
        response = client.get(f'announcements/all?page={page}&{request_args}')
        result = response.get_json()
        assert response.status_code == 200

        for announcement in result['annonces']:
            assert q in announcement['titre'] or q in announcement['description']
            assert announcement['type'] == type or type == 'Autre'
            assert announcement['date_publication'] >= start_date
            assert announcement['date_publication'] <= end_date
            assert announcement['prix'] >= start_price
            assert announcement['prix'] <= end_price
            assert wilaya in announcement['localisation']['wilaya']
            assert commune in announcement['localisation']['commune']