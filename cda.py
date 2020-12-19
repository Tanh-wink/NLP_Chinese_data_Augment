import jieba
import synonyms
import random
from random import shuffle

random.seed(100)

class CDA_class():
    def __init__(self, stop_word_path, alpha=0.3):

        # 参数配置
        self.alpha = alpha
        # 停用词加载
        self.stop_word_path = stop_word_path
        self.stop_words = self.get_stop_word(self.stop_word_path)

    # 功能：同义词替换，替换一个语句中的n个单词为其同义词
    def synonym_replacement(self, sentence):
        # segment sentence
        words, num_words = self.cut_word(sentence)
        n = max(1, int(self.alpha * num_words))
        new_words = words.copy()
        random_word_list = list(set([word for word in words if word not in self.stop_words]))
        random.shuffle(random_word_list)
        num_replaced = 0
        for random_word in random_word_list:
            synonyms = self.get_synonyms(random_word)
            if len(synonyms) >= 1:
                synonym = random.choice(synonyms)
                new_words = [synonym if word == random_word else word for word in new_words]
                num_replaced += 1
            if num_replaced >= n:
                break
        new_sentence = ''.join(new_words)
        return new_sentence

    def get_synonyms(self, word):
        return synonyms.nearby(word)[0]

    # 功能：随机插入,随机在语句中插入n个词
    def random_insertion(self, sentence):
        words, num_words = self.cut_word(sentence)
        n = max(1, int(self.alpha * num_words))
        new_words = words.copy()
        for _ in range(n):
            self.add_word(new_words)
        return new_words

    def add_word(self, new_words):
        synonyms = []
        counter = 0
        while len(synonyms) < 1:
            random_word = new_words[random.randint(0, len(new_words) - 1)]
            synonyms = self.get_synonyms(random_word)
            counter += 1
            if counter >= 10:
                return
        random_synonym = random.choice(synonyms)
        random_idx = random.randint(0, len(new_words) - 1)
        new_words.insert(random_idx, random_synonym)

    # 功能：随机交换：随机交货句子中的两个词
    def random_swap(self, sentence):
        words, num_words = self.cut_word(sentence)
        n = max(1, int(self.alpha * num_words))
        new_words = words.copy()
        for _ in range(n):
            new_words = self.swap_word(new_words)
        return new_words

    def swap_word(self, new_words):
        random_idx_1 = random.randint(0, len(new_words) - 1)
        random_idx_2 = random_idx_1
        counter = 0
        while random_idx_2 == random_idx_1:
            random_idx_2 = random.randint(0, len(new_words) - 1)
            counter += 1
            if counter > 3:
                return new_words
        new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
        return new_words

    # 功能：随机删除，以概率p删除语句中的词
    def random_deletion(self, sentence):
        words, num_words = self.cut_word(sentence)
        if len(words) == 1:
            return words
        new_words = []
        for word in words:
            r = random.uniform(0, 1)
            if r > self.alpha:
                new_words.append(word)

        if len(new_words) == 0:
            rand_int = random.randint(0, len(words) - 1)
            return [words[rand_int]]

        return new_words

    # 功能：分词
    def cut_word(self, sentence):
        seg_list = jieba.cut(sentence)
        seg_list = " ".join(seg_list)
        words = list(seg_list.split())
        num_words = len(words)
        return words, num_words

    # 功能：停用词表加载
    def get_stop_word(self, stop_word_path):
        # 停用词列表，默认使用哈工大停用词表
        f = open(stop_word_path, encoding='utf-8')
        stop_words = list()
        for stop_word in f.readlines():
            stop_words.append(stop_word[:-1])
        return stop_words


if __name__ == '__main__':
    stop_word_path = "../data/stopwords/HIT_stop_words.txt"
    cda_class = CDA_class(stop_word_path, alpha=0.5)
    sentence = '我给你约一下业主吧。'
    print(f"source sentence:{sentence}")
    new_sent = cda_class.synonym_replacement(sentence)
    print(f"new sentence:{new_sent}")