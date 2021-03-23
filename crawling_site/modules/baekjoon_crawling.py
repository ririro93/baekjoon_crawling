import datetime
import requests
import concurrent.futures
from bs4 import BeautifulSoup

class Baekjoon():
    member_URL = 'https://www.acmicpc.net/group/member/10060'
    member_selector = 'body > div.wrapper > div.container.content > div.row > div:nth-child(5)'
    member_selector2 = '#team_member'
    solves_selector = '#status-table > tbody'
    
    def __init__(self):
        self.member_ids = []
        self.member_dict = {}
        self.MAX_THREADS = 30
        
    # crawl member ids
    def crawl_member_ids(self):
        res = requests.get(self.member_URL)
        soup = BeautifulSoup(res.text, 'html.parser')
        soup1 = soup.select_one(self.member_selector)
        soup2 = soup.select_one(self.member_selector2)
        # users info
        infos1 = soup.find_all('div', {'class': 'member'})
        infos2 = soup.find_all('div', {'class': 'member'})
        for info in infos1:
            self.member_ids.append(info.h4.a.text)    
        for info in infos2:
            self.member_ids.append(info.h4.a.text)    
    
    # crawl member solves for each id
    def crawl_member_solves(self, member_id):
        solves_URL = f'https://www.acmicpc.net/status?problem_id=&user_id={member_id}&language_id=-1&result_id=4'
        res = requests.get(solves_URL)
        soup = BeautifulSoup(res.text, 'html.parser')
        soup = soup.select_one(self.solves_selector)
        solves_trs = soup.find_all('tr')
        
        # 맞은 문제는 적절한 데이터만 골라서 user_dict에 담기
        corrects = []
        for solves_tr in solves_trs:
            result_span = solves_tr.find('span', {'class': 'result-ac'})          
            if result_span:
                q = solves_tr.find('a', {'class': 'problem_title'})
                q_title = q.get('title')
                q_num = q.text
                solved_time = solves_tr.find('a', {'class': 'real-time-update'}).get('title')
                q_info_dict = {
                    'question_title': q_title,
                    'question_number': q_num,
                    'question_site': 'B',
                    'solved_time': solved_time,                
                }
                self.member_dict[member_id].append(q_info_dict)
    
    # assign threads to different ids
    def initiate_multithread_crawling(self, member_ids):
        # initiate member_dict
        for member_id in member_ids:
            self.member_dict[member_id] = []
        
        # initiate crawling with threads
        threads = min(self.MAX_THREADS, len(member_ids))
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(self.crawl_member_solves, member_ids)
    
    def get_member_solves_dict(self):
        return self.member_dict        
    
    def get_member_ids(self):
        return self.member_ids