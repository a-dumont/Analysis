import numpy as np
import scipy as sp
from Analysis import Functions as F
from Analysis import Plot as P


class Variable():
    """
    This class is used to modelize
    a controlled variable of an experiment
    """

    def __init__(self, data, name, unit, err=None, label=None, Type="Variable"):
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

        if err is not None:
            if type(err) is float or type(err) is int or type(err) is np.float64:
                self.err = self.data*0+err
            elif type(err) is list:
                self.err = np.array(err)
            elif type(err) is np.ndarray:
                self.err = err
            else:
                raise ValueError("Err must be a float,int or a list or array of floats and ints")
        else:
            self.err = None

        return

    def __call__(self):
        return self.data

    def __repr__(self):
        string = "%s from %s to %s %s in %s steps" % (
            self.name, self.data.min(), self.data.max(), self.unit, self.data.shape[0])
        return string

    def add_err(self,err):
        self.err = err
        return

    def add_label(self,label):
        self.label = label
        return

    def rescale(self, function,*args,new_name=None,new_unit=None,new_label=None,Type=None):
        """
        Rescales the parameter using the specified
        function and parameter, also changes the name
        and unit
        """
        assert callable(function), "Function must be callable"
        data = function(self.data, *args)

        if self.err is not None:
            err = function(self.err, *args)
        else:
            err = self.err

        if new_name is None:
            new_name = self.name
        if new_unit is None:
            new_unit = self.unit
        if new_label is None:
            new_label = self.label

        if Type is None:
            Type = self.type
        if Type == "Parameter":
            return Parameter(data, new_name, new_unit,err,new_label)
        elif Type == "Measurement":
            return Measurement(data, new_name, new_unit,err,new_label)
        else:
            return Variable(data, new_name, new_unit,err,new_label)

    def subset(self, start, stop=None, step=1, single=False):
        """
        This function returns another object
        of the same type but with a subset
        of the data. The slice shoud be
        a slice of an array Ex. [1:5:1]
        """

        if single is False:
            if type(start) is np.ndarray:
                data = self.data[start]
                if self.err is not None:
                    err = self.err[start]
                else:
                    err = None
            else:
                data = self.data[start:stop:step]
                if self.err is not None:
                    err = self.err[start:stop:step]
                else:
                    err = None
            if self.type == "Parameter":
                result = Parameter(data, self.name, self.unit,err,self.label)
            elif self.type == "Measurement":
                result = Measurement(data, self.name, self.unit,err,self.label)
            elif self.type == "Variable":
                result = Variable(data, self.name, self.unit,err,self.label)


        elif single is True:
            data = self.data[start]
            if self.err is not None:
                err = self.err[start]
            else:
                err = None

            result = data

        return result

    def delete(self,start,stop,step):

        data = np.delete(self.data,slice(start,stop,step))
        if self.err is not None:
            err = np.delete(self.err,slice(start,stop,step))
        else:
            err = None
        if self.type == "Parameter":
            result = Parameter(data, self.name, self.unit,err,self.label)
        elif self.type == "Measurement":
            result = Measurement(data, self.name, self.unit,err,self.label)
        elif self.type == "Variable":
            result = Variable(data, self.name, self.unit,err,self.label)


        return result



    def sort(self,index_array=None,kind="stable",Index=False):
        """
        Sorts the data using np.argsort
        """
        data = self.data
        if index_array is None:
            index_array = np.argsort(data)
        sorted_data = data[index_array]

        if self.type == "Parameter":
            result = Parameter(sorted_data,self.name,self.unit,self.err,self.label)
        elif self.type == "Measurement":
            result = Measurement(sorted_data,self.name,self.unit,self.err,self.label)
        else:
            result = Variable(sorted_data,self.name,self.unit,self.err,self.label)

        if Index is True:
            return result,index_array
        else:
            return result

    def sort_unique(self,Index=True):
        data = self.data
        sorted_data, index_array = np.unique(data,True)

        if self.type == "Parameter":
            result = Parameter(sorted_data,self.name,self.unit,self.err,self.label)
        elif self.type == "Measurement":
            result = Measurement(sorted_data,self.name,self.unit,self.err,self.label)
        else:
            result = Variable(sorted_data,self.name,self.unit,self.err,self.label)

        if Index is True:
            return result,index_array
        else:
            return result

    def min(self, Slice=None):
        """
        Returns the minimum from the whole array or
        a slice
        """

        if Slice is not None:
            data = self.data[Slice]
        else:
            data = self.data
        res = data.min()

        return res

    def argmin(self,Slice=None):
        """
        Returns the minimum's index from the
        whole array or a slice
        """

        if Slice is not None:
            data = self.data[Slice]
        else:
            data = self.data
        res = np.argmin(data)
        if Slice is not None:
            res += Slice.start

        return res


    def max(self, Slice=None):
        """
        Returns the maximum for the whole array or
        a slice
        """

        if Slice is not None:
            data = self.data[Slice]
        else:
            data = self.data
        res = data.max()

        return res

    def argmax(self,Slice=None):
        """
        Returns the maximum's index from the
        whole array or a slice
        """

        if Slice is not None:
            data = self.data[Slice]
        else:
            data = self.data
        res = np.argmax(data)
        if Slice is not None:
            res += Slice.start

        return res


    def where(self,value, closest=True):
        """
        Returns the index giving the position
        of value in the array or the closest
        value if closest is True
        """

        data = self.data
        index = np.where(data==value)[0]

        if index.shape[0] == 0:
            if closest is True:
                index = np.where(data>=value)[0]
                if index.shape[0] == 0:
                    res = None
                else:
                    res = index[0]
            else:
                res = None
        else:
            res = index

        return res


