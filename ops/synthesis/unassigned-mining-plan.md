# Unassigned Mining Plan

Date: 2026-06-28

This is the routing layer for source artifacts that have useful category labels
but no explicit project label. It is not final wiki prose. Use it to decide
which existing page, new page, or defer bucket should consume each unassigned
source.

Source inventory: [source-inventory.qmd](../clusters/2026-06-24/source-inventory.qmd)

## Method

Treat `unassigned/*` bundles as mining queues.

For each artifact, assign:

- `merge`: read during the next pass for the destination page.
- `dual-link`: split the artifact between a project-facing page and a durable
  topic page.
- `new-page`: create a candidate page before synthesis.
- `defer`: leave out of the next pass unless a later page needs it.
- `skip`: low-signal or not worth importing into the wiki.

Priority means:

- `P1`: useful for the next page-deepening pass.
- `P2`: potentially useful, but not worth blocking the next pass.
- `P3`: likely skip or archive-only.

## Queue Order

| Queue | Count | First pass |
| --- | ---: | --- |
| `unassigned/quant` | 92 | Route into existing P12n and Quant pages. |
| `unassigned/ai` | 34 | Route into Genesis, P12n, and AI topic candidates. |
| `unassigned/cognitive` | 54 | Route into Whetstone, Chronicle, and cognition topic candidates. |
| `unassigned/personal` | 46 | Route into Chronicle, Accretion, and life operations candidates. |
| `unassigned/writing` | 28 | Route into Chronicle, Conjuration, and writing topic candidates. |
| `unassigned/math` | 27 | Route into Revelation, Quant, and math topic candidates. |
| `unassigned/drawing` | 22 | Route into Conjuration and drawing topic candidates. |

## Unassigned Quant Routing

The `unassigned/quant` bundle should deepen the existing P12n and Quant pages
rather than produce a new top-level unassigned page.

Status:

- 2026-06-28: Completed first page-deepening pass for
  [adaptive filters and EMA](../../wiki/topics/quant/adaptive-filters-and-ema.md).
- 2026-06-28: Completed temporal evidence and covariance pass for
  [temporal evidence](../../wiki/topics/quant/temporal-evidence.md).
- 2026-06-28: Completed structured returns and p12n signal-study pass for
  [temporal returns experiments](../../wiki/projects/p12n/temporal-returns-experiments.md)
  and [structured return models](../../wiki/topics/quant/structured-return-models.md).

### Adaptive Filters And EMA

Primary destination:
[adaptive filters and EMA](../../wiki/topics/quant/adaptive-filters-and-ema.md).

