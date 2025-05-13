# Hybrid Tourism Recommender System
<p align="justify">
  In the industrial 4.0 era, there is an explosion of unstructured and structured data that produces broad and varied  knowledge  information  that  humans cannot  process  quickly.  This  issue  makes  the  existence  of recommendation   systems   meaningful.   This   system   studies   the   existing   information   and   provides suggestions according to the user's will. In the past, many recommendation systems have focused more on content-based  filtering methods  where  recommendation  results  are similarbased  on  the  features  of  the Content that match the user's personality. This method limits the variety of information that is relevant to users.  In  addition,  in  the  context  of  tourist  attractions,  many  studies  have  not  used  image  data  that  can contain many objects in one frame as a determining factor in providing recommendations. Therefore, in this study, the authors propose to add image features as one of the parameters of the recommendation system to determine the impact of using image features on the model performance. The best performance obtained is 0.364 RMSE metric using the Hybrid Image method.
</p>


<p align="center">
  <img src="https://github.com/pinantyo/Hybrid-Recommender-System/blob/main/HybridModel.jpg" alt="Centered Image" />
</p>

<div align="center">
  
| Method  | NDCG@5 | Accuracy@5 |	MSE |	RMSE |	MAE |
| ------------- | :--------------: | :--------------: | :--------------: | :--------------: | :--------------: |
| Matrix Factorization (MF) | 38.4%	| 52.7% |	0.653 |	0.808 |	0.649 |
| Neural Collaborative Filtering (NCF) | 15.9% | 51.8% | 0.179 | 0.423 | 0.348 |
| Hybrid Text Feature (Category + City) |	42.8% |	49.9% |	0.160 |	0.400 |	0.333 |
| Neural Collaborative Filtering Image | 62.8% | 52.1% | 0.219 | 0.468 | 0.376 |
| Matrix Factorization Image | 28.2% | 54.6% | 0.158 | 0.398 | 0.332 |
| Hybrid MF Image Recommendation (Personalized) | 71.5% | 53.8% | 0.133 | 0.364 | 0.309 |
| Hybrid NCF Image Recommendation (Personalized) | 85.8% | 52.7% | 0.133 | 0.364 | 0.311 |
| Hybrid MF + NCF Image Recommendation (Personalized) | 60.2% | 56.2% | 0.142 | 0.376 | 0.317 |
  
</div>
