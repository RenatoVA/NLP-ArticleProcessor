from transformers import AutoTokenizer, AutoModelForTokenClassification
import procesing_pdf as pp

tokenizer = AutoTokenizer.from_pretrained("ml6team/bert-base-uncased-city-country-ner")

model = AutoModelForTokenClassification.from_pretrained("ml6team/bert-base-uncased-city-country-ner")

from transformers import pipeline
nlp = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

country_to_region = {
    "afghanistan": "South Asia",
    "albania": "Europe and Central Asia",
    "algeria": "Middle East and North Africa",
    "andorra": "Europe and Central Asia",
    "angola": "Africa",
    "uk": "Europe and Central Asia",
    "argentina": "Latin America and Caribbean",
    "armenia": "Europe and Central Asia",
    "australia": "East Asia and Pacific",
    "austria": "Europe and Central Asia",
    "azerbaijan": "Europe and Central Asia",
    "bahamas": "Latin America and Caribbean",
    "bahrain": "Middle East and North Africa",
    "bangladesh": "South Asia",
    "barbados": "Latin America and Caribbean",
    "belarus": "Europe and Central Asia",
    "belgium": "Europe and Central Asia",
    "belize": "Latin America and Caribbean",
    "benin": "Africa",
    "bhutan": "South Asia",
    "bolivia": "Latin America and Caribbean",
    "bosnia and Herzegovina": "Europe and Central Asia",
    "botswana": "Africa",
    "brazil": "Latin America and Caribbean",
    "brunei": "East Asia and Pacific",
    "bulgaria": "Europe and Central Asia",
    "burkina faso": "Africa",
    "burundi": "Africa",
    "cambodia": "East Asia and Pacific",
    "cameroon": "Africa",
    "canada": "North America",
    "cape verde": "Africa",
    "central african republic": "Africa",
    "chad": "Africa",
    "chile": "Latin America and Caribbean",
    "china": "East Asia and Pacific",
    "colombia": "Latin America and Caribbean",
    "comoros": "Africa",
    "congo": "Africa",
    "costa rica": "Latin America and Caribbean",
    "croatia": "Europe and Central Asia",
    "cuba": "Latin America and Caribbean",
    "cyprus": "Europe and Central Asia",
    "czech republic": "Europe and Central Asia",
    "denmark": "Europe and Central Asia",
    "djibouti": "Africa",
    "dominica": "Latin America and Caribbean",
    "dominican republic": "Latin America and Caribbean",
    "east timor": "East Asia and Pacific",
    "ecuador": "Latin America and Caribbean",
    "egypt": "Middle East and North Africa",
    "el salvador": "Latin America and Caribbean",
    "equatorial guinea": "Africa",
    "eritrea": "Africa",
    "estonia": "Europe and Central Asia",
    "eswatini": "Africa",
    "ethiopia": "Africa",
    "fiji": "East Asia and Pacific",
    "finland": "Europe and Central Asia",
    "france": "Europe and Central Asia",
    "gabon": "Africa",
    "gambia": "Africa",
    "georgia": "Europe and Central Asia",
    "germany": "Europe and Central Asia",
    "ghana": "Africa",
    "greece": "Europe and Central Asia",
    "grenada": "Latin America and Caribbean",
    "guatemala": "Latin America and Caribbean",
    "guinea": "Africa",
    "guinea-bissau": "Africa",
    "guyana": "Latin America and Caribbean",
    "haiti": "Latin America and Caribbean",
    "honduras": "Latin America and Caribbean",
    "hungary": "Europe and Central Asia",
    "iceland": "Europe and Central Asia",
    "india": "South Asia",
    "indonesia": "East Asia and Pacific",
    "iran": "Middle East and North Africa",
    "iraq": "Middle East and North Africa",
    "ireland": "Europe and Central Asia",
    "israel": "Middle East and North Africa",
    "italy": "Europe and Central Asia",
    "jamaica": "Latin America and Caribbean",
    "japan": "East Asia and Pacific",
    "jordan": "Middle East and North Africa",
    "kazakhstan": "Europe and Central Asia",
    "kenya": "Africa",
    "kiribati": "East Asia and Pacific",
    "north korea": "East Asia and Pacific",
    "south korea": "East Asia and Pacific",
    "kuwait": "Middle East and North Africa",
    "kyrgyzstan": "Europe and Central Asia",
    "laos": "East Asia and Pacific",
    "latvia": "Europe and Central Asia",
    "lebanon": "Middle East and North Africa",
    "lesotho": "Africa",
    "liberia": "Africa",
    "libya": "Middle East and North Africa",
    "liechtenstein": "Europe and Central Asia",
    "lithuania": "Europe and Central Asia",
    "luxembourg": "Europe and Central Asia",
    "madagascar": "Africa",
    "malawi": "Africa",
    "malaysia": "East Asia and Pacific",
    "maldives": "South Asia",
    "mali": "Africa",
    "malta": "Europe and Central Asia",
    "marshall Islands": "East Asia and Pacific",
    "mauritania": "Africa",
    "mauritius": "Africa",
    "mexico": "Latin America and Caribbean",
    "micronesia": "East Asia and Pacific",
    "moldova": "Europe and Central Asia",
    "monaco": "Europe and Central Asia",
    "mongolia": "East Asia and Pacific",
    "montenegro": "Europe and Central Asia",
    "morocco": "Middle East and North Africa",
    "mozambique": "Africa",
    "myanmar": "East Asia and Pacific",
    "namibia": "Africa",
    "nauru": "East Asia and Pacific",
    "nepal": "South Asia",
    "netherlands": "Europe and Central Asia",
    "new zealand": "East Asia and Pacific",
    "nicaragua": "Latin America and Caribbean",
    "niger": "Africa",
    "nigeria": "Africa",
    "norway": "Europe and Central Asia",
    "oman": "Middle East and North Africa",
    "pakistan": "South Asia",
    "palau": "East Asia and Pacific",
    "panama": "Latin America and Caribbean",
    "papua new guinea": "East Asia and Pacific",
    "paraguay": "Latin America and Caribbean",
    "peru": "Latin America and Caribbean",
    "philippines": "East Asia and Pacific",
    "poland": "Europe and Central Asia",
    "portugal": "Europe and Central Asia",
    "qatar": "Middle East and North Africa",
    "romania": "Europe and Central Asia",
    "russia": "Europe and Central Asia",
    "rwanda": "Africa",
    "saint kitts and Nevis": "Latin America and Caribbean",
    "saint lucia": "Latin America and Caribbean",
    "saint vincent and the Grenadines": "Latin America and Caribbean",
    "samoa": "East Asia and Pacific",
    "san marino": "Europe and Central Asia",
    "sao tome and Principe": "Africa",
    "saudi arabia": "Middle East and North Africa",
    "senegal": "Africa",
    "serbia": "Europe and Central Asia",
    "seychelles": "Africa",
    "sierra leone": "Africa",
    "singapore": "East Asia and Pacific",
    "slovakia": "Europe and Central Asia",
    "slovenia": "Europe and Central Asia",
    "solomon Islands": "East Asia and Pacific",
    "somalia": "Africa",
    "south africa": "Africa",
    "south sudan": "Africa",
    "spain": "Europe and Central Asia",
    "sri lanka": "South Asia",
    "sudan": "Africa",
    "suriname": "Latin America and Caribbean",
    "sweden": "Europe and Central Asia",
    "switzerland": "Europe and Central Asia",
    "syria": "Middle East and North Africa",
    "taiwan": "East Asia and Pacific",
    "tajikistan": "Europe and Central Asia",
    "tanzania": "Africa",
    "thailand": "East Asia and Pacific",
    "togo": "Africa",
    "tonga": "East Asia and Pacific",
    "trinidad and Tobago": "Latin America and Caribbean",
    "tunisia": "Middle East and North Africa",
    "turkey": "Europe and Central Asia",
    "turkmenistan": "Europe and Central Asia",
    "tuvalu": "East Asia and Pacific",
    "uganda": "Africa",
    "ukraine": "Europe and Central Asia",
    "united arab emirates": "Middle East and North Africa",
    "united kingdom": "Europe and Central Asia",
    "united states": "North America",
    "uruguay": "Latin America and Caribbean",
    "uzbekistan": "Europe and Central Asia",
    "vanuatu": "East Asia and Pacific",
    "vatican city": "Europe and Central Asia",
    "venezuela": "Latin America and Caribbean",
    "vietnam": "East Asia and Pacific",
    "yemen": "Middle East and North Africa",
    "zambia": "Africa",
    "zimbabwe": "Africa"
}