class Parameter(Variable):

    def __init__(self, data, name, unit, err=None, label=None):
        super(Parameter, self).__init__(
            data, name, unit, err, label, Type="Parameter")
        return


class Measurement(Variable):

    def __init__(self, data, name, unit, err=None, label=None):
        super(Measurement, self).__init__(
            data, name, unit, err, label, Type="Measurement")
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

    def sort(self,parameter=None,measurements=None,unique=False):
        """
        Sorts the parameter in growing order and sorts
        the measurements accordingly
        """
        if parameter is None:
            parameter = self.parameters[0]
        if measurements is None:
            measurements = self.measurements

        if unique is True:
            param_sort, index_array = parameter.sort_unique()
            measurements_sort = [i.subset(index_array) for i in measurements]
        else:
            param_sort, index_array = parameter.sort(Index=True)
            measurements_sort = [i.subset(index_array) for i in measurements]

        return DataSet(param_sort,measurements_sort)

    def min(self,parameter,measurement,start=None,stop=None):
        """
        Returns the minimum value of a measurement
        within an interval of the parameter from
        start to stop
        """

        param = self.parameters[parameter]
        meas = self.measurements[measurement]

        if start is not None:
            start = param.where(start)

            if type(start) is np.ndarray:
                if start.shape[0] is not None:
                    start = start[0]
                else:
                    raise ValueError("Start value not in array")
            else:
                start = start
        else:
            start = 0

        if stop is not None:
            stop = param.where(stop)

            if type(stop) is np.ndarray:
                if stop.shape[0] is not None:
                    stop = stop[0]
                else:
                    raise ValueError("Stop value not in array")
            else:
                stop = stop
        else:
            stop = meas.data.shape[0]

        Slice = slice(start,stop)
        res = meas.min(Slice)

        return res

    def argmin(self,parameter,measurement,start=None,stop=None):
        """
        Returns the minimum's index  of a measurement
        within an interval of the parameter from
        start to stop
        """

        param = self.parameters[parameter]
        meas = self.measurements[measurement]

        if start is not None:
            start = param.where(start)

            if type(start) is np.ndarray:
                if start.shape[0] is not None:
                    start = start[0]
                else:
                    raise ValueError("Start value not in array")
            else:
                start = start
        else:
            start = 0

        if stop is not None:
            stop = param.where(stop)

            if type(stop) is np.ndarray:
                if stop.shape[0] is not None:
                    stop = stop[0]
                else:
                    raise ValueError("Stop value not in array")
            else:
                stop = stop
        else:
            stop = meas.data.shape[0]

        Slice = slice(start,stop)
        res = meas.argmin(Slice)

        return res


    def max(self,parameter,measurement,start=None,stop=None):
        """
        Returns the maximum value of a measurement
        within an interval of the parameter from
        start to stop
        """

        param = self.parameters[parameter]
        meas = self.measurements[measurement]

        if start is not None:
            start = param.where(start)

            if type(start) is np.ndarray:
                if start.shape[0] is not None:
                    start = start[0]
                else:
                    raise ValueError("Start value not in array")
            else:
                start = start
        else:
            start = 0

        if stop is not None:
            stop = param.where(stop)

            if type(stop) is np.ndarray:
                if stop.shape[0] is not None:
                    stop = stop[0]
                else:
                    raise ValueError("Stop value not in array")
            else:
                stop = stop
        else:
            stop = meas.data.shape[0]

        Slice = slice(start,stop)
        res = meas.argmax(Slice)

        Slice = slice(start,stop)
        res = meas.max(Slice)

        return res

    def argmax(self,parameter,measurement,start=None,stop=None):
        """
        Returns the maximum's index of a measurement
        within an interval of the parameter from
        start to stop
        """

        param = self.parameters[parameter]
        meas = self.measurements[measurement]

        if start is not None:
            start = param.where(start)

            if type(start) is np.ndarray:
                if start.shape[0] is not None:
                    start = start[0]
                else:
                    raise ValueError("Start value not in array")
            else:
                start = start
        else:
            start = 0

        if stop is not None:
            stop = param.where(stop)

            if type(stop) is np.ndarray:
                if stop.shape[0] is not None:
                    stop = stop[0]
                else:
                    raise ValueError("Stop value not in array")
            else:
                stop = stop
        else:
            stop = meas.data.shape[0]

        Slice = slice(start,stop)
        res = meas.argmax(Slice)

        return res

    def subset(self,start,stop,step,parameters=None,measurements=None):
        """
        Returns a subset of the DataSet
        """

        if parameters is None:
            parameters = self.parameters
        else:
            parameters = [self.parameters[parameters]]
        if measurements is None:
            measurements = self.measurements
        else:
            measurements = [self.measurements[measurements]]

        param_sub = [param.subset(start,stop,step) for param in parameters]
        meas_sub = [meas.subset(start,stop,step) for meas in measurements]

        return DataSet(param_sub,meas_sub)


    def derive(self,parameter=0,measurement=0,name=None,unit=None,label=None):
        """
        Uses np.gradient to derive numericaly the data
        """

        parameter = self.parameters[parameter]
        measurement = self.measurements[measurement]

        data_x = parameter.data
        data_y = measurement.data

        data = np.gradient(data_y,data_x)

        derivative = Measurement(data,name,unit,None,label)

        return derivative

    def delete(self,start,stop,step,parameters=None,measurements=None):
        """
        Returns a subset of the DataSet
        """

        if parameters is None:
            parameters = self.parameters
        if measurements is None:
            measurements = self.measurements

        param_del = [param.delete(start,stop,step) for param in parameters]
        meas_del = [meas.delete(start,stop,step) for meas in measurements]

        return DataSet(param_del,meas_del)


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

    def plots_1D(self, parameters=0, measurements=0, Fit=None, draw=True, Graph=None, colors=None, **kwargs):
        """
        A wrapper for plot_1D for multiple curves
        """

        if type(parameters) is not list:
            parameters = [parameters]
        if type(measurements) is not list:
            measurements = [measurements]
        if type(Fit) is not list:
            Fit = [Fit]
        if type(colors) is not list:
            colors = [colors]

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

        if len(colors) != nb:
                colors = [None for i in range(nb)]

        fit, err = [None for i in range(nb)], [None for i in range(nb)]

        for i in range(nb):

            # First instance
            if i == 0:
                fig, ax, fit[i], err[i] = self.plot_1D(parameters[i], measurements[i],
                                                       Fit[i], Graph, True, color=colors[i],**kwargs)
            # Other instances
            else:
                fig, ax, fit[i], err[i] = self.plot_1D(parameters[i], measurements[i],
                                                       Fit[i], self.Graph, True, color=colors[i],**kwargs)

        return fig, ax, fit, err

    def add_measurements(self,measurements):
        if type(measurements) is not list:
            measurements = [measurements]
        self.measurements = self.measurements+measurements
        return

    def add_parameters(self,parameters):
        if type(parameters) is not list:
            parameterss = [parameters]
        self.parameters = self.parameters+parameters
        return



