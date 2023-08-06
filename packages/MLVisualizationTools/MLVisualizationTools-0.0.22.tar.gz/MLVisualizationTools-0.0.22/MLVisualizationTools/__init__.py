from MLVisualizationTools.modelanalytics import analyzeTFModel, analyzeTFModelRaw
from MLVisualizationTools.modelinterface import TFModelPredictionGrid, TFModelPredictionGridRaw
from MLVisualizationTools.modelinterface import TFModelPredictionAnimation, TFModelPredictionAnimationRaw
from MLVisualizationTools.graphinterface import plotlyGrid, plotlyAnimation, matplotlibGrid

#TODO - colorizer

#A bunch of wrapper functions to make calling various tools easier
class Analytics:
    Tensorflow = analyzeTFModel
    TensorflowRaw = analyzeTFModelRaw

class Interfaces:
    TensorflowGrid = TFModelPredictionGrid
    TensorflowGridRaw = TFModelPredictionGridRaw
    TensorflowAnimation = TFModelPredictionAnimation
    TensorflowAnimationRaw = TFModelPredictionAnimationRaw

class Graphs:
    PlotlyGrid = plotlyGrid
    PlotlyAnimation = plotlyAnimation
    MatplotlibGrid = matplotlibGrid