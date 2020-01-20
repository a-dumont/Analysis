import numpy as np
import scipy as sp
from Analysis import Functions as F
from Analysis import Plot as P


class Variable():
    """
    This class is used to modelize
    a controlled variable of an experiment
    """

    def __init__(self, data, name, unit, label=None, Type="Variable"):
        """
        Parameters:
        -----------------------------
        data:   list or np.ndarray (1d)
                The values of the parameter
        name:   str
                The name of the parameter
        unit:   str
                The unit of the parameter
        """

        assert type(name) is str, "Name must be a string"
        assert type(unit) is str, "Unit must be a string"
        self.name = name
        self.unit = unit
        self.type = Type
        self.label = label

        if type(data) is list:
            self.data = np.array(data)
        elif type(data) is np.ndarray:
            self.data = data
        else:
            raise Exception("Data must be a string or a 1D array")

        return

    def __call__(self):
        return self.data

    def __repr__(self):
        string = "%s from %s to %s %s in %s steps" % (
            self.name, self.data.min(), self.data.max(), self.unit, self.data.shape[0])
        return string

    def rescale(self, function,*args,new_name=None,new_unit=None,new_label=None,Type=None):
        """
        Rescales the parameter using the specified
        function and parameter, also changes the name
        and unit
        """
        assert callable(function), "Function must be callable"
        data = function(self.data, *args)

        if new_name is None:
            new_name = self.name
        if new_unit is None:
            new_unit = self.unit
        if new_label is None:
            new_label = self.label

        if Type is None:
            Type = self.type
        if Type == "Parameter":
            return Parameter(data, new_name, new_unit,new_label)
        elif Type == "Measurement":
            return Measurement(data, new_name, new_unit,new_label)
        else:
            return Variable(data, new_name, new_unit,new_label)

        def subset(self, start, stop=None, step=1, single=False):
            """
            This function returns another object
            of the same type but with a subset
            of the data. The slice shoud be
            a slice of an array Ex. [1:5:1]
            """
            if single is False:
                data = self.data[start:stop:step]
            elif single is True:
                data = self.data[start]

            if self.type == "Parameter":
                result = Parameter(data, self.name, self.unit)
            elif self.type == "Measurement":
                result = Measurement(data, self.name, self.unit)
            elif self.type == "Variable":
                result = Variable(data, self.name, self.unit)

            return result


class Parameter(Variable):

    def __init__(self, data, name, unit, label=None):
        super(Parameter, self).__init__(
            data, name, unit, label, Type="Parameter")
        return


class Measurement(Variable):

    def __init__(self, data, name, unit, label=None):
        super(Measurement, self).__init__(
            data, name, unit, label, Type="Measurement")
        return


class DataSet():
    """
    This object contains one or more parameters
    and one or more measurements
    """

    def __init__(self, parameters, measurements, variables=None):
        if type(parameters) is not list:
            parameters = [parameters]
        if type(measurements) is not list:
            measurements = [measurements]

        for parameter in parameters:
            assert parameter.type == "Parameter", "Parameters must be instances of the Parameter class"

        for measurement in measurements:
            assert measurement.type == "Measurement", "Measurements must be instances of the Measurement class"

        if variables is not None:
            if type(variables) is not list:
                variables = [variables]
            for variable in variables:
                assert variable.type == "Variable", "Variables must be instances of the Variable class"

        self.parameters = parameters
        self.measurements = measurements
        self.variables = variables

        return

    def plot_1D(self, parameter=0, measurement=0, Fit=None, Graph=None, draw=True, **kwargs):
        """
        This function is a wrapper for Analysis.Plot.Plot_1D

        Parameters:
        -----------------------------------------------------

        parameter:  Int or instance of Parameter
                Int is the preferred method as an
                index to pick from self.parameters
                but a parameter object can be passed manually

        measurement:    See parameter
        """

        if Fit is not None:
            kwargs["Fit"] = Fit

        # If Index are passed we get the data from the set
        if type(parameter) is int:
            assert abs(parameter) < len(self.parameters), "Index %s to big for list of len %s" % (
                abs(parameter), len(self.parameters))

            parameter = self.parameters[parameter]

        if type(measurement) is int:
            assert abs(measurement) < len(self.measurements), "Index %s to big for list of len %s" % (
                abs(measurement), len(self.measurements))

            measurement = self.measurements[measurement]

        # This check is only usefull if input is not int
        assert isinstance(
            parameter, Parameter), "Parameter must be int or Parameter instance"
        assert isinstance(
            measurement, Measurement), "Measurement must be int or Measurement instance"

        # We pass the arguments
        self.Graph = P.Plot_1D(parameter, measurement, Graph)

        # We draw if needed
        if draw is True:

            if Fit is not None:
                fig, ax, fit, err = self.Graph.draw(**kwargs)
            else:
                fig, ax = self.Graph.draw(**kwargs)
                fit, err = None, None

        return fig, ax, fit, err

    def plots_1D(self, parameters=0, measurements=0, Fit=None, draw=True, **kwargs):
        """
        A wrapper for plot_1D for multiple curves
        """

        if type(parameters) is not list:
            parameters = [parameters]
        if type(measurements) is not list:
            measurements = [measurements]
        if type(Fit) is not list:
            Fit = [Fit]

        nb = len(measurements)

        if len(parameters) != nb:
            if len(parameters) == 1:
                parameters = [parameters[0] for i in range(nb)]
            else:
                raise ValueError("Too much or too few parameters")

        if len(Fit) != nb:
            if len(Fit) == 1:
                Fit = [Fit[0] for i in range(nb)]
            else:
                raise ValueError("Too much or too few Fit")

        fit, err = [None for i in range(nb)], [None for i in range(nb)]

        for i in range(nb):

            # First instance
            if i == 0:
                fig, ax, fit[i], err[i] = self.plot_1D(parameters[i], measurements[i],
                                                       Fit[i], None, True, **kwargs)
            # Other instances
            else:
                fig, ax, fit[i], err[i] = self.plot_1D(parameters[i], measurements[i],
                                                       Fit[i], self.Graph, True, **kwargs)

        return fig, ax, fit, err
