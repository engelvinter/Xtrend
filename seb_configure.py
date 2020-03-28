import argparse

import seb.operations as op

def construct_parser():
    parser = argparse.ArgumentParser(description='Configures SEB fund data')
    parser.add_argument("fund_db_path", help="the path to where the fund data files are saved")
    parser.add_argument("fund_portfolio_file", help="the full path to a file containing a fund portfolio")
    return parser

if __name__ == "__main__":
    parser = construct_parser()
    args = parser.parse_args()
    op.save_settings(args.fund_db_path, args.fund_portfolio_file)
