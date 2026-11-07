import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from backend.app.loaders import extractText

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

pdf_topics = [
    ("medicine__clinical_oncology_and_tumor_genetics.pdf", "Clinical Oncology, Somatic Tumor Genetics, and Precision Molecular Therapeutics", "oncology"),
    ("medicine__pulmonary_medicine_and_respiratory_mechanics.pdf", "Pulmonary Medicine, Respiratory Mechanics, and Critical Care Ventilation", "pulmonology"),
    ("medicine__gastroenterology_and_hepatobiliary_pathology.pdf", "Clinical Gastroenterology, Hepatobiliary Pathology, and Endoscopic Interventions", "gastroenterology"),
    ("medicine__infectious_disease_epidemiology_and_antimicrobials.pdf", "Infectious Disease Surveillance, Antimicrobial Resistance, and Nosocomial Pathogens", "infectious_disease"),
    ("engineering__electrical_power_grids_and_smart_distribution.pdf", "High-Voltage Electrical Power Systems, Synchronous Grids, and Smart Distribution", "electrical_engineering"),
    ("engineering__telecommunications_5g_and_mimo_antennas.pdf", "Telecommunications Engineering, Massive MIMO Antenna Arrays, and 5G Standards", "telecommunications"),
    ("engineering__biomedical_tissue_engineering_and_implants.pdf", "Biomedical Tissue Engineering, Biomaterial Scaffolds, and Orthopedic Implants", "biomedical_engineering"),
    ("engineering__materials_science_crystallography_and_alloys.pdf", "Materials Science, Metallurgical Crystallography, and Superalloy Microstructures", "materials_science"),
    ("engineering__environmental_wastewater_treatment_and_filtration.pdf", "Environmental Engineering, Advanced Wastewater Treatment, and Membrane Bioreactors", "environmental_engineering"),
    ("law__criminal_justice_procedure_and_constitutional_rights.pdf", "Criminal Justice Jurisprudence, Procedural Due Process, and Constitutional Rights", "criminal_law"),
    ("law__contract_doctrine_consideration_and_breach_remedies.pdf", "Contract Law Doctrines, Mutual Assent, Consideration, and Breach Remedies", "contract_law"),
    ("law__tort_liability_negligence_and_product_safety.pdf", "Tort Jurisprudence, Strict Liability, Negligence Standards, and Product Safety", "tort_law"),
    ("law__environmental_statutes_clean_air_and_water_acts.pdf", "Environmental Statutory Frameworks, Clean Air, and Water Resource Regulation", "environmental_law"),
    ("law__administrative_rulemaking_and_agency_deference.pdf", "Administrative Law, Notice-and-Comment Rulemaking, and Judicial Deference Doctrines", "administrative_law"),
    ("arts__sculpture_bronze_casting_and_marble_carving.pdf", "History of Sculpture, Lost-Wax Bronze Casting, and Classical Marble Carving", "sculpture"),
    ("arts__photography_optics_exposure_and_chemical_emulsions.pdf", "Photographic Science, Optical Lens Aberrations, Exposure, and Silver Halide Emulsions", "photography"),
    ("arts__theater_dramaturgy_stanislavski_method_and_staging.pdf", "Dramatic Arts, Theatrical Dramaturgy, Stanislavski Acting System, and Stagecraft", "theater"),
    ("arts__traditional_printmaking_woodcut_and_intaglio.pdf", "Printmaking Traditions, Relief Woodcut Engraving, Intaglio Etching, and Lithography", "printmaking"),
    ("arts__dance_choreography_spatial_geometry_and_kinesiology.pdf", "Choreographic Theory, Spatial Geometry, Laban Movement Analysis, and Dance Kinesiology", "dance"),
    ("sports__biomechanics_of_swimming_stroke_hydrodynamics.pdf", "Swimming Biomechanics, Hydrodynamic Wave Drag, and Propulsion Stroke Efficiency", "swimming_science"),
    ("sports__track_and_field_sprinting_mechanics_and_acceleration.pdf", "Track and Field Sprinting Mechanics, Horizontal Force Vector Acceleration, and Cadence", "sprint_biomechanics"),
    ("sports__combat_sports_concussion_biomechanics_and_recovery.pdf", "Combat Sports Medicine, Rotational Head Acceleration, and Concussion Management", "combat_sports"),
    ("sports__endurance_altitude_training_and_erythropoiesis.pdf", "Endurance Sports Physiology, Hypoxic Altitude Acclimatization, and Erythropoiesis", "endurance_physiology"),
    ("environment__coastal_geomorphology_barrier_islands_and_erosion.pdf", "Coastal Geomorphology, Barrier Island Migration Dynamics, and Shoreline Retreat", "coastal_geology"),
    ("environment__arctic_permafrost_thawing_and_methane_release.pdf", "Cryospheric Science, Arctic Permafrost Thawing Dynamics, and Methane Clathrate Release", "cryosphere_science"),
]

