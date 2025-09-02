# Web Scraper - Laptops

This Python project uses **Selenium** to scrape laptop details from a test e-commerce website.  
It collects the following data for each product:

Title  
Price  
Ratings  
Number of Reviews  
Product URL  
Description  

The data is saved in a JSON file (`output.json`) for further use.

## Features

- Headless browser support (runs without opening Chrome GUI)  
- Handless dynamic elements  
- Includes retry logic for product descriptions  
- Saves scraped data in structured JSON  


## Requirements

- Python 3.10+  
- Google Chrome installed  
- ChromeDriver (placed in the project folder)  

## Setup

**Clone or download the repository:**
****Cloning**
git clone https://github.com/yedukondaluchintala99-rgb/webscraper-.git
cd webscraper-

**Alternative if you don’t want to install Git**
You can download the repository as a ZIP:
Go to your GitHub repo page.
Click Code → Download ZIP.
Extract it to a folder and use it locally.

**Create a virtual environment:**
python -m venv env
# Activate it
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate

**Install dependencies:**
pip install -r requirements.txt

**How to Run**
python main.py

After the execution of the script, output will be saved in output.json. Please validate it.
