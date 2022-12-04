import time

from feature_extract import extracting
from feature_match import matching


def main():
        start = time.time()

        extracting()
        matching()

        end = time.time()
        
        print("localization delay is " + f"{end - start:.10f} sec")

if __name__ == "__main__":
    main()