from unittest.mock import patch
from core.utils import get_currency_rates

@patch('core.utils.requests.get')
def test_get_currency_rates_failure(mock_get):
    mock_get.side_effect = Exception('Connection error')
    result = get_currency_rates()
    assert 'error' in result