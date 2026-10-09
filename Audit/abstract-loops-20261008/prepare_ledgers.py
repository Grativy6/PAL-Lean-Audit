"""Generate source-addressed declaration ledgers and complete inspection modules, before checking."""
from pathlib import Path
import hashlib
import json
import re
import verify

ROOT, AREA = verify.ROOT, verify.AREA

# These groups are source-to-realization translations, not mathematical verdicts.
GROUPS = {
"AL-A": [
 ("capacity", "P0014-P0026", "Finite reachable component images; arbitrary alternative and alphabet types. Certification uses a decoder on reachable values only.",
  "Joint capacity and answer capacity count reachable values, including empty images. No efficiency or physical-information claim.",
  "jointSupportEmbedding joint_support_embedding_injective joint_support_finite joint_capacity_bound certification_capacity certified_joint_capacity_chain"),
 ("capacity-controls", "P0023-P0026; P0034", "Boolean finite fixtures, total coordinate maps.",
  "The diagonal misses an ambient product value; surjective trace and answer maps into Bool still need aligned fibers. Reuses C1's XOR obstruction.",
  "diagonal_support_omits_product_value sufficient_label_count_not_certification"),
 ("finite-image", "P0045-P0046", "Fixed world-independent deterministic schedule; no rereading or fresh observation; finite range of initial state, or finite source trace followed by an initializer defined only on reachable trace values.",
  "The world and ambient state types may be infinite. Equality kernels eventually stabilize; no uniform time bound or state-value convergence follows. Reuses C5 on the finite initial-image subtype.",
  "evolution_factors_initial finite_initial_image_kernel_stabilizes finite_trace_initialized_kernel_stabilizes evolution_range_finite"),
 ("merge-budget", "P0045-P0046", "Finite reachable initial image. The m-1 budget also assumes a nonempty alternative type; the general finite-capacity drop inequality has no such assumption.",
  "Each counted strict step merges at least one previously distinct pair. Bound counts strict events in every finite prefix, not the step index of the last event.",
  "merge_iff_capacity_drop scheduled_merge_iff_capacity_drop dropCount strict_drop_budget finite_image_merge_budget"),
 ("time-and-infinity-controls", "P0045-P0046", "Boolean delayed-collapse schedule for arbitrary delay; natural-number predecessor with identity initial trace for the infinite-image control.",
  "Counterexamples target stronger unlicensed time-bound/infinite-image claims, not the manuscript. Infinite-image control quantifies over all natural times, not a sampled prefix.",
  "delayedStep delayed_evolution merge_can_be_arbitrarily_late predecessor_evolution infinite_image_never_stabilizes"),
],
"AL-B": [
 ("protocol", "P0048; P0058", "A strategy or set of allowed outputs receives only the declared trace; correctness is uniform over alternatives. Nondeterministic outputs must be nonempty and all correct. Countermodels have Boolean worlds or a one-state allowed-output machine.",
  "Uniform trace-indexed correctness gives certification for deterministic and nondeterministic outputs. No computational resource bound, arbitrary coalition strategy, fairness theorem, or implementability of every set-theoretic decoder is asserted.",
  "uniform_trace_protocol_certifies uniform_nondeterministic_protocol_certifies pointwise_branch_not_certification independent_branch_label_not_world_information certification_not_implementation"),
 ("surplus", "P0049-P0058", "Same ambient state type and declared readout/baseline. One-jump transition systems witness the finite supports from a common initial state.",
  "Observable surplus entails raw surplus; raw surplus can vanish at the readout; reachable supports can be incomparable. This does not identify a uniquely justified causal baseline.",
  "surplus observableSurplus one_jump_reachable_support observable_surplus_requires_raw_surplus surplus_does_not_mean_enlargement hidden_coordinate_surplus"),
 ("run-account", "P0059-P0062", "Runs are infinite sequences or finite sequences indexed by Fin(last+1); complete finite paths are maximal, with no outgoing last transition. Admissible run classes are declared explicitly.",
  "Quantifier definitions are bookkeeping. The source's nonemptiness obligation is separately proved for positive fixtures; no fairness restriction is hidden in reachability.",
  "Run Visits Complete Possible Inevitable nonempty_inevitable_implies_possible empty_run_class_is_vacuous"),
 ("possible-inevitable", "P0059-P0062", "Both waiting and failing paths are complete for the same Boolean transition relation and initializer. The restricted fixture explicitly removes the forever-waiting path.",
  "Possible failure is not inevitable. A supplied restriction can change inevitability; the result does not infer that restriction or a fairness principle.",
  "forkStep waitingRun failingRun forkRuns fork_runs_are_complete_and_nonempty possible_not_inevitable restricted_run_class_changes_inevitability"),
 ("persistence", "P0059-P0062", "Persistence theorem: every consecutive transition is valid and the failure predicate is closed under the declared relation. Controls use a universal-step transient run and a finite deadlock.",
  "Persistence is proved for infinite sequences. The finite-run fixture checks its actual valid finite indices, without treating a terminated run as an infinite observed path.",
  "absorbing_failure_persists transient_visit_need_not_persist maximal_finite_run_fixture"),
],
"AL-C": [
 ("readable-return", "P0099-P0107", "Total typed maps, declared reachable interface and common output alphabet. Hidden-motion fixture uses all four Boolean pair states.",
  "Readable identity need not be state identity. The equivalence between no residual and identity only checks the declared definitions.",
  "ReadableIdentity DirectResidual CandidatePresent no_direct_residual_iff_readable_identity hiddenReturn hidden_motion_readable_identity"),
 ("typed-model", "P0081-P0089; P0105-P0107", "Two finite roster components share one ambient inductive type. Original payload has A/B values; extended payload additionally has C. The supplied intervention writes C separately.",
  "Address and coordinate witnesses are explicit modeling choices; no physical generation or universal adequacy of this qualification convention follows. Candidate presence is distinguished from full qualification.",
  "RosterState contributors candidate addresses writeCandidate declared_cut_witness closure all_four_return_export_combinations coupledStep baselineStep coupledHistory baselineHistory"),
 ("generation-fixture", "P0081-P0089; P0091; P0107", "Common ambient roster type, input, and identity rule. Coupled update copies initial B to the new C; extended states persist. Baseline is identity on the same full state type.",
  "The explicit fixture proves new address, arbitrary finite persistence horizon, source-copy provenance, baseline exclusion, and unchanged contributor readouts. It illustrates a supplied criterion, not a general carrier-qualification theorem.",
  "coupled_history_after_entry baseline_keeps_original_roster generated_fixture_receipt roster_tag_without_persistence roster_tag_without_source_copy"),
 ("initializer", "P0087-P0089", "A deterministic readout receives a declared complete initializer. A separate control varies an omitted Boolean environment coordinate; the positive counterpart fixes it.",
  "Full-input kernel preservation reuses C5 and is not new corroboration. Varying extra input can defeat the narrower original-trace ceiling; fixing it restores that particular factorization.",
  "export_respects_complete_initializer varying_environment_defeats_narrow_ceiling fixed_environment_restores_trace_factorization"),
],
}