all_regions = ['Africa', 'East Asia and Pacific','Europe and Central Asia','Latin America and Caribbean', 
               'Middle East and North Africa', 'North America', 'South Asia']
def get_region(country):
    return country_to_region.get(country, "Unknown")

def get_locations(text):
    locations_comments=''
    countries=[]
    cities=[]
    locations = pp.extract_locations(text)
    #text_locations=','.join(locations)
    #print("text_locations",text_locations)
    for location in locations:
        if get_region(location) != "Unknown":
            countries.append(location)
    if'georgia' in countries:
        locations_comments+='georgia_present'
    countries = list(set(countries))
    regions = [get_region(country) for country in countries]
    regions = list(set(regions))
    '''
    entities = nlp(text)
    print("entities",entities)
    for entity in entities:
       if entity['entity_group'] == 'COUNTRY':
          countries.append(entity['word'])
       if entity['entity_group'] == 'CITY':
          cities.append(entity['word'])
    
    regions = [get_region(country) for country in countries]
    regions = list(set(regions))
    '''
    one_hot_encoding = [0] * len(all_regions)
    for i, region in enumerate(all_regions):
        if region in regions:
            one_hot_encoding[i] = 1
    countries_string=';'.join(countries)
    return one_hot_encoding,countries_string,locations_comments

