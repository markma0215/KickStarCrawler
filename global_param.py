
from geopy.geocoders import Nominatim
import pycountry
import dryscrape
from bs4 import BeautifulSoup
import csv
import os
from paramError import ParamError
import requests

k10_k100_StartLink = "https://www.kickstarter.com/discover/advanced?category_id=33&goal=2&sort=end_date&seed=2519709&page=2"


threshold = 4
page = 53
projID = 27624

eachProj = ""
session = dryscrape.Session()
geolocator = Nominatim()


varNameList = ["Identifier", "Project Name", "Campaign Webpage", "Projects We Love (0/1)",
               "City", "State/Province", 'Country', 'Category', '# Updates', '# Comments',
               'Project Description (No Bold Title, No Pic/Doc/, No table/figure description, No website Links)',
               'Goal', 'Pledged', 'Currency', 'Minimum Pledge', 'Maximum Pledge', 'Num. Backers',
               'Funding Start (Date Format)', 'Funding End (Date Format)', 'Duration', 'Project Creator',
               '# Projects Created', '# Projects Backed', 'Identity', 'First Name', 'Last Name',
               '# Websites', 'Facebook (0/1)', '# FB Friends', 'Project Creator Link', 'Joined (Date Format)', '# Creator Comments',
               'Biography Description (No Bold Title, No Pic/Doc/, No table/figure description, No website Links)']

