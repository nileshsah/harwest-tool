from bs4 import BeautifulSoup
import urllib
import datetime


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
        sub_url = "https://codeforces.com/contest/" + contest_id + "/submission/" + submission_id
        sub_soup = self.__get_content_soup(sub_url)
        submission_code = sub_soup.find('pre', attrs={'id': 'program-source-text'}).text
        return submission_code

    def get_contest_tags(self, contest_url):
        con_soup = self.__get_content_soup(contest_url)
        span_tags = con_soup.findAll('span', attrs={'class': 'tag-box'})
        return [x.text.strip() for x in span_tags]

    def get_user_submissions(self, page_index):
        base_url = "https://codeforces.com/submissions/" + self.user + "/page/" + str(page_index)
        soup = self.__get_content_soup(base_url)
        table = soup.find('table', attrs={'class': 'status-frame-datatable'})
        submissions = []

        rows = table.find_all('tr')
        for row in rows:
            if not row.has_attr('data-submission-id'): continue
            submission_id = row['data-submission-id']
            columns = row.find_all('td')

            status = columns[5].find('span', attrs={'class': 'verdict-accepted'})
            if status is None: continue

            contest_row = columns[3].find('a')
            contest_id = contest_row['href'].split('/')[2]
            problem_name = contest_row.text.strip()
            contest_url = "https://codeforces.com" + contest_row['href']

            lang_name = columns[4].text.strip()

            print(row['data-submission-id'])
            print(contest_id, problem_name, lang_name, contest_url)

            date_time_str = columns[1].find('span').text
            date_time_obj = datetime.datetime.strptime(date_time_str, '%b/%d/%Y %H:%M')
            print(date_time_obj)

            tags_list = self.get_contest_tags(contest_url)
            print(", ".join(tags_list))
            sub_url = "https://codeforces.com/contest/" + contest_id + "/submission/" + submission_id

            submission = {
                'contest_id': contest_id,
                'problem_url': contest_url,
                'problem_name': problem_name,
                'language': lang_name,
                'timestamp': date_time_str,
                'tags': tags_list,
                'submission_id': submission_id,
                'submission_url': sub_url,
                # 'submission_code': submission_code
            }
            submissions.append(submission)
        return submissions
