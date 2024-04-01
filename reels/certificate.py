import ssl


def verify():
    ssl._create_default_https_context = ssl._create_unverified_context
