import requests
import json

lat = 35.8105056935149   # 위도
lng = 127.102527553171   # 경도
page_id = 31081  # 가게 고유명사


class Crawling:
    def __init__(self) -> None:
        self.s = requests.Session()
        self.s.headers.update({
            'x-apikey' : 'iphoneap',
            'x-apisecret' : 'fe5183cc3dea12bd0ce299cf110a75a2' #F12로 찾아야함
        })
        #self.dict_to_json_file()
        self.get_page_id_list()

    def get_response_json_data(self, url):
        """API URL -> JSON -> DICT"""
        r = self.s.get(url)
        response_str = r.content.decode('UTF-8')
        return json.loads(response_str) ## dict

    def dict_to_json_file(self):
        crawl_data = []
        restaurant_api_url = f'https://www.yogiyo.co.kr/api/v1/restaurants/{page_id}/?lat={lat}&lng={lng}'
        restaurant_info_api_url = f'https://www.yogiyo.co.kr/api/v1/restaurants/{page_id}/info/'

        restaurant_data = {
            #'restaurant_result' : self.get_response_json_data(restaurant_api_url),
            'restaurant_info_result' : self.get_response_json_data(restaurant_info_api_url)
        }

        crawl_data.append(restaurant_data)

        with open('yogiyo_data_for_parsing.json', 'w', encoding='utf-8') as file:
            print(json.dump(crawl_data, file, ensure_ascii=False, indent='\t'))

    def get_page_id_list(self):
        """레스토랑 ID 리스트"""
        crawl_data = []
        restaurant_list_url = f'https://www.yogiyo.co.kr/api/v1/restaurants-geo/?items=450&lat={lat}&lng={lng}&order=rank&page=0&search='
        restaurant_list_results = self.get_response_json_data(restaurant_list_url)['restaurants']

        #list_info_dict = {restaurant_dict['id']: restaurant_dict for restaurant_dict in restaurant_list_results}
        #restaurant_dict['~']에 들어가는걸로 이름을 정함

        crawl_data.append(restaurant_list_results)
        #crawl_data.append(list_info_dict)

        with open('yogiyo_data_for_parsing.json', 'w', encoding='utf-8') as file:
            print(json.dump(crawl_data, file, ensure_ascii=False, indent='\t'))