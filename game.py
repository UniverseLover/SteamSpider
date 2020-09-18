from bs4 import BeautifulSoup


import logging


class RequestException(Exception):
    pass


class ParseException(Exception):
    pass


class UnsupportTypeException(Exception):
    pass


class Game:

    def __init__(self, app_id, err=None):

        self.app_id = app_id
        self.err = err
        self.name = None
        self.description = None
        self.summary_lately = None
        self.summary = None
        self.price = None
        self.publish_date = None
        self.developers = None
        self.publishers = None
        self.tags = None
        self.is_ea = None

        self.singleplay = None
        self.online_pvp = None
        self.online_pve = None
        self.local_pvp = None
        self.local_pve = None
        self.lan_pvp = None
        self.lan_pve = None
        self.cross_platfrom_support = None

        self.inner_cart = None
        self.has_vac = None
        self.has_cloud = None
        self.workshop_support = None
        self.controller_support = None
        self.has_achievement = None
        self.steam_card = None

        self.tv_streaming_support = None
        self.pad_streaming_support = None
        self.phone_streaming_support = None
        self.remote_play_together = None

        self.statistic_data = None
        self.editor_support = None
        self.cc_support = None
        self.commentary_support = None

        self.vr_support = None
        self.has_drm = None
        self.chinese_support = None

    def __str__(self):

        return '\n'.join(['{}:{}'.format(i, self.__getattribute__(i)) for i in self.__dict__ if i != 'err'])

    @classmethod
    def getGameByHtml(cls, _id, html):

        if html:
            try:
                return parse_html(_id, html)
            except UnsupportTypeException:
                logging.debug(
                    'Unsurpport type!May be DLC or locked game.[app_id={}]'.format(_id))
                return Game(_id, UnsupportTypeException)
            except Exception as e:
                logging.warning(e.__str__()+'[app_id={}]'.format(_id))
                return Game(_id, ParseException)
        else:
            return Game(_id, RequestException)

    def get_json(self):
        self.__delattr__('err')
        return {i: self.__dict__[i] for i in self.__dict__}


def get_summary(soup):
    sm = soup.find_all(
        'span', class_='game_review_summary')
    return [i.getText() for i in sm] if len(sm) == 2 else (None, None)


def get_price(soup):

    pur = soup.find('div', class_='game_purchase_price price')
    ori = soup.find('div', class_='discount_original_price')
    try:
        if pur:
            pur_text = pur.getText().strip()
            if pur_text.startswith('免费') or ('free' in pur_text.lower()):
                return 0
            else:
                return float(pur_text[2:].replace(',', ''))
        elif ori:
            return float(ori.getText().strip()[2:].replace(',', ''))
    except:
        return


def in_category(cate, info):

    if not cate:
        return False

    for i in cate.find_all('a', class_='name'):
        if i.getText().strip() == info:
            return True
    return False


def get_chinese_support(soup):

    lans = soup.find('table', class_='game_language_options')
    chs_li = []

    if not lans:
        return 0

    for tr in lans.find_all('tr', class_=''):
        if tr.find('td', class_='ellipsis') and tr.find('td', class_='ellipsis').getText().strip() == '简体中文':
            chs_tr = tr
            for td in chs_tr.find_all('td', class_='checkcol'):
                chs_li.append(1 if td.getText().strip() == '✔' else 0)
            break

    if len(chs_li) != 3:
        return 0

    return chs_li[0]*4+chs_li[1]*2+chs_li[2]


def parse_html(_id, html):

    raw = Game(_id)

    soup = BeautifulSoup(html, 'html.parser')

    if soup.find('div', id='error_box')\
            or soup.find('div', class_='game_area_dlc_bubble')\
            or soup.find('div', class_='game_area_soundtrack_bubble'):
        raise UnsupportTypeException
    raw.name = soup.find('div', class_='apphub_AppName').getText()
    raw.description = soup.find(
        'div', class_='game_description_snippet').getText().strip() if soup.find(
        'div', class_='game_description_snippet') else ''
    raw.summary_lately, raw.summary = get_summary(soup)
    raw.price = get_price(soup)
    raw.publish_date = soup.find(
        'div', class_='release_date').find('div', class_='date').getText() if soup.find(
        'div', class_='release_date') else None
    raw.developers = [i.getText() for i in soup.find(
        'div', id='developers_list').find_all('a')] if soup.find(
        'div', id='developers_list') else []
    raw.publishers = [i.getText() for i in soup.find_all('div', class_='dev_row')[
        1].find_all('a')] if len(soup.find_all('div', class_='dev_row')
         )==2 else []
    raw.tags = [i.getText().strip()
                for i in soup.find_all('a', class_='app_tag')]
    raw.is_ea = bool(soup.find('div', class_='early_access_header'))

    cate = soup.find('div', id='category_block')

    raw.singleplay = in_category(cate, '单人')
    raw.online_pvp = in_category(cate, '线上玩家对战')
    raw.online_pve = in_category(cate, '在线玩家合作')
    raw.local_pvp = in_category(cate, '共享/分屏玩家对战')
    raw.local_pve = in_category(cate, '共享/分屏合作')
    raw.lan_pvp = in_category(cate, '局域网玩家对战')
    raw.lan_pve = in_category(cate, '局域网合作')
    raw.cross_platfrom_support = in_category(cate, '跨平台联机游戏')
    raw.inner_cart = in_category(cate, '应用内购买')
    raw.has_vac = in_category(cate, '启用 Valve 反作弊保护')
    raw.has_cloud = in_category(cate, 'Steam 云')
    raw.workshop_support = in_category(cate, 'Steam 创意工坊')
    raw.controller_support = in_category(cate, '完全支持控制器')
    raw.has_achievement = in_category(cate, 'Steam 成就')
    raw.steam_card = in_category(cate, 'Steam 集换式卡牌')
    raw.tv_streaming_support = in_category(cate, '在电视上远程畅玩')
    raw.pad_streaming_support = in_category(cate, '在平板上远程畅玩')
    raw.phone_streaming_support = in_category(cate, '在手机上远程畅玩')
    raw.remote_play_together = in_category(cate, '远程同乐')

    raw.statistic_data = in_category(cate, '统计数据')
    raw.editor_support = in_category(cate, '包含关卡编辑器')
    raw.cc_support = in_category(cate, '支持字幕')
    raw.commentary_support = in_category(cate, '解说可用')

    raw.vr_support = bool(soup.find('div', class_='block_title vrsupport'))
    raw.has_drm = bool(soup.find('div', class_='DRM_notice'))
    raw.chinese_support = get_chinese_support(soup)

    return raw


if __name__ == '__main__':
    from _test.test_html import test_html

    game = Game.getGameByHtml(271590, test_html)

    print(game.get_json())
