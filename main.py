# main.py
import os
import random
import time
import requests
import google.generativeai as genai
from dotenv import load_dotenv
 # schedule module no longer needed
from requests_oauthlib import OAuth1Session
import requests
from bs4 import BeautifulSoup
import time # To add delays and avoid being blocked

# --- Image Posting Logic ---
# Load environment variables from .env before any os.getenv calls
load_dotenv()

# --- Helper function to normalize GitHub URLs ---
def normalize_github_url(url):
    """
    Converts GitHub web interface URLs to raw content URLs.
    Example: https://github.com/user/repo/blob/main/file.jpg
    becomes: https://raw.githubusercontent.com/user/repo/main/file.jpg
    """
    if "github.com" in url and "/blob/" in url:
        url = url.replace("github.com", "raw.githubusercontent.com")
        url = url.replace("/blob/", "/")
    return url

# --- Image URLs Fetch Logic ---
# If IMAGE_URLS_URL is set in the environment, fetch the JSON from that URL.
# Otherwise, use the default list.
IMAGE_URLS_URL = os.getenv("IMAGE_URLS_URL", "https://raw.githubusercontent.com/Cheche-ship-it/dimension-marketing-snapshots/main/photos.json")
IMAGE_URLS = []
try:
    response = requests.get(IMAGE_URLS_URL, timeout=10)
    if response.status_code == 200:
        IMAGE_URLS = response.json()
        # Normalize all image URLs to use raw content URLs
        for item in IMAGE_URLS:
            if "image_url" in item:
                item["image_url"] = normalize_github_url(item["image_url"])
        print(f"Fetched {len(IMAGE_URLS)} images from {IMAGE_URLS_URL}")
    else:
        print(f"Failed to fetch image URLs from {IMAGE_URLS_URL}, status code: {response.status_code}")
