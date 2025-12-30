
import json
import os
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from nerna import load_annotations_from_json, NERAnnotator

def test_load_annotations():
    # Create a dummy JSON file
    dummy_data = [
        {
            "text_id": "session_0",
            "text_index": 0,
            "original_text": "Hello World",
            "entities": [{"text": "World", "type": "Location", "start": 6, "end": 11}]
        }
    ]
    
    filename = "test_annotations.json"
    with open(filename, "w") as f:
        json.dump(dummy_data, f)
        
    try:
        # Test loading
        loaded_data = load_annotations_from_json(filename)
        print("Loaded data:", loaded_data)
        
        assert len(loaded_data) == 1
        assert loaded_data[0]['original_text'] == "Hello World"
        assert loaded_data[0]['entities'][0]['type'] == "Location"
        
        print("✅ load_annotations_from_json validation passed!")
        
    finally:
        if os.path.exists(filename):
            os.remove(filename)

def test_annotator_structure():
    # Just verify the method exists
    annotator = NERAnnotator(["Test"])
    assert hasattr(annotator, 'set_annotations')
    assert hasattr(annotator, 'annotations')
    print("✅ NERAnnotator structure passed!")

if __name__ == "__main__":
    test_load_annotations()
    test_annotator_structure()
