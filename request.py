import requests as r
import logging


def get_html(_id):

    url = 'https://store.steampowered.com/app/{}'.format(_id)

    headers = {
        'Host': 'store.steampowered.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,en-US;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://store.steampowered.com/',
        'Connection': 'keep-alive',
        'Cookie': 'browserid=2141975733889957544; timezoneOffset=28800,0; recentapps=%7B%221135910%22%3A1600237411%2C%2210%22%3A1600236805%2C%221025410%22%3A1600236799%2C%22397540%22%3A1600236717%7D; steamCountry=CN%7C355fea2e41ef22f03c7515677398cf7f; sessionid=ed0b20a44001736401b4f3b7; app_impressions=397540@1_4_4__129_1|1135910@1_4_4__43_1|1046030@1_4_4__139_3|418240@1_4_4__139_3|1222140@1_4_4__139_3|435150@1_4_4__139_2|433340@1_4_4__139_2|397540@1_4_4__129_1|130@1_5_9__412|70@1_5_9__412|60@1_5_9__412|50@1_5_9__412|40@1_5_9__412|30@1_5_9__412|20@1_5_9__412|300@1_5_9__412|10:80@1_5_9__412|1066610@1_5_9__game-mods_2|1283930@1_5_9__game-mods_1|812440@1_5_9__game-mods|107410@1_5_9__300_6|218620@1_5_9__300_5|578080@1_5_9__300_4|1237970@1_5_9__300_3|359550@1_5_9__300_2|730@1_5_9__300_1|578080@1_4_4__129_1|1135910@1_4_4__43_1|1046030@1_4_4__139_3|704850@1_4_4__139_3|440900@1_4_4__139_3|466560@1_4_4__139_2|433340@1_4_4__139_2|1255270@1_5_9__405|1255260@1_5_9__405|1255250@1_5_9__405; birthtime=943977601; lastagecheckage=1-0-2000',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'Cache-Control': 'max-age=0'
    }
    try:
        for i in range(3):
            try:
                res = r.get(url, headers=headers, allow_redirects=False)
                if res.status_code == 200:
                    return res.text
                else:
                    break
            except r.exceptions.RequestException:
                i += 1
    except Exception as e:
        logging.warning(e.__str__())


if __name__ == '__main__':

    with open('./_test/test_html.py', 'w', encoding='utf-8') as f:
        f.write("test_html = '''")
        f.write(get_html(291750))
        f.write("'''")
        print('Done.')
