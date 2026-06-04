# Movie Recommender System
This project is a movie recommendation web application that helps users discover movies based on their interests. The aim of this project was to understand and implement recommendation system techniques commonly used by streaming platforms and online content services. The application uses both Content-Based Filtering and Collaborative Filtering approaches to generate movie recommendations. Content-based filtering recommends movies by analyzing features such as genres, keywords, cast, and crew, while collaborative filtering identifies patterns in user preferences and ratings to suggest movies that similar users have enjoyed. The system is built using Python and machine learning libraries, with Streamlit providing an interactive and user-friendly interface. Users can select a movie and receive a list of relevant recommendations along with movie posters, making the experience engaging and easy to use.

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit
* Pickle
* MovieLens Dataset

## Working

First, select the type of recommendation you want: Content-Based Filtering or Collaborative Filtering. For Content-Based Filtering, enter the name of a movie and click Get Recommendations. The system will suggest movies that are similar to the selected movie. For Collaborative Filtering, select one of the available user IDs and click Get Recommendations. The system will recommend movies based on what users with similar preferences have liked and rated. This way, recommendations can be generated either from movie similarities or from user preferences.
