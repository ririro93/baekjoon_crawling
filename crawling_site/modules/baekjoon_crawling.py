import datetime
import requests

from bs4 import BeautifulSoup

from .solved import Solved

class Baekjoon():
    
    # get today's date
    def get_date(self):
        now = datetime.datetime.now()
        formatted_today = f'{now.year}-{now.month:02}-{now.day:02}'
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

            # 테스트로 각 아이디 채점 현황당 3건 씩만 보기
            for prob_info in prob_infos[:3]:
                # get prob infos
                prob = prob_info.find('a', {'class': 'problem_title'})
                prob_title = prob.get('title')
                prob_num = prob.text
                solved_time = prob_info.find('a', {'class': 'real-time-update'}).get('title')
                
                # get tier info
                solved = Solved(prob_num)
                prob_tier_info = solved.get_tier()
                prob_tier = prob_tier_info.get('alt')
                prob_tier_src = prob_tier_info.get('src')

                # make dict and add to prob_infos_list
                # solved time을 어떻게 처리해야될지 고민해보기
                prob_info_dict = {
                    'question_title': prob_title,
                    'question_number': prob_num,
                    'question_tier': prob_tier,
                    'question_site': 'B',
                    'solved_time': solved_time,
                }
                user_dict[user_id].append(prob_info_dict)
        return user_dict