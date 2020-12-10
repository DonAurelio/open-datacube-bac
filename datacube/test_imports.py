import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy
import seaborn as sns
import tarfile
from pandas_profiling import ProfileReport

import pandas as pd
import numpy as np
from imblearn.over_sampling import RandomOverSampler
#from imblearn.over_sampling import MultiOutputMixin
from collections import Counter
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score, train_test_split

import joblib
import datacube

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

import matplotlib.colors as colors
from matplotlib.colors import ListedColormap
from matplotlib.pyplot import colorbar
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Desactiva la impresión de Warnings en el Notebook
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

# Configuración de Drivers para Leer KMLs
gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.model_selection import KFold 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score 

import imblearn
from imblearn.under_sampling import RandomUnderSampler