Secondary destinations when useful:
[P12n sequence-model analogies](../../wiki/projects/p12n/sequence-model-analogies.md)
and [Obelisk dynamic EMA decay](../../wiki/projects/obelisk/dynamic-ema-decay.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Adaptive Regression Models Research](../artifacts/chatgpt/67bf16db-de44-8009-a053-1fb7756e3302.md) | merge | P1 | Online and adaptive regression framing. |
| [Bias correction techniques EMA](../artifacts/chatgpt/69381b2a-a4d4-832b-94f5-7cc7c01d20e3.md) | merge | P1 | EMA initialization and correction detail. |
| [Branch - RTRL-driven Regressor Design](../artifacts/chatgpt/69ae20aa-8790-839f-9ad3-bb05bc4c5ccb.md) | dual-link | P1 | Adaptive-filter and sequence-model bridge. |
| [Decay bounds for poles](../artifacts/chatgpt/68341b7f-25b4-8009-8b87-cf7e7adee187.md) | merge | P1 | Stability bounds for decay parameters. |
| [Disjoint Moving Averages](../artifacts/chatgpt/6994248e-1824-83a1-b6c7-76a8ecf35b09.md) | merge | P1 | Fixed temporal basis construction. |
| [EKF Online Regression Analogy](../artifacts/chatgpt/69b7c1ef-0bc8-839d-8d99-a5ecace216c0.md) | merge | P1 | Kalman view of online regression. |
| [EMA Computation Efficiency](../artifacts/chatgpt/69cfd35f-b000-839d-83da-034106b7584c.md) | merge | P1 | Implementation detail for causal features. |
| [EMA Smoothing in Regression](../artifacts/chatgpt/68075640-8f14-8009-893a-cb2a34f24c1a.md) | merge | P1 | Regression use of smoothed state. |
| [EMA State Saturation](../artifacts/chatgpt/6a22202a-b30c-83ec-9c6d-ade434282e17.md) | merge | P1 | Failure mode for saturated filter state. |
| [EMA Transformation for Regression](../artifacts/chatgpt/6752bf06-1800-8009-be1a-4dd1718c840b.md) | merge | P1 | EMA as feature transform. |
| [Fast and Slow Weights](../artifacts/chatgpt/69a5b11a-3d38-839d-a554-ad4bb56bba78.md) | dual-link | P1 | Fast-weight analogy for sequence models. |
| [Fitting EMA Half-Lives](../artifacts/chatgpt/67b178be-a9a8-8009-bb82-826da560e0c8.md) | merge | P1 | Decay fitting and diagnostics. |
| [Global decay offset trick](../artifacts/chatgpt/69ccc4ca-aa38-839a-86d4-68ea6a0550e1.md) | merge | P1 | Parameterization trick for decay families. |
| [Inverse EMA in Regression](../artifacts/chatgpt/67cf90b3-984c-8009-9b64-df5238549eb5.md) | merge | P1 | Inverting smoothed features or states. |
| [Kalman Filter State-Space Integration](../artifacts/chatgpt/69abc878-f2a0-83a0-b672-01b48fb393d9.md) | merge | P1 | State-space formulation. |
| [Kalman filter update intuition](../artifacts/chatgpt/69b21439-56cc-8399-9022-6f58147ac799.md) | merge | P1 | Intuitive update rule explanation. |
| [Long EMA Overfitting Analysis](../artifacts/chatgpt/6842af6f-3198-8009-ae3c-1d48793e028e.md) | merge | P1 | Overfit risk from slow memory. |
| [Non-TD Branch - RTRL-driven Regressor Design](../artifacts/chatgpt/69ad830b-2734-83a0-ace6-1cf85c61fead.md) | dual-link | P1 | Alternative RTRL interpretation. |
| [Orthogonal Matrix EMA Simplification](../artifacts/chatgpt/6878a1fb-a638-8009-8535-4c1a8c1e2bc5.md) | merge | P1 | Structured filter simplification. |
| [Orthogonalizing EMA Features](../artifacts/chatgpt/6810fc5e-f9e8-8009-a69f-a57b3d8d56a1.md) | merge | P1 | Reducing collinearity between EMA bases. |
| [RTRL-driven Regressor Design](../artifacts/chatgpt/69a93d32-da28-839c-85b2-b1d0e285ad05.md) | dual-link | P1 | Adaptive update mechanics. |

### Temporal Evidence And Covariance

Primary destination:
[temporal evidence](../../wiki/topics/quant/temporal-evidence.md).

