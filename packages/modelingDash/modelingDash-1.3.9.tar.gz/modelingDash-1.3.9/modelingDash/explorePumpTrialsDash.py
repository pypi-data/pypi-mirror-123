from dorianUtils.dashTabsD import TabMaster
from dorianUtils.dccExtendedD import DccExtended
import dash
import dash_core_components as dcc, dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd,numpy as np
import plotly.express as px, plotly.graph_objects as go

from modelingDash.configModelisation import ConfigModelisation

class PumpTrialsMaster(TabMaster):

    def __init__(self,app,baseId,folderCsv):
        super().__init__(app,baseId)
        self.folderCs  = folderCsv
        self.cfg  = ConfigModelisation(folderCsv)

    def load_DF(self,namePump,gasUsed,typePump,trial):
        filename = self.cfg.findFilename(namePump,gasUsed,typePump,trial,ext='.pkl')
        print(filename)
        df = self.cfg.loadFile(filename)
        return df,filename

    def addWidget(self,dicWidgets):
        widgetLayout,dicLayouts = [],{}
        for wid_key,wid_val in dicWidgets.items():
            if 'dd_namePump' in wid_key:
                self.dccE.dropDownFromList(self.baseId + wid_key,self.cfg.infoFiles['namePump'].unique(),
                'Select your pump : ',defaultIdx=0)
            if 'dd_gasUsed' in wid_key:
                self.dccE.dropDownFromList(self.baseId + wid_key,self.cfg.infoFiles['gasUsed'].unique(),
                    'Select the gas used : ',defaultIdx=0)
            if 'dd_typePump' in wid_key:
                self.dccE.dropDownFromList(self.baseId + wid_key,self.cfg.infoFiles['typePump'].unique(),
                    'Select modified  or origin : ',defaultIdx=0)
            if 'dd_trial' in wid_key:
                self.dccE.dropDownFromList(self.baseId + wid_key,self.cfg.infoFiles['detailTrial'].unique(),
                    'Select the trial : ',defaultIdx=0)
            if 'dd_typeGraph' in wid_key:
                self.dccE.dropDownFromList(self.baseId + 'dd_typeGraph',['standard','severalYaxis'],
                    'Select the type of graph : ',defaultIdx=1)
            if 'dd_gasUsed' in wid_key:
                self.dccE.dropDownFromList(self.baseId + 'dd_x',self.col_options,
            'x : ',value='Temps (s)')
            if 'dd_gasUsed' in wid_key:
                self.dccE.dropDownFromList(self.baseId + 'dd_y',self.col_options,
                    'y : ',value=['massflow (m3/s)'],multi=True)

        for widObj in widgetObj:widgetLayout.append(widObj)
        return widgetLayout


