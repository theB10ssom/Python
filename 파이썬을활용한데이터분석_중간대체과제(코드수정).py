import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
from matplotlib.ticker import FormatStrFormatter


class Midterm:
    def __init__(self):
        self.root = {}
        self.names = ['South_Korea', 'Japan', 'the_United_States', 'World_population']
        self._dfP = pd.DataFrame()
        self._dfG = pd.DataFrame()

    def get_data_info(self):
        for i in self.names:
            if 'World' in i:
                self.root[i] = ('Yearly growth', f'https://en.wikipedia.org/wiki/{i}')
            else:
                self.root[i] = ('Average population', f'https://en.wikipedia.org/wiki/Demographics_of_{i}')


    def collect_data(self):
        for k, v in self.root.items():
            parser = pd.read_html(v[1], match = v[0])
            if 'World' in k:
                self.root.update({k : parser[0].iloc[:,:2].astype('object')})
            else:
                self.root.update({k : parser[0].iloc[:,:4].astype('object')})
        return self.root

class Preprocess:
    def __init__(self, data):
        self.data = data
        self.base = pd.DataFrame()

    def rename_data(self):
        columns = ['K', 'J', 'U', 'W']
        for i, k in enumerate(self.data):
            if "World" in k:
                self.data[k].columns = ['Year', 'Population']
            else:
                self.data[k].columns = ['Year', f'Population_{columns[i]}',
                                        f'Birth_{columns[i]}', f'Deaths_{columns[i]}']

    def remove_footnote(self):
        for k in self.data:
            self.data[k] = self.data[k].replace('\[[^)]*\]',"",regex=True)
            self.data[k] = self.data[k].replace(',','')
        return self.data

    def merge_data(self):
        try:
            dfs = [v for v in self.data.values()]
            self.base = reduce(lambda left, right : pd.merge(left, right,
                                                            on=['Year'], how='outer'), dfs)
        
        except:
            dfs = [v.astype('object') for v in self.data.values()]
            self.base = reduce(lambda left, right : pd.merge(left, right,
                                                             on=['Year'], how='outer'), dfs)

        return self.base


if __name__ == "__main__":
    m = Midterm()
    m.get_data_info()
    data = m.collect_data()

    p = Preprocess(data)
    p.rename_data()
    df = p.remove_footnote()
    dfP = p.merge_data()