Secondary destination:
[regression stability and validation](../../wiki/topics/quant/regression-stability-and-validation.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [ACF FFT Periodogram Relationship](../artifacts/chatgpt/69e20396-a318-839a-b481-08b08af67331.md) | merge | P1 | Autocorrelation and spectral evidence. |
| [Autocorrelation and Feature Selection](../artifacts/chatgpt/68542eff-a634-8009-86fd-ce165272e33f.md) | merge | P1 | Feature selection from temporal dependence. |
| [Forecast Horizon Generalization](../artifacts/chatgpt/69dce9bb-bd10-8399-987b-c262e6f85e63.md) | dual-link | P1 | Horizon-specific evidence and generalization. |
| [Temporal Cross-Validation Unification](../artifacts/chatgpt/69ec7a41-1fb0-839b-ad3c-7c0a3c6800c0.md) | merge | P1 | Time-series split taxonomy. |
| [Weighted Sample Covariance](../artifacts/chatgpt/69d680de-e1f8-8399-bb11-84e2daaa63ec.md) | merge | P1 | Weighted covariance as evidence primitive. |
| [covariance estimation](../artifacts/obsidian/covariance-estimation.md) | merge | P1 | Obsidian note for covariance background. |
| [temporal relationship of response](../artifacts/obsidian/generalization.md) | merge | P1 | Existing Obsidian framing of temporal response. |

### Structured Returns And P12n Signal Study

Primary destinations:
[P12n temporal returns experiments](../../wiki/projects/p12n/temporal-returns-experiments.md)
and [structured return models](../../wiki/topics/quant/structured-return-models.md).

Use `dual-link` when a source has both active p12n relevance and reusable
method content.

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Autocorrelation Based Regression](../artifacts/chatgpt/69dc435b-3bd8-839b-9ae5-06021df8d193.md) | merge | P1 | Regression model over temporal dependence. |
| [Bilinear Autoregressive LSQ](../artifacts/chatgpt/6a200ef7-f71c-83ec-8c98-cceb472c5baa.md) | merge | P1 | Structured autoregressive fitting. |
| [Branch - Lagged Returns Prediction](../artifacts/chatgpt/69e73c9f-6c8c-839e-bcc2-5e6695180ba8.md) | dual-link | P1 | Live signal study plus reusable lag structure. |
| [Comparing Financial Return Models](../artifacts/chatgpt/67d307e8-d668-8009-8008-4a8eb7d5ba55.md) | merge | P1 | Return model taxonomy. |
| [Hierarchical AR Models](../artifacts/chatgpt/69dc4552-db34-839e-8d02-50ff207486f8.md) | merge | P1 | Hierarchical autoregressive structure. |
| [Impulse Forecasting Explanation](../artifacts/chatgpt/69cccd65-5520-839f-aecd-e5420a505bc7.md) | dual-link | P1 | Impulse filter for return forecasting. |
| [Lagged Returns Prediction](../artifacts/chatgpt/69e23cd4-d9bc-839c-b2e9-63e62b275d18.md) | dual-link | P1 | Core p12n lag evidence source. |
| [Low-Rank Tensor Regression](../artifacts/chatgpt/68639f33-2858-8009-8a85-351d48135a5a.md) | merge | P1 | Low-rank structured regression. |
| [Market Making PnL Estimate](../artifacts/chatgpt/686d210c-45d8-8009-b076-ed3216006e96.md) | dual-link | P1 | Forecast-to-PnL bridge. |
| [Pooling Branch - Impulse Forecasting Explanation](../artifacts/chatgpt/69cfd775-8a8c-839d-8746-8e40e2b149a3.md) | dual-link | P1 | Pooling variant of impulse forecasting. |
| [Predicting Asset Returns](../artifacts/chatgpt/69983c39-aac0-839a-a0a9-c23e8d7d6aab.md) | dual-link | P1 | Direct return prediction framing. |
| [Predicting Returns and Fills](../artifacts/chatgpt/6710eaf9-ec70-8009-b573-28274dc3d163.md) | dual-link | P1 | Route fills to P12n execution policy. |
| [Returns Forecasting with Regression](../artifacts/chatgpt/69983e0f-e664-839b-88fb-408fd5249246.md) | dual-link | P1 | Forecasting with regression formulation. |
| [overview](../artifacts/obsidian/hyperliquid.md) | defer | P2 | Exchange context; likely P12n execution if needed. |

### Regression, Stability, And Regularization

Primary destinations:
[regression stability and validation](../../wiki/topics/quant/regression-stability-and-validation.md)
and [generalization and regularization](../../wiki/topics/quant/generalization-and-regularization.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Branch - Proxy-target training in regression](../artifacts/chatgpt/69d5ed83-dbb4-83a1-b4fd-1f878f014cf9.md) | merge | P1 | Target construction and validation risk. |
| [Flat vs Sharp Minima in Linear Regression](../artifacts/chatgpt/67b3134f-cf50-8009-9265-a47222f57525.md) | merge | P1 | Geometry and stability. |
| [Gradient Similarity and Generalization](../artifacts/chatgpt/67691f82-f864-8009-b4b0-7991c0068fa1.md) | merge | P1 | Generalization diagnostic. |
| [Least Angle Regression Explained](../artifacts/chatgpt/674c0a48-e938-8009-94fa-c205a686cd89.md) | merge | P1 | Sparse regression path method. |
| [LOOCV Error Efficient Computation](../artifacts/chatgpt/6811ed55-0e14-8009-9c2a-f4b586b27278.md) | merge | P1 | Efficient LOO identity. |
| [Mahalanobis vs Linear Regression](../artifacts/chatgpt/68480c76-7cbc-8009-aca1-4934960c1980.md) | merge | P1 | Geometry of regression and distance. |
| [Optimal Ridge Penalty Computation](../artifacts/chatgpt/6876f4ab-b368-8009-9320-b72c69c8ce00.md) | merge | P1 | Ridge penalty selection. |
| [Ridge CV vs OOF Scaling](../artifacts/chatgpt/6763f3ae-17ec-8009-8723-49f1fcb2e6c1.md) | merge | P1 | Out-of-fold scaling and leakage control. |
| [Ridge Penalty Optimization](../artifacts/chatgpt/6876f4ac-77cc-8009-8b48-a1327e12c379.md) | merge | P1 | Regularization objective. |
| [Robust Regression Research Directions](../artifacts/chatgpt/67191c44-b954-8009-8e92-c5799747b9bb.md) | merge | P1 | Robustness and research map. |
| [Sparse Features in Ridge](../artifacts/chatgpt/69cff0f3-96b8-839e-8380-caf5d0b911b6.md) | merge | P1 | Sparse feature shrinkage. |
| [ideas](../artifacts/obsidian/regression.md) | merge | P1 | Obsidian regression note. |

