# Filter at Delivery, Not at Generation

> When content has visibility tiers (draft, internal, public), filter at the **delivery boundary**, not during generation. Broken links, private items leaking, and stale drafts are symptoms of filtering in the wrong place.

## The principle

Content systems typically produce artifacts at many levels of maturity:

- Drafts that are not ready for public consumption
- Internal notes meant only for the team or a specific role
- Public items that should appear to anyone

A common mistake is to enforce visibility by **omitting** non-public items during generation — so they never enter the content store in the first place, or they enter under a different path, or they get deleted when status changes.

This breaks for several reasons:

- **References outlive visibility changes** — an item linked from another item may be downgraded to draft, but the link to it remains. The link now points to nothing.
- **Cross-references get fragile** — the system has to track, at generation time, which items can safely reference which others. Complexity explodes.
- **Review is expensive** — to verify "does this content leak private items?", you have to re-run the generation and diff.
- **History is lost** — the existence of an item is tied to its visibility state. Archived items disappear.

## The rule

Generate **everything**, with visibility metadata attached. Filter at the boundary that delivers content to its audience — API endpoint, rendered page, search index, RSS feed, whatever the delivery layer is.

```
all content + metadata ─┐
                        ├──> [filter] ─> public surface
visibility rules ───────┘        └─────> internal surface (if any)
```

The filter reads each item's metadata, compares against the audience rule, and either includes or excludes. The item itself never needs to be deleted, renamed, or moved.

## What this enables

- **Broken-link guard**: the filter at the public endpoint can also verify that every link in the emitted content points to another public item. If an item links to a draft, the link is either stripped or replaced with an anchor. No broken links reach the audience.
- **Downgrade safety**: moving an item from public to draft is a metadata change. No content is lost, no links rot at generation time. The next delivery pass reflects the new status.
- **Audit**: one layer decides visibility. You can inspect it, test it, reason about it. You don't need to trace visibility logic across the whole codebase.
- **Multiple audiences**: the same content store can serve different filtered views (public API, internal dashboard, team dump) without duplication.

## Implementation shape

At the delivery boundary:

```
for item in content_store:
    if not item.visible_to(audience):
        continue
    for link in item.links:
        if not link.target.visible_to(audience):
            link.strip_or_anchor()
    emit(item)
```

Two checks:
1. Is the item itself visible to this audience?
2. For each link the item contains, is the link's target visible to this audience?

The second check is where broken-link guards live. They belong at delivery because visibility can change over time, but the filter runs fresh at each delivery.

## When this pattern applies

Use it whenever:

- Content has tiers of visibility
- Items can reference each other (links, embeds, cross-references)
- Visibility of an item can change over its lifetime
- Multiple delivery surfaces exist (public site, internal tool, API)

Do not over-apply. If your system only has public content, there's no filter needed. This pattern pays off specifically when the cost of a leak or a broken link is real.

## The inversion

The wrong instinct is: "to make sure drafts don't leak, I'll not generate them." The right instinct is: "generate everything, then decide what each audience sees at the last moment."

The first instinct pushes complexity into every producer. The second concentrates it at one point. The second is much easier to verify and much harder to break.
