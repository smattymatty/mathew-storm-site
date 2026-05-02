---
title: "Docker for Self-Hosting, Episode 1: What It Is and How to Run Other People's Stuff"
published: 2026-05-02
modified: 2026-05-02
featured: true
author: Mathew Storm
tags:
  - docker
  - self-hosting
  - sysadmin
  - linux
  - vps
  - tutorial
description: "A two-part Docker tutorial written for self-hosters, not software developers. Episode one covers what containers are, why they matter for self-hosting, and how to pull and run images from Docker Hub on a Linux VPS - no Dockerfiles, no builds, just running other people's stuff well."
keywords: "docker tutorial, docker for self-hosting, docker for sysadmins, docker on vps, docker on linux, learn docker, docker without dockerfile, docker container basics, docker hub, caddy docker, hello-world docker, docker volumes, docker restart policy, self-hosting tutorial, docker beginners"
schema_type: Article
og_type: article
sitemap_priority: 0.8
sitemap_changefreq: monthly
---

First of two episodes. This one gets you running other people's containers on a Linux VPS. Episode 2 covers Docker Compose, which is where self-hosting actually clicks.

---

## Who this is for

Most Docker tutorials are written for software developers. They assume you're building your own app, and Docker is the thing you wrap your code in so it can ship.

So those tutorials spend most of their time on building containers, and multi-stage deployment pipelines.

For us, a container is a sealed package somebody else maintains. Our job is to know how to run it, where to put its data, how to keep it alive, and how to debug it when it breaks. That's a completely different skill set, and most tutorials skip right over it.

{~ alert type="info" ~}
If you ever want to learn the build side, that's a separate skill for a separate day. Plenty of tutorials for it - [Docker Tutorial for Beginners](https://www.youtube.com/watch?v=b0HMimUb4f0) is a good starting point.
{~~}

---

## What containers solve

Say you want to run Mastodon, which depends on Ruby, Postgres, Redis, Node, ffmpeg, and a bunch of other stuff. Each of those requires a specific version and configuration.

You have two options.

{~ card title="Option one: by hand" ~}
Hunt down every dependency, install the right version of each one, hope none of them conflict with whatever's already on your system, and repeat the whole process on every upgrade.
{~~}

