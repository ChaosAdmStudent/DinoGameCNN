'''
This module captures screenshot of game, and writes a csv file containing label and image url (local url)
'''

from pyautogui import screenshot 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd 
import time
import keyboard 
from skimage import io  
from skimage.transform import rescale

def start_browser(driver):
 
    # Make sure internet is off!
    driver.get("http://www.google.com") 

    time.sleep(2) 

    elem = driver.find_element_by_class_name('offline') 
    elem.send_keys('\ue00D') 

# To keep adding frames of training sets 
def return_x():
    '''
    Used for indexing purpose.
    '''
    try:
        f = open('x.txt', 'r') 
        x = f.read() 
        f.close()
        return int(x)
    except: 
        write_x('0')
        return 0
    
def write_x(x):
    f = open('x.txt', 'w') 
    f.write(str(x)) 
    f.close() 

def capture_img(driver):  
    '''
    driver: The Selenium web driver being used 

    This function captures screenshots of the game and stores them on your local folder.
    Press 'q' to stop recording
    '''
    
    x = return_x()  # Indexing element for unique naming of images
    labels = []  # label -- 1 ( up arrow ) |  2 (down arrow) | 0 (Stay)
    scaling_factor = 0.5 # Downscaling screenshot images to 50% 
    path = './train_images'

    while True: 
        top = 70 
        img = screenshot(region=(170, top + 130, 800-236, 350-233))

        if keyboard.is_pressed('up arrow'):
            img.save(f'{path}/frame_{x}.png')   
            img = io.imread(f'{path}/frame_{x}.png', as_gray=True)  # Converts image to grayscale
            img = rescale(img, scaling_factor , anti_aliasing = True)
            io.imsave(f'{path}/frame_{x}.png', img)
            print('Jump!')
            labels.append(1)
            x += 1
        
        if keyboard.is_pressed('down arrow'):
            img.save(f'{path}/frame_{x}.png')   
            img = io.imread(f'{path}/frame_{x}.png', as_gray=True) 
            img = rescale(img, scaling_factor, anti_aliasing = True)
            io.imsave(f'{path}/frame_{x}.png', img)
            print('Duck!')
            labels.append(2)
            x += 1

        if keyboard.is_pressed('t'):
            img.save(f'{path}/frame_{x}.png')   
            img = io.imread(f'{path}/frame_{x}.png', as_gray=True) 
            img = rescale(img, scaling_factor, anti_aliasing = True)
            io.imsave(f'{path}/frame_{x}.png', img)
            print('Stay!')
            labels.append(0)
            x += 1 
             
        if keyboard.is_pressed('q'):
            driver.close()
            break

    write_x(x) 
    return labels


def make_dataset(labels):
    
    x = return_x()
    path_img = './train_images'
    path_csv = './dataset'
    urls = [f'{path_img}/frame_{i}.png' for i in range(x-len(labels), x)]
    img_df = pd.DataFrame({'url': urls, 'label': labels})
    
    try: 
        img_df_old = pd.read_csv(f'{path_csv}/data.csv') 
        img_df_old = img_df_old.append(img_df, ignore_index = True)
        img_df_old.to_csv(f'{path_csv}/data.csv', index = False)
        return img_df_old 

    except:  
        img_df.to_csv(f'{path_csv}/data.csv', index = False)
        return img_df 


# For testing purpose
if __name__ == "__main__":
    driver = webdriver.Chrome(r'C:\Users\laksh\Downloads\chromedriver_win32\chromedriver.exe') 
    start_browser(driver)
    labels = capture_img(driver)
    img_df = make_dataset(labels) 
    