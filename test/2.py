import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import time
from scipy import stats


# 时间转换函数
# 输入参数：arr：长整型时间
# 输出：年份
def return_time(arr):
    return time.strftime('%Y', time.localtime(arr))


# 评分转换函数
# 输入参数：score：某部电影的总成绩，comments：某部电影的评论数
# 输出：某部电影成绩的贝叶斯均值
# 即：（某部电影的总成绩+所有电影的总成绩）/（某部电影的评论+所有电影的评论）
def return_rating(scores, comments):
    return (mean * mean_comments + scores) / (comments + mean_comments)

#读取文件，
movies = pd.read_csv('ml-latest-small/movies.csv')
ratings = pd.read_csv('ml-latest-small/ratings.csv')

num_ratings = ratings.shape[0]
num_movies = movies.shape[0]
mean_comments = num_ratings / num_movies

# 这一段是要把movie表genres列的类型按照|分开，再重新把类型按列排列，删掉没用的列
# 最后把修改好的类型列和原表合并
new_movies = pd.DataFrame(movies.genres.str.split('|').tolist(), index=movies.movieId)
new_movies = new_movies.stack().reset_index()
new_movies = new_movies.drop('level_1', axis=1).rename(columns={0: 'genres'})
new_movies = pd.merge(movies.drop('genres', axis=1), new_movies)
print(new_movies)
# 这一段是要把rating表timestamp列转换成年份便于计算
ratings['timestamp'] = ratings['timestamp'].apply(return_time)
print(ratings)
# 这一段把movie表的genres属性列与rating表合并，以看出电影类型与评分的关系
movie_ratings = ratings.merge(new_movies.drop('title', axis=1), on='movieId', how='inner')
print(movie_ratings)

# 统计每个类型电影的数目，并选出种类最多的一部分电影
movie_ratings2 = movie_ratings.groupby(['genres'], as_index=False)['movieId'].count().sort_values(by='movieId',
                                                                                                  ascending=0)
print(movie_ratings2)
movie_ratings2 = movie_ratings2.loc[movie_ratings2['movieId'] > 200000]
movie_ratings = movie_ratings.loc[movie_ratings['genres'].isin(movie_ratings2['genres'])]
#print(movie_ratings)
# 统计每年的各类型电影平均评分情况，和每部电影的总的平均评分情况，每部电影每年的平均评分情况
mean_genres_ratings = movie_ratings.groupby(['timestamp', 'genres'], as_index=False)['rating'].agg(np.mean)
mean_genres_ratings.rename(columns={'timestamp': 'year'}, inplace=True)
print(mean_genres_ratings)
mean_movie_ratings = movie_ratings.drop("genres", axis=1)
mean_movie_ratings = mean_movie_ratings.groupby(['movieId'], as_index=False)['rating'].agg(np.mean)
mean_movie_ratings.rename(columns={'timestamp': 'year'}, inplace=True)
print(mean_movie_ratings)
mean_movie_annual_ratings = movie_ratings.groupby(['movieId', 'genres', 'timestamp'], as_index=False)['rating'].agg(
    np.mean)
mean_movie_annual_ratings.rename(columns={'timestamp': 'year'}, inplace=True)
print(mean_movie_annual_ratings)
# 进行可视化
seaborn.set(font_scale=1, rc={'lines.linewidth': 1.0, 'figure.figsize': (15, 10)})
seaborn.pointplot(x='year', y='rating', hue='genres', data=mean_genres_ratings, palette='hls')
plt.legend(bbox_to_anchor=(1.2, 0.5), loc=7)
plt.show()
seaborn.distplot(mean_movie_ratings['rating'])
plt.legend(bbox_to_anchor=(1.2, 0.5), loc=7)
plt.show()
data = mean_movie_annual_ratings.loc[mean_movie_annual_ratings['year'].isin(['2014', '2015', '2016', '2017', '2018'])]
seaborn.boxenplot(x='year', y='rating', hue='genres', data=data, palette='hls')
plt.legend(bbox_to_anchor=(1.2, 0.5), loc=7)
plt.show()

# 改善电影评分系统，使用贝叶斯均值
new_rating = movie_ratings.groupby(['movieId'], as_index=False)['rating'].agg([np.sum, np.size])
mean = sum(list(new_rating['sum'])) / sum(list(new_rating['size']))  # 所有电影的平均分
new_rating['new_rating'] = new_rating.apply(lambda x: return_rating(x['sum'], x['size']), axis=1)
new_rating = new_rating.reset_index()
# print(new_rating)
mean_movie_ratings = mean_movie_ratings.drop('rating', axis=1)
# print(mean_movie_ratings)
mean_movie_ratings = mean_movie_ratings.merge(movies.drop('genres', axis=1), on='movieId')
mean_movie_ratings = mean_movie_ratings.merge(new_rating[['movieId', 'new_rating']], on='movieId').sort_values(
    by='new_rating', ascending=0)
print(mean_movie_ratings.head(50))

# 对不同电影类型之间用户平均评分的关联程度进行分析
# 先找每个人对每类电影的评分情况,再加以组合
user_ratings = movie_ratings.groupby(['userId', 'genres'], as_index=False)['rating'].aggregate(np.mean)
#print(user_ratings)
pivot = user_ratings.pivot_table(index='userId', columns='genres', values='rating')
print(pivot)

seaborn.set(style='darkgrid')
g = seaborn.FacetGrid(user_ratings, col='genres', height=5)
g.map(seaborn.distplot, 'rating')
plt.show()
g = seaborn.jointplot('Comedy', 'Adventure', pivot, kind='reg', color='g',height=10)
g.annotate(stats.pearsonr)
plt.show()