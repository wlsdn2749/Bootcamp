import requests
import json
from .models import Rest, Review

lat = 35.81708   # 위도
lng = 127.09063   # 경도
# 전주대 후문

class Crawling:
    def __init__(self) -> None:
        self.s = requests.Session()
        self.s.headers.update({
            'x-apikey' : 'iphoneap',
            'x-apisecret' : 'fe5183cc3dea12bd0ce299cf110a75a2' #F12로 찾아야함
        })
       # self.dict_to_json_file()
        # self.get_page_id_list()
        self.json_crawl()

    def json_crawl(self):
        """웹에서 크롤링 -> yogiyo_data_for_parsing.json파일로 저장"""
        list_info_dict = self.get_page_id_list()
        self.dict_to_json_file(list_info_dict)

    def get_response_json_data(self, url):
        """API URL -> JSON -> DICT"""
        r = self.s.get(url)
        response_str = r.content.decode('UTF-8')
        return json.loads(response_str) ## dict

    def dict_to_json_file(self, list_info_dict):
        crawl_data = []
        for page_id in list_info_dict.keys():
            restaurant_api_url = f'https://www.yogiyo.co.kr/api/v1/restaurants/{page_id}/?lat={lat}&lng={lng}'
            restaurant_info_api_url = f'https://www.yogiyo.co.kr/api/v1/restaurants/{page_id}/info/'
            review_api_url = f'https://www.yogiyo.co.kr/api/v1/reviews/{page_id}/?count=30&only_photo_review=false&page=1&sort=time'
            menu_api_url = f'https://www.yogiyo.co.kr/api/v1/restaurants/{page_id}/menu/?add_photo_menu=android&add_one_dish_menu=true&order_serving_type=delivery'
            avgrating_url = f'https://www.yogiyo.co.kr/review/restaurant/{page_id}/avgrating/'

            restaurant_data = {
            #    'list_info': list_info_dict[page_id],
                 'restaurant_results': self.get_response_json_data(restaurant_api_url),
            #    'restaurant_info_results': self.get_response_json_data(restaurant_info_api_url),
                 'review_results': self.get_response_json_data(review_api_url),
            #    'menu_results': self.get_response_json_data(menu_api_url),
            #    'avgrating_results': self.get_response_json_data(avgrating_url),
            }

            crawl_data.append(restaurant_data)

        with open('yogiyo_data_for_parsing.json', 'w', encoding='utf-8') as file:
            print(json.dump(crawl_data, file, ensure_ascii=False, indent='\t'))

        return self.json_parsing()

    def get_page_id_list(self):
        """레스토랑 ID 리스트"""
        restaurant_list_url = f'https://www.yogiyo.co.kr/api/v1/restaurants-geo/?items=100&lat={lat}&lng={lng}&order=rank&page=0&search='
        restaurant_list_results = self.get_response_json_data(restaurant_list_url)['restaurants']

        list_info_dict = {restaurant_dict['id']: restaurant_dict for restaurant_dict in restaurant_list_results}

        return list_info_dict

    def json_parsing(self):
        '''yogiyo_data_for_parsing.json파일에서 파싱에서 DB에 모델링 하는 함수'''
        with open('yogiyo_data_for_parsing.json', 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        for restaurant_data in json_data:
        #for i in range(126, len(json_data)):
            #restaurant_data = json_data[i]
            restaurant_results = restaurant_data['restaurant_results']
            review_results = restaurant_data['review_results']

            restaurant = self.restaurant_parsing(restaurant_results)
            self.review_parsing(review_results, restaurant)

    def restaurant_parsing(self, restaurant_results):
        #레스토랑 정보 db modeling
        name = restaurant_results['name']
        lat = restaurant_results['lat']
        lng = restaurant_results['lng']
        review_count = restaurant_results['review_count']
        review_avg = restaurant_results['review_avg']

        restaurant = Rest(
            rest_name = name,
            rest_star = review_avg,
            rest_location_lat = lat,
            rest_location_lon = lng,
            rest_number_reviews = review_count
        )
        restaurant.save()
        return restaurant

    def review_parsing(self, review_results, restaurant):
        for i in range(5):
            try:
                review_dict = review_results[i]
            except IndexError:
                break

            try :
                slash = review_dict['menu_summary'].find('/')
            except :
                slash = 100

            review = Review(
                restaurant=restaurant,
                comment = review_dict['comment'][:298],
                rating=review_dict['rating'],
                menu_name=review_dict['menu_summary'][:slash],
                like_count=review_dict['like_count'],
            )
            review.save()

