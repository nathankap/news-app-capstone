import requests


def fetch_reddit_posts(subreddit='django', limit=10):
    url = f'https://www.reddit.com/r/{subreddit}/top.json?limit={limit}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()
    posts = []
    for item in data.get('data', {}).get('children', []):
        post = item.get('data', {})
        posts.append({
            'title': post.get('title', ''),
            'author': post.get('author', 'unknown'),
            'url': post.get('url', ''),
            'permalink': post.get('permalink', ''),
        })
    return posts
