from MLVisualizationTools.backend import colinfo
from typing import List, Dict
import copy
import pandas as pd

#Functions for retrieving data about ml model structure

#TODO - nonlinear

class AnalyticsColumnInfo:
    """Wrapper class for holding col info"""
    def __init__(self, name: str, variance: float):
        self.name = name
        self.variance = variance

    def __lt__(self, other):
        return self.variance < other.variance

    def __repr__(self):
        return "Col with name: " + self.name + " and variance " + str(self.variance)

class AnalyticsResult:
    """Wrapper class for holding and processing col info"""
    def __init__(self):
        self.cols: List[AnalyticsColumnInfo] = []

    def append(self, name: str, variance: float):
        self.cols.append(AnalyticsColumnInfo(name, variance))

    def maxVariance(self):
        """Return a list of cols, ordered by maximum variance"""
        cols = copy.copy(self.cols)
        cols.sort(reverse=True)
        return cols

#region Tensorflow
def analyzeTFModel(model, data: pd.DataFrame, exclude: List[str] = None) -> AnalyticsResult:
    """
    Performs 1d analysis on a tensorflow model. Wrapper function for analyzeTFModelRaw()
    that automatically handles column info generation.

    :param model: A tensorflow model
    :param data: A pandas dataframe
    :param exclude: Values to be excluded from data, useful for output values
    """
    return analyzeTFModelRaw(model, colinfo(data, exclude))

def analyzeTFModelRaw(model, coldata: List[Dict], steps:int=20) -> AnalyticsResult:
    """
    Performs 1d analysis on a tensorflow model. Returns a class with lots of info for graphing.
    Call from anaylyzeTFModel to autogen params.

    Coldata should be formatted with keys 'name', 'min', 'max', 'mean'

    :param model: A tensorflow model
    :param coldata: An ordered list of dicts with col names, min max values, and means
    :param steps: Resolution to scan model with
    """

    AR = AnalyticsResult()

    for item in coldata:
        key = item['name']
        predictiondata = []

        for i in range(0, steps):
            predictionrow = []
            for subitem in coldata:
                subkey = subitem['name']
                if key == subkey:
                    predictionrow.append(i * (subitem['max'] - subitem['min'])/(steps-1) + subitem['min'])
                else:
                    predictionrow.append(subitem['mean'])

            predictiondata.append(predictionrow)
        preddata = pd.DataFrame(predictiondata)
        predictions = model.predict(preddata)
        AR.append(key, predictions.max() - predictions.min())

    return AR
#endregion