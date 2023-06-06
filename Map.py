import requests
import xml.etree.ElementTree as ET
import folium
from folium.plugins import MarkerCluster
import API_Key

class Map:
    def __init__(self):
        self.m = None
        self.theaters = [] # 영화관 정보를 저장할 리스트

    def get_city_list(self):
        city_list = [
            "수원시", "성남시", "고양시", "용인시", "부천시", "안산시", "안양시", "남양주시", "화성시", "평택시",
            "의정부시", "시흥시", "파주시", "광명시", "김포시", "군포시", "광주시", "이천시", "양주시", "오산시",
            "구리시", "남양주시", "양평시", "여주시", "안성시", "포천시", "의왕시", "하남시"
        ]  

        return city_list

    def parse_theater_data(self, xml_data):
        theaters = []
        root = ET.fromstring(xml_data)

        for row in root.findall('row'):
            theater = {}
            theater['SIGUN_NM'] = row.find('SIGUN_NM').text
            theater['BIZPLC_NM'] = row.find('BIZPLC_NM').text
            theater['LICENSG_DE'] = row.find('LICENSG_DE').text
            theater['BSN_STATE_NM'] = row.find('BSN_STATE_NM').text
            theater['REFINE_LOTNO_ADDR'] = row.find('REFINE_LOTNO_ADDR').text
            theater['REFINE_ROADNM_ADDR'] = row.find('REFINE_ROADNM_ADDR').text
            theater['REFINE_ZIP_CD'] = row.find('REFINE_ZIP_CD').text
            theater['REFINE_WGS84_LOGT'] = float(row.find('REFINE_WGS84_LOGT').text)
            theater['REFINE_WGS84_LAT'] = float(row.find('REFINE_WGS84_LAT').text)
            theaters.append(theater)

        return theaters

    def get_theater_info(self, selected_city):
        headers = {
            'KEY': API_Key.theater_api_key,
            'Type': 'xml',
            'pIndex': '1',
            'pSize': '100',
        }

        url = 'https://openapi.gg.go.kr/MovieTheater'

        params = {'SIGUN_NM': selected_city}

        response = requests.get(url, headers=headers, params=params)

        # 요청 상태 코드 확인
        if response.status_code == 200:
            print("요청이 성공적으로 수행되었습니다.")
            xml_data = response.text

            # XML 데이터 파싱
            theaters = self.parse_theater_data(xml_data)

            # 지도 생성
            self.m = folium.Map(location=[37.3402849, 126.7313189], zoom_start=13)

            self.marker_cluster = MarkerCluster()

            # 각 영화관 정보 추출
            for theater in theaters:
                self.theaters.append(theater)

                print('SIGUN_NM:', theater['SIGUN_NM'])
                print('BIZPLC_NM:', theater['BIZPLC_NM'])
                print('LICENSG_DE:', theater['LICENSG_DE'])
                print('BSN_STATE_NM:', theater['BSN_STATE_NM'])
                print('REFINE_LOTNO_ADDR:', theater['REFINE_LOTNO_ADDR'])
                print('REFINE_ROADNM_ADDR:', theater['REFINE_ROADNM_ADDR'])
                print('REFINE_ZIP_CD:', theater['REFINE_ZIP_CD'])
                print('REFINE_WGS84_LOGT:', theater['REFINE_WGS84_LOGT'])
                print('REFINE_WGS84_LAT:', theater['REFINE_WGS84_LAT'])
                print()
                '''
                # 지도에 마커 추가
                folium.Marker(
                    location=[theater['REFINE_WGS84_LAT'], theater['REFINE_WGS84_LOGT']],
                    popup=theater['BIZPLC_NM'],
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(self.m)
                '''
                self.marker_cluster.add_child(
                    # 지도에 마커 추가
                    folium.Marker(
                        location=[theater['REFINE_WGS84_LAT'], theater['REFINE_WGS84_LOGT']],
                        popup=theater['BIZPLC_NM'],
                        icon=folium.Icon(color='red', icon='info-sign')
                    )
                )
                
            # 마커 클러스터 생성 및 마커 추가
            self.m.add_child(self.marker_cluster)

            # 지도를 HTML 파일로 저장
            self.m.save('map.html')

            print("영화관 정보를 지도에 표시한 HTML 파일이 생성되었습니다.")

        else:
            print(f"요청이 실패하였습니다. 상태 코드: {response.status_code}")
                