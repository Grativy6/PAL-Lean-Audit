# GPPR transcendence dependency: external source check

Cached Ricci PDF SHA-256: `bc479d3d352aac29a5a83286a77171ef1364ac3858e840cf713557a734620a71`; pypdf extraction available. Cache record verified by the literature-cache helper; original copyright cover retained.

Checked 8 October 2026. Question: does the cited complex-power theorem apply to base -1 and exponent delta=3-sqrt(5), with log(-1)=i*pi? No novelty search is part of this check.

The prepared workspace had no literature cache hit for Schneider DOI 10.1515/crll.1935.172.65. Searches of the pinned Mathlib NumberTheory, Analysis and RingTheory source for Gelfond/Gel'fond/Schneider/Hilbert-seventh names found no relevant declaration. This is a bounded search, not a proof of absence of equivalent mathematics. The algebraic-tower and transcendence infrastructure is available.

The cited Gelfond 1934 paper's bibliographic record was found on MathNet (im4924), but the primary PDF and archive page repeatedly timed out, including one local network attempt. These failed acquisitions do not verify that paper's proof. Schneider's primary scan was not recovered.

An accessible primary research source is Giovanni Ricci, *Sul settimo problema di Hilbert*, Annali della Scuola Normale Superiore di Pisa, Classe di Scienze, series 2, volume 4 no.4 (1935), pp.341-372, Numdam identifier ASNSP_1935_2_4_4_341_0. Stable source: https://www.numdam.org/item/ASNSP_1935_2_4_4_341_0.pdf . The complete PDF is retained in the ignored project literature cache; its copyright cover is preserved. Only this extraction/application record is tracked.

Exact result: Theorem VI(1), p.348: for algebraic xi and algebraic irrational eta, with xi different from 0 and 1, xi^eta is transcendental. It is derived from the preceding results in this paper; it is not just a bibliographic citation. Footnote 5, p.343 explicitly defines the power as exp(eta log xi) for a fixed determination of the logarithm. Original printed pages 343 and 348 were visually inspected because OCR loses inequalities and Greek symbols. The entire long transcendence proof was not re-proved line by line in this audit; this is verification of a primary-source theorem and its application, not an independent proof of Gelfond-Schneider.

Dictionary: xi=-1 (algebraic, neither 0 nor 1), eta=delta=3-sqrt(5) (algebraic and irrational), logarithm value i*pi, so exp(eta log xi)=exp(2*pi*i*beta)=zeta, beta=(3-sqrt(5))/2. This implication is valid. GPPR's original OOXML was checked at P0046, P0053-P0054 and P0114-P0116: the square roots, algebraic-closure bar and logarithm choice are present; the flattened text omits some of them. Vogel's coefficient is sqrt(j), not j.

Literature classification: **known after translation of notation**; external theorem in the exact needed complex-branch form verified via Ricci's primary paper. This does not change the manuscript's original citations or establish novelty. Lean status remains separate: if the needed transcendence theorem cannot be supplied by a checked library declaration, the golden specialization must explicitly consume a named hypothesis. No new axiom is permitted.
