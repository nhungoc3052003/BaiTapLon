import time
import schedule
from PIL import Image, ImageEnhance, ImageFilter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import easyocr

# Tạo reader OCR
reader = easyocr.Reader(['en'])

# Hàm xử lý ảnh captcha
def xu_ly_anh_captcha(path):
    img = Image.open(path).convert("L")  
    img = img.filter(ImageFilter.MedianFilter()) 
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)  
    processed_path = "processed_captcha.png"
    img.save(processed_path)
    return processed_path

def tra_cuu_phat_nguoi(bien_so, loai_xe):
    driver = webdriver.Chrome()
    driver.get("https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html")
    time.sleep(10)

    try:
        # Nhập biển số xe
        bien_ks_input = driver.find_element(By.NAME, "BienKiemSoat")
        bien_ks_input.clear()
        bien_ks_input.send_keys(bien_so)

        # Chọn loại xe
        select = Select(driver.find_element(By.NAME, "LoaiXe"))
        select.select_by_value(loai_xe)

        # Chụp và xử lý Captcha
        captcha_img = driver.find_element(By.ID, "imgCaptcha")
        captcha_img.screenshot("captcha.png")
        processed_path = xu_ly_anh_captcha("captcha.png")

        # Nhận diện Captcha 
        results = reader.readtext(processed_path)
        captcha_text = results[0][-2] if results else ""
        print("Mã Captcha:", captcha_text)

        # Nhập mã captcha
        captcha_input = driver.find_element(By.NAME, "txt_captcha")
        captcha_input.clear()
        captcha_input.send_keys(captcha_text)

        # Bấm nút tra cứu
        driver.find_element(By.CLASS_NAME, "btnTraCuu").click()
        time.sleep(5)

        # # Lấy kết quả
        # soup = BeautifulSoup(driver.page_source, "html.parser")
        # table = soup.find("table")

        # if not table:
        #     print(f"Không có kết quả phạt nguội cho biển số {bien_so}.")
        # else:
        #     print(f"Kết quả phạt nguội cho biển số {bien_so}:")
        #     rows = table.find_all("tr")
        #     for row in rows[1:]:
        #         cols = row.find_all("td")
        #         if len(cols) >= 5:
        #             print(f"- Ngày: {cols[0].text.strip()}, Hành vi: {cols[2].text.strip()}, Địa điểm: {cols[3].text.strip()}")

    except Exception as e:
        print("Lỗi:", e)
    finally:
        driver.quit()

def chay_dinh_ky():
    bien_so = "98H1-186.44"
    loai_xe = "2"
    tra_cuu_phat_nguoi(bien_so, loai_xe)

# Lên lịch chạy
schedule.every().day.at("06:00").do(chay_dinh_ky)
schedule.every().day.at("12:00").do(chay_dinh_ky)

print("Chương trình đang chạy...")

while True:
    schedule.run_pending()
    time.sleep(30)
