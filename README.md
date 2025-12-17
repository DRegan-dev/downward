# Downward - A Digital Descent Journal

![DW Logo](/staticfiles/images/downward-logo.png)

A Provide space for exploring emotional descents and personal reflections. Downward provides a structured yet flexible platform for users to document and analze their emotional journeys.

## Features
- **Descent Types**: Multiple guided descent types for different emotional explorations
- **Journaling**: Rich text journal entries with emotion tracking.
- **Reflection**: Structured reflection prompts for deeper understanding
- **Responsive Design**: Fully mobile-friendly interface
- **Privacy**: Secure, private journaling environment.
- **Mobile Navigation**: Smooth mobile experience with toggle menu

## Tech Stack

- **Backend**: Django 5.2.1
- **Frontend**: HTML5, CSS3, Javescript
- **Database**: PostgreSQL
- **Authentication**: Django Auth
- **Icons**: Font Awesome

## Design Decisions
- Typography
  - Primary: 'Bebas Neue', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif
  - Rationale: 'Bebas Neue' provides a bold, distinctive voice for headings and overall brand feel; 'Inter' and system fallbacks ensure legible rendering across devices with consistent        metrics and broad OS coverage.
  - Implementation: The stack is defined as a CSS variable `--font-primary` in [static/css/base.css]
- Color Palette
  - Primary: #0D6EFD (actions), Secondary: #6C757D (muted), Background: #FFFFFF, Text: #212529
  - Accessibility: All primary text/background combinations meet WCAG AA (contrast ≥ 4.5:1).
- Navigation & Flow
  - Clear CTA on homepage (“Begin your Descent”) leading to Start Descent.
  - Auth gates redirect unauthenticated users to login/register.
  - Post-actions provide toasts and clear routes back to history/details.
- Accessibility
  - Keyboard focus management for dialogs; ARIA `aria-live="polite"` on main content.
  - Button/icon labels with descriptive titles; tooltip fallbacks for non-Bootstrap contexts.

## Getting Started

### Home page
![Homepage Wireframe](staticfiles/images/downward-homepage-wf.png)
 The user lands on a homepage that immediately allows them to understand the purpose of the website. There is a call to action button inviting the user to "Begin your Descent".
 If the user is not logged in they will be redirected to the login page where they can log in or register for an account. 
 ![DW Homepage](/staticfiles/images/downward-homepage.png)

### Login/Register page
~![Lohin Wireframe](staticfiles/images/downward-login-wf.png)
The login page provides a login form where the user is asked to input their username and password.
![DW Login](staticfiles/images/downward-login-page.png)

 It also offers the user a chance to register for an account if they do not have an account yet.
 ![DW-Register](staticfiles/images/downward-register-page.png)

 The register page asks the user to input a username, email address and password once they register they are redirected back to the homepage to begin their journey. 

 ### New Descent page
The new descent page provides the user with a list of different descent types to choose from and a button to begin their descent session. 

![DW New Descent](staticfiles/images/downward-begin-descent.png)

### Journaling page
Upon beginning their descent the user is brought to the descent page where the are provided a content text box to share their thoughts and feelings. Beneath this there is a select box where a user can indicate their emotion level and an optional textbox for reflection on their experience. 

![DW Journal page](staticfiles/images/downward-journal-page.png)

### Journal History
When a User completes there session they are redirected to the journal history page where they can view their most recent and other past journalling session.

![JH-Wireframe](staticfiles/images/downward-jh-wf.png)

![DW Journal History](staticfiles/images/downward-journal-history.png)

On this page they have the option to view the session details, edit their answers or delete their session.
If the user decides to edit their session they are brough to a page exactly like the journal page they initially filled out except their answers are prepopulated in each field. 

If a user decides to delete their session, they are brought to the delete session page where they are asked to confirm deletion or they can cancel the deletion. 

![DW Delete Session](staticfiles/images/downward-delete-session.png)

