import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from matplotlib import rcParams
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False

categories = {
    "tweetTimeline" : {
        "title": "Number of Tweets Timeline",
        "xlabel": "Period",
        "ylabel": "Number of Tweets"
    },
    "sentimentTimeline" : {
        "title": "Average Sentiment Timeline",
        "xlabel": "Period",
        "ylabel": "Average Sentiment"
    }
}

class Graph():
    def __init__(self):
        super().__init__()
        self.n = 0
        
    def generateLineGraph(self, x, y, category, startDate=None, endDate=None):
        path =  'data/tmp/' + str(self.n) + '.png'
        plt.figure(figsize=(12, 4))
        plt.grid(color='#F2F2F2', alpha=1, zorder=0)
        plt.plot(x, y, marker="o", color='#087E8B', lw=3, zorder=5)
        if (startDate):
            plt.title(categories[category]['title']+' from '+startDate+' to '+endDate, fontsize=17)
        else:
            plt.title(categories[category]['title'], fontsize=17)
        plt.xlabel(categories[category]['xlabel'], fontsize=13)
        plt.xticks(fontsize=9)
        plt.ylabel(categories[category]['ylabel'], fontsize=13)
        plt.yticks(fontsize=9)
        plt.savefig(path, dpi=300, bbox_inches='tight', pad_inches=0)
        plt.close()
        self.n += 1

        return path

    def generateWordcloud(self, arr, startDate=None, endDate=None):
        path =  'data/tmp/' + str(self.n) + '.png'
        arr = arr.replace('https://t.co', '')
        wordcloud = WordCloud(width= 3000, height = 1000, random_state=1, background_color='salmon', colormap='Pastel1', collocations=False, stopwords = STOPWORDS).generate(arr)
        plt.figure(figsize=(12, 4))
        plt.imshow(wordcloud) 
        if (startDate):
            plt.title('Wordcloud from '+startDate+' to '+endDate, fontsize=17)
        else:
            plt.title('Wordcloud', fontsize=17)
        plt.axis("off")
        plt.savefig(path, dpi=300, bbox_inches='tight', pad_inches=0)
        plt.close()
        self.n += 1

        return path