def generate_pdf_doc(filename, title, category):
    path = DATA_DIR / filename
    doc = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40,
        title=title
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        spaceAfter=15,
        textColor=colors.HexColor('#1a365d')
    )
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        spaceAfter=10,
        textColor=colors.HexColor('#2b6cb0')
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        spaceAfter=8
    )

    story = []
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 15))
    
    chapters = [
        f"Fundamental Axiomatic Principles and Theoretical Architecture of {category.replace('_', ' ').title()}",
        f"Empirical Research Protocols, Experimental Instrumentation, and Quantitative Telemetry",
        f"Historical Evolution, Scientific Milestones, and Epistemological Paradigm Shifts",
        f"Analytical Mathematical Formulations, Differential Equations, and Kinetic Modeling",
        f"Structural Failure Modes, Vulnerability Trajectories, and Degradation Mechanisms",
        f"Comparative International Benchmarks, Standardized Operating Procedures, and Quality Control",
        f"Interdisciplinary Synergies, Cross-Disciplinary Integration, and Environmental Coupling",
        f"Systemic Risk Management, Prospective Hazard Identification, and Redundancy Architecture",
        f"Technological Tooling, Digital Simulation Infrastructure, and Algorithmic Analytics",
        f"Statutory Governance, Ethical Oversight, Compliance Protocols, and Legal Standards",
        f"Longitudinal Case Studies, Retrospective Cohort Analysis, and Empirical Field Data",
        f"Future Translational Frontiers, Emerging Innovations, and Transformative Horizons"
    ]
    
    for ch_idx, ch_title in enumerate(chapters):
        story.append(Paragraph(f"Chapter {ch_idx + 1}: {ch_title}", heading_style))
        story.append(Spacer(1, 6))
        
        p1 = (
            f"The exploration of {ch_title.lower()} constitutes a foundational pillar in the modern discipline of "
            f"{category.replace('_', ' ')}. Contemporary researchers and practitioners operate within a rigorous "
            f"paradigm demanding precise quantification, empirical reproducibility, and robust theoretical grounding. "
            f"Historical investigations established the conceptual baselines upon which subsequent generations have expanded, "
            f"progressively refining diagnostic methodologies, structural tolerances, and dynamic response kinetics "
            f"across diverse operating environments."
        )
        story.append(Paragraph(p1, body_style))
        
        p2 = (
            f"Furthermore, systematic field observations and laboratory trials substantiate the critical importance of "
            f"maintaining strict control standards when implementing {category.replace('_', ' ')} protocols. "
            f"Multivariate statistical analysis reveals that minor deviations in baseline parameters can induce "
            f"non-linear propagation cascades, underscoring the absolute necessity of integrating redundant monitoring arrays "
            f"and continuous feedback control mechanisms into enterprise operational designs."
        )
        story.append(Paragraph(p2, body_style))
        
        # Add 6 comprehensive annotation paragraphs per chapter to ensure >= 5,000 words extracted
        for ann_idx in range(6):
            ann = (
                f"[{category.upper()}] Comprehensive scholarly annotation on {ch_title} (Section #{ann_idx+1} of 6): "
                f"This extended analytical commentary examines granular sub-components of {ch_title.lower()}, "
                f"evaluating sensitivity thresholds, empirical cross-validation metrics, environmental boundary conditions, "
                f"and operational mitigation strategies. Practitioners must ensure continuous compliance with certified "
                f"governance frameworks, ensuring that safety margins and high-fidelity standards remain uncompromised "
                f"throughout the operational lifecycle of the system within {category.replace('_', ' ')}."
            )
            story.append(Paragraph(ann, body_style))
            
        story.append(Spacer(1, 10))
        
    doc.build(story)
    text = extractText(path)
    wc = len(text.split())
    print(f"[{filename}] PDF generated: {len(chapters)} chapters. Extracted words: {wc}")
    assert wc >= 5000, f"Expected >= 5000 words, got {wc}"

def main():
    print("=" * 60)
    print("GENERATING 25 PDF DOCUMENTS (25 PDF)")
    print("=" * 60)
    for filename, title, category in pdf_topics:
        generate_pdf_doc(filename, title, category)
    print("\nAll 25 PDF documents generated successfully with >= 5,000 words!")

if __name__ == "__main__":
    main()

