from flask import Flask, request, jsonify
from lotsawa_transliterator import transliterate_text  # Assuming you have your Python transliterator here

app = Flask(__name__)

@app.route('/transliterate', methods=['POST'])
def transliterate():
    data = request.json
    romanized_text = data.get('text', '')
    
    # Transliterate the text using your Python function
    tibetan_text = transliterate_text(romanized_text)  # Your transliterator logic
    
    return jsonify({'tibetan': tibetan_text})

if __name__ == '__main__':
    app.run(debug=True)
