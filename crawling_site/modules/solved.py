import requests
from bs4 import BeautifulSoup
import concurrent.futures

MAX_THREADS = 30

class Solved():
    URL = 'https://solved.ac/search?query='
    selector = '#__next > div.contents > div:nth-child(3) > div:nth-child(2) > div > div.StickyTable__Wrapper-akg1ak-3.tcQcH.sticky-table > div > div:nth-child(2)'
    baek_URL = 'https://www.acmicpc.net/problem/'
    
    def __init__(self, prob_nums):
        self.prob_nums = prob_nums
        self.tier_info = []
    
    def get_tier(self, prob_num):
        prob_URL = self.URL + prob_num
        baek_URL = self.baek_URL + prob_num
        res = requests.get(prob_URL)
        soup = BeautifulSoup(res.text, 'html.parser')
        soup = soup.select_one(self.selector)
        soup_a = soup.find('a', {'href':baek_URL})
        tier_info = soup_a.img.get('alt')
        self.tier_info.append((prob_num, tier_info))
    
    def initiate_multithread_crawling(self):
        threads = min(MAX_THREADS, len(self.prob_nums))
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(self.get_tier, self.prob_nums)
    
    def get_result(self):
        return self.tier_info