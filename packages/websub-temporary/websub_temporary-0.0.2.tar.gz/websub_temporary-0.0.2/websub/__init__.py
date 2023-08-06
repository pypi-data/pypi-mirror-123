"""
WebSub publisher and subscriber implementations.

> WebSub provides a common mechanism for communication between publishers
> of any kind of Web content and their subscribers, based on HTTP web hooks.
> Subscription requests are relayed through hubs, which validate and verify
> the request. Hubs then distribute new and updated content to subscribers
> when it becomes available. WebSub was previously known as PubSubHubbub. [0]

[0]: https://w3.org/TR/websub

"""

from understory import sql, web
from understory.web import tx

subscription_lease = 60 * 60 * 24 * 90
model = sql.model(
    __name__,
    # subscriptions
    subscribers={
        "subscribed": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
        "topic_url": "TEXT",
        "callback_url": "TEXT",
    },
)


def verify_subscription(topic_url, callback_url):
    """Verify subscription request and add follower to database."""
    verification_data = {
        "hub.mode": "subscribe",
        "hub.topic": topic_url,
        "hub.challenge": web.nbrandom(32),
        "hub.lease_seconds": subscription_lease,
    }
    response = web.get(callback_url, params=verification_data)
    if response.text != verification_data["hub.challenge"]:
        return
    tx.db.insert(
        "subscribers",
        topic_url=str(web.uri(topic_url)),
        callback_url=str(web.uri(callback_url)),
    )


def publish(hub_url, topic_url, resource):
    """"""
    # TODO don't hardcode "/subscriptions"
    for subscription in get_subscriptions(tx.db, topic_url):
        if subscription["topic_url"] != topic_url:
            continue
        print(
            web.post(
                subscription["callback_url"],
                headers={
                    "Content-Type": "text/html",
                    "Link": ",".join(
                        (
                            f'<{hub_url}>; rel="hub"',
                            f'<{topic_url}>; rel="self"',
                        )
                    ),
                },
                data=resource,
            ).text
        )


def subscribe(url, callback_url):
    """Send subscription request."""
    topic_url = web.discover_link(url, "self")
    hub = web.discover_link(url, "hub")
    print()
    print(topic_url)
    print(hub)
    print()
    web.post(
        hub,
        data={
            "hub.mode": "subscribe",
            "hub.topic": str(topic_url),
            "hub.callback": callback_url,
        },
    )


@model.control
def get_topics(db):
    return db.select("topics")


@model.control
def get_subscriptions(db, topic_url):
    return db.select("subscribers", where="topic_url = ?", vals=[topic_url])
