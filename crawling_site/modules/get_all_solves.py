import requests
from bs4 import BeautifulSoup
import concurrent.futures

class AllSolves():
    profile_URL = 'https://www.acmicpc.net/user/'
    profile_selector = 'body > div.wrapper > div.container.content > div.row > div:nth-child(2) > div > div.col-md-9 > div:nth-child(1) > div.panel-body'
    
    def __init__(self, user_id):
        self.MAX_THREADS = 30
        self.user_id = user_id
        self.prob_nums = []
        self.solves_data = []
    
    def get_prob_nums(self):
        user_URL = self.profile_URL + self.user_id
        res = requests.get(user_URL)
        soup = BeautifulSoup(res.text, 'html.parser')
        soup = soup.select_one(self.profile_selector)
        solved_probs_atags = soup.find_all('a')
        for solved_probs_atag in solved_probs_atags:
            self.prob_nums.append(solved_probs_atag.text)
        return 'solved problem numbers recorded'
    
    def get_solves_data(self, prob_num):
        solve_URL = f'https://www.acmicpc.net/status?problem_id={prob_num}&user_id={self.user_id}&language_id=-1&result_id=-1'
        solve_selector = '#status-table > tbody'
        res = requests.get(solve_URL)
        soup = BeautifulSoup(res.text, 'html.parser')
        soup = soup.select_one(solve_selector)
        solved_probs_tr_tags = soup.find_all('tr')
        for solved_probs_tr_tag in solved_probs_tr_tags:
            result_span = solved_probs_tr_tag.select_one('span', {'class': 'result-ac'})      
            if result_span:
                q = solved_probs_tr_tag.find('a', {'class': 'problem_title'})
                q_title = q.get('title')
                q_num = q.text
                solved_time = solved_probs_tr_tag.find('a', {'class': 'real-time-update'}).get('title')
                q_info_dict = {
                    'question_title': q_title,
                    'question_number': q_num,
                    'question_site': 'B',
                    'solved_time': solved_time,                
                }
                self.solves_data.append(q_info_dict)
                break
    
    def multi_threading(self):
        print(self.user_id, self.get_prob_nums())
        threads = min(self.MAX_THREADS, len(self.prob_nums))
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(self.get_solves_data, self.prob_nums)
    
    def get_result(self):
        return self.solves_data