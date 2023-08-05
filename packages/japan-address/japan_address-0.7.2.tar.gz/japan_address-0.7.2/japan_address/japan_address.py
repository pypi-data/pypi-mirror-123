import os
import re
import sqlite3
from difflib import SequenceMatcher


class JapanAddress():
    conn = None
    cur = None
    table0 = str.maketrans("1234567890", "１２３４５６７８９０", "")
    table1 = str.maketrans("一二三四五六七八九", "１２３４５６７８９", "")

    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.cur = self.conn.cursor()

        dirname = os.path.dirname(__file__)
        input_file_name = f"{dirname}/data/local_government.csv"

        with open(input_file_name) as f:
            # テーブル作成
            sql = '''CREATE TABLE local_government (
                    prefecture TEXT,
                    country TEXT,
                    city TEXT,
                    pref_code TEXT,
                    city_code TEXT,
                    designated TEXT
                    )'''
            self.cur.execute(sql)

            first = True
            for line in f.readlines():
                if first:
                    # skip 1st line
                    first = False
                    continue

                data = line.strip().split(",")

                prefecture = data[0]
                country = data[1]
                city = data[2]
                code = data[3]
                pref_code = code[:2]
                city_code = code[2:]
                designated = data[4]

                sql = f"""INSERT INTO local_government values(
                        '{prefecture}',
                        '{country}',
                        '{city}',
                        '{pref_code}',
                        '{city_code}',
                        '{designated}'
                        )"""
                self.cur.execute(sql)
            self.conn.commit()


    def __del__(self):
        self.cur.close()
        self.conn.close()

    #
    # Level: 0
    #
    def get_records(self, prefecture=None, country=None, city=None, pref_code=None, city_code=None, designated=False):

        sql = "SELECT prefecture, country, city, pref_code, city_code, designated FROM local_government"

        where_clause = []
        if prefecture is not None:
            where_clause.append(f"prefecture = '{prefecture}'")
        if country is not None:
            where_clause.append(f"country = '{country}'")
        if city is not None:
            where_clause.append(f"city = '{city}'")
        if pref_code is not None:
            where_clause.append(f"pref_code = '{pref_code}'")
        if city_code is not None:
            where_clause.append(f"city_code = '{city_code}'")
        if designated:
            where_clause.append(f"designated <> '1'")
        else:
            where_clause.append(f"designated <> '2'")

        sql += " WHERE "
        sql += " AND ".join(where_clause)
        
        self.cur.execute(sql)
        results = []
        for row in self.cur:
            results.append({
                'prefecture': row[0],
                'country': row[1],
                'city': row[2],
                'pref_code': row[3],
                'city_code': row[4],
                'designated': row[5]
            })
        return results


    def get_prefecture_list(self):
        sql = "SELECT distinct prefecture FROM local_government"

        self.cur.execute(sql)

        results = []
        for row in self.cur:
            results.append(row[0])

        return results


    def get_country_list(self, prefecture=None):
        sql = "SELECT distinct country FROM local_government WHERE country <> ''"

        if prefecture is not None:
            sql += f" AND prefecture = '{prefecture}'"

        self.cur.execute(sql)

        results = []
        for row in self.cur:
            results.append(row[0])

        return results


    def get_city_list(self, prefecture=None, country=None, designated=False):
        sql = "SELECT distinct city FROM local_government"

        where_clause = []
        if prefecture is not None:
            where_clause.append(f"prefecture = '{prefecture}'")
        if country is not None:
            where_clause.append(f"country = '{country}'")
        if designated:
            where_clause.append(f"designated <> '1'")
        else:
            where_clause.append(f"designated <> '2'")
        sql += " WHERE "
        sql += " AND ".join(where_clause)

        self.cur.execute(sql)

        results = []
        for row in self.cur:
            results.append(row[0])

        return results
    
    #
    # Level: 1
    #
    def n_to_prefecture(self, n=None, prefecture=None):        
        sql = "SELECT distinct pref_code, prefecture FROM local_government"

        where_clause = []
        if n is not None:
            where_clause.append(f"pref_code = '{n.zfill(2)}'")
        if prefecture is not None:
            where_clause.append(f"prefecture = '{prefecture}'")
        if len(where_clause) != 0:
            sql += " WHERE "
            sql += " AND ".join(where_clause)

        self.cur.execute(sql)

        results = {}
        for row in self.cur:
            i = int(row[0])
            results[str(i)] = row[1]
        return results


    def nn_to_prefecture(self, nn=None, prefecture=None): 
        sql = "SELECT distinct pref_code, prefecture FROM local_government"

        where_clause = []
        if nn is not None:
            where_clause.append(f"pref_code = '{nn.zfill(2)}'")
        if prefecture is not None:
            where_clause.append(f"prefecture = '{prefecture}'")
        if len(where_clause) != 0:
            sql += " WHERE "
            sql += " AND ".join(where_clause)

        self.cur.execute(sql)

        results = {}
        for row in self.cur:
            results[f"{row[0]}"] = row[1]
        return results


    def prefecture_code_to_prefecture(self, pref_code=None, prefecture=None):
        return self.nn_to_prefecture(pref_code, prefecture)


    def city_code_to_city(self, prefecture, city_code=None, city=None, designated=False):
        sql = "SELECT city_code, city FROM local_government"

        where_clause = []
        if prefecture is not None:
            where_clause.append(f"prefecture = '{prefecture}'")
        if city_code is not None:
            where_clause.append(f"city_code = '{city_code}'")
        if city is not None:
            where_clause.append(f"city = '{city}'")
        if designated:
            where_clause.append(f"designated <> '1'")
        else:
            where_clause.append(f"designated <> '2'")
        sql += " WHERE "
        sql += " AND ".join(where_clause)

        self.cur.execute(sql)

        results = {}
        for row in self.cur:
            results[f"{row[0]}"] = row[1]
        return results


    def local_government_code_to_city(self, lg_code=None, prefecture=None, city=None, designated=False):
        sql = "SELECT pref_code, city_code, city FROM local_government"

        where_clause = []
        if lg_code is not None:
            pref_code = lg_code[:2]
            city_code = lg_code[2:]
            where_clause.append(f"pref_code = '{pref_code}'")
            where_clause.append(f"city_code = '{city_code}'")
        if prefecture is not None:
            where_clause.append(f"prefecture = '{prefecture}'")
        if city is not None:
            where_clause.append(f"city = '{city}'")
        if designated:
            where_clause.append(f"designated <> '1'")
        else:
            where_clause.append(f"designated <> '2'")
        sql += " WHERE "
        sql += " AND ".join(where_clause)

        self.cur.execute(sql)

        results = {}
        for row in self.cur:
            results[f"{row[0]}{row[1]}"] = row[2]
        return results


    def local_government_code_to_prefecture_city(self, lg_code=None, prefecture=None, city=None, designated=False):
        sql = "SELECT pref_code, city_code, prefecture, city FROM local_government"

        where_clause = []
        if lg_code is not None:
            pref_code = lg_code[:2]
            city_code = lg_code[2:]
            where_clause.append(f"pref_code = '{pref_code}'")
            where_clause.append(f"city_code = '{city_code}'")
        if prefecture is not None:
            where_clause.append(f"prefecture = '{prefecture}'")
        if city is not None:
            where_clause.append(f"city = '{city}'")
        if designated:
            where_clause.append(f"designated <> '1'")
        else:
            where_clause.append(f"designated <> '2'")
        sql += " WHERE "
        sql += " AND ".join(where_clause)

        self.cur.execute(sql)

        results = {}
        for row in self.cur:
            results[f"{row[0]}{row[1]}"] = row[2] + row[3]
        return results


    def prefecture_country_to_country(self, prefecture=None, country=None):
        sql = "SELECT distinct prefecture, country FROM local_government WHERE country <> ''"

        where_clause = []
        if prefecture is not None:
            where_clause.append(f"prefecture = '{prefecture}'")
        if country is not None:
            where_clause.append(f"country = '{country}'")
        if len(where_clause) != 0:
            sql += " AND "
            sql += " AND ".join(where_clause)

        self.cur.execute(sql)

        results = {}
        for row in self.cur:
            results[f"{row[0]}{row[1]}"] = row[1]
        # print(results)
        return results


    def prefecture_city_to_city(self, prefecture=None, city=None, designated=False):
        sql = "SELECT prefecture, city FROM local_government"

        where_clause = []
        if prefecture is not None:
            where_clause.append(f"prefecture = '{prefecture}'")
        if city is not None:
            where_clause.append(f"city = '{city}'")
        if designated:
            where_clause.append(f"designated <> '1'")
        else:
            where_clause.append(f"designated <> '2'")
        sql += " WHERE "
        sql += " AND ".join(where_clause)

        self.cur.execute(sql)

        results = {}
        for row in self.cur:
            results[f"{row[0]}{row[1]}"] = row[1]
        # print(results)
        return results


    #
    # Level: 2
    #
    def extract_prefecture(self, address):
        # addressは都道府県から始まっている前提
        for pref in self.get_prefecture_list():
            m = re.match(rf"^{pref}", address)
            if m is not None:
                return pref

        return None


    def extract_country(self, address):
        # addressは都道府県から始まっている前提
        for prefecture_country, country in self.prefecture_country_to_country().items():
            m = re.match(rf"^{prefecture_country}", address)
            if m is not None:
                pref = prefecture_country.replace(country, "")
                return pref, country

        pref = self.extract_prefecture(address)

        return pref, None


    def extract_city(self, address, designated=False):
        # addressは都道府県から始まっている前提

        # 郡があったら郡を除去する
        pref, country = self.extract_country(address)
        if country is not None:
            address = address.replace(pref + country, pref)

        for prefecture_city, city in self.prefecture_city_to_city(designated=designated).items():
            m = re.match(rf"^{prefecture_city}", address)
            if m is not None:
                pref = prefecture_city.replace(city, "")
                return pref, city

        pref = self.extract_prefecture(address)

        return pref, None


    def extract_details(self, address, designated=False):
        # addressは都道府県から始まっている前提
        # pref = self.extract_prefecture(address)
        pref, country = self.extract_country(address)
        pref, city = self.extract_city(address, designated=designated)

        # 都道府県、市区町村のいずれかが検出されなかった場合は失敗としてNoneを返却
        if pref is None or city is None:
            return None, None, None
        if country is None:
            details = re.sub(rf'^{pref}{city}', '', address)            # 都道府県+市区町村を除去
        else:
            details = re.sub(rf'^{pref}{country}{city}', '', address)   # 都道府県+郡+市区町村を除去

        return pref, city, details


    #
    # Utils
    #
    def resolve_prefecture(self, address):
        """
        把握している同一名称
            府中市: 東京都、広島県
            伊達市: 北海道、福島県

            安芸郡: 広島県、高知県
            大島郡: 山口県、鹿児島県
            熊毛郡: 山口県、鹿児島県
            日高郡: 北海道、和歌山県
            愛知郡: 愛知県、滋賀県
            海部郡: 愛知県、徳島県
            三島郡: 新潟県、大阪府
        この情報は利用していない。複数該当するときはNoneを返却
        """
        prefecture_list = []

        # 郡から始まっているケース
        for prefecture_country, country in self.prefecture_country_to_country().items():
            m = re.match(rf"^{country}", address)
            if m is not None:
                pref = prefecture_country.replace(country, "")
                prefecture_list.append(pref)
        
        # 市区町村からは始まっているケース
        for prefecture_city, city in self.prefecture_city_to_city().items():
            m = re.match(rf"^{city}", address)
            if m is not None:
                pref = prefecture_city.replace(city, "")
                prefecture_list.append(pref)

        # 総当たりで点検して1つしか候補が無いときに結果を返却
        if len(prefecture_list) == 1:
            return prefecture_list[0]
        else:
            return None     # 一意に決まらないときはNoneを返却


    def normalize_address(self, address):

        address = address.split(" ")[0].split("　")[0]

        # 半角数字は全角に
        address = address.translate(self.table0)

        key_list = [
            "丁目",
            "番地の",
            "番地",
            "番の",
            "番",
            "の",
            "号",
        ]
        pos_list = []
        for key in key_list:
            m = re.search(rf'[一二三四五六七八九十１２３４５６７８９０]+{key}', address)
            if m:  # 検索にヒット
                pos_list.append(m.start())  # hitした位置

        if len(pos_list) != 0:
            pos = min(pos_list)
            head = address[:pos]    # 前半
            tail = address[pos:]    # 後半
            tail = tail.replace("十", "").translate(self.table1)
            address = head + tail

        for key in key_list:
            address = re.sub(rf'([１２３４５６７８９０]){key}', r'\1－', address)
        address = re.sub(r'－$', '', address)

        return address


    def compare_address(self, address1, address2):

        address1 = self.normalize_address(address1)
        address2 = self.normalize_address(address2)

        if address1 == address2:
            return 100

        pref1, city1, details1 = self.extract_details(address1)
        pref2, city2, details2 = self.extract_details(address2)
        if pref1 == pref2 and city1 == city2:
            # details1とdetails2が何パーセント一致するか
            r = SequenceMatcher(None, details1, details2).ratio()
            return 50 + r * 100 / 2

        return 0
