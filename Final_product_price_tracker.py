import requests
import smtplib
from bs4 import BeautifulSoup
from tkinter import *
import threading
from twilio.rest import Client


def check_price():
    url = url_entry.get()
    target_price = float(price_entry.get())
    email_id = email_entry.get()
    whatsapp_no = whatsapp_entry.get()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    if 'amazon' in url:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        product_title = soup.find_all('span', {'class': 'a-size-large product-title-word-break'})[0].get_text().strip()
        product_price = float(soup.find_all('span', {'class': 'a-price-whole'})[0].get_text().replace(',', ''))

    else:

        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        product_title = soup.find(name="span", class_="B_NuCI").text.strip()
        product_title = product_title.encode('ascii', 'ignore').decode()
        product_price = float(soup.find(name="div", class_="_30jeq3 _16Jk6d").text.replace(',', '').replace('₹', ''))

    if product_price <= target_price:
        send_email(email_id, url, product_title, product_price)
        send_whatsapp_message(whatsapp_no, url, product_title, product_price, target_price)

    threading.Timer(43200, check_price).start()


def send_email(email_id, url, product_title, product_price):
    # Connect to SMTP server
    smtp_server = "smtp.gmail.com"
    port = 587
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login("wolverinexmen494@gmail.com", "ornhddbgvugfhzzb")

    # Compose email message
    subject = "Price Alert!!!"
    body = f"The price for {product_title} fell down to {product_price}.\nBUY NOW!!!: {url}"
    msg = f"Subject: {subject}\n\n{body}"

    # Send email
    server.sendmail("wolverinexmen494@gmail.com", email_id, msg)
    print("Email alert sent successfully!")

    # Close SMTP server
    server.quit()


def send_whatsapp_message(whatsapp_no, url, product_title, product_price, target_price):
    account_sid = 'ACea64d2c93ab764e903089b16abb8003d'
    auth_token = '77e727a298f13b40d46ca7a9bebfdb1c'
    price_diff = (target_price - product_price)
    price_diff = float(price_diff)
    client = Client(account_sid, auth_token)
    client.messages.create(
        from_='whatsapp:+14155238886',
        body=f'The price for: {product_title} has fallen down. \nIt is cheaper by ₹{price_diff} than your desired price. \n The new price is ₹{product_price}.\n BUY NOW!!!: {url}',
        to=f'whatsapp:{whatsapp_no}'
    )
    print("Whatsapp alert sent successfully!")


# GUI Setup
root = Tk()
root.title("Product Price Tracker")

labelcolor = 'gray'
labelfont = ("Roboto", 12, "bold")
headfont = ("Roboto", 20, "bold")

url_label = Label(root, text="Product URL: ")
url_label.grid(row=0, column=0)

url_entry = Entry(root, width=50)
url_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

price_label = Label(root, text="Target Price: ")
price_label.grid(row=1, column=0)

price_entry = Entry(root, width=50)
price_entry.grid(row=1, column=1, columnspan=3, padx=10, pady=10)

email_label = Label(root, text="Email Address: ")
email_label.grid(row=2, column=0)

email_entry = Entry(root, width=50)
email_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=10)

whatsapp_label = Label(root, text="WhatsApp Number: ")
whatsapp_label.grid(row=3, column=0)

whatsapp_entry = Entry(root, width=50)
whatsapp_entry.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

track_button = Button(root, text="Start Tracking", command=check_price)
track_button.grid(row=4, column=1, padx=10, pady=10)

root.mainloop()