### Optimization And Computation

Primary destination:
[optimization and computation](../../wiki/topics/quant/optimization-and-computation.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [ADMM Variable Splitting Tutorial](../artifacts/chatgpt/69a1cc34-679c-8398-a265-a5cb0821fb1e.md) | merge | P1 | Variable splitting pattern. |
| [Analytical Neural Network Training](../artifacts/chatgpt/672ba4a5-0098-8009-bf41-8abd9ed48760.md) | dual-link | P2 | Quant optimization plus Genesis AI research if useful. |
| [Autoregressive Model Optimization](../artifacts/chatgpt/69ef1db7-01f8-839e-a148-7f69cd23ab49.md) | merge | P1 | Solver view of AR models. |
| [Bi-level Linear Regression](../artifacts/chatgpt/69cfcf41-b4b0-839d-bd3b-1a3c20a6e4d5.md) | merge | P1 | Nested objective for linear regression. |
| [Block Orthogonal LS Solvers](../artifacts/chatgpt/68366f18-3ba4-8009-b87c-de2db683bc74.md) | merge | P1 | Structured least-squares solver. |
| [Branch - Meta-Optimization for Data Weighting](../artifacts/chatgpt/69cab2fa-d744-839a-877e-4de1169a753a.md) | merge | P1 | Data-weight objective. |
| [Branch - MSE Computation for Trailing Window](../artifacts/chatgpt/69e1d90a-cb1c-839d-8acb-dbf91b58ee07.md) | merge | P1 | Efficient trailing-window risk. |
| [Efficient Linear Regression Methods](../artifacts/chatgpt/68462ac7-0d9c-8009-82de-bd0feb0b02a5.md) | merge | P1 | Solver comparison. |
| [Exploring Parameter Space Solutions](../artifacts/chatgpt/672c38c2-8398-8009-8978-599861ac0f0c.md) | merge | P1 | Optimization geometry. |
| [Gauss-Newton for Nonlinear Layers](../artifacts/chatgpt/69e63991-5ef4-83a1-a9bb-cd1a23247290.md) | merge | P1 | Gauss-Newton for nonlinear heads. |
| [Gauss-Newton Optimization Insights](../artifacts/chatgpt/69ce12d1-750c-839e-9dbc-b85b63d0aa5b.md) | merge | P1 | Curvature approximation. |
| [Gradient computation for LSTQ](../artifacts/chatgpt/694233c9-c518-8322-98cc-9a709eabb499.md) | merge | P1 | Gradient computation detail. |
| [IRLS Initialization Tricks](../artifacts/chatgpt/6a09778e-befc-83ec-9902-b880f91fea81.md) | merge | P1 | Iteratively reweighted fitting. |
| [Least Squares for NN](../artifacts/chatgpt/68108d59-4888-8009-ba88-e1e9820a5728.md) | merge | P1 | Least-squares neural fitting. |
| [Least Squares Regression Estimation](../artifacts/chatgpt/6810edb2-1740-8009-a05e-5137df01c05e.md) | merge | P1 | Baseline estimation note. |
| [Linear Regression Hessian Approximation](../artifacts/chatgpt/69d09be4-a6e8-83a0-8ea9-6ef0cbf1c7f1.md) | merge | P1 | Hessian approximation. |
| [Meta-Optimization for Data Weighting](../artifacts/chatgpt/69ca7f5e-4848-839a-8937-dedf9e79b363.md) | merge | P1 | Main data-weighting source. |
| [MSE Computation for Trailing Window](../artifacts/chatgpt/69de5663-b9e0-83a1-aa8a-b0463403013b.md) | merge | P1 | Main trailing-window risk source. |
| [Speeding Up Linear Regression](../artifacts/chatgpt/674f4736-7960-8009-a075-e546853a02f9.md) | merge | P1 | Computational acceleration. |

### Tabular Nonlinearities And Feature Search

Primary destinations:
[tabular nonlinearities](../../wiki/topics/quant/tabular-nonlinearities.md)
and [P12n feature transforms and BST](../../wiki/projects/p12n/feature-transforms-and-bst.md).

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Base Learner Options TS](../artifacts/chatgpt/6830a950-368c-8009-ab4b-c7baf293dd2e.md) | merge | P1 | Base learner menu for time-series tabular models. |
| [Continuous Histogram Smoothing](../artifacts/chatgpt/6a2221ce-33d8-83ec-978d-7626e8ff3c3f.md) | merge | P1 | Smooth binning primitive. |
| [Discretization in Deep Learning](../artifacts/chatgpt/67b71b0c-5d0c-8009-8093-27d79fdb7289.md) | dual-link | P2 | Quant feature transforms plus AI research context. |
| [Faster histogram alternatives](../artifacts/chatgpt/68501c0c-6f4c-8009-b40a-1f39f1799091.md) | merge | P1 | Faster substitutes for histogram features. |
| [Feature Hashing Alternatives](../artifacts/chatgpt/68382bfb-6f44-8009-a58e-7a6a8bf15ad8.md) | merge | P1 | Hashing and sparse feature compression. |
| [Fitting Functional ANOVA Models](../artifacts/chatgpt/678f78e8-7f04-8009-8be1-1e12a5dee954.md) | merge | P1 | Interaction decomposition. |
| [Histogram smoother to B-spline](../artifacts/chatgpt/697db20f-cd94-839d-a687-af61e186b9c9.md) | merge | P1 | Spline generalization of bins. |
| [Iterative Greedy Feature Selection](../artifacts/chatgpt/69eb6c3d-c5d8-839e-97e0-8caedc8c6584.md) | dual-link | P1 | Feature search with computation concerns. |
| [Linear Model with Nonlinearity](../artifacts/chatgpt/d55275c4-b7fe-4cd7-bcce-d66d0c3f1c68.md) | merge | P1 | Linear shell with nonlinear basis. |
| [Linear Regression with Modulation](../artifacts/chatgpt/6834364d-3f9c-8009-b633-c4fc44a8399d.md) | merge | P1 | Gating or modulation on linear model. |
| [ML Regression with Product Bins](../artifacts/chatgpt/6871e0bb-14a8-8009-a8c9-fbf8690c0430.md) | merge | P1 | Product-bin modeling source. |
| [Non-linear Feature Transformations](../artifacts/chatgpt/674b3994-918c-8009-9724-e8dd5d984766.md) | merge | P1 | Transform menu. |
| [Streaming k-means extension](../artifacts/chatgpt/69b65ceb-6620-8398-8796-e663ba3066cf.md) | merge | P1 | Streaming clustering as feature primitive. |
| [Tabular ML for Time Series](../artifacts/chatgpt/67dc2d07-fa44-8009-b9fa-0ac6fc749115.md) | merge | P1 | Time-series tabular modeling overview. |

