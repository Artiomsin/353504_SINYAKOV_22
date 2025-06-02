import requests
from django.conf import settings
from django.core.cache import cache

import requests
from django.conf import settings
from django.core.cache import cache



def get_currency_rates():
    try:
        if not settings.EXCHANGE_API_KEY:
            return {'error': 'API key not configured'}
        
        url = f"https://v6.exchangerate-api.com/v6/{settings.EXCHANGE_API_KEY}/latest/USD"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            usd_to_byn = data['conversion_rates']['BYN']
            usd_to_eur = data['conversion_rates']['EUR']
            
            # EUR → BYN
            eur_to_byn = usd_to_byn / usd_to_eur
            
            return {
                'rates': {
                    'USD_BYN': usd_to_byn,
                    'EUR_BYN': eur_to_byn
                }
            }
        return {'error': f"Ошибка {response.status_code}: {response.text}"}
    
    except KeyError as e:
        return {'error': f"Ошибка формата данных: {str(e)}"}
    except ZeroDivisionError:
        return {'error': "Ошибка расчета курса"}
    except Exception as e:
        return {'error': str(e)}

def fetch_doctor_schedule(doctor_id):
    """Пример использования API для получения расписания"""
    try:
        response = requests.get(
            f"{settings.API_BASE_URL}/doctors/{doctor_id}/schedule",
            headers={"Authorization": f"Bearer {settings.API_KEY}"}
        )
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None