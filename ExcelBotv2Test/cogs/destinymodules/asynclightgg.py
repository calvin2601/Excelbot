import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import random

#
# get number of pages (N) containing w = 50 rows. Each row = weapon
columns = ['Name', 'item_id', 'light.gg URL', 'PvX', 'Weap Type', 'Archetype', 'Perk 1', 'Perk 2', 'Perk 3', 'Perk 4',
           'ID_1', 'ID_2', 'ID_3', 'ID_4']
df_master = pd.DataFrame(columns=columns)


async def page_parser(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'html.parser')
            return soup


async def get_Nv2(url='https://www.light.gg/db/category/1?etc=weapons&page=1&f=4%285%29'):
    soup = await page_parser(url)
    N = int(soup.find('a', class_='last').get('href').split('&')[0].split('=')[-1])
    print(f'N = {N}')
    return N


async def list_N_pages():
    N = await get_Nv2()
    list_N_urls = [f'https://www.light.gg/db/category/1?etc=weapons&page={page_no}&f=4%285%29' for page_no in
                   range(1, N + 1)]
    print(list_N_urls)
    return list_N_urls


async def scrape_rows(url):
    soup = await page_parser(url)
    rows = soup.find_all('div', class_='legendary item-name')
    list_w_rows = [f'https://www.light.gg{row.a.get("href")}' for row in rows]
    print(list_w_rows)
    await asyncio.sleep(1)
    return (list_w_rows)


async def scrape_weapons(url):
    soup = await page_parser(url)
    # weapon name
    name = soup.find('h2').text.strip().lower()

    # item id

    item_id = soup.find('ul', id="item-details").find_all('li')[-1].text.split(': ')[-1]

    # Weapon Type
    weapon_type = soup.find('span', class_='weapon-type').text.split(' / ')[-1].rstrip()

    # Archetype
    archetype = soup.find('span', class_='pull-left').img.get('alt')

    # Perk
    perkcolumns = soup.find_all('li', class_="random clearfix")
    pveperks = {'1': [], '2': [], '3': [], '4': []}
    pve_id = {'1': [], '2': [], '3': [], '4': []}
    pvpperks = {'1': [], '2': [], '3': [], '4': []}
    pvp_id = {'1': [], '2': [], '3': [], '4': []}
    counter = 0
    for perkcolumn in perkcolumns:
        if perkcolumn.find_all('li') != []:
            counter += 1
            for perk in perkcolumn.find_all('li'):
                perkname = perk.find('div', class_="item show-hover random").img.get('alt')
                if 'class=\"pref\"' in str(perk):
                    perk_id = await perkidcheck(perk)
                    pveperks[str(counter)].append(perkname)
                    pve_id[str(counter)].append(perk_id)
                    pvpperks[str(counter)].append(perkname)
                    pvp_id[str(counter)].append(perk_id)
                    # print(str(no) + '\t' + perkname + '\tPvE+PvP')
                if 'class=\"pref prefpve\"' in str(perk):
                    perk_id = await perkidcheck(perk)
                    pveperks[str(counter)].append(perkname)
                    pve_id[str(counter)].append(perk_id)
                    # print(str(no) + '\t' + perkname + '\tPvE')
                if 'class=\"pref prefpvp\"' in str(perk):
                    perk_id = await perkidcheck(perk)
                    pvpperks[str(counter)].append(perkname)
                    pvp_id[str(counter)].append(perk_id)
                    # print(str(no) + '\t' + perkname + '\tPvP')
                await asyncio.sleep(random.uniform(1, 2))
    return name, item_id, weapon_type, archetype, pvpperks, pveperks, pvp_id, pve_id


async def df_append(url, df=df_master):
    name, item_id, weapon_type, archetype, pvpperks, pveperks, pvp_id, pve_id = await scrape_weapons(url)
    df = df.append(
        {'Name': name, 'item_id': item_id, 'light.gg URL': url, 'Weap Type': weapon_type, 'Archetype': archetype,
         'PvX': 'pve', 'Perk 1': pveperks['1'], 'Perk 2': pveperks['2'],
         'Perk 3': pveperks['3'], 'Perk 4': pveperks['4'], 'ID_1': pve_id['1'],
         'ID_2': pve_id['2'], 'ID_3': pve_id['3'], 'ID_4': pve_id['4']}, ignore_index=True)
    df = df.append(
        {'Name': name, 'item_id': item_id, 'light.gg URL': url, 'Weap Type': weapon_type, 'Archetype': archetype,
         'PvX': 'pvp', 'Perk 1': pvpperks['1'], 'Perk 2': pvpperks['2'],
         'Perk 3': pvpperks['3'], 'Perk 4': pvpperks['4'], 'ID_1': pvp_id['1'],
         'ID_2': pvp_id['2'], 'ID_3': pvp_id['3'], 'ID_4': pvp_id['4']}, ignore_index=True)
    # print(df)
    return df


async def main():
    list_w_url_complete = []
    list_N_urls = await list_N_pages()
    for url in list_N_urls:
        list_w_url_complete.extend(await scrape_rows(url))
    # list_w_url_complete.extend([await scrape_rows(url) for url in list_N_urls])
    columns = ['Name', 'light.gg URL', 'PvX', 'Weap Type', 'Archetype', 'Perk 1', 'Perk 2', 'Perk 3', 'Perk 4']
    df = pd.DataFrame(columns=columns)
    i = 0
    for url in list_w_url_complete:
        name, item_id, weapon_type, archetype, pvpperks, pveperks, pvp_id, pve_id = await scrape_weapons(url)
        i += 1
        df = df.append(
            {'Name': name, 'item_id': item_id, 'light.gg URL': url, 'Weap Type': weapon_type, 'Archetype': archetype,
             'PvX': 'pve', 'Perk 1': pveperks['1'], 'Perk 2': pveperks['2'],
             'Perk 3': pveperks['3'], 'Perk 4': pveperks['4'], 'ID_1': pve_id['1'],
             'ID_2': pve_id['2'], 'ID_3': pve_id['3'], 'ID_4': pve_id['4']}, ignore_index=True)
        df = df.append(
            {'Name': name, 'item_id': item_id, 'light.gg URL': url, 'Weap Type': weapon_type, 'Archetype': archetype,
             'PvX': 'pvp', 'Perk 1': pvpperks['1'], 'Perk 2': pvpperks['2'],
             'Perk 3': pvpperks['3'], 'Perk 4': pvpperks['4'], 'ID_1': pvp_id['1'],
             'ID_2': pvp_id['2'], 'ID_3': pvp_id['3'], 'ID_4': pvp_id['4']}, ignore_index=True)
        print(i)
        print(len(df))
        await asyncio.sleep(random.randint(1, 3))
    return df


async def perkidcheck(perk):
    suffix_url = perk.find('div', class_="item show-hover random").a.get('href')
    perk_url = 'https://www.light.gg' + suffix_url
    perk_soup = await page_parser(perk_url)
    perk_id = perk_soup.find('ul', id="item-details").find_all('li')[-1].text.split(': ')[-1]
    return perk_id
