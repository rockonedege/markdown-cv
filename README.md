# Markdown-cv Intro

An HTML template for writting single-file CV in Markdown

I just found myself starting to update my resume the first time in more than 5 years.
Having fallen into the habit of writing everything in markdown whenever possible, I thought it was a good idea to rewrite my resume in markdown format, for better maintainability and flexibility in the output.

With a bit of search, [strapdownjs](http://strapdownjs.com) was the closest thing I wanted.
It was all great until I started adding images to my projects experience. It does not embed the images into the html, which is OK if I am to host it. However, if I want to send the resume to a hunter or upload to a job site, I really need a one-file-for-all solution.

Here's what I came up.

Markdown-CV = [strapdownjs](http://strapdownjs.com) + images embedding.

## Prerequisites

- Python 3.5+

## How To

1. clone or download this repo.
2. put markdown files into the markdown folder.
3. run `python3 collect_themes.py && python3 run.py` on Ubuntu/Linux or
   run `python collect_themes.py && python run.py` from the console on Windows


 

