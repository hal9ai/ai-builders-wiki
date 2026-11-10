---
title: "Persistent storage for many AI sandboxes"
description: "A block volume per sandbox stops scaling at the host's per-machine limit: give each sandbox a directory on a shared filesystem, and plan isolation, quotas and snapshots."
category: How-to
tags: [hosting, storage, costs]
order: 6
checked: 2026-11-10
---

<!-- NAV:START -->
[Home](README.md) › [How-to](Category-How-to.md) · Tags: [hosting](Tag-hosting.md), [storage](Tag-storage.md), [costs](Tag-costs.md)
<!-- NAV:END -->

# Persistent storage for many AI sandboxes

**Give each AI sandbox a directory on a shared filesystem instead of its own block volume once you need more than a handful per machine: a block volume attaches to one machine at a time, and hosts cap how many attach to each machine.** DigitalOcean, as one example, allows 15 volumes per Kubernetes node ([Volume limits](https://docs.digitalocean.com/products/volumes/details/limits/), checked 2026-11-10), so 16 sandboxes with a disk each cannot share that machine no matter how small they are.

A sandbox here means one [container](Glossary.md#container) running one user's or task's code: a coding agent, generated code, or a preview app. The question is how its files outlive the container.

## Why one disk per sandbox stops scaling

**A block volume is attached to a machine, not to a sandbox, and the attachment count is per machine.** Kubernetes defines `ReadWriteOnce` as "the volume can be mounted as read-write by a single node", and `ReadWriteMany` as "mounted as read-write by many nodes" ([Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes), checked 2026-11-10).

DigitalOcean is a concrete example of the limit ([Volume limits](https://docs.digitalocean.com/products/volumes/details/limits/), checked 2026-11-10):

- at most **15 volumes** attached to one Droplet or DOKS node;
- at most **5,000 volumes** per account;
- `$0.10 per GiB per month`, minimum 1 GiB, and charged whether attached or not ([Volume pricing](https://docs.digitalocean.com/products/volumes/details/pricing/), checked 2026-11-10).

So 15 is a density ceiling, not a total. Adding machines raises the total; it does not let a machine hold more volume-backed sandboxes. Other hosts have their own numbers; check theirs.

## What must survive a stop

**Files, not processes.** Stopping a sandbox ends its processes; resuming it means starting a new container on the old files. Decide which directory has to outlive the container: the workspace, configuration, conversation transcripts or database. If nothing does, no volume is needed at all.

## The options

| Approach | Shape | Scales to | Main cost or risk |
|---|---|---|---|
| Block volume per sandbox | One disk per container | The host's per-machine attachment limit | Idle disks still billed; per-volume minimums |
| Shared filesystem | One NFS share, one directory per sandbox | Hundreds per share | Shared throughput; quotas and isolation are yours to enforce |
| Object storage with a POSIX layer | Data in a bucket, metadata in a database | No per-machine limit | Metadata service and cache to run; small-file latency |
| Distributed storage on local disks | Replicated volumes across your machines | Your disks and nodes | Operational complexity |

### 1. A block volume per sandbox

Use this for a dozen or fewer sandboxes per machine, or for a database that wants a dedicated device and a hard size limit. Do not build a large sandbox fleet on it: you will run out of attachment slots while CPU and memory are still mostly free.

### 2. A shared filesystem

**One NFS server exports one filesystem; every sandbox mounts it and gets its own directory.** The sandbox count is no longer tied to attachment slots.

A managed example is DigitalOcean's Network File Storage ([features](https://docs.digitalocean.com/products/nfs/details/features/), [limits](https://docs.digitalocean.com/products/nfs/details/limits/), [pricing](https://docs.digitalocean.com/products/nfs/details/pricing/), checked 2026-11-10):

- NFSv4.1, POSIX permissions, VPC-only access;
- Standard tier `$0.15 per GiB per month`, minimum 50 GiB, up to 1 Gbps aggregate, 10,000 read / 7,000 write IOPS;
- up to 32 TiB per share, up to 32 clients per share, up to 5 snapshots per share;
- **access points** pin a client to a subdirectory: each gets its own mount IP and VPC, costs nothing extra, and a client "cannot navigate above it" ([access points](https://docs.digitalocean.com/products/nfs/how-to/manage-access-points/), checked 2026-11-10);
- **root squash is enforced**, so a workload running as root can read but not write; it must run as a non-zero user ([using NFS with DOKS](https://docs.digitalocean.com/products/kubernetes/how-to/use-nfs-storage/), checked 2026-11-10).

One trap: the DOKS NFS storage classes create **a new share for every PVC**, at the tier minimum ([dynamic provisioning](https://docs.digitalocean.com/products/kubernetes/how-to/provision-nfs-storage-dynamically/), checked 2026-11-10). Per-sandbox PVCs therefore recreate the cost problem at 50 GiB each. Create one share and one directory (or access point) per sandbox instead.

A self-hosted NFS server over a block volume has the same shape and no managed minimum. You then own the single point of failure, capacity enforcement and snapshots. It is reasonable for reproducible sandboxes; durable user data needs a redundant server or replicated storage.

### 3. Object storage with a POSIX layer

**File data goes to object storage and metadata to a metadata engine, and the result is mounted as a POSIX filesystem.** JuiceFS, for example, stores "file data ... in object storage" and "the corresponding metadata ... in the metadata engine", mounted in a POSIX-compatible way through FUSE ([architecture](https://juicefs.com/docs/community/architecture/), checked 2026-11-10).

This removes the per-machine attachment limit and suits many small files, but adds a metadata service that must stay available and a local cache on each machine. If the sandbox does not need a live filesystem, a simpler version is a snapshot: archive the workspace to object storage when the sandbox stops, restore it into a new sandbox later.

### 4. Distributed storage on your own disks

**Replicated block storage on machines you control gives you volumes without a cloud volume service.** Longhorn's native ReadWriteMany support exports each RWX volume through an in-pod NFSv4 server, requires an NFSv4 client on every node, and reclaims locks within a 90-second grace period after an abnormal share-manager termination ([RWX volumes](https://longhorn.io/docs/1.13.0/nodes-and-volumes/volumes/rwx-volumes/), checked 2026-11-10). It is the option when you own the hardware and need replication, not the simplest one.

On bare-metal Kubernetes, the default `local-path` provisioner creates node directories and, in its own words, has "No support for the volume capacity limit currently" ([local-path-provisioner](https://github.com/rancher/local-path-provisioner), checked 2026-11-10). There is no per-node volume count, but a sandbox's data is tied to that node and one sandbox can fill the disk.

## What to get right

- **A stable directory per sandbox.** `/sandboxes/<id>`. Stop keeps the directory; resume mounts it again. Do not delete the directory when the container stops.
- **Isolation is a path boundary, not a promise.** On a shared filesystem, sandboxes are neighbours. Use an access point, export or directory permission that cannot navigate above the sandbox's directory, and test it from inside a container.
- **Quotas.** A subdirectory has no size limit of its own, so one sandbox can fill the share. Use filesystem project quotas or per-directory accounting, or accept the risk deliberately.
- **Snapshots have a granularity.** On DigitalOcean they are per share, not per sandbox (checked 2026-11-10), so plan restores accordingly.
- **User mapping.** Root squash means root inside the container cannot write; run the sandbox as a non-zero user and set ownership when the directory is created.
- **An id that can resume is a credential.** If an unguessable sandbox id grants access to persisted files, give it a time limit, require the owner's key, or rotate it.
- **Idle data costs money.** A stopped sandbox still occupies storage. Set a time to live and delete abandoned sandboxes.
- **Throughput is shared.** Every sandbox on one share competes for its bandwidth; measure a many-small-files workload, which coding agents produce, before committing.

## Choosing

- **A dozen or fewer per machine, or a database:** a block volume per sandbox.
- **Many sandboxes that need a live POSIX filesystem:** one shared filesystem, one directory (or access point) per sandbox.
- **Many sandboxes, no live filesystem needed:** snapshot the workspace to object storage and restore into a new sandbox.
- **Your own hardware and a need for replication:** distributed storage such as Longhorn, with the operational work that implies.

## Related pages

- [The cloud, for AI apps](Cloud-for-AI-apps.md)
- [From idea to deployed AI app](Idea-to-deployed-AI-app.md)
- [Security for AI apps and agents](Security-for-AI-apps.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Agent](Glossary.md#agent), [Cloud](Glossary.md#cloud), [Coding agent](Glossary.md#coding-agent), [Container](Glossary.md#container), [Host](Glossary.md#host), [Snapshot](Glossary.md#snapshot).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-10.

- Kubernetes, [Persistent Volumes: Access Modes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes)
- DigitalOcean, [Volume limits](https://docs.digitalocean.com/products/volumes/details/limits/); [Volume pricing](https://docs.digitalocean.com/products/volumes/details/pricing/)
- DigitalOcean, [Network File Storage features](https://docs.digitalocean.com/products/nfs/details/features/); [limits](https://docs.digitalocean.com/products/nfs/details/limits/); [pricing](https://docs.digitalocean.com/products/nfs/details/pricing/); [access points](https://docs.digitalocean.com/products/nfs/how-to/manage-access-points/); [dynamically provision NFS storage](https://docs.digitalocean.com/products/kubernetes/how-to/provision-nfs-storage-dynamically/); [use NFS storage with Kubernetes](https://docs.digitalocean.com/products/kubernetes/how-to/use-nfs-storage/)
- JuiceFS, [Architecture](https://juicefs.com/docs/community/architecture/)
- Longhorn, [ReadWriteMany volumes](https://longhorn.io/docs/1.13.0/nodes-and-volumes/volumes/rwx-volumes/)
- Rancher, [local-path-provisioner](https://github.com/rancher/local-path-provisioner)

---

First version written with AI assistance from an architecture review on 2026-11-10, and checked against the [sources](#sources) on 2026-11-10. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