except Exception as e:
    print(f"Error fetching image URLs from {IMAGE_URLS_URL}: {e}")
    # Fallback to default list if fetch fails
    IMAGE_URLS = [
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/digital-printing/1.jpeg",
        "topic": "The \"True Color\" Guarantee:\nExplain the science of color calibration. Most clients fear their brand \"Orange\" looking \"Brown\" on a billboard. Discuss how your digital printing technology ensures Pantone consistency across every medium, from business cards to 48-sheet outdoor displays."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/digital-printing/2.jpeg",
        "topic": "Mobile Real Estate: The ROI of Vehicle Wraps:Position branded vehicles as \"The Salesperson that Never Sleeps.\" Use data to show how many thousands of impressions a single branded truck makes daily on high-traffic routes like Mombasa Road or the Express Way."    
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/digital-printing/3.jpeg",
        "topic": "Material Science: Mesh vs. Solid Vinyl:\nEducate the client on durability. Discuss why Mesh banners are essential for windy high-rise locations (to prevent tearing) versus Solid PVC for maximum color \"pop\" at eye level. This builds your reputation as a technical expert, not just a printer."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/digital-printing/4.jpeg",
        "topic": "\"Phygital\" Advertising: Integrating QR & AR\nIn 2026, print isn't static. Discuss how to integrate Augmented Reality (AR) triggers or high-res QR codes into large format prints, allowing passersby to \"scan\" a billboard and land directly on the e-commerce site we discussed earlier."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/digital-printing/5.jpeg",
        "topic": "The Psychology of Large Format Design\nShare the \"3-Second Rule:\" Explain how to design for outdoor ads so that a driver can digest the message in three seconds. This adds value by showing you care about the effectiveness of their ad, not just the print quality."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/digital-printing/6.jpeg",
        "topic": "Sustainability: Eco-Friendly \"Green\" Printing\nWith the global shift toward ESG (Environmental, Social, and Governance), discuss your use of Latex or Water-based inks and recyclable substrates. Brands are increasingly choosing vendors who help them reduce their carbon footprint."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/digital-printing/7.jpeg",
        "topic": "Interior Branding: Turning Walls into Experiences\nMarket toward HR and Office Managers. Discuss how custom wall murals and floor graphics can transform a cold corporate office into a high-energy brand environment that boosts employee morale."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/digital-printing/8.jpeg",
        "topic": "Event Readiness: The 24-Hour Turnaround\nPromote agility. Focus on your ability to deliver high-quality event backdrops and \"Step & Repeat\" banners on short notice for corporate launches, solving the \"last-minute panic\" for event planners."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/digital-printing/9.jpeg",
        "topic": "Window Graphics: The \"One-Way Vision\" Magic\nShowcase the utility of perforated vinyl. Explain how retail shops can use their windows for massive branding without blocking natural light or the view from the inside."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/digital-printing/10.jpeg",
        "topic": "The Future of Digital Printing: How we're preparing for the next generation of printing technologies."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/digital-printing/11.jpeg",
        "topic": "A classic \"Educational\" topic. Explain why a low-res JPEG from WhatsApp will look \"pixelated\" on a billboard and why Vector files are the gold standard for large format. This saves you (and the client) from quality disputes."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/digital-printing/12.jpeg",
        "topic": "The Cost of \"Cheap\" Printing\nA \"tough love\" topic. Discuss the hidden costs of low-quality printing—re-printing fees, damaged brand reputation, and peeling vinyl. Position your services as a long-term investment in brand integrity."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/heat-press/1.jpeg",
        "topic": "The \"Walking Billboard\" Strategy:\nConnect your apparel branding to your outdoor advertising. Explain how a branded t-shirt or jacket acts as a mobile extension of a massive billboard campaign. If people see the billboard on the highway and then see your team wearing the brand in the supermarket, the \"frequency of touch\" doubles."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/heat-press/2.jpeg",
        "topic": "Safety First: Reflective & High-Vis Branding\nFor your construction and logistics clients, market reflective heat-press vinyl. Discuss the importance of branding safety gear (vests, jackets) that stays visible at night. It’s not just branding; it’s a safety requirement that looks professional."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/heat-press/3.jpeg",
        "topic": "The \"No-Minimums\" Advantage:\nUnlike screen printing (which requires expensive screens), heat press is perfect for small batches. Market this to SMEs or corporate departments that only need 5 or 10 high-quality pieces. \"Professional branding, even if you’re a team of three.\""
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/heat-press/4.jpeg",
        "topic": "Texture That Talks: Puff, Glitter, & Metallic\nDigital printing is flat, but heat press can be 3D. Discuss \"Puff\" prints, metallic foils, and \"Flock\" (velvet) textures. Explain how these premium finishes make a corporate polo shirt feel like high-end retail merchandise."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/heat-press/5.jpeg",
        "topic": "The \"Anti-Crack\" Science (Durability):\nAddress the common fear that \"the sticker will peel off.\" Educate your audience on the science of Time, Temperature, and Pressure. Explain how professional-grade heat pressing fuses the design into the fibers, ensuring it survives the \"Wash Test.\""
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/heat-press/6.jpeg",
        "topic": "Personalization at Scale: Names & Numbers\nThis is the \"Sports Team\" angle. Discuss your ability to take a corporate order and add individual employee names or department titles to each garment. It’s the ultimate way to build team morale and a sense of belonging."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/heat-press/7.jpeg",
        "topic": "Branding the Unconventional: Umbrellas & Bags\nSince you do outdoor advertising, market branded umbrellas and tote bags. Heat press is the king of difficult surfaces. Use this to show how a brand can stay visible even when it’s raining in Nairobi."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/heat-press/8.jpeg",
        "topic": "The \"Billboards for the Head\": Custom Caps\nCaps are one of the highest-value promotional items. Discuss the different placements for heat press on headwear—front, side, and even the brim. It’s a low-cost, high-visibility branding \"landmark\" for the face."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/heat-press/9.jpeg",
        "topic": "The \"Wash Test\" Challenge:\nCreate a fun, interactive post where you show a heat-pressed shirt going through multiple wash cycles. This builds trust by demonstrating durability and quality in a way that’s more engaging than just saying \"it won’t peel.\""
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/heat-press/10.jpeg",
        "topic": "From Digital Design to Fabric:Show the \"Behind the Scenes\" of the Print-and-Cut process. People love seeing the precision of a plotter cutting a complex logo and the satisfying \"peel\" after the heat press is lifted. It proves the \"custom\" nature of the work."
    },
    {
        "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/large-format-printing/1.jpeg",
        "topic": "The \"Landmark\" Strategy\nTeach clients how to turn a building or a fence into a landmark. Discuss the psychological power of Building Wraps—how a brand that occupies a massive physical space is automatically perceived as a \"market leader\" or \"too big to fail.\"\nThis is especially effective for clients in competitive industries who want to assert dominance."
    },

        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/large-format-printing/2.jpeg",
            "topic": "The Science of Viewing Distance\nEducate clients on \"DPI vs. Distance.\" Explain why a billboard on the Thika Road Superhighway doesn't need the same resolution as a pull-up banner at a gala. This positions you as an expert who saves them money on file processing while ensuring the print looks crisp from 50 meters away."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/large-format-printing/3.jpeg",
            "topic": "UV-Resistance: Winning the War Against the Sun\nAddress the \"Fading\" pain point directly. Explain the technology behind UV-cured inks and specialized laminates. Show them why a \"cheap\" print that fades in three months is actually 3x more expensive than a premium print that stays vibrant for two years."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/large-format-printing/4.jpeg",
            "topic": "Mesh Banners: Engineering for the Wind\nA great technical topic. Explain why Mesh is the only choice for high-rise scaffolding or bridge banners. Discuss how the \"perforated\" nature allows wind to pass through, preventing the \"sail effect\" that can tear down expensive frames and cause safety hazards."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/large-format-printing/5.jpeg",
            "topic": "The \"Backlit\" Glow: Owning the Night\nDiscuss the difference between standard Frontlit and Backlit Flex. Focus on how illuminated large format ads ensure the brand doesn't \"disappear\" at 6:30 PM, effectively giving the client 24-hour visibility for the price of one print."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/large-format-printing/6.jpeg",
            "topic": "The \"Custom\" Advantage: Why You Can't Buy It Off the Shelf\nExplain how a custom print is more valuable than a generic one. Show how a client's unique logo, colors, and message are preserved in a way that off-the-shelf prints simply cannot match."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/large-format-printing/7.jpeg",
            "topic": "Vector vs. Raster: The \"Giant Pixel\" Horror Story\nUse humor to educate. Show a \"pixelated\" blurry face next to a crisp vector-printed face. Explain why high-quality source files are the \"DNA\" of a successful large format project. This reduces your \"bad artwork\" headaches and positions you as a quality-first shop."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/large-format-printing/8.jpeg",
            "topic": "Interior \"Experience\" Branding\nMarket to corporate architects and HR. Discuss Wall Murals and custom wallpapers. Show how large format isn't just for outdoors; it’s for turning a cold, white office lobby into a brand-immersive \"experience\" that impresses visitors and boosts staff morale."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/screen-print/1.jpeg",
            "topic": "The \"Power of the Bulk\" Economy\nEducate your clients on the \"Sweet Spot.\" Explain why screen printing is the undisputed king of large orders. Use a simple chart to show how the price per shirt drops significantly as the quantity increases—making it the most budget-friendly option for massive corporate activations or political campaigns."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/screen-print/2.jpeg",
            "topic": "Pantone Perfection: The \"Spot Color\" Advantage\nUnlike digital printers that \"guess\" colors using CMYK, screen printing uses actual mixed ink. Discuss your ability to provide 100% accurate Pantone matching. This is a major selling point for institutional brands (like LGT) that are obsessive about their specific corporate colors."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/screen-print/3.jpeg",
            "topic": "The \"Custom\" Advantage: Why You Can't Buy It Off the Shelf\nExplain how a custom print is more valuable than a generic one. Show how a client's unique logo, colors, and message are preserved in a way that off-the-shelf prints simply cannot match."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/screen-print/4.jpeg",
            "topic": "The \"Artisan\" Touch: Why Handcrafted Matters\nPosition screen printing as an art form. Discuss the craftsmanship involved in setting up screens, mixing inks, and ensuring each print is done with care. This appeals to clients who value quality and uniqueness over mass production."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/screen-print/5.jpeg",
            "topic": "The \"Legacy Shirt\" (Indestructible Durability)\nMarket the longevity of the ink. Explain how plastisol or water-based inks bond with the fabric. \"The shirt might wear out in 10 years, but the print will still be there.\" This appeals to clients who want their \"Walking Billboards\" to last through hundreds of washes."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/screen-print/6.jpeg",
            "topic": "Texture & Specialty Inks: Beyond the Flat Look\nGo where digital can't. Discuss High-Density (3D) printing, Glow-in-the-Dark, and Metallic Gold/Silver. These specialty finishes make a brand feel premium and \"bespoke\" in a way that standard digital prints cannot replicate."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/screen-print/7.jpeg",
            "topic": "Water-Based vs. Plastisol: Choosing Your Feel\nEducate the \"fashion-forward\" crowd. Explain the difference between the heavy, durable feel of Plastisol (best for workwear) and the \"Soft-Hand\" feel of water-based inks (best for high-end retail and soft t-shirts). This positions you as a consultant, not just a vendor."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/screen-print/8.jpeg",
            "topic": "The Art of the Squeegee (Process Appreciation)\nScreen printing is incredibly \"satisfying\" to watch. Use your DimensionOutlook handle to share high-definition videos of ink being pushed through the mesh. The \"Behind the Scenes\" of the darkroom and the burning of screens proves the craftsmanship involved in your work."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/screen-print/9.jpeg",
            "topic": "The \"Printed on Demand\" Advantage\nExplain how screen printing allows for small batch runs without the high setup costs of traditional offset printing. This is especially valuable for startups and small businesses that don't want to commit to large quantities."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/screen-print/10.jpeg",
            "topic": "Branding \"The Tough Stuff\" (Nylon & Canvas)\nLarge format printing often involves umbrellas, raincoats, and heavy-duty canvas bags. Market screen printing as the solution for these \"difficult\" materials where other printing methods might fail to stick or peel off."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/screen-print/11.jpeg",
            "topic": "Merchandise as a Revenue Stream\nTarget influencers, schools, and content creators. Show them how they can turn their brand into a profit center by screen-printing hoodies and tees in bulk. Provide a \"Profit Margin\" breakdown to show them how much they can make per item."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/screen-print/12.jpeg",
            "topic": "Consistency is King\nIn outdoor advertising, you might need 1,000 branded caps for a street team. Discuss how screen printing ensures that the 1st item and the 1,000th item look identical. No \"digital drift\" or color shifts mid-run."
        },
        {
            "image_url": "https://github.com/Cheche-ship-it/dimension-marketing-snapshots/blob/main/signage/1.jpeg",
            "topic": "The Landmark Effect: Turning Your Location into a Silent 24/7 Salesman."
        }
    ]
    # Normalize fallback URLs to use raw content URLs
    for item in IMAGE_URLS:
        if "image_url" in item:
            item["image_url"] = normalize_github_url(item["image_url"])

