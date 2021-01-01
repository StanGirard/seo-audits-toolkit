from summarizer import Summarizer

def summarizer_bert(text):
    model = Summarizer()
    result = model(text, min_length=60)
    full = ''.join(result)
    return full