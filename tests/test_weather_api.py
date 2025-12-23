import httpx
import pytest

# Test edeceğimiz örnek bir koordinat (İstanbul)
BASE_URL = "https://api.open-meteo.com/v1/forecast"

def test_get_current_weather_success():
    """Pozitif Test: İstanbul için hava durumu verisi başarılı dönüyor mu?"""
    params = {
        "latitude": 41.0082,
        "longitude": 28.9784,
        "current_weather": "true"
    }
    response = httpx.get(BASE_URL, params=params)
    
    assert response.status_code == 200
    assert "current_weather" in response.json()
    # Hava durumunun bir sayı (sıcaklık) içerdiğini doğrula
    assert isinstance(response.json()["current_weather"]["temperature"], (int, float))

def test_invalid_coordinates_error():
    """Negatif Test: Geçersiz koordinat gönderildiğinde sistem 400 hatası veriyor mu?"""
    params = {
        "latitude": 999, # Geçersiz enlem
        "longitude": 28.9784
    }
    response = httpx.get(BASE_URL, params=params)
    
    # API'nin hata yönetimi test edilir
    assert response.status_code == 400
    assert "error" in response.json().get("reason", "").lower() or response.status_code == 400

@pytest.mark.parametrize("city_lat, city_long", [
    (48.8566, 2.3522),  # Paris 
    (40.4168, -3.7038), # Madrid
    (51.5074, -0.1278)  # Londra
])
def test_multiple_cities_weather(city_lat, city_long):
    """Veri odaklı test (Data-driven): Farklı lokasyonlar için sistem çalışıyor mu?"""
    params = {"latitude": city_lat, "longitude": city_long, "current_weather": "true"}
    response = httpx.get(BASE_URL, params=params)
    assert response.status_code == 200