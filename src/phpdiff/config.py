# coding=utf-8
'''
Created on 2013年10月28日

@author: liwei06
'''
from datetime import date
import md5

today = date.today()
__qa_param = md5.new(today.strftime("%Y.%m.%d") + 'bingo-view-data-mode').hexdigest()

PDIFF_CONFIG = {
    'retry_time': 2,
    'report_platform': "http://cp01-rd-forum-002.cp01.baidu.com:8666/diff/result.htm?",
    'report_folder': '../../report',
    'default_ignore_value_param': ["sprite", "freq_forum", "forum_rcmd", "tracecode", "cip", "ip",
        "pub_env", "net_type", "net_speed", "cur_url", "current_clock", "tbs", "view_num", "time",
        "reply_num", "reply_amount", "post_num", "style_id", "timeline_pass", "search_time",
        "psSearchNumber", "cur_time", "comment_threshold", "comment_amount", "click_amount", "sid",
        "freq_num", "total_num", "grade_exp", "total_count", "baidu_id", "starRegInfo", "log_id",
        "repost_count", "sign_count", "sign_rank", "total_amount", "tid_hidden_num", "server_time",
        "start_time", "join_num", "week_rank", "yesterday_rank", "monthly_rank_info", "total_page",
        "advertise", "version", "last_modified_time", "last_user_id", "last_user_ip", "tidinfo",
        "group_count_in_forum", "c_sign_num", "current_rank", "pdiffTest", "click_num", "ftime",],
    'default_ignore_value_param_fuzzy': ["WAP_DISCOVERY_*", "PC_SLIDER_*", "PC_INDEX_*",
        "PC_SEARCH_*", "PC_PHOTO_*", "PC_PB_*", "PC_FRS_*", "WAP_FRS_*", "WAP_PB_*"],
    'default_ignore_key_param': ["live_info", "is_mute", "tenyear", "logid", "freq_forum", "pubEnv",
        "net_speed", "forum_rcmd", "mute_info"],
    'default_parameters': [
        '__qa=' + __qa_param,
        '__type=json'
        ]
    }


URL_REPLACE = {
                'tieba.baidu.com' : 'HOST:8080',
                'wapp.baidu.com' : 'HOST:8080',
                'c.tieba.baidu.com' : 'HOST:8080',
                'service.tieba.baidu.com' : 'HOST:8081',
                'fe.tieba.baidu.com' : 'HOST:80'
               }


