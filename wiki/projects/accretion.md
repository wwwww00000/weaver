---
title: Accretion
status: draft
page_type: project-hub
projects:
  - accretion
categories:
  - finance
  - investing
  - portfolio
source_bundles:
  - accretion/finance
  - accretion/current priorities
  - accretion/project context
  - unassigned/finance
  - unassigned/personal
source_inventory: ops/clusters/2026-06-24/source-inventory.qmd
created: 2026-06-28
updated: 2026-06-28
---

# Accretion

Accretion is the project for personal finance, wealth accumulation, and the
operating system around capital allocation.

The project should separate durable finance principles from dated account
status. Balance snapshots, current product terms, card decisions, and brokerage
tasks are useful source context, but the wiki should preserve the policy layer:
what each bucket is for, what risks are acceptable, how structured products are
evaluated, and how active finance experiments stay bounded.

## Map

- [Balance And Portfolio Policy](accretion/balance-and-portfolio-policy.md):
  liquidity, safe allocation, growth allocation, satellite experiments, and the
  investment-policy layer that prevents ad hoc decisions.
- [Structured Products And Autocallables](accretion/structured-products-and-autocallables.md):
  worst-of ELNs, autocall mechanics, EKI/strike design, fair-coupon thinking,
  and quote evaluation.
- [Option Selling And Volatility Risk](accretion/options-selling-and-volatility-risk.md):
  volatility-risk-premium ideas, wheel and single-name option selling,
  short-vol replication limits, and backtest requirements.
- [Finance Tooling And Data](accretion/finance-tooling-and-data.md):
  card/rewards optimization, options-data procurement, and personal finance
  software ideas that support the project.

## Current Shape

Accretion has two layers.

The first layer is ordinary wealth management: track the balance sheet, protect
near-term liabilities, define safe and liquid buckets, and allocate only surplus
capital to long-horizon or experimental risk.

The second layer is finance-engineering curiosity: structured products,
autocallables, option selling, implied volatility, correlation, and quote
evaluation. This layer should be allowed, but it should live inside explicit
limits. The project is not "turn every financial curiosity into portfolio
risk."

The 2026-W25 weekly note points to near-term operational work: plan the bonus
transfer, review payment/card status, consider specific cards, add to the safe
allocation, and think about housing-related tooling. Those are current tasks,
not durable conclusions.

## Boundaries

Use [P12n](p12n.md) and [Quant](../topics/quant.md) when the material is about
trading research, statistical modeling, or reusable market-method ideas.

Use [Genesis](genesis.md) when the material becomes a product, app, data
pipeline, or software build. Finance tooling can start here, but implementation
plans may belong in Genesis.

Use Chronicle for life-planning context only when financial decisions intersect
with broader priorities or stress. Accretion should keep the finance policy
explicit rather than embedding it in journal material.

## Open Questions

- What is the canonical Accretion investment policy statement?
- How much capital belongs in liquidity, allocated safe assets, core growth,
  and active or experimental sleeves?
- Which structured-product terms are acceptable versus merely tempting?
- Should option-selling and autocallable experiments be treated as education,
  active investing, or a bounded satellite strategy?
- What tooling is worth building: balance sheet tracker, card optimizer,
  structured-product pricer, or options-data scanner?

## Source Map

- [balance](../../ops/artifacts/obsidian/accretion.md)
- [2026-W25 weekly project context](../../ops/artifacts/obsidian/weekly-2026-W25.md)
- [Personal Portfolio Framework](../../ops/artifacts/chatgpt/684d9327-2dec-8009-8b2d-80d753048961.md)
- [Structured product analysis](../../ops/artifacts/chatgpt/68e22384-0fc8-8321-b96a-8c7be5b770db.md)
- [Single Stock Option Selling](../../ops/artifacts/chatgpt/6867eb0f-0504-8009-86bb-904d8cfcb365.md)
- [source inventory](../../ops/clusters/2026-06-24/source-inventory.qmd)
