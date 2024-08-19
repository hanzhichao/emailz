# emailz

![Languate - Python](https://img.shields.io/badge/language-python-blue.svg)
![PyPI - License](https://img.shields.io/pypi/l/emailz)
![PyPI](https://img.shields.io/pypi/v/emailz)
![PyPI - Downloads](https://img.shields.io/pypi/dm/emailz)

Email Easy: easy use for sending emails

## Install
```
pip install emailz
```

## Simple Use
```
from emailz import email

email.config(user='ivan-me@163.com',password='***')
email.send(subject='Test', body='hi,\n,it is a test',receivers=['han_zhichao@sina.cn'])
```

## Use HTML
```
email.send(subject='Test', html='<h2>hi,it is a test</h2>',receivers=['han_zhichao@sina.cn'])
```

## Use Template file
```
email.send(subject='Test', template='tpl.html',receivers=['han_zhichao@sina.cn'])
```

## With attachments

```
email.send(subject='Test', attachments=['tpl.html'],receivers=['han_zhichao@sina.cn'])
```

## ToDo
- Smtp Server mapping
- @email decorators
- trigger, crontab or more features
- theme and templates to choose
