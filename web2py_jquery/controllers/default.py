#coding: utf8

UNSELECTED_ID   = '__unselected__'
UNSELECTED_TEXT = T('Please select')

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

    def get_cities(self, country):
        return map_countries_to_cities.get(country)

    def get_phones(self, country, city):
        return map_countries_cities_to_tels.get((country, city))

# The ids of the html elements
COUNTRY_ID    = 'country'
CITY_ID       = 'city'
CITIES_DIV_ID = 'citiesdiv'
PHONE_ID      = 'phone'
PHONES_DIV_ID = 'phonesdiv'

def get_select(el_id, options, value, f = None, target = None, sources = None, clear_target = None):
    if options:
        try:
            opts     = [OPTION(v, _value=k) for k, v in options.items()]
        except:
            opts     = [OPTION(v, _value=v) for v in options]
    else:
        opts = []
    opts.append(OPTION(UNSELECTED_TEXT, _value=UNSELECTED_ID))
    if f != None:
        sources  = ["'%s'" % source for source in sources]
        sources  = "[%s]" % (",".join(sources))
        onchange = "ajax('%s',%s,'%s');" % (URL(f), sources, target)
        if clear_target:
            reset_select = """$('#%s').empty().append('<option selected="selected" value="%s">%s</option>');""" % (clear_target, UNSELECTED_ID, UNSELECTED_TEXT)
            onchange += reset_select
    else:
        onchange = None
    if not value: value = UNSELECTED_ID
    return SELECT(_id       = el_id,
                  _name     = el_id,  # I do not know why, but I need this
                  value     = value,
                  _onchange = onchange,
                  *opts)

def countries_select(countries, selected_country = None):
    return get_select(value = selected_country, options = countries, el_id = COUNTRY_ID, f = 'get_cities', target = CITIES_DIV_ID, sources = [COUNTRY_ID], clear_target = PHONE_ID)

def cities_select(cities, selected_city = None ):
    return get_select(value = selected_city, options = cities, el_id = CITY_ID, f = 'get_tels', target = PHONES_DIV_ID, sources = [COUNTRY_ID, CITY_ID])

def phones_select(phones, selected_phone = None):
    return get_select(value = selected_phone, options = phones, el_id = PHONE_ID)

def index():
    selected_country = None
    cities           = Data().get_cities(selected_country)
    selected_city    = None
    phones           = Data().get_phones(selected_country, selected_city)
    selected_phone   = None
    form = FORM(countries_select(countries, selected_country),
                DIV(cities_select(cities, selected_city), _id=CITIES_DIV_ID),
                DIV(phones_select(phones, selected_phone), _id=PHONES_DIV_ID)
                )
    return dict(form = form)

def get_cities():
    cities = Data().get_cities(request.vars.country)
    return cities_select(cities).xml()

def get_tels():
    phones = Data().get_phones(request.vars.country, request.vars.city)
    return phones_select(phones).xml()
