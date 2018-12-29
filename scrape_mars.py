import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time

def scrape():
    # Create url variable for later use
    url = 'https://mars.nasa.gov/news/'

    # Get response from url
    response = requests.get(url)

    # Create Beautiful Soup object
    soup = bs(response.text, 'html.parser')

    # Retrieve all of the titles on the web page
    titles = soup.find_all('div', class_="content_title")

    # Write first title to news_title variable
    news_title = titles[0].text.strip()
    
    # Find all paragraphs on web page
    paragraphs = soup.find_all('div', class_="rollover_description_inner")

    # Find all paragraphs on web page
    paragraphs = soup.find_all('div', class_="rollover_description_inner")

    # Add first paragraph to news_p variable
    news_p = paragraphs[0].text.strip()

    # Create executable path for future use
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}

    # Open browser using executable path and chrome browser display everything thats going on
    browser = Browser('chrome', **executable_path, headless=True)

    # Create url variable for the browser to visit
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Visit url
    browser.visit(url2)

    # Click link that says full image
    browser.click_link_by_partial_text('FULL IMAGE')

    # Sleep for two seconds to allow for page to load
    time.sleep(2)

    # Click link that says more info
    browser.click_link_by_partial_text('more info')

    # Click link to full image alone
    browser.click_link_by_partial_href('//photojournal.jpl.nasa.gov/jpeg/')

    # Save url of full image to variable
    featured_image_url = browser.url

    # Create url variable for future use
    url3 = 'https://twitter.com/marswxreport?lang=en'

    # Get response from url
    response = requests.get(url3)

    # Create Beautiful Soup object
    soup = bs(response.text, 'html.parser')

    # Save first tweet to variable
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()

    # Create url variable for future use
    url4 = 'https://space-facts.com/mars/'

    # Read all tables on page
    tables = pd.read_html(url4)

    # Convert to pandas dataframe
    df = tables[0]

    # Rename columns of dataframe
    df.columns = ['Description', 'Value']

    # Set index to Description column
    df = df.set_index('Description')

    # Create variable with html table
    html_table = df.to_html()

    # Create url variable for the browser to visit
    url5 = 'http://web.archive.org/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Visit url
    browser.visit(url5)

    # Create variable for later action containing html text
    html = browser.html

    # Create beautiful soup object
    soup = bs(html, 'html.parser')

    # Create list for future use
    hemisphere_image_urls = []

    # Find all titles with class H3
    hemispheres = soup.find_all('h3')

    # Append all titles and urls to dictionary
    for hemi in hemispheres:
        browser.click_link_by_partial_text(hemi.text)
        
        # Click link with Sample as text
        browser.click_link_by_text('Sample')
        
        # Append image_url with browser window url
        hemisphere_image_urls.append({'title': hemi.text, 'image_url': browser.windows[1].url})
        
        # Close opened tab
        browser.windows[1].close()
        
        # Go back to the previous page
        browser.back()

    # Close open instance of browser
    browser.quit()

    mars_data = {
        'news_title': news_title,
        'news_par': news_p,
        'feat_img': featured_image_url,
        'weather': mars_weather,
        'table': html_table,
        'hemispheres': hemisphere_image_urls
    }

    return mars_data