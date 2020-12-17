# coding=utf-8

import os
import argparse

from harwest.lib.utils import config
from harwest.lib.codeforces.workflow import CodeforcesWorkflow


def build_argument_parser():
  parser = argparse.ArgumentParser(
    description='Creates a repository of all the submissions from a given platform')
  parser.add_argument('-i', '--init', default=False, action='store_true',
                      help="Setup the local repository configuration")
  subparsers = parser.add_subparsers(
    help='The platform to scrape the solutions from')

  cf_parser = subparsers.add_parser(
    'codeforces', help="Scrape solutions from the codeforces platform")
  cf_parser.add_argument('-s', '--setup', default=False, action='store_true',
                         help="Setup the platform configurations")
  cf_parser.add_argument('-p', '--start-page', type=int, default=1,
                         help='The page index to start scraping from (default: 1)')
  cf_parser.set_defaults(func=codeforces)

  lc_parser = subparsers.add_parser(
    'leetcode', help="Scrape solutions from the leetcode platform")
  lc_parser.set_defaults(func=leetcode)

  return parser


def init():
  # Get directory details
  print("[1] We'll need to create a directory to store all your files\n",
        "   The directory will be created as", os.getcwd() + os.path.sep + "<your-input>")
  directory = input("> So, what would you like your directory to be called? ")
  path = os.path.join(os.getcwd(), directory)
  print("\U0001F44D", "Alright, so you're directory will be created at", path)
  if os.path.exists(path):
    print("\U000026A0", "WARNING! The directory with the path", path, "already exists.\n",
          "Please abort and enter a new directory name or ensure that the",
          "directory was previously created with this tool")

  # Get git commits author tag details
  print("\n[2] Then let's build your author tag which will appear in your Git commits as:\n",
        "   Author: Steve Jobs <steve.jobs@apple.com>")
  config_dict = {
    'name': input("> So what would your beautiful (Author) Full Name be? "),
    'email': input("> And of course, your magical (Author) Email Address? "),
    'directory': path
  }

  # Get remote git url for automated pushes
  print("\n[3] Guess what? We can automate the Git pushes for you too!", "\U0001F389", "\n"
        "   In case you'd like that, then please specify the remote Git Url for an \"empty\" repository\n"
        "   It would be somewhat like https://github.com/nileshsah/harwest-tool.git\n"
        "   But it's optional, in case you'd like to skip then leave it empty and just hit <enter>")
  remote = input("> (Optional) So, what would be the remote url for the repository again? ")
  if len(remote):
    config_dict['remote'] = remote
  config.write_setup_data(config_dict)

  print("\n", "\U0001F973", "You rock! We're all good to go now")
  return config_dict


def codeforces(args):
  configs = config.load_setup_data()
  if not configs:
    configs = init()
  if args.setup or 'codeforces' not in configs:
    handle = input("> So what's your prestigious Codeforces Handle Name? ")
    configs['codeforces'] = handle
    config.write_setup_data(configs)
  if not args.setup:
    CodeforcesWorkflow(configs).run(start_page_index=args.start_page)


def leetcode(args):
  print("Whoops, still in the making  ¯\\_(ツ)_/¯ Maybe you can help?")


def main():
  print("""
      __  __                              __
     / / / /___ _______      _____  _____/ /_
    / /_/ / __ `/ ___/ | /| / / _ \/ ___/ __/
   / __  / /_/ / /   | |/ |/ /  __(__  ) /_
  /_/ /_/\__,_/_/    |__/|__/\___/____/\__/

  ==========================================
  """)

  parser = build_argument_parser()
  args = parser.parse_args()

  config_map = config.load_setup_data()
  if args.init or config_map is None:
    if config_map is None:
      print("Hey there!", "\U0001F44B",
            "Looks like you're using Harwest for the first time."
            " Let's get you started", "\N{rocket}", "\n")
    init()
  if 'func' in args:
    args.func(args)
  else:
    print("Please specify the platform to har'w'est, example: `harwest codeforces`")
