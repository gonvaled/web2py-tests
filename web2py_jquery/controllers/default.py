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

def get_select(el_id, options, value, f = None, target = None, sources = None):
    try:
        opts     = [OPTION(v, _value=k) for k, v in options.items()]
    except:
        opts     = [OPTION(v, _value=v) for v in options]
    if f != None:
        sources  = ["'%s'" % source for source in sources]
        sources  = "[%s]" % (",".join(sources))
        onchange = "ajax('%s',%s,'%s');" % (URL(f), sources, target)
    else:
        onchange = None
    return SELECT(_id       = el_id,
                  _name     = el_id,  # I do not know why, but I need this
                  value     = value,
                  _onchange = onchange,
                  *opts)

def countries_select(selected_country, countries):
    return get_select(value = selected_country, options = countries, el_id = 'country', f = 'get_cities', target = 'citiesdiv',  sources = ['country'])

def cities_select(selected_city, cities):
    return get_select(value = selected_city, options = cities, el_id = 'city', f = 'get_tels', target = 'phonesdiv', sources = ['country', 'city'])

def phones_select(selected_phone, phones):
    return get_select(value = selected_phone, options = phones, el_id = 'phone')

def index():
    selected_country = 'ES'
    cities           = map_countries_to_cities[selected_country]
    selected_city    = cities.keys()[0] # TODO: this is not deterministic
    phones           = map_countries_cities_to_tels[(selected_country, selected_city)]
    selected_phone   = phones[0]
    form = FORM(countries_select(selected_country, countries),
                DIV(cities_select(selected_city, cities), _id='citiesdiv'),
                DIV(phones_select(selected_phone, phones), _id='phonesdiv')
                )
    return dict(form = form)

def get_cities():
    cities = map_countries_to_cities[request.vars.country]
    selected_city = cities.keys()[0] # TODO: this is not deterministic
    return cities_select(selected_city, cities).xml()

def get_tels():
    country = request.vars.country
    city    = request.vars.city
    key     = (country, city)
    phones  = map_countries_cities_to_tels[key]
    selected_phone = phones[0]
    return phones_select(selected_phone, phones).xml()
