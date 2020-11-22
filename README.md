# dazzlebot
A cruddy scraper that gathers lottery results

There are [betters options](https://www.magayo.com) but they cost monies.

## Runtime

This is deployed as a Cloud Function to IBM Cloud and triggered on a scheduled interval there.

## Building & Running Locally

Install Python 3.8 or higher due to Cloudant client needs.

Install required deps via pip

`python -m pip install -r requirements.txt`

Run the program

`python3 dazzle_scrape.py`

## Deploying as IBM Cloud Function

The [IBM Python runtime](https://cloud.ibm.com/docs/openwhisk?topic=openwhisk-runtimes#openwhisk_ref_python_environments) provides a number of dependencies by default (including B4 and Cloudant) so we don't need to build this as a Docker container and can just push the script.

1. Install [IBM Cloud CLI](https://cloud.ibm.com/docs/cli?topic=cloud-cli-getting-started)

2. Login (youll be prompted to generate a token via browser)

    `ibmcloud login -sso`

3. Target the ORG and Space

    `ibmcloud target -o john.a.glynn@gmail.com -s dev`

4. Create the function (initially)

    `ibmcloud fn action create dazzle_scrape dazzle_scrape.py`

5. Push updates to the existing function

    `ibmcloud fn action update dazzle_scrape dazzle_scrape.py`