class ExplorePumpTrialsDash(PumpTrialsMaster):
    def __init__(self,app,folderCSV,baseId='eptd0_'):
        super().__init__(app,baseId,folderCSV)
        self.dimensions = ["x", "y"]
        self.filterFile = ["namePump", "gasUsed","typePump","trial"]
        self.GasUsedOpt,self.typePumpOpt,self.trialOpt,self.col_options = [],[],[],[]
        self.tabLayout = self.exploreDFLayout()
        self.tabname = 'explore pumps trials'
        self._define_callbacks()

    def exploreDFLayout(self,widthG=85):
        layoutExplore = html.Div(
            [
                html.Div(
                    self.dccE.dropDownFromList(self.baseId + 'dd_namePump',self.cfg.infoFiles['namePump'].unique(),
                        'Select your pump : ',defaultIdx=0) +
                    self.dccE.dropDownFromList(self.baseId + 'dd_gasUsed',self.cfg.infoFiles['gasUsed'].unique(),
                        'Select the gas used : ',defaultIdx=0) +
                    self.dccE.dropDownFromList(self.baseId + 'dd_typePump',self.cfg.infoFiles['typePump'].unique(),
                        'Select modified  or origin : ',defaultIdx=0) +
                    self.dccE.dropDownFromList(self.baseId + 'dd_trial',self.cfg.infoFiles['detailTrial'].unique(),
                        'Select the trial : ',defaultIdx=0) +
                    self.dccE.dropDownFromList(self.baseId + 'dd_typeGraph',['standard','severalYaxis'],
                        'Select the type of graph : ',defaultIdx=1) +
                    self.dccE.dropDownFromList(self.baseId + 'dd_x',self.col_options,
                        'x : ',value='Temps (s)') +
                    self.dccE.dropDownFromList(self.baseId + 'dd_y',self.col_options,
                        'y : ',value=['massflow (m3/s)'],multi=True) +
                    [html.P('slider x :'),dcc.RangeSlider(self.baseId + 'rs_x',
                                                    min=0,max = 1,step=0.001,value=[0,1],allowCross=False)]+

                    self.dccE.dropDownFromList(self.baseId + 'dd_mg',['lines','markers','lines+markers'],
                    'mode graph : ',defaultIdx=2)+

                    [html.P('skip points: '),dcc.Input(id=self.baseId + 'in_skip',placeholder='skip points : ',type='number',value=250)]+
                    [html.P('marker size: '),dcc.Input(id=self.baseId + 'in_ms',placeholder='marker size : ',type='number',value=10)]+
                    [html.P('marker line width: '),dcc.Input(id=self.baseId + 'in_mlw',placeholder='marker line width',type='number',value=1)]+
                    [html.P('axis space'),dcc.Input(id=self.baseId + 'in_inc',placeholder='axis space',type='number',value=1)]
                    ,style={"width": str(100-widthG) + "%", "float": "left",'color':'blue','fontsize':15},
                ),
                dcc.Graph(id=self.baseId + "graph", style={"width": str(widthG) + "%", "display": "inline-block"}),
            ]
        )
        return layoutExplore

    def _define_callbacks(self):
        @self.app.callback(Output(self.baseId + 'dd_gasUsed', 'options'),
                            Input(self.baseId + 'dd_namePump','value'))
        def updateGas(namePump):
            l = self.cfg.getPossibleGasUsed(namePump)
            return [dict(label=x, value=x) for x in l]


        @self.app.callback(Output(self.baseId + 'dd_typePump', 'options'),
                            Input(self.baseId + 'dd_namePump','value'),
                            Input(self.baseId + 'dd_gasUsed','value'))
        def updatePumpType(namePump,gasUsed):
            l = self.cfg.getPossibleTypePump(namePump,gasUsed)
            return [dict(label=x, value=x) for x in l]


        @self.app.callback(Output(self.baseId + 'dd_trial', 'options'),
                            Input(self.baseId + 'dd_namePump','value'),
                            Input(self.baseId + 'dd_gasUsed','value'),
                            Input(self.baseId + 'dd_typePump','value'))
        def updateTrials(namePump,gasUsed,typePump):
            l = self.cfg.getPossibleTrial(namePump,gasUsed,typePump)
            return [dict(label=x, value=x) for x in l]


        @self.app.callback([Output(self.baseId + 'dd_' + d, "options") for d in self.dimensions],
                            Input(self.baseId + 'dd_trial', 'value'),
                            State(self.baseId + 'dd_namePump','value'),
                            State(self.baseId + 'dd_gasUsed','value'),
                            State(self.baseId + 'dd_typePump','value'))
        def updateDropdowns(trial,namePump,gasUsed,typePump):
            df,filename = self.load_DF(namePump,gasUsed,typePump,trial)
            return [[dict(label=x, value=x) for x in df.columns] for d in self.dimensions]


        listInputsG=['dd_typeGraph','dd_x','dd_y','in_skip','in_ms','in_mlw','in_inc','dd_mg']
        listStatesG=['dd_namePump','dd_gasUsed','dd_typePump','dd_trial','rs_x']

        @self.app.callback(Output(self.baseId + "graph", "figure"),
                    [Input(self.baseId + v, "value") for v in listInputsG],
                    [State(self.baseId + v, "value") for v in listStatesG],
                    )
        def make_figure(typeGraph,x, y,skip,ms,mlw,inc,modeG,pump,gas,typeP,trial,rsx):
            # self.cfg.utils.printListArgs(typeGraph,x, y,skip,ms,mlw,inc,pump,gas,typeP,trial)
            df,filename = self.load_DF(pump,gas,typeP,trial)
            df = df.iloc[::skip,:]
            if typeGraph == 'standard' :
                fig = px.scatter(df,x=x,y=y,height=900,title=filename.split('/')[-1])
            elif typeGraph == 'severalYaxis':
                df = df.set_index(x)
                if x in y : df[x]=df.index

                N = len(df)
                x1,x2=[df.index[max(0,int(k*N)-1)] for k in rsx]
                df = df[(df.index>x1)&(df.index<x2)]


                df=df.loc[:,y]
                print(df)
                self.cfg.utils.printListArgs(x, y)
                fig = self.cfg.utils.multiUnitGraph(df)
                fig.update_layout(height=900,title=filename.split('/')[-1],xaxis_title=x)
                fig.update_yaxes(showgrid=False)
                ################## to add ###############################3
            elif typeGraph == 'subplot' :
                fig = self.cfg.utils.goSubplots(df,x,y,inc=inc/100)
                ################## to add ###############################3
            fig.update_traces(mode=modeG, marker_line_width=mlw/10, marker_size=ms)
            return fig