![Mastodon's required versions of Postgres and Ruby clashing with versions already installed on the VPS, plus Redis, Node, and ffmpeg dependencies stacked underneath](/static/tech/tutorials-docker/dependency-conflicts.png)

{~ card title="Option two: containers" ~}
A container is a sealed bag. Inside the bag is the app and every single thing it depends on, at exactly the right version.

The Mastodon bag has the right Ruby. The Postgres bag has the right Postgres. You don't install any of it on your host. You just run the containers.
{~~}

![Mastodon and Postgres each running in their own container on a single VPS, with Mastodon's Ruby and Redis dependencies sealed inside its bag](/static/tech/tutorials-docker/containers-as-bags.png)

This gives you three things that matter for self-hosting.

**Things stay separate.** Mastodon's Postgres can't fight your host's Postgres, because they're in different bags. Want to also run PeerTube with its own Postgres? Different bag. They don't see each other.

**Things are reproducible.** The bag you run on your laptop is the same bag running in production. No more 'but it works on my machine' excuses.

**Things are throwaway.** If a container gets weird, you delete it and run a new one from the same bag. You don't fix containers, you replace them. Servers used to be pets we'd name and care for. Containers are cattle.

---

## Containers vs VMs

A virtual machine pretends to be a whole computer. It has its own operating system kernel, and a dedicated amount of resources. They tend to be pretty heavy.

A container shares the host's kernel and just pretends to be its own isolated userspace. Much lighter.

![Side-by-side stack diagram: virtual machines run three apps with three guest OSes and three kernels above a hypervisor; containers run three apps over a single shared kernel and host OS via the Docker engine](/static/tech/tutorials-docker/vms-vs-containers.png)

A box that could run two VMs can comfortably run a dozen containers.

{~ alert type="info" ~}
Your VPS is likely a VM already. Your provider sliced up a physical server into virtual machines and rented you one. So you're going to be running containers inside a VM.
{~~}

Sounds like overkill, but it's the standard self-hosting setup. The VM gives you a clean Linux install. Containers give you isolation between apps inside it. There are two layers for two jobs.

---

## Linux and the terminal

Everything in this series happens in a terminal on a Linux box. No Docker Desktop.

Two reasons:

1. Your VPS doesn't have a GUI. You're going to be SSH'd into a remote machine. The sooner you get used to that, the better.
2. GUIs hide what's happening. You learn faster when you can see the moving parts.

Don't be scared of the terminal. Every command in this series is something you can copy and paste.

If you're on Windows or Mac at home, that's fine. The real work happens on a Linux server. For web hosting, Linux is the answer.

Windows can technically run containers, but with subtle differences and edge cases.

---

## Installing Docker (and a habit you need)

The fast way to install Docker is the official script:

```bash
curl -fsSL https://get.docker.com | sh
```

It works. Docker publishes it themselves. You'll be fine if you run it.

But piping a script straight from the internet into a root shell is not a habit you want to build. The script runs as root and does whatever it says, and you have no idea what that is unless you read it first. What if the domain name becomes compromised?

For a server you're going to run real things on, take a few extra minutes and follow the instructions in the [Docker docs](https://docs.docker.com/engine/install/) instead. You add their apt repo with a signed key and install the package. It's the same end result, you just know what got installed.

{~ alert type="info" ~}
Once you're running a server with people's data on it, "I know exactly what's on this box" is the baseline. Get used to it now while it's just you.
{~~}

Either way, come back when `docker version` prints two blocks of output.

```
Client:      ← the `docker` command you typed
 Version: 27.x

Server:      ← dockerd, the background process
 Engine:
  Version: 27.x
```

Client and Server are two separate programs. That's why you can restart Docker without your running containers dying.

One last thing once it's installed:

```bash
sudo usermod -aG docker $USER
```

Add your user to the `docker` group so you don't need `sudo` every time.

Log out, log back in. Or skip the disconnect with:

```bash
newgrp docker
```

That applies the group change to your current terminal immediately. Done.

---

## Prove it works, hello-world

You just installed Docker. Let's prove it actually runs.

There's an image on Docker Hub literally called `hello-world` that exists for exactly this purpose. It prints a message and exits. That's it. That's the whole image.

```bash
docker run hello-world
```

You'll see Docker do a few things.

```
Unable to find image 'hello-world:latest' locally   ← not cached
latest: Pulling from library/hello-world            ← fetching
Status: Downloaded newer image for hello-world      ← got it

Hello from Docker!                                  ← the container ran
```

It downloads something from the internet (we'll get to where in a minute), then starts a container from it. The container prints a message, then exits.

Read what the message actually says when you run it. It walks through the four steps that just happened: client talked to daemon, daemon pulled an image, daemon ran a container, container printed text and quit.

That's the whole loop you're going to use for everything from here on out.

Run it again:

```bash
docker run hello-world
```

This time it doesn't download. The thing it pulled the first time is already on your machine, cached in `/var/lib/docker/`. Pulls are a one-time cost per machine.

Now look at what's left over:

```bash
docker ps -a
```

`docker ps` on its own shows only running containers. The `-a` flag shows all of them, including stopped ones. We need `-a` here because hello-world has already exited. You'll see two stopped containers sitting there, one for each time you ran the command.

Containers don't clean themselves up.

Clean them up:

```bash
docker container prune
```

{~ alert type="info" ~}
`docker container prune` will ask if you're sure, then delete every stopped container. Running containers are safe.
{~~}

You just ran your first container, saw the pull-and-run cycle, and cleaned up after yourself. That's the whole rhythm of working with Docker.

---

## Images and containers

What you just downloaded was an image. What you ran from it was a container. Let's name the difference.

An image is a recipe. A container is a running instance, cooked from the recipe.

![A single read-only caddy:2 image on the left, with three independent running containers (web1, web2, web3) cooked from it on the right](/static/tech/tutorials-docker/image-vs-containers.png)

You can cook the same recipe many times. The image is read-only and gets stored once on disk.

Each container you run from it gets a thin writable layer on top, so it can keep its own state without messing up the original.

```bash
# Download the recipe
docker pull caddy:2

# Cook an instance from it
docker run -d --name web1 caddy:2

# Cook another from the same recipe
docker run -d --name web2 caddy:2
```

`web1` and `web2` are two separate containers running the same image. Stop one, the other keeps going. They don't know about each other.

This is also what you saw with hello-world. The first `docker run` pulled the image and ran a container from it. The second `docker run` skipped the pull (image already cached) and ran another container from the same image.

---

## Where images come from, and the `latest` trap

Images live in registries. Docker Hub is the default and the biggest. GitHub has one too (`ghcr.io`). Most self-hosting images you'll want are on Docker Hub.

An image's full name has four parts:

```
   docker.io / library / caddy : 2
       ↑         ↑        ↑    ↑
    registry  publisher  name  tag
```

Docker fills in the boring defaults. `caddy:2` becomes `docker.io/library/caddy:2`. `library` is what Docker Hub calls its "official" namespace.

For non-official images you write the publisher yourself:

```bash
docker pull dxflrs/garage:v2
```

{~ alert type="warning" ~}
The `latest` tag is just a label, and whoever publishes the image can move it to a new build whenever they want. So `mastodon:latest` today and `mastodon:latest` next month can be two completely different images.
{~~}

Use specific version tags for anything you care about:

```bash
# Don't
docker pull mastodon/mastodon:latest

# Do
docker pull mastodon/mastodon:v4.3.1
```

Upgrade on purpose. No surprises.

---

## Something real, Caddy serving an HTML page

Hello-world was a toy. Let's run something that actually does work.

Caddy is a web server. It's small, fast, configures itself for HTTPS automatically (we'll use that in Episode 2), and it's the front door of the stack we're going to build.

For now we're just going to use it to serve a single HTML file.

First, on your VPS, make a folder and put an HTML file in it:

```bash
mkdir -p /srv/site
echo "<h1>hello from my vps</h1>" > /srv/site/index.html
```

Now run Caddy and point it at that folder:

```bash
docker run -d \
  --name web \
  --restart unless-stopped \
  -p 80:80 \
  -v /srv/site:/usr/share/caddy \
  caddy:2
```

Walking through what's new.

`-d` means detached. The container runs in the background instead of hijacking your terminal.

Hello-world ran in the foreground because it exited immediately. A web server doesn't exit, so we put it in the background.

`--name web` gives the container a name. Without this, Docker generates one like `nostalgic_einstein`. Funny once, useless every time after.

`--restart unless-stopped` is the most important flag for self-hosting. When your VPS reboots, this container comes back automatically. We'll cover the other restart policies later.

`-p 80:80` maps port 80 on the host to port 80 in the container.

![Port 80 traffic flowing from a browser to the VPS to port 80 inside the Caddy container, labeled with the -p 80:80 mapping](/static/tech/tutorials-docker/port-mapping.png)

Format is `host:container`. When something hits port 80 on your VPS, Docker forwards it into the container.

`-v /srv/site:/usr/share/caddy` is a volume mount. It plugs your VPS folder into the container at the path Caddy looks for files.

![The VPS folder /srv/site mounted into the container at /usr/share/caddy, connected by a -v volume mount arrow](/static/tech/tutorials-docker/volume-mount.png)

This is the first hint of the big rule we'll name at the end. For now, just know your HTML file is reachable from inside the container.

`caddy:2` is the image, pinned to major version 2.

Check it's running:

```bash
docker ps
```

Open a browser, hit your VPS's IP, you should see your "hello from my vps" page.

{~ alert type="warning" ~}
Make sure you type `http://`, not `https://`. We're not doing TLS yet, that's Episode 2 territory.

Modern browsers (especially Chrome) will sometimes refuse to load `http://` and force an upgrade to `https://`, which fails because there's no cert. If your browser won't cooperate, drop into a terminal on your local machine and run:

```bash
curl http://<your-vps-ip>
```

That bypasses the browser entirely and proves the container is serving correctly. If you see your HTML come back, the container is working - the browser is just being protective.
{~~}

You're now serving a website from a container on a server you control.

If you want to change the page, edit `/srv/site/index.html` on the VPS and refresh the browser. No rebuild, no restart. The container reads the file off your host filesystem in real time.

That's the volume mount doing its job.

---

## Operating your container

You've got a web container running. Now you need to know how to inspect it, talk to it, and turn it off.

Three commands do most of the work.

{~ card title="docker logs - what is the container saying?" ~}
Your number one debugging tool. When something doesn't work, run logs first.

```bash
docker logs web              # everything since the container started
docker logs -f web           # follow live, Ctrl+C to stop watching
docker logs --tail 50 web    # just the last 50 lines
```
{~~}

{~ card title="docker exec - run a command inside the container" ~}
Most of the time you'll use it to get a shell.

```bash
docker exec -it web sh
```

`-it` means interactive plus terminal. Type `exit` or hit Ctrl+D to leave.
{~~}

{~ alert type="info" ~}
A lot of production images are deliberately tiny and don't have a shell. If `bash` doesn't work, try `sh`. If `sh` doesn't work either, the image is "distroless" and there's no shell at all, on purpose. Less stuff inside means less to attack.
{~~}

{~ card title="Stopping and removing" ~}
```bash
docker stop web        # gentle stop
docker start web       # start a stopped container
docker restart web     # both at once
docker rm web          # delete (must be stopped)
docker rm -f web       # force delete (stops it for you)
```

A stopped container is not gone. It's paused. `docker start` brings it back exactly as it was. `docker rm` is what actually destroys it.
{~~}

When your disk fills up six months from now, this is how you clean up:

```bash
docker container prune    # remove all stopped containers
docker image prune        # remove unused images
docker system prune -a    # nuke all of the above, aggressively
```

When we ran Caddy earlier we used `--restart unless-stopped` and I said we'd come back to it. Here's why.

By default, when your VPS reboots, your containers do not come back. They sit in stopped state and your website is down until you SSH in and start them by hand.

Your VPS will reboot eventually. Kernel update, provider maintenance, fat finger. It will happen.

The fix is the restart policy:

| Policy | What it does |
|---|---|
| `no` | Default. Never restarts. |
| `on-failure` | Restarts only if the container crashes. |
| `always` | Restarts always, even if you stopped it on purpose. |
| `unless-stopped` | Restarts always, except if you stopped it on purpose. |

`unless-stopped` is the right answer for self-hosting.

It means: if the box rebooted, bring my stuff back up. If I deliberately stopped this thing, leave it alone, don't fight me.

{~ alert type="success" ~}
Put `--restart unless-stopped` on every container you actually care about.
{~~}

---

## Volumes, the rule

That `-v` flag we used when running Caddy is the single most important habit in self-hosting. Time to name what it's actually for.

{~ alert type="warning" ~}
**Containers are throwaway. Your data is not.**

If you `docker rm` a container, everything inside it goes with it. Database, uploads, config. Gone.
{~~}

That's the whole point of containers being disposable. So your real data lives on the host filesystem, and gets plugged into the container at runtime with `-v`.

![VPS host filesystem holding /srv/site, /srv/db, and /srv/caddy/config, with a volume mount arrow connecting it to throwaway containers below](/static/tech/tutorials-docker/host-filesystem-rule.png)

Delete the container, run a new one with the same `-v` flag, and the new container picks up exactly where the old one left off. The data was never inside the container in the first place.

This is why you can stop being scared of `docker rm`.

{~ alert type="success" ~}
**Anything you'd cry about losing goes in a volume. Everything else is the container's problem.**
{~~}

That's the foundation. Episode 2 is Compose, where you describe your whole stack (app, database, cache, reverse proxy, all the volumes) in one file and bring it up with one command.

That's where self-hosting starts to feel good. See you there.