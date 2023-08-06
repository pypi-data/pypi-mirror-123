from typing import List, Dict
from MLVisualizationTools.backend import colinfo
import pandas as pd

#Functions for passing data to ml models

#region Tensorflow
#region grid
def TFModelPredictionGrid(model, x:str, y:str, data:pd.DataFrame,
                          exclude:List[str] = None, steps:int=20) -> pd.DataFrame:
    """
    Creates a dataset from a 2d prediction on a tensorflow model. Wrapper function for TFModelPredictionGridRaw()
    that automatically handles column info generation.

    :param model: A tensorflow model
    :param x: xaxis for graph data
    :param y: yaxis for graph data
    :param data: A pandas dataframe
    :param exclude: Values to be excluded from data, useful for output values
    :param steps: Resolution to scan model with
    """
    return TFModelPredictionGridRaw(model, x, y, colinfo(data, exclude), steps)

def TFModelPredictionGridRaw(model, x:str, y:str, coldata:List[Dict], steps:int=20) -> pd.DataFrame:
    """
    Creates a dataset from a 2d prediction on a tensorflow model. Wrapper function for TFModelPredictionGridRaw()
    that automatically handles column info generation.

    Call from TFModelPredictionGrid to autogen params.

    Coldata should be formatted with keys 'name', 'min', 'max', 'mean'

    :param model: A tensorflow model
    :param model: A tensorflow model
    :param x: xaxis for graph data
    :param y: yaxis for graph data
    :param coldata: An ordered list of dicts with col names, min max values, and means
    :param steps: Resolution to scan model with
    """
    cols = []
    for item in coldata:
        cols.append(item['name'])
    preddata = pd.DataFrame(columns=cols)

    assert x in cols, "X must be in coldata"
    assert y in cols, "Y must be in coldata"

    for xpos in range(0, steps):
        for ypos in range(0, steps):
            predictionrow = {}
            for item in coldata:
                key = item['name']
                if key == x:
                    predictionrow[x] = xpos * (item['max'] - item['min']) / (steps - 1) + item['min']
                elif key == y:
                    predictionrow[y] = ypos * (item['max'] - item['min']) / (steps - 1) + item['min']
                else:
                    predictionrow[key] = item['mean']

            preddata = preddata.append(predictionrow, ignore_index=True)

    predictions = model.predict(preddata)
    preddata['Output'] = predictions
    return preddata
#endregion grid

#region animation
def TFModelPredictionAnimation(model, x:str, y:str, anim:str, data: pd.DataFrame,
                               exclude:List[str] = None, steps:int=20) -> pd.DataFrame:
    """
    Creates a dataset from a 2d prediction on a tensorflow model. Wrapper function for TFModelPredictionGridRaw()
    that automatically handles column info generation.

    :param model: A tensorflow model
    :param x: xaxis for graph data
    :param y: yaxis for graph data
    :param anim: Animation axis for graph data
    :param data: A pandas dataframe
    :param exclude: Values to be excluded from data, useful for output values
    :param steps: Resolution to scan model with
    """
    return TFModelPredictionAnimationRaw(model, x, y, anim, colinfo(data, exclude), steps)

def TFModelPredictionAnimationRaw(model, x:str, y:str, anim:str, coldata:List[Dict], steps:int=20) -> pd.DataFrame:
    """
    Creates a dataset from a 2d prediction on a tensorflow model. Wrapper function for TFModelPredictionGridRaw()
    that automatically handles column info generation.

    Call from TFModelPredictionGrid to autogen params.

    Coldata should be formatted with keys 'name', 'min', 'max', 'mean'

    :param model: A tensorflow model
    :param model: A tensorflow model
    :param x: xaxis for graph data
    :param y: yaxis for graph data
    :param anim: Animation axis for graph data
    :param coldata: An ordered list of dicts with col names, min max values, and means
    :param steps: Resolution to scan model with
    """
    cols = []
    for item in coldata:
        cols.append(item['name'])
    preddata = pd.DataFrame(columns=cols)

    assert x in cols, "X must be in coldata"
    assert y in cols, "Y must be in coldata"
    assert anim in cols, "Anim must be in coldata"

    for xpos in range(0, steps):
        for ypos in range(0, steps):
            for animpos in range(0, steps):
                predictionrow = {}
                for item in coldata:
                    key = item['name']
                    if key == x:
                        predictionrow[x] = xpos * (item['max'] - item['min']) / (steps - 1) + item['min']
                    elif key == y:
                        predictionrow[y] = ypos * (item['max'] - item['min']) / (steps - 1) + item['min']
                    elif key == anim:
                        predictionrow[anim] = animpos * (item['max'] - item['min']) / (steps - 1) + item['min']
                    else:
                        predictionrow[key] = item['mean']

                preddata = preddata.append(predictionrow, ignore_index=True)

    predictions = model.predict(preddata)
    preddata['Output'] = predictions
    return preddata
#endregion
#endregion