import datetime
import noseapp
from noseapp.ext.requests import RequestsEx, make_config
from requests import HTTPError
# setting up
endpoint = make_config()
endpoint.configure(
    base_url='http://127.0.0.1:5000/',
    key='127.0.0.1:5000'
)
endpoint.session_configure(
    always_return_json=True,
    raise_on_http_error=False
)
requests_ex = RequestsEx(endpoint)

# gather all tests
suite = noseapp.Suite('first_suite')

# setup for requests
api = requests_ex.get_endpoint_session('127.0.0.1:5000')


@suite.register
class TestCaseGetOne(noseapp.TestCase):
    """
        get request
    """
    def test_get_404(self):
        # check existence
        self.assertEqual(HTTPError(404).message, api.get('dictionary/123')['code'])

    def test_get_added_element(self):
        # add element for test
        api.post('dictionary', {"key": "test_get", "value": "test_me"})
        # check existing element
        self.assertTrue(api.get('dictionary/test_get').get('test_get'))

        self.assertEqual("test_me", api.get('dictionary/test_get')['test_get'])

        # delete element
        self.assertEqual(api.delete('dictionary/test_get')['test_get'], 'null')
        # check existing element
        self.assertTrue(not api.get('dictionary/test_get').get('test_get'))

    # check time - must be equivalent to out time
    def test_get_time(self):
        # add element for test
        api.post('dictionary', {"key": "test_get", "value": "test_me"})
        # check existing element
        self.assertTrue(api.get('dictionary/test_get').get('test_get'))

        self.assertEqual(api.get('dictionary/test_get')['time'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

        # delete element
        self.assertEqual(api.delete('dictionary/test_get')['test_get'], 'null')
        # check existing element
        self.assertTrue(not api.get('dictionary/test_get').get('test_get'))


@suite.register
class TestCasePost(noseapp.TestCase):
    """
       post requests
    """
    def test_post_added_element(self):
        # add element for test
        api.post('dictionary', {"key": "test_post", "value": "target"})
        # check existing element
        self.assertTrue(api.get('dictionary/test_post').get('test_post'))

        self.assertEqual("target", api.get('dictionary/test_post')['test_post'])

        # delete element
        self.assertEqual(api.delete('dictionary/test_post')['test_post'], 'null')
        # check existing element
        self.assertTrue(not api.get('dictionary/test_post').get('test_post'))

    # adding already existed element
    def test_post_409(self):
        # add element for test
        api.post('dictionary', {"key": "test_post", "value": "target"})
        # check existing element
        self.assertTrue(api.get('dictionary/test_post').get('test_post'))

        self.assertEqual(HTTPError(409).message, api.post('dictionary', {"key": "test_post", "value": "1"})['code'])

        # delete element
        self.assertEqual(api.delete('dictionary/test_post')['test_post'], 'null')
        # check existing element
        self.assertTrue(not api.get('dictionary/test_post').get('test_post'))

    # pass one missing param
    def test_post_400_one_param(self):
        self.assertEqual(HTTPError(400).message, api.post('dictionary', {"key": "test_post", "value": ""})['code'])

    # pass two missing params
    def test_post_400_two_params(self):
        self.assertEqual(HTTPError(400).message, api.post('dictionary', {"key": "", "value": ""})['code'])

    # check time - must be equivalent to out time
    def test_post_time(self):
        self.assertEqual(api.post('dictionary', {"key": "test_post", "value": "target"})['time'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

        # delete element
        self.assertEqual(api.delete('dictionary/test_post')['test_post'], 'null')
        # check existing element
        self.assertTrue(not api.get('dictionary/test_post').get('test_post'))


@suite.register
class TestCasePut(noseapp.TestCase):
    """
       put requests
    """
    def test_put_change_element(self):
        # add element for test
        api.post('dictionary', {"key": "test_put", "value": "test_me"})
        # check existing element
        self.assertTrue(api.get('dictionary/test_put').get('test_put'))

        # change element
        api.put('dictionary', {"key": "test_put", "value": "test_me_again"})

        self.assertTrue(api.get('dictionary/test_put').get('test_put'))
        self.assertEqual("test_me_again", api.get('dictionary/test_put')['test_put'])

        # delete element
        self.assertEqual(api.delete('dictionary/test_put')['test_put'], 'null')
        # check existing element
        self.assertTrue(not api.get('dictionary/test_put').get('test_put'))

    def test_put_404(self):
        # add element for test
        api.post('dictionary', {"key": "test_put", "value": "test_me"})
        # check existing element
        self.assertTrue(api.get('dictionary/test_put').get('test_put'))

        self.assertEqual(HTTPError(404).message, api.put('dictionary', {"key": 'another_key', "value": 'another_value'})['code'])

        # delete element
        self.assertEqual(api.delete('dictionary/test_put')['test_put'], 'null')
        # check existing element
        self.assertTrue(not api.get('dictionary/test_put').get('test_put'))

    def test_put_time(self):
        # add element for test
        api.post('dictionary', {"key": "test_put", "value": "test_me"})
        # check existing element
        self.assertTrue(api.get('dictionary/test_put').get('test_put'))

        self.assertEqual(api.put('dictionary', {"key": 'test_put', "value": 'another_value'})['time'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

        # delete element
        self.assertEqual(api.delete('dictionary/test_put')['test_put'], 'null')
        # check existing element
        self.assertTrue(not api.get('dictionary/test_put').get('test_put'))


@suite.register
class TestCaseDelete(noseapp.TestCase):
    """
    delete requests
    """
    # double deleting same element to check 200
    def test_delete_ok(self):
        # add element for test
        api.post('dictionary', {"key": "test_delete", "value": "speech"})
        # check existing element
        self.assertTrue(api.get('dictionary/test_delete').get('test_delete'))

        self.assertEqual(api.delete('dictionary/test_delete')['test_delete'], 'null')
        # check existing element
        self.assertTrue(not api.get('dictionary/test_delete').get('test_delete'))

        self.assertEqual(api.delete('dictionary/test_delete')['test_delete'], 'null')
        # check existing element
        self.assertTrue(not api.get('dictionary/test_delete').get('test_delete'))

    def test_delete_time(self):
        # add element for test
        api.post('dictionary', {"key": "test_delete", "value": "speech"})
        # check existing element
        self.assertTrue(api.get('dictionary/test_delete').get('test_delete'))

        self.assertEqual(api.delete('dictionary/test_delete')['time'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        # check existing element
        self.assertTrue(not api.get('dictionary/test_delete').get('test_delete'))


app = noseapp.NoseApp('flask_test_with_noseapp')
app.register_suite(suite)

app.run()