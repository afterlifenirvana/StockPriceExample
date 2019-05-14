import csv
from dateutil.parser import parse
from datetime import timedelta
from fuzzywuzzy import process
import statistics

class StockAnalytics(object):
    # mode = csvreader, custom
    def __init__(self, csv_path, stock_code, mode="csvreader"):
        self.csv_path = csv_path
        self.stock_code = stock_code
        self.stock_codes = []
        self.codes = []
        self.data = {}
        self.match_status = False
        self.mode = mode
        self.csv_data = None
        self.dates_sorted = None
        self.start_date = None
        self.end_date = None
        self.final_list = []
        self.results = {
        }
        self.keys = {
            "stockname": 0,
            "stockdate": 1,
            "stockprice": 2
        }

    def load_data(self):
        if self.mode == "csvreader":
            self.default_csv_reader()
        else:
            self.custom_read_method()
  
    def match_found(self):
        return self.match_status

    def set_header_positions(self, headers):
        headers = [head.lower() for head in headers]
        for key in self.keys:
            try:
                self.keys[key] = headers.index(key)
                break
            except:
                print("Error searching default headers name switching to default header format \n StockPrice, StockData, StockPrice")
                
    def default_csv_reader(self):
        with open(self.csv_path) as file:
            reader = csv.reader(file)
            headers = next(reader)
            if not len(headers) == 3:
                print("Wrong header format for the stock file.")
                exit(1)
            self.set_header_positions(headers)
            for line_no, row in enumerate(reader):
                if str(row[self.keys["stockname"]]) == self.stock_code:
                    if self.match_status == False:
                        self.match_status = True
                    try:
                        values = {
                        parse(values[self.keys["stockdate"]]).date(): {
                            "price": float(values[self.keys["stockprice"]]),
                            "name": values[self.keys["stockname"]]
                        }
                    }
                    except Exception as e:
                        print(e)
                        print("Error while parsing line_no {}".format(line_no))
                    self.data.update(values)
                else:
                    self.codes.append((row[self.keys["stockname"]], line_no))

    def custom_read_method(self):
        with open(self.csv_path) as file:
            headers = file.readline().strip().split(",")
            self.set_header_positions(headers)
            if not len(headers) == 3:
                print("Wrong format for the stock file.")
                exit(1)
            for line_no, line in enumerate(file):
                self.read_csv_line(line, line_no)
                pass

    def read_csv_line(self, line, line_no):
        values = line.strip().split(",")
        if len(values) == 3:
            if self.stock_code == values[self.keys["stockname"]]:
                if self.match_status == False:
                    self.match_status = True
                try:
                    values = {
                        parse(values[self.keys["stockdate"]]).date(): {
                            "price": float(values[self.keys["stockprice"]]),
                            "name": values[self.keys["stockname"]]
                        }
                    }
                    self.data.update(values)
                except Exception as e:
                    print(e)
                    print("Error while parsing line {}".format(line_no))
            else:
                self.codes.append((values[self.keys["stockname"]], line_no))
        else:
            return None

    def get_close_matches(self):
        choices = (tup[0] for tup in self.codes)
        close_match = process.extractOne(self.stock_code, choices)
        if close_match[1] > 85:
            return close_match[0]
        else:
            None
    
    def accept_suggestion(self, suggestion):
        self.__init__(self.csv_path, suggestion, self.mode)
        self.load_data()        

    def check_dates_missing(self, start_date, end_date):
        # sort
        tmp = None
        tmp_dict = {}
        self.start_date = start_date
        self.end_date = end_date
        self.dates_sorted = sorted(self.data.keys())
        # check if data exist before start date
        tmp = self.return_match_or_prev(start_date)
        if tmp != None:
            pass
        else:
            self.start_date = self.dates_sorted[0]
            print("Stock Data for this start date doesn't exist. Everything will be calculated since the price for the stock is available.")
        st = self.start_date
        while st <= self.end_date:
            tmp  = self.return_match_or_prev(st)
            if tmp:
                tmp_dict[st] = self.data[tmp]
            st = st + timedelta(days=1)
        self.final_list = tmp_dict
        
                    
    def return_match_or_prev(self, date):
        prev = self.dates_sorted[0]
        for x in self.dates_sorted:
            if date == x:
                return x
            if date > x:
                prev = x
            elif (date < x) and (date > prev):
                return prev
                
    def run_analytics(self):
        if self.final_list:
            data = [self.final_list[x]["price"] for x in self.final_list]
            keys = list(self.final_list.keys())
            self.results["standard_deviation"] = statistics.stdev(data)
            self.results["mean"] = statistics.mean(data)
            profit = self.maxProfit(data, len(data))
            if profit:
                self.results["profit"] = profit[0]
                self.results["buy"] = (
                    keys[profit[1]], self.final_list[keys[profit[1]]]
                )
                self.results["sell"] = (
                    keys[profit[2]], self.final_list[keys[profit[2]]]  
                )

    def maxProfit(self, price, n):
        max_diff = price[1] - price[0]
        min_element = price[0]
        min_i = 0
        max_i = 1
        for i in range(1, n):
            if (price[i] - min_element > max_diff):
                max_diff = price[i] - min_element
                min_i = price.index(min_element)
                max_i = i
            if (price[i] < min_element):
                min_element = price[i]
        return (max_diff, min_i, max_i)

    def get_results(self):
       return self.results
    # Table to store results of subproblems  
    # profit[t][i] stores maximum profit  
    # using atmost t transactions up to  
    # day i (including day i)  
   

