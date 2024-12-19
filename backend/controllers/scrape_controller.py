from flask import Blueprint, request, jsonify
from services.scraper.scraper_service import scrape_blog_posts

scrape_bp = Blueprint('scrape', __name__)

@scrape_bp.route('/scrape', methods=['POST'])
def handle_scrape():
    """
    Endpoint to handle web scraping
    
    Returns:
        JSON response with scraped blog posts or error message
    """
    try:
        # Check if request is JSON
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({"error": "URL is required"}), 400

        # Scrape blog posts
        results = scrape_blog_posts(url)

        if results:
            return jsonify(results)
        else:
            return jsonify({"error": "No blog data found"}), 404

    except Exception as e:
        print(f"Error: {str(e)}")  # Log the exception
        return jsonify({'error': str(e)}), 500