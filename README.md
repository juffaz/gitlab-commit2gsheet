# Python Gitlab Commits to Excel and Google Sheets


## Running Locally

```shell
git clone https://github.com/juffaz/gitlab-commit2gsheet.git
cd gitlab-commit2gsheet && pip install -r req.txt 
export PRIVATE_TOKEN="GITLAB_TOKEN" 
export GITLAB_GROUPS="123,456" 
export GITLAB_DOMAIN="gitlab.com"
export WORKSHEET_KEY="GOOGLE_SHEET_KEY"
#### Change cred.json from Google Accout
python gitlab_commits2telegram.py
```


## Runnning with docker

```shell
# docker build
git clone https://github.com/juffaz/gitlab-commit2gsheet.git
cd gitlab-commit2gsheet && docker build . -t gitlab-commit2gsheet
docker run -e PRIVATE_TOKEN="GITLAB_TOKEN" -e GITLAB_GROUPS="123,456" -e GITLAB_DOMAIN="gitlab.com" -e WORKSHEET_KEY="GOOGLE_SHEET_KEY" -it gitlab-commit2gsheet 

# docker run from docker hub
docker run -e PRIVATE_TOKEN="GITLAB_TOKEN" -e GITLAB_GROUPS="123,456" -e GITLAB_DOMAIN="gitlab.com" -e WORKSHEET_KEY="GOOGLE_SHEET_KEY" -v $(pwd)/cred.json:/app/cred.json -it yuvenaliyt/python-gitlab-commit2gsheet


```
