import requests
import time

import codeforces_api
from datetime import datetime
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()


class CodeforcesClient:
    def __init__(self, user_name):
        self.user = user_name
        self.session = requests.Session()
        self.cf_api = codeforces_api.CodeforcesApi()
        self.cf_parser = codeforces_api.CodeforcesParser()

    def __get_url_content(self, url):
        return self.session.get(url, verify=False).content

    def __get_content_soup(self, url):
        return BeautifulSoup(self.__get_url_content(url), 'lxml')

    @staticmethod
    def get_platform_name():
        return "Codeforces", "CF"

    def get_submissions_page_count(self):
        base_url = "https://codeforces.com/submissions/" + self.user
        sub_soup = self.__get_content_soup(base_url)
        pages = sub_soup.findAll('span', attrs={'class': 'page-index'})
        return int(pages[-1].find('a').text)

    def get_submission_code(self, contest_id, submission_id):
        try:
            return self.cf_parser.get_solution(contest_id, submission_id)
        except Exception:
            return None

    def get_contest_tags(self, problem_url):
        con_soup = self.__get_content_soup(problem_url)
        span_tags = con_soup.findAll('span', attrs={'class': 'tag-box'})
        return [x.text.strip() for x in span_tags]

    def get_user_submissions(self, page_index):
        response = self.cf_api.user_status(self.user, (page_index - 1) * 50 + 1, 50)

        submissions = []
        for row in response['result']:
            if 'verdict' not in row.keys():
                continue
            if 'contestId' not in row.keys():
                continue
            if row['testset'] != "TESTS":
                continue

            contest_id = row['contestId']
            if contest_id > 100000: continue  # Ignore gym submissions

            status = row['verdict']
            if status != "OK": continue  # Only process accepted solutions

            submission_id = int(row['id'])

            problem = row['problem']
            problem_index = problem['index']
            problem_name = problem['name']
            tags_list = problem['tags']
            if 'rating' in problem:
                tags_list.append("*" + str(problem['rating']))

            contest_url = "https://codeforces.com/contest/{contest_id}/problem/{problem_index}".format(
                contest_id=contest_id,
                problem_index=problem_index
            )
            lang_name = row['programmingLanguage']

            # print(submission_id, contest_id, problem_name, lang_name, contest_url)

            timestamp = row['creationTimeSeconds']
            date_time_str = datetime.fromtimestamp(timestamp).strftime('%b/%d/%Y %H:%M')

            sub_url = "https://codeforces.com/contest/{contest_id}/submission/{submission_id}".format(
                contest_id=contest_id,
                submission_id=submission_id
            )
            submission = {
                'contest_id': contest_id,
                'problem_index': problem_index,
                'problem_url': contest_url,
                'problem_name': problem_name,
                'language': lang_name,
                'timestamp': date_time_str,
                'tags': tags_list,
                'submission_id': submission_id,
                'submission_url': sub_url,
                'platform': self.get_platform_name()[0]
            }
            submissions.append(submission)
        time.sleep(0.2) # You can make 5 requests per second to Codeforces API, so you need to wait for 0.2 seconds to avoid Call limit error.
        return submissions
