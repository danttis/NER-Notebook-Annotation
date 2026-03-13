# NERNA (NER & Text Classification for Notebooks)

Follow the official repository: [NER-Notebook-Annotation - GitHub](https://github.com/danttis/NER-Notebook-Annotation/) 	


**NERNA** is a lightweight package designed for **Named Entity Recognition (NER) annotation** and **Text Classification** directly within Python notebooks.

Originally intended as a Streamlit-based interface, it has been reworked to run natively inside notebook environments (such as Jupyter, Google Colab, Databricks, etc.). This makes it easier to use without requiring deployment of web applications or cloud server contracts.

## Key Features

* ✅ Lightweight, interactive JavaScript interface embedded in notebooks
* ✅ Compatible with local notebooks and cloud platforms (e.g., Colab, Databricks)
* ✅ Supports both Span-level NER Annotation and Document-level Classification
* ✅ No need for external servers or deployments
* ⚠️ Annotations are made using **JavaScript**, so **they cannot be accessed directly as Python variables**. However, the input to the tool must be a **Python list of strings (or a list of `[id, text]` tuples)**.

---

## 1. NER Annotation

```python
from nerna import NERAnnotator

# List of texts to annotate
texts = [
    'Brazil won the 2002 World Cup.',
    'The planet’s drinking water is running out.'
]

# Initialize annotation (optionally customize labels)
annotator = NERAnnotator(texts, labels=['Location', 'Date', 'Event'])

# Render the interactive annotation interface
annotator.render(variable_name="annotator")
```

After annotating in the UI, click **"🐍 Export to Python"** and access your data:
```python
print(annotator.annotations)
```

---

## 2. Text Classification

The `TextClassifier` provides a fast way to label entire documents with a single click.

```python
from nerna import TextClassifier

# Using tuples to preserve document IDs
data = [
    ["doc_01", "The new smartphone has a great battery life but the camera is sub-par."],
    ["doc_02", "I love the design, very sleek and modern!"]
]

labels = ["Positive", "Negative", "Neutral"]

# Initialize the classifier
classifier = TextClassifier(texts=data, labels=labels)

# Render the UI
classifier.render(variable_name="classifier")
```

After classifying in the UI, click **"🐍 Export to Python"** and retrieve:
```python
print(classifier.classifications)
# Output format: {"doc_01": "Negative", "doc_02": "Positive"}
```

---

## Notes

### Retrieving Data

There are two ways to retrieve the annotated data back into Python:

**Option A: Export to Python Variable (Recommended for Colab/Jupyter)**

Pass the name of your variable to the `render` method:
```python
annotator.render(variable_name="annotator")
# or for classification:
# classifier.render(variable_name="classifier")
```
*   In the UI, click the **"🐍 Export to Python"** button.
*   Access the data in Python via `.annotations` or `.classifications`.

**Option B: Load from JSON (Fallback)**

*   Click **"📥 Download JSON"** in the UI to save a `.json` file.
*   Load it manually in Python.

---

* Ideal for manual review, small-scale labeling tasks, or quick experimentation in NLP workflows.

