import datetime
import pytz
import requests

from pprint import pprint
from bs4 import BeautifulSoup

class Baekjoon():
    
    # get today's date
    def get_date(self):
        now = datetime.datetime.now()
        formatted_today = f'{now.year}-{now.month:02}-{now.day-1:02}'
        return formatted_today

    # get info from web
    def get_info(self, subject, URL, selector):
        result = []
        res = requests.get(URL)
        soup = BeautifulSoup(res.text, 'html.parser')
        soup = soup.select_one(selector)
        # users info
        if subject == 'users':
            infos = soup.find_all('div', {'class': 'member'})
            for info in infos:
                result.append(info.h4.a.text)
            return result
        # problems info
        elif subject == 'problems':
            infos = soup.find_all('tr')
            for info in infos:
                result_span = info.find('span', {'class': 'result-ac'})          
                # 맞았으면 통째로 반환
                if result_span:
                    result.append(info)
            return result

    # get user ids -> returns dictionary of key: user_id ,val: []
    def get_user_ids(self):
        user_URL = 'https://www.acmicpc.net/group/member/10060'
        user_selector = 'body > div.wrapper > div.container.content > div.row > div:nth-child(5)'

        user_ids = self.get_info('users', user_URL, user_selector)
        # print(f'오늘자 서울_1반 알고리즘 스터디 가입자:\n{user_ids}\n')

        # initialize dictionary to record todays' solves
        dic = {}
        for user_id in user_ids:
            dic[user_id] = []
        return user_ids, dic

    # get results for each user
    def get_all_results(self):
        user_ids, user_dict = self.get_user_ids()
        formatted_today = self.get_date()
        for user_id in user_ids:
            grading_URL = f'https://www.acmicpc.net/status?problem_id=&user_id={user_id}&language_id=-1&result_id=-1'
            grading_selector = '#status-table > tbody'
            prob_infos = self.get_info('problems', grading_URL, grading_selector)
        
        for prob_info in prob_infos:
            # print(prob_info)
            prob = prob_info.find('a', {'class': 'problem_title'})
            prob_title = prob.get('title')
            prob_num = prob.text
            date = prob_info.find('a', {'class': 'real-time-update'}).get('title')[:10]
            if date == formatted_today:
                user_dict[user_id].append((prob_num, prob_title))

        # show results
        # print('오늘 푼 문제 목록:')
        # pprint(user_dict)
        return user_dict