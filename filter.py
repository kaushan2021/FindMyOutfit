import numpy as np
import pandas as pd

df = pd.read_csv('outfit.csv')
print("Find My Outfit ")

# print(df)
del df["year"]
del df["Unnamed: 10"]
del df["Unnamed: 11"]

age = 30
gender = "Men"
event = "Sports"
season = "Summer"

# Reccomended Topwear
topwear = df.loc[
    (df['subCategory'] == 'Topwear') & (df['gender'] == gender) & (df['usage'] == event) & (df['season'] == season)]

# Reccomended Bottomwear
bw = pd.read_csv('outfit.csv')
del bw["year"]
del bw["Unnamed: 10"]
del bw["Unnamed: 11"]
bottomwear = bw.loc[
    (df['subCategory'] == 'Bottomwear') & (df['gender'] == gender) & (df['usage'] == event) & (df['season'] == season)]

# Reccomended Footwear
fw = pd.read_csv('outfit.csv')
del fw["year"]
del fw["Unnamed: 10"]
del fw["Unnamed: 11"]
footwear = df.loc[
    (df['masterCategory'] == 'Footwear') & (df['gender'] == gender) & (df['usage'] == event) & (df['season'] == season)]

# Normal Filtering Method
print("Reccomended Topwear")
top = topwear['id'].sample(5).to_numpy()
print(top)

print("Reccomended Bottomwear")
bottom = bottomwear['id'].sample(5).to_numpy()
print(bottom)

print("Reccomended Footwear")
foot = footwear['id'].sample(5).to_numpy()
print(foot)

# top,bottom,foot arrays need to be sent to the front end

#######################################################
# collaborative  filtering

ratings_df = pd.read_csv('ratings.csv')

userInput = [
    {'outfitID': 5, 'rating': 5},
    {'outfitID': 2, 'rating': 3.5},
    {'outfitID': 296, 'rating': 2},
    {'outfitID': 1274, 'rating': 5},
    {'outfitID': 1938, 'rating': 4.5}
]
inputOutfit = pd.DataFrame(userInput)

userSubset = ratings_df[ratings_df['outfitID'].isin(inputOutfit['outfitID'].tolist())]

# Groupby creates several sub dataframes where they all have the same value in the column specified as the parameter
userSubsetGroup = userSubset.groupby(['userId'])

userSubsetGroup = sorted(userSubsetGroup, key=lambda x: len(x[1]), reverse=True)

userSubsetGroup = userSubsetGroup[0:100]

# Store the Pearson Correlation in a dictionary, where the key is the user Id and the value is the coefficient
pearsonCorrelationDict = {}

# For every user group in our subset
for name, group in userSubsetGroup:

    # sorting the input and current user group so the values aren't mixed up later on
    group = group.sort_values(by='outfitID')
    inputOutfit = inputOutfit.sort_values(by='outfitID')

    # Get the N (total similar movies watched) for the formula
    nRatings = len(group)

    # Get the review scores for the movies that they both have in common
    temp_df = inputOutfit[inputOutfit['outfitID'].isin(group['outfitID'].tolist())]

    # store them in a temporary buffer variable in a list format to facilitate future calculations
    tempRatingList = temp_df['rating'].tolist()

    # put the current user group reviews in a list format
    tempGroupList = group['rating'].tolist()

    # calculate the pearson correlation between two users, so called, x and y

    Sxx = sum([i ** 2 for i in tempRatingList]) - pow(sum(tempRatingList), 2) / float(nRatings)
    Syy = sum([i ** 2 for i in tempGroupList]) - pow(sum(tempGroupList), 2) / float(nRatings)
    Sxy = sum(i * j for i, j in zip(tempRatingList, tempGroupList)) - sum(tempRatingList) * sum(tempGroupList) / float(
        nRatings)

    # If the denominator is different than zero, then divide, else, 0 correlation.
    if Sxx != 0 and Syy != 0:
        pearsonCorrelationDict[name] = Sxy / np.sqrt(Sxx * Syy)
    else:
        pearsonCorrelationDict[name] = 0

pearsonDF = pd.DataFrame.from_dict(pearsonCorrelationDict, orient='index')

pearsonDF.columns = ['similarityIndex']
pearsonDF['userId'] = pearsonDF.index
pearsonDF.index = range(len(pearsonDF))

topUsers = pearsonDF.sort_values(by='similarityIndex', ascending=False)[0:50]

topUsersRating = topUsers.merge(ratings_df, left_on='userId', right_on='userId', how='inner')

topUsersRating['weightedRating'] = topUsersRating['similarityIndex'] * topUsersRating['rating']

tempTopUsersRating = topUsersRating.groupby('outfitID').sum()[['similarityIndex', 'weightedRating']]
tempTopUsersRating.columns = ['sum_similarityIndex', 'sum_weightedRating']

# Creates an empty dataframe
recommendation_df = pd.DataFrame()
# Now we take the weighted average
recommendation_df['weighted average recommendation score'] = tempTopUsersRating['sum_weightedRating'] / \
                                                             tempTopUsersRating['sum_similarityIndex']
recommendation_df['outfitID'] = tempTopUsersRating.index

recommendation_df = recommendation_df.sort_values(by='weighted average recommendation score', ascending=False)

outfits = ratings_df.loc[ratings_df['outfitID'].isin(recommendation_df['outfitID'].tolist())]

# Recommended top 10 outfits
print()
print("Top 10 collaborative filtering outfits")
topTen=outfits[['outfitID']].head(5).to_numpy()
print(topTen)


