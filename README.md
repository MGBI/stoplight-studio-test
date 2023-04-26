# stoplight-studio-test

### Testing
Run:
```
$ ./server.py
```
and open `http://localhost:8080`

### Building
Run:
```
$ ./bundle.sh
```

If you need things about X-Vendors Authorization (internal documentation), run:
```
$ INTERNAL_DOCS=1 ./bundle.sh
```

In case of success, `openapi-bundle.v1.yaml` and `redoc-static.html` will be
updated.
