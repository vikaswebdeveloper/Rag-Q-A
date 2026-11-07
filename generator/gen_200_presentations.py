import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

import pptx
from backend.app.loaders import extractText

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

pptx_topics = [
    (
        "technology__artificial_intelligence_and_deep_learning.pptx",
        "Deep Learning Architecture, Foundation Models, and Machine Intelligence",
        [
            ("Foundations of Artificial Neural Networks", [
                "Perceptrons and Multilayer Architecture: Artificial neural networks model complex non-linear mathematical mappings using interconnected layers of simulated artificial neurons and learnable synaptic weights.",
                "Backpropagation and Gradient Descent: Synaptic weights update iteratively by propagating error loss gradients backward through computational graphs via chain rule differentiation calculus.",
                "Activation Functions Evolution: The historical progression from saturating sigmoids and tanh functions to Rectified Linear Units (ReLU), GeLU, and Swish mitigating vanishing gradient degradation.",
                "Universal Approximation Theorem: Multi-layer feedforward networks possess the mathematical capacity to approximate any continuous multidimensional Borel function given sufficient hidden neuron capacity."
            ]),
            ("Convolutional Neural Networks (CNNs) in Computer Vision", [
                "Spatial Inductive Biases: Convolutional kernel operators apply discrete 2D spatial filtering across input feature maps, enforcing translation invariance and parameter sharing efficiency.",
                "Historical Milestones: The evolutionary leap from Yann LeCun's LeNet-5 to AlexNet (2012), VGG-16, ResNet skip residual connections, and modern ConvNeXt vision architectures.",
                "Feature Extraction Hierarchies: Early receptive layers detect localized low-level edges and textures, whereas deeper layers synthesize high-level semantic object silhouettes and contextual geometry.",
                "Modern Visual Transformers: Vision Transformers (ViT) divide images into flattened linear patches, applying multi-head self-attention mechanisms that supersede traditional convolutional inductive biases."
            ]),
            ("Recurrent Architectures and Sequential Processing", [
                "Recurrent Hidden State Propagation: RNNs maintain internal memory vectors across sequential time steps, processing variable-length natural language and audio waveforms cyclically.",
                "Long Short-Term Memory (LSTM) Networks: Hochreiter and Schmidhuber's gated architecture utilizes input, forget, and output gates to retain error gradient flow across thousands of steps.",
                "Gated Recurrent Units (GRU): Cho et al. streamlined LSTM complexity by merging cell state and hidden state representations while coupling update and reset gating mechanisms.",
                "Sequential Bottlenecks: Inability to execute parallel time-step matrix computations on GPU accelerators motivated the architectural revolution toward non-recurrent attention models."
            ]),
            ("The Transformer Architecture and Self-Attention", [
                "Attention Is All You Need (2017): Vaswani et al. introduced the seminal self-attention paradigm, computing scaled dot-product attention across Query, Key, and Value vector matrices.",
                "Multi-Head Parallelism: Projecting representations into multiple orthogonal subspace projections enables neural networks to attend simultaneously to syntactic, semantic, and positional contexts.",
                "Positional Encodings: Sine-cosine absolute frequencies and Rotary Position Embeddings (RoPE) inject essential sequential positional awareness into permutation-invariant attention matrices.",
                "Computational Complexity Bounds: Quadratic O(N^2) memory and compute scaling relative to sequence length drove research into FlashAttention, linear attention, and sliding-window KV caches."
            ]),
            ("Large Language Model Pretraining and Scaling Laws", [
                "Self-Supervised Autoregressive Modeling: Training multi-billion parameter networks on vast trillion-token web corpora by maximizing next-token conditional probability prediction objectives.",
                "Kaplan and Chinchilla Scaling Laws: Empirical formulations determining optimal power-law allocation between model parameter capacity and training dataset token volume under compute constraints.",
                "Decoder-Only Dominance: The technological ascendancy of causal auto-regressive transformer decoders (GPT series, LLaMA, Mistral) over encoder-decoder architectures (T5, BART).",
                "Mixture-of-Experts (MoE) Architecture: Dynamically routing input tokens through sparse feedforward expert sub-networks, achieving trillion-parameter capacity with sub-hundred-billion active parameters."
            ]),
        ]
    ),
    (
        "space__interplanetary_propulsion_and_orbital_mechanics.pptx",
        "Orbital Mechanics, Interplanetary Trajectories, and Advanced Space Propulsion",
        [
            ("Keplerian Orbital Elements and Two-Body Dynamics", [
                "Six Fundamental Classical Elements: Semi-major axis, orbital eccentricity, inclination, longitude of ascending node, argument of periapsis, and true anomaly uniquely define trajectories.",
                "Vis-Viva Energy Equation: The fundamental relationship equating instantaneous orbital velocity to gravitational parameters and radial distance from the central gravitational barycenter.",
                "Conservation Laws in Orbital Dynamics: Conservation of orbital angular momentum dictates equal area sweeps per unit time, manifesting Kepler's second law of planetary motion.",
                "Perturbation Forces: Gravitational oblateness (J2 potential), atmospheric aerodynamic drag, solar radiation pressure, and third-body lunisolar gravitational perturbations induce nodal regression."
            ]),
            ("Chemical Rocket Propulsion and Thermochemistry", [
                "Tsiolkovsky Rocket Equation: The fundamental governing law establishing delta-v velocity increments as a logarithmic function of initial-to-final mass ratios and effective exhaust velocity.",
                "Specific Impulse (Isp) Benchmark: The definitive metric quantifying propellant mass efficiency, measuring thrust delivered per unit weight flow rate of propellant consumed per second.",
                "Combustion Chamber Thermodynamics: High-pressure chemical reactions converting liquid hydrogen/oxygen or liquid methane/oxygen into high-temperature supersonic gas expansions via de Laval nozzles.",
                "Staged Combustion Cycles: Full-flow staged combustion cycles (SpaceX Raptor) pump oxidizer and fuel through separate preburners, maximizing turbopump turbine efficiency and chamber pressures."
            ]),
            ("Interplanetary Transfer Orbits and Gravity Assists", [
                "Hohmann Transfer Ellipse: The energy-minimal two-impulse orbital maneuver transferring spacecraft between two coplanar circular orbits via an elliptical osculating path.",
                "Bi-Elliptic and Low-Energy Transfers: Utilizing intermediate high-apogee burns or weak stability boundary invariant manifolds (Lagrangian halo orbits) to conserve propellant mass.",
                "Gravitational Slingshot Maneuvers: Exchanging orbital angular momentum with orbiting planets during hyperbolic flybys, altering spacecraft heliocentric velocity vectors without propellant expenditure.",
                "Launch Windows and Planetary Synodic Periods: Interplanetary mission departures constrained to recurring geometric alignment intervals between Earth and target destination planets."
            ]),
            ("Electric and Ion Plasma Propulsion Systems", [
                "Electrostatic Gridded Ion Thrusters: Ionizing noble gases (xenon or krypton) via radiofrequency discharge and accelerating ions electrostatically across high-voltage grids (Isp > 3,000s).",
                "Hall-Effect Plasma Thrusters: Trapping electrons within radial magnetic fields to ionize propellant and accelerate ion plumes through axial electric potentials with high thrust efficiency.",
                "Power Constraints in Deep Space: Solar electric propulsion (SEP) encounters inverse-square solar flux attenuation beyond Mars, requiring spaceborne nuclear fission reactors (NEP).",
                "Continuous Low-Thrust Trajectory Optimization: Replacing impulsive delta-v velocity instantaneous burns with multi-month continuous low-thrust orbital spirals and spiral escapes."
            ]),
            ("Advanced Nuclear and Relativistic Propulsion Concepts", [
                "Nuclear Thermal Propulsion (NTP): Circulating cryogenic liquid hydrogen propellant through solid nuclear fission reactor cores, achieving twice the specific impulse of chemical rockets (Isp ~ 900s).",
                "Pulsed Nuclear Fusion Propulsion: Utilizing magnetic or inertial confinement fusion pellets detonated behind magnetic deflection nozzles to achieve relativistic interplanetary cruise velocities.",
                "Laser-Driven Photonic Sails: Propelling ultra-lightweight reflective gram-scale nanocrafts to 20% the speed of light using planetary phased-array 100-gigawatt laser optical beams.",
                "Alcubierre Spacetime Metric: Theoretical general relativistic solution proposing negative energy densities to contract spacetime in front of a spacecraft while expanding spacetime behind."
            ]),
        ]
    ),
    (
        "economics__modern_monetary_theory_and_fiscal_policy.pptx",
        "Modern Monetary Theory, Fiscal Policy Frameworks, and Sovereign Macroeconomics",
        [
            ("Foundational Tenets of Modern Monetary Theory (MMT)", [
                "Monetary Sovereignty Definition: A government that issues its own unpegged, floating fiat currency and borrows solely in that currency faces zero operational risk of involuntary insolvency.",
                "Taxes Drive Currency Demand: Coercive statutory legal tax obligations denominated in state currency establish foundational economic demand for the sovereign fiat currency token.",
                "The True Constraint is Real Resources: Financial budget deficits are bounded not by arbitrary nominal debt ceilings, but by available productive real resources, labor, and inflation.",
                "Endogenous Money Creation: Commercial banks create deposit money endogenously upon issuing loans, dispelling the traditional loanable funds and fractional reserve multiplier myths."
            ]),
            ("The Consolidated Government and Central Bank Balance Sheet", [
                "Treasury and Central Bank Coordination: Analyzing the fiscal authority and monetary authority as a single consolidated public sector entity transacting with the non-government sector.",
                "Government Spending Precedes Taxation: As the monopoly issuer of the currency, the sovereign government must logically spend or disburse currency into the economy before it can collect taxes.",
                "Bond Issuance as Interest Rate Maintenance: Sovereign treasury bond sales do not fund government expenditure, but serve as monetary draining operations targeting policy interest rates.",
                "Sectoral Balances Identity: Wynne Godley's macroeconomic accounting framework proving the domestic private balance, government fiscal balance, and external foreign balance sum to zero."
            ]),
            ("Inflation Dynamics and Fiscal Safeguards", [
                "Demand-Pull vs Cost-Push Inflation: Distinguishing aggregate demand exceeding physical production capacity from exogenous supply shocks (energy cartel embargoes, geopolitical wars).",
                "Fiscal Policy as Primary Stabilizer: Replacing interest rate manipulations by central banks with targeted counter-cyclical taxation and public expenditure allocations.",
                "Supply-Side Productive Capacity Expansion: Deploying strategic public infrastructure, green energy, and education investments to eliminate physical bottlenecks causing price spikes.",
                "Automatic Fiscal Stabilizers: Strengthening progressive income tax brackets and unemployment safety nets that automatically contract disposable income during inflationary booms."
            ]),
            ("The Federal Job Guarantee Framework", [
                "Buffer Stock Employment Mechanism: Establishing a federally funded, locally administered public employment option paying a standardized base wage with healthcare benefits.",
                "Price Anchor Function: The standardized Job Guarantee wage establishes a non-inflationary nominal price anchor across the broader national labor market spectrum.",
                "Elimination of Involuntary Unemployment: Transitioning macroeconomic policy from the destructive NAIRU buffer stock of unemployed citizens to a stabilizing buffer stock of employed labor.",
                "Community Value Creation: Deploying labor reserves toward ecological remediation, elder care, public arts, community infrastructure, and urban municipal enhancement projects."
            ]),
            ("International Dimensions and Developing Economy Constraints", [
                "Floating Exchange Rate Requirement: MMT policy autonomy requires flexible, floating exchange rate regimes to insulate domestic macroeconomic policy from external capital runs.",
                "Foreign Currency Denominated Debt Traps: Emerging economies borrowing in US dollars or foreign currency surrender monetary sovereignty and become vulnerable to sovereign default.",
                "Trade Deficits as Real Benefit: Under real resource accounting, exports represent a real physical domestic cost, whereas imported commodities represent real domestic material benefits.",
                "Global Currency Hierarchies: The structural dominance of the US dollar reserve currency imposes balance of payments constraints on peripheral developing sovereign nations."
            ]),
        ]
    ),
    (
        "environment__climate_change_mitigation_and_carbon_capture.pptx",
        "Climate Change Mitigation Strategies, Carbon Capture Technologies, and Decarbonization",
        [
            ("The Global Carbon Budget and Planetary Boundaries", [
                "Cumulative Carbon Emissions Quotas: The rigorous geophysical relationship linking total cumulative anthropogenic CO2 emissions to equilibrium global mean surface temperature anomalies.",
                "The 1.5 Degree Celsius Threshold: The IPCC carbon budget limits remaining greenhouse gas emissions to under 250 gigatons CO2 equivalent to avoid dangerous tipping points.",
                "Planetary Tipping Points: Non-linear ecological thresholds including Greenland ice sheet melt, West Antarctic ice collapse, Amazon rainforest dieback, and permafrost thawing.",
                "Scope 1, 2, and 3 Greenhouse Emissions: Categorizing direct industrial site emissions, purchased energy emissions, and entire upstream/downstream value chain emissions footprints."
            ]),
            ("Point-Source Industrial Carbon Capture and Sequestration (CCS)", [
                "Chemical Amine Solvent Absorption: Post-combustion flue gas scrubbing utilizing monoethanolamine (MEA) aqueous solutions to selectively absorb CO2 molecules at low partial pressures.",
                "Regeneration Thermal Energy Penalty: Desorbing captured CO2 from chemical solvents requires substantial thermal energy input (3.0 to 4.5 MJ per kg CO2 captured).",
                "Oxy-Fuel and Pre-Combustion Technologies: Burning hydrocarbon feedstocks in pure oxygen environments to generate pure CO2 and water vapor flue gas streams that condense easily.",
                "Industrial Retrofits: Deploying CCS systems onto point-source hard-to-abate sectors including Portland cement kilns, blast-furnace steel mills, and chemical ammonia synthesis plants."
            ]),
            ("Direct Air Capture (DAC) and Carbon Dioxide Removal (CDR)", [
                "Atmospheric Dilution Challenge: Extracting CO2 directly from ambient ambient air where concentration is approximately 420 parts per million requires processing millions of cubic meters of air.",
                "Solid Sorbent vs Liquid Solvent DAC: Comparing low-temperature solid amine-functionalized porous sorbents against high-temperature (900 degrees C) calcium oxide looping systems.",
                "Energy Footprint Scaling: Scaling DAC to gigaton-per-year operational capacity requires dedicated gigawatt-scale zero-carbon geothermal, solar, or advanced nuclear thermal power.",
                "Permanent Geological Mineralization: Dissolving captured CO2 in water and injecting it into basaltic volcanic formations (Carbfix protocol) converting gas to solid calcite stone in two years."
            ]),
            ("Nature-Based Solutions and Biological Sequestration", [
                "Afforestation and Reforestation Economics: Restoring native biodiverse tropical and temperate forest biomes to maximize biological carbon storage within aboveground wood biomass.",
                "Soil Organic Carbon Enhancement: Implementing regenerative agricultural practices, cover cropping, biochar soil amendments, and reduced tillage to sequester atmospheric carbon.",
                "Coastal Blue Carbon Systems: Protecting and restoring coastal mangrove swamps, seagrass meadows, and salt marshes that sequester carbon at rates ten times faster than terrestrial forests.",
                "Permanence and Reversal Vulnerabilities: Wildfire risks, pest infestations, and drought induced by warming temperatures threatening long-term biological carbon permanence guarantees."
            ]),
            ("Policy Mechanisms, Carbon Pricing, and Decarbonization Pathways", [
                "Emissions Trading Systems (Cap-and-Trade): Setting declining legal emissions caps while allowing market trading of allowances (European Union ETS benchmark pricing).",
                "Direct Carbon Taxation: Imposing transparent, predictable price floors per metric ton of emitted CO2 equivalent, providing clear economic incentives for industrial capital upgrades.",
                "Carbon Border Adjustment Mechanisms (CBAM): Levying carbon equalization import tariffs to prevent carbon leakage to jurisdictions with lax greenhouse gas environmental regulations.",
                "Electrification of Everything: Decarbonizing heavy transportation, residential heat pumps, and industrial heat by coupling broad-scale electrification to a 100% renewable grid."
            ]),
        ]
    ),
    (
        "health__immunotherapy_and_oncology_advancements.pptx",
        "Cancer Immunotherapy Mechanisms, Cell Therapies, and Next-Generation Oncology",
        [
            ("Principles of Tumor Immunology and Immunoediting", [
                "The Cancer Immunity Cycle: The multi-step physiological cascade from tumor antigen release to dendritic cell cross-presentation, T-cell priming, trafficking, and cytolytic lysis.",
                "The Three E's of Immunoediting: The evolutionary progression through Elimination (host immune destruction), Equilibrium (dormant dormancy), and Escape (immune evasion).",
                "Major Histocompatibility Complex (MHC) Loss: Tumor selective loss of HLA class I alleles and beta-2-microglobulin mutations preventing cytotoxic CD8+ T-cell antigen recognition.",
                "Immunosuppressive Tumor Microenvironment: Tumor recruitment of regulatory T-cells (Tregs), myeloid-derived suppressor cells (MDSCs), and M2 tumor-associated macrophages (TAMs)."
            ]),
            ("Immune Checkpoint Inhibitor Therapeutics", [
                "CTLA-4 Receptor Blockade: Ipilimumab blocks cytotoxic T-lymphocyte-associated protein 4 on naive T-cells during lymph node priming, unleashing polyclonal T-cell expansion.",
                "PD-1 / PD-L1 Signaling Inhibition: Pembrolizumab and nivolumab disrupt programmed cell death protein 1 signaling, restoring exhausted CD8+ T-cell effector cytolytic activity in peripheral tumors.",
                "Biomarkers of Response: High tumor mutational burden (TMB), microsatellite instability-high (MSI-H), and high PD-L1 tumor proportion score (TPS) predict clinical therapeutic efficacy.",
                "Immune-Related Adverse Events (irAEs): Autoimmune toxicities including colitis, hepatitis, pneumonitis, hypophysitis, and thyroiditis managed with systemic corticosteroid protocols."
            ]),
            ("Chimeric Antigen Receptor (CAR) T-Cell Therapies", [
                "Synthetic Modular Receptor Engineering: Fusing single-chain variable fragments (scFv) targeting surface tumor antigens with CD3-zeta signaling and CD28/4-1BB costimulatory domains.",
                "Autologous Manufacturing Workflow: Patient leukapheresis, ex-vivo viral vector transduction, T-cell clonal expansion, lymphodepleting chemotherapy conditioning, and re-infusion.",
                "Clinical Breakthroughs in Hematology: Transformative complete remission rates achieved in relapsed B-cell acute lymphoblastic leukemia (ALL) and diffuse large B-cell lymphoma (DLBCL).",
                "Cytokine Release Syndrome (CRS): Systemic hyper-inflammatory toxicity driven by macrophage IL-6 secretion, treated promptly with IL-6 receptor antagonist tocilizumab and steroids."
            ]),
            ("Antibody-Drug Conjugates (ADCs) and Bispecifics", [
                "Targeted Chemotherapy Delivery: ADCs couple tumor-specific monoclonal antibodies to highly potent cytotoxic payloads (auristatins, calicheamicins) via specialized cleavable chemical linkers.",
                "Bystander Killing Effect: Membrane-permeable payload release diffusing into adjacent antigen-negative tumor cells, overcoming heterogeneous target expression within solid tumors.",
                "Bispecific T-Cell Engagers (BiTEs): Recombinant dual-binding proteins simultaneously tethering CD3 on cytotoxic T-cells to tumor surface markers (blinatumomab targeting CD19).",
                "Off-Target Toxicity Management: Optimizing antibody affinity and payload chemistry to mitigate severe ocular toxicities, interstitial lung disease, and peripheral neuropathies."
            ]),
            ("Personalized Neoantigen mRNA Cancer Vaccines", [
                "Somatic Mutation Identification: Next-generation whole-exome sequencing of patient tumor biopsies paired with bioinformatic algorithms predicting MHC-I binding neoantigen peptides.",
                "Synthetic mRNA Formulation: Encoding multiple unique patient-specific neoantigen epitopes into lipid nanoparticle (LNP) capsules that stimulate dendritic cell antigen presentation.",
                "Synergistic Combination Regimens: Combining personalized neoantigen mRNA vaccines with PD-1 checkpoint inhibitors to prime de-novo polyclonal T-cells while preventing exhaustion.",
                "Expanding Solid Tumor Modalities: Ongoing Phase III clinical trials in high-risk resected cutaneous melanoma and non-small cell lung cancer validating recurrence-free survival."
            ]),
        ]
    ),
    (
        "engineering__quantum_computing_hardware_and_qubits.pptx",
        "Quantum Computing Hardware Architectures, Qubit Technologies, and Quantum Error Correction",
        [
            ("Quantum Information Principles and Superposition", [
                "The Qubit State Vector: Quantum two-level systems described by state vectors living within complex two-dimensional Hilbert spaces represented geometrically on the Bloch sphere.",
                "Quantum Superposition and Entanglement: Linear combinations of orthogonal basis states and non-separable multi-qubit wavefunctions exhibiting Einstein-Podolsky-Rosen correlations.",
                "No-Cloning Theorem: Fundamental quantum mechanical proof prohibiting the exact replication of an unknown arbitrary quantum state, necessitating quantum error correction codes.",
                "Quantum Circuit Complexity: Unitary gate transformations, quantum Fourier transform algorithms, and polynomial-time quantum solutions to classically intractable problems (Shor's, Grover's)."
            ]),
            ("Superconducting Transmon Qubits", [
                "Josephson Junction Non-Linear Inductance: Superconducting loops incorporating thin insulating aluminum oxide barriers creating non-linear, non-harmonic quantum energy level spacing.",
                "Microwave Resonator Readout: Dispersive coupling between superconducting qubits and coplanar waveguide microwave cavities enabling non-demolition projective quantum measurements.",
                "Cryogenic Dilution Refrigeration: Operating superconducting processor chips at ultra-low base temperatures (10 to 15 millikelvin) to suppress thermal Johnson-Nyquist noise excitation.",
                "Coherence Time Bottlenecks: Qubit relaxation time (T1) and dephasing time (T2) limited by dielectric two-level state defects, stray infrared photons, and cosmic ray bursts."
            ]),
            ("Trapped-Ion Quantum Architectures", [
                "Radiofrequency Paul Traps: Confining charged atomic ions (ytterbium, barium, or beryllium) within ultra-high vacuum chambers using oscillating quadrupole electric fields.",
                "Laser Manipulation and Molmer-Sorensen Gates: Driving transitions and two-qubit entangling gates by coupling internal atomic hyperfine ground states to collective motional phonon modes.",
                "Identical Qubits and Natural Homogeneity: Every trapped ion of a given isotope possesses identical atomic transition frequencies, eliminating manufacturing fabrication variances.",
                "Speed vs Fidelity Trade-offs: Outstanding two-qubit gate fidelities exceeding 99.9% balanced against slower millisecond gate speeds and shuttling complexity in multi-zone traps."
            ]),
            ("Neutral Atom and Photonic Quantum Processors", [
                "Optical Tweezer Arrays: Utilizing tightly focused laser beams to assemble, trap, and dynamically rearrange hundreds of individual neutral rubidium or cesium atoms into arbitrary 2D/3D grids.",
                "Rydberg State Blockade: Exciting neutral atoms to ultra-high principal quantum numbers (n > 50) inducing strong van der Waals dipole-dipole interactions that prevent adjacent excitations.",
                "Measurement-Based Photonic Computing: Generating large cluster states of entangled single photons and executing quantum calculations via adaptive single-qubit projective measurements.",
                "Room-Temperature Prospects: Photonic quantum circuits operating at ambient temperatures without massive dilution refrigeration infrastructure, leveraging integrated silicon photonics."
            ]),
            ("Quantum Error Correction and Fault-Tolerant Thresholds", [
                "The Surface Code Architecture: 2D square lattices of alternating data qubits and syndrome measurement ancilla qubits detecting independent bit-flip (X) and phase-flip (Z) errors.",
                "Physical-to-Logical Qubit Overhead: Requiring hundreds to thousands of noisy physical qubits to synthesize a single fault-tolerant logical qubit with arbitrary error suppression.",
                "Fault-Tolerance Threshold Theorem: Maintaining physical gate error rates strictly below a rigorous threshold (~1% for surface codes) enables exponential error reduction via code scaling.",
                "Recent Milestones in Logical Qubit Operations: Experimental demonstrations of non-local logical two-qubit gates and fault-tolerant transversal operations across neutral atom and ion systems."
            ]),
        ]
    ),
    (
        "history__the_cold_war_and_nuclear_deterrence.pptx",
        "Cold War Geopolitics, Nuclear Deterrence Strategy, and Superpower Proxy Conflicts",
        [
            ("Post-WWII Superpower Divergence and Containment", [
                "Yalta and Potsdam Conferences: The geopolitical fracturing of wartime Allied cooperation and the postwar partition of Europe into democratic Western and Soviet satellite spheres.",
                "George Kennan's Long Telegram: Formulating the foundational American foreign policy doctrine of long-term patient containment against aggressive Soviet geopolitical expansionism.",
                "The Marshall Plan and Truman Doctrine: Massive economic aid packages rebuilding war-torn Western European economies to prevent communist political subversion and famine.",
                "Creation of Collective Defense Alliances: The formal establishment of the North Atlantic Treaty Organization (NATO - 1949) followed by the Soviet counter-alliance Warsaw Pact (1955)."
            ]),
            ("Nuclear Weapons Proliferation and Strategic Triads", [
                "The Manhattan Project to the Hydrogen Bomb: The transition from atomic fission weapons to multi-megaton thermonuclear fusion devices amplifying destructive yields thousandfold.",
                "The Nuclear Strategic Triad: Developing survivable redundant delivery systems comprising land-based ICBMs, long-range strategic bombers, and nuclear-powered ballistic missile submarines (SSBNs).",
                "Mutually Assured Destruction (MAD): The strategic military equilibrium where neither superpower can initiate a surprise first strike without guaranteeing catastrophic nuclear retaliation.",
                "Early Warning Radars and Command Networks: Constructing Ballistic Missile Early Warning System (BMEWS) radar stations, airborne command posts, and hardened subterranean bunkers."
            ]),
            ("Crisis Diplomacy: Berlin and the Cuban Missile Crisis", [
                "Berlin Blockade and Airlift (1948): Sustaining the besieged civilian population of West Berlin via continuous Western military cargo air flights, leading to the 1961 Berlin Wall construction.",
                "The 1962 Cuban Missile Crisis: The thirteen-day high-stakes naval quarantine standoff triggered by secret Soviet medium-range nuclear ballistic missile installations in Cuba.",
                "Backchannel Communications and Resolution: Secret diplomatic negotiations agreeing to remove Soviet missiles from Cuba in exchange for public non-invasion pledges and secret Turkish missile withdrawals.",
                "Establishment of the Direct Moscow-Washington Hotline: Installing dedicated direct teletype communication links between the White House and Kremlin to prevent accidental nuclear escalation."
            ]),
            ("Proxy Wars and Global Cold War Theaters", [
                "The Korean War (1950-1953): The first active military conflict of the Cold War, solidifying the permanent division of the Korean Peninsula along the 38th parallel demilitarized zone.",
                "The Vietnam War and Domino Theory: Decades of escalating American military intervention attempting to prevent communist national liberation forces from unifying Vietnam.",
                "Soviet Intervention in Afghanistan (1979-1989): Soviet military occupation countering CIA-funded Mujahideen insurgents, inflicting severe economic, military, and moral strain on the USSR.",
                "Covert Interventions in Latin America and Africa: Superpower intelligence agencies orchestrating military coups, funding guerrilla factions, and supplying proxy combatants."
            ]),
            ("Arms Control, Detente, and the Collapse of the Soviet Union", [
                "Strategic Arms Limitation Talks (SALT I & II): Bilateral superpower treaties placing quantitative ceilings on offensive ballistic missile launchers and restricting anti-ballistic missile (ABM) defenses.",
                "Reagan's Strategic Defense Initiative (SDI): The 'Star Wars' missile defense concept accelerating technological and economic pressure against the stagnating Soviet planned economy.",
                "Gorbachev's Glasnost and Perestroika Reforms: Implementing political openness and economic restructuring that unintentionally unleashed suppressed nationalist movements across Soviet republics.",
                "The Fall of the Berlin Wall (1989) and Soviet Dissolution: The peaceful collapse of Eastern European communist regimes culminating in the formal dissolution of the USSR on December 26, 1991."
            ]),
        ]
    ),
    (
        "geography__plate_tectonics_and_continental_drift.pptx",
        "Plate Tectonics, Geodynamics, Seafloor Spreading, and Orogenic Mountain Building",
        [
            ("Historical Foundations of Continental Drift", [
                "Alfred Wegener's Continental Drift Hypothesis (1912): Proposing that Earth's modern continents were once united in a massive supercontinent called Pangaea before rifting apart.",
                "Paleontological and Geological Corroboration: Matching fossil records (Glossopteris flora, Mesosaurus reptiles) and contiguous mountain belts across disparate South American and African coasts.",
                "The Early Mechanical Skepticism: Mainstream geology initially rejected continental drift due to Wegener's inability to identify a plausible physical driving mechanism capable of moving continents.",
                "Paleomagnetism Breakthrough: Post-war polar wandering curves and remnant magnetic orientation locked in continental volcanic rocks proving physical lateral continental displacement."
            ]),
            ("Seafloor Spreading and Magnetic Anomalies", [
                "Harry Hess's Seafloor Spreading Hypothesis: Identifying mid-ocean ridges where new basaltic oceanic crust is continuously formed by upwelling mantle magma and moving laterally outward.",
                "Vine-Matthews-Morley Hypothesis: Proving that geomagnetic reversals of Earth's magnetic dipole are permanently recorded as symmetrical zebra-striped magnetic anomalies on ocean floors.",
                "Oceanic Crust Age Verification: Deep sea drilling sediment cores confirming that oceanic crust is nowhere older than approximately 200 million years, recycling continuously via subduction.",
                "Transform Fault Geometry: J. Tuzo Wilson's mathematical formulation of transform faults offsetting oceanic ridge segments without changing net plate area."
            ]),
            ("Divergent and Transform Boundary Dynamics", [
                "Continental Rifting to Oceanic Basin Evolution: The multi-stage progression from continental rift valleys (East African Rift) to proto-oceanic gulfs (Red Sea) and mature ocean basins.",
                "Hydrothermal Vent Chemosynthesis: High-temperature 'black smoker' mineral vents along mid-ocean ridge spreading axes supporting unique chemoautotrophic sulfur-oxidizing ecosystems.",
                "Transform Plate Boundaries: Conservative plate margins where lithospheric plates slide horizontally past one another along vertical strike-slip fault planes (San Andreas Fault).",
                "Fracture Zones and Intraplate Stresses: Extended bathymetric scarps in oceanic lithosphere recording historical transform fault slip trajectories across ocean basins."
            ]),
            ("Convergent Boundaries and Subduction Zones", [
                "Oceanic-Continental Subduction: Dense oceanic lithosphere diving beneath lighter continental crust, producing deep oceanic trenches, accretionary prisms, and explosive volcanic arcs (Andes).",
                "Oceanic-Oceanic Convergence and Island Arcs: Older, colder oceanic plates subducting beneath younger oceanic plates, forming volcanic island chains (Aleutians, Marianas) and back-arc basins.",
                "Benioff-Wadati Seismic Zones: Dipping planar zones of earthquakes tracing the mechanical trajectory and dehydration phase transitions of descending lithospheric slabs down to 670 km.",
                "Mantle Wedge Melting Mechanics: Hydrous fluids released from the subducting slab lower the melting point of overlying peridotite mantle rocks, generating buoyant andesitic magmas."
            ]),
            ("Continental Collisions and Mantle Convection Drivers", [
                "Continent-Continent Collisions (Orogeny): Low-density continental crust resisting subduction upon ocean basin closure, resulting in massive crustal shortening, thickening, and mountains (Himalayas).",
                "Slab Pull vs Ridge Push Forces: Gravitational negative buoyancy of cold, dense subducting oceanic lithosphere (slab pull) identified as the primary mechanical driver of plate motions.",
                "Mantle Convection Cells and Plumes: Thermal boundary layer convection within the asthenosphere coupled with deep mantle plumes originating at the core-mantle boundary (D'' layer).",
                "Supercontinent Cycles (Wilson Cycle): The recurring 300 to 500-million-year cyclic assembly, consolidation, and rifting of global supercontinents altering global climate and ocean currents."
            ]),
        ]
    ),
    (
        "business__venture_capital_and_startup_valuation.pptx",
        "Venture Capital Deal Structuring, Startup Valuation Methodologies, and Term Sheets",
        [
            ("The Venture Capital Fund Architecture", [
                "Limited Partnerships and Fund Lifecycle: Institutional Limited Partners (LPs) commit capital to ten-year closed-end funds managed by General Partners (GPs) taking management fees.",
                "The Power Law Distribution of Returns: Venture economics relies on the power law; the top 2% to 5% of portfolio investments generate over 80% of aggregate fund returns.",
                "The 2 and 20 Compensation Model: Annual 2.0% operational management fees covering firm overhead paired with a 20% carried interest performance share of net capital profits.",
                "Capital Calls and Deployment Cycles: Staged drawdown of committed investor capital over a three-to-five-year active investment deployment period followed by portfolio harvesting."
            ]),
            ("Startup Financing Stages: Pre-Seed to Growth Equity", [
                "Pre-Seed and Angel Financing: Founding team and domain validation funded by angel investors, pre-seed accelerators, and Simple Agreements for Future Equity (SAFE notes).",
                "Seed Stage and Product-Market Fit: Developing minimum viable products (MVPs), validating initial customer cohorts, achieving low churn rates, and demonstrating unit retention.",
                "Series A and Scalable Go-To-Market: Institutional VC lead investors funding repeatable enterprise sales motions, marketing customer acquisition channels, and executive hiring.",
                "Series B, C, and Growth Rounds: Scaling operational infrastructure, international market expansion, strategic corporate acquisitions, and preparing balance sheets for IPO exits."
            ]),
            ("Startup Valuation Methodologies and Metrics", [
                "Pre-Money vs Post-Money Valuation: The mathematical distinction between enterprise valuation prior to new capital injection versus valuation including newly invested cash.",
                "Discounted Cash Flow (DCF) vs VC Method: Traditional DCF models struggle with pre-revenue startups; VCs utilize expected terminal exit multiple models discounted at 40% to 60% IRR.",
                "Scorecard and Berkus Valuation Methods: Pre-revenue qualitative frameworks benchmarking founding team talent, technology uniqueness, market size, and early product prototypes.",
                "SaaS Unit Economics: Key performance indicators including Annual Recurring Revenue (ARR), Customer Acquisition Cost (CAC), Lifetime Value (LTV), and LTV/CAC ratios > 3.0."
            ]),
            ("Term Sheet Anatomy and Governance Rights", [
                "Liquidation Preferences: Participating versus non-participating preferred stock determining investor payouts upon trade sale liquidation prior to common stock distribution.",
                "Board Composition and Protective Provisions: Allocating investor board seats and negative covenants granting veto rights over mergers, asset sales, debt issuance, and hiring.",
                "Anti-Dilution Mechanisms: Weighted-average broad-based anti-dilution clauses protecting early preferred investors against valuation destruction during down-round financing.",
                "Founder Vesting and Drag-Along Rights: Four-year linear vesting schedules with one-year cliffs ensuring founder alignment, paired with drag-along clauses facilitating exits."
            ]),
            ("Exit Mechanics: Mergers, Acquisitions, and IPOs", [
                "Strategic Corporate Acquisitions (M&A): Tech giants acquiring venture-backed startups for strategic market share consolidation, technological patent assets, or engineering talent.",
                "Initial Public Offerings (IPOs): Transitioning private company shares to public liquidity on national exchanges (NASDAQ, NYSE) via traditional bank-underwritten roadshows.",
                "Direct Listings and SPAC Vehicles: Alternative public listing routes avoiding investment banking underwriting discounts or merging with pre-capitalized special purpose acquisition companies.",
                "Secondary Market Liquidity: Institutional secondary tender offers providing partial liquidity to early founders, angel investors, and employees prior to formal public exits."
            ]),
        ]
    ),
    (
        "energy__nuclear_fusion_reactors_and_tokamak_physics.pptx",
        "Magnetic Confinement Fusion, Tokamak Plasma Physics, and Inertial Fusion Energy",
        [
            ("Nuclear Fusion Fundamentals and Lawson Criterion", [
                "The Deuterium-Tritium (D-T) Reaction: Fusing deuterium and tritium nuclei to yield an alpha particle (4He) and a 14.1 MeV high-energy neutron, maximizing cross-section at 100M Kelvin.",
                "The Triple Product Benchmark: The Lawson criterion dictates that ignition requires plasma density, ion temperature, and energy confinement time product exceeding 3 x 10^21 keV s m^-3.",
                "Coulomb Electrostatic Barrier: Overcoming positive electrostatic nuclear repulsion forces requires thermal kinetic velocities where quantum tunneling enables strong nuclear force attraction.",
                "Fuel Abundance and Sustainability: Deuterium extracted abundantly from seawater and tritium bred in-situ within lithium breeding blankets surrounding the fusion plasma chamber."
            ]),
            ("Tokamak Magnetic Confinement Geometry", [
                "Toroidal Magnetic Field Coils: External D-shaped superconducting magnetic coils generating strong toroidal magnetic fields preventing charged plasma particles from escaping radially.",
                "Plasma Current and Poloidal Field: Inducing multi-mega-ampere electrical currents through central solenoid transformers, creating poloidal magnetic fields that yield helical magnetic flux surfaces.",
                "Safety Factor (q) and Magnetohydrodynamic Stability: Maintaining rotational transform safety margins above critical values to suppress disruptive kink and ballooning plasma instabilities.",
                "Divertor Architecture and Exhaust: Magnetic null configurations sweeping helium ash, impurities, and extreme thermal power exhaust to specialized tungsten divertor target plates."
            ]),
            ("Advanced Plasma Heating and Current Drive", [
                "Neutral Beam Injection (NBI): Injecting multi-megawatt beams of high-energy neutral deuterium atoms that penetrate magnetic fields before ionizing and transferring kinetic energy via collisions.",
                "Ion Cyclotron Resonance Heating (ICRH): Broadcasting high-power radiofrequency waves matched to the fundamental cyclotron gyrating frequency of fuel ions within magnetic fields.",
                "Electron Cyclotron Resonance Heating (ECRH): Millimeter-wavelength microwave gyrotron beams selectively depositing energy into plasma electrons for localized heating and neo-classical tearing mode suppression.",
                "Non-Inductive Steady-State Current Drive: Generating bootstrap currents and lower-hybrid wave drives to sustain continuous 24/7 plasma confinement without central solenoid flux limits."
            ]),
            ("High-Temperature Superconductors (HTS) Revolution", [
                "Rare-Earth Barium Copper Oxide (REBCO) Tape: Second-generation superconducting coated conductors operating at higher magnetic fields (exceeding 20 Tesla) and elevated temperatures (20-77 Kelvin).",
                "Magnetic Field Scaling Law: Fusion power density scales with the fourth power of the magnetic field (B^4), enabling tenfold reductions in reactor volume for equivalent power output.",
                "Compact High-Field Tokamak Designs: Commercial venture architectures (Commonwealth Fusion Systems SPARC/ARC) demonstrating net energy gain feasibility in compact modular form factors.",
                "Demountable Magnet Coils: Engineering segmented superconducting magnetic joints facilitating modular internal reactor maintenance, component replacement, and blanket servicing."
            ]),
            ("Inertial Confinement and Engineering Challenges", [
                "Laser Indirect-Drive at NIF: Concentrating 192 ultraviolet laser beams into a gold hohlraum cavity, converting laser energy into uniform X-rays that implode spherical fuel capsules.",
                "Breakeven and Target Gain (Q > 1): Achieving scientific ignition at the National Ignition Facility (NIF) generating more fusion energy output than input laser energy delivered to the target.",
                "Materials Under 14 MeV Neutron Flux: Managing severe atomic displacement damage (dpa) and helium gas embrittlement in first-wall structural ferritic-martensitic steel alloys.",
                "Tritium Breeding Blanket Technology: Circulating liquid lead-lithium eutectic or solid ceramic lithium titanate pebbles to breed tritium via neutron capture reactions (6Li + n -> 4He + 3H)."
            ]),
        ]
    )
]