### Defer Or Human Review

These are not necessarily bad sources. They are just not clear enough to route
without reading the artifact body, or they are broad notes better saved for a
later targeted page.

| Artifact | Action | Priority | Note |
| --- | --- | --- | --- |
| [Gated Layers and Approximations](../artifacts/chatgpt/6728c741-b2f8-8009-b3e5-c1fabd74ad94.md) | defer | P2 | Likely sequence-model analogy, but route after reading. |
| [Machine Learning Algorithms for Finance](../artifacts/chatgpt/686fde92-6040-8009-bad0-f98d2ea123d5.md) | defer | P2 | Broad survey source. |
| [Model fitting ideas](../artifacts/chatgpt/6909bf03-39e4-8323-8729-b0fe673a7db8.md) | defer | P2 | Broad note; mine only if a page needs filler detail. |
| [pc setup](../artifacts/obsidian/pc-setup.md) | defer | P3 | Infrastructure context, not a quant method source. |
| [zzz's framework](../artifacts/obsidian/zzz-s-framework.md) | defer | P2 | Broad framework note; route after body review. |

## Next Pass

Next, run a page-deepening pass for the regression, stability, and
regularization queue:
[regression stability and validation](../../wiki/topics/quant/regression-stability-and-validation.md)
and [generalization and regularization](../../wiki/topics/quant/generalization-and-regularization.md).

This pass should keep validation protocol, target construction, and regularizer
selection explicit, because those concerns cut across several p12n model pages.
