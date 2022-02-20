from bs4 import BeautifulSoup
import csv
import re
import requests
from db import db_connect

def wol_crawling():
    url = 'https://wol.jw.org/ko/wol/meetings/r8/lp-ko/2022/7'
    response = requests.get(url)

    html = response.text

    if response.status_code == 200:
        bs = BeautifulSoup(html, 'html.parser')

        # 집회교제 템플릿
        template = bs.select_one('div.itemData')

        # header 부분
        header = template.select_one('header')
        # 집회 날짜
        meeting_date = header.select_one('h1 > strong').get_text()
        # 성서읽기 범위
        weekly_script = header.select_one('h2 > a > strong').get_text()

        # body 부분
        body = template.select_one('div.bodyTxt')
        # 시작노래 및 소개말
        section1 = body.select_one('#section1')
        # 시작노래 및 기도
        start_song = section1.select_one('div.pGroup > ul > li:nth-child(1) > #p3').get_text()
        # 소개말
        intro = section1.select_one('div.pGroup > ul > li:nth-child(2) > #p4').get_text()

        # 성경에 담긴 보물
        section2 = body.select_one('#section2 > div.pGroup > ul')
        # 10분 연설
        speech_10 = section2.select_one('li:nth-child(1) > #p6').get_text()
        # 영적 보물 찾기
        spiritual_gems_title = section2.select_one('li:nth-child(2) > #p7').get_text()
        # 영적 보물 찾기 질문1
        sg_q1 = section2.select_one('li:nth-child(2) > ul > li:nth-child(1) > #p8').get_text()
        # 영적 보물 찾기 질문2
        sg_q2 = section2.select_one('li:nth-child(2) > ul > li:nth-child(2) > #p9').get_text()
        # 성경 낭독
        bible_reading = section2.select_one('li:nth-child(3) > #p10').get_text()

        # 야외 봉사에 힘쓰십시오
        section3_first = ''
        section3_second = ''
        section3_third = ''
        section3 = body.select_one('#section3 > div.pGroup > ul')
        # 첫번째 프로
        if section3.select_one('li:nth-child(1) > #p12') is not None:
            section3_first = section3.select_one('li:nth-child(1) > #p12').get_text()
        # 두번째 프로
        if section3.select_one('li:nth-child(2) > #p13') is not None:
            section3_second = section3.select_one('li:nth-child(2) > #p13').get_text()
        # 세번째 프로
        if section3.select_one('li:nth-child(3) > #p14') is not None:
            section3_third = section3.select_one('li:nth-child(3) > #p14').get_text()

        # 그리스도인 생활
        section4_first = ''
        section4_second = ''
        section4_third = ''
        section4_fourth = ''
        section4_fifth = ''
        section4 = body.select_one('#section4 > div.pGroup > ul')
        # 중간 노래
        middle_song = section4.select_one('li:nth-child(1) > #p16').get_text()
        section4_first = section4.select_one('li:nth-child(2) > #p17').get_text()
        section4_second = section4.select_one('li:nth-child(3) > #p18').get_text()
        section4_third = section4.select_one('li:nth-child(4) > #p19').get_text()
        section4_fourth = section4.select_one('li:nth-child(5) > #p20').get_text()
        if section4.select_one('li:nth-child(6) > #p21') is not None:
            section4_fifth = section4.select_one('li:nth-child(6) > #p21').get_text()

        cursor, db = db_connect()

        sql = """INSERT INTO meeting_schedule (
            meeting_date, weekly_script, start_song, intro, speech_10, spiritual_gems_title, sg_q1, sg_q2,
            bible_reading, section3_first, section3_second, section3_third, middle_song, section4_first,
            section4_second, section4_third, section4_fourth, section4_fifth
        ) VALUES (
            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(
            meeting_date, weekly_script, start_song, intro, speech_10, spiritual_gems_title, sg_q1, sg_q2,
            bible_reading, section3_first, section3_second, section3_third, middle_song, section4_first,
            section4_second, section4_third, section4_fourth, section4_fifth
        )

        cursor.execute(sql)
        db.commit()

    else:
        print(response.status_code)


if __name__ == '__main__':
    wol_crawling()