def readfile(filename, parameter_name_unit, measurement_names_units, measurement_labels=None, delimiter=None,Out="DataSet"):
    """
    Used to generate a DataSet from a file using np.genfromtxt

    Parameters:
    ---------------------------------------------------------
    parameter_name_unit:    tuple("name","unit")
    measurement_names_units:    list(tuple("name","unit") for number of measurements)
    """

    assert type(parameter_name_unit) is tuple, "parameter_name_unit must be a tuple"

    if type(measurement_names_units) is not list:
        if type(measurement_names_units) is tuple:
            measurement_names_units = [measurement_names_units]
        else:
            raise TypeError("measurement_names_units must be a list of tuples or a single tuple")
    else:
        assert type(measurement_names_units[0]) is tuple, "measurement_names_units must be a list of tuples or a single tuple"

    raw_data = np.genfromtxt(filename, delimiter=delimiter).T
    shape = raw_data.shape[0]

    parameter = Parameter(raw_data[0],*parameter_name_unit)
    shape -= 1


    if measurement_labels is None:
        measurement_labels = [None for i in range(shape)]
    measurements = []
    for i in range(shape):
        measurements.append(Measurement(raw_data[i+1],*measurement_names_units[i],label=measurement_labels[i]))

    if Out == "DataSet":
        res = DataSet(parameter,measurements)
    elif Out == "Measurements":
        res = measurements
    elif Out == "Parameter":
        res =  parameter

    return res









