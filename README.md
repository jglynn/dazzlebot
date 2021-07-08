# dazzlebot

A crummy scraper that gathers lottery results

There are [betters options](https://www.magayo.com) for source data but they cost monies.

## Runtime

This is deployed as a Cloud Function to IBM Cloud and triggered on a scheduled interval there.

Provided

* [Python 3.7](https://cloud.ibm.com/docs/openwhisk?topic=openwhisk-runtimes#openwhisk_ref_python_environments)
* [Packages (cloudant, beautifulSoup4, etc.)](https://cloud.ibm.com/docs/openwhisk?topic=openwhisk-runtimes#python-packages)

## Running Locally

1. Install Python 3.7

2. Install required modules

    `python -m pip install -r requirements.txt`

3. Runs

    `python3 dazzle_scrape.py`

## Deploying as IBM Cloud Function

1. Install [IBM Cloud CLI](https://cloud.ibm.com/docs/cli?topic=cloud-cli-getting-started)

2. Login (youll be prompted to generate a token via browser)

    `ibmcloud login -sso`

3. Target the ORG and Space

    `ibmcloud target -o john.a.glynn@gmail.com -s dev`

4. Create the function (initially)

    `ibmcloud fn action create dazzle_scrape dazzle_scrape.py`

5. Push updates to the existing function

    `ibmcloud fn action update dazzle_scrape dazzle_scrape.py`

## Dependencies

Lotto records are persisted to a Cloudant instance named `lottodb` see [Cloudant Admin Console)](https://7e06cc45-79b7-4b54-b3b2-8d23b5f13268-bluemix.cloudant.com/dashboard.html#/database/lottodb/_all_docs)

The Cloud Function action is triggered periodically, history is available via [Cloud Function dashboard](https://cloud.ibm.com/functions/dashboard).
