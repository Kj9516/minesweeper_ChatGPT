# scoreboard.py

import csv
from datetime import datetime

class Scoreboard:
    def __init__(self, filename='scores.csv'):
        self.filename = filename

    def save_score(self, level, width, height, mines, time_spent):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([now, level, width, height, mines, time_spent])

    def load_scores(self):
        scores = []
        try:
            with open(self.filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    score = {
                        'datetime': row[0],
                        'level': row[1],
                        'width': int(row[2]),
                        'height': int(row[3]),
                        'mines': int(row[4]),
                        'time': float(row[5])
                    }
                    scores.append(score)
                scores.sort(key=lambda x: x['time'])
                return scores
        except FileNotFoundError:
            return []
