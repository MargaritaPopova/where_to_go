## Настройка переменных окружения

Для локальной разработки настройка переменных окружения не требуется. Просто следуйте инструкциям [README](README.md)

Для разворачивания на production-сервере необходимо создать файл ```.env``` в той же папке, где лежит ```settings.py```,
и поместить туда следующие переменные.

[**SECRET_KEY**](https://docs.djangoproject.com/en/3.1/ref/settings/#secret-key)

**DEBUG**   
В продакшене всегда False

**AWS_ACCESS_KEY_ID**, **AWS_SECRET_ACCESS_KEY**  
Ключи для Amazon IAM. Необходимы для загрузки файлов на ваш S3 Bucket. Находятся в разделе My Security Credentials.
Прописывать их в ```settings.py``` не нужно.

**AWS_STORAGE_BUCKET_NAME**  
Название S3 Bucket'а

**AWS_S3_CUSTOM_DOMAIN**   
Название домена AWS CloudFront

**AWS_LOCATION**  
Название папки со статикой на сервере Amazon S3 (например, ```'static'```)

**Переменные для https**  
Установить в значения:  
SECURE_HSTS_SECONDS = <значение в секундах, например 31536000>  
SECURE_HSTS_PRELOAD = True   
SECURE_SSL_REDIRECT = True