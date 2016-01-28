import datetime
import noseapp
from noseapp.ext.requests import RequestsEx, make_config
from requests import HTTPError

endpoint = make_config()
endpoint.configure(
    base_url='http://127.0.0.1:5000/dictionary/',
    key='127.0.0.1:5000'
)
endpoint.session_configure(
    always_return_json=True,
    raise_on_http_error=True
)
requests_ex = RequestsEx(endpoint)

suite = noseapp.Suite('first_suite')

api = requests_ex.get_endpoint_session('127.0.0.1:5000')

@suite.register
class TestCase(noseapp.TestCase):
    
    """
        get request
    """
    def test_404(self):
        self.assertEqual(HTTPError(404).message, api.get('123')['code'])

    def test_200(self):
        # creepy
        self.assertNotEqual(HTTPError(404).message, api.get('name')['name'])

    # check time - must be equivalent to out time
    def test_time(self):
        self.assertEqual(api.get('name')['time'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))


@suite.register
class StepByStepCase(noseapp.ScreenPlayCase):

    def begin(self):
        pass

    @noseapp.step(1, 'comment to step')
    def step_one(self):
        self.assertTrue(True)

    @noseapp.step(2, 'comment to step')
    def step_two(self):
        self.assertTrue(True)

    def finalize(self):
        pass


@suite.register
def test_case(case):
    case.assertTrue(True)


@suite.register(simple=True)
def simple_test_case():
    assert True


app = noseapp.NoseApp('example')
app.register_suite(suite)

app.run()