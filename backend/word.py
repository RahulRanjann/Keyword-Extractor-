from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import urllib.parse

html_snippet = '''
<div class="w-full mb-4" id="relatedsearches1" style="height: auto;">
    <iframe frameborder="0" marginwidth="0" marginheight="0" allowtransparency="true" scrolling="no" width="100%"
    name="{&quot;name&quot;:&quot;master-1&quot;,&quot;master-1&quot;:{&quot;container&quot;:&quot;relatedsearches1&quot;,&quot;styleId&quot;:&quot;2513417533&quot;,&quot;personalizedAds&quot;:false,&quot;adPage&quot;:1,&quot;domainName&quot;:&quot;fastanswershere.com&quot;,&quot;fexp&quot;:&quot;21404,17301437,17301438,17301442,17301266,72717108,49280903,72771953&quot;,&quot;masterNumber&quot;:1,&quot;number&quot;:0,&quot;pubId&quot;:&quot;pub-1203149545224208&quot;,&quot;role&quot;:&quot;m&quot;,&quot;sct&quot;:&quot;ID=9db6c00b9a32cd20:T=1733475358:RT=1733475358:S=ALNI_MbOQxUuLnITes75nxrINDiI3472lw&quot;,&quot;sc_status&quot;:6,&quot;adLoadedCallback&quot;:null,&quot;hl&quot;:&quot;en&quot;,&quot;resultsPageBaseUrl&quot;:&quot;https://fastanswershere.com/search-result-pick-up-truck-a-versatile-vehicle-for-every-need?mode=light&amp;channel=null&amp;network=null&amp;sid=2513417533&amp;theme=0&quot;,&quot;resultsPageQueryParam&quot;:&quot;query&quot;,&quot;terms&quot;:&quot;Pickup Trucks for Sale Near Me, Pickup Truck Secondhand, Pickup Trucks Used For Sale, Pickup Truck for Sale, Ford F150 Pickup Truck, Used Pickup Trucks for Sale, Cheap Pickup Trucks For Sale, Used Pickup Trucks For Sale Near Me&quot;,&quot;kw&quot;:&quot;Pick-Up Truck: A Versatile Vehicle for Every Need&quot;,&quot;ie&quot;:&quot;UTF-8&quot;,&quot;maxTop&quot;:4,&quot;minTop&quot;:0,&quot;numRepeated&quot;:0,&quot;oe&quot;:&quot;UTF-8&quot;,&quot;relatedSearches&quot;:8,&quot;type&quot;:&quot;relatedsearch&quot;,&quot;linkTarget&quot;:&quot;_blank&quot;,&quot;relatedSearchTargeting&quot;:&quot;content&quot;,&quot;ignoredPageParams&quot;:&quot;channel,campaignid,tid,gad_source,gclid,t,utm_source,wbraid,gbraid,fbclid,g_ci,subId,rf,network,creative,utm_medium,tblci,g_ai,nx,mibextid,utm_campaign,recirc,ny,continueFlag,utm_id,mb,testAd&quot;}}"
    id="master-1" src="https://syndicatedsearch.goog/afs/ads?adsafe=low&amp;adtest=off&amp;psid=2513417533&amp;pcsa=false&amp;adpage=1&amp;client=pub-1203149545224208&amp;r=m&amp;sct=ID%3D9db6c00b9a32cd20%3AT%3D1733475358%3ART%3D1733475358%3AS%3DALNI_MbOQxUuLnITes75nxrINDiI3472lw&amp;sc_status=6&amp;hl=en&amp;rpbu=https%3A%2F%2Ffastanswershere.com%2Fsearch-result-pick-up-truck-a-versatile-vehicle-for-every-need%3Fmode%3Dlight%26channel%3Dnull%26network%3Dnull%26sid%3D2513417533%26theme%3D0&amp;rpqp=query&amp;terms=Pickup%20Trucks%20for%20Sale%20Near%20Me%2C%20Pickup%20Truck%20Secondhand%2C%20Pickup%20Trucks%20Used%20For%20Sale%2C%20Pickup%20Truck%20for%20Sale%2C%20Ford%20F150%20Pickup%20Truck%2C%20Used%20Pickup%20Trucks%20for%20Sale%2C%20Cheap%20Pickup%20Trucks%20For%20Sale%2C%20Used%20Pickup%20Trucks%20For%20Sale%20Near%20Me&amp;kw=Pick-Up%20Truck%3A%20A%20Versatile%20Vehicle%20for%20Every%20Need"
    data-observe="1" allow="attribution-reporting" style="visibility: visible; height: 657px; display: block;" title=""></iframe>
</div>
'''

# Parse the HTML
soup = BeautifulSoup(html_snippet, 'html.parser')

# Find the iframe and extract its src attribute
iframe = soup.find('iframe')
src_url = iframe['src']

# Parse the URL and extract the 'terms' parameter
parsed_url = urlparse(src_url)
params = parse_qs(parsed_url.query)
terms = params.get('terms', [''])[0]

# Decode and split the terms
keywords = urllib.parse.unquote(terms).split(', ')

# Output the keywords
print(keywords)
