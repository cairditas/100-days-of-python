
import csv
from numpy import average
import pandas as pd

data = pd.read_csv("weather.csv")

def read_csv():
    with open("weather.csv") as file:
        data = csv.reader(file)
        [print(row) for row in data]
    return data

def get_temperatures():
    with open("weather.csv") as file:
        data = csv.reader(file)
        temperatures = [int(row[1]) for row in data if row[1] != "temp"]
    return temperatures

def use_pd():
    data = pd.read_csv("weather.csv")
    print(data["temp"])

def data_to_dict():
    data = pd.read_csv("weather.csv")
    data_dict = data.to_dict()
    print(data_dict)

def average():
    print(data["temp"].mean())

def max():
    print(data["temp"].max())

def day_with_max_temp():
    print(data[data.temp == data.temp.max()].day)

def monday_temp_in_f():
    print(data[data.day == "Monday"].temp * 9/5 + 32)

def create_df():
    dd = {
        "students": ["Amy", "Todd", "Brian"], 
        "scores": [93, 85, 43]
    }

    d = pd.DataFrame(dd)
    d.to_csv("new.csv")
    print(d)

def squirrel():
    sd = pd.DataFrame(pd.read_csv("2018_sq.csv"))
    
    # Count all unique fur colors
    fur_color_counts = sd["Primary Fur Color"].dropna().value_counts().reset_index()
    fur_color_counts.columns = ['fur color', 'count']
    
    print(fur_color_counts)
    


if __name__ == "__main__":
    # data = read_csv()
    # print(get_temperatures())
    # use_pd()
    # data_to_dict()
    # average()
    # max()
    # day_with_max_temp()
    # monday_temp_in_f()
    # create_df()
    squirrel()