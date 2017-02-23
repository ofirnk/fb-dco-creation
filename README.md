# fb-dco-creation
Automate process of creating DCO campaigns

This script automates the process for creating DCO campaigns, asset feed and ad sets. There are 3 steps involved in running this script

1. Populate dco_inputs.csv with all the images, bodies, titles, descriptions and links for your DCO campaign. Ensure that you follow the format in the sample file in this repo

2. Open dco.py and edit input parameters on top to include required parameters including campaign_name, account_id, access_token, promoted_page_id and ad_set_budget

3. Open script in your terminal and run python dco.py -f dco_input.csv
