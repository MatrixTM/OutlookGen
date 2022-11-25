import warnings
from json import loads

from six import PY3
from six.moves.urllib_parse import urljoin
from requests import Session
import time

SLEEP_EVERY_CHECK_FINISHED = 3
MAXIMUM_JOIN_TIME = 200

if PY3:

    def split(value, sep, maxsplit):
        return value.split(sep, maxsplit=maxsplit)

else:
    def split(value, sep, maxsplit):
        parts = value.split(sep)
        return parts[:maxsplit] + [sep.join(parts[maxsplit:]), ]


class Job(object):
    client = None
    task_id = None
    _last_result = None

    def __init__(self, client, task_id, time_sleep=2, typecaptcha=None):
        self.client = client
        self.task_id = task_id
        self.time_sleep = time_sleep
        self.typecaptcha = typecaptcha

    def _update(self):
        self._last_result = self.client.getTaskResult(self.task_id)

    def check_is_ready(self):
        self._update()
        if self._last_result['errorId'] != 0:
            return 2
        if self._last_result["status"] == "ready":
            return 1
        return 0

    def get_solution_response(self):  # Recaptcha
        if self._last_result['errorId'] != 0:
            return "ERROR|" + self._last_result['errorDescription']

        if self.typecaptcha == "funcaptcha":
            return self._last_result["solution"]["token"]
        if self.typecaptcha == "text":
            return self._last_result["solution"]["text"]
        return self._last_result["solution"]["gRecaptchaResponse"]

    def get_token_response(self):  # Funcaptcha
        return self._last_result["solution"]["token"]

    def get_answers(self):
        return self._last_result["solution"]["answers"]

    def get_captcha_text(self):  # Image
        return self._last_result["solution"]["text"]

    def get_cells_numbers(self):
        return self._last_result["solution"]["cellNumbers"]

    def report_incorrect(self):
        warnings.warn(
            "report_incorrect is deprecated, use report_incorrect_image instead",
            DeprecationWarning,
        )
        return self.client.reportIncorrectImage()

    def report_incorrect_image(self):
        return self.client.reportIncorrectImage(self.task_id)

    def report_incorrect_recaptcha(self):
        return self.client.reportIncorrectRecaptcha(self.task_id)

    def join(self, maximum_time=200):
        elapsed_time = 0
        maximum_time = maximum_time or MAXIMUM_JOIN_TIME

        while True:
            time.sleep(self.time_sleep)
            sts = self.check_is_ready()

            if sts == 0:
                continue
            elif sts == 1:
                return
            else:
                return "ERROR"

            elapsed_time += SLEEP_EVERY_CHECK_FINISHED
            if elapsed_time is not None and elapsed_time > maximum_time:
                return "ERROR|TIMEOUT"

        while not self.check_is_ready():
            time.sleep(self.time_sleep)
            elapsed_time += SLEEP_EVERY_CHECK_FINISHED
            if elapsed_time is not None and elapsed_time > maximum_time:
                return "ERROR|TIMEOUT"


