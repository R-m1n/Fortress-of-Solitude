
def charrier(sentence: str) -> list:
    return sorted({letter: sentence.count(letter) for letter in sentence}.items(), key=lambda repeated: repeated[1], reverse=True)
