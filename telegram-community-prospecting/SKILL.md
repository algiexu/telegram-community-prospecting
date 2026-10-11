---
name: telegram-community-prospecting
description: Find and evaluate Telegram trading communities from seed channels, similar-channel recommendations and public search, review their latest 100 messages, and draft evidence-based partnership outreach. Use for community prospecting and outreach preparation, not automated messaging.
---

# Telegram trading community prospecting

Turn recent community discussions into a partnership decision and a short, personalized opening message. Optimize for relevant trading users and an actionable contact, not account counts or member totals.

## Inputs and setup

Use the user's target market, language, trading products, sender identity and exchange name. Reuse session context; ask only for missing information that affects selection. Never invent an identity or platform capability.

For Telegram setup and commands, read [references/telegram-tools.md](references/telegram-tools.md). The bundled reader and discovery helper use the user's own local credentials. They do not send messages, join groups or mark messages read.

## Discover relevant communities

1. Start with user-provided seeds or a few public searches tied to real trading behavior: futures trading, trade review, order flow, footprint, trading bots, or local-language equivalents. A tool keyword is a way to find users, not proof they developed that tool.
2. Use Telegram's similar-channel recommendations when available. They generally apply to broadcast channels; a group is not guaranteed to have recommendations. Inspect linked discussion groups for promising channels. If recommendations are unavailable, use public search or a public community link actually present in the source. Do not invent a universal similar-group API.
3. Expand promising seeds, deduplicating by Telegram ID and public username. Record discovery source and seed. Respect the user's requested scope; do not turn a single-link review into a discovery campaign. With no requested count, use a small initial batch of up to 10 candidates.
4. Consult any existing research/exclusion records. Previously rejected and already-reviewed communities do not become new leads just because another seed recommends them. Deduplicate contacts separately before preparing outreach; absence of local sending evidence does not prove no prior contact.

## Read and judge the latest 100 messages

Read up to 100 newest messages per candidate, including non-text messages in the sample count. Record read time, actual sample count, oldest/newest message dates and access restrictions. Display times in the user's timezone, preserving source timezone. Fewer than 100 available messages is an access/sample limitation, not proof of inactivity.

Assess these questions from the actual sample:

- Is there recent, substantive discussion of trading, positions, execution, strategy or risk? Distinguish human exchanges from bot notifications, repeated promotions and forwarded news.
- Do several identifiable participants ask and answer trading questions? One admin posting repeatedly does not demonstrate a lively community. Missing/anonymous author information stays unknown.
- What products and venues are discussed: crypto futures, spot, Forex, prop accounts, traditional futures or bots? BTC/ETH labels and leverage alone do not establish crypto-exchange futures usage.
- How much of the sample is advertising, repetitive solicitation or unrelated content? Explain the observed pattern rather than assigning arbitrary universal quality thresholds. Affiliate links alone do not disqualify a community.
- Is there a public owner/admin or partnership contact with supporting evidence? Do not identify an arbitrary member as the owner or enumerate private member details.

The reader marks media types; it does not inspect image or video contents. When a judgment depends on media, use an available authorized media reader and inspect at most the newest 10 relevant images unless the user requests another scope. Report actual coverage; unseen attachments remain unknown.

Choose one outcome: **worth contacting**, **needs clarification**, **skip**. Skip clear product mismatch, predominantly spam with no substantive trading discussion, demonstrated inactivity, or an unusable contact route. Incomplete evidence belongs under clarification, not a confident quality verdict. Member count, screenshots, claimed profits and affiliate links do not prove conversion ability.

## Extract the outreach strategy

From the sample, identify the object's role (trader/KOL, community, tool/project, exchange BD), one verifiable discussion or user need, and a plausible partnership angle. Separate observation from inference. For example, bot debugging suggests a technical discussion; API integration remains conditional on confirmed platform support. Forex or prop communities need crypto-demand clarification before a crypto-futures pitch.

Pick one main opening action: ask about partnership interest when crypto-futures fit is demonstrated; ask about spot/futures audience when fit is unclear; ask for the partnership contact when messaging a team. For an exchange BD peer, connect about their market/work rather than presuming they control a community.

## Fixed opening template

Preserve the structure **identity → evidence-based hook → one question**. Substitute only supported details and write naturally in the recipient's language:

> Hi [name], I'm [sender], handling [product] partnerships at [exchange]. I came across [community] and saw [specific discussion with evidence]. Would you be open to discussing a partnership for your [product] trading community?

When product fit is uncertain, replace the final question:

> Are members trading crypto futures, or is the community mainly focused on [observed product]?

When the contact is organizational:

> Who on your team handles exchange partnerships?

Do not claim long-term following, verified profits, user conversion or friendship without evidence. Do not insert rates, budgets, VIP benefits, activity rewards or integration promises from historical examples. If no reliable hook exists, mark it missing instead of generating artificial personalization. Drafts require user review and manual sending; this skill does not authorize outreach, CRM writes or scheduling.

## Deliver and keep records

For a single object, give a concise conclusion, the key evidence, unknowns and one draft with a full translation into the user's language. For batches, use these seven fields per object:

1. Channel / Link
2. Type
3. Evidence — message ID/link, date and short original quote with translation
4. Key Observations — include sample/read coverage and material unknowns
5. Personalization Hook
6. Final DM — recipient language plus full user-language translation; empty for Skip
7. Recommendation / Skip Reason

Keep failures separate; do not fill the quota with unreviewed accounts. Save research only in the designated local output directory. Keep draft, reviewed, sent and replied states distinct. Do not upload message exports or contacts with the reusable skill. Stop affected requests on Telegram rate limits and report the returned wait; do not retry through another account or promise completion.