class AnycaptchaClient(object):
    client_key = None
    CREATE_TASK_URL = "/createTask"
    TASK_RESULT_URL = "/getTaskResult"
    BALANCE_URL = "/getBalance"
    REPORT_IMAGE_URL = "/reportIncorrectImageCaptcha"
    REPORT_RECAPTCHA_URL = "/reportIncorrectRecaptcha"
    APP_STAT_URL = "/getAppStats"
    SOFT_ID = 847
    language_pool = "en"
    response_timeout = 5

    def __init__(
            self, client_key, language_pool="en", host="api.anycaptcha.com", use_ssl=True
    ):
        self._client_ip = None
        self.client_key = client_key
        self.language_pool = language_pool
        self.base_url = "{proto}://{host}/".format(
            proto="https" if use_ssl else "http", host=host
        )
        self.session = Session()

    @property
    def client_ip(self):
        if not hasattr(self, "_client_ip"):
            self._client_ip = self.session.get(
                "https://api.myip.com", timeout=self.response_timeout
            ).json()["ip"]
        return self._client_ip

    def _check_response(self, response):
        pass

    def createTask(self, task, typecaptcha=None):

        request = {
            "clientKey": self.client_key,
            "task": task.serialize(),
            "softId": self.SOFT_ID,
            "languagePool": self.language_pool,
        }
        response = self.session.post(
            urljoin(self.base_url, self.CREATE_TASK_URL),
            json=request,
            timeout=self.response_timeout,
        ).json()

        self._check_response(response)

        return Job(self, response["taskId"], time_sleep=task.time_sleep, typecaptcha=typecaptcha)

    def createTaskSmee(self, task, timeout=MAXIMUM_JOIN_TIME):
        """
        Beta method to stream response from smee.io
        """
        response = self.session.head(
            "https://smee.io/new", timeout=self.response_timeout
        )
        smee_url = response.headers["Location"]
        task = task.serialize()
        request = {
            "clientKey": self.client_key,
            "task": task,
            "softId": self.SOFT_ID,
            "languagePool": self.language_pool,
            "callbackUrl": smee_url,
        }
        r = self.session.get(
            url=smee_url,
            headers={"Accept": "text/event-stream"},
            stream=True,
            timeout=(self.response_timeout, timeout),
        )
        response = self.session.post(
            url=urljoin(self.base_url, self.CREATE_TASK_URL),
            json=request,
            timeout=self.response_timeout,
        ).json()
        self._check_response(response)
        for line in r.iter_lines():
            content = line.decode("utf-8")
            if '"host":"smee.io"' not in content:
                continue
            payload = loads(split(content, ":", 1)[1].strip())
            if "taskId" not in payload["body"] or str(payload["body"]["taskId"]) != str(
                    response["taskId"]
            ):
                continue
            r.close()
            if task["type"] == "CustomCaptchaTask":
                payload["body"]["solution"] = payload["body"]["data"][0]
            job = Job(client=self, task_id=response["taskId"])
            job._last_result = payload["body"]
            return job

    def getTaskResult(self, task_id):
        request = {"clientKey": self.client_key, "taskId": task_id}
        response = self.session.post(
            urljoin(self.base_url, self.TASK_RESULT_URL), json=request
        ).json()
        self._check_response(response)
        return response

    def getBalance(self):
        request = {
            "clientKey": self.client_key,
            "softId": self.SOFT_ID,
        }
        response: dict = self.session.post(
            urljoin(self.base_url, self.BALANCE_URL), json=request
        ).json()
        self._check_response(response)
        if "errorDescription" in response:
            exit("Error while Checking Balance %s" % response["errorDescription"])
        return response.get("balance", 0)

    def getAppStats(self, soft_id, mode):
        request = {"clientKey": self.client_key, "softId": soft_id, "mode": mode}
        response = self.session.post(
            urljoin(self.base_url, self.APP_STAT_URL), json=request
        ).json()
        self._check_response(response)
        return response

    def reportIncorrectImage(self, task_id):
        request = {"clientKey": self.client_key, "taskId": task_id}
        response = self.session.post(
            urljoin(self.base_url, self.REPORT_IMAGE_URL), json=request
        ).json()
        self._check_response(response)
        return response.get("status", False) != False

    def reportIncorrectRecaptcha(self, task_id):
        request = {"clientKey": self.client_key, "taskId": task_id}
        response = self.session.post(
            urljoin(self.base_url, self.REPORT_RECAPTCHA_URL), json=request
        ).json()
        self._check_response(response)
        return response["status"] == "success"


class BaseTask(object):
    def serialize(self, **result):
        return result


class FunCaptchaProxylessTask(BaseTask):
    type = "FunCaptchaTaskProxyless"
    websiteURL = None
    websiteKey = None
    time_sleep = 0.1

    def __init__(self, website_url, website_key, *args, **kwargs):
        self.websiteURL = website_url
        self.websiteKey = website_key
        super(FunCaptchaProxylessTask, self).__init__(*args, **kwargs)

    def serialize(self, **result):
        result = super(FunCaptchaProxylessTask, self).serialize(**result)
        result.update(
            {
                "type": self.type,
                "websiteURL": self.websiteURL,
                "websitePublicKey": self.websiteKey,
            }
        )
        return result
