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

    def __init__(self,parameter, measurement):
        self.parameter = parameter
        self.measurement = measurement
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
            assert fit in self.fit_functions, "%s "
            fit_function = self.fit_functions[fit]
            data_label = "Experimental Data"
            fit_label = "%s fit" % s(fit)

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

        self.fig, self.ax = plt.subplots()

        if fit is not None:
            self.ax.plot(*data, label=data_label, **kwargs)
            self.ax.plot(data[0], fit_function(data[0], *fit_params),label=fit_label)

        else:
            self.ax.plot(*data,**kwargs)


        return
