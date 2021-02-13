# import time

# from celery import shared_task

# from .views import update_members, update_questions_and_solves, update_question_tiers


# # run this task every 5 minutes in the background
# @shared_task
# def periodic_crawl():
#     print('automatic background crawling started')
#     print(update_members())
#     print(update_questions_and_solves())
#     print(update_question_tiers())
#     print('automatic background crawling finished')