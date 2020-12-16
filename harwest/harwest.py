# coding=utf-8

__version__ = "0.1.0"

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
  directory = input("Directory Name: ")
  path = os.path.join(os.getcwd(), directory)
  if os.path.exists(path):
    print("⚠️ WARNING! The directory with the path", path, "already exists.\n",
          "Please abort and enter a new directory name or ensure that the",
          "directory was previously created with this tool")
  config_dict = {
    'name': input("Author Name: "),
    'email': input("Author Email: "),
    'directory': directory
  }
  remote = input("(Optional) Remote URL: ")
  if len(remote):
    config_dict['remote'] = remote
  config.write_setup_data(config_dict)
  return config_dict


def codeforces(args):
  configs = config.load_setup_data()
  if not configs:
    configs = init()
  if args.setup or 'codeforces' not in configs:
    handle = input("Codeforces Handle Name: ")
    configs['codeforces'] = handle
    config.write_setup_data(configs)
  if not args.setup:
    CodeforcesWorkflow(configs).run(start_page_index=args.start_page)


def leetcode(args):
  print("Whoops, still in the making  ¯\\_(ツ)_/¯")


def main():
  parser = build_argument_parser()
  args = parser.parse_args()

  config_map = config.load_setup_data()
  if args.init or config_map is None:
    init()
  if 'func' in args:
    args.func(args)
  else:
    print("Please specify the platform to harvest, example: harwest codeforces")
