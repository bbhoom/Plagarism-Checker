import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from bs4 import BeautifulSoup
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Your Google API key and CSE ID
GOOGLE_API_KEY = 'AIzaSyAatmdgQYnNARCgB8K6VFN6px_JaJ0vnOY'
SEARCH_ENGINE_ID = '739ac959c426c4f5f'


@csrf_exempt
def hello_world(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '')  # Submitted text

        # Split text into phrases
        phrases = text.split('. ')
        random_phrases = random.sample(phrases, min(
            len(phrases), 3))  # Select 3 random phrases

        results = []
        max_similarity_scores = []
        for phrase in random_phrases:
            search_results = google_search(phrase)
            top_results = search_results[:5]  # Get the top 5 results

            phrase_results = []
            sim = 0  # Track the maximum similarity score for this phrase

            for result in top_results:
                page_content = scrape_dynamic_page(result['link'])
                if page_content:
                    # Calculate similarity score between submitted text and the scraped page content
                    similarity_score = compare_similarity(text, page_content)

                    # Check if the current similarity score is greater than the current max (sim)
                    if similarity_score > sim:
                        sim = similarity_score

                    phrase_results.append({
                        'title': result['title'],
                        'link': result['link'],
                        'snippet': result['snippet'],
                        # Include the similarity score
                        'similarity_score': similarity_score
                    })

            # Append the max similarity score for this phrase
            max_similarity_scores.append(sim)

            # Store the max similarity score for this phrase in the result
            results.append({
                'phrase': phrase,
                'max_similarity_score': sim
            })

        # Initialize variables to track the link with the most plagiarism
        top_link = None
        max_similarity_score = 0

        # Find the maximum similarity score and the corresponding link
        for result in top_results:
            page_content = scrape_dynamic_page(result['link'])
            if page_content:
                similarity_score = compare_similarity(text, page_content)

                # Check if similarity_score has been initialized before comparing
                if similarity_score > max_similarity_score:
                    max_similarity_score = similarity_score
                    top_link = result['link']  # Store the top plagiarized link

        # Return the results and the maximum similarity score
        return JsonResponse({
            'max_similarity_score': max_similarity_score,
            'top_link': top_link
        })

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def google_search(query):
    """Perform a Google Custom Search for the given query."""
    url = f'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': GOOGLE_API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
    }
    response = requests.get(url, params=params)
    search_results = []

    if response.status_code == 200:
        data = response.json()
        for item in data.get('items', []):
            search_results.append({
                'title': item.get('title'),
                'link': item.get('link'),
                'snippet': item.get('snippet')
            })

    return search_results


def scrape_dynamic_page(url):
    """Scrape content from a dynamically rendered page using Selenium."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-fullscreen-for-tab")
    chrome_options.add_argument("--disable-features=Fullscreen")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")
    prefs = {"profile.default_content_setting_values.notifications": 2,
             "profile.default_content_setting_values.popups": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(url)
        driver.execute_script("""
            document.documentElement.requestFullscreen = function() {};
            document.body.requestFullscreen = function() {};
        """)
        driver.implicitly_wait(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

    main_content = soup.find('main') or soup.find(
        'article') or soup.find('div', {'class': 'content'})
    if not main_content:
        print(f"Could not find main content for {url}")
        return None

    for tag in main_content(['header', 'footer', 'nav', 'aside', 'script', 'style']):
        tag.decompose()

    paragraphs = [p.get_text() for p in main_content.find_all('p')]
    return ' '.join(paragraphs) if paragraphs else None


def compare_similarity(submitted_text, scraped_content):
    """Compare the similarity between the submitted text and scraped content using cosine similarity."""
    try:
        if not submitted_text or not scraped_content:
            print("One of the texts is empty. Cannot compute similarity.")
            return 0.0

        submitted_text = clean_text(str(submitted_text))
        scraped_content = clean_text(str(scraped_content))

        documents = [submitted_text, scraped_content]

        vectorizer = TfidfVectorizer().fit_transform(documents)
        vectors = vectorizer.toarray()

        cosine_sim = cosine_similarity(vectors)[0][1]
        print(f"Similarity score: {cosine_sim * 100:.2f}%")
        return round(cosine_sim * 100, 2)

    except Exception as e:
        print(f"Error comparing similarity: {e}")
        return 0.0


def clean_text(text):
    """Clean the text by removing unwanted characters and lowercasing."""
    # Perform any text cleaning needed for comparison
    return text.strip().lower()
