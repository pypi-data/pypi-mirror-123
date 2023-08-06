""""""

import websub
from understory import sql, web
from understory.web import tx

model = sql.model(
    __name__,
    channels={"uid": "TEXT UNIQUE", "name": "TEXT UNIQUE", "unread": "INTEGER"},
    followings={
        "feed_id": "TEXT UNIQUE",
        "url": "TEXT UNIQUE",
        "callback_url": "TEXT",
        "added": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    },
)


@model.control
def search(db, query):
    """
    Return a list of feeds associated with given query.

    If query is a URL, fetch it and look for feeds (inline and external).

    """
    # TODO Use canopy.garden for discovery.
    # TODO If query is a keyword, make suggestions.
    url = query
    if not url.startswith(("http://", "https://")):
        url = f"http://{url}"
    resource = tx.cache.add(url)[1]
    feeds = []
    if resource.feed["entries"]:
        feed = {"type": "feed", "url": url, "name": "Unknown"}
        if resource.card:
            feed["name"] = resource.card["name"][0]
            try:
                feed["photo"] = resource.card["photo"]
            except KeyError:
                pass
        feeds.append(feed)
    for url in resource.mf2json["rels"].get("feed", []):
        feed = {"type": "feed", "url": url, "name": "Unknown"}
        subresource = tx.cache.add(url)[1]
        if subresource.card:
            feed["name"] = subresource.card["name"][0]
            try:
                feed["photo"] = subresource.card["photo"]
            except KeyError:
                pass
        feeds.append(feed)
    return feeds


@model.control
def preview(db, url):
    """Return as much information about the URL as possible."""
    resource = tx.cache.add(url)[1]
    items = []
    for entry in resource.feed["entries"]:
        item = {"type": "entry"}
        if "published" in entry:
            item["published"] = entry["published"]
        if "url" in entry:
            item["url"] = entry["url"]
        if "content" in entry:
            item["content"] = {
                "html": entry["content"],
                "text": entry["content-plain"],
            }
        if "category" in entry:
            item["category"] = entry["category"]
        if "photo" in entry:
            item["photo"] = entry["photo"]
        if "syndication" in entry:
            item["syndication"] = entry["syndication"]
        items.append(item)
    return {"items": items}


@model.control
def get_channels(db):
    """Return your subscription channels."""
    return [{"uid": "notifications", "name": "Notifications", "unread": 0}] + [
        {"uid": c["uid"], "name": c["name"], "unread": c["unread"]}
        for c in db.select("channels")
    ]


@model.control
def add_channel(db, name):
    """Add a subscription channels."""
    db.insert("channels", uid=name.lower().replace(" ", "_"), name=name)
    return tx.sub.get_channels()


@model.control
def follow(db, url):
    """Start following the feed at given url."""
    feed_id = web.nbrandom(9)
    callback_url = f"{tx.origin}/hub/{feed_id}"
    db.insert("followings", url=url, feed_id=feed_id, callback_url=callback_url)
    web.enqueue(websub.subscribe, url, callback_url)


@model.control
def get_following(db):
    """Return the feeds you're currently following."""
    return [{"type": "feed", "url": f["url"]} for f in db.select("following")]
