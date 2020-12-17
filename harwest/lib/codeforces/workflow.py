import os
from harwest.lib.utils import config

from harwest.lib.codeforces.client import CodeforcesClient
from harwest.lib.utils.repository import Repository
from harwest.lib.utils.submissions import Submissions


class CodeforcesWorkflow:
  def __init__(self, user_data):
    self.user_data = user_data
    self.submissions_directory = user_data['directory']
    self.client = CodeforcesClient(user_data['codeforces'])
    self.repository = Repository(self.submissions_directory)
    self.submissions = Submissions(self.submissions_directory)

  def __add_submission(self, submission):
    submission_id = submission['submission_id']
    submission['submission_id'] = "CF" + str(submission['submission_id'])
    if self.submissions.contains(submission['submission_id']):
      return False
    problem_url = submission['problem_url']
    submission['tags'] = self.client.get_contest_tags(problem_url)
    solution_file_path = self.__get_solution_path(submission)
    solution_code = self.client.get_submission_code(
      contest_id=submission['contest_id'], submission_id=submission_id)
    if solution_code is None:
      return False
    with open(solution_file_path, 'w') as fp:
      fp.write(solution_code)
    submission['path'] = self.__to_git_path(self.__get_solution_path(submission))

    self.submissions.add(submission)
    self.repository.add(solution_file_path)

    commit_message = "Add solution for problem `{problem_index} - {problem_name}`\n".format(
      problem_name=submission['problem_name'],
      problem_index=submission['problem_index']
    )
    commit_message += "Link: {problem_url}\n".format(problem_url=problem_url)
    commit_message += "Tags: {tags}\n".format(
      tags=', '.join(submission['tags']))
    commit_message += "Ref: {sub_url}".format(
      sub_url=submission['submission_url'])
    self.repository.commit(commit_message, submission['timestamp'])

    return True

  def __get_solution_path(self, submission):
    submission_lang = submission['language']
    lang_ext = config.get_language_extension(submission_lang)
    problem_code = submission['problem_index']
    solution_file_name = problem_code + "." + lang_ext
    solution_file_path = \
      os.path.join(self.submissions_directory, "codeforces",
                   str(submission['contest_id']), solution_file_name)
    os.makedirs(os.path.dirname(solution_file_path), exist_ok=True)
    return solution_file_path

  @staticmethod
  def __to_git_path(path):
    return os.path.join(*path.split(os.sep)[-3:])

  @staticmethod
  def __print_progress(submission, page_index, iteration, total, width):
    text = "\r\U0000231B  Currently scanning page #%d: (%d/%d) " \
           % (page_index, iteration, total)
    text += submission['problem_name'] + " " + submission['problem_url']
    print("\r", " " * width, end='\r')
    print(text, end='\r')
    return len(text)

  def run(self, start_page_index=1):
    print ("\U000026CF", "️Harvesting Codeforces (%s) Submissions to %s" %
           (self.user_data['codeforces'], self.submissions_directory))
    page_index = start_page_index
    try:
      while True:
        submissions = self.client.get_user_submissions(page_index)
        response = []
        last_width = 0
        for index, submission in enumerate(submissions):
          response.append(self.__add_submission(submission))
          last_width = self.__print_progress(
            submission, page_index, index + 1, len(submissions), last_width)
        if not len(response) or not any(response):
          break
        page_index += 1
    finally:
      print()

    self.repository.push()
    print("\U00002705", "The repository was successfully updated!")
