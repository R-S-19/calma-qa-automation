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
    
    expect(page).to_have_url(re.compile(".*dashboard"))

def test_create_task(page: Page):
    login(page)
    
    page.get_by_role("link", name="Add task").click()
    page.get_by_placeholder("What do you need to do?").fill("Test Task")
    page.click("button[type='submit']")
    
    expect(page.get_by_text("Test Task")).to_be_visible()

def test_create_task_empty_title(page: Page):
    login(page)
    
    page.get_by_role("link", name="Add task").click()
    page.get_by_placeholder("What do you need to do?").click()
    
    button = page.locator("button[type='submit']")
    expect(button).to_be_disabled()