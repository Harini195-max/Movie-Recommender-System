import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")


user_movie_matrix = ratings.pivot_table(
    index="userId",
    columns="movieId",
    values="rating"
).fillna(0)


user_similarity = cosine_similarity(user_movie_matrix)

def recommend_for_user(user_id, num_recommendations=5):
    if user_id not in user_movie_matrix.index:
        return ["User ID not found"]

    user_idx = user_movie_matrix.index.tolist().index(user_id)
    similarity_scores = user_similarity[user_idx]

    weighted_ratings = similarity_scores @ user_movie_matrix.values
    weighted_ratings = weighted_ratings / similarity_scores.sum()

    movie_scores = pd.Series(weighted_ratings, index=user_movie_matrix.columns)

    watched_movies = ratings[ratings["userId"] == user_id]["movieId"]
    movie_scores = movie_scores.drop(watched_movies, errors="ignore")

    top_movies = movie_scores.sort_values(ascending=False).head(num_recommendations)

    recommended_titles = movies[movies["movieId"].isin(top_movies.index)]["title"]

    return recommended_titles.tolist()