Should a user just wish to view their previous entries of a particular session they can click the view details button and be brought to the session details page.


![DW Session Detail](staticfiles/images/downward-session-details page.png)

For a session that the user has not completed they are also given the option to start over if they so wish. 

## Admin functionality. 

![Admin DB Wireframe](staticfiles/images/downward-admin-wf.png)

Upon logging in, a superuser has can access all of the same pages as a site user but with the added functionality of being able to view an admin dashboard where they can create, read update and delete descent types and also view recent activity of other users. 

![DW Admin Dash](staticfiles/images/downward-admin-recent-activity.png)

![DW Admin Dash](staticfiles/images/downward-admin-descent-types.png)


### Database Schema

#### Entity Relationship Diagram (ERD)
```
+---------------+       +------------------+       +-------------+
|    User       |       |   DescentType   |       |   Entry     |
+---------------+       +------------------+       +-------------+
| id (PK)       |<----->| id (PK)         |       | id (PK)     |
| username      |       | name            |<----->| session (FK)|
| email         |       | description     |       | content     |
| password      |       | type            |       | timestamp   |
| date_joined   |       | is_active       |       | emotion_level
+---------------+       +------------------+       | reflection  |
        ^                                          +-------------+
        |                                                 ^
        |                                                 |
        |                                          +-------------+
        +---------------------------------------->| DescentSession|
                                                 +-------------+
                                                 | id (PK)     |
                                                 | user (FK)   |
                                                 | descent_type|
                                                 | status      |
                                                 | started_at  |
                                                 | completed_at|
                                                 | notes       |
                                                 +-------------+
```

#### Models
- **User**: Django's built-in user model
- **DescentType**: Defines types of descents (Emotional, Mental, etc.)
- **DescentSession**: Tracks user's descent sessions
- **Entry**: Individual journal entries within a session

## Testing

### Test Coverage
```
Coverage report:
Name                          Stmts   Miss  Cover
-------------------------------------------------
journal/__init__.py              0      0   100%
journal/admin.py                15      0   100%
journal/apps.py                  4      0   100%
journal/forms.py                25      0   100%
journal/models.py               25      0   100%
journal/templatetags/__init__.py 0      0   100%
journal/views.py               120      5    96%
-------------------------------------------------
TOTAL                           189      5    97%
```

### Running Tests
```bash
# Running All Tests
python3 manage.py test

# Run Specific Test Case
python3 manage.py test journal.tests.test_views
```
### Manual Testing
- [x] User Registration and authentication
- [x] Creating and managing descent sessions
- [x] Adding and editing hournal entries
- [x] Viewing Journal history
- [x] Admin interface functionality

- **[Authentication: Register]**
  - Purpose: Verify a new user can register successfully and is redirected appropriately.
  - Preconditions: User is logged out.
  - Steps:
    1. Navigate to `/accounts/register/` or click Register from the Login page.
    2. Enter unique username, valid email, and a valid password (and confirmation if present).
    3. Submit the form.
  - Expected Result: User account is created. User is redirected to the homepage and/or prompted to log in. Success toast appears.
  - Actual Result: Pass (2025-11-19). User created, redirected to homepage, toast displayed.

- **[Authentication: Login/Logout]**
  - Purpose: Verify that an existing user can log in and out.
  - Preconditions: Registered user exists.
  - Steps:
    1. Go to `/accounts/login/`.
    2. Enter valid username and password, submit.
    3. Click Logout from the navbar.
  - Expected Result: After login, user sees authenticated navbar and can access journaling features. After logout, user is redirected and session cleared.
  - Actual Result: Pass (2025-11-19). Authenticated navbar visible; logout clears session.

