from nltk.sentiment.vader import SentimentIntensityAnalyzer


def sa(uinp):
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(uinp)
    print(score)
    if not score["pos"]:
        return score["pos"] - score["neg"] + score["neu"]/4
    else:
        return score["pos"] - score["neg"]

if __name__ == '__main__':
    print(sa("happy"))
    print(sa("sad"))