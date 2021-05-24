import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

#중간고사대체과제

class Midterm:
    names = {
    'South_Korea' : 'Average population',
    'Japan' : 'Average population',
    'the_United_States' : 'Average population',
    'China' : 'Average population',
    'World_population' : 'Yearly growth'
    }

    gdp_names = {
    'South_Korea' : '1980',
    'Japan' : 'Inflation rate'
    }

    def __init__(self):
        self._root = []
        self._gdp_root = []
        self._dfP = pd.DataFrame()
        self._dfG = pd.DataFrame()
        self._new_dfP = pd.DataFrame()

    def DataCollection(self):
        #각 나라별 인구수 가져오기
        for k, v in Midterm.names.items():
            if 'World' in k:
                web_loc = f'https://en.wikipedia.org/wiki/{k}'
                parser = pd.read_html(web_loc, match = v)
                self._root.append(parser[0].astype('object'))
            else:
                web_loc = f'https://en.wikipedia.org/wiki/Demographics_of_{k}'
                parser = pd.read_html(web_loc, match = v)
                self._root.append(parser[0].iloc[:,:4].astype('object'))

        self._root[-1] = self._root[-1].iloc[:,:2]
        #한국과 일본의 GDP 가져오기
        for k, v in Midterm.gdp_names.items():
            loc = f'https://en.wikipedia.org/wiki/Economy_of_{k}'
            parse = pd.read_html(loc, match = v)
            self._gdp_root.append(parse[0].iloc[:,:3].astype('object'))
        return self._root, self._gdp_root

    def Preprocessing(self):
        #원하는 Column의 이름을 바꿔줌
        columns = ['K', 'J', 'U', 'C', 'W']
        i = 0
        for data in self._root:
            if i == 4: #world population인 경우
                data.columns = ['Year', 'Population']
            else:
                data.columns = ['Year', f'Population_{columns[i]}', f'Birth_{columns[i]}', f'Death_{columns[i]}']
            i += 1

        columns = ['K', 'J']
        for i in range(len(self._gdp_root)):
            self._gdp_root[i].columns = ['Year' , f'GDP_{columns[i]}[US$]', f'GDP_per_capita_{columns[i]}[US$]']

        self._root[0].iloc[-3:,0] = ['2018','2019', '2020']
        self._root[1].iloc[-1:,0] = self._root[1].iloc[-1:,0].str.strip('p')
        self._root[3].iloc[69, 0] = '2019'

        for i in range(len(self._root)):
            #print(f'{i} | {type(self.__root[i].Year[0])}')
            if type(self._root[i].Year[0]) == int:
                self._root[i].Year = self._root[i].Year.astype('str')
                #print(f'{i} | changed')

        return self._root, self._gdp_root

    def DataMerge(self):
        self._dfP = self._root[1].merge(self._root[0], how = 'outer', on = 'Year')
        self._dfP = self._dfP.merge(self._root[2], how = 'outer', on = 'Year')
        self._dfP = self._dfP.merge(self._root[3], how = 'outer', on = 'Year')
        self._dfP = self._dfP.merge(self._root[4], how = 'outer', on = 'Year')

        self._dfG = self._gdp_root[0].merge(self._gdp_root[1], how = 'outer', on = 'Year')
        return self._dfP, self._dfG

    def RemoveFootnote(self):
        ind, col = self._dfP.shape #ind와 col 값을 얻어서 데이터 하나하나 확인하는 것
        for c in range(1, col):
            for i in range(ind):
                datum = str(self._dfP.iloc[i, c]).replace(',', '').rfind('[')
                #데이터에서 ,를 찾고 
                if datum != -1:
                    self._dfP.iloc[i, c] = float(str(self._dfP.iloc[i, c]).replace(',', '')[ : datum])
                    #print(f"({i},{c}) | {datum} | {self._dfP.iloc[i, c]}")
                elif type(self._dfP.iloc[i, c]) == str:
                    try:
                        self._dfP.iloc[i, c] = int(self._dfP.iloc[i, c])
                    except:
                        self._dfP.iloc[i, c] = int(str(self._dfP.iloc[i, c]).replace(',', ''))

    def DataVisualization(self, norm = False, plotting = 1):
        '''
        norm  = boolean
        Data Normalization option, default = False
        Normalization can be only used with plotting = 1, plotting = 2

        plotting = 1 or 2 or 3
        '''
        plt.style.use('seaborn')
        use = ['Population_K', 'Population_J', 'Population_U', 'Population_C', 'Population']
        title = ['Population of Korea', 'Population of Japan', 'Population of United States', 'Population of China', 'Population of World']
        # 인구수 그래프 그리기
        if norm == 0 and plotting == 1:
            for i in range(len(use)):
                plt.figure(figsize = (20, 20))
                self._dfP.plot(x = 'Year', y = use[i],
                                title = f'{title[i]}',
                                fontsize = 15)
                plt.xlabel('Year', fontsize = 15)
                plt.show();
        
        elif norm == 1 and plotting == 2:
            self._new_dfP = self._dfP.loc[:,['Year'] + use].dropna().reset_index(drop = True)
            self._new_dfP[use] = self._new_dfP[use].apply(lambda x: x/x[0])
            self._new_dfP = self._new_dfP.astype('float')
            plt.figure(figsize = (20, 20))
            self._new_dfP.plot(x = 'Year', y = use,
                                fontsize = 15)
            plt.title('Normalized Population', fontsize = 15)
            plt.ylabel(r'Population (${P_i / P_{1950}})$', fontsize = 15)
            plt.xlabel('Year', fontsize = 15)
            plt.show();

        #GDP 그래프 그리기
        elif plotting == 3:
            use = ['GDP_per_capita_K[US$]', 'GDP_per_capita_J[US$]']

            plt.figure(figsize = (20, 20))
            self._dfG.loc[:,['Year'] + use].plot(x = 'Year', y = use,
                                                  fontsize = 15)
            plt.xlabel('Year', fontsize = 15)
            plt.ylabel('GDP per Capita [US$]', fontsize = 15)
            plt.title('GDP per Capita of Korea and Japan', fontsize = 15)
            plt.show();


if __name__ == "__main__":
    midterm = Midterm()
    raw_root, raw_gdp_root = midterm.DataCollection() #자료수집
    root, gdp_root = midterm.Preprocessing() #자료정리
    root_m, gdp_root_m = midterm.DataMerge() #자료취합
    midterm.RemoveFootnote() #주석 및 str 형태를 int로 변경
    midterm.DataVisualization(norm = False, plotting = 1)