countryMap = {
    "UK": ['GB'.encode('utf-8'), 'GBP'.encode('utf-8')],
    'United States of America': ['US'.encode('utf-8'), 'USD'.encode('utf-8')],
    'Switzerland': ['CH'.encode('utf-8'), 'CHF'.encode('utf-8')],
    'Canada': ['CA'.encode('utf-8'), 'CAD'.encode('utf-8')],
    'Taiwan': ['TW'.encode('utf-8'), 'TWD'.encode('utf-8')],
    'Germany': ['DE'.encode('utf-8'), 'EUR'.encode('utf-8')],
    'Italy': ['IT'.encode('utf-8'), 'EUR'.encode('utf-8')],
    'Hong Kong': ['HK'.encode('utf-8'), 'HKD'.encode('utf-8')],
    'Japan': ['JP'.encode('utf-8'), 'JPY'.encode('utf-8')],
    'France': ['FR'.encode('utf-8'), 'EUR'.encode('utf-8')],
    'Mexico': ['MX'.encode('utf-8'), 'MXN'.encode('utf-8')],
    'China': ['CN'.encode('utf-8'), 'CNY'.encode('utf-8')],
    'Spain': ['ES'.encode('utf-8'), 'EUR'.encode('utf-8')],
    'Poland': ['PL'.encode('utf-8'), 'PLN'.encode('utf-8')],
    'Denmark': ['DK'.encode('utf-8'), 'DKK'.encode('utf-8')],
    'NZ': ['NZ'.encode('utf-8'), 'NZD'.encode('utf-8')],
    'Netherlands': ['NL'.encode('utf-8'), 'EUR'.encode('utf-8')],
    'Australia': ['AU'.encode('utf-8'), 'AUD'.encode('utf-8')],
    'Ethiopia': ['ET'.encode('utf-8'), 'ETB'.encode('utf-8')],
    'Sweden': ['SE'.encode('utf-8'), 'SEK'.encode('utf-8')],
    'Brazil': ['BR'.encode('utf-8'), 'BRL'.encode('utf-8')],
    'Ukraine': ['UA'.encode('utf-8'), 'UAH'.encode('utf-8')],
    'Ghana': ['GH'.encode('utf-8'), 'GHS'.encode('utf-8')],
    'Czech Republic': ['CZ'.encode('utf-8'), 'CZK'.encode('utf-8')],
    'Czechia': ['CZ'.encode('utf-8'), 'CZK'.encode('utf-8')],
    'Serbia': ['RS'.encode('utf-8'), 'RSD'.encode('utf-8')],
    'Russia': ['RU'.encode('utf-8'), 'RUB'.encode('utf-8')],
    'Belgium': ['BE'.encode('utf-8'), 'EUR'.encode('utf-8')],
    'Pakistan': ['PK'.encode('utf-8'), 'PKR'.encode('utf-8')],
    'Greenland': ['GL'.encode('utf-8'), 'DKK'.encode('utf-8')],
    'Papua New Guinea': ['PG'.encode('utf-8', 'PGK'.encode('utf-8'))],
    'Antigua and Barbuda': ['AG'.encode('utf-8'), 'XCD'.encode('utf-8')],
    'Turkey': ['TR'.encode('utf-8'), 'TRY'.encode('utf-8')],
    'Norway': ['NO'.encode('utf-8'), 'NOK'.encode('utf-8')],
    'Bangladesh': ['BD'.encode('utf-8'), 'BDT'.encode('utf-8')],
    'Iceland': ['IS'.encode('utf-8'), 'ISK'.encode('utf-8')],
    'Austria': ['AT'.encode('utf-8'), 'EUR'.encode('utf-8')],
    'Portugal': ['PT'.encode('utf-8'), 'EUR'.encode('utf-8')],
    'Latvia': ['LV'.encode('utf-8'), 'EUR'.encode('utf-8')],
    'South Korea': ['KR'.encode('utf-8'), 'KRW'.encode('utf-8')],
    'Ireland': ['IE'.encode('utf-8'), 'EUR'.encode('utf-8')],
    'Guatemala': ['GT'.encode('utf-8'), 'GTQ'.encode('utf-8')],
    'South Africa': ['ZA'.encode('utf-8'), 'ZAR'.encode('utf-8')],
    'Indonesia': ['ID'.encode('utf-8'), 'IDR'.encode('utf-8')],
    'Israel': ['IL'.encode('utf-8'), 'ILS'.encode('utf-8')],
    'Jamaica': ['JM'.encode('utf-8'), 'JMD'.encode('utf-8')],
    'Belize': ['BZ'.encode('utf-8'), 'BZD'.encode('utf-8')],
    'Kazakhstan': ['KZ'.encode('utf-8'), 'KZT'.encode('utf-8')],
    'Argentina': ['AR'.encode('utf-8'), 'ARS'.encode('utf-8')],
    'Greece': ['GR'.encode('utf-8'), 'EUR'.encode('utf-8')],
    'India': ['IN'.encode('utf-8'), 'INR'.encode('utf-8')],
    'Nepal': ['NP'.encode('utf-8'), 'NPR'.encode('utf-8')],
    'Egypt': ['EG'.encode('utf-8'), 'EGP'.encode('utf-8')],
    'Peru': ['PE'.encode('utf-8'), 'PEN'.encode('utf-8')],
    'Bahrain': ['BH'.encode('utf-8'), 'BHD'.encode('utf-8')],
    'Bosnia and Herzegovina': ['BA'.encode('utf-8'), 'BAM'.encode('utf-8')],
    'Nigeria': ['NG'.encode('utf-8'), 'NGN'.encode('utf-8')],
    'Armenia': ['AM'.encode('utf-8'), 'AMD'.encode('utf-8')],
    'Monaco': ['MC'.encode('utf-8'), 'EUR'.encode('utf-8')],
    'Colombia': ['CO'.encode('utf-8'), 'COP'.encode('utf-8')],
    'Singapore': ['SG'.encode('utf-8'), 'SGD'.encode('utf-8')],
    'Cuba': ['CU'.encode('utf-8'), 'CUP'.encode('utf-8')],
    'Thailand': ['TH'.encode('utf-8'), 'THB'.encode('utf-8')],
    'United Arab Emirates': ['AE'.encode('utf-8'), 'AED'.encode('utf-8')],
    'Trinidad and Tobago': ['TT'.encode('utf-8'), 'TTD'.encode('utf-8')],
    'Haiti': ['HT'.encode('utf-8'), 'HTG'.encode('utf-8')],
    'Bolivia': ['BO'.encode('utf-8'), 'BOB'.encode('utf-8')],
    'North Korea': ['KP'.encode('utf-8'), 'KPW'.encode('utf-8')],
    'Afghanistan': ['AF'.encode('utf-8'), 'AFN'.encode('utf-8')],
    'Sri Lanka': ['LK'.encode('utf-8'), 'LKR'.encode('utf-8')],
    'Iraq': ['IQ'.encode('utf-8'), 'IQD'.encode('utf-8')],
    'Dominican Republic': ['DO'.encode('utf-8'), 'DOP'.encode('utf-8')],
    'Luxembourg': ['LU', 'EUR'],
    'Croatia': ['HR', 'HRK'],
    'Bahamas': ['BS', 'BSD'],
    'Cambodia': ['KH', 'KHR'],
    'Mongolia': ['MN', 'MNT'],
    'Hungary': ['HU', 'HUF'],
    'Slovenia': ['SI', 'EUR'],
    'Estonia': ['EE', 'EUR'],
    'Cyprus': ['CY', 'EUR'],
    'Puerto Rico': ['PR', 'USD'],
    'Bulgaria': ['BG', 'BGN'],
    'Romania': ['RO', 'RON'],
    'Marshall Islands': ['MH', 'USD'],
    'Iran': ['IR', 'IRR'],
    'Finland': ['FI', 'EUR'],
    'Venezuela': ['VE', 'VEF'],
    'Mali': ['ML', 'XOF'],
    'Suriname': ['SR', 'SRD'],
    'Lithuania': ['LT', 'EUR'],
    'Ecuador': ['EC', 'USD'],
    'Guadeloupe': ['GP', 'EUR'],
    "Cote d'Ivoire": ['CI', 'XOF'],
    'Slovakia': ['SK', 'EUR'],
    'Belarus': ['BY', 'BYR'],
    'Zambia': ['ZM', 'ZMW'],
    'Macedonia': ['MK', 'MKD'],
    'Malta': ['MT', 'EUR'],
    'Antarctica': ['AQ', ' '],
    'Svalbard and Jan Mayen': ['SJ', 'NOK'],
    'Panama': ['PA', 'PAB'],
    'Micronesia': ['FM', 'USD'],
    'Liechtenstein': ['LI', 'CHF'],
    'French Guiana': ['GF', 'EUR'],
    'the Democratic Republic of': ['CD', 'CDF'],
    'Martinique': ['MQ', 'EUR'],
    'Burkina Faso': ['BF', 'XOF'],
    'Senegal': ['SN', 'XOF'],
    'Palestinian Territories': ['PS', ' '],
    'Georgia': ['GE', 'GEL'],
    'Cameroon': ['CM', 'XAF'],
    'Kiribati': ['KI', 'AUD'],
    'Mozambique': ['MZ', 'MZN'],
    'Niger': ['NE', 'XOF'],
    'Sudan': ['SD', 'SDG']
}