class ComparePumpTrialsDash(PumpTrialsMaster):

    def __init__(self,app,folderCSV,baseId='cptd0_'):
        super().__init__(app,baseId,folderCSV)
        self.GasUsedOpt,self.typePumpOpt,self.trialOpt,self.col_options = [],[],[],[]
        self.tabLayout = self.compareEchellonsLayout()
        self.tabname = 'compare pump trials'
        self._define_callbacks()

    def compareEchellonsLayout(self,widthG=88):
        compareLayout = html.Div(
            [
                html.H1("Compare graphs"),
                html.Div(
                    self.dccE.dropDownFromList(self.baseId + 'dd_x',self.cfg.getColumnsDF(),'x',value='Temps (s)')+
                    self.dccE.dropDownFromList(self.baseId + 'dd_y',self.cfg.getColumnsDF(),'y',value='yield (%)')+
                    [
                        html.P('skip points: '),
                        dcc.Input(id=self.baseId + 'in_skip',placeholder='skip points : ',type='number',value=1),
                        html.P('marker size: '),
                        dcc.Input(id=self.baseId + 'in_ms',placeholder='marker size : ',type='number',value=10),
                        html.P('marker line width: '),
                        dcc.Input(id=self.baseId + 'in_mlw',placeholder='marker line width',type='number',value=2)
                    ]+
                    self.dccE.dropDownFromList(self.baseId + 'dd_mg',['lines','markers','lines+markers'],
                    'mode graph : ',defaultIdx=2),
                    style={"width": str(100-widthG)  + "%", "float": "left",'color':'blue','fontsize':15}
                ),
                html.Div(

                    self.dccE.dropDownFromList(self.baseId + 'dd_listFiles',self.cfg.getValidFiles('echelon'),
                        'Select files : ',multi=True,value=self.cfg.getValidFiles('echelon')[3:4]) +
                    [dcc.Graph(id=self.baseId + "graph")],
                    style={"width": str(widthG)  + "%", "display": "inline-block"}),
            ]
        )
        return compareLayout

    def _define_callbacks(self):
        listInputsG=['dd_listFiles','dd_mg','dd_x','dd_y','in_skip','in_mlw','in_ms']
        @self.app.callback(Output(self.baseId + "graph", "figure"),
                    [Input(self.baseId + v, "value") for v in listInputsG],
                    )
        def make_figure(filenames,mg,x,y,skip,mlw,ms):
            df = self.cfg.get_AllsteadyStates([self.cfg.folderPkl + f for f in filenames])
            df=df.iloc[::skip]
            fig = px.scatter(df,x=x,y=y,color='filename',height=900)
            fig.update_traces(mode=mg, marker_line_width=mlw/10, marker_size=ms)
            fig.update_layout(font=dict(family="Courier New, monospace",size=18))
            return fig

