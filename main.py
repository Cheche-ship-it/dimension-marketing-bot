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

# --- Image URLs Fetch Logic ---
# If IMAGE_URLS_URL is set in the environment, fetch the JSON from that URL.
# Otherwise, use the default list.
IMAGE_URLS_URL = os.getenv("IMAGE_URLS_URL", "https://raw.githubusercontent.com/Nduhiu17/marketing-snapshots/refs/heads/main/photos.json")
IMAGE_URLS = []
# try:
#     response = requests.get(IMAGE_URLS_URL, timeout=10)
#     if response.status_code == 200:
#         IMAGE_URLS = response.json()
#         print(f"Fetched {len(IMAGE_URLS)} images from {IMAGE_URLS_URL}")
#     else:
#         print(f"Failed to fetch image URLs from {IMAGE_URLS_URL}, status code: {response.status_code}")
# except Exception as e:
#     print(f"Error fetching image URLs from {IMAGE_URLS_URL}: {e}")
#     # Fallback to default list if fetch fails
#     # IMAGE_URLS = [
#     #     {
#     #         "image_url": "https://ecogreencontractors.solutions/static/media/about1.1c4f9ffe16b2ddba4075.jpg",
#     #         "topic": "Outside garden with flowers and walk ways"
#     #     },
#     #     # Add more image dicts as needed
#     # ]

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