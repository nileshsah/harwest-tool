import requests

from datetime import datetime
from bs4 import BeautifulSoup
from functools import lru_cache

requests.packages.urllib3.disable_warnings()


class AtcoderClient:
    SUBMISSION_URL = "https://atcoder.jp/contests/{contest_id}/submissions/{submission_id}"
    CONTEST_URL = "https://atcoder.jp/contests/{contest_id}/tasks/{problem_id}"
    PAGE_SIZE_LIMIT = 20

    def __init__(self, user_name):
        self.user = user_name
        self.session = requests.Session()

    @lru_cache(maxsize = PAGE_SIZE_LIMIT + 5)
    def __http_get(self, url):
        req = self.session.get(url, verify=False)
        if req.status_code != 200:
            raise AssertionError("Unable to fetch response from: " + url +
                                 " response code: " + req.status_code)
        return req


    def __get_url_content(self, url):
        return self.__http_get(url).content

    def __get_content_soup(self, url):
        return BeautifulSoup(self.__get_url_content(url), 'lxml')

    def get_problem_name(self, submission_url):
        sub_soup = self.__get_content_soup(submission_url)
        return sub_soup.findAll('div', {"class": 'panel panel-default'})[0] \
                       .findAll('td')[1].text

    @staticmethod
    def get_platform_name():
        return "AtCoder", "AC"

    def get_submission_code(self, contest_id, submission_id):
        submission_url = AtcoderClient.SUBMISSION_URL \
            .format(contest_id=contest_id, submission_id=submission_id)
        sub_soup = self.__get_content_soup(submission_url)
        submission_code = sub_soup.find('pre', attrs={"id": "submission-code"})
        if submission_code is None:
            return None
        return submission_code.text

    def get_contest_tags(self, problem_url):
        con_soup = self.__get_content_soup(problem_url)
        span_tags = con_soup.findAll('span', attrs={'class': 'tag-box'})
        return [x.text.strip() for x in span_tags]

    def get_user_submissions(self, page_index):
        # Fetch submission list for the user using Kenkoooo API
        base_url = "https://kenkoooo.com/atcoder/atcoder-api/results?user={}".format(
            self.user,
        )
        response = self.__http_get(base_url).json()
        if response is None or not len(response):
            raise ValueError("No submissions found for user " + self.user)
        response = sorted(response, key=lambda k: k['epoch_second'], reverse=True)

        submissions = []
        start_index = AtcoderClient.PAGE_SIZE_LIMIT * (page_index - 1)
        end_index = min(len(response), AtcoderClient.PAGE_SIZE_LIMIT * page_index)
        for index in range(start_index, end_index):
            # Row -> a dict of submission details
            row = response[index]
            if 'result' not in row.keys():
                continue
            if 'contest_id' not in row.keys():
                continue

            contest_id = row['contest_id']
            status = row['result']
            if status != "AC": continue  # Only process accepted solutions

            submission_id = int(row['id'])
            problem_id = row['problem_id']
            points = int(row['point'])
            tags_list = ["AtCoder", "*" + str(points)]
            problem_url = AtcoderClient.CONTEST_URL \
                .format(contest_id=contest_id, problem_id=problem_id)
            lang_name = row['language']

            # print(submission_id, contest_id, problem_name, lang_name, contest_url)

            timestamp = row['epoch_second']
            date_time_str = datetime.fromtimestamp(timestamp).strftime('%b/%d/%Y %H:%M')
            submission_url = AtcoderClient.SUBMISSION_URL \
                .format(contest_id=contest_id, submission_id=submission_id)

            submission = {
                'contest_id': contest_id,
                # 'problem_index': problem_index, @ enriched in workflow
                'problem_url': problem_url,
                # 'problem_name': problem_name, @ enriched in workflow
                'language': lang_name,
                'timestamp': date_time_str,
                'tags': tags_list,
                'submission_id': submission_id,
                'submission_url': submission_url,
                'platform': self.get_platform_name()[0]
            }
            submissions.append(submission)
        return submissions
