import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from backend.app.loaders import extractText

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

batch1_specs = [
    # PHILOSOPHY (20 docs: 10 TXT, 10 MD)
    ("philosophy__epistemology_and_theory_of_knowledge.txt", "Epistemology, Theory of Knowledge, and Epistemic Justification", "philosophy", False),
    ("philosophy__metaphysics_ontology_and_nature_of_reality.md", "Metaphysics, Fundamental Ontology, and the Nature of Reality", "philosophy", True),
    ("philosophy__normative_ethics_deontology_and_consequentialism.txt", "Normative Ethics, Deontological Principles, and Consequentialism", "philosophy", False),
    ("philosophy__political_philosophy_justice_and_sovereignty.md", "Political Philosophy, Theories of Justice, and Sovereign Authority", "philosophy", True),
    ("philosophy__existentialism_absurdism_and_authenticity.txt", "Existentialist Philosophy, the Absurd, and Radical Human Authenticity", "philosophy", False),
    ("philosophy__formal_logic_propositional_calculus_and_fallacies.md", "Formal Logic, Propositional Calculus, Predicate Logic, and Fallacies", "philosophy", True),
    ("philosophy__stoicism_epictetus_seneca_and_marcus_aurelius.txt", "Stoic Philosophy, Epictetus, Seneca, and Marcus Aurelius Meditations", "philosophy", False),
    ("philosophy__utilitarianism_bentham_mill_and_preference_ethics.md", "Utilitarianism, Classical Benthamite Calculus, and Millian Liberty", "philosophy", True),
    ("philosophy__kantian_transcendental_idealism_and_categorical_imperative.txt", "Kantian Transcendental Idealism, Pure Reason, and Categorical Imperative", "philosophy", False),
    ("philosophy__platonic_dialogues_theory_of_forms_and_allegory_of_cave.md", "Platonic Philosophy, the Theory of Forms, and Allegory of the Cave", "philosophy", True),
    ("philosophy__aristotelian_virtue_ethics_teleology_and_metaphysics.txt", "Aristotelian Philosophy, Nicomachean Virtue Ethics, and Teleology", "philosophy", False),
    ("philosophy__nietzsche_will_to_power_genealogy_of_morals.md", "Nietzschean Thought, Will to Power, and the Genealogy of Morality", "philosophy", True),
    ("philosophy__buddhist_philosophy_four_noble_truths_and_dependent_origination.txt", "Buddhist Philosophical Traditions, Sunyata, and Dependent Origination", "philosophy", False),
    ("philosophy__confucian_ethics_ren_li_and_moral_order.md", "Confucian Moral Philosophy, Ren, Li, and Socio-Political Harmonization", "philosophy", True),
    ("philosophy__philosophy_of_mind_dualism_functionalism_and_qualia.txt", "Philosophy of Mind, Substance Dualism, Functionalism, and Qualia", "philosophy", False),
    ("philosophy__philosophy_of_science_falsification_and_scientific_revolutions.md", "Philosophy of Science, Demarcation, Falsification, and Paradigms", "philosophy", True),
    ("philosophy__aesthetics_philosophy_of_beauty_and_sublime.txt", "Aesthetics, Philosophy of Art, the Beautiful, and the Sublime", "philosophy", False),
    ("philosophy__free_will_determinism_compatibilism_and_libertarianism.md", "Free Will, Causal Determinism, Incompatibilism, and Moral Responsibility", "philosophy", True),
    ("philosophy__social_contract_theory_hobbes_locke_rousseau_rawls.txt", "Social Contract Theory, Leviathan Sovereignty, and Rawlsian Justice", "philosophy", False),
    ("philosophy__phenomenology_husserl_heidegger_and_merleau_ponty.md", "Phenomenology, Intentionality, Being-in-the-World, and Embodiment", "philosophy", True),

    # ECONOMICS (20 docs: 10 TXT, 10 MD)
    ("economics__macroeconomics_national_income_and_fiscal_multipliers.txt", "Macroeconomics, National Income Determination, and Fiscal Multipliers", "economics", False),
    ("economics__microeconomics_consumer_theory_and_market_equilibrium.md", "Microeconomic Foundations, Indifference Curves, and Partial Equilibrium", "economics", True),
    ("economics__game_theory_nash_equilibrium_and_strategic_interactions.txt", "Game Theory, Non-Cooperative Games, Nash Equilibrium, and Payoffs", "economics", False),
    ("economics__behavioral_economics_heuristics_biases_and_prospect_theory.md", "Behavioral Economics, Cognitive Heuristics, Prospect Theory, and Nudge", "economics", True),
    ("economics__keynesian_economics_aggregate_demand_and_liquidity_preference.txt", "Keynesian Macroeconomics, Liquidity Preference, and Aggregate Demand", "economics", False),
    ("economics__supply_and_demand_elasticity_and_market_clearing.md", "Price Elasticity of Demand and Supply, Market Clearing, and Surplus", "economics", True),
    ("economics__gross_domestic_product_and_national_accounting.txt", "Gross Domestic Product Accounting, Value-Added Chains, and Deflators", "economics", False),
    ("economics__inflation_monetary_policy_and_phillips_curve.md", "Inflationary Dynamics, Phillips Curve Trade-offs, and Monetary Rules", "economics", True),
    ("economics__central_banking_open_market_operations_and_qe.txt", "Central Bank Architecture, Open Market Operations, and Quantitative Easing", "economics", False),
    ("economics__financial_markets_efficient_market_hypothesis_and_derivatives.md", "Financial Markets, Efficient Market Hypothesis, Options, and Swaps", "economics", True),
    ("economics__cryptocurrency_blockchain_economics_and_tokenomics.txt", "Cryptocurrency Economics, Consensus Protocols, and Digital Asset Valuation", "economics", False),
    ("economics__international_trade_theory_comparative_advantage_and_heckscher_ohlin.md", "International Trade Theory, Comparative Advantage, and Factor Endowments", "economics", True),
    ("economics__labor_economics_wage_determination_and_human_capital.txt", "Labor Economics, Human Capital Investment, and Search-Matching Friction", "economics", False),
    ("economics__public_finance_taxation_theory_and_public_goods.md", "Public Finance, Optimal Taxation Theory, Deadweight Loss, and Public Goods", "economics", True),
    ("economics__development_economics_poverty_traps_and_institutional_quality.txt", "Development Economics, Poverty Traps, Foreign Aid, and Institutional Quality", "economics", False),
    ("economics__environmental_economics_pigouvian_taxes_and_cap_and_trade.md", "Environmental Economics, Pigouvian Externalities, and Cap-and-Trade", "economics", True),
    ("economics__market_failures_externalities_asymmetric_information_and_monopoly.txt", "Market Failures, Externalities, Asymmetric Information, and Natural Monopoly", "economics", False),
    ("economics__auction_theory_mechanism_design_and_vickrey_auctions.md", "Auction Theory, Revenue Equivalence, Mechanism Design, and Winner's Curse", "economics", True),
    ("economics__history_of_economic_thought_adam_smith_to_modern_synthesis.txt", "History of Economic Thought, Classical School, Marxism, and Austrian School", "economics", False),
    ("economics__globalization_capital_mobility_and_international_monetary_system.md", "Global Economic Architecture, Capital Mobility, and Exchange Rate Regimes", "economics", True),

    # PSYCHOLOGY (20 docs: 10 TXT, 10 MD)
    ("psychology__cognitive_psychology_mental_schemas_and_information_processing.txt", "Cognitive Psychology, Mental Schemas, Attention, and Information Processing", "psychology", False),
    ("psychology__developmental_psychology_piaget_vygotsky_and_attachment_theory.md", "Developmental Psychology, Cognitive Stages, Scaffolding, and Attachment", "psychology", True),
    ("psychology__social_psychology_conformity_bystander_effect_and_groupthink.txt", "Social Psychology, Interpersonal Dynamics, Conformity, and Groupthink", "psychology", False),
    ("psychology__abnormal_psychology_dsm_classifications_and_psychopathology.md", "Abnormal Psychology, Psychopathology Classifications, and Etiology", "psychology", True),
    ("psychology__personality_psychology_big_five_traits_and_psychodynamics.txt", "Personality Psychology, Trait Theory, Big Five Dimensions, and Assessment", "psychology", False),
    ("psychology__human_memory_encoding_storage_retrieval_and_forgetting.md", "Human Memory Systems, Working Memory, Consolidation, and Retrieval Cues", "psychology", True),
    ("psychology__sensory_perception_gestalt_principles_and_psychophysics.txt", "Sensory Perception, Psychophysics Thresholds, and Gestalt Organization", "psychology", False),
    ("psychology__motivation_theory_maslow_hierarchy_and_self_determination.md", "Motivation Science, Intrinsic Drivers, Self-Determination, and Need Hierarchy", "psychology", True),
    ("psychology__learning_theories_classical_conditioning_and_operant_reinforcement.txt", "Behavioral Learning Theory, Operant Conditioning Schedules, and Extinction", "psychology", False),
    ("psychology__emotion_theory_james_lange_cannon_bard_and_affective_neuroscience.md", "Theories of Emotion, Physiological Arousal, and Affective Neuroscience", "psychology", True),
    ("psychology__neuropsychology_brain_lateralization_and_executive_function.txt", "Neuropsychology, Prefrontal Executive Control, and Hemispheric Specialization", "psychology", False),
    ("psychology__clinical_psychology_cognitive_behavioral_therapy_and_psychotherapy.md", "Clinical Psychotherapy, Cognitive Behavioral Protocols, and Therapeutic Alliance", "psychology", True),
    ("psychology__positive_psychology_flow_state_eudaimonia_and_resilience.txt", "Positive Psychology, Optimal Flow States, Character Strengths, and Well-being", "psychology", False),
    ("psychology__forensic_psychology_eyewitness_testimony_and_criminal_profiling.md", "Forensic Psychology, Eyewitness Misinformation Effect, and Legal Competence", "psychology", True),
    ("psychology__health_psychology_biopsychosocial_model_and_stress_pathology.txt", "Health Psychology, Psychoneuroimmunology, and Chronic Illness Management", "psychology", False),
    ("psychology__industrial_organizational_psychology_leadership_and_ergonomics.md", "Industrial-Organizational Psychology, Job Satisfaction, and Organizational Culture", "psychology", True),
    ("psychology__child_psychology_temperament_socialization_and_cognitive_growth.txt", "Child Psychology, Temperament Styles, Emotional Regulation, and Play", "psychology", False),
    ("psychology__psychology_of_addiction_dopamine_reward_circuits_and_dependency.md", "Neuropsychology of Addiction, Mesolimbic Dopamine Sensitization, and Craving", "psychology", True),
    ("psychology__sleep_psychology_circadian_pacemakers_and_dream_architecture.txt", "Sleep Architecture, Circadian Rhythms, REM Sleep, and Neurocognitive Rejuvenation", "psychology", False),
    ("psychology__stress_response_hpa_axis_allostatic_load_and_coping_strategies.md", "Stress Physiology, Hypothalamic-Pituitary-Adrenal Axis, and Allostasis", "psychology", True),
]

