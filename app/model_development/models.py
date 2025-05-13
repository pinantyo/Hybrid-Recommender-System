# import django
# django.setup()

# Text-based
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


# Model Loading
import tensorflow as tf
import numpy as np
import pandas as pd
# import random as python_random

# Configuration
import os
# from django.conf import settings
# os.environ["CUDA_VISIBLE_DEVICES"] = settings.CUDA_AVAILABLE

# Model taken time
import time, gc

# Data Preprocessing
from app.model_development import data_preprocessing as dp

# tf.random.set_seed(42)
# np.random.seed(42)
# python_random.seed(42)

class GenerateRecommenderSystem():
    def __init__(self, tourism, ensemble=0, model_name='NMFPersonalizedImageResNet50V2'): #NCFPersonalizedImageResNet50V2 # MFPersonalizedImageResNet50V2
        self.__category = None
        self.__data = self.generate_tourism_data(tourism)
        self.__ensemble = ensemble

        self.init_recc_system(model_name)
            

    def init_recc_system(self, model_name):
        startTime = time.perf_counter()
        # Import models
        self.__model = tf.keras.models.load_model(os.path.join(
            os.getcwd(),
            f'./app/model_development/saved_models/v11/{model_name}' #v3
        ))

    
        self.__model.compile(
            loss = 'mse',
            optimizer=tf.keras.optimizers.Adam(0.000045), #0.0005
            metrics=['mae','mse'],
            jit_compile=False
        ) # XLA error CUDA jit_compile True

        if self.__ensemble:
            self.__ensemble = tf.keras.models.load_model(os.path.join(
                os.getcwd(),
                f'./app/model_development/saved_models/v11/{model_name}'
            ))

        print(f'Model Loading Time: {time.perf_counter()-startTime} s')


    def generate_tourism_data(self, data) -> dict:
        startTime = time.perf_counter()
        place = np.array(list(data.values_list('place_id', flat=True)))

        # Read images
        img = [os.path.join(os.getcwd(), f'./media/{i["img"]}') for i in data.values()]

        img = dp.DataPreprocessing(img).get_images()

        """
            Category
        """
        self.__category = list(data.values_list('category__category_name', flat=True))
        category = np.array(dp.DataPreprocessing(pd.Series(self.__category)).convert_categorical_data_to_cols(series=False))
        self.__category = set(self.__category)

        # Category Tourism Sites
        content_data = {
            'Img':img,
            'Category':category,
            'Place':place
        }

        print(f'Data Creation Time: {time.perf_counter()-startTime} s')
        return content_data

    
    # Result Prediction
    def regression_prediction(self, user, k:int, personalization):
        startTime = time.perf_counter()

        # Age
        # self.__data['Age'] = [user.age] * len(self.__data['Place'])

        # Fetch personalization
        if personalization is not None:
            personalization = [list(i.values())[0] for i in personalization]
            personalization = [1 if i in personalization else 0 for i in self.__category]
        else:
            personalization = [0] * len(self.__category)
        
        self.__data['Personalization'] = [personalization] * len(self.__data['Place'])

        # Age
        self.__data['Age'] = [user.age] * len(self.__data['Place'])

        # ID User
        self.__data['User'] = [user.id] * len(self.__data['Place'])

        print(f'User adding to data time: {time.perf_counter()-startTime}')

        # Prediction Data
        keys = list(self.__data.keys())[::-1]


        results = self.__model.predict(x=[self.__data[i] if i == 'Img' else np.array(self.__data[i]) for i in keys]).reshape(-1)

        if self.__ensemble:
            results_ensembled = self.__ensemble.predict(x=[self.__data[i] if i == 'Img' else np.array(self.__data[i]) for i in keys]).reshape(-1)
            results = np.mean(np.array([results, results_ensembled]), axis=0)
        
        
        results = [(self.__data['Place'][i], results[i]) for i in range(len(results))]

        self.__data.pop('User')
        self.__data.pop('Personalization')
        self.__data.pop('Age')

        results = np.array(results, dtype=[('Place',int),('Prob',float)])

        tf.keras.backend.clear_session()
        gc.collect()
        return [i[0] for i in np.sort(results, order='Prob')[-1*k:]]
    

    # Training
    def update_model(self, data, personalization, new_data=1):
        current_data, y_train = None, None

        if personalization is not None:
            personalization = [list(i.values())[0] for i in personalization]
            personalization = [1 if i in personalization else 0 for i in self.__category]
        else:
            personalization = [0] * len(self.__category)


        if new_data:
            index_data = [list(self.__data['Place']).index(int(i)) for i in data['place']]
            
            current_data = {
                'Img':[],
                'Category':[],
                'Place':[],
                # 'Age':[],
                'Personalization':[],
                'Age':[],
                'User':[]
            }

            for index, i in enumerate(index_data):
                current_data['Img'].append(self.__data['Img'][i])
                current_data['Category'].append(self.__data['Category'][i])
                current_data['Place'].append(int(data['place'][index]))
                current_data['Personalization'].append(personalization)
                current_data['Age'].append(20)
                current_data['User'].append(int(data['user'][0]))

            current_data['Img'] = np.array(current_data['Img'])

            y_train = [float(3) for i in range(len(index_data))]
        
        else:
            index_data = list(self.__data['Place']).index(data.place.place_id)

            current_data = {
                'Img':self.__data['Img'][index_data:index_data+1],
                'Category':self.__data['Category'][index_data:index_data+1],
                'Place':[data.place.place_id],
                # 'Age':[data.user.age],
                'Personalization':[personalization],
                'Age':[data.user.age],
                'User':[data.user.id]
            }

            y_train = [float(data.place_ratings)]
        
        # Normalize
        y_train = np.array([dp.DataPreprocessing(i).normalization_min_max() for i in y_train])

        if self.__ensemble:
            self.__ensemble.compile(
                loss = 'mae',
                optimizer=tf.keras.optimizers.Adam(0.05), #0.0001
                metrics=['mae','mse'],
                jit_compile=False
            ) # XLA error CUDA jit_compile True

            self.__ensemble.fit(
                x=[current_data[i] if i == 'Img' else np.array(current_data[i]) for i in list(current_data.keys())[::-1]],
                y=y_train,
                batch_size=1,
                epochs=1,
            )
        else:
            self.__model.fit(
                x=[current_data[i] if i == 'Img' else np.array(current_data[i]) for i in list(current_data.keys())[::-1]],
                y=y_train,
                batch_size=1,
                epochs=1,
            )
        
        tf.keras.backend.clear_session()
        # gc.collect()

        return f"Model Trained"




# Text-based
class ContentRecc():
    def __init__(self, data):
        self.__data = data.values_list('place_name', flat=True)
        self.__feature_extractor = TfidfVectorizer(ngram_range=(1,2))
    
    def vectorized_similarity(self, id, k=5):
        self.__id = list(self.__data).index(self.__data.get(place_id=id))
        
        features = self.__feature_extractor.fit_transform(self.__data).toarray()

        similarity = cosine_similarity([features[self.__id]], features).reshape(-1)
        similarity = np.array([(i+1, probs) for i, probs in enumerate(similarity)], dtype=[('Place','int'),('Probs','float')])
        similarity =  np.sort(similarity, order='Probs')[(-1)*(k+1):-1]
        return [i[0] for i in similarity]
        






