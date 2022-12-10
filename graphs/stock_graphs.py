import pandas
import plotly.graph_objects as go
class stock_graphs():
    __data = {}
    __layout = {}
    __config = {
        'stock':
        {
            'b_view': False,
            'type': False,
            'stock_name':"",
            'currency_name':"",
            'simple_col': "close",
            'simple_hover':"y",
            'color': "#42C4F7",
            'yaxis': "y1"
        },
        'rsi':
        {
            'b_view': False,
            'pos':'below',
            'type': False,
            'domain':"",
            'name': "Relative Strength Index",
            'window':14,
            'yaxis': "y2",
            'simple_col': "rsi",
            'simple_hover':"y",
            'color':"#a85c32"
        },
        'ma':
        {
            
            'b_view': False,
            'pos':'below',
            'type': False,
            'name': "Moving Average",
            'window': 14

        },
        "general":
        {
            'n_graphs':0,
            'indicators':["rsi","ma"],
            'domain':
            { #config of the domain in the layout for diferent position
                'two':
                {
                    'below':
                    {
                        'yaxis_domain':[0.3, 1],
                        'yaxis2':{"domain": [0, 0.20]}
                    },
                     'over':
                    {
                        'yaxis_domain':[0, 0.20],
                        'yaxis2':{"domain": [0.3, 1]}
                    }
                },
                'three':
                {
                    'below':
                    {
                        'yaxis_domain':[0.4, 1],
                        'yaxis2':{"domain": [0, 0.10]},
                        'yaxis3':{"domain": [0.15, 0.30]}
                    },
                     'over':
                    {
                        'yaxis_domain':[0.2, 0.8],
                        'yaxis2':{"domain": [0, 0.10]},
                        'yaxis3':{"domain": [0.85, 1]}
                    }
                }
            }
        }
    }
    def __create_simple_layout(self):
        self.__layout = dict(
            autosize=True,
            xaxis_rangeslider_visible=True,
            showlegend=False,
        )
        return True
    def __create_multiple_layout(self,ind:str):
        self.__layout = dict(
            autosize=True,
            xaxis_rangeslider_visible=True,
            showlegend=False,
        )
        self.__layout.update(self.__config[ind]["domain"])
        return True
    
    def __add_simple(self,df: pandas.DataFrame,ind: str):
        self.__data[ind] = dict( 
            type="scatter",
            y=df[self.__config[ind]['simple_col']].values,
            x=df.index.values,
            yaxis=self.__config[ind]["yaxis"],
            line={"color": self.__config[ind]["color"]},
            hoverinfo=self.__config[ind]['simple_hover'],
            mode="lines",
        )
    
    def __get_pos(self,ind: str):
        mask = [self.__config[b]["b_view"] for b in self.__config["general"]["indicators"]]
        pos_n = [self.__config[b]["pos"] for b in self.__config["general"]["indicators"]]
        n_graphs = "two"
        conf = "below"
        if any(mask) & (~self.__config[ind]["b_view"]):
            n_graphs = "tree"
            if pos_n[mask] == "over":
                conf = "over"
                self.__config[ind]["pos"] = "below"
        self.__config[ind]["domain"] = self.__config["general"]["domain"][n_graphs][conf]
        return True
        
    def add_stock(self,df: pandas.DataFrame,g_type:str):
        """
        Add stock configuration to a figure

        Parameters:
        df (pandas.DataFrame): dataframe that contains the column with numeric values to be calculated 
        g_type (str): graph type can be "simple" for a line and "candels" if you want to change to candel type

        Returns:
        bool: true if added false if not. 
        """
        if g_type == "simple":
            self.__add_simple(df,"stock")
            self.__create_simple_layout()
        elif g_type == "candels":
            #draw candels
            True
        self.__config["stock"]["b_view"] = True
        return True
    

    
    def add_rsi(self,df: pandas.DataFrame,g_type:str):
        """
        Add gri configuration to a figure

        Parameters:
        df (pandas.DataFrame): dataframe that contains the column with numeric values to be calculated 
        g_type (str): graph type can be "over" for a line behind principal graph and "below" if you 
        want a separated indicator graph.

        Returns:
        bool: true if added false if not. 
        """
        self.__config["stock"]["pos"] = g_type
        if g_type == "on":
            self.__config["rsi"]["yaxis"] = "y1"
            self.__add_simple(df,"rsi")
            self.__create_simple_layout()
        elif g_type == "below":
            self.__config["rsi"]["yaxis"] = "y2"
            self.__add_simple(df,"rsi")
            self.__get_pos("rsi")
            self.__create_multiple_layout("rsi")
            
        self.__config["stock"]["b_view"] = True
        return True
    
    def add_ma(self,df: pandas.DataFrame,g_type:str):
        """
        Add ma configuration to a figure

        Parameters:
        df (pandas.DataFrame): dataframe that contains the column with numeric values to be calculated 
        g_type (str): graph type can be "over" for a line behind principal graph and "below" if you 
        want a separated indicator graph.

        Returns:
        bool: true if added false if not. 
        """
        if g_type == "on":
            #add line behind (addTrace)
            True
        elif g_type == "below":
            #adline separate (addScatter)
            True
        return True

    def update_graph(self):
        
        if "stock" not in self.__data.keys():
            raise KeyError("At least need stock data to update the graph, add it")

        return go.Figure(
            data = list(self.__data.values()),
            layout= self.__layout,
        )

    def __update_layout(self):
        indicators = []
        for b in self.__config["general"]["indicators"]:
            if  self.__config[b]["b_view"]:
                indicators.append(b)
        if (len(indicators)==1) and (self.__config[indicators[0]]["pos"]!="on"):
            self.__get_pos(indicators[0])
            self.__create_multiple_layout(indicators[0])
        else:
            self.__create_simple_layout()
        return True

    def delete_indicator(self,indicator):
        
        if indicator not in self.__data.keys():
            raise KeyError(f"Cannot Delete what not exist: {indicator} not added")
        self.__data.pop(indicator)
        self.__config[indicator]["b_view"] = False
        self.__update_layout()
        return True
