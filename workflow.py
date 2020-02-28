import os
import shutil

from git import Repo, GitCommandError

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

    def __init_submissions_directory(self):
        if not os.path.exists(self.submissions_directory):
            git = Repo.init(self.submissions_directory).git
            shutil.copy2("readme.template", self.readme_path)
            git.add("README.md")
            git.commit(message="Initial commit with README.md", date="Jan/01/2000 00:00", author=self.author)
        self.git = Repo(self.submissions_directory).git
        self.submissions = config.load_submissions_data(self.submission_json_path)

    def __get_solution_path(self, submission):
        submission_lang = submission['language']
        lang_ext = config.get_language_extension(submission_lang)
        problem_code = submission['problem_index']
        solution_file_name = problem_code + "." + lang_ext
        solution_file_path = os.path.join(self.submissions_directory, "codeforces",
                                          str(submission['contest_id']), solution_file_name)
        os.makedirs(os.path.dirname(solution_file_path), exist_ok=True)
        return solution_file_path

    @staticmethod
    def __to_git_path(path):
        return os.path.join(*path.split(os.sep)[1:])

    def __generate_readme(self, sub_list):
        submissions = sorted(
            sub_list,
            key=lambda s: s['submission_id'],
            reverse=True
        )
        index = len(sub_list)
        rows = []
        for submission in submissions:
            row = str(index) + " | "
            row += '[{problem_index} - {problem_name}]({problem_url}) | '.format(
                problem_index=submission['problem_index'],
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
        readme_data = template.format(submission_placeholder="\n".join(rows))
        with open(self.readme_path, 'w') as fp:
            fp.write(readme_data)

    def __add_submission(self, submission):
        submission_id = submission['submission_id']
        problem_url = submission['problem_url']
        if str(submission_id) in self.submissions.keys():
            return False
        submission['tags'] = self.client.get_contest_tags(problem_url)
        solution_file_path = self.__get_solution_path(submission)
        solution_code = self.client.get_submission_code(contest_id=submission['contest_id'], submission_id=submission_id)
        with open(solution_file_path, 'w') as fp:
            fp.write(solution_code)
        self.submissions[str(submission_id)] = submission
        self.__generate_readme(list(self.submissions.values()))
        config.write_submissions_data(self.submission_json_path, self.submissions)

        self.git.add(os.path.abspath(self.readme_path))
        self.git.add(os.path.abspath(solution_file_path))
        self.git.add(os.path.abspath(self.submission_json_path))

        commit_message  = "Add solution for problem `{problem_index} - {problem_name}`\n".format(
            problem_name=submission['problem_name'],
            problem_index=submission['problem_index']
        )
        commit_message += "Link: {problem_url}\n".format(problem_url=problem_url)
        commit_message += "Tags: {tags}\n".format(tags=', '.join(submission['tags']))
        commit_message += "Ref: {sub_url}".format(sub_url=submission['submission_url'])
        self.git.commit(message=commit_message, date=submission['timestamp'], author=self.author)

        return True

    def run(self, start_page_index=1):
        self.__init_submissions_directory()
        page_index = start_page_index
        while True:
            print("Currently scanning page " + str(page_index))
            submissions = self.client.get_user_submissions(page_index)
            response = [self.__add_submission(x) for x in submissions]
            if not len(response) or not any(response):
                break
            page_index += 1

        if "remote" in self.user_data.keys():
            try: self.git.remote("add", "origin", self.user_data['remote'])
            except GitCommandError: pass
            # self.git.push("-f", "origin", "master") # Not recommended
            self.git.push("origin", "master")
