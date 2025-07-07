import requests
from bs4 import BeautifulSoup
import time
import winsound

# Takip edilecek Zara ürün linkleri
PRODUCT_URLS = [
    "https://www.zara.com/tr/tr/100-keten-gomlek-p04334181.html?v1=433535886",
    "https://www.zara.com/tr/tr/100-keten-gomlek-p04334181.html?v1=433535884",
    "https://www.zara.com/tr/tr/sinirli-sayida-uretilmis-100-keten-gomlek-p04443300.html?v1=440211031"
]

# Takip edilecek bedenler
SIZES_TO_CHECK = ["S", "M"]

# Kontrol sıklığı (saniye cinsinden)
CHECK_INTERVAL = 30


def check_stock(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()

        for size in SIZES_TO_CHECK:
            if size in text and "STOKTA YOK" not in text.upper():
                print(f"🟢 {size} bedeni stokta bulundu! -> {url}")
                return True
        return False
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return False


def alert():
    print("🔔 Ürün stokta! Sesli uyarı veriliyor.")
    for _ in range(5):
        winsound.Beep(1000, 300)  # 1000 Hz, 0.3 saniye
        time.sleep(0.2)


if __name__ == "__main__":
    print("🛍️ Zara stok takip başlatıldı. Her 30 saniyede bir kontrol ediliyor...\n")
    while True:
        for url in PRODUCT_URLS:
            in_stock = check_stock(url)
            if in_stock:
                alert()
        time.sleep(CHECK_INTERVAL)
