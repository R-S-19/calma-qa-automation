# Calma QA Automation Suite

Automated end-to-end test suite for [Calma](https://calma-beta.vercel.app), a task manager, habit tracker, and focus session app I built. This project demonstrates automated UI testing with Playwright, CI/CD via GitHub Actions, and real-world debugging of a live deployed application.

## What This Tests

- **Authentication**: successful login, invalid email, invalid password
- **Task creation**: successful task creation with a unique title, and validation that the submit button stays disabled with an empty title

## Tech Stack

- **Playwright** (Python) — browser automation
- **pytest** — test runner
- **pytest-rerunfailures** — automatic retries for network-related flakiness
- **python-dotenv** — environment variable management
- **GitHub Actions** — CI/CD, running the full suite on every push

## Running It Yourself

1. Clone the repo and install dependencies:

   ```bash
   pip install -r requirements.txt
   python -m playwright install
   ```

2. Create a `.env` file in the project root with the following:

   ```
   CALMA_URL=https://calma-beta.vercel.app
   CALMA_EMAIL=your-test-account-email
   CALMA_PASSWORD=your-test-account-password
   ```

3. Run the suite:

   ```bash
   python -m pytest calma_test.py test_create_task.py -v
   ```

## Real-World Issues Debugged Along the Way

- **SPA routing on Vercel**: direct navigation to routes like `/login` returned 404s until a `vercel.json` rewrite rule was added to redirect unmatched routes to `index.html`.
- **Strict-mode selector conflicts**: Playwright refused to click ambiguous text matches (e.g. "Add task" matching both a nav link and unrelated page copy); resolved with more precise `get_by_role()` locators.
- **Test data collisions**: repeated runs using a static task title caused later assertions to match multiple stale entries. Fixed by generating a unique, timestamped title per run.
- **CI flakiness**: occasional slow responses from the live backend (cold starts on serverless infrastructure) caused intermittent failures. Addressed with `pytest-rerunfailures` for automatic retries rather than just extending timeouts indefinitely.

## Notes

Tests run against a dedicated test account, not a real user account, to avoid polluting production data with test entries.
