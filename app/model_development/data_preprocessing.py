# import django
# django.setup()

import pandas as pd
import numpy as np
import cv2
import threading
# import multiprocessing as mp
import os

class DataPreprocessing():
    def __init__(self, data):
        self.__data = data
    
    def resize_images(self, image, width, height):
        image = cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), (width,height))  
        return image
    
    def convert_images(self, index, image, data_list):
        image = cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2RGB)
        data_list.append(self.resize_images(image, 100, 100))

    def get_images(self):
        # Convert from BGR to RGB

        # Multiprocessing
        # results = mp.Manager().list([])

        # with mp.Pool(os.cpu_count()) as p:
        #     for i, img in enumerate(self.__data):
        #         p.starmap(self.convert_images, [(i, img, results)])

        # Multithreading
        results = []

        list_thread = []
        for i, img in enumerate(self.__data):
            t = threading.Thread(target=self.convert_images, args=(i, img, results))
            t.start()
            list_thread.append(t)
        
        for t in list_thread:
            t.join()


        # Normalization [0, 1]
        images = np.array(results) / 255.0
        return images

    def convert_categorical_data_to_cols(self, series=True, target=None):
        if series:
            return self.__data.str.get_dummies()
            
        return pd.get_dummies(self.__data, prefix=None, prefix_sep='', columns=target, drop_first=True)

    def normalization_min_max(self):
        min = 0
        max = 1
        ratingmin = 1
        ratingmax = 5
        return ((self.__data-ratingmin)*(max-min)/(ratingmax-ratingmin))+min