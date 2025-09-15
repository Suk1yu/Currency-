from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests
import os

myapp = Flask(__name__)

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
]

# Nilai tukar fallback yang lebih lengkap
fallback_rates = {
    "USD": {"EUR": 0.93, "IDR": 15500, "JPY": 147, "GBP": 0.79, "AUD": 1.52, 
            "CAD": 1.36, "CHF": 0.88, "CNY": 7.18, "KRW": 1320, "SGD": 1.35, 
            "MXN": 17.2, "BRL": 5.12, "ZAR": 18.9, "TRY": 32.1},
    "EUR": {"USD": 1.08, "IDR": 16700, "JPY": 158, "GBP": 0.85, "AUD": 1.63, 
            "CAD": 1.46, "CHF": 0.95, "CNY": 7.75, "KRW": 1420, "SGD": 1.45, 
            "MXN": 18.5, "BRL": 5.51, "ZAR": 20.3, "TRY": 34.5},
    "IDR": {"USD": 0.000064, "EUR": 0.000060, "JPY": 0.0095, "GBP": 0.000051, 
            "AUD": 0.000096, "CAD": 0.000073, "CHF": 0.000057, "CNY": 0.00046, 
            "KRW": 0.085, "SGD": 0.000087, "MXN": 0.00101, "BRL": 0.00032, 
            "ZAR": 0.00118, "TRY": 0.00207},
    "JPY": {"USD": 0.0068, "EUR": 0.0063, "IDR": 105, "GBP": 0.0054, 
            "AUD": 0.0103, "CAD": 0.0092, "CHF": 0.0060, "CNY": 0.049, 
            "KRW": 9.0, "SGD": 0.0092, "MXN": 0.117, "BRL": 0.035, 
            "ZAR": 0.129, "TRY": 0.218},
    "GBP": {"USD": 1.27, "EUR": 1.17, "IDR": 19700, "JPY": 185, 
            "AUD": 1.92, "CAD": 1.72, "CHF": 1.12, "CNY": 9.08, 
            "KRW": 1665, "SGD": 1.70, "MXN": 21.6, "BRL": 6.43, 
            "ZAR": 23.7, "TRY": 40.2},
    "AUD": {"USD": 0.66, "EUR": 0.61, "IDR": 10300, "JPY": 97, 
            "GBP": 0.52, "CAD": 0.90, "CHF": 0.58, "CNY": 4.72, 
            "KRW": 870, "SGD": 0.89, "MXN": 11.3, "BRL": 3.37, 
            "ZAR": 12.4, "TRY": 21.1},
    "CAD": {"USD": 0.73, "EUR": 0.68, "IDR": 11400, "JPY": 108, 
            "GBP": 0.58, "AUD": 1.11, "CHF": 0.65, "CNY": 5.28, 
            "KRW": 970, "SGD": 0.99, "MXN": 12.6, "BRL": 3.76, 
            "ZAR": 13.9, "TRY": 23.6},
    "CHF": {"USD": 1.14, "EUR": 1.05, "IDR": 17500, "JPY": 167, 
            "GBP": 0.89, "AUD": 1.72, "CAD": 1.54, "CNY": 8.16, 
            "KRW": 1500, "SGD": 1.53, "MXN": 19.5, "BRL": 5.82, 
            "ZAR": 21.5, "TRY": 36.5},
    "CNY": {"USD": 0.14, "EUR": 0.13, "IDR": 2150, "JPY": 20.4, 
            "GBP": 0.11, "AUD": 0.21, "CAD": 0.19, "CHF": 0.12, 
            "KRW": 184, "SGD": 0.19, "MXN": 2.4, "BRL": 0.71, 
            "ZAR": 2.63, "TRY": 4.47},
    "KRW": {"USD": 0.00076, "EUR": 0.00070, "IDR": 11.7, "JPY": 0.11, 
            "GBP": 0.00060, "AUD": 0.00115, "CAD": 0.00103, "CHF": 0.00067, 
            "CNY": 0.0054, "SGD": 0.0010, "MXN": 0.013, "BRL": 0.0039, 
            "ZAR": 0.014, "TRY": 0.024},
    "SGD": {"USD": 0.74, "EUR": 0.69, "IDR": 11500, "JPY": 109, 
            "GBP": 0.59, "AUD": 1.12, "CAD": 1.01, "CHF": 0.65, 
            "CNY": 5.30, "KRW": 970, "MXN": 12.7, "BRL": 3.79, 
            "ZAR": 14.0, "TRY": 23.8},
    "MXN": {"USD": 0.058, "EUR": 0.054, "IDR": 900, "JPY": 8.5, 
            "GBP": 0.046, "AUD": 0.088, "CAD": 0.079, "CHF": 0.051, 
            "CNY": 0.42, "KRW": 77, "SGD": 0.079, "BRL": 0.30, 
            "ZAR": 1.10, "TRY": 1.87},
    "BRL": {"USD": 0.20, "EUR": 0.18, "IDR": 3100, "JPY": 29.4, 
            "GBP": 0.16, "AUD": 0.30, "CAD": 0.27, "CHF": 0.17, 
            "CNY": 1.41, "KRW": 258, "SGD": 0.26, "MXN": 3.33, 
            "ZAR": 3.69, "TRY": 6.27},
    "ZAR": {"USD": 0.053, "EUR": 0.049, "IDR": 820, "JPY": 7.8, 
            "GBP": 0.042, "AUD": 0.081, "CAD": 0.072, "CHF": 0.047, 
            "CNY": 0.38, "KRW": 70, "SGD": 0.071, "MXN": 0.91, 
            "BRL": 0.27, "TRY": 1.70},
    "TRY": {"USD": 0.031, "EUR": 0.029, "IDR": 480, "JPY": 4.6, 
            "GBP": 0.025, "AUD": 0.047, "CAD": 0.042, "CHF": 0.027, 
            "CNY": 0.22, "KRW": 41, "SGD": 0.042, "MXN": 0.54, 
            "BRL": 0.16, "ZAR": 0.59}
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
