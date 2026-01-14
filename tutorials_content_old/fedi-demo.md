# Django + ActivityPub: A Match Made in Heaven

## Why This Matters

The fediverse is growing. Mastodon crossed 10 million users. Threads is federating. PeerTube, Pixelfed, Lemmy - the ActivityPub ecosystem keeps expanding. This isn't a niche anymore.

If you're building with Django, you should know how to plug into this network. Not because it's trendy, but because it solves a real problem: your users are tired of creating accounts.

Think about it. Every new platform, every new service, every new app equals another signup form, another password, another email confirmation. Your users already have an identity. They already have followers, a profile, a presence. It lives at @them@their.instance.

Why make them start over?

ActivityPub lets you say: "Sign in with Mastodon." One click. They're in. Their fediverse identity is their identity on your platform. Their comments show up linked to their real profile. No new password to forget. No new username to squat.

This isn't just convenience. It's a shift in how we think about identity online. Instead of every platform owning a slice of you, you own your identity and bring it with you. The protocol serves the person, not the platform.

Django is already built for this. Swappable auth backends. Clean user model extension. Robust request handling. Everything you need to speak ActivityPub is already in the toolkit - you just need to know how to wire it up.

That's what this post is about.

## Part 1: Understanding ActivityPub (The Theory)

If you've built anything with Django, you already understand most of ActivityPub. The concepts map cleanly to things you know.

**Actors Are Just Users.**

An Actor in ActivityPub is like your Django User model - but public and fetchable via URL.

```python
# What you're used to:
user = User.objects.get(username='smattymatty')

# What ActivityPub does:
# GET https://techhub.social/users/smattymatty
# Returns JSON describing the actor
```

When you fetch an Actor, you get something like:

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Person",
  "id": "https://techhub.social/users/smattymatty",
  "preferredUsername": "smattymatty",
  "name": "Mathew Storm",
  "inbox": "https://techhub.social/users/smattymatty/inbox",
  "outbox": "https://techhub.social/users/smattymatty/outbox",
  "followers": "https://techhub.social/users/smattymatty/followers",
  "following": "https://techhub.social/users/smattymatty/following"
}
```

That id is the Actor's unique identifier across the entire fediverse. Think of it like a primary key, but global.

**Inbox and Outbox: How Messages Flow**

Every Actor has two endpoints: inbox and outbox. Think of them like mailboxes.

- **Outbox:** What the actor has posted publicly. GET this to see their content.
- **Inbox:** Where you send things TO that actor. POST here to deliver a message.

When you fetched my actor earlier, you saw:

```json
{
  "inbox": "https://techhub.social/users/smattymatty/inbox",
  "outbox": "https://techhub.social/users/smattymatty/outbox"
}
```

These are just URLs. Mastodon implements views at those URLs. If you wanted to see what I've posted:

```python
import requests

response = requests.get(
    "https://techhub.social/users/smattymatty/outbox",
    headers={"Accept": "application/activity+json"}
)
activities = response.json()
```

For authentication (our goal), you don't need to implement inbox or outbox. You just need to:

1. Look up the user's actor via WebFinger
2. Verify they control that identity (OAuth)
3. Create a local user linked to their ActivityPub ID

You only build your own inbox/outbox when you want federation - when you want activities from other servers to flow into your system, and your users' activities to flow out. That's Part 3.

**Activities Wrap Objects**

In ActivityPub, you don't just send content - you send actions. Every action is an Activity that wraps an Object.

You don't post a Note. You post a Create activity containing a Note:
```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Create",
  "actor": "https://techhub.social/users/smattymatty",
  "object": {
    "type": "Note",
    "content": "Hello fediverse!"
  }
}
```

The common Activity types:

- **Create** - new content (posts, comments)
- **Like** - someone liked something
- **Announce** - a boost/share
- **Follow** - subscription request
- **Accept / Reject** - response to a Follow
- **Delete** - content removal
- **Undo** - reverse a previous action (un-like, un-follow)

The common Object types:

- **Note** - short post (like a tweet/toot)
- **Article** - long-form content
- **Image / Video / Audio** - media
- **Person** - an actor (yes, actors are objects too)

Think of it like this: "**Actor** did **Activity** to **Object**." Mathew (Person) did Create (Activity) to "Hello fediverse!" (Note).

**WebFinger: The Phonebook**

Users don't type full URLs. They type handles like `@smattymatty@techhub.social`. WebFinger translates between the two.

Every fediverse server exposes a lookup endpoint at `/.well-known/webfinger`. You query it with an account identifier, it tells you where to find the actor.
```python
import requests

# User enters: @smattymatty@techhub.social
username = "smattymatty"
domain = "techhub.social"

# Query WebFinger
response = requests.get(
    f"https://{domain}/.well-known/webfinger",
    params={"resource": f"acct:{username}@{domain}"},
    headers={"Accept": "application/json"}
)

webfinger_data = response.json()
```

You get back:
```json
{
  "subject": "acct:smattymatty@techhub.social",
  "links": [
    {
      "rel": "self",
      "type": "application/activity+json",
      "href": "https://techhub.social/users/smattymatty"
    }
  ]
}
```

The `href` with `type: "application/activity+json"` is your actor URL. Now you can fetch the full actor object.
```python
# Find the ActivityPub link
for link in webfinger_data["links"]:
    if link.get("type") == "application/activity+json":
        actor_url = link["href"]
        break

# Fetch the actor
actor = requests.get(
    actor_url,
    headers={"Accept": "application/activity+json"}
).json()

# Now you have their full profile
print(actor["name"])  # "Mathew Storm"
print(actor["id"])    # "https://techhub.social/users/smattymatty"
```

This is the foundation of ActivityPub auth. User gives you a handle, you resolve it to an actor, you verify they control it. That's Part 2.

## Part 2: ActivityPub Auth for Django (The Implementation)
- WebFinger lookup
- Actor discovery
- OAuth flow with remote instance
- Linking to local User model
- Issuing JWTs like normal

## Part 3: Federated Comments (The Payoff)
- Receiving activities in your inbox
- HTTP Signatures for trust
- Storing and displaying comments
- Sending replies back out

## Part 4: What I Learned
- Gotchas
- Libraries that helped (or didn't)
- What I'd do differently