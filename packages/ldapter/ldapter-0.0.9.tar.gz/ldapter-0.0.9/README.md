ldapter
=======

A lightweight adapter API for python-ldap that provides simplified 
access to LDAP objects and attributes in native Python types, as well as
transparent read-through caching support using either a simple in-memory
cache or Redis.

Installation
------------

_Ldapter_ is available from PyPi and can be installed using `pip` or
whatever package management solution you prefer.

```shell
pip install ldapter
```

If you want to use `datetime` types to represent ISO-8601 formatted 
date strings in your LDAP entries, you'll also need to install
python-dateutil

```shell
pip install python-dateutil
```

Running the Demo
----------------

The source repository includes a demo. Of course, you'll need an LDAP
server and (optionally) a Redis cache in order to see _ldapter_ at work.
To make this easy, the repository includes everything you need to run
the demo using Docker and Docker Compose on your local workstation.

Start up the demo LDAP server and Redis cache in a terminal.

```shell
cd src/demo/docker
docker compose up --build
```

Depending on the version of Docker you have installed, you might find 
that you need to use `docker-compose` instead of `docker compose` in
the second line above.

Run the demo in another terminal.

```shell
cd src/demo/python
PYTHONPATH=../main/python python demo.py
```

Using the ldapter API
---------------------

The `Directory` object class is the top-level API.

```python
from ldapter import Directory
from ldapter import inet_org_person_schema

# Create a directory adapter with no cache.
directory = Directory(schema=inet_org_person_schema())
```

The `Directory.fetch_all` method returns a list of tuples, each of which 
contains a `DistinguishedName` and an `Entry`. The list will be empty if
the LDAP search returned no entries.

```python
from ldapter import Directory, Scope
from ldapter import inet_org_person_schema

directory = Directory(schema=inet_org_person_schema())
base = "dc=example,dc=org"
search_filter = "uid=fletcher"
for dn, entry in directory.fetch_all(base, Scope.SUBTREE, search_filter):
    print(dn)
    for k, v in entry.items():
        print(f"{k}: {v}")
```

A `DistinguishedName` is an object that implements a subset of the
dict protocol, allowing relative names (RDN) to be easily extracted.

An `Entry` is an object that uses the directory schema to transform
attribute values into useful Python data types. It implements a subset 
of the dict protocol, so that attribute values can be easily accessed
by name. A single-valued attribute has a common Python
data type (e.g. str, int, bool, datetime) or `DistinguishedName`.
A multi-valued attribute is a Python list whose values are one of
these types.

Caching Strategy
----------------

When an LDAP search is performed (via the `Directory.fetch_all` or
`Directory.fetch_one` methods) a resulting set of matching
LDAP entries is returned (which may be empty). Each entry has an LDAP distinguished name that serves as the
"primary key" for retrieving that specific entry. Each retrieved object
is placed into the cache using its distinguished name as the key. 
Additionally, the search base, scope, and filter expression specified for
the search are used as a key for a cache entry that contains the
set of distinguished names found by the search.

Conceptually you can think of the cache as a simple hash table 
where each entry has a key string and corresponding JSON value (an
array or object). If we perform a search using `dc=example,dc=org` 
as the base, SUBTREE as the scope, and a filter expression such as 
`(&(sn=Smith)(givenName=Mary*)`, the cache might have entries such as the
following:

