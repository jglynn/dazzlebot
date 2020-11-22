# Build and Deploy Docker Image
```
docker build --tag=scraper .

docker login

docker tag scraper dazzlebot/scraper:v1

docker push dazzlebot/scraper:v1

```

# Push to IBM Cloud

```

ibmcloud login -sso
# Generate token

ibmcloud target -o john.a.glynn@gmail.com -s dev

# Initial deployment
ibmcloud fn action create scraper_action --docker dazzlebot/scraper:v1
ibmcloud fn action create <action_name> --docker <dockerhub_username>/<repo_name>:<tag_name>

# Subsequent deployments
ibmcloud fn action update scraper_action --docker dazzlebot/scraper:v1

```