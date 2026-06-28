# Unassigned Math Mining Plan

Date: 2026-06-28

This is the routing layer for `unassigned/math` source artifacts. It is not
final wiki prose. Use it to decide which existing page, new page, or defer
bucket should consume each source.

Source inventory: [source-inventory.qmd](../clusters/2026-06-24/source-inventory.qmd)

## Method

Treat `unassigned/math` as applied mathematical infrastructure, not as a single
math hub. Most sources are regression, optimization, and validation notes that
belong under Quant/P12n. The smaller learning-resource tail belongs under
Revelation.

Destinations:

- `quant`: reusable regression algebra, validation formulas, optimization,
  covariance, solvers, ridge, and computational shortcuts.
- `p12n`: active structured-return modeling details, especially bilinear,
  low-rank, autoregressive, and tensor formulations.
- `revelation`: math-learning resources, problem-heavy texts, fatigue, and
  conceptual study practice.
- `whetstone`: only when a source is about cognitive load or learning method
  rather than math content.

Actions:

- `merge`: read during the next pass for the destination page.
- `dual-link`: split between a project-facing page and a reusable method page.
- `new-page`: create a candidate page before synthesis.
- `defer`: leave out of the next pass unless a later page needs it.
- `skip`: low-signal, duplicate, empty, or already mined into an existing page.

Priority means:

- `P1`: useful for the next page-deepening pass.
- `P2`: potentially useful, but not worth blocking the next pass.
- `P3`: likely skip or archive-only.

## Queue Order

| Queue | Count | First pass |
| --- | ---: | --- |
| Linear Regression Algebra And Solvers | 10 | Create a reusable Quant method page if the material is too detailed for existing validation/computation pages. |
| Ridge, Convex Optimization, And Internal Risk | 6 | Deepen Quant optimization, validation, and regularization pages. |
| Bilinear, Low-Rank, And Structured Regression | 5 | Deepen P12n n-linear and Quant structured-return pages. |
| Revelation Learning Resources | 4 | Deepen Revelation active-learning page and maybe add a resource note. |
| Already Mined Or Reference Only | 2 | Mark as source-map/reference material unless a later pass needs details. |

## Status

- 2026-06-28: Created initial routing plan for `unassigned/math`.
- 2026-06-28: Completed the linear regression algebra and solvers pass:
  [Linear Regression Identities And Solvers](../../wiki/topics/quant/linear-regression-identities-and-solvers.md),
  with links from [Quant](../../wiki/topics/quant.md),
  [Regression Stability And Validation](../../wiki/topics/quant/regression-stability-and-validation.md),
  and [Optimization And Computation](../../wiki/topics/quant/optimization-and-computation.md).
- 2026-06-28: Completed the ridge, convex optimization, and internal risk pass
  by deepening
  [Generalization And Regularization](../../wiki/topics/quant/generalization-and-regularization.md),
  [Regression Stability And Validation](../../wiki/topics/quant/regression-stability-and-validation.md),
  and [Optimization And Computation](../../wiki/topics/quant/optimization-and-computation.md).
- 2026-06-28: Completed the bilinear, low-rank, and structured regression pass
  by deepening
  [N-Linear Returns Models](../../wiki/projects/p12n/n-linear-returns-models.md)
  and [Structured Return Models](../../wiki/topics/quant/structured-return-models.md).
- 2026-06-28: Completed the Revelation math-learning resources and reference
  tail by deepening
  [Active Learning For Math And Physics](../../wiki/projects/revelation/active-learning-for-math-and-physics.md).

## Linear Regression Algebra And Solvers

Primary destination:
new Quant method page candidate
`wiki/topics/quant/linear-regression-identities-and-solvers.md`.

Secondary destinations:
[Regression Stability And Validation](../../wiki/topics/quant/regression-stability-and-validation.md)
and [Optimization And Computation](../../wiki/topics/quant/optimization-and-computation.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Block Orthogonal LS Solvers](../artifacts/chatgpt/68366f18-3ba4-8009-b87c-de2db683bc74.md) | merge | P1 | Block-orthogonal least-squares computation. |
| [CorrGCV Formulation Summary](../artifacts/chatgpt/6867e44f-d85c-8009-95f8-42ee9d7effda.md) | dual-link | P1 | Correlated GCV; link validation and computation. |
| [Exploring Parameter Space Solutions](../artifacts/chatgpt/672c38c2-8398-8009-8978-599861ac0f0c.md) | merge | P2 | Geometry of solution space; likely linear algebra intuition. |
| [Flat vs Sharp Minima in Linear Regression](../artifacts/chatgpt/67b3134f-cf50-8009-9265-a47222f57525.md) | merge | P1 | Linear regression geometry and Hessian interpretation. |
| [Least Angle Regression Explained](../artifacts/chatgpt/674c0a48-e938-8009-94fa-c205a686cd89.md) | merge | P2 | LARS and pathwise feature entry. |
| [Linear Regression Hessian Approximation](../artifacts/chatgpt/69d09be4-a6e8-83a0-8ea9-6ef0cbf1c7f1.md) | merge | P1 | Hessian versus gradient covariance. |
| [Linear Regression Tricks](../artifacts/chatgpt/685d3eb8-5fec-8009-a4e3-e5b91d369995.md) | merge | P1 | General OLS identities and shortcuts. |
| [LOOCV Error Efficient Computation](../artifacts/chatgpt/6811ed55-0e14-8009-9c2a-f4b586b27278.md) | dual-link | P1 | Efficient LOOCV; already overlaps validation page. |
| [Speeding Up Linear Regression](../artifacts/chatgpt/674f4736-7960-8009-a075-e546853a02f9.md) | merge | P1 | Solver and computational backend ideas. |
| [linear regression](../artifacts/obsidian/linear-regression.md) | merge | P2 | Obsidian reference notes. |

