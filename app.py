from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests
import os
import logging
from dateutil import parser
from dateutil.relativedelta import relativedelta

# Setup logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# API Key untuk News API
NEWS_API_KEY = "0aff32f485434cdab0112137e4f0b8f5"

# Data mata uang dengan kode, nama, dan kode bendera
currencies = [
    {"code": "USD", "name": "US Dollar", "flag": "us"},
    {"code": "EUR", "name": "Euro", "flag": "eu"},
    {"code": "IDR", "name": "Indonesian Rupiah", "flag": "id"},
    {"code": "JPY", "name": "Japanese Yen", "flag": "jp"},
    {"code": "GBP", "name": "British Pound", "flag": "gb"},
    {"code": "AUD", "name": "Australian Dollar", "flag": "au"},
    {"code": "CAD", "name": "Canadian Dollar", "flag": "ca"},
    {"code": "CHF", "name": "Swiss Franc", "flag": "ch"},
    {"code": "CNY", "name": "Chinese Yuan", "flag": "cn"},
    {"code": "KRW", "name": "South Korean Won", "flag": "kr"},
    {"code": "SGD", "name": "Singapore Dollar", "flag": "sg"},
    {"code": "MXN", "name": "Mexican Peso", "flag": "mx"},
    {"code": "BRL", "name": "Brazilian Real", "flag": "br"},
    {"code": "ZAR", "name": "South African Rand", "flag": "za"},
    {"code": "TRY", "name": "Turkish Lira", "flag": "tr"},
    {"code": "INR", "name": "Indian Rupee", "flag": "in"},
    {"code": "RUB", "name": "Russian Ruble", "flag": "ru"},
    {"code": "AED", "name": "UAE Dirham", "flag": "ae"},
    {"code": "SAR", "name": "Saudi Riyal", "flag": "sa"},
    {"code": "THB", "name": "Thai Baht", "flag": "th"},
    {"code": "MYR", "name": "Malaysian Ringgit", "flag": "my"},
    {"code": "VND", "name": "Vietnamese Dong", "flag": "vn"},
    {"code": "PHP", "name": "Philippine Peso", "flag": "ph"},
    {"code": "HKD", "name": "Hong Kong Dollar", "flag": "hk"},
    {"code": "TWD", "name": "New Taiwan Dollar", "flag": "tw"},
    {"code": "NZD", "name": "New Zealand Dollar", "flag": "nz"},
    {"code": "SEK", "name": "Swedish Krona", "flag": "se"},
    {"code": "NOK", "name": "Norwegian Krone", "flag": "no"},
    {"code": "DKK", "name": "Danish Krone", "flag": "dk"},
    {"code": "PLN", "name": "Polish Złoty", "flag": "pl"},
    {"code": "HUF", "name": "Hungarian Forint", "flag": "hu"},
    {"code": "CZK", "name": "Czech Koruna", "flag": "cz"},
    {"code": "ILS", "name": "Israeli Shekel", "flag": "il"},
    {"code": "EGP", "name": "Egyptian Pound", "flag": "eg"},
    {"code": "NGN", "name": "Nigerian Naira", "flag": "ng"},
    {"code": "ARS", "name": "Argentine Peso", "flag": "ar"},
    {"code": "CLP", "name": "Chilean Peso", "flag": "cl"},
    {"code": "COP", "name": "Colombian Peso", "flag": "co"},
    {"code": "PEN", "name": "Peruvian Sol", "flag": "pe"},
    {"code": "UAH", "name": "Ukrainian Hryvnia", "flag": "ua"},
    {"code": "RON", "name": "Romanian Leu", "flag": "ro"},
    {"code": "BGN", "name": "Bulgarian Lev", "flag": "bg"},
    {"code": "HRK", "name": "Croatian Kuna", "flag": "hr"},
    {"code": "RSD", "name": "Serbian Dinar", "flag": "rs"},
    {"code": "ISK", "name": "Icelandic Króna", "flag": "is"},
    {"code": "KWD", "name": "Kuwaiti Dinar", "flag": "kw"},
    {"code": "QAR", "name": "Qatari Riyal", "flag": "qa"},
    {"code": "OMR", "name": "Omani Rial", "flag": "om"},
    {"code": "BHD", "name": "Bahraini Dinar", "flag": "bh"},
    {"code": "JOD", "name": "Jordanian Dinar", "flag": "jo"},
    {"code": "LKR", "name": "Sri Lankan Rupee", "flag": "lk"},
    {"code": "BDT", "name": "Bangladeshi Taka", "flag": "bd"},
    {"code": "PKR", "name": "Pakistani Rupee", "flag": "pk"},
    {"code": "KES", "name": "Kenyan Shilling", "flag": "ke"},
    {"code": "ETB", "name": "Ethiopian Birr", "flag": "et"},
    {"code": "GHS", "name": "Ghanaian Cedi", "flag": "gh"},
    {"code": "MAD", "name": "Moroccan Dirham", "flag": "ma"},
    {"code": "DZD", "name": "Algerian Dinar", "flag": "dz"},
    {"code": "TND", "name": "Tunisian Dinar", "flag": "tn"},
    {"code": "UGX", "name": "Ugandan Shilling", "flag": "ug"},
    {"code": "TZS", "name": "Tanzanian Shilling", "flag": "tz"},
    {"code": "XAF", "name": "Central African CFA Franc", "flag": "cm"},
    {"code": "XOF", "name": "West African CFA Franc", "flag": "sn"},
    {"code": "XPF", "name": "CFP Franc", "flag": "pf"},
    {"code": "CRC", "name": "Costa Rican Colón", "flag": "cr"},
    {"code": "DOP", "name": "Dominican Peso", "flag": "do"},
    {"code": "GTQ", "name": "Guatemalan Quetzal", "flag": "gt"},
    {"code": "HNL", "name": "Honduran Lempira", "flag": "hn"},
    {"code": "NIO", "name": "Nicaraguan Córdoba", "flag": "ni"},
    {"code": "PYG", "name": "Paraguayan Guaraní", "flag": "py"},
    {"code": "UYU", "name": "Uruguayan Peso", "flag": "uy"},
    {"code": "BOB", "name": "Bolivian Boliviano", "flag": "bo"},
    {"code": "PAB", "name": "Panamanian Balboa", "flag": "pa"},
    {"code": "BZD", "name": "Belize Dollar", "flag": "bz"},
    {"code": "TTD", "name": "Trinidad & Tobago Dollar", "flag": "tt"},
    {"code": "JMD", "name": "Jamaican Dollar", "flag": "jm"},
    {"code": "BSD", "name": "Bahamian Dollar", "flag": "bs"},
    {"code": "BBD", "name": "Barbadian Dollar", "flag": "bb"},
    {"code": "XCD", "name": "East Caribbean Dollar", "flag": "ag"},
    {"code": "AWG", "name": "Aruban Florin", "flag": "aw"},
    {"code": "ANG", "name": "Netherlands Antillean Guilder", "flag": "cw"},
    {"code": "KYD", "name": "Cayman Islands Dollar", "flag": "ky"},
    {"code": "FJD", "name": "Fijian Dollar", "flag": "fj"},
    {"code": "WST", "name": "Samoan Tala", "flag": "ws"},
    {"code": "TOP", "name": "Tongan Paʻanga", "flag": "to"},
    {"code": "VUV", "name": "Vanuatu Vatu", "flag": "vu"},
    {"code": "SBD", "name": "Solomon Islands Dollar", "flag": "sb"},
    {"code": "PGK", "name": "Papua New Guinean Kina", "flag": "pg"},
    {"code": "KHR", "name": "Cambodian Riel", "flag": "kh"},
    {"code": "LAK", "name": "Laotian Kip", "flag": "la"},
    {"code": "MMK", "name": "Myanmar Kyat", "flag": "mm"},
    {"code": "MNT", "name": "Mongolian Tögrög", "flag": "mn"},
    {"code": "NPR", "name": "Nepalese Rupee", "flag": "np"},
    {"code": "BTN", "name": "Bhutanese Ngultrum", "flag": "bt"},
    {"code": "MVR", "name": "Maldivian Rufiyaa", "flag": "mv"},
    {"code": "AFN", "name": "Afghan Afghani", "flag": "af"},
    {"code": "IRR", "name": "Iranian Rial", "flag": "ir"},
    {"code": "IQD", "name": "Iraqi Dinar", "flag": "iq"},
    {"code": "SYP", "name": "Syrian Pound", "flag": "sy"},
    {"code": "YER", "name": "Yemeni Rial", "flag": "ye"},
    {"code": "LBP", "name": "Lebanese Pound", "flag": "lb"},
    {"code": "JEP", "name": "Jersey Pound", "flag": "je"},
    {"code": "GGP", "name": "Guernsey Pound", "flag": "gg"},
    {"code": "IMP", "name": "Isle of Man Pound", "flag": "im"},
    {"code": "FKP", "name": "Falkland Islands Pound", "flag": "fk"},
    {"code": "GIP", "name": "Gibraltar Pound", "flag": "gi"},
    {"code": "SHP", "name": "Saint Helena Pound", "flag": "sh"},
    {"code": "CUC", "name": "Cuban Convertible Peso", "flag": "cu"},
    {"code": "CUP", "name": "Cuban Peso", "flag": "cu"},
    {"code": "ZMW", "name": "Zambian Kwacha", "flag": "zm"},
    {"code": "ZWL", "name": "Zimbabwean Dollar", "flag": "zw"},
    {"code": "NAD", "name": "Namibian Dollar", "flag": "na"},
    {"code": "BWP", "name": "Botswana Pula", "flag": "bw"},
    {"code": "LSL", "name": "Lesotho Loti", "flag": "ls"},
    {"code": "SZL", "name": "Swazi Lilangeni", "flag": "sz"},
    {"code": "MGA", "name": "Malagasy Ariary", "flag": "mg"},
    {"code": "MUR", "name": "Mauritian Rupee", "flag": "mu"},
    {"code": "SCR", "name": "Seychellois Rupee", "flag": "sc"},
    {"code": "CDF", "name": "Congolese Franc", "flag": "cd"},
    {"code": "RWF", "name": "Rwandan Franc", "flag": "rw"},
    {"code": "BIF", "name": "Burundian Franc", "flag": "bi"},
    {"code": "DJF", "name": "Djiboutian Franc", "flag": "dj"},
    {"code": "KMF", "name": "Comorian Franc", "flag": "km"},
    {"code": "GNF", "name": "Guinean Franc", "flag": "gn"},
    {"code": "MRO", "name": "Mauritanian Ouguiya", "flag": "mr"},
    {"code": "MRU", "name": "Mauritanian Ouguiya", "flag": "mr"},
    {"code": "STD", "name": "São Tomé & Príncipe Dobra", "flag": "st"},
    {"code": "STN", "name": "São Tomé & Príncipe Dobra", "flag": "st"},
    {"code": "ERN", "name": "Eritrean Nakfa", "flag": "er"},
    {"code": "SSP", "name": "South Sudanese Pound", "flag": "ss"},
    {"code": "SDG", "name": "Sudanese Pound", "flag": "sd"},
    {"code": "LYD", "name": "Libyan Dinar", "flag": "ly"},
    {"code": "MZN", "name": "Mozambican Metical", "flag": "mz"},
    {"code": "AOA", "name": "Angolan Kwanza", "flag": "ao"},
    {"code": "GMD", "name": "Gambian Dalasi", "flag": "gm"},
    {"code": "SLL", "name": "Sierra Leonean Leone", "flag": "sl"},
    {"code": "LRD", "name": "Liberian Dollar", "flag": "lr"},
    {"code": "CVE", "name": "Cape Verdean Escudo", "flag": "cv"},
    {"code": "AMD", "name": "Armenian Dram", "flag": "am"},
    {"code": "AZN", "name": "Azerbaijani Manat", "flag": "az"},
    {"code": "BAM", "name": "Bosnia-Herzegovina Convertible Mark", "flag": "ba"},
    {"code": "GEL", "name": "Georgian Lari", "flag": "ge"},
    {"code": "MDL", "name": "Moldovan Leu", "flag": "md"},
    {"code": "ALL", "name": "Albanian Lek", "flag": "al"},
    {"code": "MKD", "name": "Macedonian Denar", "flag": "mk"},
    {"code": "BYN", "name": "Belarusian Ruble", "flag": "by"},
    {"code": "KZT", "name": "Kazakhstani Tenge", "flag": "kz"},
    {"code": "KGS", "name": "Kyrgyzstani Som", "flag": "kg"},
    {"code": "TJS", "name": "Tajikistani Somoni", "flag": "tj"},
    {"code": "TMT", "name": "Turkmenistani Manat", "flag": "tm"},
    {"code": "UZS", "name": "Uzbekistani Som", "flag": "uz"},
]
# Nilai tukar fallback yang lebih lengkap
fallback_rates = {
    "USD": {
        "EUR": 0.92, "GBP": 0.79, "JPY": 150.25, "AUD": 1.52, "CAD": 1.35,
        "CHF": 0.90, "CNY": 7.25, "HKD": 7.82, "NZD": 1.64, "SEK": 10.45,
        "NOK": 10.60, "DKK": 6.88, "SGD": 1.35, "KRW": 1320.0, "INR": 83.15,
        "BRL": 5.05, "RUB": 92.50, "ZAR": 18.75, "TRY": 32.10, "MXN": 17.15,
        "IDR": 15600.0, "THB": 35.80, "MYR": 4.72, "PHP": 56.25, "VND": 24750.0,
        "AED": 3.67, "SAR": 3.75, "PLN": 4.02, "HUF": 355.0, "CZK": 22.80,
        "ILS": 3.65, "CLP": 925.0, "COP": 3950.0, "ARS": 850.0, "PEN": 3.75,
        "UAH": 38.50, "RON": 4.55, "BGN": 1.80, "HRK": 6.95, "RSD": 108.0,
        "ISK": 135.0, "KWD": 0.308, "QAR": 3.64, "OMR": 0.385, "BHD": 0.377,
        "JOD": 0.709, "LKR": 320.0, "BDT": 109.5, "PKR": 280.0, "KES": 157.0,
        "ETB": 56.5, "GHS": 12.25, "MAD": 10.05, "DZD": 134.5, "TND": 3.12,
        "UGX": 3800.0, "TZS": 2500.0, "XAF": 605.0, "XOF": 605.0, "XPF": 110.0,
        "CRC": 530.0, "DOP": 58.5, "GTQ": 7.82, "HNL": 24.65, "NIO": 36.75,
        "PYG": 7300.0, "UYU": 39.25, "BOB": 6.91, "PAB": 1.00, "BZD": 2.02,
        "TTD": 6.78, "JMD": 156.0, "BSD": 1.00, "BBD": 2.00, "XCD": 2.70,
        "AWG": 1.79, "ANG": 1.79, "KYD": 0.83, "FJD": 2.25, "WST": 2.70,
        "TOP": 2.35, "VUV": 120.0, "SBD": 8.45, "PGK": 3.75, "KHR": 4100.0,
        "LAK": 20750.0, "MMK": 2100.0, "MNT": 3400.0, "NPR": 133.0, "BTN": 83.15,
        "MVR": 15.40, "AFN": 71.5, "IRR": 42000.0, "IQD": 1310.0, "SYP": 12500.0,
        "YER": 250.0, "LBP": 15000.0, "JEP": 0.79, "GGP": 0.79, "IMP": 0.79,
        "FKP": 0.79, "GIP": 0.79, "SHP": 0.79, "CUC": 1.00, "CUP": 24.0,
        "ZMW": 23.5, "ZWL": 322.0, "NAD": 18.75, "BWP": 13.65, "LSL": 18.75,
        "SZL": 18.75, "MGA": 4500.0, "MUR": 46.25, "SCR": 13.5, "CDF": 2700.0,
        "RWF": 1290.0, "BIF": 2850.0, "DJF": 178.0, "KMF": 450.0, "GNF": 8600.0,
        "MRU": 39.5, "STN": 22.5, "ERN": 15.0, "SSP": 1300.0, "SDG": 600.0,
        "LYD": 4.82, "MZN": 63.5, "AOA": 850.0, "GMD": 65.5, "SLL": 22500.0,
        "LRD": 190.0, "CVE": 102.0, "AMD": 390.0, "AZN": 1.70, "BAM": 1.80,
        "GEL": 2.65, "MDL": 17.85, "ALL": 95.5, "MKD": 56.5, "BYN": 3.25,
        "KZT": 470.0, "KGS": 89.5, "TJS": 10.95, "TMT": 3.50, "UZS": 12500.0
    }
}

