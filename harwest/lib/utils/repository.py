import os
import shutil
from harwest.lib.utils import config

from git import Repo, GitCommandError


class Repository:
  def __init__(self, submissions_directory):
    self.submissions_directory = submissions_directory
    self.submission_json_path = \
      os.path.join(self.submissions_directory, "submissions.json")
    self.readme_path = os.path.join(self.submissions_directory, "README.md")
    self.author = config.get_author()
    if not os.path.exists(self.submissions_directory):
      self.init()
    self.git = Repo(self.submissions_directory).git
    self.submissions = config.load_submissions_data(self.submission_json_path)

  def init(self):
    if not os.path.exists(self.submissions_directory):
      git = Repo.init(self.submissions_directory).git
      git.config("user.email", config.get_author_email())
      git.config("user.name", config.get_author_name())
      shutil.copy2(
        str(config.RESOURCES_DIR.joinpath("readme.template")),
        self.readme_path)
      git.add("README.md")
      git.commit(message="Initial commit with README.md",
                 date="Jan/01/2000 00:00", author=self.author)

  def add(self, file_path):
    self.git.add(os.path.abspath(file_path))
    self.git.add(os.path.abspath(self.readme_path))
    self.git.add(os.path.abspath(self.submission_json_path))

  def commit(self, commit_message, timestamp):
    self.git.commit(message=commit_message, date=timestamp, author=self.author)

  def push(self, force_push=False):
    remote_url = config.get_remote_url()
    if not remote_url:
      print("\U00002757", "The remote git repository url is not defined, skipping push")
    else:
      try:
        self.git.remote("add", "origin", remote_url)
      except GitCommandError: pass
      args = ["origin", "master"]
      if force_push:
        args.insert(0, "-f")
      self.git.push(*args)
      print("\U0001F44C", "The updates were automatically pushed to the remote repository")
