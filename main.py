import os 
import argparse
from dateutil.parser import parse

from core import StockAnalytics

CSV_PATH = None
FLAG = True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Stock Analytics Program.")
    parser.add_argument("--path-csv", help = "Path to csv file for stock analytics", required = True)
    args = parser.parse_args()
    CSV_PATH = args.path_csv
    if not os.path.isfile(CSV_PATH):
        print("File doesn't exists at the given path.")
        exit(1)
    while FLAG:
        stock_code = input("Welcome Agent! Which stock you need to process ? :-")
        if stock_code == "":
            print("No stock code entered !")
            exit(1)
        sa = StockAnalytics(CSV_PATH, str(stock_code), mode="custom")
        sa.load_data()
        if not sa.match_found():
            suggestion = sa.get_close_matches()
            if suggestion:
                choice = input("Oops! Do you mean {}? y or n :- ".format(suggestion))
                if choice == "y":
                    sa.accept_suggestion(suggestion)
                else:
                    exit(1)
                pass
            else:
                print("Given Stock name not found !")
                exit(1)
        # Read file for the give code if not found suggest nearby one.
        start_date = input("From which date you want to start :- ")
        try:
            start_date = parse(start_date).date()
        except Exception as e:
            print("Unknown Date Format")
            exit(1)
        end_date = input("Till which date you want to analyze :- ")
        try:
            end_date = parse(end_date).date()
        except Exception as e:
            exit(1)
            print("Unknown Date Format")
        # Add missing dates, get mean, median  and sell dates
        sa.check_dates_missing(start_date, end_date)
        sa.run_analytics()
        if sa.get_results():
            results = sa.get_results()
            print("Mean for the selected date:- {} Standard Deviation for stock {}.\n Max Profit that can be achieved \
                :- {} by buying on {} at {} and selling on {} at {}".format(results["mean"], results["standard_deviation"], 
                results["profit"], results["buy"][0], results["buy"][1]["price"], results["sell"][0], results["sell"][1]["price"]
                ))
        choice = input("Do you want to analyze more stocks  ? y or no :- ")
        if choice == "n":
            FLAG = False
        else:
            FLAG = True

