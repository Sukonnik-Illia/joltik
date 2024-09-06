Target: Google Ads Campaign
Fields:
 - username (db)
 - compaign_name (customer form)
 - google_client_id (should have in db and we can take it from Google ADS)
Flow:
- User clicks on create campaign
- we show form with data needed to be field



Regular sync?
Rows in states:
- new rows
to implement next we need to think on match field - some sheet.id
- deleted rows (present in db not present in table)
- edited rows

Second variant:
- remove all in db
- add new data


Sheets Cons:
- sheets give user to add remove columns (strictly defined fields)
- eventually consistent (we sync periodically or by click)

Ideas:
- do not edit data in DB, just sync from sheets
- one spreadsheet with data


Customer give us his spreadshit
