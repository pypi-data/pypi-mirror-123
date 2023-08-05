import re, pandas as pd,datetime as dt,pickle, numpy as np, os
from dateutil import parser
from dorianUtils.configFilesD import ConfigMaster
from scipy.fft import fft, fftfreq
import scipy.signal as scisig
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from scipy.optimize import curve_fit

class ConfigModelisation(ConfigMaster):
    def __init__(self,folderCSV,folderPkl=None):
        super().__init__(folderCSV)
        self.folderCSV = folderCSV
        self.appDir  = os.path.dirname(os.path.realpath(__file__))
        self.confFolder = self.appDir +'/confFiles/'
        self.folderPkl = folderPkl
        if not self.folderPkl:self.folderPkl = self.folderCSV+'pkl/'
        self.filesCsv  = self.utils.get_listFilesPklV2(self.folderCSV,'*.csv')
        self.filesPkl  = self.utils.get_listFilesPklV2(self.folderPkl)
        self.infoFiles = self.__getInfosEssais__()

    def getColumnsDF(self):
        return list(self.loadFile(self.filesPkl[0]).columns)

    def getValidFiles(self,type,ext='.pkl'):
        filenames = list(self.infoFiles[self.infoFiles.typeTrial==type].filename)
        if ext=='.pkl':filenames = [f.split('/')[-1][:-4]+ext for f in filenames]
        return filenames

    def __getInfosEssais__(self):
        dates,nameEssais,namePump,GasUsed,typePump,detailTrial,typeTrial=[],[],[],[],[],[],[]
        for filename in self.filesCsv:
            infile      = open(filename, 'r',encoding='latin-1')
            dates.append(infile.readline().split(';')[1])
            bd = filename.split('_')
            namePump.append(bd[0].split('/')[-1])
            GasUsed.append(bd[1])
            typePump.append(bd[2])
            nameEssais.append(infile.readline().split(';')[1])
            detailTrial.append('_'.join(filename.split('_')[9:])[:-4])
            if re.findall('\d{1,5}hz',filename):
                typeTrial.append('wobulationFreq')
            elif 'triangle' in filename.lower():
                typeTrial.append('triangle')
            else :
                typeTrial.append('echelon')
            infile.close()
        df = pd.DataFrame([namePump,GasUsed,typePump,typeTrial,detailTrial,dates,nameEssais,self.filesCsv],
                            index= ['namePump','gasUsed','typePump','typeTrial','detailTrial','date','nameEssai','filename'])
        return df.transpose()

    def getPossibleGasUsed(self,namePump):
        return list(self.utils.combineFilter(self.infoFiles,['namePump'],[namePump]).gasUsed.unique())

    def getPossibleTypePump(self,namePump,gasUsed):
        return list(self.utils.combineFilter(self.infoFiles,['namePump','gasUsed'],[namePump,gasUsed]).typePump.unique())

    def getPossibleTrial(self,namePump,gasUsed,typePump):
        return list(self.utils.combineFilter(self.infoFiles,['namePump','gasUsed','typePump'],[namePump,gasUsed,typePump ]).detailTrial.unique())

    def findFilename(self,namePump,gasUsed,typePump,detailTrial,ext='.pkl'):
        # print(namePump,gasUsed,typePump,detailTrial)
        dfi=self.infoFiles
        dfp = dfi[dfi.namePump==namePump]

        dfg = dfp[dfp.gasUsed==gasUsed]
        if dfg.empty:
            print('trial : of '+ namePump,'has no trial with gas ' + gasUsed)
            print(dfp)
            return dfp

        dft = dfg[dfg.typePump==typePump]
        if dft.empty:
            print('trial : of '+ namePump + 'and gas ' + gasUsed +'has no trial with typePump ' + typePump)
            print(dfg)
            return dfg

        dfd = dft[dft.detailTrial==detailTrial]
        if dfd.empty:
            print('trial : of '+ namePump,'and gas ' + gasUsed + ' and typePump ' + typePump + 'has no trial with detailTrial ' + detailTrial)
            print(dft)
            return dft
        filename = dfd.filename.iloc[0]
        if ext == '.pkl' : filename = self.folderPkl+filename.split('/')[-1][:-4]+'.pkl'
        return filename

    def read_csv(self,filename,encode="latin-1",**kwargs):
        df = pd.read_csv(filename,sep=';',decimal=',',encoding=encode,low_memory=False,**kwargs)
        df = df.iloc[:,~df.columns.str.contains('Unnamed')]
        dateTrial=parser.parse(df.columns[1])
        df.index=[dateTrial+dt.timedelta(milliseconds=k) for k in df['Temps (ms)']]
        df = df.drop(df.columns[[0,1]],axis=1)
        return df

    def convert_csv2pkl(self):
        import os
        if not os.path.exists(self.folderPkl) : os.mkdir(self.folderPkl)
        for f in self.filesCsv:
            print(f)
            df = self.read_csv(f)
            df = self.computePhysics(df)
            filePkl = self.folderPkl + f.split('/')[-1][:-4] + '.pkl'
            print('saving pkl : ',filePkl)
            with open(filePkl , 'wb') as handle:
                pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def getUnits(self,listCols,pattern='unitsInParenthesis'):
        if pattern == 'unitsInParenthesis':
            return [re.findall('\([\w\W]+\)',x)[0][1:-1] for x in listCols]

    def computePhysics(self,df):
        df['Temps (s)']  = df.filter(regex='\(ms\)', axis=1)/1000
        df['pression rel.(Pa)'] = df.filter(regex='PR33X', axis=1)*100
        try : df['pression abs.(Pa)'] = df.filter(regex='PAA33X', axis=1)*100
        except: print('column containing PAA33X is absent in dataframe')
        try: df['massflow (m3/s)'] = df.filter(regex='\(l/h\)', axis=1)/3600/1000#m3/s
        except: print('column containing (l/h) is absent in dataframe')
        try : df['electric power (W)']  = 24*df.filter(regex='\(A\)', axis=1)
        except: print('column containing (A) is absent in dataframe')
        df['hydraulic power (W)'] = df['pression rel.(Pa)']*df['massflow (m3/s)']
        df['yield (%)'] = df['hydraulic power (W)']/df['electric power (W)']*100
        return df

    def getSteadyStates(self,df,trfinims=90100,lastPtsForMean = 100):
        dfSS = df[df['Temps (ms)']>trfinims] ## select only the data after a certain time to surpress the ramp
        if 'Consigne' in dfSS.columns : dfSS = dfSS[dfSS['Consigne'].diff()<-dfSS.Consigne.max()/20]
        elif 'Consigne (pts ou mbars)' in dfSS.columns : dfSS = dfSS[dfSS['Consigne (pts ou mbars)'].diff()<-dfSS['Consigne (pts ou mbars)'].max()/20]
        elif 'Sortie ana. (pts)' in dfSS.columns : dfSS = dfSS[dfSS['Sortie ana. (pts)'].diff()<-dfSS['Sortie ana. (pts)'].max()/20]
        else :
            print('Consigne ',',Consigne (pts ou mbars) ','et Sortie ana. (pts) ne sont pas des colonnes du df')
            return pd.DataFrame()
        if not dfSS.empty:
            dfSS=pd.concat([df.loc[k-dt.timedelta(seconds=6)] for k in dfSS.index],axis=1).transpose()
        return dfSS

    def get_AllsteadyStates(self,filenames):
        dfs = []
        for filename in filenames:
            print(filename)
            df = self.loadFile(filename)
            df = self.getSteadyStates(df)
            df['filename'] = filename.split('/')[-1]
            dfs.append(df)
            # print(df)
        dfT = pd.concat(dfs,axis=0)
        return dfT

    def plotCheckdfS(self,filePkl):
        import plotly.graph_objects as go

        df   = self.loadFile(filePkl)
        dfSS = self.getSteadyStates(df)
        trace1 = go.Scatter(x=dfSS.index,y=dfSS['Consigne'],name='sample',mode='markers',
                            marker=dict(symbol='circle',size=10))
        trace2 = go.Scatter(x=df.index,y=df['Consigne'],name='Consigne')
        fig = go.Figure([trace1,trace2])
        return fig

    def getSpeed(self,x,Pa,k,window=100,check=False):
        xt = x[window*(k-1):window*k]
        Pat = Pa[window*(k-1):window*k]
        N,T = len(xt), np.median(np.diff(xt))
        xf = fftfreq(N, T)[:N//2]*1000
        yf = fft(Pat)
        absfft=2.0/N * np.abs(yf[0:N//2])
        peaks,h = scisig.find_peaks(absfft,height=0.5,distance=10,prominence=0.5)
        h = h['peak_heights'].tolist()
        if len(h)>1:
            hmax = max(h)
            f_max = xf[peaks[h.index(hmax)]]
            speed = f_max*60
        else :speed=np.nan

        if check:
            fig = make_subplots(rows=1, cols=2,vertical_spacing=0.05)
            fig.add_trace(go.Scatter(x=xt, y=Pat,name='pression'),row=1, col=1)
            fig.add_trace(go.Scatter(x=xf, y=absfft,name='fft pression'),row=1,col=2),
            fig.add_trace(go.Scatter(x=xf[peaks], y=h,name='peaks',marker=dict(symbol='circle'),mode='markers'),row=1,col=2),
            fig.update_xaxes(title='frequence (hz)',row=1,col=2)
            fig.update_xaxes(title='temps(ms)',row=1,col=1)
            fig.show()
            return fig
        else : return speed

    def computeSpeedTrial(self,df,consigne='Sortie ana. (pts)',window=100):
        df = df.set_index('Temps (ms)')
        Pa = list(df['PR33X (mBar non filtré)'])
        x = df.index
        speeds,consignes,times,pressions = [],[],[],[]
        maxk = len(df)//window
        for k in range(1,maxk):
            # print(k)
            speed = self.getSpeed(x,Pa,k,window=window,check=False)
            speeds.append(speed)
            times.append(np.median(df.index[window*(k-1):window*k]))
            consignes.append(df[consigne].iloc[window*(k-1):window*k].mean())
            pressions.append(df['PR33X (mBar non filtré)'].iloc[window*(k-1):window*k].mean())

        dfT = pd.DataFrame([times,consignes,speeds,pressions]).transpose()
        dfT.columns = ['time (ms)','consigne','vitesse(N/min)','PR33X(mbar)']
        return dfT

    def decomposeFrequenciesPlot(self,df,x,y,ncol=4,norm=True):
        if not isinstance(y,list):y=[y]
        allFrequencies = list(df['Fréquence (Hz)'].unique())
        dfs = []
        for f in allFrequencies:
            dftmp = df[df['Fréquence (Hz)']==f]
            dftmp['Temps (ms)']=[k - dftmp['Temps (ms)'][0] for k in dftmp['Temps (ms)']]
            if norm:
                dftmp[y]=dftmp[y].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
            dfs.append(dftmp)
        df = pd.concat(dfs)
        fig = px.scatter(df,x=x,y=y,facet_col='Fréquence (Hz)',facet_col_wrap=ncol)
        fig.update_xaxes(matches=None)
        fig.update_yaxes(matches=None)
        return fig

    def fit_sin(self,tt, yy):
        '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
        tt = np.array(tt)
        yy = np.array(yy)
        ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
        Fyy = abs(np.fft.fft(yy))
        guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
        guess_amp = np.std(yy) * 2.**0.5
        guess_offset = np.mean(yy)
        guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])

        def sinfunc(t, A, w, p, c):  return A * np.sin(w*t + p) + c
        popt, pcov = curve_fit(sinfunc, tt, yy, p0=guess,bounds=[0,np.inf])
        A, w, p, c = popt
        f = w/(2.*np.pi)
        fitfunc = lambda t: A * np.sin(w*t + p) + c
        return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}

    def bodeDiagrammFromSineFit(self,df):
        fs = list(df['Fréquence (Hz)'].unique())
        dfs,resp,ress = [],{},{}
        for f in fs:
            print(f)
            dftmp = df[df['Fréquence (Hz)']==f].iloc[int(max(fs)//f):,:]
            p=dftmp['PR33X (mBar relatif non filtré)']
            t=(dftmp['Temps (ms)']-dftmp['Temps (ms)'][0])/1000
            s=dftmp['Sortie ana. 1 (pts)']
            try :
                resp[str(f)+'Hz']= self.fit_sin(t,p)
            except :
                resp[str(f)+'Hz']= {'amp':np.nan,'phase':np.nan,'offset':np.nan}
            ress[str(f)+'Hz']= self.fit_sin(t,s)

        offsets,amps,phases=[],[],[]
        for k,v in resp.items():
            offset  = v['offset']
            if v['offset']>40*0.9 and v['offset']<40*1.1:
                offsets.append(offset)
                amps.append(v['amp'])
                phases.append((v['phase']-ress[k]['phase'])*180/np.pi)
            else:
                offsets.append(np.nan)
                amps.append(np.nan)
                phases.append(np.nan)
        return fs,amps,phases,offsets

    def bodeDiagrammFromFFT(self,df):
        H   = fft(df['PR33X (mBar relatif non filtré)'].to_list())/fft(df['Sortie ana. 1 (pts)'].to_list())
        xt  = df['Temps (ms)']
        N,T = len(xt), np.median(np.diff(xt))
        f = df['Fréquence (Hz)']
        xf  = fftfreq(N, T)[:N//2]*1000
        mag = np.abs(H)
        phi = np.arctan(H.imag/H.real)*180/np.pi
        minf,maxf=f.min(),f.max()
        idx=[k for k in range(len(xf)) if xf[k]<maxf and xf[k]>minf]
        return xf[idx],mag[idx],phi[idx]

    def bodePlot(self,fs,amps,phases):
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        fig = make_subplots(rows=2,cols=1)
        fig.add_trace(go.Scatter(x=fs,y=amps,name='magnitude'),row=1,col=1)
        fig.add_trace(go.Scatter(x=fs,y=phases,name='phase(degrés)'),row=2,col=1)
        fig.update_xaxes(type="log")
        return fig

class ElectricMotors():
    def __init__(self,):
        from dorianUtils.utilsD import Utils
        self.utils=Utils()
        self.wikiLink='https://en.wikipedia.org/wiki/Brushed_DC_electric_motor'

    def modelingRonan(self,Kb=1,E=48):
        C = np.linspace(0,500,100) #Nm
        Cmax =  500#Nm

        Cv = 50
        I = Kb*(C+Cv)

        omega0 = 4000
        omega = omega0*(1 - C/Cmax)

        Pabs = E*I
        Pmeca = C*omega*2*np.pi/60 #W

        eta=Pmeca/Pabs
        etaN =eta/eta.max()
        PmecaN=Pmeca/Pmeca.max()
        omegaN=omega/omega.max()
        IN=I/I.max()
        PabsN=Pabs/Pabs.max()
        CN=C/C.max()
        return

    def plotRonan(self,):
        plts = [[omega,etaN  ,'g-' ,r'$\eta$'],
                [omega,PmecaN,'b--',r'$P_{meca}(W)$'],
                [omega,CN    ,'m',r'$C(Nm)$'],
                [omega,IN ,'r',r'$I(A)$']
                ]
        pathFig='moteurCurveSimulated.png'
        fig,ax = dsp.stddisp(plts,xylims=['y',-0.05,1.05],texts=[[3090,1.02,'$\eta_{max}$','g']],
            labs=[r'$N(tr/min)$','normalized unit'],lw=2,fonts={'lab':25},axPos=[0.2, 0.1,0.7,0.8],
            name=pathFig,opt='sc')
        dsp.addyAxis(fig,ax,[[omega,IN ,'r','']],'I(A)','r')

    def caraDC_Motor_SS(self,Kt,Ke,Ra,ei=24,torqueMax=50,N=1000):
        '''
        Kt : electromotric force (lorentz)
        Ke : induction (lenz) or couterelectromotric force
        Ra : resistance in Ohm
        ei : voltage in Volt
        '''
        df=pd.DataFrame()
        df['torque (Nm)'] = np.linspace(0,torqueMax,N)
        df['I (A)']=df['torque (Nm)']/Kt
        df['speed (rad/s)']=(ei-df['I (A)']*Ra)/Ke
        df['speed (tours/min)']=df['speed (rad/s)']/np.pi*60
        df['Mecanical power (W)']=df['torque (Nm)']*df['speed (rad/s)']
        df['Electrical power (W)']=df['I (A)']*ei
        df['yield (%)']=df['Mecanical power (W)']/df['Electrical power (W)']
        df = df.set_index('torque (Nm)')
        return df

    def plotElectricMotor(self,Kt,Ke,Ra,wiki=True,**kwargs):
        df = self.caraDC_Motor_SS(Kt=Kt,Ke=Ke,Ra=Ra,**kwargs)
        df=df[df['speed (tours/min)']>0]
        fig = self.utils.multiUnitGraph(df.iloc[:,[0,2,3,4,5]])
        fig = self.utils.updateStyleGraph(fig)
        params = {'Kt':Kt,'Ke':Ke,'Ra':Ra,}
        figname = 'electric motor characteristic ' + self.utils.figureName(params)
        fig = self.utils.quickLayout(fig,title=figname,xlab='torque(Nm)',style='std')
        fig.update_yaxes(showgrid=False)
        return fig

    def plotElectricMotorWiki(self,Kb,Rm,phi,**kwargs):
        df = self.brushedDCEquationsWiki(Kb,Rm,phi,**kwargs)
        df=df[df['speed (tours/min)']>0]
        fig = self.utils.multiUnitGraph(df.iloc[:,[0,3,4,6]])
        fig = self.utils.updateStyleGraph(fig)
        params = {'Kb':Kb,'Rm':Rm,'phi':phi}
        figname = 'electric motor characteristic ' + self.utils.figureName(params)
        fig = self.utils.quickLayout(fig,title=figname,xlab='torque(Nm)',style='std')
        fig.update_yaxes(showgrid=False)
        return fig

    def brushedDCEquationsWiki(self,Kb=1,Rm=1,phi=10,Tmax=10,Vm=24,N=50):
        df=pd.DataFrame()
        Kt = Kb/(2*np.pi)
        df['torque (Nm)'] = np.linspace(0,Tmax,N)
        df['current (A)']=df['torque (Nm)']/(Kt*phi)# torque equation(lorenz+pfd)
        df['emf (V)']=Vm-Rm*df['current (A)']#motor voltage equation
        df['speed (rad/s)']=df['emf (V)']/(Kb*phi)# motor counter emf equation(lenz)
        df['speed (tours/min)']=df['speed (rad/s)']/np.pi*60
        df['Mecanical power (W)']=df['torque (Nm)']*df['speed (rad/s)']
        df['Electrical power (W)']=df['current (A)']*Vm
        df['yield (%)']=df['Mecanical power (W)']/df['Electrical power (W)']
        df = df.set_index('torque (Nm)')
        return df

class ThermicIndicateurs():
    def __init__(self,):
        self.appDir  = os.path.dirname(os.path.realpath(__file__))
        self.confFolder = self.appDir +'/confFiles/'
        self.dfConstants =self.__loadConstants()
        self.dfMateriaux =self.__loadMaterials()
        self.vmol = 22.4#mol/L
        for k in self.dfConstants.index:
            setattr(self,k,self.dfConstants.loc[k].value)

    def __loadConstants(self):
        dfConstants=pd.read_excel(self.confFolder + 'Moulinette_preparation_manips_bruleur.xlsx',sheet_name='NomsExcel').iloc[:,[1,2,3,4]]
        dfConstants.columns=['description','variableName','value','unit']
        dfConstants = dfConstants.set_index('variableName')
        dfConstants = dfConstants[['value','description','unit']]
        dfConstants = dfConstants.dropna()
        return dfConstants

    def __loadMaterials(self):
        dfMaterials=pd.read_csv(self.confFolder + 'materials.csv')
        # dfMaterials.columns=['description','variableName','value','unit']
        dfMaterials = dfMaterials.set_index('Material')
        # dfMaterials = dfMaterials[['value','description','unit']]
        # dfMaterials = dfMaterials.dropna()
        return dfMaterials

    def fluxQfix(self,q_mol_s,dT,material='air'):
        M,Cp = self.dfConstants.loc['Mmol_'+material.capitalize(),'value'],self.dfConstants.loc['Cp_'+material,'value']
        return self.vmol*M*Cp*dT*q_mol_s

    def TmaxBruleur(self,debitH2In,courant,coefStock,debitO2BruleurIn,TinFuel ,TinAir):
        debitH2_mols = debitH2In/60/22.4 # mol/s
        debitConsoStack = courant-2 #mol/s ##### CHANGER FORMULE ICI #################
        debitH2BruleurIn=debitH2_mols-debitConsoStack

        debitO2In  = debitH2BruleurIn/2*coefStock #mol/s
        debitO2min =  debitO2In/21*100*60*22.4 #Nl/mn

        mCP_Fuel = debitH2BruleurIn*self.Mmol_H2*self.Cp_H2 #W/K
        mCP_Air = debitO2BruleurIn*self.Mmol_Air*self.Cp_air/60/22.4 #W/K

        T0BeforeCombustion = (mCP_Air*TinAir+mCP_Fuel*TinFuel)/(mCP_Air+mCP_Fuel)
        WthCombustion = debitH2BruleurIn*self.PCImol_H2

        mCP_vapCombustion = debitH2BruleurIn*self.Mmol_H2O*self.Cp_eau_vap
        mCP_airResiduel = (debitO2BruleurIn/60/22.4-debitH2BruleurIn/2)*self.Mmol_Air*self.Cp_air
        mCP_fuelResiduel = 0
        mCP_fumees = mCP_vapCombustion+mCP_airResiduel+mCP_fuelResiduel

        TmaxBruleur = T0BeforeCombustion + (WthCombustion/mCP_fumees)
        d={'debit H2 initial (Nl/mn)':debitH2In,'TmaxBruleur(°C)':TmaxBruleur,'T avant combustion (°C)':T0BeforeCombustion,
            'debitO2min(Nl/mn)':debitO2min,'W Combustion (W)':WthCombustion,}
        df = pd.DataFrame(d).set_index('debit H2 initial (Nl/mn)')
        return df

    def condenseur(self,T_in_condenseur,debit_eau,fuite,T_out_condenseur):
        g_s_fuites = debit_eau/60*(1-fuite)
        refroidissementVapeur = g_s_fuites*(T_in_condenseur-100)*self.Cp_eau_vap
        condensation = g_s_fuites*self.Cl_H2O
        refroidissementEauCond = g_s_fuites*self.Cp_eau_liq*(100-T_out_condenseur)
        thermicN2=3.9/60/22.4*self.Mmol_N2*self.Cp_N2*(T_in_condenseur-T_out_condenseur)*(1-fuite)
        df = pd.DataFrame({'g_s_fuites':g_s_fuites,'refroidissementVapeur':refroidissementVapeur,'condensation':condensation,
        'refroidissementEauCond':refroidissementEauCond,'thermicN2':thermicN2},index=[0])
        df['Total thermique'] = df.sum(axis=1)
        return df

    def solveHeatEquation2HotPlates1D(self,dt,dy,t_max,y_max,k,T1,T2,Ti):
        y = np.arange(0,y_max+dy,dy)
        t = np.arange(0,t_max+dt,dt)
        T = np.zeros([len(t),len(y)])
        ###### boundary conditions
        T[0,:] = Ti # temperature initiale
        T[:,0] = T1 # thermostat plaque 1
        T[:,-1] = T2 # thermostat plaque 2
        ###### resolution of differential equation
        for n in range(0,len(t)-1):
            for j in range(1,len(y)-1):
                # k = interpolate(k_air,T[n,j])
                s = k*dt/(dy**2)
                T[n+1,j] = T[n,j] + s*(T[n,j-1] - 2*T[n,j] + T[n,j+1])
        T = pd.DataFrame(T,columns=['y = {:.3f} mm'.format(1000*k) for k in y])
        T.index = t
        return T,s

    def flux2sources(self,T1=50+273,T2= 150+273,S=1,l=1.5,materiau='copper'):
        thermalLambda = self.dfMateriaux.loc[materiau,'Thermal conductivity [W·m−1·K−1]']
        a = np.abs(T2-T1)/l
        return a*S*thermalLambda