# --- Configuration ---
# Gemini API Key: Get this from Google AI Studio or Google Cloud Console.
# It's crucial to keep this secure and not hardcode it in public repositories.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Social Media API Credentials (PLACEHOLDERS - DO NOT USE IN PRODUCTION AS IS)
# For Facebook:
# You need a Facebook Page ID and a Long-Lived Page Access Token.
# Obtaining this token involves creating a Facebook Developer App, getting user
# authentication with specific permissions (e.g., 'pages_manage_posts'),
# and then exchanging a short-lived user token for a long-lived page token.
# This process is complex and typically handled by a secure backend server.
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "YOUR_FACEBOOK_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN", "YOUR_FACEBOOK_ACCESS_TOKEN")

# For Twitter (X):
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "YOUR_TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "YOUR_TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "YOUR_TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "YOUR_TWITTER_ACCESS_TOKEN_SECRET")

# Predefined topics for social media post generation
TOPICS = topics = [
    "The 'Local First' Advantage: Why Kenyan businesses need a brand identity that resonates with local culture.",
    "Logo Evolution: When is it time for a brand refresh vs. a total rebrand?",
    "Color Psychology in Kenya: Choosing brand colors that stand out in Nairobi’s urban landscape.",
    "Consistency is King: How unified branding across stationery and billboards builds trust.",
    "Small Business, Big Identity: Branding tips for Kenyan SMEs to look like multinationals.",
    "Brand Storytelling: How to turn your company’s 'Why' into a visual identity.",
    "The Cost of 'Cheap' Branding: Why investing in professional design saves money in the long run.",
    "Modernizing Traditional Brands: How to update a classic Kenyan brand for the digital market.",
    "Sensory Branding: Using texture in print and physical presence to define your brand.",
    "Internal Branding: Using office wall graphics and branded apparel to boost employee morale.",
    "Billboards in the Digital Age: Why physical outdoor ads drive high trust in 2026.",
    "The 3-Second Rule: Designing billboards that commuters can read in Nairobi traffic.",
    "Strategic Placement: The best high-traffic spots in Kenya for specific industries.",
    "The 'Mobile Billboard' Effect: Why vehicle wraps are the most cost-effective outdoor ads.",
    "Illuminated Signage: How 24-hour backlit banners keep your brand visible at night.",
    "Seasonal Outdoor Campaigns: Leveraging Kenyan holidays for high-impact advertisements.",
    "Street Furniture Ads: Using bus stops and charging kiosks to capture pedestrian attention.",
    "Digital vs. Static Billboards: Which is right for your budget and campaign goals?",
    "Guerilla Marketing in Nairobi: Innovative ways to use outdoor space that stop people in their tracks.",
    "Measuring OOH Success: How to track ROI on a billboard using QR codes.",
    "Beyond Banners: Creative uses for large format printing like murals and floor graphics.",
    "The Tech Behind the Print: How UV-resistant inks survive the harsh Kenyan sun.",
    "Event Dominance: Must-have print assets for Kenyan trade shows and expos.",
    "Retail Transformation: Using window graphics to turn window shoppers into buyers.",
    "Mesh Vinyl 101: Why mesh is the secret weapon for windy outdoor environments.",
    "Photo-Ready Backdrops: Designing 'Instagrammable' banners for Kenyan corporate launches.",
    "The Power of Texture: Using canvas prints for high-end office decor.",
    "Sustainability in Printing: Moving toward eco-friendly materials and recyclable vinyl.",
    "Speed vs. Quality: Why 'Same-Day Turnaround' is a game-changer for event planners.",
    "Durability Testing: A guide to choosing the right PVC thickness for long-term campaigns."
]


