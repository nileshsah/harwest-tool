import os
import shutil
import pystache
import datetime

from git import Repo

import config
from codeforces import CodeforcesClient


class Workflow:
    def __init__(self, user_data):
        self.user_data = user_data
        self.submissions_directory = user_data['directory']
        self.submission_json_path = os.path.join(self.submissions_directory, "submissions.json")
        self.readme_path = os.path.join(self.submissions_directory, "README.md")
        self.client = CodeforcesClient(user_data['username'])
        self.author = '{name} <{email}>'.format(name=user_data['name'], email=user_data['email'])
        self.submissions = config.load_submissions_data(self.submission_json_path)

    def __init_submissions_directory(self):
        if not os.path.exists(self.submission_json_path):
            git = Repo.init(self.submission_json_path).git
            shutil.copy2("readme.template", self.readme_path)
            git.add("README.md")
            git.commit(message="Initial commit with README.md", date="20 years ago", author=self.author)
        self.git = Repo.init(self.submissions_directory).git

    def __get_solution_path(self, submission):
        submission_lang = submission['language']
        lang_ext = config.get_language_extension(submission_lang)
        problem_code = submission['problem_name'].split()[0]
        solution_file_name = problem_code + "." + lang_ext
        solution_file_path = os.path.join(self.submissions_directory, "src",
                                          str(submission['contest_id']), solution_file_name)
        os.makedirs(os.path.dirname(solution_file_path), exist_ok=True)
        return solution_file_path

    @staticmethod
    def __to_git_path(path):
        return os.path.join(*path.split(os.sep)[1:])

    def __generate_readme(self, sub_list):
        submissions = sorted(
            sub_list,
            key=lambda s: datetime.datetime.strptime(s['timestamp'], '%b/%d/%Y %H:%M'),
            reverse=True
        )
        index = len(sub_list)
        rows = []
        for submission in submissions:
            row = str(index) + " | "
            row += '[{problem_name}]({problem_url}) | '.format(
                problem_name=submission['problem_name'],
                problem_url=submission['problem_url']
            )
            row += '[{lang}](./{path}) | '.format(
                lang=submission['language'],
                path=self.__to_git_path(self.__get_solution_path(submission))
            )
            row += ' '.join(['`{tag}`'.format(tag=x) for x in submission['tags']]) + " | "
            row += str(submission['timestamp']) + " | "
            rows.append(row)
            index -= 1
        template = open('readme.template', 'r').read()
        readme_data = pystache.render(template, {'submissions': "\n".join(rows)})
        with open(self.readme_path, 'w') as fp:
            fp.write(readme_data)

    def __add_submission(self, submission):
        submission_id = submission['submission_id']
        problem_url = submission['problem_url']
        if submission_id in self.submissions.keys():
            return False
        submission['tags'] = self.client.get_contest_tags(problem_url)
        solution_file_path = self.__get_solution_path(submission)
        solution_code = self.client.get_submission_code(contest_id=submission['contest_id'], submission_id=submission_id)
        with open(solution_file_path, 'w') as fp:
            fp.write(solution_code)
        self.submissions[submission_id] = submission
        self.__generate_readme(list(self.submissions.values()))
        config.write_submissions_data(self.submission_json_path, self.submissions)

        self.git.add(os.path.abspath(self.readme_path))
        self.git.add(os.path.abspath(solution_file_path))
        self.git.add(os.path.abspath(self.submission_json_path))

        commit_message  = "Add solution for problem `" + submission['problem_name'] + "`\n"
        commit_message += "Link: " + problem_url + "\n"
        commit_message += "Tags: " + ', '.join(submission['tags']) + "\n"
        commit_message += "Ref: " + submission['submission_url']
        self.git.commit(message=commit_message, date=submission['timestamp'], author=self.author)

        return True

    def run(self):
        self.__init_submissions_directory()
        last_page_index = self.client.get_submissions_page_count()
        for page_index in range(1, last_page_index + 1):
            print("Currently scanning page " + str(page_index) + " of " + str(last_page_index))
            submissions = self.client.get_user_submissions(page_index)
            response = [self.__add_submission(x) for x in submissions]
            if not any(response):
                break

myflow = Workflow(config.load_setup_data())
myflow.run()









