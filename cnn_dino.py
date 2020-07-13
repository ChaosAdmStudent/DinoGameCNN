'''
This module trains a CNN model on the dataset acquired. 
'''

import tensorflow as tf  


def make_model():
    xavier_init = tf.keras.initializers.GlorotNormal() 
    model = tf.keras.Sequential([
        # Add Convo Layers here 
        tf.keras.layers.Conv2D(filters=30, kernel_size=3, activation='relu', input_shape = [58,282,1]),  
        tf.keras.layers.MaxPool2D(pool_size=2, strides=2), 
        tf.keras.layers.Conv2D(filters=30, kernel_size=3, activation='relu'),  
        tf.keras.layers.MaxPool2D(pool_size=2, strides=2),
        # Add ANN here 
        tf.keras.layers.Flatten() ,
        tf.keras.layers.Dense(units = 256, activation= 'relu', kernel_initializer=xavier_init),  # Hidden Layer 1 
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(units = 256, activation= 'relu', kernel_initializer=xavier_init),  # Hidden Layer 2
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(units = 3, activation= 'softmax', kernel_initializer= xavier_init)  # Output Layer 
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy']) 
    model.save('./model/model.h5')

if __name__ == "__main__":
    make_model()







