# strftime format text
#%a abbreviated weekday name
#%A full weekday name
#%b abbreviated month name
#%B full month name
#%c date and time representation appropriate for locale
#%d day of month as decimal number (01-31)
#%H hour (24-hour clock) as decimal number (00-23)
#%I hour (12-hour clock) as decimal number (01-12)
#%j day of year as decimal number (001-366)
#%m month as decimal number (01-12)
#%M minute as decimal number (00-59)
#%p current locale’s AM or PM indicator for 12-hour clock
#%S second as decimal number (00-59)
#%U week of year (Sunday as first day of week) as decimal number (00-53)
#%w weekday as decimal number (0-6; Sunday is 0)
#%W week of year (Monday as first day of week) as decimal number (00-53)
#%x date representation for current locale
#%X time representation for current locale
#%y year without century as decimal number (00-99)
#%Y year with century as decimal number
#%Z time zone name (no characters if no time zone exists)
#%G ISO 8601 year with century as decimal number
#%u ISO 8601 weekday as decimal number (1-7; Monday is 1)
#%V ISO 8601 week of year (Monday as first day of week) as decimal number (01-53)
#%f microsecond as decimal number (000000-999999)
#%z UTC offset in the form +HHMM or -HHMM (empty string if the the object is naive)

# 12-dec-2022
#%d-%b-%Y

# 12-dec-2022 12:00:00
#%d-%b-%Y %H:%M:%S

# 12-dec-2022 12:00:00.000000
#%d-%b-%2022 %H:%M:%S.%f

# 12-dec-2022 12:00:00.000000+0000
#%d-%b-%Y %H:%M:%S.%f%z

# 12-dec-2022 12:00:00.000000+00:00
#%d-%b-%Y %H:%M:%S.%f%z
