# 200 – OK
# Everything is working. The resource has been transmitted in the message body.

# 201 – CREATED
# A new resource has been created.

# 204 – NO CONTENT
# The resource was successfully deleted. But, no response body was transmitted

# 400 – BAD REQUEST
# The request was invalid or cannot be served. The exact error should be explained in the error payload.

# 401 – UNAUTHORIZED
# The request requires user authentication.

# 403 – FORBIDDEN
# The server understood the request but is refusing it or the access is not allowed.

# 404 – NOT FOUND
# There is no resource behind the URI.

# 500 – INTERNAL SERVER ERROR API
# If an error occurs in the global catch blog, the stack trace should be logged and not returned as a response.