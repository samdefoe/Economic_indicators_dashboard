from data_retrieval import retrieve_all_data
from visualize_data import create_economic_dashboard
from dotenv import load_dotenv
import os
import time

if __name__ == '__main__':
    start = time.perf_counter()
    load_dotenv()
    retrieve_all_data()
    create_economic_dashboard()
    end = time.perf_counter()
    print(f"It took {end-start:.2f} seconds")

    

