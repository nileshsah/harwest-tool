import os
from harwest.lib.utils import config

from harwest.lib.atcoder.client import AtcoderClient
from harwest.lib.utils.repository import Repository
from harwest.lib.utils.submissions import Submissions


class AtcoderWorkflow:
  def __init__(self, user_data):
    self.user_data = user_data
    self.submissions_directory = user_data['directory']
    self.client = AtcoderClient(user_data['atcoder'])
    self.repository = Repository(self.submissions_directory)
    self.submissions = Submissions(self.submissions_directory)


  def __add_submission(self, submission):
    submission_id = submission['submission_id']
    submission['submission_id'] = "AC" + str(submission['submission_id'])
    if self.submissions.contains(submission['submission_id']):
      return False
    problem_url = submission['problem_url']
    submission_url = submission['submission_url']

    submission['tags'] = ""

    solution_file_path = self.__get_solution_path(submission)

    solution_code = self.client.get_submission_code(submission_url=submission_url)
    
    # solution_code is a [source_code, problem_name]
    submission['problem_name'] = solution_code[1] # Get the problem name
    solution_code = solution_code[0] # Get the source_code

    if solution_code is None:
      return False
      
    with open(solution_file_path, 'wb') as fp:
      fp.write(solution_code.encode("utf-8"))
    submission['path'] = self.__to_git_path(self.__get_solution_path(submission))

    self.submissions.add(submission)
    self.repository.add(solution_file_path)


    commit_message = "Add solution for problem `{problem_name}`\n".format(
      problem_name=submission['problem_name'],
    )

    commit_message += "Link: {problem_url}\n".format(problem_url=submission['problem_url'])
    commit_message += "Ref: {sub_url}".format(
      sub_url=submission_url)
    self.repository.commit(commit_message, submission['timestamp'])

    return True

  def __get_solution_path(self, submission):
    submission_lang = submission['language']
    lang_ext = config.get_language_extension(submission_lang)
    problem_code = submission['problem_index']
    solution_file_name = problem_code + "." + lang_ext
    solution_file_path = \
      os.path.join(self.submissions_directory, "atcoder",
                   str(submission['contest_id']), solution_file_name)
    os.makedirs(os.path.dirname(solution_file_path), exist_ok=True)
    return solution_file_path

  @staticmethod
  def __to_git_path(path):
    return os.path.join(*path.split(os.sep)[-3:])




  @staticmethod
  def __print_progress(submission, iteration, total):
    text = "\r\U0000231B  Currently scanning : (%d/%d) " \
           % (iteration, total)
    text += submission['problem_index']
    print("\r", " ", end='\r')
    print(text, end='\r')
    return len(text)

  def run(self, start_page_index=1):
    print ("\U000026CF", "️Harvesting Atcoder (%s) Submissions to %s" %
           (self.user_data['atcoder'], self.submissions_directory))
    submission_index = start_page_index
    try:
      submissions = self.client.get_user_submissions(submission_index)
      for index, submission in enumerate(submissions):
        self.__add_submission(submission)
        last_width = self.__print_progress(submission, index + 1, len(submissions))
    except:
      print("Some Error Occured.")

    self.repository.push()
    print("\U00002705", "The repository was successfully updated!")
