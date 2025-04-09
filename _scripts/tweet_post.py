import os
import requests
from requests_oauthlib import OAuth1Session
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import json
import sys

# --- Configuration ---
SITEMAP_URL = os.environ.get("SITEMAP_URL", "https://www.async-let.com/sitemap.xml")
LOG_FILE = os.environ.get("LOG_FILE", "_scripts/tweeted_links.log")
SITE_URL_BASE = os.environ.get("SITE_URL", "https://www.async-let.com/") # Used to filter relevant sitemap URLs
CONSUMER_KEY = os.environ.get("TWITTER_API_KEY")
CONSUMER_SECRET = os.environ.get("TWITTER_API_SECRET_KEY")
ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

# --- Helper Functions ---

def set_output(name, value):
    """Sets an output variable for the GitHub Actions workflow."""
    github_output_path = os.environ.get('GITHUB_OUTPUT')
    if github_output_path:
        with open(github_output_path, 'a') as fh:
            print(f'{name}={value}', file=fh)
    else:
        print(f"::set-output name={name}::{value}") # Fallback for older runners

def load_tweeted_links(filepath):
    """Loads the set of already tweeted URLs from the log file."""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                # Use a set for efficient lookup
                return set(line.strip() for line in f if line.strip())
        else:
            print(f"Log file '{filepath}' not found, creating later.")
            return set()
    except Exception as e:
        print(f"Error loading log file {filepath}: {e}")
        return set() # Return empty set on error

def save_tweeted_links(filepath, links_set):
    """Saves the set of tweeted URLs to the log file, one URL per line."""
    try:
        # Ensure directory exists
        log_dir = os.path.dirname(filepath)
        if log_dir and not os.path.exists(log_dir):
             os.makedirs(log_dir)
             print(f"Created directory {log_dir}")

        # Sort for consistency, although order doesn't strictly matter for a set
        sorted_links = sorted(list(links_set))
        with open(filepath, 'w', encoding='utf-8') as f:
            for link in sorted_links:
                f.write(link + '\n')
        print(f"Successfully saved {len(sorted_links)} links to {filepath}")
        return True
    except Exception as e:
        print(f"Error saving log file {filepath}: {e}")
        return False

