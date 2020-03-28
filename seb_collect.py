import argparse

import seb.operations as op

def construct_parser():
    parser = argparse.ArgumentParser(description='Collects SEB fund data')
    return parser

if __name__ == "__main__":
    parser = construct_parser()
    args = parser.parse_args()

    op.load_settings()
    op.collect()
