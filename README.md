[![Build Status](https://travis-ci.org/learningpython08/flask-file-sharing.svg?branch=master)](https://travis-ci.org/learningpython08/flask-file-sharing)
### flask-file-sharing
A flask-based app to share file.
This is work in-progress.

### how to run

Below steps assume you're on your virtualenv.

```
$ pip install -r requirements.txt
$ python run.py

```

### how to upload file

```
$ curl --upload-file /tmp/screen_locked.png localhost:5000/myfile.png -s
http://localhost:5000/mnNYun/myfile.png

$ curl -X POST -F file=@/tmp/screen_locked.png localhost:5000
http://localhost:5000/Yix7Hf/screen_locked.png
```

