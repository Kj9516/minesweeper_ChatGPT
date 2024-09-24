import json

class Scoreboard:
    def __init__(self, filename='scores.json'):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_score(self, time):
        self.scores.append(time)
        self.scores.sort()
        with open(self.filename, 'w') as f:
            json.dump(self.scores, f)