# API alternatif untuk nilai tukar
EXCHANGE_API_URLS = [
    "https://api.exchangerate.host/latest?base=",
    "https://open.er-api.com/v6/latest/",
    "https://api.exchangerate-api.com/v4/latest/"
]

def format_number(number, decimals=2):
    try:
        if number > 0 and number < 0.01:
            return f"{number:.6f}"
        
        # Format angka dengan pemisah ribuan
        return f"{number:,.{decimals}f}"
    except:
        return str(number)

def format_currency(amount, currency_code, with_symbol=False):
    try:
        # Untuk IDR dan mata uang lain tanpa desimal, jangan tampilkan tempat desimal
        decimals = 0 if currency_code in ["IDR", "JPY", "KRW"] else 2
        
        if with_symbol:
            # Simulasi pemformatan mata uang dengan simbol
            symbol_map = {
                "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", 
                "IDR": "Rp", "CNY": "¥", "KRW": "₩"
            }
            symbol = symbol_map.get(currency_code, currency_code + " ")
            return f"{symbol}{format_number(amount, decimals)}"
        else:
            return format_number(amount, decimals)
    except:
        return str(amount)

def convert_currency(amount, from_curr, to_curr):
    exchange_rate = 0
    inverse_rate = 0
    use_fallback = False
    api_used = "Fallback"
    
    # Coba beberapa API berbeda
    for api_url in EXCHANGE_API_URLS:
        try:
            url = f"{api_url}{from_curr}"
            print(f"Trying API: {url}")
            
            response = requests.get(url, timeout=10)
            
            if not response.ok:
                continue
            
            data = response.json()
            
            # Handle format respons yang berbeda dari berbagai API
            rates = None
            if 'rates' in data:
                rates = data['rates']
            elif 'conversion_rates' in data:
                rates = data['conversion_rates']
            
            if not rates or to_curr not in rates:
                continue
            
            # Hitung hasil dan nilai tukar
            exchange_rate = rates[to_curr]
            result = amount * exchange_rate
            inverse_rate = 1 / exchange_rate
            api_used = api_url
            break
            
        except Exception as error:
            print(f"API {api_url} failed: {error}")
            continue
    
    # Jika semua API gagal, gunakan fallback rates
    if exchange_rate == 0:
        use_fallback = True
        if from_curr in fallback_rates and to_curr in fallback_rates[from_curr]:
            exchange_rate = fallback_rates[from_curr][to_curr]
            result = amount * exchange_rate
            inverse_rate = 1 / exchange_rate
            api_used = "Fallback"
        else:
            # Jika tidak ada fallback, coba hitung melalui USD
            try:
                if from_curr != "USD" and to_curr != "USD":
                    # Konversi from_curr -> USD -> to_curr
                    usd_rate_from = fallback_rates[from_curr]["USD"] if from_curr in fallback_rates and "USD" in fallback_rates[from_curr] else 1
                    usd_rate_to = fallback_rates["USD"][to_curr] if to_curr in fallback_rates["USD"] else 1
                    exchange_rate = usd_rate_to / usd_rate_from
                    result = amount * exchange_rate
                    inverse_rate = 1 / exchange_rate
                    api_used = "Fallback via USD"
                else:
                    raise Exception("No conversion rate available")
            except:
                raise Exception("No conversion rate available")
    
    print(f"Used {api_used} for conversion: {from_curr} to {to_curr}")
    return result, exchange_rate, inverse_rate, use_fallback

