import numpy as np
import scipy as sp
from Analysis import Functions as F
from matplotlib import pyplot as plt


class Variable():
    """
    This class is used to modelize
    a controlled variable of an experiment
    """

    def __init__(self, data, name, unit, Type="Variable"):
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

    def rescale(self, function, new_name, new_unit, *args, Type=None):
        """
        Rescales the parameter using the specified
        function and parameter, also changes the name
        and unit
        """
        assert callable(function), "Function must be callable"
        data = function(self.data, *args)

        if Type is None:
            Type = self.type
        if Type == "Parameter":
            return Parameter(data, new_name, new_unit)
        elif Type == "Measurement":
            return Measurement(data, new_name, new_unit)
        else:
            return Variable(data, new_name, new_unit)

        def subset(self,start,stop=None,step=1,single=False):
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
                result = Parameter(data,self.name,self.unit)
            elif self.type == "Measurement":
                result = Measurement(data,self.name,self.unit)
            elif self.type == "Variable":
                result = Variable(data,self.name,self.unit)

            return result

class Parameter(Variable):

    def __init__(self, data, name, unit):
        super(Parameter, self).__init__(data, name, unit, Type="Parameter")
        return


class Measurement(Variable):

    def __init__(self, data, name, unit):
        super(Measurement, self).__init__(data, name, unit, Type="Measurement")
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


