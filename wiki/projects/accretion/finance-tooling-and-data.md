---
title: Finance Tooling And Data
status: draft
page_type: concept
projects:
  - accretion
  - genesis
categories:
  - finance
  - software
  - data
source_bundles:
  - unassigned/finance
  - unassigned/idea
  - accretion/current priorities
created: 2026-06-28
updated: 2026-06-28
---

# Finance Tooling And Data

Accretion has several software-shaped ideas. They should be kept visible, but
not confused with the investment policy itself.

The useful distinction is: tooling can improve execution, recordkeeping, and
analysis; it should not create permission to take more risk than the policy
allows.

## Card And Rewards Optimizer

The personal finance app idea is a rewards optimizer for credit-card spending.
The tractable part is a manual copilot:

- model cards, reward rates, caps, exclusions, and billing cycles;
- accept amount, merchant, category, currency, and date;
- recommend the card with the best marginal reward after cap usage;
- track remaining caps and explain why a card was chosen.

The harder version is automatic card routing for physical NFC payments. The
source notes conclude that ordinary Android apps likely cannot programmatically
select an existing Google Wallet card for the next tap. A true router card or
wallet would require payments infrastructure, issuer or processor integration,
and regulatory work. That belongs in a Genesis-style product feasibility track
if it is ever pursued.

## Options Data And Scanners

The options-data procurement notes are about building an unusual-options-flow
or option-selling research pipeline without full OPRA-scale data.

The practical path is nightly or end-of-day data first:

- contract-level prices, volume, open interest, greeks, and implied volatility;
- Parquet storage partitioned by date and symbol;
- contract selection and quote-cleaning rules;
- underlying-level anomaly aggregation before contract-level alerts;
- later upgrade paths for signed volume or intraday feeds.

For Accretion, this tooling supports two questions: whether option-selling
strategies have evidence after costs, and whether structured-product quotes are
reasonable relative to listed-option markets.

## Structured Product Pricer

The autocallable pricer is the most directly Accretion-specific tool. It should
answer:

- what fair coupon does the model imply?
- what implied correlation rationalizes the offered coupon?
- how sensitive is the quote to volatility, skew, correlation, and jump
  assumptions?
- how many coupons are expected under the KO convention?
- what tail losses or delivery outcomes dominate bad states?

This tool does not need to be institutionally perfect. It needs to turn opaque
sales quotes into explicit assumptions and comparable diagnostics.

## Relationship To Genesis

If any of these become actual software projects, [Genesis](../genesis.md)
should own the build plan. Accretion owns the finance objective and acceptance
criteria.

## Open Questions

- Which tool has the highest leverage: balance sheet tracker, card optimizer,
  structured-product pricer, or options-data pipeline?
- What data is sufficient for decision support, as opposed to curiosity?
- How should tooling outputs feed back into the investment policy statement?
- Are any of these tools worth building before the basic Accretion policy is
  written?

## Source Map

- [Personal finance app idea](../../../ops/artifacts/chatgpt/6a012e6a-f408-83ec-afd8-e3c638f3ce1d.md)
- [Options Activity Data Procurement](../../../ops/artifacts/chatgpt/68270ece-16ec-8009-98d2-540f572a0844.md)
- [Pricer Evaluation Approach](../../../ops/artifacts/chatgpt/6957d8f3-0b0c-8324-86c4-6c3d6dc473cc.md)
- [Numpy worst-of put pricer](../../../ops/artifacts/chatgpt/68f4ff45-27bc-8322-9921-bc8236488e39.md)
- [2026-W25 weekly project context](../../../ops/artifacts/obsidian/weekly-2026-W25.md)
