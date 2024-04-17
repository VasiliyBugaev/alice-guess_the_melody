from pathlib import Path
import random
import csv


class CsvAnswerParser:
    def __init__(self, path: str = 'answers.csv'):
        file_path = Path(__file__).with_name(path)
        with file_path.open('r', encoding='utf-8') as csvfile:
            answer_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            self.links = []
            self.song_writers = []
            self.songs = []
            self.used = []
            self.audio = self.song_writer = self.song = None
            for row in answer_reader:
                self.links.append(row[0])
                self.song_writers.append(row[1])
                self.songs.append(row[2])

    def random_data(self):
        max_num = len(self.links)
        random_index = random.choice([e for e in range(max_num) if e not in self.used])
        self.used.append(random_index)
        self.audio = self.links[random_index]
        self.song_writer = self.song_writers[random_index]
        self.song = self.songs[random_index]

    def get_answer(self):
        assert self.song_writer
        assert self.song
        return self.song_writer, self.song

    def get_audio(self):
        assert self.audio
        return self.audio
