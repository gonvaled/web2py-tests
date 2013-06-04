#coding: utf8

countries = {
    'DE': 'Germany',
    'ES': 'Spain',
}

MAD_ID = 'MAD'
BCN_ID = 'BCN'
CAC_ID = 'CAC'
BER_ID = 'BER'
DUS_ID = 'DUS'
MUN_ID = 'MUN'

map_countries_to_cities = {
    'ES': { MAD_ID: 'Madrid',  BCN_ID: 'Barcelona',   CAC_ID: u'Cáceres'},
    'DE': { BER_ID: 'Berlin',  DUS_ID: u'Düsseldorf', MUN_ID: u'München'},
}

map_countries_cities_to_tels = {
    ('ES', MAD_ID) : [ '+3491423432', '+34913223432' ],
    ('ES', BCN_ID) : [ '+3493423432', '+34933223432' ],
    ('ES', CAC_ID) : [ '+3497423432', '+34973223432' ],
    ('DE', BER_ID) : [ '+4991423432', '+49913223432' ],
    ('DE', DUS_ID) : [ '+4993423432', '+49933223432' ],
    ('DE', MUN_ID) : [ '+4997423432', '+49973223432' ],
    }

class Data:

    def get_countries(self):
        return countries

    def get_cities(self, country):
        return map_countries_to_cities.get(country)

    def get_phones(self, country, city):
        log.error('Getting phones for country %s and city %s', country, city)
        return map_countries_cities_to_tels.get((country, city))

