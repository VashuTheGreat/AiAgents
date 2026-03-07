from keybert import KeyBERT

kw_model = KeyBERT()

doc = """
Deep learning uses neural networks with multiple layers.
CNNs are widely used for image recognition.
"""

keywords = kw_model.extract_keywords(doc, top_n=5)

print(keywords)