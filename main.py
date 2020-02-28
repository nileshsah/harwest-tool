from config import load_setup_data
from workflow import Workflow

if __name__ == '__main__':
    myflow = Workflow(load_setup_data())
    myflow.run(start_page_index=1)
