name: Update RSS Feeds

on:
  schedule:
    # Run every hour
    - cron: '0 * * * *'
  workflow_dispatch: # allows manual trigger

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install feedparser

    - name: Run RSS script
      run: |
        python scripts/generate_rss.py

    - name: Commit and push changes
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add rss/*.xml
        git commit -m "Update RSS feeds"
        git push
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
