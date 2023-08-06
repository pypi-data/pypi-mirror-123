# pygrafanaapi

pygrafanaapi contains some functions to facilitate the usage of grafana apis inside python modules.

[The source for this project is available here][src].

---

Example of importing grafanaapi inside a python module :

import os
from pygrafanaapi import GrafanaApi

url = "http://localhost:3000"
json = "apikey2.json"
itoken = os.environ.get("GRAFANA_TOKEN")
key, message= GrafanaApi.createApiKey(url, json, token=itoken)
print(key)
print(message)
keys = GrafanaApi.listApiKeys(url, token=itoken)
for key in keys:
print(key)

---

[packaging guide]: https://packaging.python.org
[distribution tutorial]: https://packaging.python.org/tutorials/packaging-projects/
[src]: https://github.com/stormalf/grafana_apis
[rst]: http://docutils.sourceforge.net/rst.html
[md]: https://tools.ietf.org/html/rfc7764#section-3.5 "CommonMark variant"
[md use]: https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
