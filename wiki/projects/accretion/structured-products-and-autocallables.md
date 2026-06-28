---
title: Structured Products And Autocallables
status: draft
page_type: research-thread
projects:
  - accretion
categories:
  - finance
  - options
  - structured-products
source_bundles:
  - accretion/finance
  - unassigned/finance
created: 2026-06-28
updated: 2026-06-28
---

# Structured Products And Autocallables

The Accretion structured-product thread is about understanding when a bank
product is a reasonable wrapper around a desired exposure, and when the wrapper
turns a simple risk into an opaque one.

The central source cluster is a worst-of equity-linked autocallable note with
monthly coupons, knockout mechanics, a European knock-in level, and physical
share delivery if the downside condition is breached.

## Mental Model

Treat the note as a funding instrument plus embedded options:

- fixed coupons while the note is alive;
- an issuer-friendly autocall feature that truncates future coupons in good
  states;
- a worst-of downside option that makes the investor short tail risk on the
  weakest underlying;
- issuer credit, fees, liquidity, and model spread embedded in the coupon.

This framing avoids the misleading version of the product: "high coupon with
some protection." A better framing is: "compensation for selling a specific
path-dependent and correlation-sensitive downside exposure."

## Terms That Matter

The important terms are not only the headline coupon.

The basket controls weak-link risk. More names and lower correlations usually
increase worst-of tail exposure. A basket should not be chosen merely because
each name is individually acceptable; the relevant question is whether the
worst delivered name is acceptable in the bad state.

The KO convention controls expected life. Daily-memory KO and per-stock memory
can make early redemption likely in benign states. That is not free yield,
because the feature is priced into the coupon and cuts off carry when the trade
is going well.

The EKI and strike relationship controls delivery frequency and loss shape. A
lower EKI than strike creates a grace band: some below-strike outcomes still
return principal. Setting EKI equal to strike better matches a clean "buy the
dip" intent, but increases conversion frequency.

Quanto, dividends, skew, correlation, and issuer assumptions all affect fair
coupon. They should be treated as model inputs rather than background detail.

## Quote Evaluation

A practical quote-review loop should produce a few interpretable diagnostics:

- fair coupon under a baseline model;
- issuer margin or equivalent coupon haircut;
- implied average correlation needed to match the offered coupon;
- sensitivity to volatility, skew, correlation, and jump or crash assumptions;
- probability and timing distribution of KO;
- tail scenario losses and delivery concentration.

The sources suggest a useful first-pass pricer: anchor marginal volatility to
listed option markets, impose a correlation matrix, simulate the autocallable
features, and compare the model-fair coupon to the offered coupon. The model
does not need to be perfect to be useful, but it should expose which assumption
the bank quote is asking the investor to accept.

## Design Principles

For carry-first exposure, prefer terms that do not merely maximize headline
coupon. Easy KO can turn the trade into a short-lived coupon clip plus
reinvestment problem. Bigger baskets and low-correlation names can increase
coupon by adding exactly the weak-link risk that should be avoided.

For "buy the dip" exposure, the cleaner instrument may be a single-name
cash-secured put, put spread, or one-name ELN at a true desired acquisition
level. Worst-of baskets are a poor fit when the investor only wants to own each
name under separate conditions.

## Open Questions

- What model assumptions should be standard in the Accretion pricer?
- Should implied correlation be the primary quote-comparison statistic?
- Which terms are non-negotiable for personal suitability: max basket size,
  strike, EKI, KO convention, tenor, or issuer?
- When is the product simpler than listed-options replication, and when is it
  merely more convenient?

## Source Map

- [Structured product analysis](../../../ops/artifacts/chatgpt/68e22384-0fc8-8321-b96a-8c7be5b770db.md)
- [Pricer Evaluation Approach](../../../ops/artifacts/chatgpt/6957d8f3-0b0c-8324-86c4-6c3d6dc473cc.md)
- [Numpy worst-of put pricer](../../../ops/artifacts/chatgpt/68f4ff45-27bc-8322-9921-bc8236488e39.md)
- [autocallables](../../../ops/artifacts/obsidian/autocallables.md)
- [Personal Portfolio Framework](../../../ops/artifacts/chatgpt/684d9327-2dec-8009-8b2d-80d753048961.md)
