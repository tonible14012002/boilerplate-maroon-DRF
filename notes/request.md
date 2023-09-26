# REQUEST OBJECT AND RESPONSE

## The HttpRequest
### attributes
- `.scheme` return `http or https`
- `.body` return bytestring body
- `.path` return full path to url string (not contain domain, querystring)
- `.path_info`
- `.method` return uppercased method string: `POST`, `GET`, ...
- `.encoding` return current encoding string (or None if using `DEFAULT_CHARSET` in settings.py) used to parsed form data.Ex: `utf-8`. Write to this attribute to change encoding, and all later access of data will use that new encoding.
- `.POST`: (QueryDict) Dictionaries-like object contain all form data (raw data => use `.body` instead)
- `.GET`: (QueryDict) Dictionaries-like object contain querySet parametters.
    > For DjangoRestFramework, use `.query_params` for a more correct namming (some other methods than GET http still can include queryParams)
- `.FILE`: Dictionary-like object containing all uploaded files.
- `.COOKIES`
- `.META`: Contains all HTTP headers
- `.headesr`: CaseInsensitive HTTP headers dict
 
### Header atttributes
- `.content_type`
- `.content_params`

## QueryDict
`QueryDict` is a subset of dictionary (contains all behavior of a dictionary)
### Additionals behavior
> One key can contain more than one value but access only return the latest value.
- `__init__` initialize QueryDict with a `querystring` or it initial value will be empty
- `.get()` return value of key, raise `MultiValueDictKeyError` if key does not exist. Return Default value if provided
- `.__contains__(key)` return True if key is set. ex: `if "foo" in request.GET`
- `.setdefault()`: just like dictionary but use `__setitem__()` internally
- `.update(other_dict)`: 
- `.items()`: Return iterator object
- `.copy()` Return deepCopy, this object will be mutable even if the orignal is not
- `.getlist(key, default=None)`
- `.setlist(key, list_)`
- `appendlist(key, item)`
- `.lists()`: [('a', ['1','2','3'])]
- `.pop()`
- `.dict()`