class WobulationTrialsDash(PumpTrialsMaster):
    def __init__(self,folderData,app,baseId='wtd0_'):
        PumpTrialsMaster.__init__(self,app,baseId,folderData)
        self.listY = ['Consigne (pts ou mbars)','Sortie ana. 1 (pts)','Sortie ana. 2 (pts)','SLA5863s (l/h)',
                        'PR33X (mBar relatif non filtré)','PAA33X (mBar absolue non filtré)','Température (°C)','Courant (A)',
                        'pression rel.(Pa)','pression abs.(Pa)','massflow (m3/s)','electric power (W)','hydraulic power (W)','yield (%)']
        self.tabname = 'wobulation frequence'
        self.tabLayout = self._buildLayout()
        self._define_callbacks()

    def _buildLayout(self,widthG=85):
        dicWidgets = {
                        'btn_update':0,
                        'dd_resampleMethod' : 'mean',
                        'dd_style':'lines+markers','dd_typeGraph':'scatter',
                        'dd_cmap':'jet',
                        }
        basicWidgets = self.dccE.basicComponents(dicWidgets,self.baseId)
        specialWidgets = self.dccE.dropDownFromList(self.baseId + 'dd_y',self.listY,'y : ',value=['Sortie ana. 1 (pts)','PR33X (mBar relatif non filtré)'],multi=True)
        specialWidgets = specialWidgets+[html.P('nb pts :'),dcc.Input(self.baseId + 'in_pts',type='number',step=1,min=0,value=1000)]
        specialWidgets = specialWidgets + [html.P('slider x :'),dcc.RangeSlider(self.baseId + 'rs_x',
                                        min=0,max = 1,step=0.001,value=[0,1],allowCross=False)]
        specialWidgets = specialWidgets + [dcc.Checklist(id=self.baseId+'check_button',options=[{'label': 'Bode', 'value': 'bode'},{'label': 'Normalised', 'value': 'norm'}])]
        # reodrer widgets
        widgetLayout = basicWidgets+ specialWidgets
        listFilesWidget = dcc.Dropdown(id=self.baseId+'dd_listFiles',options=[{'label':t,'value':t} for t in self.cfg.getValidFiles('wobulationFreq')])
        graphLayout = html.Div([listFilesWidget]+[dcc.Graph(id=self.baseId+'graph')],style={"width": str(widthG)+"%", "display": "inline-block"})
        return [html.Div(widgetLayout,style={"width": str(100-widthG) + "%", "float": "left"}),graphLayout]

    def _define_callbacks(self):
        listInputsGraph = {
                        'dd_listFiles':'value',
                        'dd_y':'value',
                        'check_button':'value',
                        'btn_update':'n_clicks',
                        'dd_resampleMethod':'value',
                        'dd_typeGraph':'value',
                        'dd_cmap':'value',
                        'dd_style':'value'
                        }
        listStatesGraph = {
                            'graph':'figure',
                            'in_pts':'value',
                            'rs_x': 'value',
                            }
        @self.app.callback(
        Output(self.baseId + 'graph', 'figure'),
        [Input(self.baseId + k,v) for k,v in listInputsGraph.items()],
        [State(self.baseId + k,v) for k,v in listStatesGraph.items()],
        )
        def updateGraph(filename,ycols,checkBut,upBtn,rsMethod,typeGraph,cmap,style,fig,pts,rsx):
            # self.cfg.utils.printListArgs(filename,ycols,norm,upBtn,rsMethod,typeGraph,cmap,style,pts,rsx)
            ctx = dash.callback_context
            trigId = ctx.triggered[0]['prop_id'].split('.')[0]
            if not upBtn or trigId in [self.baseId+k for k in ['btn_update','dd_listFiles','dd_y']]:
                df = self.cfg.loadFile(self.cfg.folderPkl+filename)
                N = len(df)
                x1,x2=[df.index[max(0,int(k*N)-1)] for k in rsx]
                df = df[(df.index>x1)&(df.index<x2)]
                if pts==0 : inc=1
                else :
                    l = np.linspace(0,len(df),pts)
                    inc = np.median(np.diff(l))
                df = df[::int(np.ceil(inc))]
                if not checkBut:checkBut=[]
                if 'bode' in checkBut:
                    fig = self.cfg.bodePlot(df)
                else:
                    print(df)
                    fig = self.cfg.decomposeFrequenciesPlot(df,x='Temps (ms)',y=ycols,norm='norm' in checkBut)
            else :fig = go.Figure(fig)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(height=900)
            fig.update_traces(mode=style)
            return fig