## Ridge, Convex Optimization, And Internal Risk

Primary destinations:
[Optimization And Computation](../../wiki/topics/quant/optimization-and-computation.md),
[Regression Stability And Validation](../../wiki/topics/quant/regression-stability-and-validation.md),
and [Generalization And Regularization](../../wiki/topics/quant/generalization-and-regularization.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Convex Optimization for ML](../artifacts/chatgpt/696c37d0-2dc8-8321-b04a-cd5880291cda.md) | merge | P1 | Convex optimization vocabulary and ML relevance. |
| [KKT Branch · Convex Optimization for ML](../artifacts/chatgpt/696c3b6e-f18c-8323-9762-31b04e290fd4.md) | merge | P1 | KKT branch of same source. |
| [IRLS Initialization Tricks](../artifacts/chatgpt/6a09778e-befc-83ec-9902-b880f91fea81.md) | dual-link | P2 | Optimization initialization plus gated/nonlinear regression. |
| [Optimal Ridge Penalty Computation](../artifacts/chatgpt/6876f4ab-b368-8009-9320-b72c69c8ce00.md) | merge | P1 | Analytic or efficient ridge tuning. |
| [Ridge Penalty Optimization](../artifacts/chatgpt/6876f4ac-77cc-8009-8b48-a1327e12c379.md) | merge | P1 | Ridge penalty and KKT-style optimization. |
| [covariance estimation](../artifacts/obsidian/covariance-estimation.md) | merge | P2 | Covariance estimation reference; may link regularization and risk. |

Status: complete. The pass added spectral ridge and fold-ratio shrinkage,
covariance shrinkage as risk control, KKT/proximal selection primitives, and
IRLS-style one-shot fitting for sigmoid gates.

## Bilinear, Low-Rank, And Structured Regression

Primary destinations:
[N-Linear Returns Models](../../wiki/projects/p12n/n-linear-returns-models.md)
and [Structured Return Models](../../wiki/topics/quant/structured-return-models.md).

Secondary destination:
[Optimization And Computation](../../wiki/topics/quant/optimization-and-computation.md)
for ALS and conditional-linear fitting details.

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Bilinear Autoregressive LSQ](../artifacts/chatgpt/6a200ef7-f71c-83ec-8c98-cceb472c5baa.md) | dual-link | P1 | Active structured-return model source. |
| [Bilinear Regression Closed Form](../artifacts/chatgpt/671d1f8c-7784-8009-953f-437c04a0766d.md) | merge | P1 | Closed-form bilinear regression discussion. |
| [Low-Rank Tensor Regression](../artifacts/chatgpt/68639f33-2858-8009-8a85-351d48135a5a.md) | merge | P1 | Low-rank tensor model formulation. |
| [Robust Regression Research Directions](../artifacts/chatgpt/67191c44-b954-8009-8e92-c5799747b9bb.md) | merge | P2 | Robust regression research ideas; likely quant method follow-up. |
| [ideas](../artifacts/obsidian/regression.md) | merge | P2 | Obsidian regression notes. |

Status: complete. The pass added fixed-mask bilinear attention equations,
amortized local regression versus sliding-window OLS, asymmetry versus
same-vector quadratic identifiability, low-rank tensor regression choices, and
categorical-product partial-pooling analogies. The robust-regression source is
already represented by the validation-aware regularization and bilevel sections
in the Quant pages.

## Revelation Learning Resources

Primary destination:
[Active Learning For Math And Physics](../../wiki/projects/revelation/active-learning-for-math-and-physics.md).

Secondary destination:
possible Revelation child page if source material becomes a durable reading map.

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Learning Advanced Math and Physics](../artifacts/chatgpt/7e133f9f-c25c-412b-8993-f64981624d37.md) | skip | P3 | Already mined into Revelation active learning. |
| [Mathematical Modelling Resources](../artifacts/chatgpt/696908b8-9e90-832a-a5a9-313769c74a30.md) | merge | P2 | Modeling resources; inspect for reusable reading map. |
| [Mental Fatigue: Reading Mathematics](../artifacts/chatgpt/f4d0ea68-cbba-4e8f-a5b8-8031e03a037d.md) | skip | P3 | Already mined into active learning and Whetstone/cognitive pass. |
| [Problem-Based Mathematics Texts](../artifacts/chatgpt/69884bb9-b520-83a0-83a0-5f7b8ab0d935.md) | skip | P3 | Already represented in active learning source map. |

Status: complete. The pass added a resource-backlog stance and mathematical
modelling drill lane to the Revelation active-learning page.

## Already Mined Or Reference Only

Primary destination:
source-map/reference only unless a later page needs exact details.

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [bookmarks](../artifacts/obsidian/mathematics.md) | merge | P2 | Math bookmark/reference note; inspect with Revelation resources. |
| [Iterative Greedy Feature Selection](../artifacts/chatgpt/69eb6c3d-c5d8-839e-97e0-8caedc8c6584.md) | skip | P3 | Already mined into Quant tabular/feature-search pages. |

Status: complete. The bookmarks source is represented in the Revelation
resource-backlog section and source map. The greedy feature-selection source was
already mined into the Quant feature-search material.

## Next Pass

`unassigned/math` is complete for this initial mining pass. Future work should
be just-in-time review and fleshing, not a mandatory bulk pass.
