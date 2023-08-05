import dorianUtils.utilsD as utilsD
import importlib,numpy as np
from scipy import signal
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class UsefulCircuits():
    def __init__(self):
        self.utils=utilsD.Utils()


    def bodeFromTransferFunction(self,s,n=200,log=True):
        w, mag, phase = signal.bode(s,n=n)
        f = w/(2*np.pi)

        fig = make_subplots(rows=2,cols=1)
        fig.add_trace(go.Scatter(x=f,y=mag,name='magnitude'),row=1,col=1)
        fig.add_trace(go.Scatter(x=f,y=phase,name='phase(degrés)'),row=2,col=1)
        if log :
            fig.update_xaxes(type="log")
            fig.update_yaxes(type="log")
        fig.update_xaxes(matches='x')
        fig=self.utils.updateStyleGraph(fig)
        fig.update_layout(height=1000)

        denT='+'.join([str(k)+'s^'+str(s) for s,k in enumerate(s.den)])
        numT='+'.join([str(k)+'s^'+str(s) for s,k in enumerate(s.num)])
        HFormula = r'$H=\frac{' + np.flip(numT) + '}{' + np.flip(denT) + '}'
        fig = px.scatter(x=f,y=mag,title=HFormula)
        return fig

    def parameterTxts(self,params,joinCara='<br>',egal='=',fdec=2):
        listParams=[]
        fdec='{:.' + str(fdec) + 'f}'
        for k,v in params.items():
            tmp = ''
            if isinstance(v[0],int):tmp = k + egal + '{:d}'.format(v[0]) + ' ' + v[1]
            if isinstance(v[0],float):tmp=k + egal + fdec.format(v[0]) + ' ' + v[1]
            if isinstance(v[0],str):
                if len(v[0])>0 : tmp= k + egal +v[0] +' ' + v[1]
            if not not tmp:listParams.append(tmp)
        return joinCara.join(listParams)


    def RLC_Series(self,L=1e-2,C=1e-8,R=500,**kwargs):
        # series RLC
        num,den = [1/L,0],[1, R/L, 1/(L*C)]
        RLC_Series = signal.TransferFunction(num, den)
        fig = self.bodeFromTransferFunction(RLC_Series,**kwargs)

        w0 = 1/np.sqrt(L*C)
        f0 = w0/(2*np.pi)
        Q = 1/R*np.sqrt(L/C)
        params = {'w0':[w0,'s-1'],'f0':[f0,'Hz'],'Q':[Q,'']}

        fig.add_vline(x=f0, line_dash="dot",
                annotation_text=self.parameterTxts({'f0':[f0/1000,'kHz']}),
                annotation_position="bottom right",
                annotation_font_size=20,
                annotation_font_color="blue"
                        )
        fig.add_vrect(x0=f0*(1-1/(Q*2)), x1=f0*(1+1/(2*Q)),
            annotation_text=self.parameterTxts(params),
            fillcolor="green", opacity=0.25, line_width=0)
        return RLC_Series,fig
