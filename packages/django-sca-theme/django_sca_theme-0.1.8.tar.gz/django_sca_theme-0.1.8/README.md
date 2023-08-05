# Django Theme

Django theme 是一个自定义系统主题风格的库，可以生成前端所需要的配置信息。

## 安装

`pip install django-sca-theme`

## 配置

一. 将 `django_theme` 添加到 `INSTALLED_APPS`，就像这样：

```python

INSTALLED_APPS = [
    ...
    'django_theme',
]

```

二. 将 `django_theme` 的 URL 配置到项目的 `urls.py` 中：

```python
path("", include("django_theme.urls")),
```

三. 将设置好 `MEDIA_ROOT` 和 `MEDIA_URL` 到 `settings.py`:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / '/media'
```

四. 运行 `python manage.py migrate` 应用数据库修改

五. 运行 `python manage.py runserver`，创建一个配置.

六. 请求 `http://localhost:5000/api/system/theme` 获取主题
