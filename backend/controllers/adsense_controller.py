from flask import Blueprint, request, jsonify
from services.adsense_services import ads_earning
import asyncio
adsense_bp = Blueprint('adsense', __name__)

@adsense_bp.route('/ads-earning', methods=['POST'])
def handle_ads_earning():
    try:
        data = request.json
        # clientName = data.get('clientName')
        dateStart = data.get('dateStart')
        dateEnd = data.get('dateEnd')
        # countryName = data.get('countryName')
        channelName = data.get('channelName')
        viewMode = data.get('viewMode')

        response = asyncio.run(ads_earning(dateStart,dateEnd,channelName,viewMode))
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    