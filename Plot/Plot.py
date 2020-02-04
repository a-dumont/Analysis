from Analysis import Experiment as E
from Analysis import Functions as F
from Analysis import Fit as Fit

from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import scipy as sp


class Plot_1D():
    """
    Plots a simple x,y graph
    """

    def __init__(self, parameter, measurement, graph=None):
        """
        A Simple 1D Plot

        Parameters:
        --------------------------------------

        parameter:  An instance of Analysis.Experiment.Parameter
        measurement: An instance of Analysis.Experiment.Measurement
        graph:  An instance of Plot_1D if present used to add curves
                to the same figure
        """
        self.parameter = parameter
        self.measurement = measurement



        self.graph = graph
        self.fit_functions = {
            func.__name__: func for func in F.__dict__.values() if callable(func)}
        return

    def draw(self, **kwargs):
        """
        Draws the plot, kwargs are ax.plots() execept Fit
        which is used to determine how to fit the data
        """
        # Define the data and the labels
        data = np.array([self.parameter.data, self.measurement.data])

        if self.parameter.unit is not None and self.parameter.unit != "":
            xlabel = "%s (%s)" % (self.parameter.name, self.parameter.unit)
        else:
            xlabel = "%s" % (self.parameter.name)

        if self.measurement.unit is not None and self.measurement.unit != "":
            ylabel = "%s (%s)" % (self.measurement.name, self.measurement.unit)
        else:
            ylabel = "%s" % (self.measurement.name)

        data_label = self.measurement.label

        # Determine if a fit is wanted
        try:
            fit = kwargs.pop("Fit")
            assert fit in self.fit_functions, "%s not a fit function"%(fit)
            fit_function = self.fit_functions[fit]

            fit_label = "%s fit" % (fit)

            # Determine if there are any fit params
            try:
                bounds = kwargs.pop("bounds")
            except KeyError:
                bounds = (-np.inf, np.inf)
            try:
                p0 = kwargs.pop("p0")
            except KeyError:
                p0 = None
            try:
                sigma = kwargs.pop("sigma")
            except KeyError:
                sigma = None

            fit_params, fit_err = Fit.fit(
                fit_function, data[0], data[1], p0=p0, sigma=sigma, bounds=bounds)
        except KeyError:
            fit = None

        if self.graph is None:
            self.fig, self.ax = plt.subplots()
        else:
            assert isinstance(
                self.graph, Plot_1D) is True, "graph must be an instance of Plot_1D"
            self.fig, self.ax = self.graph.fig, self.graph.ax

        if fit is not None:
            if self.parameter.err is not None or self.measurement.err is not None:
                xerr = self.parameter.err
                yerr = self.measurement.err
                self.ax.errorbar(data[0],data[1],yerr,xerr,label=data_label, **kwargs)
                self.ax.plot(data[0], fit_function(
                    data[0], *fit_params), label=fit_label)
            else:
                self.ax.plot(*data, label=data_label, **kwargs)
                self.ax.plot(data[0], fit_function(
                    data[0], *fit_params), label=fit_label)
            self.ax.legend()
            self.ax.set_xlabel(xlabel)
            self.ax.set_ylabel(ylabel)

        else:
            if self.parameter.err is not None or self.measurement.err is not None:
                xerr = self.parameter.err
                yerr = self.measurement.err
                self.ax.errorbar(data[0],data[1],yerr,xerr,label=data_label, **kwargs)

            else:
                self.ax.plot(*data, label=data_label,**kwargs)
                if data_label is not None:
                    self.ax.legend()
            self.ax.set_xlabel(xlabel)
            self.ax.set_ylabel(ylabel)

        #xticks = abs(self.parameter.data.max()-self.parameter.data.min())/4
        #yticks = abs(self.measurement.data.max()-self.measurement.data.min())/4
        self.ax.xaxis.set_major_locator(ticker.MaxNLocator(5))
        self.ax.yaxis.set_major_locator(ticker.MaxNLocator(5))
        self.ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(4))
        self.ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(4))

        if fit is not None:
            return self.fig, self.ax, fit_params, fit_err
        else:
            return self.fig, self.ax


def Plot2D():

    return
