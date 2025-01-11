from flask import Blueprint, request, jsonify
from services.keyword_extractor_service import extract_keywords

keyword_bp = Blueprint('keyword', __name__)

@keyword_bp.route('/extract-keywords', methods=['POST'])
def handle_keyword_extraction():
    """
    Endpoint to handle keyword extraction
    
    Returns:
        JSON response with extracted keywords or error message
    """
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({"error": "URL is required in the POST body"}), 400
        
        keywords = extract_keywords()
        return jsonify({"keywords": keywords}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500