USState = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN',
           'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV',
           'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN',
           'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']


def getCountryCur(location):
    if location.split(', ')[-1] in countryMap:
        return countryMap[location.split(', ')[-1]]

    if location.split(', ')[-1] in USState:
        return countryMap['United States of America']

    fail = True
    firstTime = True
    country = location.split(', ')[-1]
    while fail:
        try:
            country = pycountry.countries.lookup(country)
        except LookupError:
            if firstTime:
                try:
                    country = geolocator.geocode(location).address.split(', ')[-1]
                except AttributeError:
                    print 'Cannot locate this location ' + location
                    country = raw_input('Please type into new country \n')
                    print 'Searching new country: ' + country
                finally:
                    firstTime = False
            else:
                print 'Cannot find location ' + location
                country = raw_input('Please type into new country \n')
                print 'Searching new country: ' + country
        else:
            fail = False

    currency = pycountry.currencies.get(numeric=country.numeric).alpha_3
    country = country.alpha_2
    print country + ', ' + currency
    return [country, currency]


def listPage(link):
    global session
    # print link
    session.visit(link)
    # print 'finished!!!!'
    doc = session.body()
    # print session.url()
    global eachProj
    eachProj = BeautifulSoup(doc, "lxml")


def refreshWebPage(link):
    # print 'before request'
    res = requests.get(link)
    # print 'end request'
    if res.status_code != 200:
        raise ParamError('in refresh element, response code is not 200, it is %s' % res.status_code)

    global eachProj
    eachProj = BeautifulSoup(res.content, 'lxml')


def writeCrawlData(data):
    if os.path.exists('10K_100k_data.csv'):
        hasFile = True
    else:
        hasFile = False

    if hasFile:
        with open('10K_100k_data.csv', 'ab') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=varNameList, delimiter=',', lineterminator='\n')
            writer.writerow(rowdict=data)
    else:
        with open('10K_100k_data.csv', 'wb') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=varNameList, delimiter=',', lineterminator='\n')
            writer.writeheader()
            writer.writerow(rowdict=data)

