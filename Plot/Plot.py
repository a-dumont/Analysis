from Analysis import Experiment as E
from Analysis import Functions as F
from Analysis import Fit as Fit

from matplotlib import pyplot as plt
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
        xlabel = "%s (%s)" % (self.parameter.name, self.parameter.unit)
        ylabel = "%s (%s)" % (self.measurement.name, self.measurement.unit)

        # Determine if a fit is wanted
        try:
            fit = kwargs.pop("Fit")
            assert fit in self.fit_functions, "%s not a fit function"%(fit)
            fit_function = self.fit_functions[fit]

            try:
                data_label = kwargs.pop("label")
            except KeyError:
                data_label = "Experimental Data"
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
            self.ax.plot(*data, label=data_label, **kwargs)
            self.ax.plot(data[0], fit_function(
                data[0], *fit_params), label=fit_label)
            self.ax.legend()

        else:
            self.ax.plot(*data, **kwargs)
            self.ax.legend()

        if fit is not None:
            return self.fig, self.ax, fit_params, fit_err
        else:
            return self.fig, self.ax


def Plot2D():

    return
