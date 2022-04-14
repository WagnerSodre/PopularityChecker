from datetime import datetime, timedelta

from matplotlib.pyplot import xlabel

class Utils():
    def __init__(self):
        super().__init__()

    def sort(self, arr, xLabel, yLabel):
        arr.sort(key=lambda r: int((datetime.strptime(r[xLabel], '%Y-%m-%dT%H:%M:%S.%fZ') - datetime(1970, 1, 1)).total_seconds()))

        x = [datetime.strptime(date[xLabel].split('T')[0], "%Y-%m-%d").date() for date in arr]
        y = [data[yLabel] for data in arr]
        
        return x, y

    def getOutliers(self, arr, xLabel, yLabel, zLabel, average):
        res = []
        for row in arr:
            if row[zLabel] > average * 5:
                start = datetime.strptime(row[xLabel].split('T')[0], "%Y-%m-%d").date() - timedelta(days=7)
                end = datetime.strptime(row[yLabel].split('T')[0], "%Y-%m-%d").date() + timedelta(days=7)
                res.append({"start": start.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), "end": end.strftime('%Y-%m-%dT%H:%M:%S.%fZ')})

        return res

    def filterTweetCount(self, arr, outlier):
        filtered = list(filter(lambda x: x['start'] >= outlier['start'] and x['end'] <= outlier['end'], arr))
        return self.sort(filtered, 'start', 'tweet_count')

    def chunks(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
            