- **[Start New Descent]**
  - Purpose: Ensure a user can start a new descent session from `journal/start_descent`.
  - Preconditions: Logged-in user; at least one `DescentType` exists.
  - Steps:
    1. Navigate to Start New Descent.
    2. Select a descent type from `{{ form.descent_type }}`.
    3. Click "Begin Descent".
  - Expected Result: A `DescentSession` is created with status "in progress"; user navigates to the journaling page.
  - Actual Result: Pass (2025-11-19). Session created and redirected to journaling.

- **[Journaling: Create Entry]**
  - Purpose: Verify a user can add a journal entry with emotion level and optional reflection.
  - Preconditions: Active session exists.
  - Steps:
    1. On the journaling page, enter content in the text area.
    2. Select an emotion level.
    3. Optionally add reflection text.
    4. Submit the form.
  - Expected Result: Entry saved and visible in session details/history. Validation errors shown for missing required fields.
  - Actual Result: Pass (2025-11-19). Entry saved; invalid submission shows inline validation and prevents save.

- **[Journaling: Client-side Validation]**
  - Purpose: Confirm front-end validation/UX from `static/js/main.js` is applied.
  - Steps:
    1. Blur a required field without value.
    2. Attempt to submit with missing required inputs.
  - Expected Result: Required inputs gain `is-invalid` styling; first invalid field focused. Feedback messages shown/hidden appropriately.
  - Actual Result: Pass (2025-11-19). Visual feedback and focus behavior correct.

- **[Journal History: List]**
  - Purpose: Ensure completed and in-progress sessions display in history.
  - Preconditions: User has at least one completed and/or in-progress session.
  - Steps:
    1. Navigate to Journal History page.
  - Expected Result: Sessions are listed with actions: View, Edit, Delete; in-progress sessions marked accordingly.
  - Actual Result: Pass (2025-11-19). Actions available and functional.

- **[Session Detail: View]**
  - Purpose: Verify session detail page renders entries and meta information.
  - Steps:
    1. From Journal History, click View on a session.
  - Expected Result: Page shows descent type, timestamps, and entries in order.
  - Actual Result: Pass (2025-11-19). Details render correctly.

- **[Edit Session/Entry]**
  - Purpose: Ensure user can edit a session/entry and see pre-populated fields.
  - Steps:
    1. From Journal History, click Edit.
    2. Modify content and emotion level.
    3. Save changes.
  - Expected Result: Changes persist and are reflected on the detail/history pages.
  - Actual Result: Pass (2025-11-19). Changes persisted.

- **[Delete Session]**
  - Purpose: Validate delete confirmation flow and data removal.
  - Steps:
    1. From Journal History, click Delete.
    2. Confirm deletion.
  - Expected Result: Session deleted and removed from the list; success toast shown.
  - Actual Result: Pass (2025-11-19). Session removed as expected.

- **[Navigation: Mobile Menu]**
  - Purpose: Verify mobile nav toggle from `initializeMobileMenu()` works across pages.
  - Steps:
    1. Narrow browser to mobile width.
    2. Toggle menu open/close and click links.
  - Expected Result: Toggle icon switches between bars/times; menu closes on outside click and on link click.
  - Actual Result: Pass (2025-11-19). Behavior matches expected.

- **[Accessibility Basics]**
  - Purpose: Validate ARIA and keyboard flows per `initializeAccessibilityFeatures()`.
  - Steps:
    1. Tab through primary navigation and forms.
    2. Open any modal/dialog and test focus trap and Escape.
  - Expected Result: Logical tab order; focus trapped within modal; Escape closes if a close control exists.
  - Actual Result: Pass (2025-11-19). Behavior acceptable.

- **[Tooltips]**
  - Purpose: Verify Bootstrap and fallback tooltips from `initializeTooltips()`.
  - Steps:
    1. Hover/focus elements with `data-bs-toggle="tooltip"` and elements with `title` only.
  - Expected Result: Bootstrap tooltips appear when available; fallback tooltips show otherwise.
  - Actual Result: Pass (2025-11-19). Both paths verified.