| Key   | Value |
|-------|-------|
| s:dc=example,dc=org:SUBTREE:(&(sn=Smith)(givenName=Mary*) | \["uid=liz,dc=example,dc=org", "uid=mas87,dc=example,dc=org", "uid=msmith,dc=example,dc=org", ...] |
| e:uid=liz,dc=example,dc=org | { "uid": "liz", sn="Smith", "givenName": "Mary Elizabeth", ... } |
| e:uid=mas87,dc=example,dc=org | { "uid": "mas87", sn="Smith", "givenName": "Mary Anne", ... } |
| e:uid=msmith,dc=example,dc=org | { "uid": "msmith", sn="Smith", "givenName": "Mary", ... } |

The keys are prefixed with a namespace identifier based on the type
of the value. In this example, we use `s:` for a search result and `e:` 
for an LDAP entry. This makes the keys easy to distinguish when viewing
the cache and prevents any potential for collisions of keys representing
different types.

On a subsequent search request with the same base, scope, and filter 
expression, the cached list of distinguished names is retrieved, 
and those names are used to retrieve the corresponding LDAP entries from
the cache. In this way, different searches can share the same LDAP
entries in the cache -- any given LDAP entry is stored at most once.

No attempt is made to analyze the filter expression to predict what might
be returned by the LDAP server. Cached searches are simply the list of 
distinguished names that matched the given search criteria when the 
search was performed. This strategy works well for accelerating searches
that are performed repeatedly with the _same_ search criteria, but it
does nothing for a search whose criteria are even slightly different
from a previously executed search. As discussed below in [Optimizing
Single Entry Fetches](#optimizing-single-entry-fetches), additional
optimizations are included to accelerate the common case of fetching 
LDAP entries using the distinguished name as a primary key.

### Using a Cache

The module includes two cache providers.

1. A provider that acts as a Redis client.
2. A provider that uses a simple dict-based in-memory cache.

The simple dict-based cache is suitable mostly for testing. For 
optimal performance and persistence beyond the runtime of a Python
script, Redis is recommended.

To use a cache, specify the cache provider when creating a `Directory`.

```python
from ldapter import Directory
from ldapter import RedisDirectoryCache
from ldapter import inet_org_person_schema

# Create a directory adapter that uses a Redis cache
cache = RedisDirectoryCache(host="localhost", port=6379, db=0)
directory = Directory(schema=inet_org_person_schema(), cache=cache)
```

By default, the Redis cache provider uses the same time-to-live (TTL) 
for all LDAP search result lists and corresponding LDAP entries. In most
cases, you will want to differentiate the TTL for an entry, based on the
object type, since the probability that an entry will be updated in the
source LDAP server tends to vary based on object type. For example,
attributes about a person change relatively infrequently, while the
composition of groups of people changes more often and it may be
important to observe such changes when groups are used for 
authorization.

When constructing the cache object, you can specify a dict with
TTLs for different object types defined in the schema.

```python
from datetime import timedelta
from ldapter import Directory
from ldapter import RedisDirectoryCache
from ldapter import inet_org_person_schema

# Create a directory adapter that uses a Redis cache
cache = RedisDirectoryCache(
    host="localhost", port=6379, db=0,
    search_ttl=timedelta(minutes=15),
    entry_ttl={
        "inetOrgPerson": timedelta(hours=4)
    })

directory = Directory(schema=inet_org_person_schema(), cache=cache)
```

The `search_ttl` is used when caching the search criteria (base, scope, 
filter) and corresponding list of distinguished names that were 
retrieved by a search.

The `entry_ttl` dict is used when caching the LDAP entries returned by
a search.  By default, the Redis cache provider uses the `objectClass` 
attribute to distinguish LDAP entries by type. It checks the `entry_ttl`
dict for a TTL specific to the given type. If not found it uses the
`search_ttl` as the fallback.

### Configuring Redis

When using the Redis cache provider, the cache eviction policy is an
important consideration. When the cache encounters memory pressure, 
Redis can evict some cache entries to make room for new additions to
the cache. For LDAP, the Redis Least Frequently Used (LFU) eviction
policy tends to be good choice. The LFU policy uses an estimator of
cache entry usage frequency, and tends to prefer evicting cache entries
that are unlikely to be needed based on frequency, rather than last
access time.

All cache entries managed by _ldapter_ have a TTL that controls the
maximum lifetime of the cache entry -- whether a search result list or 
and LDAP object entry. To configure Redis to evict cache entries based 
on the LFU policy, configure a maximum memory size and specify the 
volatile LFU policy in the Redis configuration.

```
maxmemory 2gb
maxmemory-policy volatile-lfu 
```

### Optimizing Single Entry Fetches

When fetching a specific LDAP entry using the entry's distinguished 
name, the caching implementation can provide an additional optimization,
allowing a single object search to be satisfied from cache entries
created by prior searches.

A common situation where this optimization is useful is when a UI 
provides a means to search for a person using the person's name as
search criteria.

```python
people = directory.fetch_all(
    "dc=example,dc=org", Scope.SUBTREE, "(&(sn=Smith)(givenName=Mary*))")
```

Since the surname and given name are both quite common, this is likely
to return several matching entries. In the UI, the matches are presented
with other distinguishing attributes (middle name, department, etc)
allowing the user to select specific person. Often, after the specific
person has been selected, there will be a need to fetch the specific
person entry again soon after the original search is performed. The subsequent
search could be performed using a filter expression based on some unique
attribute of LDAP person entry.

```python
person = directory.fetch_one(
    "dc=example,dc=org", Scope.SUBTREE, "uid=liz")
```

This approach will indeed work. However, it will not necessarily
take advantage of the fact the person entry to be fetched was just placed
into the cache by the prior search. In fact, it will perform an LDAP
search unless the same search criteria (base, scope, filter expression) was 
performed recently to retrieve this person's LDAP entry.

However, if the subsequent fetch for this person object instead used
the distinguished name of the person entry, the previously cached 
entry would be returned without the need to perform an LDAP search.

```python
import random
from ldapter import Directory, Scope
from ldapter import RedisDirectoryCache
from ldapter import inet_org_person_schema

# Create a directory adapter that uses a Redis cache with default config
cache = RedisDirectoryCache()
directory = Directory(schema=inet_org_person_schema(), cache=cache)

# Find everyone named Mary Smith
people = directory.fetch_all(
    "dc=example,dc=org", Scope.SUBTREE, "(&(sn=Smith)(givenName=Mary*))")

# pick one at random
selected = random.randint(0, len(people))
selected_person = people[selected]

# get the DN from the selected tuple
dn = selected_person[0]

# this fetch will be always be satisfied from cache
person = directory.fetch_one(dn, Scope.BASE)
```

When the scope is BASE, the search is essentially a primary key search
and has no filter expression. If the cache contains the entry with the
requested DN, there's no reason to perform the search.
