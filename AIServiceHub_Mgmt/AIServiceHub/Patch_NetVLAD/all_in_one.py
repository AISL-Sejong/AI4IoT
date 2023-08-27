import time
import argparse

from feature_extract import extracting
from feature_match import matching


def main(source):
        start = time.time()

        extracting(source)
        matching(source)

        end = time.time()
        
        print("localization delay is " + f"{end - start:.10f} sec")

def parse_opt():
        parser = argparse.ArgumentParser(description='visualLocalization')
        parser.add_argument('--source', type=str, default= '{address}/AI4IoT/AIServiceHub_Mgmt/AIServiceHub/Patch_NetVLAD/patchnetvlad/mobius/union/PID2387754Image.jpg', help='query image path')
        opt = parser.parse_args()
        return opt

if __name__ == "__main__":
        opt = parse_opt()
        time.sleep(1)
        print(opt)
        main(opt.source)