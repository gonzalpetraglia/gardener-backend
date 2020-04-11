def test_healthcheck(client):

    rv = client.get('/healthcheck')
    assert b'Im fine' in rv.data