- **[Static Files & Whitenoise]**
  - Purpose: Ensure static files are served in dev and by Whitenoise in production.
  - Steps:
    1. In dev, verify CSS/JS load.
    2. In production (Heroku), confirm static assets load and cache headers present.
  - Expected Result: Assets load without 404; hashed filenames with `CompressedManifestStaticFilesStorage` in production.
  - Actual Result: Pass (2025-11-19). Assets load; hashed files present on Heroku.

- **[Environment Configuration]**
  - Purpose: Verify environment-driven settings in `downward/settings.py`.
  - Steps:
    1. Set `DEBUG=True` locally and `DEBUG=False` on Heroku.
    2. Test behavior and error pages.
  - Expected Result: Debug toolbar/messages only in dev; friendly 500 in prod.
  - Actual Result: Pass (2025-11-19). Behavior matches expectations.

- **[Error Handling: 404/500]**
  - Purpose: Validate custom error templates (if present) or defaults.
  - Steps:
    1. Visit a non-existent URL for 404.
    2. Temporarily raise an exception in a view to trigger 500 (dev only).
  - Expected Result: Appropriate error pages render; no sensitive data leaked in production.
  - Actual Result: Pass (2025-11-19). Verified.

- **[Admin: CRUD Descent Types]**
  - Purpose: Ensure superuser can manage `DescentType` via Django admin.
  - Steps:
    1. Log in to `/admin/` as superuser.
    2. Create, edit, and delete a DescentType; verify list filters and recent activity.
  - Expected Result: CRUD operations succeed; changes reflect in user flows.
  - Actual Result: Pass (2025-11-19). CRUD verified.

- **[Cross-Browser Smoke]**
  - Purpose: Smoke test on Chrome, Firefox, Safari (latest stable).
  - Steps:
    1. Run through primary user flows on each browser.
  - Expected Result: No functional regressions.
  - Actual Result: Pass (2025-11-19).


## Deployment 

## 🚀 Local Development Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 13+
- Git
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/downward.git
cd downward
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/downward
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Set Up Database
1. Create a new PostgreSQL database named `downward`
2. Run migrations:
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## 🚀 Deployment to Heroku

### Prerequisites
- Heroku CLI installed
- Git installed
- Heroku account

### 1. Login to Heroku
```bash
heroku login
```

### 2. Create New Heroku App
```bash
heroku create your-app-name
```

### 3. Add PostgreSQL Add-on
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### 4. Set Environment Variables
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-production-secret-key
heroku config:set ALLOWED_HOSTS=.herokuapp.com
heroku config:set DISABLE_COLLECTSTATIC=1  # For first deploy
```

### 5. Deploy to Heroku
```bash
git push heroku main  # or master depending on your branch
```

### 6. Run Migrations
```bash
heroku run python manage.py migrate
```

### 7. Create Superuser
```bash
heroku run python manage.py createsuperuser
```

### 8. Set Up Static Files
```bash
heroku config:unset DISABLE_COLLECTSTATIC
git commit --allow-empty -m "Enable collectstatic"
git push heroku main
```

### 9. Open Your App
```bash
heroku open
```

## 🔧 Troubleshooting

### Static Files Not Loading
```bash
heroku run python manage.py collectstatic --noinput
heroku restart
```

### Database Connection Issues
```bash
heroku pg:info  # Check database status
heroku pg:reset DATABASE_URL  # Reset database (WARNING: deletes all data)
heroku run python manage.py migrate
```

### View Logs
```bash
heroku logs --tail
```
## Performance

#### Lighthouse Scores
![Lighthouse Score](staticfiles/images/downward-lighthouse-score.png)
 

## Known Bugs
There are no known bugs for this project but please reposrt any you may find. 

## Validation 

HTML has been validated using https://validator.w3.org with no issues found.

Javascript has been tested from this website has been tested with https://jshint.com with no issues found. 


## Acknoledgements 

Thank you to my mentor, student support services and family for all the help and support. 





