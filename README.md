# SubZerod

- Discover sub-domains given a domain name
- Discover domain(s) given an IPv4 address

## Installation

```
pip install subzerod
```

## Usage

The command-line client works as follows:

### Discover sub-domains

```bash
subzerod lobste.rs
```

output:

```text
lobste.rs
l.lobste.rs
www.lobste.rs
```

### Discover domain(s) on an IPv4

```bash
subzerod 135.125.235.26
```

output:

```text
sanderf.nl
photos.sanderf.nl
```

### As a webservice

```
subzerod web
```

`http://127.0.0.1:9342/scan/135.125.235.26`

Responses are returned in JSON.

### Programmatically

```python
from subzerod import SubZerod

subdomains = await SubZerod.find_subdomains("lobste.rs")
domains = await SubZerod.find_domains("135.125.235.26")
```

## Legacy

SubZerod is a fork of [Sublist3r](https://github.com/aboul3la/Sublist3r) with some improvements:

- modern python 3
- asyncio instead of threading
- scans are considerably faster
- comes with a webserver because why not
