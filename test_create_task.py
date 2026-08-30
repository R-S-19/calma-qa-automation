import re
from playwright.sync_api import Page, expect

def login(page: Page):
    page.goto("http://localhost:5173/login")
    
    page.fill("#email", "test@email.com")
    page.fill("#password", "test123!")
    
    page.click("button[type='submit']")
    
    expect(page).to_have_url(re.compile(".*dashboard"))

def test_create_task(page: Page):
    login(page)
    
    page.get_by_text("Add task").click()
    page.get_by_placeholder("What do you need to do?").fill("Test Task")
    page.click("button[type='submit']")
    
    expect(page.get_by_text("Test Task")).to_be_visible()

def test_create_task_empty_title(page: Page):
    login(page)
    
    page.get_by_text("Add task").click()
    page.get_by_placeholder("What do you need to do?").click()
    
    button = page.locator("button[type='submit']")
    expect(button).to_be_disabled()