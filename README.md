# Calma QA Automation Suite

Automated UI and API test suite for [Calma](https://calma-beta.vercel.app), a task manager, habit tracker, and focus session app I built. It tests the live deployed app with Playwright and pytest, and runs automatically in GitHub Actions on every push.

## What This Tests

**UI (end-to-end, Playwright)**

- **Authentication**: successful login, invalid email, invalid password
- **Task creation**: successful task creation with a unique title, and validation that the submit button stays disabled with an empty title

**API (requests)**

- Login returns a token
- Creating a task returns `201` and the response contains the title that was sent
- Empty and whitespace-only titles are rejected with a `4xx`
- Special-character titles (HTML tags, quotes, non-English text, emoji) are stored and returned unchanged
- A 500-character title never causes a server error (`< 500`)

## Test Design

- **Independent tests**: each test creates its own data using unique, timestamped titles
- **Self-cleaning**: fixtures with `yield` delete every task a test creates through the API, even when the test fails
- **Shared login**: one authentication fixture in `conftest.py` serves both UI and API tests
- **Real-data verification**: after a run, the test account is checked to confirm nothing is left behind

## Tech Stack

- **Playwright** (Python) — browser automation
- **requests** — API testing
- **pytest** — test runner, fixtures and parametrization
- **pytest-rerunfailures** — automatic retries for network-related flakiness
- **python-dotenv** — environment variable management
- **GitHub Actions** — CI/CD, running the full suite on every push

## Project Structure

```
calma_test.py          UI tests: login
test_create_task.py    UI tests: task creation
test_api.py            API tests
conftest.py            shared fixtures (login, test data cleanup)
pytest.ini             pytest settings and retry configuration
.github/workflows/     GitHub Actions workflow
```

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

   `CALMA_API_URL` is optional and defaults to the deployed backend.

3. Run the suite:

   ```bash
   python -m pytest -v
   ```

## Real-World Issues Debugged Along the Way

- **SPA routing on Vercel**: direct navigation to routes like `/login` returned 404s until a `vercel.json` rewrite rule was added to redirect unmatched routes to `index.html`.
- **Strict-mode selector conflicts**: Playwright refused to click ambiguous text matches (e.g. "Add task" matching both a nav link and unrelated page copy); resolved with more precise `get_by_role()` locators.
- **Test data collisions**: repeated runs using a static task title caused later assertions to match multiple stale entries. Fixed with unique, timestamped titles, and later with automatic cleanup of everything the tests create.
- **Missing dependency in CI**: tests passed locally but failed in CI with a `dotenv` import error, because the package was installed in my local environment but missing from `requirements.txt`. Regenerating the file fixed it.
- **CI flakiness**: the backend runs on a free hosting tier that sleeps when idle, so the first request can be very slow. Addressed with longer timeouts and `pytest-rerunfailures` as a safety net, while still treating retries as a way to manage flakiness rather than fix it.

## Notes

Tests run against a dedicated test account, not a real user account. Credentials are stored in a local `.env` file and in GitHub Secrets for CI, never in the repo.