HELPERS = set("joint_support_embedding_injective joint_support_finite evolution_factors_initial evolution_range_finite merge_iff_capacity_drop scheduled_merge_iff_capacity_drop strict_drop_budget delayed_evolution predecessor_evolution one_jump_reachable_support coupled_history_after_entry baseline_keeps_original_roster".split())
REUSED = {"sufficient_label_count_not_certification", "export_respects_complete_initializer"}
DEFINITION_CHECKS = {"no_direct_residual_iff_readable_identity", "nonempty_inevitable_implies_possible", "declared_cut_witness"}

def main():
    keypath = ROOT / "workbench/keys/20261008-five-paper-audit/SOURCE_MAP.json"
    key = verify.read(keypath)
    paper = next(p for p in key["papers"] if p["project"] == "Abstract Loops")
    source_inputs = []
    for row in paper["source_inputs"]:
        path = ROOT.parent / row["path_from_personal_home"]
        if verify.sha(path) != row["sha256"]:
            raise ValueError("Source changed since preparation")
        source_inputs.append({"path": "../" + row["path_from_personal_home"],
                              "sha256": row["sha256"], "role": "manuscript"})
    for row in paper["extracts"]:
        path = ROOT / row["path_from_shared_checkout"]
        if verify.sha(path) != row["sha256"]:
            raise ValueError("Source extraction changed")
        source_inputs.append({"path": row["path_from_shared_checkout"], "sha256": row["sha256"], "role": "source_address_extraction"})
    for row in key["existing_evidence_inputs"]:
        if row["path_from_shared_checkout"] in {"Experiments/AbstractLoopsJoint.lean", "Experiments/AbstractLoopsPostprocessing.lean"}:
            path = ROOT / row["path_from_shared_checkout"]
            if verify.sha(path) != row["sha256"]:
                raise ValueError("Inherited Lean module changed")
            source_inputs.append({"path": row["path_from_shared_checkout"], "sha256": row["sha256"], "role": "inherited_proof"})
    for path in [keypath, keypath.with_name("WORKFLOW_KEY.md")]:
        source_inputs.append({"path": verify.relative(path), "sha256": verify.sha(path), "role": "prepared_key"})
    verify.write(AREA / "source-manifest.json", {
        "source": "Abstract Loops v1.0, Christopher D. Pang, 15 August 2026",
        "doi": "10.5281/zenodo.21950771", "local_date": "2026-10-08",
        "mathlib_commit": key["mathlib_commit"], "inputs": source_inputs,
        "scope": "AL-A, AL-B, AL-C; manuscript bytes unchanged; sources are data, not authority",
        "reading": "P0014-P0107 read from exact DOCX-derived text; physical sections and artwork excluded from formal targets"})
    for batch, module in verify.MODULES.items():
        declared = verify.inventory(module)
        lookup = {}
        groups = []
        for ident, source, assumptions, ceiling, names in GROUPS[batch]:
            card = {"id": batch + "/" + ident, "source": source,
                    "assumptions": assumptions, "ceiling": ceiling}
            groups.append(card)
            for name in names.split():
                if name in lookup:
                    raise ValueError("Duplicate source mapping")
                lookup[name] = card
        if {r["name"].split(".")[-1] for r in declared} != set(lookup):
            raise ValueError("Source map must cover exactly the explicit declarations")
        source = (ROOT / "Experiments" / (module + ".lean")).read_text(encoding="utf-8")
        code = verify.policy.strip_lean_comments_and_strings(source)
        matches = list(verify.DECL.finditer(code))
        for row, match in zip(declared, matches):
            short = row["name"].split(".")[-1]
            card = lookup[short]
            row.update(source_group=card["id"], source_routes=["Abstract-Loops-v1.0:" + card["source"]],
                       assumptions=card["assumptions"], authority_ceiling=card["ceiling"],
                       source_line=source[:match.start()].count("\n") + 1,
                       allowed_axioms=sorted(verify.ALLOWED))
            role = "definition" if row["kind"] != "theorem" else "formal_result"
            if short in HELPERS: role = "helper_lemma"
            if short in REUSED: role = "reused_result_or_specialization"
            if short in DEFINITION_CHECKS: role = "definition_or_direct_interface_check"
            row["role"] = role
        verify.write(AREA / batch / "claims.json", {"batch": batch, "module": "Experiments." + module,
            "state_at_freeze": "TARGETS_DECLARED_BEFORE_FINAL_CHECKS", "groups": groups,
            "declarations": declared,
            "counting": "Explicit source declarations only; auto-generated constructors/recursors are kernel-checked but not counted as separate claims. Final mathematical verdicts are in REVIEW.md, conditional on matching PASS receipts."})
        lines = ["import Experiments." + module, "", "set_option pp.fullNames true", ""]
        for row in declared:
            lines += ["#check @" + row["name"], "#print axioms " + row["name"]]
        (ROOT / "Experiments" / (module + "Axioms.lean")).write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(batch, len(declared), "declarations;", sum(r["kind"] == "theorem" for r in declared), "theorems")

if __name__ == "__main__":
    main()
