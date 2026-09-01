import os
import re
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

CALMA_URL = os.getenv("CALMA_URL")
CALMA_EMAIL = os.getenv("CALMA_EMAIL")
CALMA_PASSWORD = os.getenv("CALMA_PASSWORD")

def login(page: Page):
    page.goto(f"{CALMA_URL}/login")
    
    page.fill("#email", CALMA_EMAIL)
    page.fill("#password", CALMA_PASSWORD)
    
    page.click("button[type='submit']")
    
    expect(page).to_have_url(re.compile(".*dashboard"), timeout=15000)

def test_successful_login(page: Page):
    login(page)

def test_login_with_wrong_email(page: Page):
    page.goto(f"{CALMA_URL}/login")
    
    page.fill("#email", "wrong@email.com")
    page.fill("#password", CALMA_PASSWORD)
    
    page.click("button[type='submit']")
    
    expect(page.get_by_text("Invalid email or password")).to_be_visible(timeout=15000)
    expect(page).to_have_url(re.compile(".*login"))

def test_login_with_wrong_password(page: Page):
    page.goto(f"{CALMA_URL}/login")
    
    page.fill("#email", CALMA_EMAIL)
    page.fill("#password", "wrongpassword")
    
    page.click("button[type='submit']")
    
    expect(page.get_by_text("Invalid email or password")).to_be_visible(timeout=15000)
    expect(page).to_have_url(re.compile(".*login"))