import datetime


def set_cookie(response, key, value, time_expire=7):
    if time_expire == 7:
        max_age = 7 * 24 * 60 * 60  # 7 day
    else:
        max_age = time_expire * 60 * 60  # hour
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
    )
