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





