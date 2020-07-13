import tensorflow as tf 
import numpy as np 
import pandas as pd 
from skimage import io
from sklearn.preprocessing import StandardScaler
    
def load_data(): 
    df = pd.read_csv(r'C:\Users\laksh\Documents\MLCourse\Dino Game\dataset\data.csv')
    X = []

    for url in df.url: 
        img = io.imread(url)
        img = img.reshape([58,282,1])
        X.append(img) 
        
    X = np.array(X) 
    y = np.array(df.label)
    y = tf.keras.utils.to_categorical(y ,num_classes=3)  

    return (X,y) 

if __name__ == "__main__":
    X, y = load_data() 
    print(X.shape, '\n',X.max(), X.min()) 
    print(y.shape, '\n', y)    