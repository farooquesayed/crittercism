__author__ = 'fsayed'

CRITTERCISM = "Crittercism"


class Constants(object):
    NIGHTLY = "nightly"
    pass

class BrowserConstants(Constants):
    COMMIT = "commit"
    SUBMIT = "submit"

class IOS(object):
    PLATFORM = '"platform-ios"'
    PREFIX = "IOS-"

class ANDROID(object):
    PLATFORM = '"platform-android"'
    PREFIX = "ANDRD-"
    pass

class HTML(object):
    PLATFORM = '"platform-html5"'
    PREFIX = "HTML-"

class WINDOWS(object):
    PLATFORM = '"platform-wp"'
    PREFIX = "WP-"

class ACCOUNT_TYPES(object):
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "ent"
    PROPLUS = "pro_plus"

class ALERT_TYPES(object):
    APP_LOADS = '0'
    CRASHES = '1'
    DAILY_USERS = '2'
    MONTHLY_USERS = '3'
    CRASH_PERCENTAGE = '4'
    DAILY_USERS_CRASH_PERCENTAGE = '5'
    USERS_WITH_MORE_THAN_0_CRASHES = '6'
    LATENCY = '7'
    HTTP_ERROR_RATE = '8'
    REQUEST_VOLUME = '9'
    DATA_IN = '10'
    DATA_OUT = '11'