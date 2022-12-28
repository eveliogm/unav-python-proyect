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
            'domain':"",
            'name': "Moving Average Index",
            'window':14,
            'yaxis': "y2",
            'simple_col': "media_movil",
            'simple_hover':"y",
            'color':"#a85c32"

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
    
    def __set_domain(self,ind: str):
        if self.__config[ind]["pos"] == "below":
            self.__config[ind]["domain"] = self.__config["general"]["domain"]["two"]["below"]
        return True

    def __check_pos(self,ind: str, pos:str):
        b_result = True
        indicators = {}
        for key in self.__config["general"]["indicators"]:
            indicators[key] = self.__config[key]
        print(indicators)
        print(indicators.items())
        for key, value in indicators.items():
            if value["b_view"] and (value["b_view"]=="below") and (key != ind) and (pos == "below") :
                print(f"The indicator {key} was on the graph, delete it before adding the {ind} indicator")
                b_result = False

        return b_result
        
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
    def __add_indicator(self,df: pandas.DataFrame,ind:str,g_type:str):


        self.__config[ind]["pos"] = g_type
        if g_type == "on":
            self.__config[ind]["yaxis"] = "y1"
            self.__add_simple(df,ind)
            self.__create_simple_layout()
        elif g_type == "below":
            self.__config[ind]["yaxis"] = "y2"
            self.__add_simple(df,ind)
            self.__set_domain(ind)
            self.__create_multiple_layout(ind)
            
        self.__config["stock"]["b_view"] = True
        return True  
    
    def add_rsi(self,df: pandas.DataFrame):
        """
        Add gri configuration to a figure

        Parameters:
        df (pandas.DataFrame): dataframe that contains the column with numeric values to be calculated 
        g_type (str): graph type can be "over" for a line behind principal graph and "below" if you 
        want a separated indicator graph.

        Returns:
        bool: true if added false if not. 
        """
        if self.__check_pos("rsi","below"):
            self.__add_indicator(df,"rsi","below")
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
        if g_type in (["on","below"]):
            self.__add_indicator(df,"ma",g_type)
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
        b_below = False
        for b in self.__config["general"]["indicators"]:
            if  self.__config[b]["b_view"]:
                indicators.append(b)
                if self.__config[b]["pos"] == "below":
                    b_below = True
           
        if (len(indicators)==1) and b_below:
            self.__set_domain(indicators[0])
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
