''' 
This module is responsible for generating predicted responses from our CNN model which was created earlier. 
This script will be the end result. Will run the game in browser.
'''

from tensorflow.keras.models import load_model 
import capture_actions as ca 
import numpy as np
from pyautogui import screenshot
from selenium import webdriver
from skimage.transform import rescale
import keyboard 

def predict_state(model):
    '''
    Uses CNN model to classify a screenshot being either class [0,1,2]
    '''
    
    #Start browser
    driver = webdriver.Chrome(r'C:\Users\laksh\Downloads\chromedriver_win32\chromedriver.exe')  
    ca.start_browser(driver) 
    
    #Continuous screenshots 
    scaling_factor = 0.5
    while True: 
        top = 70 
        img = screenshot(region=(170, top + 130, 800-236, 350-233)).convert('L')  # Converts PIL Image to Grayscale
        img = np.array(img) 
        img = rescale(img, scaling_factor , anti_aliasing = True) 
        img = img.reshape([1,58,282,1])

        # Predict class 

        prediction = model.predict(img).argmax() 
        move_dino(driver, prediction) 

        # Stopping game 
        if keyboard.is_pressed('q'):
            break  
    


def move_dino(driver, prediction): 
    '''
    Sends prediction key to driver to move the dino
    '''
    elem = driver.find_element_by_class_name('offline') 
    
    if prediction == 0:
        print('Stay!') 
    if prediction == 1: 
        elem.send_keys('\ue013')
        print('Jump!') 
    if prediction == 2: 
        elem.send_keys('\ue015')
        print('Jump!') 
    
# Testing Purpose
if __name__ == "__main__":  
    model = load_model('./model/model.h5') 
    predict_state(model)