@app.route('/')
def index():
    return render_template('index.html', currencies=currencies)

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    
    try:
        amount = float(data.get('amount', 1))
        from_currency = data.get('fromCurrency', 'USD')
        to_currency = data.get('toCurrency', 'IDR')
        
        if amount <= 0:
            return jsonify({
                'success': False,
                'error': 'Please enter a valid amount greater than zero.'
            })
        
        if from_currency == to_currency:
            # Jika mata uang sama, hasilnya adalah amount itu sendiri
            result = amount
            exchange_rate = 1
            inverse_rate = 1
            use_fallback = True
        else:
            result, exchange_rate, inverse_rate, use_fallback = convert_currency(
                amount, from_currency, to_currency
            )
        
        # Dapatkan nama mata uang
        from_currency_name = next((c["name"] for c in currencies if c["code"] == from_currency), from_currency)
        to_currency_name = next((c["name"] for c in currencies if c["code"] == to_currency), to_currency)
        
        # Format hasil
        base_amount = f"{amount:.2f}"
        formatted_result = format_currency(result, to_currency)
        formatted_inverse_rate = format_number(inverse_rate, 6)
        
        # Waktu saat ini
        now = datetime.now()
        last_updated = now.strftime("%b %d, %Y, %I:%M %p") + " UTC"
        
        if use_fallback:
            last_updated = "Using fallback rates - Live API unavailable"
        
        return jsonify({
            'success': True,
            'rateText': f"{base_amount} {from_currency} =",
            'convertedAmount': formatted_result,
            'currencyName': to_currency_name,
            'inverseRateText': f"1 {to_currency} = {formatted_inverse_rate} {from_currency}",
            'fromCurrencyName': from_currency_name,
            'toCurrencyName': to_currency_name,
            'lastUpdated': last_updated
        })
        
    except Exception as e:
        print(f"Conversion error: {e}")
        return jsonify({
            'success': False,
            'error': 'Sorry, we couldn\'t fetch the conversion rate. Please try again later.'
        })

