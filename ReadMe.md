# How to Install
Execute the following steps in order to get the software up and running: 
1. Clone this repository
2. Create a virtual python environment with version 3.10.13
3. Execute the following command: ```pip install -r requirements.txt```
4. Copy the PDFs to analyze into ```./rule_based_pipeline/raw_pdf```\
   If the directory does not exist create it
5. Open ```config_for_rb``` and check if the directories with a ```TODO``` are set correctly.
6. Execute the ```main.py```

In order to make changes at the true data, it is easier to make changes in the ```Expected_Values_JSON``` since the data is there stored in a more structured way.\
Execute the ```main_conversion.py``` in order to refresh the ```Expected_Values_CSV``` directory. \
The entry point  ```main_analyze_page_in_pdfs.py``` can be used to analyze specific pages of a report.