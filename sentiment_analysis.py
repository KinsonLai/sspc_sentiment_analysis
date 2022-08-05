from nltk.sentiment.vader import SentimentIntensityAnalyzer


def sa(uinp):
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(uinp)
    if not score["pos"] == 0:
        return score["pos"] - score["neg"] + score["neu"]/4
    else:
        return score["pos"] - score["neg"]