# Initialize Gemini API
# This checks if the API key is available before configuring the model.
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash') # Using the specified Gemini model
else:
    print("Warning: GEMINI_API_KEY not found in .env. AI content generation will not work.")
    model = None
    


def download_image(url, filename):
    """
    Downloads an image from a URL and saves it locally.
    Returns the filename if successful, else None.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename
        else:
            print(f"Failed to download image: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def post_image_to_facebook_page(image_path, message):
    url = f"https://graph.facebook.com/v24.0/{FACEBOOK_PAGE_ID}/photos"
    payload = {
        "caption": message,
        "access_token": FACEBOOK_ACCESS_TOKEN
    }
    files = {
        "source": open(image_path, "rb")
    }
    response = requests.post(url, data=payload, files=files)
    print("Facebook image response:", response.text)
    return response.status_code == 200

def post_image_to_twitter(image_path, message):
    from requests_oauthlib import OAuth1
    import mimetypes
    # 1. Upload image
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "image/png"  # Default
    with open(image_path, "rb") as image_file:
        files = [
            ('media', (os.path.basename(image_path), image_file, mime_type))
        ]
        payload = {
            'media_type': mime_type,
            'media_category': 'tweet_image'
        }
        response = requests.post(
            "https://api.x.com/2/media/upload",
            auth=OAuth1(
                TWITTER_API_KEY,
                TWITTER_API_SECRET,
                TWITTER_ACCESS_TOKEN,
                TWITTER_ACCESS_TOKEN_SECRET
            ),
            data=payload,
            files=files
        )
    # Twitter returns both 'id' and 'media_key'. For posting, use 'id' (numeric string)
    media_id = response.json().get("data", {}).get("id")
    print("Twitter image upload response:", response.text)
    # print("Media ID:", media_id)
    # Check if media_id is present
    # If not, log the error and return False
    # This is important to ensure we don't proceed with an invalid media ID
    # If media_id is None or empty, it means the upload failed
    # and we should not attempt to post the tweet.
    # This prevents errors when trying to post a tweet with an invalid media ID.
    # If media_id is None or empty, it means the upload failed
    # and we should not attempt to post the tweet.
    # This prevents errors when trying to post a tweet with an invalid media ID.
    
    print("Media ID:", media_id)
    if not media_id:
        print("Twitter image upload failed:", response.text)
        return False
  
    # Dynamically generate OAuth1 header using requests_oauthlib
    from requests_oauthlib import OAuth1
    print("message length", len(message))
    url = "https://api.x.com/2/tweets"
    payload = {
        "text": message,
        "media": {
            "media_ids": [str(media_id)]
        }
    }
    try:
        oauth = OAuth1Session(
            TWITTER_API_KEY,
            client_secret=TWITTER_API_SECRET,
            resource_owner_key=TWITTER_ACCESS_TOKEN,
            resource_owner_secret=TWITTER_ACCESS_TOKEN_SECRET,
        )
        response = oauth.post(url, json=payload, timeout=10)
        print("Status code:", response.status_code)
        print("Response:", response.text)
        if response.status_code == 201 or response.status_code == 200:
            try:
                response_json = response.json()
                tweet_id = response_json.get("data", {}).get("id")
                if tweet_id:
                    print(f"Successfully posted to Twitter! Tweet ID: {tweet_id}")
                else:
                    print(f"Successfully posted to Twitter! Response: {response_json}")
            except Exception:
                print(f"Successfully posted to Twitter! Response: {response.text}")
            return True
        else:
            print(f"Twitter post failed. Status: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error posting to Twitter: {e}")
        return False



def get_kenya_trends():
    url = "https://trends24.in/kenya/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    } # Mimic a web browser

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')

        # --- IMPORTANT: You need to inspect the trends24.in/kenya/ HTML to find the correct selectors ---
        # Look for the HTML structure that contains the trending topics.
        # This is a placeholder example based on common patterns:
        trending_list_container = soup.find('div', class_='list-container') # Or whatever the actual class/id is
        
        if trending_list_container:
            trends = trending_list_container.find_all('li') # Assuming each trend is an <li> item
            
            kenya_trends = []
            for trend_item in trends:
                hashtag_element = trend_item.find('a') # Assuming the hashtag is in an <a> tag

                if hashtag_element:
                    hashtag = hashtag_element.get_text(strip=True)
                    kenya_trends.append(hashtag)
            return kenya_trends[:6]  # Return top 4 trends
        else:
            print("Could not find the trending list container on the page.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return []
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
        return []

def append_hashtags_to_message(message, hashtags):
    """
    Appends a list of hashtags to the message, separated by spaces.
    Ensures each hashtag starts with #. If the final message is longer than 278 characters,
    removes hashtags without # one by one until the message is <= 278 chars.
    """
    hashtags_list = []
    if hashtags:
        if isinstance(hashtags, list):
            hashtags_list = [(h if h.strip().startswith('#') else f'#{h.strip()}') for h in hashtags if h.strip()]
        else:
            h = hashtags.strip()
            hashtags_list = [h if h.startswith('#') else f'#{h}']
    final_message = message + " " + " ".join(hashtags_list).strip()
    # If too long, remove hashtags without # one by one
    if len(final_message) > 278:
        # Find indices of hashtags that originally did NOT have #
        original_hashtags = hashtags if isinstance(hashtags, list) else [hashtags]
        indices_to_remove = [i for i, h in enumerate(original_hashtags) if not h.strip().startswith('#')]
        hashtags_copy = hashtags_list.copy()
        for idx in indices_to_remove:
            if idx < len(hashtags_copy):
                hashtags_copy.pop(idx)
                temp_message = message + " " + " ".join(hashtags_copy).strip()
                if len(temp_message) <= 278:
                    final_message = temp_message
                    break
        # If still too long, truncate hashtags until fits
        while len(final_message) > 278 and hashtags_copy:
            hashtags_copy.pop()
            final_message = message + " " + " ".join(hashtags_copy).strip()
    # Ensure final message is not longer than 278 characters
    if len(final_message) > 278:
        final_message = final_message[:278]
    print("Final message length:", len(final_message))
    return final_message

def generate_twitter_ai_content(topic):
    """
    Generates engaging social media post content for Twitter using the Gemini AI model.
    The prompt is designed to create concise, engaging, and hashtag-rich tweets (max 180 characters).
    Returns None if generation fails.
    """
    if not model:
        print(f"AI model not configured. Cannot generate Twitter content for topic '{topic}'.")
        return None

    prompt = f"""
        You are an experienced social media marketing proffessional for Dimensio Outlook Company, a leading Branding and  Outdoor advertisement company.

        Your goal is to generate ONE concise, engaging, and lead-generating social media post for Facebook (max 215 characters).

        The post should:

        - Be interesting and encourage potential customers to inquire about your products.

        - Use relevant emojis to make it appealing.

        - The content should be engaging and lead to inquiries.

        - Content length does not matter though it should be concise and clear.

        - Format the content well with proper spacing and line breaks.

        - Only output a single message/no multiple options.

        - include  trending hashtags.

        - add call to action to visit website https://dimensionoutlook.com and chat on whatsapp to number +254722117264.

        Topic: "{topic}"
                """
    try:
        response = model.generate_content(prompt)
        print("Twitter API Response:", response)
        if response.candidates and response.candidates[0].content.parts:
            single_tweet = response.candidates[0].content.parts[0].text.strip()
            if not single_tweet:
                print(f"Error: Generated Twitter content is empty for topic '{topic}'.")
                return None
            return single_tweet
        else:
            print(f"Error: Gemini API response structure unexpected or empty content for topic '{topic}'.")
            return None
    except Exception as e:
        print(f"Error generating Twitter content for topic '{topic}': {e}")
        return None



# --- Helper Functions ---

def generate_facebook_ai_content(topic):
    """
    Generates engaging social media post content using the Gemini AI model.
    The prompt is designed to create lead-generating and engaging messages.
    Returns None if generation fails.
    """
    if not model:
        print(f"AI model not configured. Cannot generate Facebook content for topic '{topic}'.")
        return None

    prompt = f"""
        You are an experienced social media marketing proffessional for Dimensio Outlook Company, a leading Branding and  Outdoor advertisement company.

        Your goal is to generate ONE concise, engaging, and lead-generating social media post for Facebook (max 700 characters).

        The post should:

        - Be interesting and encourage potential customers to inquire about your products.

        - Use relevant emojis to make it appealing.

        - The content should be engaging and lead to inquiries.

        - Content length does not matter though it should be concise and clear.

        - Format the content well with proper spacing and line breaks.

        - Only output a single message/no multiple options.

        - include  trending hashtags.

        - add call to action to visit website https://dimensionoutlook.com and chat on whatsapp to number +254722117264.


