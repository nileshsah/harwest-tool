import requests

from datetime import datetime
from bs4 import BeautifulSoup
from functools import lru_cache

requests.packages.urllib3.disable_warnings()


class CodechefClient:
    CODE_URL = "https://www.codechef.com/viewplaintext/{submission_id}"
    PAGE_URL = "https://www.codechef.com/recent/user?page={page_number}&user_handle={handle_name}"
    SUBMISSIONS_URL = "https://www.codechef.com/{contest_id}/status/{problem_id},{handle_name}?status=15"
    CONTEST_URL = "https://www.codechef.com/api/contests/{contest_id}/problems/{problem_id}"
    PAGE_SIZE_LIMIT = 12

    def __init__(self, user_name):
        self.user = user_name
        self.session = requests.Session()

    @lru_cache(maxsize=PAGE_SIZE_LIMIT * 2)
    def __http_get(self, url):
        req = self.session.get(url, verify=False)
        if req.status_code != 200:
            raise AssertionError("Unable to fetch response from: " + url +
                                 " response code: " + str(req.status_code))
        return req

    def __get_url_content(self, url):
        return self.__http_get(url).content

    def __get_content_soup(self, url):
        return BeautifulSoup(self.__get_url_content(url), 'lxml')

    def get_problem_name(self, problem_url):
        response = self.__http_get(problem_url).json()
        return response['problem_name']

    @staticmethod
    def get_platform_name():
        return "CodeChef", "CC"

    def get_submission_id(self, contest_id, problem_id):
        submissions_url = CodechefClient.SUBMISSIONS_URL.format(
            contest_id=contest_id, problem_id=problem_id, handle_name=self.user) \
            .replace('m//', 'm/')
        sub_soup = self.__get_content_soup(submissions_url)
        return int(sub_soup.findAll('td', attrs={"width": "60"})[0].text)

    def get_submission_code(self, contest_id, submission_id):
        submission_url = CodechefClient.CODE_URL.format(submission_id=submission_id)
        submission_code = self.__get_content_soup(submission_url)
        if submission_code is None:
            return None
        return submission_code.text.strip()

    def get_problem_tags(self, problem_url):
        tags_html = self.__http_get(problem_url).json()['tags']
        tags_soup = BeautifulSoup(tags_html, 'lxml')
        return [tag.text.strip() for tag in tags_soup.findAll(
            'a', attrs={'class': 'problem-tag-small'})]

    def get_user_submissions(self, page_index):
        # Fetch submission list for the user using Kenkoooo API
        base_url = CodechefClient.PAGE_URL.format(
            page_number=page_index - 1,
            handle_name=self.user
        )
        response = self.__http_get(base_url).json()
        if response is None or not len(response):
            raise ValueError("No submissions found for user " + self.user)

        max_length = response['max_page']

        submissions = []
        start_index = CodechefClient.PAGE_SIZE_LIMIT * (page_index - 1)
        end_index = min(max_length, CodechefClient.PAGE_SIZE_LIMIT * page_index)
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



client = CodechefClient('nellex')
print (client.get_problem_name('https://www.codechef.com/api/contests/SEPT19A/problems/FUZZYLIN'))
print (client.get_problem_tags('https://www.codechef.com/api/contests/SEPT19A/problems/FUZZYLIN'))
print (client.get_submission_id('COOK77', 'CHEFARRB'))
print (client.get_submission_code('', 3672267))

