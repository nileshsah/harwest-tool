from lib.utils.config import load_setup_data
from lib.codeforces.workflow import CodeforcesWorkflow

if __name__ == '__main__':
    myflow = CodeforcesWorkflow(load_setup_data())
    myflow.run(start_page_index=1)