Topic: "{topic}"
"""
    try:
        # Make the API call to Gemini
        print("Generating Facebook AI content with prompt:..............................................", prompt)  # Debugging line to see the prompt
        response = model.generate_content(prompt)
        print("API Response:,.,.,.,.,.,,.,,.,.,.,.,.,.,.,.,.,.,.,.,..", response)  # Debugging line to see the full response structure
        # Extract the text from the API response
        if response.candidates and response.candidates[0].content.parts:
            single_post = response.candidates[0].content.parts[0].text.strip()
            # Check if content is empty
            if not single_post:
                print(f"Error: Generated Facebook content is empty for topic '{topic}'.")
                return None
            return single_post
        else:
            print(f"Error: Gemini API response structure unexpected or empty content for topic '{topic}'.")
            return None
    except Exception as e:
        # Catch any exceptions during the API call or response parsing
        print(f"Error generating Facebook content for topic '{topic}': {e}")
        return None

def post_to_facebook(message):
    """
    Posts a message to a Facebook Page using the Graph API.
    
    Requirements:
    - The FACEBOOK_ACCESS_TOKEN must be a Page Access Token (not a User Access Token).
    - The token must have both 'pages_read_engagement' and 'pages_manage_posts' permissions.
    - The user who generated the token must be an admin of the page.
    
    How to obtain the correct token:
    1. Go to Facebook Developer Portal > My Apps > [Your App].
    2. Request 'pages_read_engagement' and 'pages_manage_posts' permissions.
    3. Use Graph API Explorer to generate a User Access Token with these permissions.
    4. Exchange for a long-lived token (optional).
    5. Use /me/accounts to get the Page Access Token for your page.
    6. Update your .env with this token.
    """
    print(f"Attempting to post to Facebook: {message[:70]}...")
    # Validate credentials and token format
    if not FACEBOOK_PAGE_ID or not FACEBOOK_ACCESS_TOKEN or FACEBOOK_ACCESS_TOKEN == "YOUR_FACEBOOK_ACCESS_TOKEN" or FACEBOOK_PAGE_ID == "YOUR_FACEBOOK_PAGE_ID":
        print("Facebook API credentials not properly configured. Skipping Facebook post.")
        print("Make sure you have a valid Page Access Token with 'pages_read_engagement' and 'pages_manage_posts' permissions.")
        return False
 
    url = f"https://graph.facebook.com/{FACEBOOK_PAGE_ID}/feed"
    payload = {
        "message": message,
        "access_token": FACEBOOK_ACCESS_TOKEN
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code == 200:
            response_json = response.json()
            post_id = response_json.get("id")
            if post_id:
                print(f"Successfully posted to Facebook! Post ID: {post_id}")
                return True
            else:
                print(f"Facebook API response did not contain post ID: {response_json}")
                return False
        elif response.status_code == 400 and "(#200)" in response.text:
            print("Facebook API error (#200): Insufficient permissions or wrong token type.")
            print("Make sure your token is a Page Access Token with the required permissions and you are an admin of the page.")
            print("See the function docstring for step-by-step instructions.")
            return False
        else:
            print(f"Facebook post failed. Status: {response.status_code}, Response: {response.text}")
            return False
    except requests.exceptions.Timeout:
        print("Facebook post request timed out.")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error posting to Facebook: {e}")
        return False

def post_to_twitter(message):
    """
    Posts a message to Twitter using the Twitter API v2 and OAuth1Session.
    Handles credit depletion gracefully.
    """
    print(f"Attempting to post to Twitter (X): {message}")
    print("posting to twitter a message with length", len(message))
    url = "https://api.twitter.com/2/tweets"
    payload = {"text": message}
    try:
        oauth = OAuth1Session(
            TWITTER_API_KEY,
            client_secret=TWITTER_API_SECRET,
            resource_owner_key=TWITTER_ACCESS_TOKEN,
            resource_owner_secret=TWITTER_ACCESS_TOKEN_SECRET,
        )
        response = oauth.post(url, json=payload, timeout=10)
        print("Status code:", response.status_code)
        print("Response:", response.text)
        if response.status_code == 201 or response.status_code == 200:
            try:
                response_json = response.json()
                tweet_id = response_json.get("data", {}).get("id")
                if tweet_id:
                    print(f"Successfully posted to Twitter! Tweet ID: {tweet_id}")
                else:
                    print(f"Successfully posted to Twitter! Response: {response_json}")
            except Exception:
                print(f"Successfully posted to Twitter! Response: {response.text}")
            return True
        elif response.status_code == 402:
            # Handle credit depletion error
            try:
                error_json = response.json()
                error_title = error_json.get("title", "Unknown error")
                error_detail = error_json.get("detail", "No details available")
                print(f"⚠️  Twitter API Credits Depleted: {error_title}")
                print(f"Details: {error_detail}")
                print("Please add credits to your Twitter API account to resume posting.")
                print("Visit: https://developer.twitter.com/en/portal/dashboard")
            except:
                print(f"Twitter API error 402: Credits depleted. Please add credits to your account.")
            return False
        elif response.status_code == 401 or response.status_code == 403:
            # Handle authentication/authorization errors
            print(f"Twitter API Authentication Error (Status {response.status_code})")
            print("Please verify your API credentials are correct and have not expired.")
            print("Response:", response.text)
            return False
        else:
            print(f"Twitter post failed. Status: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error posting to Twitter: {e}")
        return False

def send_social_media_post():
    """
    Main function to orchestrate the social media post generation and sending process.
    This function is called by the scheduler.
    """
    print(f"\n--- Starting new social media post cycle at {time.ctime()} ---")
    
    # 1. Randomly select a topic
    selected_topic = random.choice(TOPICS)
    print(f"Selected topic: {selected_topic}")

    # 2. Fetch trending hashtags in Kenya
    trending_hashtags = get_kenya_trends()
    print(f"Trending hashtags in Kenya: {trending_hashtags}")

    # 3. Randomly decide to post with image or not 
    # If IMAGE_URLS is empty, use_image will be False
    # ALSO choose randomly between true and false
    # to decide whether to use an image or not
    use_image = bool(IMAGE_URLS) and random.choice([True, False])
    # use_image = True
    image_path = None
    image_url = None
    image_topic = None
    if use_image:
        image_dict = random.choice(IMAGE_URLS)
        image_url = image_dict["image_url"]
        image_topic = image_dict["topic"]
        print(f"Selected image URL: {image_url}")
        print(f"Image topic: {image_topic}")
        image_path = download_image(image_url, "temp_image.jpg")
    if use_image and image_path:
        # --- Image Validation ---
        valid_image = True
        # 1. Check file size (must be < 4MB)
        try:
            file_size = os.path.getsize(image_path)
            if file_size > 4 * 1024 * 1024:
                print(f"Image too large for Facebook upload: {file_size/1024/1024:.2f} MB. Skipping upload.")
                valid_image = False
        except Exception as e:
            print(f"Could not check image file size: {e}")
            valid_image = False
        # 2. Check file extension/type
        allowed_exts = [".jpg", ".jpeg", ".png", ".gif", ".tiff", ".heif", ".webp"]
        ext = os.path.splitext(image_path)[1].lower()
        if ext not in allowed_exts:
            print(f"Image file type {ext} not allowed for Facebook upload. Skipping upload.")
            valid_image = False
        # 3. Try to verify image with Pillow if installed
        try:
            from PIL import Image
            with Image.open(image_path) as img:
                img.verify()
            print("Image verified with Pillow.")
        except ImportError:
            print("Pillow not installed, skipping image verification.")
        except Exception as e:
            print(f"Image verification failed: {e}. Skipping upload.")
            valid_image = False
        if not valid_image:
            print("Image did not pass validation. Facebook upload skipped.")
        else:
            # Generate AI marketing message for image using the image's topic
            fb_post_content = generate_facebook_ai_content(image_topic)
            if fb_post_content is None:
                print("ERROR: Failed to generate Facebook content for image. Aborting post cycle.")
                return
            x_post_content = generate_twitter_ai_content(image_topic)
            if x_post_content is None:
                print("ERROR: Failed to generate Twitter content for image. Aborting post cycle.")
                return
            x_post_content_with_hashtags = append_hashtags_to_message(x_post_content, trending_hashtags)
            # Facebook
            facebook_success = post_image_to_facebook_page(image_path, fb_post_content)
            print(f"Facebook image post success: {facebook_success}")
            print("\nPosting to Twitter with image...")
            print(f"Twitter post content: {x_post_content_with_hashtags}")
            # Twitter
            twitter_success = post_image_to_twitter(image_path, x_post_content_with_hashtags)
            print(f"Twitter image post success: {twitter_success}")
        # Clean up temp image
        try:
            os.remove(image_path)
        except Exception:
            pass
    else:
        # Generate AI content for Facebook (no image)
        post_content = generate_facebook_ai_content(selected_topic)
        if post_content is None:
            print("ERROR: Failed to generate Facebook content. Aborting post cycle.")
            return
        facebook_success = post_to_facebook(post_content)
        print(f"Facebook post success: {facebook_success}")
        # Generate AI content for Twitter and append hashtags
        twitter_post_content = generate_twitter_ai_content(selected_topic)
        if twitter_post_content is None:
            print("ERROR: Failed to generate Twitter content. Aborting post cycle.")
            return
        twitter_post_content_with_hashtags = append_hashtags_to_message(twitter_post_content, trending_hashtags)
        print(f"Twitter post content: {twitter_post_content_with_hashtags}")
        twitter_success = post_to_twitter(twitter_post_content_with_hashtags)
        print(f"Twitter post success: {twitter_success}")
    print("--- End of post cycle ---")

# --- Main Execution Block ---
if __name__ == "__main__":
    send_social_media_post()