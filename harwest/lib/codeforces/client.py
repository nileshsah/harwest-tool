import urllib
import requests

from datetime import datetime
from bs4 import BeautifulSoup


class CodeforcesClient:
    def __init__(self, user_name):
        self.user = user_name

    @staticmethod
    def __get_url_content(url):
        return urllib.request.urlopen(url).read()

    def __get_content_soup(self, url):
        return BeautifulSoup(self.__get_url_content(url), 'lxml')

    def get_submissions_page_count(self):
        base_url = "https://codeforces.com/submissions/" + self.user
        sub_soup = self.__get_content_soup(base_url)
        pages = sub_soup.findAll('span', attrs={'class': 'page-index'})
        return int(pages[-1].find('a').text)

    def get_submission_code(self, contest_id, submission_id):
        sub_url = "https://codeforces.com/contest/{contest_id}/submission/{submission_id}".format(
            contest_id=contest_id,
            submission_id=submission_id
        )
        sub_soup = self.__get_content_soup(sub_url)
        # For debug purpose
        # print(sub_url)
        # open("last_submission_page.html", "w").write(str(sub_soup))
        submission_code = sub_soup.find('pre', attrs={'id': 'program-source-text'})
        if submission_code is None:
            return None
        return submission_code.text

    def get_contest_tags(self, problem_url):
        con_soup = self.__get_content_soup(problem_url)
        span_tags = con_soup.findAll('span', attrs={'class': 'tag-box'})
        return [x.text.strip() for x in span_tags]

    def get_user_submissions(self, page_index):
        base_url = "https://codeforces.com/api/user.status?handle={handle}&from={start_page}&count=50".format(
            handle=self.user,
            start_page=(page_index - 1) * 50 + 1
        )
        response = requests.get(base_url).json()
        if not response['status'] == "OK":
            raise ValueError("Error while fetching submissions: " + response)

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
            }
            submissions.append(submission)
        return submissions
