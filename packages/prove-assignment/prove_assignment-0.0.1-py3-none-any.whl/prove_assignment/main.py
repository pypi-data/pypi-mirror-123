import pandas as pd
import yfinance as yf
import datetime



class Project():
    def __init__(self) -> None:
        start_stream = datetime.datetime(2018,1,1)
        end_stream = datetime.datetime(2020,10,1)
        # downloading Apple adj closes
        s = 'AAPL'
        print("[] downloading\t -> ", end = "")
        self.data = yf.download(s, start = start_stream, end = end_stream)
        print("Done")
        # for test only
        a = pd.DataFrame()
        print(a)

    def get_data_adj(self):
        return self.data['Adj Close']
    
    def get_data_volume(self):
        return self.data['Volume']


if __name__ == "__main__":
    print('Creating Project')
    main = Project()
    print('Created')

    adj = main.get_data_adj()
    print(adj)
    vol = main.get_data_volume()
    print(vol)
