# Doctor-Patient


To set up flask:

    1. create virtual environment with:  python -m venv venv

    2. activate virtual environment with: 
        a. For windows computer:  venv\Scripts\activate
        b. For linux computer: source venv/bin/activate

    3. pip install -r requirements.txt

To run the flask app:   `python app.py`

The strategy_design file location:   `utilities/user_role_manager.py`


How it works in strategy_design:

Upon registration, the first and second users shall be registered under the user_role `Doctor`, and any other user shall be registered under user_role `User`.

This will be seen in effect in the Doctor Recommendations page, as only users with the user role `Doctor` can post conclusions and recommendations, as well as upvote another doctor's feedback.

Email and phone have to be unique for each record.

Users have to be logged in to access any records further than the home page

The app runs on `http:127.0.0.1:5000`