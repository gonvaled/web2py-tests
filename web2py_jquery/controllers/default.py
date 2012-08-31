from mydata import Data

# The ids of the html elements
HTML_ID_PREFIX = 'aaa'
COUNTRY_ID     = HTML_ID_PREFIX + 'telcountry'
CITY_ID        = HTML_ID_PREFIX + 'telcity'
CITIES_DIV_ID  = HTML_ID_PREFIX + 'telcitiesdiv'
PHONE_ID       = HTML_ID_PREFIX + 'telphone'
PHONES_DIV_ID  = HTML_ID_PREFIX + 'telphonesdiv'

# Unselected entry
UNSELECTED_ID   = '__unselected__'
UNSELECTED_TEXT = T('Please select')

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
    countries        = Data().get_countries()
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
    cities = Data().get_cities(request.vars[COUNTRY_ID])
    return cities_select(cities).xml()

def get_tels():
    phones = Data().get_phones(request.vars[COUNTRY_ID], request.vars[CITY_ID])
    return phones_select(phones).xml()

