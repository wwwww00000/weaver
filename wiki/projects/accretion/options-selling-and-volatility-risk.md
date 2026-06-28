---
title: Option Selling And Volatility Risk
status: draft
page_type: research-thread
projects:
  - accretion
categories:
  - finance
  - options
  - volatility
source_bundles:
  - accretion/finance
  - unassigned/finance
created: 2026-06-28
updated: 2026-06-28
---

# Option Selling And Volatility Risk

The option-selling thread in Accretion is about whether volatility risk premium
can be harvested responsibly at personal scale.

The recurring lesson is that short-volatility strategies often feel stable
until they do not. They exchange frequent small gains for infrequent large
losses. That profile can be rational, but only if the exposure is sized,
bounded, and understood as insurance-selling rather than income generation.

## Volatility Risk Premium

Options can contain a premium because implied volatility often exceeds realized
volatility. Selling options attempts to harvest that difference.

The underlying alone does not give the same expected return source. Dynamic
replication shows how an option payoff can be hedged under idealized
conditions; it does not imply that spot-only trading captures the volatility
risk premium. The premium comes from selling optionality and taking the
associated gamma, jump, and tail risk.

## Single-Name Option Selling

Single-name option selling is more fragile than broad index option selling.
The source material emphasizes idiosyncratic gaps, earnings, litigation,
regulatory events, meme dynamics, and crowded retail trades. The apparent edge
in screenshots can reflect selection bias, leverage, bull-market drift, or
unreported tail exposure.

If explored at all, single-name option selling belongs in a bounded satellite
sleeve. It needs rules for:

- maximum notional and margin use;
- event avoidance or explicit event pricing;
- defined-risk structures where appropriate;
- assignment planning;
- realized drawdown and expected shortfall limits;
- post-trade attribution.

## Wheel Strategy

The wheel is a sequence: sell cash-secured puts, accept assignment if it
occurs, then sell covered calls against the shares.

The durable insight is not that the wheel is safe. It is that the strategy
combines short-volatility exposure with a long-equity bias and a stock-selection
constraint. It works best when the investor truly wants to own the underlying
at the effective entry level and is not forced to keep selling premium after
the thesis deteriorates.

For Accretion, the wheel is a possible object of study, not a default policy.

## Backtest Requirements

The option-selling sources suggest evaluating strategies with both retailable
and research lenses:

- sell-to-expiry or managed cash-secured-put PnL;
- delta-hedged straddle PnL as a cleaner volatility-risk-premium probe;
- realistic bid/ask fills and fees;
- earnings and event filters;
- margin-aware returns;
- drawdown, tail, and stress statistics;
- robustness sweeps over delta, DTE, exits, and spread penalties.

A useful result should survive transaction costs, event handling, and
survivorship-bias controls. If a backtest only works with generous fills or no
tail stress, it is not Accretion-grade evidence.

## Relationship To Quant

Reusable option-pricing, backtesting, implied-volatility, and data-engineering
methods may belong in [Quant](../../topics/quant.md). This page should keep the
personal-policy question visible: what risk, if any, should Accretion actually
own?

## Open Questions

- Is option-selling in Accretion an educational exercise, a bounded strategy,
  or merely context for evaluating bank products?
- What is the maximum acceptable loss for the entire satellite sleeve?
- Which strategies are plausible at personal scale after costs: cash-secured
  puts, spreads, collars, calendars, or none?
- Should option-selling be evaluated through a custom backtester before any
  capital is allocated?

## Source Map

- [Single Stock Option Selling](../../../ops/artifacts/chatgpt/6867eb0f-0504-8009-86bb-904d8cfcb365.md)
- [Retail option sellers success](../../../ops/artifacts/chatgpt/68e67423-7698-832a-b19a-afc3586e1eb9.md)
- [Short volatility replication](../../../ops/artifacts/chatgpt/68f44586-113c-8323-8ce3-06405a8f9d1a.md)
- [The Wheel Strategy Explained](../../../ops/artifacts/chatgpt/674898d0-c6b8-8009-b916-cbc095f4068c.md)
- [Options Trading at SIG](../../../ops/artifacts/chatgpt/6974e1fa-ba28-8323-a950-2ec1fc2bc646.md)
- [Personal Portfolio Framework](../../../ops/artifacts/chatgpt/684d9327-2dec-8009-8b2d-80d753048961.md)