def fetch_sitemap_data(url):
    """Fetches and parses the sitemap, returning a list of (url, lastmod_datetime) tuples."""
    try:
        print(f"Fetching sitemap from {url}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status() # Raise an exception for bad status codes
        print("Sitemap fetched successfully.")

        # Define the XML namespace (often needed for sitemaps)
        # Common namespaces, adjust if yours is different
        namespaces = {
            'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9',
            # Add other namespaces if present in your sitemap, e.g., 'image', 'video'
        }

        root = ET.fromstring(response.content)
        urls = []

        # Find all 'url' elements within the sitemap namespace
        for url_element in root.findall('sitemap:url', namespaces):
            loc_element = url_element.find('sitemap:loc', namespaces)
            lastmod_element = url_element.find('sitemap:lastmod', namespaces)

            if loc_element is not None and loc_element.text:
                loc = loc_element.text.strip()
                lastmod_str = lastmod_element.text.strip() if lastmod_element is not None and lastmod_element.text else None

                # Parse lastmod date string into a datetime object
                lastmod_dt = None
                if lastmod_str:
                    try:
                        # Handle different possible ISO 8601 formats (with or without timezone)
                        if 'Z' in lastmod_str:
                             lastmod_dt = datetime.fromisoformat(lastmod_str.replace('Z', '+00:00'))
                        elif '+' in lastmod_str or '-' in lastmod_str[10:]: # Check for explicit timezone offset
                             lastmod_dt = datetime.fromisoformat(lastmod_str)
                        else: # Assume UTC if no timezone info
                             lastmod_dt = datetime.fromisoformat(lastmod_str).replace(tzinfo=timezone.utc)
                    except ValueError:
                        print(f"Warning: Could not parse lastmod date '{lastmod_str}' for URL {loc}")
                        # Assign a default old date if parsing fails? Or skip? Let's assign epoch.
                        lastmod_dt = datetime.fromtimestamp(0, tz=timezone.utc)

                # If no lastmod, use epoch time as a fallback for sorting
                if lastmod_dt is None:
                    lastmod_dt = datetime.fromtimestamp(0, tz=timezone.utc)

                urls.append((loc, lastmod_dt))

        print(f"Parsed {len(urls)} URLs from sitemap.")
        return urls

    except requests.exceptions.RequestException as e:
        print(f"Error fetching sitemap: {e}")
        return []
    except ET.ParseError as e:
        print(f"Error parsing sitemap XML: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred fetching sitemap data: {e}")
        return []

def fetch_post_metadata(url):
    """Fetches post HTML and extracts twitter:title and twitter:description."""
    try:
        print(f"Fetching post HTML from {url}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        print("Post HTML fetched successfully.")

        soup = BeautifulSoup(response.content, 'lxml') # Using lxml parser

        title_tag = soup.find('meta', attrs={'name': 'twitter:title'})
        desc_tag = soup.find('meta', attrs={'name': 'twitter:description'})

        title = title_tag['content'].strip() if title_tag and 'content' in title_tag.attrs else None
        description = desc_tag['content'].strip() if desc_tag and 'content' in desc_tag.attrs else None

        if not title:
            # Fallback to regular <title> tag if twitter:title is missing
            title_tag_html = soup.find('title')
            if title_tag_html:
                title = title_tag_html.text.strip()
                print("Warning: twitter:title meta tag not found, using HTML <title> tag.")
            else:
                 print("Error: Could not find twitter:title or HTML <title> tag.")
                 return None, None # Cannot tweet without a title

        print(f"Extracted Title: {title}")
        print(f"Extracted Description: {description}")
        return title, description

    except requests.exceptions.RequestException as e:
        print(f"Error fetching post HTML for {url}: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred fetching metadata for {url}: {e}")
        return None, None

def format_tweet(title, description, url):
    """Formats the tweet text, handling potential truncation."""
    base_text = f"{title}" # Start with title
    url_part = f"\n\n{url}" # URL on its own lines

    # Calculate remaining chars for description (if any)
    max_len = 280
    available_len = max_len - len(base_text) - len(url_part)

    desc_part = ""
    if description:
        # Add description if space allows, with ellipsis if truncated
        if available_len > 4: # Need space for "..." and potentially a newline/space
            if len(description) <= available_len - 2: # -2 for potential "\n"
                desc_part = f"\n{description}"
            else:
                desc_part = f"\n{description[:available_len - 5]}..." # Truncate with "..."
        else:
            print("Warning: Not enough space for description in tweet.")

    full_text = f"{base_text}{desc_part}{url_part}"

    # Final check - if title alone + URL is too long, truncate title
    if len(full_text) > max_len:
        print("Warning: Tweet exceeds 280 chars even after description omission/truncation. Truncating title.")
        title_max_len = max_len - len(url_part) - 5 # Space for "..." and safety
        if title_max_len < 10: # Arbitrary minimum title length
            print("Error: Cannot compose tweet, URL might be too long or title too short after truncation.")
            return None
        truncated_title = f"{title[:title_max_len]}..."
        full_text = f"{truncated_title}{url_part}" # Rebuild with truncated title, no desc

    print(f"Formatted tweet ({len(full_text)} chars): {full_text}")
    return full_text


def post_tweet(text):
    """Posts a tweet using Twitter API v2 (OAuth 1.0a)."""
    if not all([CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        print("Error: Twitter API credentials not found in environment variables.")
        return False

    payload = {"text": text}
    try:
        oauth = OAuth1Session(
            CONSUMER_KEY,
            client_secret=CONSUMER_SECRET,
            resource_owner_key=ACCESS_TOKEN,
            resource_owner_secret=ACCESS_TOKEN_SECRET,
        )
        print("Attempting to post to Twitter API v2...")
        response = oauth.post(
            "https://api.twitter.com/2/tweets",
            json=payload,
        )
        print(f"Twitter API Response Status: {response.status_code}")
        print(f"Twitter API Response Body: {response.text}")

        if response.status_code != 201:
            print(f"Error posting tweet: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Parsed Error: {json.dumps(error_data, indent=2)}")
            except json.JSONDecodeError:
                pass # Already printed raw text
            return False
        else:
            print(f"Successfully posted tweet: {json.dumps(response.json(), indent=2)}")
            return True
    except requests.exceptions.RequestException as e:
        print(f"Request error posting tweet: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred posting tweet: {e}")
        return False

# --- Main Execution ---
if __name__ == "__main__":
    print("--- Starting Tweet Script ---")
    log_updated = False

    # 1. Load already tweeted links
    tweeted_links = load_tweeted_links(LOG_FILE)
    print(f"Loaded {len(tweeted_links)} previously tweeted links.")

    # 2. Fetch and parse sitemap
    sitemap_entries = fetch_sitemap_data(SITEMAP_URL)
    if not sitemap_entries:
        print("Error: Could not fetch or parse sitemap. Exiting.")
        sys.exit(1) # Exit with error

    # 3. Filter for relevant blog posts and identify untweeted ones
    # Assuming blog posts contain '/blog/' in their URL and are from the main site
    potential_posts = [
        (url, lastmod) for url, lastmod in sitemap_entries
        if url.startswith(SITE_URL_BASE) and '/blog/' in url
    ]
    print(f"Found {len(potential_posts)} potential blog posts in sitemap.")

    untweeted_posts = [
        (url, lastmod) for url, lastmod in potential_posts
        if url not in tweeted_links
    ]
    print(f"Found {len(untweeted_posts)} untweeted blog posts.")

    # 4. If untweeted posts exist, select the latest one
    if untweeted_posts:
        # Sort by lastmod date, descending (newest first)
        untweeted_posts.sort(key=lambda item: item[1], reverse=True)
        latest_post_url, latest_post_date = untweeted_posts[0]
        print(f"Latest untweeted post: {latest_post_url} (Lastmod: {latest_post_date})")

        # 5. Fetch metadata for the latest post
        title, description = fetch_post_metadata(latest_post_url)

        if title:
            # 6. Format the tweet
            tweet_text = format_tweet(title, description, latest_post_url)

            if tweet_text:
                # 7. Post the tweet
                if post_tweet(tweet_text):
                    # 8. Add to log and save if successful
                    tweeted_links.add(latest_post_url)
                    if save_tweeted_links(LOG_FILE, tweeted_links):
                        log_updated = True
                        print(f"Successfully tweeted and updated log for: {latest_post_url}")
                    else:
                         print("Error: Tweet posted but failed to save log file!")
                         # Consider exiting with error? For now, just warn.
                else:
                    print(f"Error: Failed to post tweet for {latest_post_url}")
            else:
                 print(f"Error: Could not format tweet for {latest_post_url}. Skipping.")
        else:
            print(f"Error: Could not fetch title for {latest_post_url}. Skipping tweet.")
    else:
        print("No new blog posts found to tweet.")

    # 9. Set output for GitHub Actions workflow
    set_output('log_updated', str(log_updated).lower())
    print(f"Set workflow output log_updated={str(log_updated).lower()}")

    print("--- Tweet Script Finished ---")
