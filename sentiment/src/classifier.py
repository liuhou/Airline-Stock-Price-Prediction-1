class Entry:
    """Entry in the dictionary"""
    def __init__(self, line):
        attributes = line.split('\t', 8)
        self.word = attributes[0]
        self.happiness_mean = float(attributes[2])
        self.happiness_var = float(attributes[3])


class NaiveClassifier:
    """Naive classifier with bag of words."""
    def __init__(self, fn):
        self.dictionary = {}
        with open(fn) as f:
            for line in f:
                if len(line) > 1 and line[0] != '#':
                    entry = Entry(line)
                    # Not consider the neutral word.
                    if entry.happiness_mean > 6.0 or entry.happiness_mean < 4.0:
                        self.dictionary[entry.word] = entry

    def toBag(self, twitter):
        text = twitter.replace(',', ' ')
        text = text.strip().lower()
        return text.split()

    def showReason(self, twitter):
        bag = self.toBag(twitter)
        for word in bag:
            if word in self.dictionary:
                # print word, self.dictionary[word].happiness_mean
                # Weight the mean by the 1 / variance.
                print word + " " + str(self.dictionary[word].happiness_mean) + " " + str(self.dictionary[word].happiness_var)

    def classify(self, twitter):
        cnt = 0
        var_sum = 0.0
        happiness_sum = 0.0
        bag = self.toBag(twitter)
        for word in bag:
            if word in self.dictionary:
                cnt += 1
                # print word, self.dictionary[word].happiness_mean
                # Weight the mean by the 1 / variance.
                var = 1.0 / self.dictionary[word].happiness_var
                happiness = self.dictionary[word].happiness_mean
                happiness_sum += var * happiness
                var_sum += var
        if cnt < 1:
            # Not enough sentiment words.
            return -1.0
        else:
            return happiness_sum / var_sum