@app.route('/get_news')
def get_news():
    try:
        # Mendapatkan berita finansial dari News API
        query = "currency OR forex OR exchange rate OR central bank OR interest rates"
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        
        app.logger.info(f"Requesting news from: {url}")
        response = requests.get(url)
        app.logger.info(f"Response status: {response.status_code}")
        
        if response.status_code != 200:
            app.logger.error(f"NewsAPI returned status code: {response.status_code}")
            app.logger.error(f"Response text: {response.text}")
            raise Exception(f"NewsAPI returned status code {response.status_code}")
        
        data = response.json()
        
        # Check if we got articles
        if data.get('status') != 'ok':
            app.logger.error(f"NewsAPI returned error: {data.get('message', 'Unknown error')}")
            raise Exception(f"NewsAPI error: {data.get('message', 'Unknown error')}")
        
        # Format berita untuk frontend
        articles = []
        for article in data.get('articles', [])[:100]:  # Ambil 10 berita terbaru
            try:
                # Parse waktu publish dengan dateutil untuk akurasi lebih baik
                published_at = parser.parse(article['publishedAt'])
                current_time = datetime.utcnow()
                time_diff = relativedelta(current_time, published_at)
                
                # Tentukan teks waktu yang sesuai
                if time_diff.years > 0:
                    time_ago = f"{time_diff.years} years ago" if time_diff.years > 1 else "1 year ago"
                elif time_diff.months > 0:
                    time_ago = f"{time_diff.months} months ago" if time_diff.months > 1 else "1 month ago"
                elif time_diff.days > 0:
                    time_ago = f"{time_diff.days} days ago" if time_diff.days > 1 else "1 day ago"
                elif time_diff.hours > 0:
                    time_ago = f"{time_diff.hours} hours ago" if time_diff.hours > 1 else "1 hour ago"
                elif time_diff.minutes > 0:
                    time_ago = f"{time_diff.minutes} minutes ago" if time_diff.minutes > 1 else "1 minute ago"
                else:
                    time_ago = "Just now"
                    
            except Exception as e:
                app.logger.error(f"Error parsing time for article: {e}")
                # Fallback jika parsing gagal
                time_ago = "Recently"
                
            articles.append({
                'title': article['title'],
                'description': article['description'] or 'No description available',
                'source': article['source']['name'],
                'time': time_ago,
                'url': article['url'],
                'published_at': article['publishedAt']  # Menyimpan waktu asli untuk debugging
            })
        
        app.logger.info(f"Successfully fetched {len(articles)} news articles")
        # Log waktu untuk debugging
        for article in articles:
            app.logger.debug(f"Article: {article['title']} - Published: {article['published_at']} - Display: {article['time']}")
        
        return jsonify({'articles': articles})
    
    except Exception as e:
        app.logger.error(f"Error fetching news: {str(e)}")
        # Return berita sampel jika API tidak bekerja
        return jsonify({
            'articles': [
                {
                    'title': "US Dollar Strengthens Against Major Currencies",
                    'description': "The US dollar reached a two-month high against a basket of currencies as economic data surpassed expectations.",
                    'source': "Bloomberg",
                    'time': "2 hours ago",
                    'url': "#",
                    'published_at': datetime.utcnow().isoformat()
                },
                {
                    'title': "ECB Holds Rates Steady Amid Inflation Concerns",
                    'description': "The European Central Bank maintained its current interest rates while signaling potential cuts later this year.",
                    'source': "Financial Times",
                    'time': "5 hours ago",
                    'url': "#",
                    'published_at': datetime.utcnow().isoformat()
                },
                {
                    'title': "Yen Volatility Increases as Bank of Japan Meets",
                    'description': "The Japanese yen experienced heightened volatility as traders anticipated the Bank of Japan's policy decision.",
                    'source': "Reuters",
                    'time': "Yesterday",
                    'url': "#",
                    'published_at': datetime.utcnow().isoformat()
                }
            ]
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5093))
    app.run(host='0.0.0.0', port=port, debug=True)
