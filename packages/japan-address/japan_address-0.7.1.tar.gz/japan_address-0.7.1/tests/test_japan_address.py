import pytest
import os
import japan_address

address_list = [
    "東京都千代田区永田町１丁目７−１",
    "東京都西多摩郡瑞穂町大字箱根ヶ崎2335番地",
]
pref_list = [
    "東京都",
    "東京都",
]
country_list = [
    None,
    "西多摩郡"
]
city_list = [
    "千代田区",
    "瑞穂町",
]
details_list = [
    "永田町１丁目７−１",
    "大字箱根ヶ崎2335番地",
]

ja = japan_address.JapanAddress()

class TestJapanAddress():

    n_to_prefecture = {}
    nn_to_prefecture = {}
    prefecture_list = [] 
    country_list = []
    city_list = []
    prefecture_country_to_country = {}
    prefecture_city_to_city = {}

    def setup_method(self, method):
        dirname = os.path.dirname(__file__)
        input_file_name = f"{dirname}/../japan_address/data/local_government.csv"
        with open(input_file_name) as f:
            first = True
            for line in f.readlines():
                if first:
                    first = False
                    continue
                line = line.strip() # 改行を削除
                data = line.split(",")  # カンマ区切り
                nn = data[3][:2]
                n = str(int(nn))
                if n not in self.n_to_prefecture:
                    self.n_to_prefecture[n] = data[0]
                if nn not in self.nn_to_prefecture:
                    self.nn_to_prefecture[nn] = data[0]

                if data[0] not in self.prefecture_list:
                    self.prefecture_list.append(data[0])
                if data[1] not in self.country_list:
                    if data[1] != "":
                        self.country_list.append(data[1])
                if data[2] not in self.city_list:
                    if data[4] != "2":
                        self.city_list.append(data[2])
                if data[1] != "" and data[0]+data[1] not in self.prefecture_country_to_country:
                    self.prefecture_country_to_country[data[0]+data[1]] = data[1]
                if data[4] != "2":
                    self.prefecture_city_to_city[data[0]+data[2]] = data[2]
                            

    def teardown_method(self, method):
        pass


    def test_init(self):

        assert ja.n_to_prefecture() == self.n_to_prefecture
        assert ja.n_to_prefecture(n="1") == {"1": self.nn_to_prefecture["01"]}
        assert ja.n_to_prefecture(prefecture="北海道") == {"1": self.nn_to_prefecture["01"]}
        assert ja.n_to_prefecture(n="1", prefecture="北海道") == {"1": self.nn_to_prefecture["01"]}

        assert ja.nn_to_prefecture() == self.nn_to_prefecture
        assert ja.nn_to_prefecture(nn="01") == {"01": self.nn_to_prefecture["01"]}
        assert ja.nn_to_prefecture(prefecture="北海道") == {"01": self.nn_to_prefecture["01"]}
        assert ja.nn_to_prefecture(nn="01", prefecture="北海道") == {"01": self.nn_to_prefecture["01"]}

        assert ja.n_to_prefecture(n="2", prefecture="北海道") == {}
        assert ja.nn_to_prefecture(nn="02", prefecture="北海道") == {}
        

    #
    # Test Level:0
    #
    def test_get_records(self):
        records = ja.get_records()
        assert len(records) == 1741

        records = ja.get_records(prefecture="北海道", city="札幌市")
        assert len(records) == 1
        assert records[0] == {
            "prefecture": "北海道",
            "country": "",
            "city": "札幌市",
            "pref_code": "01",
            "city_code": "1002",
            "designated": "1",
        }


    def test_get_prefecture_list(self):
        # Test Data
        list0 = self.prefecture_list
        list1 = ja.get_prefecture_list()

        assert len(list0) == len(list1)

        for value in list0:
            assert value in list1

        for value in list1:
            assert value in list0

        assert list0 == list1


    def test_get_country_list(self):
        # Test Data
        list0 = self.country_list
        list1 = ja.get_country_list()

        assert len(list0) == len(list1)

        for value in list0:
            assert value in list1

        for value in list1:
            assert value in list0

        assert list0 == list1

        # prefecture
        list1 = ja.get_country_list(prefecture="")
        assert len(list1) == 0
        assert list1 == []

        list1 = ja.get_country_list(prefecture="福井県")
        assert len(list1) == 7
        assert list1 == [
            "吉田郡",
            "今立郡",
            "南条郡",
            "丹生郡",
            "三方郡",
            "大飯郡",
            "三方上中郡",
        ]


    def test_get_city_list(self):
        # Test Data
        list0 = self.city_list
        list1 = ja.get_city_list()

        assert len(list0) == len(list1)

        for value in list0:
            assert value in list1

        for value in list1:
            assert value in list0

        assert list0 == list1

        # prefecture, country
        list1 = ja.get_city_list(prefecture="")
        assert len(list1) == 0
        assert list1 == []

        list1 = ja.get_city_list(prefecture="福井県", country="大飯郡")
        assert len(list1) == 2
        assert list1 == [
            "高浜町",
            "おおい町",                       
        ]

        list1 = ja.get_city_list(prefecture="熊本県", designated=True)
        assert list1 == [
            "八代市",
            "人吉市",
            "荒尾市",
            "水俣市",
            "玉名市",
            "山鹿市",
            "菊池市",
            "宇土市",
            "上天草市",
            "宇城市",
            "阿蘇市",
            "天草市",
            "合志市",
            "美里町",
            "玉東町",
            "南関町",
            "長洲町",
            "和水町",
            "大津町",
            "菊陽町",
            "南小国町",
            "小国町",
            "産山村",
            "高森町",
            "西原村",
            "南阿蘇村",
            "御船町",
            "嘉島町",
            "益城町",
            "甲佐町",
            "山都町",
            "氷川町",
            "芦北町",
            "津奈木町",
            "錦町",
            "多良木町",
            "湯前町",
            "水上村",
            "相良村",
            "五木村",
            "山江村",
            "球磨村",
            "あさぎり町",
            "苓北町",
            "熊本市中央区",
            "熊本市東区",
            "熊本市西区",
            "熊本市南区",
            "熊本市北区",                  
        ]


    #
    # Test Level:1
    #
    def test_n_to_prefecture(self):
        n_to_prefecture = ja.n_to_prefecture()
        assert len(n_to_prefecture) == 47
        assert n_to_prefecture['2'] == '青森県'

        assert ja.n_to_prefecture(n='') == {}

        assert ja.n_to_prefecture(n='1') == {'1': '北海道'}
        assert ja.n_to_prefecture(prefecture='北海道') == {'1': '北海道'}
        assert ja.n_to_prefecture(n='1', prefecture='北海道') == {'1': '北海道'}


    def test_nn_to_prefecture(self):
        nn_to_prefecture = ja.nn_to_prefecture()
        assert len(nn_to_prefecture) == 47
        assert nn_to_prefecture['47'] == '沖縄県'

        assert ja.nn_to_prefecture(nn='') == {}

        assert ja.nn_to_prefecture(nn='01') == {'01': '北海道'}
        assert ja.nn_to_prefecture(prefecture='北海道') == {'01': '北海道'}
        assert ja.nn_to_prefecture(nn='01', prefecture='北海道') == {'01': '北海道'}


    def test_prefecture_code_to_prefecture(self):
        prefecture_code_to_prefecture = ja.prefecture_code_to_prefecture()
        assert len(prefecture_code_to_prefecture) == 47
        assert prefecture_code_to_prefecture['47'] == '沖縄県'

        assert ja.prefecture_code_to_prefecture(pref_code='') == {}

        assert ja.prefecture_code_to_prefecture(pref_code='01') == {'01': '北海道'}
        assert ja.prefecture_code_to_prefecture(prefecture='北海道') == {'01': '北海道'}
        assert ja.prefecture_code_to_prefecture(pref_code='01', prefecture='北海道') == {'01': '北海道'}


    def test_city_code_to_city(self):
        city_code_to_city = ja.city_code_to_city(prefecture="北海道")
        assert len(city_code_to_city) == 179
        assert city_code_to_city["1002"] == "札幌市"

        city_code_to_city = ja.city_code_to_city(prefecture="")
        assert city_code_to_city == {}

        city_code_to_city = ja.city_code_to_city(prefecture="北海道", city_code="1002", city="札幌市")
        assert city_code_to_city == {"1002": "札幌市"}
        
        city_code_to_city = ja.city_code_to_city(prefecture="熊本県", city="熊本市中央区", designated=True)
        assert city_code_to_city == {
            "1010": "熊本市中央区",
        }


    def test_local_government_code_to_city(self):
        local_government_code_to_city = ja.local_government_code_to_city()
        assert len(local_government_code_to_city) == 1741
        assert local_government_code_to_city["011002"] == "札幌市"

        local_government_code_to_city = ja.local_government_code_to_city(prefecture="")
        assert local_government_code_to_city == {}

        local_government_code_to_city = ja.local_government_code_to_city(lg_code="011002", city="札幌市")
        assert local_government_code_to_city == {"011002": "札幌市"}

        local_government_code_to_city = ja.local_government_code_to_city(prefecture="熊本県", city="熊本市中央区", designated=True)
        assert local_government_code_to_city == {
            "431010": "熊本市中央区",
        }


    def test_local_government_code_to_prefecture_city(self):
        local_government_code_to_prefecture_city = ja.local_government_code_to_prefecture_city()
        assert len(local_government_code_to_prefecture_city) == 1741
        assert local_government_code_to_prefecture_city["011002"] == "北海道札幌市"

        local_government_code_to_prefecture_city = ja.local_government_code_to_prefecture_city(prefecture="")
        assert local_government_code_to_prefecture_city == {}

        local_government_code_to_prefecture_city = ja.local_government_code_to_prefecture_city(lg_code="011002", city="札幌市")
        assert local_government_code_to_prefecture_city == {"011002": "北海道札幌市"}

        local_government_code_to_prefecture_city = ja.local_government_code_to_prefecture_city(prefecture="熊本県", city="熊本市中央区", designated=True)
        assert local_government_code_to_prefecture_city == {
            "431010": "熊本県熊本市中央区",
        }


    def test_prefecture_country_to_country(self):
        dict0 = self.prefecture_country_to_country
        dict1 = ja.prefecture_country_to_country()

        assert len(dict0) == len(dict1)

        for key, value in dict0.items():
            # print(key, value)
            assert value == dict1[key]

        for key, value in dict1.items():
            assert value == dict0[key]

        assert dict0 == dict1

        dict1 = ja.prefecture_country_to_country(prefecture="")
        assert dict1 == {}

        dict1 = ja.prefecture_country_to_country(prefecture="福井県")
        assert dict1 == {
            "福井県吉田郡": "吉田郡",
            "福井県今立郡": "今立郡",
            "福井県南条郡": "南条郡",
            "福井県丹生郡": "丹生郡",
            "福井県三方郡": "三方郡",
            "福井県大飯郡": "大飯郡",
            "福井県三方上中郡": "三方上中郡",
        }

        dict1 = ja.prefecture_country_to_country(prefecture="福井県", country="吉田郡")
        assert dict1 == {
            "福井県吉田郡": "吉田郡",
        }


    def test_prefecture_city_to_city(self):
        dict0 = self.prefecture_city_to_city
        dict1 = ja.prefecture_city_to_city()

        assert len(dict0) == len(dict1)

        for key, value in dict0.items():
            # print(key, value)
            assert value == dict1[key]

        for key, value in dict1.items():
            assert value == dict0[key]

        assert dict0 == dict1

        dict1 = ja.prefecture_city_to_city(prefecture="")
        assert dict1 == {}

        dict1 = ja.prefecture_city_to_city(prefecture="福井県")
        assert dict1 == {
            "福井県福井市": "福井市",
            "福井県敦賀市": "敦賀市",
            "福井県小浜市": "小浜市",
            "福井県大野市": "大野市",
            "福井県勝山市": "勝山市",
            "福井県鯖江市": "鯖江市",
            "福井県あわら市": "あわら市",
            "福井県越前市": "越前市",
            "福井県坂井市": "坂井市",

            "福井県永平寺町": "永平寺町",
            "福井県池田町": "池田町",
            "福井県南越前町": "南越前町",
            "福井県越前町": "越前町",
            "福井県美浜町": "美浜町",
            "福井県高浜町": "高浜町",
            "福井県おおい町": "おおい町",
            "福井県若狭町": "若狭町",

        }

        dict1 = ja.prefecture_city_to_city(prefecture="福井県", city="福井市")
        assert dict1 == {
            "福井県福井市": "福井市",
        }

        dict1 = ja.prefecture_city_to_city(prefecture="熊本県", city="熊本市中央区", designated=True)
        assert dict1 == {"熊本県熊本市中央区": "熊本市中央区"}


    #
    # Test Level:2
    #
    def test_extract_prefecture(self):
        for i in range(len(address_list)):
            pref = ja.extract_prefecture(address_list[i])
            assert pref == pref_list[i]


    def test_extract_country(self):
        for i in range(len(address_list)):
            pref, country = ja.extract_country(address_list[i])
            assert pref == pref_list[i]
            assert country == country_list[i]


    def test_extract_city(self):
        for i in range(len(address_list)):
            pref, city = ja.extract_city(address_list[i])
            assert pref == pref_list[i]
            assert city == city_list[i]

        pref, city = ja.extract_city("千葉県千葉市中央区青葉1の1の1", designated=True)
        assert city == "千葉市中央区"

    def test_extract_details(self):
        for i in range(len(address_list)):
            pref, city, details = ja.extract_details(address_list[i])
            assert pref == pref_list[i]
            assert city == city_list[i]
            assert details == details_list[i]

        pref, city, details = ja.extract_details("千葉県千葉市中央区青葉1の1の1", designated=True)
        assert city == "千葉市中央区"
        assert details == "青葉1の1の1"
    #
    # Utils
    #
    def test_resolve_prefecture(self):
        assert ja.resolve_prefecture("渋谷区代々木２－２－２") == "東京都"


    def test_normalize_address(self):
        address = ja.normalize_address("東京都渋谷区代々木２－２－２")
        assert address == "東京都渋谷区代々木２－２－２"

        address = ja.normalize_address("東京都渋谷区代々木２丁目２番２号")
        assert address == "東京都渋谷区代々木２－２－２"

        address = ja.normalize_address("東京都港区六本木二十一丁目二番二号")
        assert address == "東京都港区六本木２１－２－２"


    def test_compare_address(self):
        addr1 = "東京都渋谷区代々木２丁目２番２号"
        addr2 = "東京都渋谷区代々木２－２－２"

        assert ja.compare_address(addr1, addr2) == 100

