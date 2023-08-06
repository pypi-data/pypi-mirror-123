import numpy as np
from importlib import reload
import matplotlib.pyplot as plt

from ipywidgets import IntSlider, Output
from IPython.display import display
from IPython.display import update_display


class LivePlotNotebook(object):

    def __init__(self, obj_id, xlabel="", ylabel="", title="", legend=None):
        
        fig,ax = plt.subplots(1,1)
        
        ax.plot([0], label=legend)
        
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
        ax.legend()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid()
        ax.set_title(title)
        
        self.ax = ax
        self.fig = fig
        self.obj_id = obj_id
        
        display(self.fig, display_id=obj_id)

    def update(self, X, Y):
        X = np.array(X)
        Y = np.array(Y)
        
        # update Vales
        line = self.ax.lines[0]
        line.set_xdata(X)
        line.set_ydata(Y)

        # update limits
        self.ax.set_xlim(X.min(), X.max())
        self.ax.set_ylim(Y.min(), Y.max())
        self.ax.set_xmargin(0.1)
        self.ax.set_ymargin(0.1)
        
        #clear_output()
        update_display(self.fig, display_id=self.obj_id)
    
    def end(self):
        plt.close(self.fig)
        


class LiveScatterNotebook(object):

    def __init__(self, obj_id, xlabel="", ylabel="", title="", legend=None):
        
        fig,ax = plt.subplots(1,1)
        
        ax.plot([0], 'o', label=legend)
        
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
        ax.legend()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid()
        ax.set_title(title)
        
        self.ax = ax
        self.fig = fig
        self.obj_id = obj_id
        
        display(self.fig, display_id=obj_id)

    def update(self, X, Y):
        X = np.array(X)
        Y = np.array(Y)
        
        # update Vales
        line = self.ax.lines[0]
        line.set_xdata(X)
        line.set_ydata(Y)

        # update limits
        self.ax.set_xlim(X.min(), X.max())
        self.ax.set_ylim(Y.min(), Y.max())
        self.ax.set_xmargin(0.1)
        self.ax.set_ymargin(0.1)
        
        #clear_output()
        update_display(self.fig, display_id=self.obj_id)
    
    def end(self):
        plt.close(self.fig)