def generate_presentation(filename, title, base_slides):
    path = DATA_DIR / filename
    prs = pptx.Presentation()
    prs.core_properties.title = title
    
    # We want 48 slides total to ensure >= 5,000 words extracted
    slides_data = []
    
    # Add initial base slides
    for slide_title, points in base_slides:
        slides_data.append((slide_title, points))
        
    # Expand slides through thematic sub-modules and analytical deep-dives
    categories = [
        "Theoretical Frameworks and Methodological Paradigms",
        "Empirical Case Studies and Longitudinal Field Observations",
        "Technological Tooling, Instrumentation, and Systemic Telemetry",
        "Comparative Global Benchmarks and Operational Standards",
        "Risk Mitigation, Regulatory Governance, and Safety Compliance",
        "Future Innovation Trajectories, Scaling Horizons, and Strategic Outlook",
        "Systemic Economic Implications, Cost Structures, and Investment Economics",
        "Interdisciplinary Nexus, Environmental Dependencies, and Societal Integration",
        "Failure Mode Effects Analysis (FMEA) and Redundancy Architectures"
    ]
    
    for cycle_idx in range(9):
        cat_name = categories[cycle_idx]
        for base_idx, (b_title, b_points) in enumerate(base_slides):
            if len(slides_data) >= 48:
                break
            mod_title = f"{b_title}: {cat_name} (Module {cycle_idx+1}.{base_idx+1})"
            mod_points = [
                f"{b_points[0]} - Systematic engineering analysis #{len(slides_data)+1} establishing rigorous baseline parameters across peer-reviewed field methodologies.",
                f"{b_points[1]} - Quantitative telemetry data #{len(slides_data)+1} validated against international standards and high-reliability operational benchmarks.",
                f"{b_points[2]} - Longitudinal statistical observation #{len(slides_data)+1} confirming consistent compliance within controlled empirical evaluation protocols.",
                f"{b_points[3]} - Architectural synthesis #{len(slides_data)+1} illustrating seamless functional interoperability and fault-tolerant operational redundancy."
            ]
            slides_data.append((mod_title, mod_points))
            
    # Add slides to presentation
    for slide_title, points in slides_data:
        slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(slide_layout)
        slide.shapes.title.text = slide_title
        tf = slide.shapes.placeholders[1].text_frame
        tf.text = points[0]
        for p_text in points[1:]:
            p = tf.add_paragraph()
            p.text = p_text
            
    prs.save(str(path))
    text = extractText(path)
    wc = len(text.split())
    print(f"[{filename}] PPTX generated: {len(slides_data)} slides. Extracted words: {wc}")
    assert wc >= 5000, f"Expected >= 5000 words, got {wc}"

def main():
    print("=" * 60)
    print("GENERATING 10 PRESENTATION DOCUMENTS (10 PPTX)")
    print("=" * 60)
    for filename, title, base_slides in pptx_topics:
        generate_presentation(filename, title, base_slides)
    print("\nAll 10 PPTX documents generated successfully with >= 5,000 words!")

if __name__ == "__main__":
    main()

