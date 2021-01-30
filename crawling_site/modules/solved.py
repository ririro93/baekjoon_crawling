import requests
from bs4 import BeautifulSoup

class Solved():
    URL = 'https://solved.ac/search?query='
    selector = '#__next > div.contents > div:nth-child(3) > div:nth-child(2) > div > div.StickyTable__Wrapper-akg1ak-3.tcQcH.sticky-table > div > div:nth-child(2)'
    baek_URL = 'https://www.acmicpc.net/problem/'
    
    def __init__(self, prob_num):
        self.prob_num = str(prob_num)
    
    def get_tier(self):
        self.URL += self.prob_num
        self.baek_URL += self.prob_num
        res = requests.get(self.URL)
        soup = BeautifulSoup(res.text, 'html.parser')
        soup = soup.select_one(self.selector)
        soup_a = soup.find('a', {'href':self.baek_URL})
        tier_info = soup_a.img
        return tier_info
        