from MLVisualizationTools import Analytics, Interfaces, Graphs
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #stops agressive error message printing
from tensorflow import keras

try:
    import matplotlib.pyplot
except:
    raise ImportError("Matplotlib is required to run this demo. If you don't have matplotlib installed, install it"
                      "with `pip install matplotlib` or run the plotly demo instead.")

def main():
    model = keras.models.load_model('Models/titanicmodel')
    df = pd.read_csv('Datasets/Titanic/train.csv')

    AR = Analytics.Tensorflow(model, df, ["Survived"])
    maxvar = AR.maxVariance()

    grid = Interfaces.TensorflowGrid(model, maxvar[0].name, maxvar[1].name, df, ["Survived"])
    fig, _, _ = Graphs.MatplotlibGrid(grid, maxvar[0].name, maxvar[1].name)
    fig.show()

    grid = Interfaces.TensorflowGrid(model, 'Parch', 'SibSp', df, ["Survived"])
    fig, _, _ = Graphs.MatplotlibGrid(grid, 'Parch', 'SibSp')
    fig.show()

main()