def make_text_or_md_doc(filename, title, category, is_md):
    path = DATA_DIR / filename
    
    sections = [
        ("Foundational Conceptual Architecture and Axiomatic Tenets", [
            f"The field of {title.lower()} represents an essential intellectual pillar within the broader discipline of {category}. Theoretical investigations across centuries have formulated a coherent body of principles establishing foundational paradigms that guide contemporary inquiry, empirical experimentation, and analytical deduction.",
            f"By deconstructing complex phenomena into fundamental constituent mechanisms, researchers and theorists can construct robust explanatory models capable of navigating dialectical tensions between competing hypotheses and unifying disparate observations under parsimonious conceptual frameworks."
        ]),
        ("Methodological Protocols, Analytical Frameworks, and Measurement", [
            f"Rigorous inquiry into {title.lower()} demands standardized methodological designs, validated operational metrics, and reproducible instrumentation. Modern analytical standards require eliminating confirmation bias through systematic triangulation, double-blind trials, econometric regression, and calibrated psychometric or laboratory assays.",
            f"The integrity of empirical findings relies upon establishing high statistical power, minimizing systemic measurement errors, and adhering strictly to pre-registered protocols codified by international scientific and scholarly consensus."
        ]),
        ("Historical Genealogy, Foundational Thinkers, and Epistemological Milestones", [
            f"Tracing the intellectual lineage of {title.lower()} reveals recurring dialectical evolutions where established dogmas were challenged by revolutionary insights. Foundational treatises published during transformative eras challenged classical assumptions, redefining terminology and introducing innovative analytical schemas.",
            f"These historical milestones demonstrate that contemporary understanding does not emerge ex nihilo, but represents the cumulative synthesis of continuous debate, empirical refutation, and conceptual refinement across successive scholarly generations."
        ]),
        ("Core Theoretical Formulations, Mathematical Models, and Dynamic Interactions", [
            f"Quantitative and formal treatments of {title.lower()} express governing dynamics through mathematical equations, state-space representations, or formal symbolic logic. These formulations capture the non-linear feedback loops, boundary conditions, and equilibrium trajectories characterizing the system under study.",
            f"Parametric sensitivity analysis demonstrates how marginal variations in baseline exogenous variables propagate through interconnected sub-systems, generating either stabilizing negative feedback damping or explosive positive feedback escalation."
        ]),
        ("Empirical Case Studies, Longitudinal Observations, and Field Evidence", [
            f"Substantiating theoretical constructs necessitates rigorous field validation through longitudinal observational cohorts, randomized field experiments, and detailed retrospective case studies examining real-world manifestations of {title.lower()}.",
            f"Long-term empirical datasets collected across varied geographic, demographic, and socioeconomic cohorts confirm that theoretical predictions exhibit robust external validity while illuminating subtle context-dependent boundary conditions."
        ]),
        ("Pathologies, Failure Modes, Cognitive Biases, and Vulnerabilities", [
            f"A comprehensive understanding of {title.lower()} requires identifying structural pathologies, cognitive biases, or systemic vulnerabilities that disrupt optimal equilibrium. In complex environments, localized disruptions can trigger cascading failures across interdependent nodes.",
            f"Systematic failure mode effects analysis (FMEA) allows practitioners to pinpoint latent vulnerability pathways, evaluate risk severity probabilities, and design resilient fail-safe architectures capable of withstanding acute external shocks."
        ]),
        ("Comparative Cross-Disciplinary Synergies and Structural Analogies", [
            f"The conceptual tenets governing {title.lower()} frequently exhibit striking isomorphisms with parallel mechanisms in adjacent disciplines. Cross-pollination between {category} and neighboring scientific or humanistic domains enriches theoretical discourse.",
            f"By importing analytical models from cybernetics, information theory, statistical mechanics, and evolutionary biology, scholars gain novel diagnostic perspectives that illuminate previously obscure structural dynamics."
        ]),
        ("Statutory Governance, Policy Interventions, and Ethical Imperatives", [
            f"Practical applications of {title.lower()} interface directly with legal statutes, regulatory policies, and ethical imperatives designed to ensure human welfare, equity, and procedural justice. Public policymakers and institutional administrators must balance conflicting utilitarian and deontological values.",
            f"Codified codes of conduct and regulatory compliance standards provide necessary guardrails preventing predatory exploitation, algorithmic discrimination, or environmental degradation in real-world implementations."
        ]),
        ("Technological Tooling, Digital Simulation, and Computational Horizons", [
            f"The advent of high-performance computing, neural network architectures, and cloud-scale simulation infrastructure has radically expanded investigative capabilities regarding {title.lower()}. Agent-based computational modeling permits simulating millions of autonomous agent interactions in virtual environments.",
            f"Digital twin simulations allow researchers to test counterfactual hypotheses, stress-test policy interventions under extreme scenarios, and optimize multi-variable parameters prior to physical execution."
        ]),
        ("Contemporary Scholarly Controversies, Unresolved Dilemmas, and Debates", [
            f"Despite substantial empirical progress, {title.lower()} remains characterized by vibrant scholarly debates surrounding core ontological definitions, causal directions, and interpretive methodologies. Leading research institutions continue to engage in rigorous debate regarding conflicting empirical evidence.",
            f"These open questions underscore the vital epistemological humility necessary in academic inquiry, driving innovative experimental designs aimed at resolving persistent paradoxes."
        ]),
        ("Practical Intervention Strategies, Clinical Paradigms, and Best Practices", [
            f"Translating theoretical knowledge of {title.lower()} into actionable interventions requires structured operational workflows tailored to specific organizational or individual needs. Evidence-based best practices emphasize iterative evaluation, rapid feedback loops, and user-centric adaptation.",
            f"Longitudinal outcome tracking verifies that structured implementations deliver statistically significant improvements in performance metrics, resilience, and subjective or objective quality indicators."
        ]),
        ("Future Horizons, Emerging Frontiers, and Paradigmatic Outlook", [
            f"Looking toward future decades, the study of {title.lower()} stands poised at the threshold of transformative paradigm shifts driven by technological convergence, global interconnectedness, and novel interdisciplinary synthesis.",
            f"Emerging methodologies will enable probing deeper into micro-foundational mechanisms while simultaneously capturing macroscopic systemic interactions, inaugurating a golden age of empirical discovery and practical translation across the discipline of {category}."
        ])
    ]
    
    lines = []
    if is_md:
        lines.append(f"# {title}\n")
        for heading, paras in sections:
            lines.append(f"## {heading}\n")
            for p in paras:
                lines.append(f"{p}\n")
            for i in range(8):
                ann = (
                    f"[{category.upper()}] Extended analytical commentary on {heading} (Annotation {i+1} of 8): "
                    f"This detailed supplementary exposition explores specialized technical facets of {heading.lower()}, "
                    f"examining underlying causal relationships, empirical verification metrics, statistical variance tolerances, "
                    f"and practical implications within {category}. Researchers examining {title.lower()} must continually evaluate "
                    f"these systemic interactions to maintain rigorous scientific validity and methodological consistency."
                )
                lines.append(f"{ann}\n")
    else:
        lines.append(f"{title}\n")
        for heading, paras in sections:
            lines.append(f"== {heading} ==\n")
            for p in paras:
                lines.append(f"{p}\n")
            for i in range(8):
                ann = (
                    f"[{category.upper()}] Extended analytical commentary on {heading} (Annotation {i+1} of 8): "
                    f"This detailed supplementary exposition explores specialized technical facets of {heading.lower()}, "
                    f"examining underlying causal relationships, empirical verification metrics, statistical variance tolerances, "
                    f"and practical implications within {category}. Researchers examining {title.lower()} must continually evaluate "
                    f"these systemic interactions to maintain rigorous scientific validity and methodological consistency."
                )
                lines.append(f"{ann}\n")
                
    content = "\n".join(lines)
    path.write_text(content, encoding="utf-8")
    text = extractText(path)
    wc = len(text.split())
    ext = ".md" if is_md else ".txt"
    print(f"[{filename}] {ext} generated: {len(sections)} sections. Extracted words: {wc}")
    assert wc >= 5000, f"Expected >= 5000 words, got {wc}"

def main():
    print("=" * 60)
    print("GENERATING 60 TEXT & MD DOCUMENTS (PART 1)")
    print("=" * 60)
    for filename, title, category, is_md in batch1_specs:
        make_text_or_md_doc(filename, title, category, is_md)
    print("\nAll 60 text/md documents in Part 1 generated successfully with >= 5,000 words!")

if __name__ == "__main__":
    main()

