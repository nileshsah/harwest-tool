import requests

from datetime import datetime
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()

class AtcoderClient:
    def __init__(self, user_name):
        self.user = user_name

    @staticmethod
    def __get_url_content(url):
        return requests.get(url, verify=False).content

    def __get_content_soup(self, url):
        return BeautifulSoup(self.__get_url_content(url), 'lxml')

    def get_submission_code(self, submission_url):
        src = self.__get_content_soup(submission_url)
        src2 = src
        src  = src.findAll('pre')[0].text
        fname = src2.findAll('div',{"class":'panel panel-default'})[0].findAll('td')[1].text
        return [src,fname]


    def get_user_submissions(self, submission_index):

        #Fetch all submissions of a user
        base_url = "https://kenkoooo.com/atcoder/atcoder-api/results?user={}".format(
            self.user,
        )
        try:
            response = requests.get(base_url, verify=False).json()
        except:
            raise ValueError("Error while fetching submissions: " + response)

        submissions = []

        for i in range(submission_index,len(response)):

            # Row -> a dict of submission details
            row = response[i]


            if 'result' not in row.keys():
                continue
            if 'contest_id' not in row.keys():
                continue

            
            contest_id = row['contest_id'] ## Contest ID - eg. abc123,arc063
            status = row['result']  ## Verdict of submission

            if status != "AC": continue  # Only process accepted solutions

            submission_id = int(row['id']) ## Id of submission
            problem_index = row['problem_id'] ## ID/Code of a problem e.g abc145_d
            problem_url = "https://atcoder.jp/contests/{}/tasks/{}".format(contest_id,problem_index) # Url of the problem page

            submission_url = "https://atcoder.jp/contests/{}/submissions/{}".format(
                contest_id,
                submission_id
            ) ## Submission URL

            lang_name = row['language'] ## Submission Language

            # print(submission_id, contest_id, problem_name, lang_name, contest_url)

            timestamp = row['epoch_second'] ## Time of submission
            
            date_time_str = datetime.fromtimestamp(timestamp).strftime('%b/%d/%Y %H:%M')


            submission = {
                'contest_id': contest_id,
                'problem_index': problem_index,
                'problem_url':problem_url,
                'submission_url':submission_url,
                'language': lang_name,
                'timestamp': date_time_str,
                'submission_id': submission_id,
            }
            submissions.append(submission)
        return submissions
