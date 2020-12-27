from harwest.lib.abstractworkflow import AbstractWorkflow
from harwest.lib.codeforces.client import CodeforcesClient


class CodeforcesWorkflow(AbstractWorkflow):
  def __init__(self, user_data):
    super().__init__(CodeforcesClient(user_data['codeforces']), user_data)

  def enrich_submission(self, submission):
    submission['tags'] = self.client.get_contest_tags(submission['problem_url'])
