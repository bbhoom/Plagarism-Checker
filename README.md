# Plagiarism Detector
This project is a plagiarism detection tool built with a React frontend and Django backend. It checks for content similarity by analyzing text input, extracting key phrases, performing web searches for potential matches, and comparing similarities with retrieved content. The similarity score is displayed on a gauge chart, along with the link to the most similar content found.

# Features
Random Phrase Selection: Extracts random phrases from the input text to use for plagiarism checks.
Web Search and Scraping: Searches the web for potential matching content using Google Custom Search API and scrapes the content from results.
Similarity Calculation: Uses TF-IDF and cosine similarity to calculate and display how similar the input text is to the top-matching content found online.
Gauge Chart: Shows the similarity score visually with a gauge chart.
Dynamic Scraping with Selenium: Allows scraping of dynamically generated pages by using Selenium.
# Tech Stack
Frontend: React, react-gauge-chart for visualization
Backend: Django, Django REST framework, BeautifulSoup, Selenium, Scikit-Learn (for TF-IDF and cosine similarity calculations)
API: Google Custom Search API

# Project Structure
Frontend: React app to handle user input, send requests to the backend, and display results using a gauge chart.
Backend: Django app with a single API endpoint that:
Selects random phrases from the input text.
Performs a Google search and scrapes top results.
Calculates similarity between the input text and the scraped content using cosine similarity.

# Future Improvements
Add more robust error handling and logging.
Increase the number of sources or use additional APIs for more reliable plagiarism checks.
Improve scraping capabilities to handle a wider range of website structures and avoid pop-ups effectively.

# Images
![image](https://github.com/user-attachments/assets/e73deb19-4f3d-4156-8a07-576d163c098e)
![image](https://github.com/user-attachments/assets/e4d18a82-0f20-472d-9aee-311c22d03b3e)
![image](https://github.com/user-attachments/assets/64521e51-58c7-4ecb-b31c-8c71445984fe)
