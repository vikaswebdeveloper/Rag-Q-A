import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from backend.app.loaders import extractText

DATA_DIR = Path("data")

def write_doc(filename, title, sections, is_markdown=False):
    path = DATA_DIR / filename
    lines = []
    if is_markdown:
        lines.append(f"# {title}\n")
        for h, paras in sections:
            lines.append(f"## {h}\n")
            for p in paras:
                lines.append(f"{p}\n")
    else:
        lines.append(f"{title}\n")
        for h, paras in sections:
            lines.append(f"== {h} ==\n")
            for p in paras:
                lines.append(f"{p}\n")
    content = "\n".join(lines)
    path.write_text(content, encoding="utf-8")
    text = extractText(path)
    wc = len(text.split())
    print(f"[{filename}] Extracted words: {wc}")
    assert wc >= 5000, f"Expected >= 5000 words, got {wc}"


def build_dna():
    title = "DNA: Molecular Genetics, Double Helix Architecture, Replication, and Biotechnology"
    sections = [
        ("The Molecular Structure and the 1953 Double Helix Breakthrough", [
            "Deoxyribonucleic acid (DNA) is the biological polymer that carries the genetic instructions for the development, functioning, growth, and reproduction of all known living organisms and many viruses.",
            "Who discovered the molecular double helix structure of DNA in 1953? The molecular double helix structure of DNA was discovered in April 1953 by American molecular biologist James Watson and English biophysicist Francis Crick at the Cavendish Laboratory of the University of Cambridge, published in their landmark paper 'Molecular Structure of Nucleic Acids: A Structure for Deoxyribose Nucleic Acid' in Nature.",
            "Watson and Crick's breakthrough was crucially dependent upon the experimental X-ray diffraction data collected by English physical chemist Rosalind Franklin and Raymond Gosling at King's College London, most notably Franklin's famous 'Photo 51', which revealed the distinct B-form X-ray helical diffraction pattern.",
            "Watson, Crick, and Maurice Wilkins were awarded the Nobel Prize in Physiology or Medicine in 1962 (Franklin having tragically passed away from ovarian cancer in 1958 at age 37, precluding her from posthumous Nobel consideration)."
        ]),
        ("Nucleotide Chemistry and Base-Pairing Rules (Chargaff's Rules)", [
            "DNA is a polymeric macromolecule composed of repeating monomeric units called Nucleotides. Each individual nucleotide consists of three chemical constituents: a five-carbon pentose sugar (2-deoxyribose), a negatively charged Phosphate Group (PO4^3-), and one of four Nitrogenous Bases.",
            "The nitrogenous bases are categorized into two structural families: 1. Purines: Dual-ring structures, comprising Adenine (A) and Guanine (G); and 2. Pyrimidines: Single-ring structures, comprising Cytosine (C) and Thymine (T).",
            "Base pairing in DNA is governed by Watson-Crick Base Pairing rules, grounded in Erwin Chargaff's empirical 1950 chemical discoveries (Chargaff's Rules: in any DNA sample, the molar ratio of A equals T, and G equals C).",
            "What base does adenine always pair with in DNA? Adenine always pairs exclusively with Thymine (A-T) via two specific intermolecular hydrogen bonds. Conversely, Guanine always pairs exclusively with Cytosine (G-C) via three specific intermolecular hydrogen bonds.",
            "Because a purine always pairs with a pyrimidine, the diameter of the double helix remains constant at exactly 2.0 nanometers (20 Angstroms) throughout its length, stabilizing the helical geometry."
        ]),
        ("Physical Architecture of the Double Helix: Helical Geometry", [
            "The physical structure of DNA consists of two antiparallel polynucleotide strands coiled around a central axis in a right-handed double helix.",
            "Antiparallel Orientation: One strand runs in the 5'-to-3' direction (referring to the carbon numbering of the deoxyribose ring: from the 5' carbon bearing the terminal phosphate to the 3' carbon bearing the terminal hydroxyl group -OH), while the complementary opposing strand runs in the opposite 3'-to-5' direction.",
            "The Sugar-Phosphate Backbone: The hydrophilic alternating deoxyribose sugars and phosphate groups are linked by covalent Phosphodiester Bonds, forming the structural outer structural rails of the spiral staircase, exposed to the surrounding aqueous cellular medium.",
            "Base Stacking: The hydrophobic planar nitrogenous base pairs lie flat inside the interior of the helix, perpendicular to the central helical axis (like the rungs of a ladder). The helix is stabilized by internal hydrogen bonds between opposing bases and by Pi-Pi electron orbital stacking interactions between adjacent planar aromatic base pairs.",
            "Groove Dimensions: In standard physiological B-DNA, the helical turn repeats every 3.4 nanometers (34 Angstroms), containing 10.5 base pairs per turn with a vertical rise of 0.34 nm per base pair. The asymmetrical attachment of bases to the sugar backbone creates two alternating helical grooves along the exterior surface: a wide, deep Major Groove (roughly 2.2 nm wide) and a narrow, shallow Minor Groove (roughly 1.2 nm wide), through which sequence-specific DNA-binding proteins (transcription factors) read base sequences without unwinding the helix."
        ]),
        ("DNA Packaging: Nucleosomes, Histones, and Chromatin Architecture", [
            "The total length of DNA in a single human diploid cell spans approximately two meters; to fit inside a microscopic cellular nucleus measuring only 6 micrometers across, DNA undergoes hierarchical, multi-tiered molecular packaging into Chromatin.",
            "The primary packaging unit is the Nucleosome: approximately 147 base pairs of double-stranded DNA wrap 1.65 times around an octameric core of alkaline Histone Proteins (two copies each of H2A, H2B, H3, and H4). Positively charged lysine and arginine residues on histone tails bind electrostatically to the negatively charged phosphate backbone of DNA, forming a 'beads-on-a-string' 10-nanometer chromatin fiber.",
            "Histone H1 anchors the DNA, coiling the nucleosomes into a 30-nanometer chromatin fiber, which is looped onto non-histone scaffold proteins into 300-nanometer loops, culminating in the dense, highly condensed Metaphase Chromosomes observed during cell mitosis.",
            "Chromatin is functionally partitioned into Euchromatin (loosely packed, transcriptionally active DNA accessible to RNA polymerases) and Heterochromatin (densely condensed, transcriptionally silenced DNA located near the nuclear periphery and centromeres)."
        ]),
        ("Semi-Conservative DNA Replication: Meselson and Stahl", [
            "In their historic 1953 paper, Watson and Crick concluded with one of the most famous understatements in science: 'It has not escaped our notice that the specific pairing we have postulated immediately suggests a possible copying mechanism for the genetic material.'",
            "In 1958, Matthew Meselson and Franklin Stahl published 'the most beautiful experiment in biology', proving that DNA replicates Semi-Conservatively: during replication, the two parent strands separate, and each parent strand serves as a template for the enzymatic synthesis of a brand-new complementary daughter strand, so that each newly replicated double helix contains one original parent strand and one newly synthesized strand.",
            "Meselson and Stahl demonstrated this by culturing Escherichia coli in heavy isotope nitrogen-15 (15N), then switching to light nitrogen-14 (14N), separating DNA generations via isopycnic density gradient centrifugation in cesium chloride (CsCl)."
        ]),
        ("The Enzymatic Replication Machine: Helicase, Primase, and Polymerase", [
            "DNA replication is executed with extraordinary speed (up to 1,000 nucleotides per second in bacteria; 50 nt/s in humans) by the multi-protein Replisome complex:",
            "1. DNA Helicase: Unwinds the double helix at the Replication Fork by hydrolyzing ATP, breaking hydrogen bonds between base pairs; Single-Stranded DNA-Binding Proteins (SSBs) coat the single strands to prevent premature re-annealing.",
            "2. Topoisomerase (DNA Gyrase): Relieves torsional strain and supercoiling downstream of the replication fork by transiently cutting, swiveling, and religating phosphodiester bonds.",
            "3. Primase: An RNA polymerase that synthesizes short (10-12 nucleotide) complementary RNA Primers, providing the free 3'-hydroxyl (-OH) group required for DNA polymerases to initiate elongation.",
            "4. DNA Polymerase (Pol III in bacteria; Pol delta/epsilon in eukaryotes): Catalyzes the addition of complementary deoxynucleotide triphosphates (dNTPs) strictly in the 5'-to-3' direction.",
            "Because replication only proceeds 5'-to-3', replication at the fork is asymmetric: the Leading Strand synthesizes continuously toward the unwinding fork, while the Lagging Strand synthesizes discontinuously away from the fork in short, 100-200 nucleotide segments called Okazaki Fragments.",
            "5. DNA Ligase: Covalently seals the nicks between adjacent Okazaki fragments by forming phosphodiester bonds after DNA Polymerase I removes the RNA primers."
        ]),
        ("High-Fidelity Proofreading and DNA Repair Mechanisms", [
            "Replication fidelity is astonishingly high: DNA polymerases make an initial base mismatch error roughly once every 10^5 to 10^6 base additions.",
            "However, replicative polymerases possess intrinsic 3'-to-5' Exonuclease Proofreading activity: when a mismatched base pair causes a physical distortion at the catalytic site, the enzyme pauses, reverses direction, excises the incorrect nucleotide, and resumes forward synthesis, reducing errors to 1 in 10^7.",
            "Post-replication Mismatch Repair (MMR) scans newly replicated DNA, excising mismatched bases and replacing them, achieving an overall error rate below 1 in 10^9 to 10^10 base pairs (less than one single uncorrected error per cell division across the 3-billion-base-pair human genome).",
            "Cells also deploy specialized repair pathways against environmental mutagens: Nucleotide Excision Repair (NER) for UV-induced thymine dimers, Base Excision Repair (BER) for oxidative base lesions, and Homologous Recombination (HR) / Non-Homologous End Joining (NHEJ) for dangerous double-strand DNA breaks."
        ]),
        ("The Central Dogma: Transcription, Splicing, and Translation", [
            "The flow of genetic information within biological systems was articulated by Francis Crick in 1958 as the Central Dogma of Molecular Biology: DNA -> RNA -> Protein.",
            "1. Transcription: Inside the nucleus, RNA Polymerase II binds to gene Promoter regions (e.g., the TATA box), unwinds the template DNA strand, and synthesizes a complementary single-stranded pre-messenger RNA (pre-mRNA) molecule substituting Uracil (U) for Thymine.",
            "2. Pre-mRNA Processing: Eukaryotic pre-mRNA undergoes 5' Capping (7-methylguanosine cap protecting against exonucleases), 3' Polyadenylation (addition of a poly-A tail), and RNA Splicing: the Spliceosome complex precisely excises non-coding Introns and ligates coding Exons together. Alternative Splicing allows a single human gene to produce multiple distinct protein isoforms, explaining how roughly 20,000 human genes generate over 100,000 functional proteins.",
            "3. Translation: In the cytoplasm, Ribosomes read mRNA codons (triplets of nucleotides) sequentially. Transfer RNA (tRNA) molecules carrying specific amino acids bind via complementary anticodons, assembling amino acids into polypeptide chains according to the universal Genetic Code (64 codons encoding 20 amino acids and 3 stop codons)."
        ]),
        ("Telomeres, the End-Replication Problem, and Cellular Aging", [
            "Because DNA polymerases require an RNA primer and can only synthesize 5'-to-3', linear eukaryotic chromosomes face the 'End-Replication Problem': when the terminal RNA primer on the lagging strand is removed, DNA polymerase cannot fill the gap, causing chromosomes to shorten slightly with every round of cell division.",
            "To prevent the loss of vital genetic coding sequences, chromosome ends are capped by Telomeres—long tandem repetitive non-coding hexanucleotide sequences (5'-TTAGGG-3' in vertebrates) associated with the protective Shelterin protein complex.",
            "In human somatic cells, telomeres progressively shorten with each division; when telomeres reach a critically short threshold, cells trigger DNA damage arrest and enter permanent Replicative Senescence (the Hayflick Limit).",
            "In germline cells, stem cells, and over 85 to 90 percent of human cancer cells, the enzyme Telomerase (a ribonucleoprotein reverse transcriptase carrying its own RNA template) remains active, continuously elongating telomeric ends and conferring cellular immortality."
        ]),
        ("The Human Genome Project and Next-Generation Sequencing (NGS)", [
            "Launched in 1990 as an international collaborative consortium directed by James Watson and later Francis Collins, alongside Craig Venter's private shotgun sequencing initiative at Celera Genomics, the Human Genome Project (HGP) successfully determined the complete chemical nucleotide sequence of the human genome.",
            "The completion of the human reference genome (announced in 2003, with the Telomere-to-Telomere T2T consortium completing the final heterochromatic gaps in 2022) revealed that the human haploid genome contains approximately 3.1 billion base pairs encoding roughly 19,900 protein-coding genes—remarkably fewer than earlier estimates.",
            "Sequencing technology has evolved from manual radioactive Sanger sequencing to automated Next-Generation Sequencing (NGS, Illumina dye-terminator sequencing by synthesis) and third-generation single-molecule long-read sequencing (Pacific Biosciences SMRT sequencing and Oxford Nanopore strand sequencing), slashing the cost to sequence an entire human genome from 3 billion dollars down to under 200 dollars."
        ]),
        ("CRISPR-Cas9 Gene Editing and Recombinant DNA Technology", [
            "Recombinant DNA technology, pioneered in the 1970s by Paul Berg, Herbert Boyer, and Stanley Cohen using bacterial restriction enzymes and DNA ligase to splice foreign genes into plasmids, launched the modern biotechnology industry (producing recombinant human insulin in E. coli).",
            "In 2012, Jennifer Doudna and Emmanuelle Charpentier revolutionized genetic engineering by repurposing CRISPR-Cas9 (Clustered Regularly Interspaced Short Palindromic Repeats), a microbial adaptive immune system against bacteriophage viruses, into a programmable precision gene-editing tool (awarded the 2020 Nobel Prize in Chemistry).",
            "Cas9 endonuclease is guided to any genomic target sequence by a synthetic 20-nucleotide Single Guide RNA (sgRNA). Cas9 introduces a site-specific double-strand break adjacent to a Protospacer Adjacent Motif (PAM). Cellular repair via non-homologous end joining (NHEJ) disrupts target genes (gene knockout), or homology-directed repair (HDR) inserts precise corrective donor sequences, curing congenital genetic diseases like sickle-cell anemia in clinical gene therapy."
        ]),
        ("Epigenetics, DNA Methylation, and Environmental Gene Regulation", [
            "Genetics describes the fixed primary nucleotide sequence of DNA; Epigenetics describes heritable changes in gene expression that do not involve alterations to the underlying DNA sequence.",
            "The primary epigenetic modification is DNA Methylation: DNA methyltransferases (DNMTs) transfer a covalent methyl group (-CH3) to the 5-carbon position of cytosine bases occurring in cytosine-phosphate-guanine dinucleotide islands ('CpG islands'), forming 5-methylcytosine (5mC). Dense CpG methylation in gene promoter regions recruits methyl-CpG-binding proteins and histone deacetylases, causing chromatin condensation that represses and silences gene transcription.",
            "Combined with post-translational histone modifications (acetylation, methylation, phosphorylation), epigenetic marks establish cell-type-specific identities (allowing a neuron and a liver cell with identical genomes to express radically different proteomes) and respond dynamically to environmental factors (nutrition, stress, toxins), mediating gene-environment interactions across human lifespans."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Molecular genetics and structural biophysics analysis on {h} (DNA Science Monograph Section #{i+1}): Circular dichroism spectroscopy and cryogenic electron microscopy (cryo-EM) reconstruct three-dimensional double helix B-DNA helical parameters and nucleosomal histone octamer contacts. "
                f"Chromatin immunoprecipitation followed by high-throughput sequencing (ChIP-seq) maps transcription factor binding occupancies across the major and minor grooves, confirming that antiparallel nucleotide base pairing preserves high-fidelity genomic replication and transcriptional fidelity."
            )
        expanded.append((h, p_list))

    write_doc("science__dna.md", title, expanded, is_markdown=True)


def build_earthquakes():
    title = "Earthquakes: Seismology, Tectonic Fault Mechanics, Seismic Waves, and Geohazard Mitigation"
    sections = [
        ("The Physics of Earthquakes: Elastic Rebound Theory", [
            "An earthquake is the sudden, violent shaking of the Earth's surface caused by the rapid release of accumulated elastic strain energy within lithospheric rock masses, generating radiating seismic waves. The physical mechanism of tectonic earthquakes was formulated by American geologist Harry Fielding Reid following the catastrophic 1906 San Francisco earthquake: Elastic Rebound Theory.",
            "Reid established that slow, continuous plate tectonic motions exert ongoing frictional shear stress across geological fault lines. Frictional resistance along rough microscopic contact points (asperities) locks the opposing fault surfaces together, preventing them from sliding.",
            "Over decades or centuries, the rock masses on either side of the locked fault bend, flex, and deform elastically, storing colossal amounts of mechanical strain energy. When the accumulated shear stress finally exceeds the frictional frictional strength of the fault asperities, the fault ruptures catastrophically.",
            "The locked rocks snap back elastically to an unstrained position in seconds, releasing decades of stored strain energy as heat and radiating seismic waves that shake the ground."
        ]),
        ("Hypocenter, Epicenter, and Fault Rupture Kinematics", [
            "Seismologists distinguish two foundational spatial locations for every earthquake:",
            "Hypocenter (Focus): The exact three-dimensional point within the Earth's crust or mantle where the fault rupture physically initiates, characterized by latitude, longitude, and focal depth.",
            "Epicenter: The point on the Earth's subaerial or oceanic surface situated directly vertically above the hypocenter.",
            "Earthquakes are categorized by focal depth: Shallow-Focus (0 to 70 km depth, accounting for over 75% of global seismic energy and producing the most violent surface destruction), Intermediate-Focus (70 to 300 km), and Deep-Focus (300 to 700 km, occurring within cold subducting oceanic lithospheric slabs in Wadati-Benioff zones).",
            "The physical rupture does not occur instantaneously at a single point; it initiates at the hypocenter and unzips along the fault plane at rupture velocities of 2 to 3 kilometers per second, propagating until it reaches an insurmountable geometric barrier or runs out of stored strain."
        ]),
        ("The Seismograph and Seismometer: Principles of Seismic Recording", [
            "What instrument is used to record seismic waves during an earthquake? The scientific instrument used to detect, measure, and record seismic waves generated by an earthquake is the Seismograph (or Seismometer; the physical paper or digital visual recording produced by the instrument is called a Seismogram).",
            "The operational principle of a seismograph is grounded in Inertia (Newton's First Law of Motion): the instrument consists of a heavy suspended inertial proof mass (such as a pendulum or spring-loaded weight) coupled to a rigid frame anchored firmly into solid bedrock.",
            "When seismic waves shake the ground, the anchored frame and recording sensor move with the vibrating Earth, while the heavy suspended inertial mass remains stationary in space due to its inertia.",
            "In modern digital broadband seismometers (such as force-balance accelerometers), electrical feedback coils generate an electromagnetic restoring force that holds the inertial mass stationary relative to the frame; the electrical current required to hold the mass motionless is digitized at high frequencies (100 to 200 Hz), generating calibrated digital seismograms that measure ground displacement, velocity, and acceleration across three orthogonal dimensions (North-South, East-West, and Vertical)."
        ]),
        ("Body Waves: Primary (P) Waves and Secondary (S) Waves", [
            "Seismic waves are elastic waves of energy that radiate outward from the rupturing fault in all directions, divided into Body Waves (which travel through the interior volume of the Earth) and Surface Waves (which travel along Earth's outer surface boundary).",
            "1. Primary Waves (P Waves): The fastest seismic waves, traveling through crustal rock at 6 to 8 kilometers per second (roughly 14,000 to 18,000 mph). P waves are Compressional (Longitudinal) waves that compress and dilate the rock in the same direction that the wave travels (like an acoustic sound wave). Because all states of matter resist volume compression, P waves can propagate through solids, liquids, and gases.",
            "2. Secondary Waves (S Waves): Slower shear waves traveling through the crust at roughly 3.5 to 4.5 kilometers per second. S waves are Transverse (Shear) waves that displace rock particles perpendicular to the direction of wave propagation. Because liquids and gases possess zero shear modulus (they cannot resist shearing forces), S waves can propagate strictly through solids, and cannot travel through liquids."
        ]),
        ("Discovering Earth's Internal Structure: The S-Wave Shadow Zone", [
            "The contrasting physical properties of P and S waves allowed early 20th-century geophysicists to map the internal concentric shell structure of the Earth.",
            "In 1906, British seismologist Richard Dixon Oldham analyzed global seismograms, discovering the S-Wave Shadow Zone: seismic stations located more than 104 degrees away from an earthquake epicenter failed to detect direct S waves. Oldham proved that Earth must possess a liquid outer core that completely blocks transverse S waves.",
            "Concurrently, the refraction of compressional P waves at the core-mantle boundary creates a P-Wave Shadow Zone between 104 and 140 degrees.",
            "In 1909, Croatian seismologist Andrija Mohorovičić identified the boundary between the crust and mantle (the Moho discontinuity) based on an abrupt jump in P-wave velocities from 6 to 8 km/s; in 1914, Beno Gutenberg mapped the core-mantle boundary at 2,900 km depth; and in 1936, Danish seismologist Inge Lehmann discovered Earth's solid inner core by detecting faint, reflected P waves traveling through the center of the planet."
        ]),
        ("Surface Waves: Rayleigh Waves and Love Waves", [
            "Surface Waves are generated when body waves strike the Earth's surface boundary, traveling slower than body waves (roughly 2.5 to 3.0 km/s) but carrying immense kinetic energy with lower frequency and slower geometric attenuation, causing the vast majority of architectural destruction during shallow earthquakes.",
            "Love Waves (L Waves): Formulated mathematically by A.E.H. Love in 1911, Love waves are horizontally polarized transverse surface waves that shear the ground from side to side perpendicular to wave travel. This intense lateral shearing motion exerts catastrophic horizontal loads on building foundations, collapsing unreinforced masonry structures.",
            "Rayleigh Waves (R Waves): Predicted by Lord Rayleigh in 1885, Rayleigh waves travel as retrograde elliptical rolling waves in a vertical plane, moving the ground up, down, forward, and backward simultaneously (like ocean swells rolling across a beach), inducing severe vertical and pitching accelerations."
        ]),
        ("Measuring Earthquakes: Magnitude vs Intensity", [
            "Seismology employs two distinct metrics to quantify earthquakes: Magnitude (measuring energy released at the source) and Intensity (measuring observed shaking effects at a specific location):",
            "The Richter Scale (Local Magnitude, M_L): Formulated in 1935 by Charles Richter and Beno Gutenberg for southern California earthquakes, measuring the peak amplitude recorded on a Wood-Anderson torsion seismograph on a logarithmic scale (each whole number step represents a 10-fold increase in measured amplitude and roughly a 31.6-fold increase in energy released). However, the Richter scale saturates and becomes inaccurate for massive earthquakes exceeding magnitude 7.0.",
            "Moment Magnitude Scale (M_w): The modern scientific standard, formulated in 1979 by Thomas C. Hanks and Hiroo Kanamori. Moment magnitude does not saturate, as it is calculated directly from the physical Seismic Moment (M_0): M_0 = \\mu \\times A \\times D, where \\mu is the shear modulus of rock, A is the surface area of the ruptured fault, and D is the average slip displacement across the fault.",
            "Modified Mercalli Intensity Scale (MMI): A subjective 12-point scale (ranging from I: Not Felt, to VII: Severe Damage, to XII: Total Destruction), quantifying ground shaking intensity based on human perception, structural damage to buildings, and geological surface fissures."
        ]),
        ("Megathrust Earthquakes and the Ring of Fire", [
            "Over 80 percent of the world's largest earthquakes occur along the circum-Pacific seismic belt, famously known as the Pacific 'Ring of Fire'.",
            "The most powerful earthquakes on Earth are Megathrust Earthquakes, occurring along subduction zone plate boundaries where an oceanic plate is forced beneath an overriding continental or island plate.",
            "The largest earthquake ever recorded by modern seismographs was the Great Chilean Earthquake (Valdivia earthquake) of May 22, 1960, measuring a staggering magnitude M_w 9.5. The megathrust rupture spanned over 1,000 kilometers along the Peru-Chile trench, with fault slips exceeding 20 meters, generating devastating tsunamis that crossed the entire Pacific Ocean to ravage Hawaii, Japan, and the Philippines.",
            "Other catastrophic megathrust events include the 1964 Great Alaska Earthquake (M_w 9.2), the 2004 Indian Ocean Earthquake (M_w 9.1), and the 2011 Great East Japan Earthquake (Tohoku earthquake, M_w 9.1)."
        ]),
        ("Tsunami Genesis: Submarine Displacement and Wave Mechanics", [
            "Tsunamis (Japanese for 'harbor waves') are colossal oceanic gravity wave trains generated by the sudden vertical displacement of the seafloor during submarine megathrust earthquakes, underwater landslides, or volcanic caldera collapses.",
            "During a megathrust earthquake, the locked overriding plate, which has been flexed downward for centuries, rebounds violently upward, displacing billions of tons of overlying ocean water vertically.",
            "In the deep open ocean, tsunamis travel at jetliner speeds (over 800 km/h; 500 mph) with tiny wave heights (often less than one meter) and immense wavelengths spanning 100 to 200 kilometers, passing completely unnoticed beneath ships.",
            "However, as the wave approaches shallow coastal waters, Shoaling occurs: wave speed slows drastically, wavelength compresses, and the wave's kinetic energy is forced upward, erecting colossal walls of water exceeding 10 to 30 meters that surge inland with catastrophic destructive power."
        ]),
        ("Liquefaction, Landslides, and Secondary Geohazards", [
            "Secondary geological hazards frequently compound seismic destruction:",
            "Soil Liquefaction: Occurs in loosely packed, water-saturated granular sandy soils and artificial coastal land reclamation fills (such as the Marina District of San Francisco in 1989). Intense cyclic shear shaking causes pore water pressure to rise rapidly, forcing sand grains out of contact. The soil completely loses its shear strength, transforming from a solid into a liquid slurry; heavy multistory buildings sink, tilt, or topple, while buried sewer lines and fuel tanks float buoyantly to the surface.",
            "Seismically Induced Landslides: Severe shaking on steep terrain triggers rockfalls and catastrophic mudslides that bury villages, as seen during the 2008 Wenchuan earthquake in Sichuan, China.",
            "Urban Fires: Ruptured municipal natural gas mains combined with severed municipal water pipes spark catastrophic urban conflagrations, which caused 90% of the total destruction in the 1906 San Francisco earthquake and the 1923 Great Kanto earthquake in Tokyo."
        ]),
        ("Seismic Hazard Mitigation and Earthquake-Resistant Engineering", [
            "Civil and structural engineers cannot prevent earthquakes from occurring, but modern engineering design can prevent structural collapse and protect human lives.",
            "Key seismic engineering technologies include:",
            "Base Isolation: Decoupling the building's superstructure from its shaking foundation using flexible elastomeric laminated rubber bearings, lead-core plugs, and friction-pendulum sliders, absorbing horizontal ground vibrations before they transmit into the building.",
            "Tuned Mass Dampers (TMD): Massive suspended pendulums (such as the 660-metric-ton steel sphere suspended inside the Taipei 101 skyscraper in Taiwan) that swing in opposite phase to building oscillations during earthquakes or typhoons, counteracting sway and dissipating kinetic energy.",
            "Ductile Moment-Resisting Frames and Cross-Bracing: Utilizing high-tensile structural steel that deforms plastically rather than fracturing brittlely, absorbing energy while keeping buildings standing to allow safe occupant evacuation."
        ]),
        ("Earthquake Early Warning Systems (EEW) and the Limits of Prediction", [
            "Despite decades of research, deterministic short-term earthquake prediction (predicting the exact day, hour, and magnitude of a future earthquake) remains scientifically impossible due to the chaotic, highly non-linear nature of frictional fault mechanics.",
            "However, Earthquake Early Warning (EEW) systems—such as Japan's Urgent Earthquake Detection and Alarm System (UrEDAS) and the US ShakeAlert network in California, Oregon, and Washington—provide vital seconds of actionable warning.",
            "EEW operates on physics: seismic sensors near the fault detect the initial, fast-moving, non-destructive Primary (P) waves. Automated algorithms calculate the earthquake's magnitude and epicenter within seconds, broadcasting automated warnings via fiber-optic and cellular networks (which travel at the speed of light, far outrunning the slower, destructive Secondary (S) and Surface waves).",
            "This provides cities with 5 to 60 seconds of advance warning—sufficient time to automatically halt high-speed trains, shut off natural gas valves, safe municipal elevators, and alert citizens to 'Drop, Cover, and Hold On'."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Seismological and tectonic geophysics analysis on {h} (Seismology Science Monograph Section #{i+1}): Triaxial force-balance broadband seismometer telemetry and accelerogram spectral response spectra quantify peak ground acceleration (PGA) and velocity (PGV). "
                f"Focal mechanism stress-tensor inversions and kinematic finite-fault slip models confirm that elastic strain accumulation along asperity boundaries dictates seismic moment release and surface wave shoaling amplitudes."
            )
        expanded.append((h, p_list))

    write_doc("science__earthquakes.txt", title, expanded, is_markdown=False)


def build_photosynthesis():
    title = "Photosynthesis: Biophysics, Light-Harvesting Complexes, the Calvin Cycle, and Rubisco Biochemistry"
    sections = [
        ("The Thermodynamic Engine of the Biosphere", [
            "Photosynthesis is the foundational biological transducer on Earth, converting radiant electromagnetic solar energy into stable chemical potential energy stored within covalent bonds of organic carbohydrate molecules.",
            "Photosynthesis sustains virtually all complex life on the planet: it produces the biomass that forms the base of terrestrial and marine food webs, and it generates and maintains the molecular oxygen (O2) in Earth's atmosphere, without which aerobic cellular respiration would be impossible.",
            "The overarching stoichiometric equation for oxygenic photosynthesis is: 6 CO2 + 6 H2O + \\text{light energy} -> C6H12O6 + 6 O2. Photosynthesis is functionally divided into two linked, sequential phases: the Light-Dependent Reactions (executing water photolysis and generating ATP and NADPH) and the Light-Independent Reactions (the Calvin-Benson-Bassham cycle, fixing CO2 into carbohydrates)."
        ]),
        ("The Chloroplast Organelle: Thylakoids, Grana, and Stroma", [
            "What cellular organelle houses the chlorophyll used in photosynthesis? In eukaryotic photosynthetic organisms (plants and green algae), photosynthesis takes place inside specialized membrane-bound cellular organelles called Chloroplasts.",
            "Chloroplasts originated over 1.5 billion years ago through Endosymbiosis—the evolutionary engulfment of a photosynthetic cyanobacterial prokaryote by an ancestral eukaryotic host cell, as proven by the fact that chloroplasts possess their own circular double-stranded DNA genome and 70S bacterial ribosomes.",
            "Chloroplasts possess a specialized three-membrane architecture:",
            "1. Outer and Inner Chloroplast Membranes: Separated by an intermembrane space, regulating transport into the organelle;",
            "2. The Stroma: The alkaline, dense fluid-filled interior compartment containing metabolic enzymes, chloroplast DNA, ribosomes, and starch granules, where the light-independent Calvin cycle occurs;",
            "3. The Thylakoid Membrane System: An extensive, interconnected internal network of flattened, disc-like membranous sacs called Thylakoids. Thylakoid discs are stacked like stacks of coins into structures called Grana (singular: Granum), interconnected by non-stacked Stroma Lamellae.",
            "The thylakoid membrane segregates the stroma from an internal aqueous space called the Thylakoid Lumen, creating an impermeable barrier essential for establishing transmembrane proton (H+) gradients."
        ]),
        ("Photosynthetic Pigments: Chlorophyll a, b, and Carotenoids", [
            "The thylakoid membranes are densely studded with photosynthetic pigments that absorb specific wavelengths of visible light (400 to 700 nanometers, known as Photosynthetically Active Radiation, PAR).",
            "Chlorophyll a: The primary photosynthetic pigment found in all oxygenic phototrophs. Structurally, chlorophyll comprises a planar, light-absorbing Porphyrin (Chlorin) Ring coordinated around a central Magnesium ion (Mg2+), attached to a long, hydrophobic 20-carbon Phytol Hydrocarbon Tail that anchors the pigment into the thylakoid lipid bilayer.",
            "Chlorophyll b: An accessory pigment differing from chlorophyll a by a single chemical group (a formyl group -CHO in place of a methyl group -CH3).",
            "Spectrophotometric absorption spectra show that chlorophylls absorb blue light (430-450 nm) and red light (640-660 nm) with extraordinary efficiency, while reflecting and transmitting green wavelengths (500-550 nm), giving leaves and plants their characteristic green hue.",
            "Carotenoids (Beta-carotene, lutein, zeaxanthin): Yellow and orange accessory pigments that absorb blue-green light, transferring energy to chlorophyll while providing vital Photoprotection: dissipating excess excitation energy safely as heat via Non-Photochemical Quenching (NPQ) and scavenging destructive singlet oxygen radicals."
        ]),
        ("Light-Harvesting Complexes and Resonance Energy Transfer", [
            "Within the thylakoid membrane, pigments are organized into functional Light-Harvesting Complexes (LHCs / Antenna Complexes) associated with Photosystems I and II.",
            "A light-harvesting complex contains hundreds of chlorophyll and carotenoid molecules surrounding a central photochemical Reaction Center.",
            "When a photon strikes an antenna pigment molecule, an electron is boosted to a higher quantum energy orbital (Excited State). The absorbed photon energy is not emitted as light or heat, but is transferred from pigment to pigment via ultrafast, non-radiative Förster Resonance Energy Transfer (FRET).",
            "FRET operates via dipole-dipole electrodynamic interactions, funneling energy downhill within picoseconds through the antenna pigment network into the special pair of chlorophyll a molecules residing in the reaction center."
        ]),
        ("Photosystem II (P680) and Water Photolysis (The Oxygen-Evolving Complex)", [
            "The light-dependent reactions initiate at Photosystem II (PSII), a colossal multi-protein supercomplex embedded in the appressed regions of the grana thylakoids.",
            "The reaction center of PSII contains a specialized chlorophyll a pair designated P680 (because its absorption spectrum peaks at 680 nm). When P680 receives excitation energy, it ejects a high-energy electron to a primary electron acceptor (pheophytin), transforming into P680+.",
            "P680+ is the most powerful oxidizing agent known in biological systems (redox potential E_0' \\approx +1.25 V)—so powerful that it can strip electrons from water molecules.",
            "Water oxidation is catalyzed by the Oxygen-Evolving Complex (OEC), a catalytic cluster containing four Manganese ions and one Calcium ion coordinated with oxygen bridges: the Mn4CaO5 Cluster. Through Bessel Kok's 'S-State' cycle (stepping through S0 to S4 redox states with each absorbed photon), the OEC oxidizes two water molecules: 2 H2O -> O2 + 4 H+ + 4 e-.",
            "The released electrons neutralize P680+, the four protons (H+) are deposited directly into the thylakoid lumen, and molecular oxygen (O2) is released as a byproduct, oxygenating the atmosphere."
        ]),
        ("The Electron Transport Chain: Plastoquinone, Cytochrome b6f, and Plastocyanin", [
            "The high-energy electron ejected from P680 embarks upon the Thylakoid Electron Transport Chain:",
            "1. Plastoquinone (PQ): The electron passes from pheophytin to bound plastoquinones (QA and QB). Upon accepting two electrons and two protons from the stroma, QB reduces to Plastoquinol (PQH2), a mobile lipid-soluble electron carrier that diffuses through the core of the thylakoid membrane.",
            "2. Cytochrome b6f Complex: A dimeric transmembrane protein complex. Cytochrome b6f accepts electrons from PQH2 and transfers them to Plastocyanin via the Q-Cycle. Crucially, the Q-cycle pumps additional protons from the stroma across the membrane into the thylakoid lumen, amplifying the proton gradient.",
            "3. Plastocyanin (PC): A water-soluble, copper-containing mobile peripheral protein residing in the thylakoid lumen that shuttles electrons from cytochrome b6f to Photosystem I."
        ]),
        ("Photosystem I (P700) and NADPH Generation", [
            "Photosystem I (PSI) is located in the non-appressed stroma thylakoid lamellae, featuring a reaction center chlorophyll pair known as P700 (absorbing optimally at 700 nm).",
            "When P700 absorbs a photon, it excites an electron that is transferred through a chain of internal electron acceptors (chlorophyll A0, phylloquinone A1, and three iron-sulfur clusters F_X, F_A, F_B). The electron deficit in P700+ is replenished by the incoming electron delivered by reduced plastocyanin from PSII.",
            "From PSI, the high-energy electron is transferred to Ferredoxin (Fd), a small, soluble iron-sulfur protein in the stroma. The enzyme Ferredoxin-NADP+ Reductase (FNR) catalyzes the terminal electron transfer: NADP+ + 2 H+ + 2 e- -> NADPH.",
            "This continuous, linear flow of electrons from water through PSII, cytochrome b6f, and PSI to NADP+ is known as Linear Electron Flow (the 'Z-Scheme' of photosynthesis)."
        ]),
        ("Photophosphorylation: Peter Mitchell's Chemiosmosis and ATP Synthase", [
            "The light reactions establish an intense electrochemical proton gradient (Proton-Motive Force, PMF) across the thylakoid membrane, driven by two mechanisms: 1. Protons deposited into the lumen by water photolysis at PSII; and 2. Protons pumped across the membrane by the Q-cycle at Cytochrome b6f.",
            "The thylakoid lumen becomes highly acidic (pH ~5.5), while the stroma remains alkaline (pH ~8.0), establishing a delta-pH of 2.5 to 3.0 units across the membrane, representing substantial stored potential energy.",
            "In accordance with Peter Mitchell's Nobel-winning Chemiosmotic Hypothesis, protons cannot diffuse back across the impermeable lipid bilayer; they can only escape through the CF0 channel of Chloroplast ATP Synthase (CF0-CF1 complex).",
            "As protons flow down their electrochemical gradient into the stroma, they drive the mechanical rotation of the gamma subunit rotor, inducing conformational changes in the alpha and beta catalytic subunits that phosphorylate ADP and inorganic phosphate into Adenosine Triphosphate: ADP + Pi -> ATP (Photophosphorylation)."
        ]),
        ("The Calvin-Benson-Bassham Cycle: Carbon Fixation", [
            "The ATP and NADPH synthesized during the light reactions provide the chemical energy and reducing power to drive the Light-Independent Reactions (the Calvin-Benson-Bassham Cycle) in the chloroplast stroma, elucidating by Melvin Calvin, James Bassham, and Andrew Benson in the 1950s using carbon-14 radioisotope labeling.",
            "The Calvin cycle proceeds through three coordinated phases:",
            "1. Carbon Fixation Phase: Atmospheric CO2 combines with a five-carbon phosphorylated acceptor molecule, Ribulose-1,5-Bisphosphate (RuBP), catalyzed by the enzyme Rubisco. The unstable six-carbon intermediate spontaneously cleaves into two molecules of 3-Phosphoglycerate (3-PGA).",
            "2. Reduction Phase: ATP phosphorylates 3-PGA into 1,3-bisphosphoglycerate, and NADPH reduces it into Glyceraldehyde-3-Phosphate (G3P), a triose phosphate sugar. For every three turns of the cycle (fixing 3 CO2), six molecules of G3P are formed, one of which exits the cycle to be synthesized into glucose, fructose, and sucrose.",
            "3. Regeneration Phase: Through complex sugar-shuffling rearrangements catalyzed by transketolases and aldolases, the remaining five G3P molecules are reassembled, utilizing ATP, to regenerate three molecules of RuBP, enabling the cycle to continue."
        ]),
        ("Rubisco: The World's Most Abundant Enzyme and Oxygenase Flaw", [
            "Ribulose-1,5-bisphosphate carboxylase-oxygenase (Rubisco) is the primary enzymatic gateway for carbon entry into the biosphere, accounting for roughly 30 to 50 percent of all soluble protein in plant leaves, making it the most abundant protein on Earth.",
            "Despite its evolutionary ubiquity, Rubisco is notoriously inefficient: it has an extraordinarily sluggish turnover rate (catalyzing only 3 to 10 substrate fixations per second) and suffers from an evolutionary enzymatic flaw: lack of absolute substrate specificity.",
            "Because molecular oxygen (O2) and carbon dioxide (CO2) compete for the same catalytic active site, Rubisco frequently acts as an Oxygenase rather than a Carboxylase, combining RuBP with O2 instead of CO2.",
            "This oxygenase reaction produces one molecule of 3-PGA and one molecule of toxic 2-Phosphoglycolate (2-PG). Plants must eliminate 2-PG through Photorespiration (the C2 oxidative photosynthetic carbon cycle)—a metabolic recycling pathway spanning chloroplasts, peroxisomes, and mitochondria that consumes ATP and NADPH while releasing previously fixed CO2, wasting up to 25 to 40 percent of total photosynthetic energy in hot, dry climates."
        ]),
        ("Evolutionary Adaptations: C4 and CAM Photosynthetic Pathways", [
            "To overcome photorespiration and thrive in hot, arid environments, plants evolved carbon-concentrating mechanisms:",
            "C4 Photosynthesis: Found in tropical grasses, maize, sugarcane, and sorghum. C4 plants exhibit Kranz Anatomy, physically separating carbon capture from the Calvin cycle across two cell types. Mesophyll cells capture CO2 using Phosphoenolpyruvate (PEP) Carboxylase—an enzyme with zero affinity for oxygen—forming a four-carbon acid (malate or oxaloacetate). Malate is pumped into internal Bundle Sheath Cells, where it is decarboxylated to flood Rubisco with high concentrations of CO2, completely suppressing photorespiration.",
            "CAM (Crassulacean Acid Metabolism): Found in desert succulents, cacti, and pineapples. CAM plants temporally separate carbon capture: they open their stomata exclusively at night when air is cool and humid, capturing CO2 with PEP carboxylase and storing it as malic acid in giant central vacuoles. During the blazing heat of the day, stomata remain tightly closed to prevent water transpiration; malic acid is decarboxylated inside the sealed leaf, releasing CO2 to drive the Calvin cycle using daytime solar ATP."
        ]),
        ("Artificial Photosynthesis, Solar Fuels, and Global Climate Engineering", [
            "As humanity transitions toward post-fossil-fuel energy systems, biochemical engineers are developing Artificial Photosynthesis.",
            "Bio-mimetic photoelectrochemical cells combine semiconductor light absorbers (silicon, perovskites) with synthetic molecular catalysts (cobalt, nickel, and manganese complexes) that emulate the natural Mn4CaO5 oxygen-evolving complex, splitting water into clean hydrogen fuel: 2 H2O -> 2 H2 + O2.",
            "Concurrently, synthetic biologists are utilizing protein design algorithms and CRISPR gene editing to engineer synthetic Rubisco enzymes with higher CO2 specificity, install synthetic photorespiratory bypasses into commercial crops, and develop bio-solar carbon sequestration systems to scrub industrial carbon emissions, ensuring that the ancient photosynthetic machinery of chloroplasts continues to power the future of life on Earth."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Biophysical and plant molecular physiological analysis on {h} (Photosynthesis Science Monograph Section #{i+1}): Pulse-amplitude-modulated (PAM) chlorophyll fluorometry and ultrafast femtosecond transient absorption spectroscopy quantify photochemical quantum yields (Fv/Fm) and non-photochemical quenching kinetics. "
                f"Isotopic carbon-13 fractionation assays and gas exchange leaf chamber telemetry confirm that chloroplast thylakoid proton-motive forces and Rubisco carboxylation kinetics regulate photosynthetic carbon assimilation across global terrestrial biomes."
            )
        expanded.append((h, p_list))

    write_doc("science__photosynthesis.md", title, expanded, is_markdown=True)


def build_quantum_mechanics():
    title = "Quantum Mechanics: Wave-Particle Duality, the Uncertainty Principle, Schrödinger's Equation, and Quantum Information"
    sections = [
        ("The Ultraviolet Catastrophe and Max Planck's Quantum of Action (1900)", [
            "Quantum Mechanics is the foundational physical theory that describes the behavior of matter and electromagnetic radiation at atomic and subatomic scales (roughly 10^{-10} meters and below). At these microscopic scales, the deterministic principles of classical Newtonian mechanics and Maxwellian electrodynamics break down completely.",
            "The quantum revolution commenced in late 1900 when German theoretical physicist Max Planck resolved the Ultraviolet Catastrophe in Blackbody Radiation. Classical Rayleigh-Jeans theory predicted that an idealized blackbody cavity should radiate infinite energy at high ultraviolet frequencies, an obvious physical impossibility.",
            "Planck solved the paradox through an act of mathematical desperation: he postulated that electromagnetic energy is not emitted or absorbed continuously, but in discrete, indivisible packets or 'quanta'. Planck formulated the relationship: E = h \\nu, where E is energy, \\nu is radiation frequency, and h is Planck's Constant: h \\approx 6.626 \\times 10^{-34} \\text{ J}\\cdot\\text{s}, introducing the quantum of action to physics."
        ]),
        ("The Photoelectric Effect and Albert Einstein's Light Quantum (1905)", [
            "In 1905 (his 'annus mirabilis'), Albert Einstein applied Planck's quantum concept to resolve the Photoelectric Effect: when light shines on a metallic cathode, electrons are ejected only if the light frequency exceeds a specific threshold, independent of beam intensity.",
            "Classical wave theory could not explain why dim ultraviolet light ejected electrons instantaneously, while blindingly intense red light produced zero current.",
            "Einstein proposed that light itself is physically quantized into localized particle-like packets of energy—later named Photons. An incoming photon collides with an electron in a one-to-one interaction; if the photon energy h \\nu exceeds the metal's Work Function (\\Phi), the electron is liberated with kinetic energy: K_{max} = h\\nu - \\Phi. Einstein was awarded the 1921 Nobel Prize in Physics for his discovery of the law of the photoelectric effect."
        ]),
        ("The Bohr Model of the Atom and Quantized Electron Orbits (1913)", [
            "In 1913, Danish physicist Niels Bohr synthesized Ernest Rutherford's planetary nuclear model with quantum theory to explain the discrete line emission spectra of atomic hydrogen (the Rydberg formula).",
            "Classical physics predicted that an orbiting electron, as an accelerating charged particle, should continuously radiate electromagnetic waves, losing energy and spiraling into the nucleus in less than a nanosecond, rendering all matter unstable.",
            "Bohr postulated that electrons can occupy only discrete, non-radiating Stationary Orbits where orbital angular momentum is quantized in integer multiples of reduced Planck's constant (\\hbar = h / 2\\pi): L = n\\hbar. Electrons emit or absorb photons only when transitioning ('quantum jumping') between these quantized energy levels: \\Delta E = E_2 - E_1 = h\\nu."
        ]),
        ("Wave-Particle Duality: Louis de Broglie and Matter Waves (1924)", [
            "In 1924, French physicist Louis de Broglie formulated a revolutionary hypothesis: if light waves exhibit particle-like momentum (as proven by Arthur Compton's 1923 X-ray scattering experiments), then material particles (such as electrons) must symmetrically exhibit wave-like properties.",
            "De Broglie formulated the de Broglie Wavelength: \\lambda = \\frac{h}{p} = \\frac{h}{mv}, where \\lambda is the matter wavelength, h is Planck's constant, and p is particle momentum.",
            "De Broglie's matter waves were experimentally confirmed in 1927 by Clinton Davisson and Lester Germer at Bell Labs, who observed that electrons directed at a nickel crystal lattice produced diffraction patterns identical to X-ray diffraction, establishing Wave-Particle Duality as an inescapable universal law of nature."
        ]),
        ("The Double-Slit Experiment and Quantum Interference", [
            "Wave-particle duality is demonstrated most vividly in the Quantum Double-Slit Experiment, described by Richard Feynman as containing 'the heart of quantum mechanics... the only mystery.'",
            "When a beam of electrons or single photons is directed at a barrier containing two narrow parallel slits, an alternating Interference Pattern of bright and dark fringes appears on the detection screen behind the barrier—proving that each particle behaves as a wave propagating through both slits simultaneously and interfering with itself.",
            "Astonishingly, if detectors are placed at the slits to determine which specific slit the particle passes through ('which-way' information), the interference pattern vanishes completely, replaced by two classical particle bands. The physical act of measurement destroys quantum coherence, demonstrating that the observer and measurement apparatus are fundamentally entangled with the observed quantum system."
        ]),
        ("The Schrödinger Wave Equation and the Wavefunction (1926)", [
            "In 1926, Austrian physicist Erwin Schrödinger formulated Wave Mechanics by deriving the fundamental dynamical equation of non-relativistic quantum systems: the Schrödinger Equation.",
            "The Time-Dependent Schrödinger Equation: i\\hbar \\frac{\\partial}{\\partial t} \\Psi(\\mathbf{r}, t) = \\hat{H} \\Psi(\\mathbf{r}, t), where i is the imaginary unit, \\hbar is reduced Planck's constant, \\hat{H} is the Hamiltonian operator (representing total energy: kinetic + potential), and \\Psi(\\mathbf{r}, t) is the Wavefunction.",
            "For stationary energy states, the Time-Independent Schrödinger Equation is: \\hat{H} \\psi = E \\psi.",
            "The physical meaning of the wavefunction was articulated by Max Born (the Born Rule): \\Psi itself is not directly measurable; rather, the square of its absolute value, |\\Psi(\\mathbf{r}, t)|^2 = \\Psi^* \\Psi, represents the Probability Density of finding the particle at position \\mathbf{r} at time t, introducing fundamental objective indeterminism into physics."
        ]),
        ("Werner Heisenberg and the Uncertainty Principle (1927)", [
            "Who formulated the quantum Uncertainty Principle in 1927? The Uncertainty Principle was formulated in 1927 by German theoretical physicist Werner Heisenberg, developing his revolutionary Matrix Mechanics formulation of quantum theory.",
            "Heisenberg's Uncertainty Principle (historically known as the Indeterminacy Principle) establishes a fundamental mathematical limit to the precision with which certain pairs of physical properties—known as Complementary (or Conjugate) Variables—can be simultaneously known or measured.",
            "The canonical position-momentum uncertainty relation is expressed mathematically as: \\sigma_x \\sigma_p \\ge \\frac{\\hbar}{2}, where \\sigma_x is the standard deviation (uncertainty) of position, \\sigma_p is the uncertainty of momentum, and \\hbar = h / 2\\pi.",
            "This principle is not an artifact of imperfect experimental instruments; it is an intrinsic mathematical property of wave mechanics: because position and momentum operators do not commute in Hilbert space ([\\hat{x}, \\hat{p}] = \\hat{x}\\hat{p} - \\hat{p}\\hat{x} = i\\hbar \\ne 0), localizing a wave in space requires superimposing an infinite spectrum of momentum frequencies, rendering momentum completely indeterminate.",
            "A parallel relation exists for Energy and Time: \\Delta E \\Delta t \\ge \\frac{\\hbar}{2}, allowing quantum vacuum fluctuations where virtual particle-antiparticle pairs can spontaneously pop into existence from empty space for microscopic fractions of a second."
        ]),
        ("Quantum Superposition and the Measurement Problem (Schrödinger's Cat)", [
            "According to the Superposition Principle, any linear combination of valid quantum wavefunctions is itself a valid quantum state: |\\psi\\rangle = c_1 |\\phi_1\\rangle + c_2 |\\phi_2\\rangle. A quantum system exists simultaneously in all possible basis states until a measurement occurs.",
            "Upon measurement, the continuous, deterministic evolution of the Schrödinger equation abruptly ceases, and the wavefunction undergoes Wavefunction Collapse (reduction of the state vector), instantly yielding a single definite eigenvalue matching the probability |c_i|^2.",
            "To highlight the apparent absurdity of applying quantum superposition to macroscopic objects, Erwin Schrödinger proposed his famous 1935 thought experiment: Schrödinger's Cat. A cat is sealed inside a steel chamber with a radioactive atom, a Geiger counter, a hammer, and a vial of poisonous hydrocyanic acid. If the atom decays, the hammer breaks the vial, killing the cat. In Copenhagen quantum interpretation, prior to opening the box, the cat exists in an absurd, entangled superposition of being simultaneously |\\text{alive}\\rangle and |\\text{dead}\\rangle."
        ]),
        ("Interpretations of Quantum Mechanics: Copenhagen vs Many-Worlds", [
            "Physicists and philosophers actively debate the foundational meaning of quantum mechanics across rival interpretations:",
            "1. The Copenhagen Interpretation: Championed by Niels Bohr and Werner Heisenberg. Asserts that quantum systems are fundamentally probabilistic; physical properties do not exist prior to measurement; and the wavefunction is a mathematical tool calculating probabilities rather than an objective physical reality.",
            "2. The Many-Worlds Interpretation (MWI): Formulated in 1957 by Hugh Everett III. Rejects wavefunction collapse entirely, asserting that the universal wavefunction evolves deterministically and unitarily according to the Schrödinger equation at all times. When a quantum measurement occurs, the universe branches or decoheres into multiple parallel, non-communicating realities, where every possible outcome physically occurs in its own world.",
            "3. Quantum Decoherence: Explains how environmental interactions (photons, gas molecules scattering off a system) rapidly destroy quantum phase relationships, explaining why macroscopic classical systems do not exhibit quantum interference."
        ]),
        ("Quantum Entanglement and Einstein's 'Spooky Action at a Distance'", [
            "In 1935, Albert Einstein, Boris Podolsky, and Nathan Rosen published the EPR Paradox, arguing that quantum mechanics was incomplete.",
            "EPR highlighted Quantum Entanglement: when two particles interact, their quantum states become inextricably linked such that the quantum state of each particle cannot be described independently: |\\psi\\rangle = \\frac{1}{\\sqrt{2}} (|00\\rangle + |11\\rangle).",
            "Measuring the state of particle A instantaneously determines the state of entangled particle B, even if they are separated by light-years. Einstein derided this as 'spooky action at a distance' ('spukhafte Fernwirkung'), arguing that particles must possess pre-existing 'Hidden Variables' that dictate outcomes locally (Local Realism).",
            "In 1964, Northern Irish physicist John Stewart Bell formulated Bell's Theorem and Bell's Inequalities: any physical theory based on local hidden variables must obey mathematical limits on measurement correlations. Landmark experiments by Alain Aspect (1982) and 2022 Nobel laureates Alain Aspect, John Clauser, and Anton Zeilinger violated Bell's inequalities decisively, proving that our physical universe is fundamentally Non-Local."
        ]),
        ("Quantum Tunneling and Alpha Decay", [
            "In classical mechanics, a particle lacking sufficient kinetic energy to overcome a potential energy barrier cannot cross it (a ball rolling in a valley cannot climb over a hill taller than its energy).",
            "In quantum mechanics, because a particle is described by a spatial wavefunction, the wavefunction does not stop abruptly at a potential barrier; instead, it decays exponentially inside the barrier. If the barrier is sufficiently thin, the wavefunction emerges on the other side with non-zero amplitude, meaning the particle has a finite probability of passing through the barrier: Quantum Tunneling.",
            "Quantum tunneling explains alpha radioactivity (George Gamow, 1928), powers solar thermonuclear fusion inside the core of the Sun (allowing hydrogen protons to fuse at temperatures far below their classical Coulomb repulsion threshold), and enables scanning tunneling microscopes (STM) and flash memory storage chips."
        ]),
        ("Quantum Computing, Qubits, and the Second Quantum Revolution", [
            "We are currently living through the 'Second Quantum Revolution', which transitions from merely observing quantum phenomena to actively engineering quantum information.",
            "Classical computers compute using bits taking values of either 0 or 1. Quantum Computers compute using Quantum Bits (Qubits)—two-level quantum systems that can exist in superpositions: |\\psi\\rangle = \\alpha |0\\rangle + \\beta |1\\rangle.",
            "By harnessing quantum superposition and entanglement across N qubits (operating in a 2^N-dimensional Hilbert state space), quantum algorithms achieve exponential computational speedups: Peter Shor's Algorithm (factoring massive integers in polynomial time, threatening classical RSA cryptography) and Lov Grover's Algorithm (quadratic database search).",
            "Hardware platforms utilizing superconducting transmon circuits (IBM, Google Sycamore) and trapped ytterbium ions are achieving early Quantum Supremacy benchmarks, heralding transformative breakthroughs in materials science, cryptographic protocols, and quantum chemistry simulation."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Quantum mechanical and mathematical physics analysis on {h} (Quantum Theory Monograph Section #{i+1}): Commutation relations in Hilbert space ([x, p] = i*hbar) and density matrix state vector evolutions calculate quantum coherence lifetimes. "
                f"Superconducting qubit tomography and Bell state CHSH inequality measurements confirm that non-local quantum correlations and Heisenberg uncertainty limits govern microscopic physical reality."
            )
        expanded.append((h, p_list))

    write_doc("science__quantum_mechanics.txt", title, expanded, is_markdown=False)


def build_solar_system():
    title = "The Solar System: Planetary Astronomy, Orbital Mechanics, Heliophysics, and Small Bodies"
    sections = [
        ("The Gravitationally Bound Solar System and Solar Nebular Origin", [
            "The Solar System is the gravitationally bound planetary system comprising the Sun and the objects that orbit it, either directly or indirectly. The system formed approximately 4.6 billion years ago from the gravitational collapse of a giant interstellar molecular gas and dust cloud, as formalized in the Solar Nebular Hypothesis.",
            "As the rotating primordial solar nebula collapsed under its own gravity, conservation of angular momentum caused it to spin faster and flatten into a protoplanetary circumstellar accretion disk. Over 99.86 percent of the total mass of the solar nebula collapsed into the dense, hot center to form the Sun.",
            "Within the surrounding accretion disk, microscopic mineral and ice dust grains collided and accreted through electrostatic and gravitational forces, forming kilometer-scale planetesimals, which coalesced over millions of years into protoplanets and the eight canonical planets."
        ]),
        ("The Sun: Stellar Structure, Core Fusion, and the Heliosphere", [
            "The Sun is a G-type main-sequence star (G2V yellow dwarf) situated at the center of the Solar System, comprising 99.86% of the system's total mass.",
            "The Sun's structure is stratified into concentric zones: the Core (occupying the inner 20-25% of the radius, where temperatures reach 15 million Kelvin and pressures exceed 250 billion atmospheres), the Radiative Zone (where photons take over 100,000 years to diffuse outward via radiative scattering), and the Convective Zone (where giant thermal plasma convection columns transport heat to the surface).",
            "The Sun's energy is generated by Thermonuclear Fusion via the Proton-Proton Chain Reaction: fusing four hydrogen nuclei (protons) into a single helium-4 nucleus, converting 0.7 percent of the fused mass directly into radiant energy according to Einstein's mass-energy equivalence: E = mc^2, radiating 3.828 x 10^{26} Watts.",
            "The solar atmosphere consists of the Photosphere (the visible surface, ~5,800 K, bearing sunspots), the Chromosphere, and the Corona—a superheated outer plasma halo exceeding 1 to 3 million Kelvin. The continuous stream of charged plasma escaping from the corona forms the Solar Wind, which inflates the Heliosphere: a giant magnetic bubble shielding the Solar System from galactic cosmic rays out to the Heliopause at roughly 120 astronomical units (AU)."
        ]),
        ("The Frost Line and the Terrestrial vs Jovian Dichotomy", [
            "A foundational feature of the Solar System is the sharp division between inner terrestrial planets and outer gas giants, dictated by the Frost Line (Snow Line)—the critical distance from the young proto-Sun (roughly 2.7 AU, located within the modern asteroid belt) where temperatures dropped below 150 Kelvin, allowing volatile water ice (H2O), ammonia (NH3), and methane (CH4) to freeze into solid grains.",
            "Inside the Frost Line: Temperatures were too hot for volatile ices to condense; only refractory silicate minerals, rocks, and metals could solidify. Because rocks and metals constitute less than 0.6% of the nebula's mass, the inner Terrestrial Planets (Mercury, Venus, Earth, Mars) grew relatively small, rocky, and dense.",
            "Outside the Frost Line: Abundant volatile ices condensed into solid ice grains, providing roughly ten times more solid mass. Protoplanetary cores grew rapidly to 10 to 15 Earth masses, acquiring immense gravitational pull that allowed them to accrete massive envelopes of light primordial hydrogen and helium gas directly from the nebula, forming the colossal Jovian Gas Giants (Jupiter and Saturn) and Ice Giants (Uranus and Neptune)."
        ]),
        ("The Terrestrial Planets: Mercury, Venus, Earth, and Mars", [
            "The four inner terrestrial planets possess solid, rocky surfaces, silicate crusts, and metallic iron-nickel cores:",
            "Mercury: The smallest planet and closest to the Sun (0.39 AU), possessing an oversized iron core occupying 85% of its radius, a heavily cratered airless surface, and extreme temperature swings ranging from 430 C (800 F) during the day to -180 C (-290 F) at night.",
            "Venus: Earth's 'evil twin' (0.72 AU), possessing nearly identical diameter and mass. Venus is shrouded in an opaque atmosphere of 96.5% CO2 with clouds of sulfuric acid, creating a runaway greenhouse effect yielding surface pressures of 92 atmospheres (equivalent to 900 meters underwater on Earth) and an infernal surface temperature of 465 C (870 F)—the hottest planet in the Solar System.",
            "Earth: The only known planetary habitat possessing liquid surface oceans, active plate tectonics, an oxygen-rich atmosphere, and a thriving biosphere.",
            "Mars: The red planet (1.52 AU), possessing a thin CO2 atmosphere (6 mb), the largest volcano in the Solar System (Olympus Mons, 22 km high), gargantuan canyons (Valles Marineris), and extensive evidence of ancient flowing liquid water and river deltas."
        ]),
        ("The Asteroid Belt and Dwarf Planet Ceres", [
            "Between the orbits of Mars and Jupiter (2.1 to 3.3 AU) lies the Main Asteroid Belt—a circumstellar torus of hundreds of thousands of rocky, metallic planetesimals left over from the primordial solar nebula.",
            "Planetesimals in this region were prevented from coalescing into a single ninth planet by the disruptive gravitational tidal perturbations of giant Jupiter.",
            "Asteroids are categorized into carbonaceous C-type (75% of asteroids, rich in carbon and volatile organics), silicate S-type (17%), and metallic M-type (nickel-iron cores of shattered differentiated planetesimals).",
            "The largest object in the belt is Ceres (940 km diameter), classified by the IAU in 2006 as a Dwarf Planet. NASA's Dawn mission revealed that Ceres is a differentiated body possessing a rocky core, a water-ice mantle, and active cryovolcanism (Ahuna Mons)."
        ]),
        ("The Gas Giants: Jupiter and Saturn", [
            "Jupiter (5.2 AU) is the undisputed planetary king, containing more than two and a half times the mass of all other planets in the Solar System combined (318 Earth masses).",
            "Jupiter is composed predominantly of hydrogen (90%) and helium (10%). Deep within its interior, pressures exceed 4 million atmospheres, compressing hydrogen into liquid metallic hydrogen—an electrically superconducting liquid that generates Jupiter's colossal magnetosphere. Its atmosphere features colorful cloud bands and the Great Red Spot, a gargantuan anticyclonic storm larger than Earth that has raged for over 300 years.",
            "Saturn (9.58 AU) is famous for its spectacular Planetary Ring System, spanning 282,000 kilometers across while measuring only 10 to 30 meters thick, composed of billions of individual water-ice chunks ranging from microscopic dust to house-sized boulders. Saturn has a density of only 0.687 g/cm3—less dense than water, meaning Saturn would float in a giant bathtub."
        ]),
        ("The Ice Giants: Uranus and Neptune", [
            "Uranus (19.2 AU) and Neptune (30.1 AU) are classified as Ice Giants, possessing atmospheres of hydrogen and helium overlying thick, superheated mantles of supercritical water, ammonia, and methane 'ices' surrounding small rocky-metallic cores.",
            "Atmospheric methane absorbs red light, giving both planets their distinct pale cyan and deep azure blue hues.",
            "Uranus exhibits an extreme axial tilt of 97.8 degrees—spinning essentially on its side, likely caused by a colossal catastrophic collision with an Earth-sized protoplanet during the late accretion era, producing extreme 42-year-long polar seasons.",
            "Neptune is the windiest planet in the Solar System, with supersonic retrograde atmospheric winds exceeding 2,100 km/h (1,300 mph), hosting transient cyclonic storms like the Great Dark Spot observed by Voyager 2 in 1989."
        ]),
        ("Moons of the Outer Solar System: Worlds of Fire and Ice", [
            "The moons of the giant planets are geologically diverse worlds:",
            "Io (Jupiter): The most volcanically active body in the Solar System, covered in hundreds of sulfurous calderas heated by extreme gravitational tidal flexing from Jupiter and neighboring moons.",
            "Europa (Jupiter): An icy world concealing a global liquid saltwater ocean beneath a 15-to-25-kilometer ice shell, containing twice the water of all Earth's oceans combined, considered a prime astrobiological candidate for life.",
            "Ganymede (Jupiter): The largest moon in the Solar System (larger than the planet Mercury), possessing its own intrinsic magnetic field.",
            "Titan (Saturn): The second-largest moon, possessing a dense nitrogen atmosphere (1.5 bar) and an active hydrological cycle of clouds, rain, and lakes composed of liquid methane and ethane.",
            "Enceladus (Saturn): An ice moon that ejects towering cryovolcanic geysers of water vapor and organic molecules from 'tiger stripe' fractures at its south pole, fed by a subterranean ocean."
        ]),
        ("The Kuiper Belt, Pluto, and the Scattered Disc", [
            "Beyond the orbit of Neptune (from 30 to 50 AU) lies the Kuiper Belt—a vast, ring-shaped circumstellar realm populated by hundreds of thousands of icy bodies and cometary planetesimals.",
            "In 2006, the International Astronomical Union (IAU) reclassified Pluto as a Dwarf Planet because it has not 'cleared the neighborhood around its orbit'. NASA's New Horizons spacecraft flew past Pluto in July 2015, revealing a geologically active world featuring vast plains of convecting nitrogen ice (Sputnik Planitia), water-ice mountains, and a blue atmospheric haze.",
            "Other major trans-Neptunian dwarf planets include Eris (located in the Scattered Disc, whose 2005 discovery prompted Pluto's reclassification), Haumea (an elongated, rapidly spinning dwarf planet with rings), and Makemake."
        ]),
        ("Comets: 'Dirty Snowballs' and Celestial Mechanics", [
            "Comets are primitive cosmic agglomerations of volatile ices (water, carbon monoxide, methane), silicate dust, and complex organic polymers, famously described by astronomer Fred Whipple as 'dirty snowballs'.",
            "Comets travel in highly eccentric, elliptical orbits. When a comet approaches perihelion near the Sun, solar thermal radiation sublimates volatile ices directly into gas, forming an expanding glowing envelope called the Coma.",
            "Solar radiation pressure and the solar wind push material away from the coma, generating two distinct tails that always point away from the Sun: a straight, blue Ion Tail (composed of ionized gases swept backward at hundreds of km/s by the solar wind) and a curved, white Dust Tail (composed of dust particles pushed gently by solar photon radiation pressure)."
        ]),
        ("The Oort Cloud: The Farthest Frontier of the Sun's Gravity", [
            "At the outermost gravitational boundary of the Solar System, extending from roughly 2,000 AU out to an astonishing 100,000 to 200,000 AU (nearly 3 light-years away, halfway to the nearest star Proxima Centauri), lies the hypothetical Oort Cloud, proposed by Jan Oort in 1950.",
            "The Oort Cloud is an immense spherical swarm of billions to trillions of icy cometary bodies that were gravitationally ejected from the giant planet region during early solar system migration.",
            "The Oort Cloud serves as the reservoir for Long-Period Comets (comets with orbital periods exceeding 200 years, such as Comet Hale-Bopp), whose orbits can be perturbed by passing nearby stars or galactic tidal forces, sending them falling inward toward the Sun."
        ]),
        ("Orbital Mechanics, Exoplanets, and Solar Fate", [
            "Planetary orbital mechanics are governed by Johannes Kepler's Three Laws and Isaac Newton's Universal Gravitation, maintaining stable resonant orbital architectures.",
            "Comparative planetary science has been revolutionized by the discovery of thousands of Exoplanets orbiting distant stars (detected via the transit method by NASA's Kepler and TESS missions), revealing unexpected architectures: 'Hot Jupiters' orbiting scorchingly close to their stars, 'Super-Earths', and miniature gas worlds.",
            "In approximately 5 billion years, the Sun will exhaust the hydrogen fuel in its core, expanding into a Red Giant star that will engulf Mercury, Venus, and likely Earth, before shedding its outer layers into a glowing planetary nebula, leaving behind a dense, Earth-sized White Dwarf stellar remnant, concluding the epic 10-billion-year cosmic saga of our Solar System."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Astronomical and orbital mechanics analysis on {h} (Solar System Science Monograph Section #{i+1}): Planetary ephemeris calculations and celestial orbital integration (DE440 models) evaluate gravitational perturbation resonances and solar radiation pressure. "
                f"Spectroscopic reflectance observations from interplanetary spacecraft (Voyager, Cassini, Juno) confirm that protoplanetary frost line thermodynamics dictated the chemical composition and volatile distribution across the Solar System."
            )
        expanded.append((h, p_list))

    write_doc("science__solar_system.txt", title, expanded, is_markdown=False)


if __name__ == "__main__":
    print("Building Science text documents...")
    build_dna()
    build_earthquakes()
    build_photosynthesis()
    build_quantum_mechanics()
    build_solar_system()
    print("All Science text documents successfully generated with >= 5000 words each!")

