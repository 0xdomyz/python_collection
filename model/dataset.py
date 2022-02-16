from sklearn.datasets import load_iris
import pandas as pd
import matplotlib.pyplot as plt

data = load_iris(as_frame = True)

print(data['DESCR'])
data['filename']
data['target_names']
data['feature_names']

data['frame']

x, y = load_iris(return_X_y = True,as_frame = True)

df = pd.concat([x,y],axis=1)

df.columns = ['sep_len','sep_wid','pet_len','pet_wid','target']

df = df.assign(
    target_cat = lambda x:x.target.map(
        {
            0:'cat 0',
            1:'cat 1',
            2:'cat 2'
        }
    )
)

df.plot(y='sep_len',x='target_cat',kind = 'scatter'); plt.show()
