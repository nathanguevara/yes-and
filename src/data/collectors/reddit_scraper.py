import requests
import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import time
from tqdm import tqdm


class RedditScraper:
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.headers = {
            'User-Agent': 'ComedyBot/1.0 (Comedy Data Collection)'
        }
        self.subreddits = ['jokes', 'dadjokes', 'oneliners', 'clevercomebacks']
    
    def scrape_subreddit(
        self,
        subreddit: str,
        limit: int = 1000,
        time_filter: str = 'all'
    ) -> List[Dict]:
        posts = []
        after = None
        
        with tqdm(total=limit, desc=f"Scraping r/{subreddit}") as pbar:
            while len(posts) < limit:
                url = f"https://www.reddit.com/r/{subreddit}/top.json"
                params = {
                    'limit': min(100, limit - len(posts)),
                    't': time_filter,
                    'after': after
                }
                
                try:
                    response = requests.get(url, headers=self.headers, params=params)
                    response.raise_for_status()
                    data = response.json()
                    
                    if not data['data']['children']:
                        break
                    
                    for post in data['data']['children']:
                        post_data = self._extract_post_data(post['data'])
                        if post_data:
                            posts.append(post_data)
                            pbar.update(1)
                    
                    after = data['data']['after']
                    if not after:
                        break
                    
                    time.sleep(2)  # Rate limiting
                    
                except Exception as e:
                    print(f"Error scraping {subreddit}: {e}")
                    break
        
        return posts
    
    def _extract_post_data(self, post: Dict) -> Optional[Dict]:
        if post.get('is_self') and post.get('selftext'):
            return {
                'id': post['id'],
                'title': post['title'],
                'body': post['selftext'],
                'score': post['score'],
                'num_comments': post['num_comments'],
                'created_utc': post['created_utc'],
                'subreddit': post['subreddit'],
                'permalink': f"https://reddit.com{post['permalink']}"
            }
        elif not post.get('is_self'):
            return {
                'id': post['id'],
                'title': post['title'],
                'body': '',
                'score': post['score'],
                'num_comments': post['num_comments'],
                'created_utc': post['created_utc'],
                'subreddit': post['subreddit'],
                'permalink': f"https://reddit.com{post['permalink']}"
            }
        return None
    
    def scrape_comments(self, post_id: str, subreddit: str) -> List[Dict]:
        url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            if len(data) < 2:
                return []
            
            comments = []
            comment_data = data[1]['data']['children']
            
            for comment in comment_data[:10]:  # Top 10 comments
                if comment['kind'] == 't1':
                    comments.append({
                        'id': comment['data']['id'],
                        'body': comment['data']['body'],
                        'score': comment['data']['score'],
                        'author': comment['data']['author']
                    })
            
            return comments
            
        except Exception as e:
            print(f"Error fetching comments for {post_id}: {e}")
            return []
    
    def save_data(self, posts: List[Dict], filename: str):
        output_path = self.output_dir / f"{filename}.json"
        
        with open(output_path, 'w') as f:
            json.dump(posts, f, indent=2)
        
        print(f"Saved {len(posts)} posts to {output_path}")
    
    def scrape_all(self, posts_per_subreddit: int = 500):
        all_posts = []
        
        for subreddit in self.subreddits:
            print(f"\nScraping r/{subreddit}...")
            posts = self.scrape_subreddit(subreddit, limit=posts_per_subreddit)
            
            for post in posts[:50]:  # Get comments for top 50 posts
                comments = self.scrape_comments(post['id'], subreddit)
                if comments:
                    post['top_comment'] = comments[0]['body']
                    post['comments'] = comments
                time.sleep(1)  # Rate limiting
            
            all_posts.extend(posts)
            self.save_data(posts, f"{subreddit}_{datetime.now().strftime('%Y%m%d')}")
        
        self.save_data(all_posts, f"all_comedy_posts_{datetime.now().strftime('%Y%m%d')}")
        
        return all_posts