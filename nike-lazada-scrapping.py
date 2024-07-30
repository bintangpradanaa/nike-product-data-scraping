from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

# Configure WebDriver
opsi = webdriver.ChromeOptions()
opsi.add_argument('--headless')
servis = Service('chromedriver.exe')
driver = webdriver.Chrome(service=servis, options=opsi)

base_url = "https://www.lazada.co.id/tag/nike/?q=nike&catalog_redirect_tag=true"
driver.set_window_size(1300, 800)

list_nama, list_link, list_gambar, list_harga, list_diskon, list_terjual, list_lokasi, list_rating = [], [], [], [], [], [], [], []

page = 1
while True:
    print(f"Scraping page {page}")
    url = f"{base_url}&page={page}"
    driver.get(url)

    time.sleep(5)
    content = driver.page_source

    # Parsing HTML content
    soup = BeautifulSoup(content, 'html.parser')
    products = soup.find_all('div', class_='Bm3ON')

    if not products:
        print("Produk sudah tidak ditemukan!")
        break

    for product in products:
        print(f'Memproses data produk di page {page}')
        
        # Nama
        nama_area = product.find('div', class_='RfADt')
        if nama_area:
            nama_link = nama_area.find('a')
            if nama_link:
                nama = nama_link.get_text(strip=True)
            else:
                nama = "Tidak ada informasi"
        else:
            nama = "Tidak ada informasi"

        # Gambar
        gambar_area = product.find('img')
        if gambar_area and gambar_area.get('src'):
            gambar = gambar_area.get('src')
        else:
            gambar = "Tidak ada informasi"

        # Link
        link_area = product.find('a', href=True)
        if link_area:
            link = link_area['href']
        else:
            link = "Tidak ada informasi"

        # Harga
        harga_area = product.find('span', class_='ooOxS')
        if harga_area:
            harga = harga_area.get_text(strip=True)
        else:
            harga = "Tidak ada informasi"

        # Diskon
        diskon_area = product.find('span', class_='IcOsH')
        if diskon_area:
            diskon = diskon_area.get_text(strip=True)
        else:
            diskon = "Tidak ada informasi"

        # Jumlah Terjual
        terjual_area = product.find('span', class_='_1cEkb')
        if terjual_area:
            terjual = terjual_area.get_text(strip=True)
        else:
            terjual = "Tidak ada informasi"

        # Lokasi
        lokasi_area = product.find('span', class_='oa6ri')
        if lokasi_area:
            lokasi = lokasi_area.get_text(strip=True)
        else:
            lokasi = "Tidak ada informasi"

        # Rating
        rating_area = product.find('div', class_='mdmmT')
        if rating_area:
            rating_stars = len(rating_area.find_all('i', class_='_9-ogB Dy1nx'))
            rating = f"{rating_stars}"
        else:
            rating = "Tidak ada informasi"

        list_nama.append(nama)
        list_gambar.append(gambar)
        list_link.append(link)
        list_harga.append(harga)
        list_diskon.append(diskon)
        list_terjual.append(terjual)
        list_lokasi.append(lokasi)
        list_rating.append(rating)
        print("-------")
        
    page += 1
    time.sleep(5)
    
driver.quit()

# DataFrame
df = pd.DataFrame({
    'nama': list_nama, 
    'gambar': list_gambar,
    'link': list_link,
    'harga': list_harga,
    'diskon': list_diskon,
    'terjual': list_terjual,
    'lokasi': list_lokasi,
    'rating': list_rating
})

# Save to Excel
with pd.ExcelWriter('nike-lazada.xlsx') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False)

print("Data telah berhasil disimpan!")
