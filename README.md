# Assignment Submission Portal

A small Flask portal where students submit their name, registration number, assignment title and a submission URL. Every push to GitHub runs automated tests, and the test report is sent to a local receiver that saves it as test-report.json.

## Run the application

    pip install -r requirements.txt
    python app.py

Open http://127.0.0.1:5000 in the browser.

## Run the tests

    python -m pytest -v

## Start the report receiver

    python receiver.py

The receiver listens on http://localhost:9000/report and saves every report it receives to test-report.json in the same folder.

## CI pipeline

GitHub Actions (.github/workflows/ci.yml) runs the tests on every push using a self-hosted runner. After the tests, send_report.py builds the report from the real test results and posts it to the local receiver.