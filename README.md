# COA-COVID-app

This repository is a dash app showing the COVID reporting data and history for College of the Atlantic. The app is deployed at coa-covid.heroku.com from a local repo on Lio's laptop, but can be deployed from a different computer by anyone with admin privileges on the Heroku app.

The app gets its COA data from a Google Sheet owned by Dan, which is shared with Lio and the app's Google service account. The sheet is populated by responses from a Google Form, also editable by Lio and Dan. Deb should be the only one to fill out the form. The form collects email addresses, so one can visually check the sheet to ensure that Deb really is the only one filling in data.

Lio's COA email owns the service account, and Dan is also an authorized admin for it. The account is validated using OAuth 2.0. The Drive API key is stored securely as an environment variable in Heroku. The app accesses the key on its own.

Because of OAuth, this app can no longer run locally by anyone without the API key. To run it locally, obtain the API key from Lio or Heroku and store it in the same directory as app.py. Start a virtualenv (make sure to install all dependencies in requirements.txt) and set an environment variable `GOOGLE_APPLICATION_CREDENTIALS` by writing `export GOOGLE_APPLICATION_CREDENTIALS="<api_key_file>.json"` at the end of the /bin/activate file, and `unset GOOGLE_APPLICATION_CREDENTIALS` at the end of the `deactivate()` method. Then you should be able to run the app locally by running `python app.py` in the command line and visiting http://127.0.0.1:8050/ in your browser.

Maine and Hancock county data are sourced from the Maine CDC at this link: https://docs.google.com/spreadsheets/d/e/2PACX-1vRPtRRaID4XRBSnrzGomnTtUUkq5qsq5zj8fGpg5xse8ytsyFUVqAKKypYybVpsU5cHgIbY3BOiynOC/pub?gid=0&single=true&output=csv

For questions, contact Lio (or Dan, who will probably contact Lio).

