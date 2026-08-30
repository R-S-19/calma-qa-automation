import re
from playwright.sync_api import Page, expect

def test_successful_login(page: Page):
    page.goto("http://localhost:5173/login")
    
    page.fill("#email", "test@email.com")
    page.fill("#password", "test123!")
    
    page.click("button[type='submit']")
    
    expect(page).to_have_url(re.compile(".*dashboard"))
    
def test_login_with_wrong_email(page: Page):
    page.goto("http://localhost:5173/login")
    
    page.fill("#email", "wrong@email.com")
    page.fill("#password", "test123!")
    
    page.click("button[type='submit']")
    
    expect(page.get_by_text("Invalid email or password")).to_be_visible()       
    expect(page).to_have_url(re.compile(".*login"))
    
def test_login_with_wrong_password(page: Page):
    page.goto("http://localhost:5173/login")
    
    page.fill("#email", "test@email.com")
    page.fill("#password", "wrongpassword")
    
    page.click("button[type='submit']")
    
    expect(page.get_by_text("Invalid email or password")).to_be_visible()
    expect(page).to_have_url(re.compile(".*login"))