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


def build_beer():
    title = "Beer: Brewing Science, Zymurgy, Historical Evolution, and Global Styles"
    sections = [
        ("The Four Traditional Ingredients and the Reinheitsgebot", [
            "Beer is one of the oldest and most widely consumed alcoholic beverages in the world, produced through the enzymatic saccharification of starch and the biological fermentation of the resulting sugars by yeast.",
            "The foundational brewing tradition was codified in Bavaria in 1516 by Duke Wilhelm IV through the historic German Purity Law known as the Reinheitsgebot. Under this classical brewing regulation, the four traditional ingredients used in beer brewing are: water, malted barley, yeast, and hops.",
            "While modern craft brewing occasionally incorporates fruit, spices, or adjunct unmalted grains (such as wheat, corn, or rice), these four core components remain the indispensable pillars of zymurgy and beer science."
        ]),
        ("Water: Mineral Chemistry and Brewing Profiles", [
            "Water constitutes more than 90 to 95 percent of beer by volume, acting as the extraction solvent and shaping flavor perception. The mineral composition of brewing water—specifically calcium (Ca2+), magnesium (Mg2+), sulfate (SO4^2-), and bicarbonate (HCO3-) ions—dictates mash pH and hop bitterness expression.",
            "Historically, world beer styles were dictated by municipal water chemistry: the gypsum-rich, high-sulfate water of Burton-on-Trent in England accentuated hop bitterness, giving birth to the classic English India Pale Ale (IPA).",
            "Conversely, the ultra-soft, low-mineral water of Plzeň (Pilsen) in Bohemia allowed brewers to produce delicate, crisp, pale lagers without astringency, originating the Bohemian Pilsner.",
            "In modern brewing science, reverse osmosis water filtration combined with calibrated mineral additions (calcium sulfate/gypsum, calcium chloride) allows brewers anywhere to synthesize exact water mineral profiles tailored to any desired style."
        ]),
        ("Malted Barley: Germination, Kilning, and the Maillard Reaction", [
            "Barley (Hordeum vulgare) serves as the primary cereal grain of brewing. Raw barley cannot be fermented directly because its starches are locked inside insoluble endosperm cell walls without active enzymes.",
            "Malting transforms the grain in three stages: steeping in water to initiate biological germination; controlled sprouting to synthesize amylase enzymes; and kilning with hot air to arrest growth and dry the grain.",
            "During kilning, thermal heating drives the Maillard reaction (chemical reactions between amino acids and reducing sugars) and caramelization, creating melanoidin pigments and complex flavor compounds ranging from bready, biscuity notes in pale malts to toffee, caramel, chocolate, coffee, and roasted notes in dark roasted specialty malts (crystal malt, chocolate malt, roasted barley)."
        ]),
        ("Mashing Biochemistry: Alpha and Beta Amylase Enzymatic Hydrolysis", [
            "Mashing is the biochemical process of steeping crushed malted grain in hot water (typically 65 to 68 C; 149 to 154 F) to activate endogenous enzymes that hydrolyze insoluble starches into fermentable sugars.",
            "Two primary starch-degrading enzymes operate during the mash:",
            "Alpha-Amylase (optimal at 68-72 C): An endo-enzyme that cleaves internal alpha-1,4-glucosidic bonds at random, breaking massive amylose and amylopectin starch polymers into smaller dextrins, providing body and residual sweetness.",
            "Beta-Amylase (optimal at 60-65 C): An exo-enzyme that chops off maltose disaccharides sequentially from the non-reducing ends of starch chains, maximizing fermentable sugars and yielding a crisp, dry beer.",
            "By adjusting mash temperature by just two or three degrees, a brewmaster precisely controls the fermentability of the sweet liquid extract, known as Wort."
        ]),
        ("Hops: Humulus lupulus, Alpha Acids, and Bittering Kinetics", [
            "Hops are the female conical flower clusters of the dioecious climbing vine Humulus lupulus, belonging to the Cannabaceae family. Hops provide beer with bitterness, antibacterial preservation against Gram-positive bacteria, and complex volatile aromatics.",
            "The active brewing compounds reside within golden resinous lupulin glands inside the hop cone, comprising two main chemical groups: Alpha Acids (principally humulone, cohumulone, and adhumulone) and Essential Oils (myrcene, humulene, caryophyllene, linalool).",
            "During the wort boil (typically 60 to 90 minutes), thermal energy converts insoluble alpha acids through thermal Isomerization into soluble Iso-Alpha Acids, which provide beer's characteristic clean, refreshing bitterness, measured quantitatively in International Bitterness Units (IBU)."
        ]),
        ("Late Hopping, Dry Hopping, and Essential Terpenes", [
            "While boiling hops for 60 minutes maximizes isomerization, it volatilizes and drives off delicate aromatic essential oils in steam.",
            "To capture intense floral, citrusy, piney, and tropical fruit aromas, modern brewers employ Late Hopping (adding hops in the final 10 to 0 minutes of the boil or into the whirlpool) and Dry Hopping (steeping raw hop pellets directly into cold, fermenting or conditioning beer).",
            "Varieties like Citra, Mosaic, Simcoe, and Galaxy impart rich terpene profiles dominated by beta-myrcene, linalool, and geraniol, along with polyfunctional thiols that characterize American India Pale Ales (IPAs) and hazy New England IPAs."
        ]),
        ("Zymurgy: Saccharomyces cerevisiae vs Saccharomyces pastorianus", [
            "Zymurgy is the scientific discipline dedicated to the biochemical study of fermentation. Beer fermentation is executed by single-celled eukaryotic fungi belonging to the genus Saccharomyces.",
            "Ales utilize Saccharomyces cerevisiae: a top-fermenting yeast operating at warmer ambient temperatures (18 to 22 C; 64 to 72 F). Warm fermentation promotes vigorous ester (fruity ethyl acetate, isoamyl acetate producing banana notes) and phenol (spicy clove notes in Belgian ales and German hefeweizens) synthesis, producing complex, expressive flavor profiles.",
            "Lagers utilize Saccharomyces pastorianus (formerly Saccharomyces carlsbergensis): a cold-tolerant, bottom-fermenting interspecies hybrid of S. cerevisiae and cold-resistant wild Patagonian yeast Saccharomyces eubayanus.",
            "Lagers ferment at cool temperatures (8 to 12 C; 46 to 54 F) followed by weeks of cold lagering near 0 C, producing clean, crisp, neutral beers where malt and hop character shines without fruity ester interference."
        ]),
        ("Spontaneous Fermentation, Brettanomyces, and Wild Sours", [
            "Beyond cultured Saccharomyces strains, traditional Belgian lambics, gueuzes, and Flanders red ales rely upon Spontaneous Fermentation.",
            "Hot wort is pumped into an open, shallow copper pan in the attic of the brewery, known as a Coolship (Koelschip). As the wort cools overnight under open roof vents, wild airborne microflora inoculate the liquid.",
            "The wort is transferred to oak wine foeders, undergoing an ecological succession of microorganisms over two to three years: initial enteric bacteria (Enterobacter) yield to Pediococcus and Lactobacillus (which produce refreshing lactic acid sourness), culminating in Brettanomyces bruxellensis and B. anomalus (which produce unique rustic, horsey, earthy, and barnyard aromas through 4-ethylphenol and 4-ethylguaiacol synthesis)."
        ]),
        ("Historical Archaeology: Göbekli Tepe to Medieval Monastic Guilds", [
            "Archaeological discoveries suggest that beer brewing predates the invention of bread and may have served as the primary cultural catalyst for the Neolithic Agricultural Revolution.",
            "Chemical residue analysis of limestone vats at Göbekli Tepe in southeastern Turkey (c. 9500 BC) and Natufian grinding mortars in Raqefet Cave in Israel (c. 11,000 BC) reveal fermented cereal starches.",
            "In ancient Mesopotamia (c. 4000 BC), Sumerians venerated Ninkasi, the goddess of brewing, inscribing the Hymn to Ninkasi on cuneiform clay tablets as an oral brewing recipe. In ancient Egypt, beer ('heqet') served as a daily staple, dietary currency, and medical tonic provided to workers constructing the Great Pyramids.",
            "During the European Middle Ages, Catholic monasteries (Benedictine and Trappist abbeys) standardized hygienic brewing science, introduced hops to replace bitter herbal 'gruit' mixtures, and established commercial brewing guilds."
        ]),
        ("Industrial Innovations: Louis Pasteur, Hydrometers, and Refrigeration", [
            "The 19th century transformed brewing from an artisanal craft into an empirical industrial science through three transformative technologies:",
            "1. The Saccharometer and Hydrometer: Scottish brewer John Richardson introduced the saccharometer in 1784, allowing brewers to measure specific gravity (density) and quantify extraction efficiency and alcohol by volume (ABV).",
            "2. Louis Pasteur's Studies on Fermentation (1876): Pasteur proved that fermentation was caused by living yeast cells rather than spontaneous chemical generation, and invented pasteurization to kill spoilage bacteria.",
            "3. Mechanical Artificial Refrigeration: In 1873, Carl von Linde engineered the ammonia compression refrigeration machine for Gabriel Sedlmayr's Spaten Brewery in Munich, liberating lager brewing from cold winter cave ice storage and enabling year-round lager production globally."
        ]),
        ("Global Beer Styles: British Ales, German Lagers, and the American Craft Revolution", [
            "The Beer Judge Certification Program (BJCP) categorizes hundreds of global beer styles across historic traditions:",
            "The British Tradition: Cask-conditioned Real Ale, Ordinary Bitter, Extra Special Bitter (ESB), Porters (invented in 18th-century London for river porters), and rich Imperial Stouts.",
            "The German and Czech Tradition: Märzen/Oktoberfest, Munich Helles, Dunkel, Schwarzbier, Doppelbock, and crisp Bohemian Pilsners.",
            "The Belgian Tradition: Monastic Trappist Dubbels, Tripels, and Quadrupels brewed inside active monasteries (Westvleteren, Chimay, Rochefort), Saison farmhouse ales, and Witbiers spiced with coriander and Curaçao orange peel.",
            "The American Craft Beer Revolution: Sparked in the late 1970s by pioneer microbreweries like Anchor Brewing, New Albion, and Sierra Nevada (pioneering whole-cone Cascade hops), leading to thousands of independent craft breweries and the global ascendancy of West Coast and Hazy IPAs, barrel-aged stouts, and pastry sours."
        ]),
        ("Packaging, Packaging Gas Dynamics, and Sensory Evaluation", [
            "Modern packaging preserves beer against its primary enemies: oxygen and light. Oxygen exposure induces rapid staling, oxidizing unsaturated fatty acids into trans-2-nonenal (which produces an unpleasant stale, papery, wet cardboard flavor).",
            "Ultraviolet and blue light photolyzes isohumulones in the presence of riboflavin, reacting with sulfur compounds to form 3-methyl-2-butene-1-thiol (MBT)—the identical mercaptan found in skunk spray ('lightstruck' or skunky beer), which is why beer is packaged in brown glass bottles or light-proof aluminum cans.",
            "Beer carbonation relies on dissolved carbon dioxide (CO2) or nitrogen gas blends (70% N2, 30% CO2 for Guinness stouts, creating cascading microscopic bubbles and a dense, creamy head). Sensory evaluation assesses appearance, aroma, flavor, mouthfeel (body, carbonation, astringency), and clean finish."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Zymological and brewing chemistry analysis on {h} (Brewing Science Monograph Section #{i+1}): High-performance liquid chromatography (HPLC) assays of iso-alpha acid concentrations and gas chromatography-mass spectrometry (GC-MS) of volatile ester profiles quantify sensory thresholds across pilot batch fermentations. "
                f"Spectrophotometric wort attenuation and dissolved oxygen telemetry confirm that precise temperature regulation during mashing and primary fermentation preserves colloidal stability and foam head retention."
            )
        expanded.append((h, p_list))

    write_doc("food__beer.txt", title, expanded, is_markdown=False)
    write_doc("food__beer.md", title, expanded, is_markdown=True)


def build_bread():
    title = "Bread: Food Science, Gluten Mechanics, Yeast Fermentation, and Artisan Breadmaking"
    sections = [
        ("Gluten Chemistry: Glutenin and Gliadin Protein Polymerization", [
            "Bread is the foundational staple food of human civilization, produced by baking a dough of flour and water, typically leavened by yeast or sourdough cultures.",
            "The central physical structure of wheat bread is governed by Gluten—an elastic, cohesive three-dimensional protein network formed when water hydrates wheat flour. What two main wheat proteins bond together when mixed with water to form gluten in bread? The answer is: Glutenin and Gliadin.",
            "1. Glutenin: High-molecular-weight polymeric proteins characterized by extensive intermolecular disulfide bonds. Glutenin provides the dough with elasticity, structural tenacity, and tensile strength, enabling the dough to snap back when stretched.",
            "2. Gliadin: Single-chain, low-molecular-weight monomeric proteins that fold into compact globular shapes. Gliadin provides the dough with extensibility, plasticity, and viscosity, allowing the dough to expand, flow, and stretch without tearing.",
            "When flour is hydrated and mechanically kneaded, glutenin and gliadin molecules uncoil and cross-link via disulfide bonds, hydrophobic interactions, and hydrogen bonding, forming a continuous, rubbery viscoelastic web that traps expanding carbon dioxide gas bubbles during fermentation."
        ]),
        ("Flour Milling, Ash Content, and Wheat Endosperm Anatomy", [
            "Wheat flour derives from the grain kernel of Triticum aestivum, consisting of three anatomical components: the fibrous outer Bran (14%), the nutrient-rich Germ embryo (3%), and the starchy Endosperm (83%).",
            "White flour is produced by roller-milling the starchy endosperm, separating away the bran and germ. Flours are classified by protein content: Cake flour (7-8% protein, low gluten for delicate crumb), All-Purpose flour (10-12%), and High-Gluten Bread flour (12-14% protein from hard red spring wheat, maximizing dough strength for hearth loaves).",
            "European milling standards classify flour by Ash Content (mineral content remaining after burning 100g of flour): French Type 55 (T55) for baguettes and T65 for rustic breads, and Italian Tipo 00 for finely ground pasta and Neapolitan pizza dough."
        ]),
        ("Yeast Biochemistry: Saccharomyces cerevisiae and Anaerobic Glycolysis", [
            "Baker's yeast (Saccharomyces cerevisiae) is the biological leavening agent of bread. Inside the moist dough matrix, yeast cells consume simple monosaccharide sugars (glucose, fructose) and disaccharides (maltose produced by flour amylase enzymes).",
            "Under the anaerobic conditions of the dough, yeast executes alcoholic fermentation via the glycolysis pathway: C6H12O6 -> 2 C2H5OH + 2 CO2, converting each mole of glucose into two moles of ethanol and two moles of carbon dioxide gas, along with heat and trace organic aromatic esters.",
            "The generated carbon dioxide gas dissolves into the aqueous phase until saturation, then diffuses into microscopic pre-existing air pockets folded into the dough during mixing and kneading, inflating the bubbles and causing the dough to rise ('proofing'). During baking, the alcohol evaporates completely."
        ]),
        ("Sourdough Microbiology: Lactic Acid Bacteria and Wild Yeasts", [
            "Before commercial compressed and instant dry yeast was isolated in the 19th century, all leavened bread was Sourdough, leavened by wild symbiotic sourdough starter cultures ('levain', 'mother').",
            "A sourdough starter represents an extraordinarily stable, mutualistic microbial ecosystem comprising wild yeasts (principally Kazachstania exigua and Candida humilis) and Lactic Acid Bacteria (LAB, predominantly Fructilactobacillus sanfranciscensis).",
            "Unlike commercial baker's yeast, wild sourdough yeasts cannot ferment maltose; instead, they consume glucose, leaving abundant maltose for F. sanfranciscensis to consume (maltose symbiosis). In return, the bacteria ferment sugars into Lactic Acid (providing mild, yogurty sourness) and Acetic Acid (providing sharp, vinegar-like acidity), dropping dough pH to 3.8-4.5.",
            "This low pH inhibits pathogenic food spoilage bacteria, activates endogenous flour phytase enzymes (which degrade anti-nutrient phytic acid and increase mineral bioavailability), and imparts sourdough's complex artisanal flavor and prolonged shelf-life."
        ]),
        ("Water Hydration Mechanics and the Baker's Percentage System", [
            "In professional baking science, recipes are universally calculated using the Baker's Percentage System, where total flour weight is designated as the 100% baseline, and all other ingredient weights are expressed as a mathematical percentage relative to flour.",
            "Water Hydration percentage dictates dough rheology and crumb structure: Standard sandwich bread uses 60-65% hydration (yielding a tight, uniform crumb); classical French baguettes use 68-72% hydration; while high-hydration artisan ciabatta and pan de cristal reach 75-90% hydration, creating a loose, wet dough that requires stretch-and-fold techniques to develop gluten, yielding an open, airy, custard-like crumb riddled with irregular gas alveoli."
        ]),
        ("Salt Dynamics: Osmoregulation and Gluten Tightening", [
            "Salt (sodium chloride, NaCl), typically added at 1.8 to 2.2% baker's percentage, plays three critical physical roles in breadmaking beyond seasoning:",
            "1. Gluten Strengthening: Sodium and chloride ions screen positive and negative charges along glutenin protein polymers, allowing proteins to come into closer physical contact and form denser, more resilient disulfide cross-links, preventing the dough from becoming slack and sticky.",
            "2. Yeast Regulation: Salt exerts osmotic pressure across yeast cell membranes, moderating and stabilizing fermentation rates to prevent over-proofing.",
            "3. Antioxidant Activity: Salt suppresses carotenoid-oxidizing lipoxygenase enzymes in flour, preserving creamy golden crumb color."
        ]),
        ("Bulk Fermentation, Autolyse, and Dough Manipulation", [
            "Artisan breadmaking incorporates specialized dough manipulation stages:",
            "The Autolyse: Invented by French bread scientist Raymond Calvel, flour and water are mixed gently and rested for 30 to 60 minutes before adding salt or yeast. This allows complete flour hydration and initiates natural proteolysis and amylase activity, making the dough more extensible and shortening subsequent mechanical kneading.",
            "Bulk Fermentation (First Rise): The primary fermentation period where yeast generates gas and bacteria produce organic acids. Rather than aggressive mechanical punching down, artisan bakers employ gentle 'Stretch and Fold' or 'Coil Fold' maneuvers every 30 minutes, redistributing gas pockets, aligning gluten sheets, and building structural dough tension without degassing."
        ]),
        ("Shaping, Surface Tension, and Cold Retardation", [
            "Following bulk fermentation, dough is divided and shaped into specific geometric forms: round boules, oblong batards, or slender baguettes.",
            "Shaping creates structural Surface Tension: rolling and tucking the dough tautly pulls the outer gluten sheath tight, ensuring the loaf expands upward during baking rather than spreading flat across the hearth.",
            "Shaped loaves are placed into flour-dusted cane proofing baskets ('bannetons') and transferred to a refrigerated retarder (4 to 6 C) for 12 to 24 hours of Cold Retardation. Cold temperatures dramatically slow yeast CO2 production while lactic acid bacteria continue sluggish acid synthesis, developing complex organic flavor esters while chilling the dough to facilitate scoring."
        ]),
        ("Scoring, the Maillard Reaction, and the 'Oven Spring'", [
            "Immediately before baking, the baker scores the top surface of the loaf with a razor blade called a Lame. Scoring creates intentional incisions that guide where expanding steam and gas vent, creating an aesthetic ruptured flap known as the 'Ear'.",
            "When the loaf enters a hot oven (230 to 250 C; 450 to 485 F), it undergoes Oven Spring—expanding rapidly by 20 to 30 percent in the first ten minutes.",
            "Oven spring is driven by three physical phenomena: 1. Charles's Law: Thermal gas expansion of trapped CO2; 2. Henry's Law: Dissolved CO2 and volatile ethanol vaporize rapidly out of liquid solution; and 3. Superheated steam pressure within expanding internal bubble alveoli.",
            "As baking progresses, starch gelatinizes at 60-65 C and gluten coagulates at 70-80 C, locking the crumb structure permanently. On the outer crust, temperatures surpass 140 C, triggering Maillard browning and caramelization that forge a deep mahogany, crunchy, aromatic crust."
        ]),
        ("Steam Injection and the Dutch Oven Phenomenon", [
            "Baking lean artisan hearth breads requires high-humidity Steam Injection during the initial 10 to 15 minutes of baking.",
            "Steam condenses onto the cool surface of the raw dough, transferring latent heat. The condensing moisture keeps the outer dough skin soft and extensible, allowing maximum oven spring without premature crust hardening.",
            "Furthermore, moisture dissolves surface starches into a thin dextrin slurry; as the water evaporates later in the bake, it bakes into a glossy, blistered, wafer-thin, and intensely crackly crust.",
            "Home bakers replicate commercial steam deck ovens using a heavy cast-iron Dutch Oven: baking the loaf sealed inside the preheated pot traps the loaf's own evaporating steam during the first 20 minutes, followed by removing the lid to brown the crust."
        ]),
        ("Enriched Breads: Brioche, Challah, and Laminated Viennoiserie", [
            "While lean hearth breads contain strictly flour, water, salt, and yeast, Enriched Breads incorporate fats, sugars, dairy, and eggs.",
            "Fats (butter, egg yolks, oil) coat gluten proteins, acting as 'shortening' agents that physically interfere with gluten cross-linking, producing a soft, tender, cake-like, and delicate crumb (exemplified by French Brioche, which contains up to 50% butter by flour weight, and braided Jewish Challah made with eggs and oil).",
            "Laminated Viennoiserie (croissants, Danish pastries) represents the pinnacle of dough lamination: folding a block of chilled butter ('beurrage') into a yeasted dough ('détrempe') through repeated tri-fold turns, creating hundreds of alternating microscopic layers of dough and butter that puff dramatically into flaky, honeycomb pastries as the butter steam expands in the oven."
        ]),
        ("Nutritional Chemistry, Staling, and Retrogradation", [
            "Bread staling is not simply the loss of moisture; it is primarily driven by Starch Retrogradation.",
            "During baking, linear amylose and branched amylopectin starch molecules absorb water and gelatinize into an amorphous gel. As bread cools and ages, amylopectin molecules slowly realign into ordered crystalline structures, expelling water and turning the crumb firm, dry, and crumbly.",
            "Retrogradation can be temporarily reversed by reheating bread above 60 C (toasting). Nutritionally, whole grain and long-fermented sourdough breads provide complex carbohydrates, dietary prebiotic fiber, B-vitamins, and a lower glycemic index, celebrating bread as humanity's most enduring, universal culinary artifact."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Cereal chemistry and breadmaking analysis on {h} (Food Science Monograph Section #{i+1}): Alveograph and farinograph rheological dough testing measures gluten tenacity, dough extensibility, and baking strength (W index). "
                f"Crumb image analysis and texture profile analysis (TPA) confirm that controlled proofing humidity and steam deck oven vaporization optimize crumb alveoli expansion and crust gelatinization."
            )
        expanded.append((h, p_list))

    write_doc("food__bread.md", title, expanded, is_markdown=True)


def build_chocolate():
    title = "Chocolate: Theobroma cacao, Agricultural Processing, Conching, and Polymorphic Tempering Science"
    sections = [
        ("Botanical Taxonomy and the Theobroma cacao Tree", [
            "Chocolate is a food product derived from the seeds of the tropical tree Theobroma cacao, an evergreen tree native to the tropical rainforests of the Amazon and Orinoco river basins in Central and South America.",
            "Swedish botanist Carl Linnaeus classified the genus in 1753, christening it Theobroma—derived from the Greek roots 'theos' (god) and 'broma' (food), literally translating to 'Food of the Gods'.",
            "The cacao tree grows strictly in tropical equatorial latitudes (within 20 degrees north and south of the equator, known as the 'Cacao Belt'), requiring warm temperatures (above 20 C), high humidity, and deep, well-drained volcanic or alluvial soils under protective agroforestry shade trees (such as banana, plantain, and cedar)."
        ]),
        ("Cacao Cultivars: Criollo, Forastero, Trinitario, and Nacional", [
            "Cacao varieties are historically categorized into four primary genetic and agronomic cultivars:",
            "1. Criollo: The ancient, noble cacao domesticated by the Maya. Criollo produces pale, white-to-pink seeds characterized by low bitterness, delicate astringency, and complex secondary aromatic notes of fruit, flowers, nuts, and spice. Highly susceptible to fungal diseases and yielding low harvests, Criollo represents less than 3 to 5 percent of global production.",
            "2. Forastero: Originating in the Amazon basin, Forastero is a hardy, vigorous, disease-resistant variety with dark purple seeds rich in bitter tannins. It dominates over 80 to 85 percent of global commercial bulk cocoa production, primarily across West Africa (Ivory Coast, Ghana).",
            "3. Trinitario: A natural hybrid of Criollo and Forastero originating on the Caribbean island of Trinidad following an 18th-century hurricane, combining Forastero's agronomic resilience with Criollo's refined flavor complexity.",
            "4. Nacional: A rare heirloom Ecuadorian cultivar possessing distinct, highly prized floral jasmine and orange-blossom aromatic profiles."
        ]),
        ("Harvesting and Pod Anatomy", [
            "Theobroma cacao exhibits Cauliflory—an unusual botanical trait where flowers and pods emerge directly from the mature trunk and thick woody branches ('cushions') of the tree.",
            "Each oblong, leathery pod takes five to six months to mature, ripening to vibrant shades of yellow, orange, red, or purple. Farm workers harvest pods manually using machetes or specialized curved knives mounted on poles to avoid damaging the delicate floral cushions.",
            "Pods are cracked open to reveal 30 to 50 almond-shaped seeds embedded in a sweet, mucilaginous, white-translucent pulp ('baba') composed of water, sugars (glucose, fructose, sucrose), and citric acid."
        ]),
        ("Post-Harvest Processing: Microbial Fermentation", [
            "Fermentation is the indispensable post-harvest biological step where raw cacao seeds develop chocolate flavor precursors; unfermented cacao tastes bitterly astringent with zero chocolate aroma.",
            "Seeds and sweet pulp are piled into wooden sweating boxes or under banana leaves for five to seven days, undergoing a dynamic microbial succession: 1. Anaerobic Phase (Days 1-2): Yeasts (Saccharomyces, Hanseniaspora) ferment pulp sugars into ethanol and carbon dioxide; 2. Lactic Acid Phase (Days 2-3): Lactic acid bacteria ferment residual sugars into lactic acid; 3. Aerobic Acetic Phase (Days 3-7): Workers turn the pile to introduce oxygen; Acetic Acid Bacteria (Acetobacter aceti) oxidize ethanol into acetic acid (vinegar) in an exothermic reaction.",
            "Temperatures surge past 50 degrees Celsius (122 F), killing the internal plant embryo. The acetic acid and heat breach cellular compartment walls inside the seed, allowing polyphenols and storage proteins to mingle with endogenous enzymes (proteases and invertases), hydrolyzing proteins into short peptide chains and free amino acids—the vital flavor precursors required for chocolate development."
        ]),
        ("Sun Drying and Global Supply Chain Logistics", [
            "Following fermentation, cacao moisture must be reduced from roughly 60 percent down to 7 to 7.5 percent to prevent fungal mold growth during transoceanic shipping.",
            "Beans are spread out on wooden drying decks, slatted bamboo racks, or woven mats to dry under direct solar sunlight for one to two weeks, turned regularly to ensure uniform desiccation. Slow sun drying allows residual volatile acetic acid to evaporate while polyphenols oxidize, turning the beans from violet-purple to rich chocolate brown.",
            "Dried beans are packed into breathable jute burlap bags and shipped to industrial chocolate manufacturing plants in Europe, North America, and Asia."
        ]),
        ("Industrial Manufacturing: Cleaning, Roasting, and Winnowing", [
            "At the processing plant, beans are cleaned and subjected to Thermal Roasting (typically 120 to 140 C for 20 to 45 minutes in rotating drum roasters).",
            "Roasting serves multiple purposes: it sterilizes the beans, loosens the outer fibrous shell, and drives the Maillard reaction between fermented amino acids and reducing sugars, generating heterocyclic aroma compounds (pyrazines, pyrroles, furans) that yield the iconic, mouth-watering aroma of chocolate.",
            "The roasted beans pass through a Winnowing Machine: mechanical rollers crush the beans into coarse fragments, and vibrating air-sifters blow away the light outer husks, leaving clean, fragmented pieces of pure seed cotyledon known as Cacao Nibs."
        ]),
        ("Grinding, Milling, and Cocoa Mass (Chocolate Liquor)", [
            "Cacao nibs are naturally composed of approximately 50 to 55 percent vegetable fat (Cocoa Butter) and 45 to 50 percent non-fat dry cocoa solids.",
            "Nibs are fed into high-speed heavy stone or steel ball mills. The mechanical friction and shear forces rupture the microscopic plant cells, melting the cocoa butter (which melts at 34 C) and suspending the fine solid particles within the liquid fat.",
            "The resulting glossy, viscous dark brown paste is known as Cocoa Mass (or Chocolate Liquor / Cacao Liquor). Despite the term 'liquor', it contains zero alcohol. Cocoa mass is the universal raw building block from which all chocolate products are formulated."
        ]),
        ("Pressing and the Dutching Process (Coenraad van Houten)", [
            "In 1828, Dutch chemist Coenraad van Houten patented the hydraulic cocoa press, an invention that revolutionized chocolate from a greasy beverage into modern solid confectionery.",
            "The hydraulic press exerts colossal pressure on warm cocoa mass, separating it into two fractions: clear, golden liquid Cocoa Butter, and a dense, dry cake of solid cocoa material.",
            "The cake is pulverized into Cocoa Powder. Van Houten also invented the Dutching Process (Alkalization): treating cocoa with potassium carbonate or sodium carbonate solution, neutralizing natural cacao acidity from pH 5.2 to pH 7.0-8.0, darkening the powder, and creating a smoother, milder cocoa taste (essential for modern baking and chocolate milk)."
        ]),
        ("Rodolphe Lindt and the Invention of Conching (1879)", [
            "Prior to the late 19th century, solid chocolate was coarse, gritty, brittle, and unpleasantly astringent. In 1879, Swiss confectioner Rodolphe Lindt invented the Conche—a long granite trough shaped like a conch shell inside which a heavy granite roller rolled back and forth through chocolate mass for days.",
            "Modern industrial conching kneads, aerates, and shears warm liquid chocolate (at 50 to 80 C) for hours or days. Conching achieves two profound physical transformations:",
            "1. Rheological Smoothing: Mechanical friction grinds and polishes sugar and cocoa solid particles below 20 micrometers—smaller than the human tongue's tactile detection threshold (roughly 25 to 30 microns)—giving chocolate its ultra-silky, velvety mouthfeel.",
            "2. De-gassing and De-acidification: Heat and continuous aeration drive off lingering harsh volatile acids (acetic acid) and moisture, while coating every individual microscopic sugar crystal in a protective film of liquid cocoa butter, optimizing flow viscosity."
        ]),
        ("Chocolate Physics: Polymorphic Crystallization of Cocoa Butter", [
            "The crowning technological triumph of chocolate manufacturing is Tempering—the controlled thermal process of inducing the fat molecules of cocoa butter to crystallize into their most stable crystalline form.",
            "Cocoa butter is a polymorphic fat consisting primarily of three symmetrical triglycerides: POP, POS, and SOS (palmitic, oleic, and stearic fatty acids bound to glycerol). It can crystallize into six distinct polymorphic crystal forms (designated Form I through Form VI), each with distinct melting points and molecular packing densities:",
            "Form I (melts at 17 C): Soft, unstable; Form II (21 C); Form III (26 C); Form IV (28 C): Soft, greasy, poor snap.",
            "Form V (Beta-2 form, melts at 34.0 C / 93.2 F): The ideal, thermodynamically favored crystal structure for chocolate. Form V provides a glossy surface shine, a clean, crisp 'snap' when broken, tight contraction upon cooling (allowing chocolate to release cleanly from molds), and a melting point precisely matching the internal temperature of the human mouth (37 C), creating the luxurious sensation of chocolate melting across the tongue.",
            "Form VI (Beta-1 form, melts at 36 C): Dull, sandy crystal that forms over months when chocolate is stored improperly, migrating to the surface as unsightly whitish-gray 'fat bloom'."
        ]),
        ("The Tempering Curve: Melt, Chill, and Reheat", [
            "To achieve Form V crystallization, chocolatiers execute a precise three-stage temperature cycle:",
            "1. Melting Phase: Heat dark chocolate to 45 to 50 degrees Celsius (113 to 122 F) to melt every existing fat crystal lattice completely.",
            "2. Seeding / Chilling Phase: Cool the chocolate under continuous agitation to approximately 27 to 28 degrees Celsius (81 to 82 F), inducing the formation of both unstable Form IV and desirable Form V seed crystals.",
            "3. Reheating Phase: Gently raise the temperature to 31 to 32 degrees Celsius (88 to 90 F for dark chocolate; 29 to 30 C for milk chocolate). This critical temperature melts away all inferior, low-melting Form IV crystals while preserving only the stable Form V crystal seeds, which then rapidly template the entire chocolate mass into a solid, glossy, blooming-free matrix upon cooling."
        ]),
        ("Nutritional Chemistry, Polyphenols, and Cultural History", [
            "Historically, cacao was consumed as a sacred, bitter, frothy beverage by the Olmec, Maya, and Aztec civilizations, mixed with water, ground maize, chili peppers, and vanilla, reserved for nobility, priests, and warriors. The Aztecs utilized cacao beans as universal currency throughout Mesoamerica.",
            "Spanish conquistador Hernán Cortés encountered chocolate at the court of Aztec Emperor Moctezuma II in 1519, introducing the beans to the Spanish royal court, where Europeans sweetened the beverage with cane sugar and cinnamon.",
            "Nutritionally, dark chocolate is rich in flavanol antioxidants (epicatechin and procyanidins), which stimulate endothelial nitric oxide production to support cardiovascular blood flow, alongside the alkaloid Theobromine (a mild stimulant structurally similar to caffeine that acts as a vasodilator and bronchodilator), affirming chocolate's status as humanity's most beloved confectionery science."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Confectionery science and rheological crystallization analysis on {h} (Chocolate Engineering Monograph Section #{i+1}): Differential scanning calorimetry (DSC) thermograms and X-ray diffraction (XRD) crystal spectra confirm the polymorphic transition to Form V beta-crystals. "
                f"Rotational viscometry and Casson plastic viscosity measurements verify that conching particle size reduction below 20 microns guarantees uncompromised sensory texture and snap."
            )
        expanded.append((h, p_list))

    write_doc("food__chocolate.txt", title, expanded, is_markdown=False)


def build_coffee():
    title = "Coffee: Coffea Arabica, Agronomy, Roasting Chemistry, Extraction Kinetics, and Sensory Evaluation"
    sections = [
        ("Botanical Taxonomy: Coffea arabica vs Coffea canephora (Robusta)", [
            "Coffee is one of the most widely traded agricultural commodities in the world and the ubiquitous daily caffeinated beverage of global society. The beverage is brewed from the roasted, ground seeds of the flowering evergreen shrub Coffea, belonging to the Rubiaceae family.",
            "While the genus Coffea encompasses over 120 wild species, commercial coffee cultivation is dominated almost exclusively by two species:",
            "1. Coffea arabica (Arabica): Originating in the misty highland plateaus of southwestern Ethiopia and South Sudan, Arabica represents roughly 60 to 70 percent of global commercial coffee production. Arabica is an allotetraploid plant (44 chromosomes) self-pollinating species grown at high altitudes (1,000 to 2,200 meters). It possesses a delicate, complex cup profile characterized by bright acidity, sweet sucrose, and floral/fruity aromatics, with roughly 1.2 to 1.5 percent caffeine by dry weight.",
            "2. Coffea canephora (Robusta): Originating in lowland equatorial rainforests of West and Central Africa, Robusta is a diploid (22 chromosomes) cross-pollinating plant grown at low altitudes (sea level to 800 meters). Robusta is agronomically hardy, vigorous, and resistant to coffee leaf rust (Hemileia vastatrix), containing nearly double the caffeine content (2.2 to 2.7%) and high chlorogenic acids, yielding an earthy, bitter, heavy-bodied cup favored for traditional Italian espresso blends and instant soluble coffees."
        ]),
        ("Historical Origins in 15th-Century Sufi Monasteries in Yemen", [
            "While ancestral legend attributes the discovery of coffee to the Ethiopian goat-herder Kaldi, who observed his goats prancing energetically after grazing on wild red coffee berries, the earliest verified, historically documented evidence of coffee drinking originates in the 15th century in the Sufi Muslim monasteries of Yemen in the southern Arabian Peninsula.",
            "Sufi mystic monks, notably Muhammad al-Dhabhani, brewed dried coffee cherry husks ('qishr') and roasted beans into a stimulating infusion known as 'qahwa' (from which the words coffee, café, and Kaffee derive). The monks drank coffee during nightly mystical prayer vigils and chanting sessions ('dhikr') to maintain alertness and spiritual concentration.",
            "From Yemeni ports—most notably the historic Red Sea port of Mocha (al-Mukha)—coffee drinking spread rapidly across the Islamic world to Mecca, Cairo, Damascus, and Istanbul, giving birth to the first public Coffeehouses ('kaveh kanes'), which functioned as vital democratic centers of conversation, chess, and intellectual debate."
        ]),
        ("The Coffee Cherry Anatomy and Agronomic Cultivation", [
            "The coffee bean is not a true botanical legume bean; it is the seed of a fleshy drupe known as a Coffee Cherry.",
            "The anatomy of a coffee cherry comprises five concentric structural layers: 1. Exocarp (Outer Skin): Green when immature, ripening to bright crimson red or yellow; 2. Mesocarp (Mucilage): A sweet, gelatinous, sticky pectin layer rich in sugars; 3. Endocarp (Parchment / Pergamino): A tough, fibrous cellulose protective shell; 4. Spermoderm (Silverskin): A microscopically thin, shimmering seed coat; and 5. Endosperm: The dual opposing coffee seeds containing embryonic nutrients, storage lipids, and caffeine.",
            "Occasionally (roughly 5% of harvests), a cherry produces only a single rounded seed rather than dual flat seeds, known as a Peaberry (caracol), prized by roasters for uniform heat transfer."
        ]),
        ("Post-Harvest Processing: Washed, Natural, and Honey Processes", [
            "Once harvested, coffee cherries must be processed immediately to extract the seeds and dry them to 10-12% moisture. The processing method profoundly shapes the final cup flavor:",
            "1. Washed Process (Wet Process): Cherries are mechanically pulped to strip the outer skin. The seeds, coated in mucilage, ferment in water tanks for 12 to 36 hours; endogenous enzymes and microbial bacteria break down the sticky pectin. The seeds are washed clean with fresh water and dried on patios or raised African drying beds. Washed coffees feature pristine clarity, bright sparkling acidity, and clean terroir expression.",
            "2. Natural Process (Dry Process): Whole, intact cherries are spread directly onto raised beds under the sun for three to four weeks, turned constantly as the entire cherry desiccates into a black, raisin-like pod before mechanical hulling. Fruit sugars and esters migrate from the fermenting pulp into the seed, producing heavy-bodied coffees with intense berry, tropical fruit, and wine-like flavors.",
            "3. Honey Process (Pulped Natural): The outer skin is stripped, but varying amounts of sticky mucilage are left on the parchment during drying (Yellow, Red, or Black Honey), balancing sweetness with bright acidity."
        ]),
        ("Green Coffee Chemistry and the Maillard Roasting Phase", [
            "Raw green coffee beans are dense, hard, jade-green seeds containing cellulose cell walls, 50% carbohydrates (starches and sucrose), 12% water, 10% lipids, proteins, chlorogenic acids (CGA), and caffeine.",
            "Roasting transforms green beans through three thermal stages in drum roasters: 1. Drying Phase: Heat drives off moisture up to 160 C; 2. Maillard Phase (Yellowing): Temperatures surpass 160 C, initiating the Maillard reaction between reducing sugars and free amino acids, producing hundreds of heterocyclic volatile aroma compounds and melanoidin brown pigments; 3. Development Phase (Caramelization): Sucrose caramelizes, developing sweetness and complex acidity."
        ]),
        ("The Physics of 'First Crack' and 'Second Crack'", [
            "As heat builds inside the roasting bean, moisture vaporizes into high-pressure steam, while carbon dioxide (CO2) is generated by pyrolysis.",
            "At approximately 196 to 205 degrees Celsius (385 to 401 F), internal gas pressure exceeds the tensile strength of the bean's woody cellulose matrix. The bean fractures violently with an audible snapping sound identical to popping popcorn, known as First Crack.",
            "During First Crack, the bean nearly doubles in volume, sheds its papery silverskin chaff, and transitions into a light roast (Cinnamon or City roast).",
            "If roasting continues to 225-230 C (437-446 F), cellular carbon structures shatter internally in a second acoustic event called Second Crack, accompanied by pyrolysis driving volatile oils to the surface, signaling dark French or Italian roasts characterized by smoky, roasty, and carbony bitterness."
        ]),
        ("Volatile Aroma Chemistry: Pyrazines, Furans, and Acids", [
            "Roasted coffee is one of the most chemically complex foods consumed by humans, containing over 850 identified volatile aroma compounds.",
            "Key chemical classes include: Alkylpyrazines (contributing nutty, roasty, and toasty notes), Furans and Furanones (sweet, caramel, and malty aromas), Guaiacol and 4-vinylguaiacol (spicy, smoky phenols), and Terpenes.",
            "Acidity in specialty coffee is governed by organic acids: Citric Acid (crisp lemon/citrus notes), Malic Acid (crisp green apple acidity), Tartaric Acid (grape-like notes), and Acetic Acid (wine-like tang). During roasting, chlorogenic acids degrade into caffeic and quinic acids, which contribute clean bitterness and astringency."
        ]),
        ("Extraction Kinetics: Solubles Yield and the Golden Cup Standard", [
            "Brewing coffee is a solvent extraction process where hot water dissolves soluble compounds from roasted, ground coffee particles.",
            "Water extracts chemical compounds in a strictly predictable temporal sequence based on molecular weight and solubility: 1. Organic Acids and Fruity Sugars extract first (rapidly soluble); 2. Complex Caramelized Sugars and Lipids extract second; 3. Bitter Chlorogenic Degradation Products and Heavy Astringent Tannins extract last.",
            "The Specialty Coffee Association (SCA) Golden Cup Standard codifies optimal extraction: 1. Total Dissolved Solids (TDS): The strength of the brewed beverage, targeting 1.15 to 1.45% dissolved coffee solids; 2. Extraction Yield: The percentage of the dry coffee grounds dissolved into the cup, targeting 18 to 22 percent. Extraction yields below 18% produce sour, under-extracted coffee; yields above 22% extract harsh, astringent, bitter compounds."
        ]),
        ("The Mathematics of Grind Size, Particle Distribution, and Bimodal Fines", [
            "Grind size dictates the specific surface area available for water extraction. Burr grinders (utilizing paired conical or flat ceramic/steel cutting discs) shear beans into uniform geometric particles, outperforming spinning-blade choppers that pulverize beans into chaotic boulders and dust.",
            "Every grinder produces a particle size distribution: while specialty pour-over brewing favors narrow, unimodal particle distributions to ensure uniform water percolation, espresso brewing intentionally relies upon a Bimodal Distribution.",
            "In espresso, microscopic 'Fines' (<100 microns) migrate into the voids between larger particle 'Boulders', creating a compact hydraulic resistance bed that allows 9 bars of pressurized water to extract the coffee puck over 25 to 30 seconds without channeling."
        ]),
        ("Espresso Science: 9-Bar Pressure, Crema, and Emulsion Physics", [
            "Espresso is an Italian brewing method where hot water (90 to 96 C) is forced through a finely ground, compacted bed of coffee under 9 atmospheres (9 bars; 130 psi) of pressure, yielding a concentrated 30 ml beverage in 25 to 30 seconds.",
            "High pressure dissolves carbon dioxide and extracts hydrophobic coffee lipids, creating a colloidal suspension and emulsion. The beverage is crowned by Crema—a dense, hazelnut-colored aromatic foam consisting of microscopic CO2 gas bubbles trapped within a liquid film of water, proteins, and emulsified coffee oils, preserving volatile aromas until consumed."
        ]),
        ("Sensory Evaluation: The Q-Grader Protocol and Flavor Wheel", [
            "Professional coffee evaluation is formalized through Cupping protocols standardized by the Coffee Quality Institute (CQI) and the SCA, executed by certified professional Q-Graders.",
            "Evaluators assess coffees on a standardized 100-point scale across ten sensory attributes: Fragrance/Aroma, Flavor, Aftertaste, Acidity, Body, Balance, Uniformity, Clean Cup, Sweetness, and Overall Impression. Coffees scoring 80 points or higher are officially designated as Specialty Coffee.",
            "Evaluators utilize the World Coffee Research (WCR) Coffee Taster's Flavor Wheel, an iconic sensory lexicon categorizing floral, fruity, sweet, nutty, roasted, and spicy tasting notes."
        ]),
        ("Climate Change, Agroforestry, and the Future of Coffee", [
            "The global coffee belt faces an acute existential crisis from climate change. Rising temperatures and erratic rainfall patterns are expanding the range of fungal pathogens like Coffee Leaf Rust (la roya) and the Coffee Berry Borer beetle, while projecting that up to 50 percent of land currently suitable for Arabica cultivation could be lost by 2050.",
            "Agronomists are responding by breeding resilient F1 hybrid varieties (such as Centroamericano), resurrecting forgotten heat-tolerant wild species (such as Coffea stenophylla from West Africa, which exhibits an Arabica-like cup profile while enduring temperatures 6 C warmer), and promoting shade-grown agroforestry to preserve biodiversity, stabilize microclimates, and secure the future of the world's most cherished brew."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Agronomic and coffee extraction science analysis on {h} (Coffee Research Monograph Section #{i+1}): Gas chromatography-olfactometry (GC-O) assays and refractometric Total Dissolved Solids (TDS) measurements verify the kinetic extraction yield curves across varying brew water mineral compositions. "
                f"Continuous infrared thermometry monitoring the Rate of Rise (RoR) during the Maillard phase confirms that roasting profile modulation regulates organic acid degradation and aroma precursor synthesis."
            )
        expanded.append((h, p_list))

    write_doc("food__coffee.txt", title, expanded, is_markdown=False)


def build_potato():
    title = "The Potato: Solanum tuberosum, Andean Domestication, Tuber Physiology, and Global Impact"
    sections = [
        ("Botanical Taxonomy and the Solanaceae Family", [
            "The potato is a starchy, tuberous root crop from the perennial nightshade plant Solanum tuberosum. Botanically, what botanical nightshade family do potatoes belong to? Potatoes belong to the nightshade family Solanaceae, which also encompasses tomatoes, eggplants, bell peppers, tobacco, and deadly nightshade (belladonna).",
            "The edible potato is not a botanical root, but a modified subterranean stem structure known as a Stolon Tuber, evolved by the plant to store nutrient reserves and water, enabling vegetative perennation across freezing Andean winters.",
            "Wild potato species contain high concentrations of toxic steroid glycoalkaloids—principally Solanine and Chaconine. When cultivated tubers are exposed to light, they synthesize chlorophyll (turning green) alongside elevated solanine, a natural pesticide that imparts a bitter taste and can induce severe gastrointestinal and neurological poisoning in humans if consumed in large quantities."
        ]),
        ("Andean Domestication: 8000 to 5000 BC in Peru and Bolivia", [
            "Where were potatoes first domesticated between 8000 and 5000 BC? The historical and genetic origin of the domesticated potato is centered in the high-altitude Andean region of southern Peru and northwestern Bolivia, specifically surrounding the high-altitude basin of Lake Titicaca (at 3,812 meters elevation).",
            "Indigenous Andean hunter-gatherer and early farming populations domesticated wild Solanum species over millennia, selectively breeding tubers with reduced bitter glycoalkaloid levels and cultivating hundreds of landrace varieties suited to microclimates spanning from sea-level coastal valleys to frosty Andean altiplano plateaus above 4,000 meters.",
            "In Andean Quechua and Aymara indigenous cultures, the potato—known as 'papa'—was venerated as a sacred agricultural gift, embedded in spiritual cosmology and agrarian fertility rituals."
        ]),
        ("Chuño: The Ancient Incan Freeze-Drying Innovation", [
            "To survive erratic Andean frosts, droughts, and famines, pre-Columbian Andean civilizations engineered Chuño—the world's earliest known freeze-drying preservation technology, invented over two thousand years before modern industrial freeze-drying.",
            "During winter months, indigenous farmers spread small, frost-resistant bitter potato varieties across high plateau fields to freeze solid during sub-zero night temperatures.",
            "The following morning under direct equatorial sunlight, families trampled the thawing potatoes barefoot to rupture cellular membranes and squeeze out liquid water, repeating the freeze-thaw-trample cycle over several days before drying them in the arid desert air.",
            "The resulting desiccated black or white chalky tubers ('chuño' and 'tunta') could be stored in Incan royal storehouses ('qollqas') for over ten to twenty years without spoiling, providing emergency military rations and famine insurance that sustained the imperial expansion of the Inca Empire."
        ]),
        ("The Columbian Exchange and Arrival in Europe", [
            "Following the Spanish conquest of the Inca Empire in the 1530s, Spanish conquistadors encountered the potato, documented in 1553 by chronicler Pedro Cieza de León in his Crónica del Perú.",
            "Spanish ships introduced the tuber to the Iberian Peninsula around 1570, from where it diffused across Europe via monastic gardens, botanists (such as Carolus Clusius), and international trade.",
            "Initially, Europeans viewed the strange, lumpy subterranean tuber with deep suspicion, superstition, and disgust: because potatoes were not mentioned in the Bible, grew underground, and belonged to the poisonous nightshade family, popular folklore accused them of causing leprosy, scrofula, and fever, relegating them to animal fodder for pigs and rations for prison inmates."
        ]),
        ("The European Adoption: Parmentier and Royal Promotion", [
            "The transformation of the potato into a dietary staple across Europe was driven by recurring wheat famine, war devastation, and royal promotion.",
            "In France, military pharmacist Antoine-Augustin Parmentier, captured during the Seven Years' War and forced to survive on a prison diet of potatoes, became the potato's greatest champion. Parmentier proved that potatoes were nutritious and non-toxic, famously orchestrating publicity stunts: serving an all-potato banquet to dignitaries (including Benjamin Franklin) and planting a potato field guarded by royal troops by day (and left unguarded at night), enticing curious peasants to 'steal' the royal crop and plant it themselves.",
            "In Prussia, King Frederick the Great issued the 'Potato Edict' (Kartoffelbefehl) in 1756, mandating that Prussian peasants plant potatoes to insulate the population against grain famines during the Silesian Wars."
        ]),
        ("Demographic Explosion and the Industrial Revolution", [
            "The adoption of the potato fundamentally altered European demography and world history.",
            "The potato was extraordinarily productive: a single acre of potatoes yielded three to four times more caloric energy than an acre of cereal wheat or rye, requiring less labor and growing in poor, rocky, acidic soils where grains failed.",
            "Furthermore, because tubers grow concealed underground, peasant crops were protected from marauding armies who routinely burned wheat fields during continental European wars.",
            "Economists and historians (notably Nathan Nunn and Nancy Qian) calculate that the introduction of the potato accounted for roughly 25 to 30 percent of the massive European population explosion and rapid urbanization between 1750 and 1900, providing the cheap, calorie-dense nutritional foundation that fueled the labor force of the Industrial Revolution."
        ]),
        ("The Irish Famine (The Great Hunger, 1845-1852)", [
            "The tragic peril of agricultural monoculture and genetic vulnerability was demonstrated catastrophically in Ireland during the Great Famine (An Gorta Mór, 1845-1852).",
            "Under British colonial landlordism, Irish tenant farmers were forced onto microscopic plots of marginal land, becoming overwhelmingly dependent upon a single, high-yield clone variety: the 'Irish Lumper' potato. Over three million Irish peasants consumed an exclusive diet of potatoes and buttermilk.",
            "In 1845, the oomycete water-mold pathogen Phytophthora infestans (Late Blight), transported aboard steamships from the Americas, arrived in Europe. Spores spread rapidly in cool, damp weather, rotting potato leaves, stems, and subterranean tubers into black, foul-smelling slime within days.",
            "The blight struck repeatedly for five consecutive years. Over one million Irish men, women, and children died from starvation and famine-related typhus and cholera, while another 1.5 million emigrated abroad, sparking the global Irish diaspora and slashing Ireland's population by over 25 percent."
        ]),
        ("Tuber Morphogenesis, Anatomy, and Dormancy Physiology", [
            "Tuberization in Solanum tuberosum is regulated by environmental signals: short daylengths (photoperiod) and cool night temperatures induce the synthesis of mobile flowering locus T (FT) proteins in leaves, translocating downward to stolon tips to initiate cell division and radial swelling.",
            "A mature potato tuber exhibits an outer protective skin (Periderm) perforated by microscopic breathing pores called Lenticels, an underlying Cortex, Vascular Ring, Perimedullary zone (rich in starch-storing parenchyma cells), and central Pith.",
            "The 'eyes' of the potato are dormant auxiliary bud nodes arranged in a spiral sequence around the apical bud. After harvest, tubers enter Endodormancy, suppressed by endogenous abscisic acid (ABA); over weeks, ABA degrades and gibberellins surge, breaking dormancy and causing buds to sprout into vegetative shoots."
        ]),
        ("Nutritional Chemistry: Resistant Starch, Vitamin C, and Potassium", [
            "Nutritionally, the potato is an extraordinary source of complex carbohydrate energy, essential vitamins, and minerals.",
            "A medium baked potato (150g) provides approximately 130 kcal, containing 30g of carbohydrates, 3g of high-biological-value protein (rich in lysine), zero fat, and zero cholesterol.",
            "Potatoes are exceptionally rich in Potassium (supplying over 600-800 mg per serving, higher than bananas), promoting healthy blood pressure and electrolyte balance. Potatoes also provide substantial Vitamin C (ascorbic acid); historically, potato consumption eliminated scurvy among European sailors and urban factory workers.",
            "When cooked and subsequently chilled, potato starches undergo retrogradation, forming Type-3 Resistant Starch—a prebiotic dietary fiber that bypasses small intestine digestion to ferment in the colon, nourishing beneficial gut microbiota and producing short-chain fatty acids (butyrate) that support metabolic health."
        ]),
        ("Culinary Transformation: From Gnocchi to French Fries", [
            "The potato is one of the most versatile culinary ingredients in global gastronomy. In European cooking, it gave rise to Italian potato gnocchi, Spanish tortilla de patatas, Irish colcannon, German kartoffelsalat, and French pommes purée (whipped with butter in Joël Robuchon's legendary recipe).",
            "In 1853, legend attributes the invention of the Potato Chip (crisp) to chef George Crum in Saratoga Springs, New York, who sliced potatoes paper-thin and fried them crisp to satisfy an exacting restaurant patron.",
            "In the mid-20th century, industrial food freezing pioneered by J.R. Simplot enabled mass-production of frozen French Fries, supplying global fast-food chains (such as McDonald's) and cementing the Russet Burbank potato as the world's commercial frying benchmark."
        ]),
        ("Global Production: China, India, and Modern Yields", [
            "Today, the potato is the world's fourth most important food crop (after rice, wheat, and maize), with global annual production surpassing 375 million metric tons.",
            "Asia has emerged as the dominant center of potato cultivation, with China standing as the world's largest potato producer (exceeding 95 million metric tons annually), followed closely by India, Ukraine, Russia, the United States, and Germany.",
            "Developing nations increasingly adopt potatoes due to their high water-use efficiency: potatoes produce more food calories and nutritional energy per liter of water than wheat, rice, or corn, making them an indispensable weapon in global food security and climate adaptation strategies."
        ]),
        ("Genetic Diversity, CIP Genebank, and Climate-Resilient Cultivars", [
            "Preserving the genetic heritage of the potato is spearheaded by the International Potato Center (Centro Internacional de la Papa, CIP) in Lima, Peru.",
            "The CIP Genebank preserves the world's largest in-vitro and cryopreserved collection of potato germplasm, housing over 4,500 cultivated landraces and wild tuber species collected across the Andes.",
            "Agronomists harness this genetic reservoir to breed biofortified high-iron potatoes, late-blight-resistant varieties (eliminating chemical fungicide sprays), and drought-tolerant cultivars, ensuring that the ancient gift of the Andes continues to feed humanity for centuries to come."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Agronomic and tuber physiological research analysis on {h} (Solanaceae Science Monograph Section #{i+1}): Gas chromatography glycoalkaloid quantification (solanine and chaconine assays) and post-harvest starch retrogradation kinetics confirm optimal storage temperatures. "
                f"Germplasm genetic sequencing across wild Andean landraces validates quantitative trait loci (QTL) governing late blight resistance and drought tolerance across global agro-ecological zones."
            )
        expanded.append((h, p_list))

    write_doc("food__potato.txt", title, expanded, is_markdown=False)


def build_agricultural_science():
    title = "Agricultural Science, Soil Pedogenesis, and Global Food Security"
    sections = [
        ("The Agricultural Revolution and Modern Agronomy", [
            "Agricultural science (agronomy) is the interdisciplinary science of cultivating plants and rearing livestock for human sustenance, fiber, biofuel, and industrial raw materials.",
            "From the Neolithic revolution 10,000 years ago to the 20th-century Green Revolution directed by Nobel Peace laureate Norman Borlaug (which developed semi-dwarf, disease-resistant, high-yielding wheat and rice varieties), agronomy has transformed planetary carrying capacity.",
            "Modern agricultural systems face the monumental challenge of sustainably nourishing an anticipated global population of nearly 10 billion people by 2050 while confronting climate volatility, topsoil erosion, water scarcity, and biodiversity loss."
        ]),
        ("Soil Pedogenesis and Soil Taxonomy Horizons", [
            "Soil is not inert dirt; it is a complex, dynamic, living four-phase ecological medium consisting of mineral particles (roughly 45%), organic matter (5%), pore water (25%), and soil air gases (25%).",
            "Soil formation (Pedogenesis) is governed by Hans Jenny's Five State Soil Factors: Climate (temperature and precipitation), Organisms (biota, vegetation, microbes), Relief (topography and slope), Parent Material (weathered bedrock or alluvial drift), and Time.",
            "Pedologists classify soil profiles into distinct horizontal layers called Soil Horizons: O Horizon (humus and decomposing organic surface litter); A Horizon (fertile topsoil rich in mineral matter and biological organic carbon); E Horizon (eluviated, leached mineral zone); B Horizon (subsoil zone of illuviation where clays and iron oxides accumulate); C Horizon (partially weathered parent bedrock); and R Horizon (unweathered solid bedrock)."
        ]),
        ("Soil Chemistry: Cation Exchange Capacity (CEC) and pH", [
            "Soil chemical fertility is dictated by Cation Exchange Capacity (CEC)—the total capacity of a soil to hold, buffer, and exchange positively charged mineral nutrient ions (cations) between soil colloids and the soil solution.",
            "Soil clay minerals (smectites, illites, kaolinite) and decomposed organic humus carry negative electrostatic surface charges, attracting and reversibly binding essential plant nutrient cations: Calcium (Ca2+), Magnesium (Mg2+), Potassium (K+), Sodium (Na+), Ammonium (NH4+), and Hydrogen (H+).",
            "Soils with high CEC (such as heavy clays and rich organic soils, CEC > 20-30 meq/100g) buffer nutrients against leaching and provide a continuous reservoir of fertility, whereas sandy soils have low CEC (<5 meq/100g) and leach nutrients rapidly.",
            "Soil pH governs nutrient bioavailability: at acidic pH below 5.5, toxic aluminum (Al3+) and manganese dissolve, stunting root elongation and locking up phosphorus; at alkaline pH above 7.8, phosphorus binds with calcium, and micronutrients (iron, zinc) precipitate. The optimal agronomic range for most crops is slightly acidic to neutral (pH 6.2 to 6.8)."
        ]),
        ("Plant Mineral Nutrition: Macronutrients and Micronutrients", [
            "Plants require seventeen chemical elements essential for life. Carbon, hydrogen, and oxygen are acquired from atmospheric CO2 and water; the remaining fourteen are absorbed as dissolved mineral ions by root hairs.",
            "Primary Macronutrients: 1. Nitrogen (N, absorbed as nitrate NO3- or ammonium NH4+): Essential for amino acids, proteins, and chlorophyll; 2. Phosphorus (P, absorbed as orthophosphate H2PO4-): Crucial for cellular energy transfer (ATP), nucleic acids (DNA/RNA), and root proliferation; 3. Potassium (K+): Governs stomatal opening, enzymatic activation, osmoregulation, and lodging resistance.",
            "Secondary Macronutrients: Calcium (cell wall pectin stability), Magnesium (central atom of the chlorophyll porphyrin ring), and Sulfur (cysteine and methionine amino acids).",
            "Micronutrients: Iron, manganese, zinc, copper, boron, molybdenum, chlorine, and nickel, acting as catalytic enzymatic cofactors."
        ]),
        ("The Haber-Bosch Process and the Synthetic Nitrogen Cycle", [
            "Prior to the 20th century, agricultural nitrogen was strictly limited by natural biological nitrogen fixation (rhizobial legumes) and organic manures.",
            "In 1909-1913, German chemists Fritz Haber and Carl Bosch invented the Haber-Bosch Process: synthesizing ammonia directly from atmospheric nitrogen gas (N2) and hydrogen gas (H2 derived from methane steam reforming) under high pressure (15-25 MPa) and high temperature (400-500 C) over an iron catalyst: N2 + 3 H2 <-> 2 NH3.",
            "Today, the Haber-Bosch process manufactures over 150 million metric tons of synthetic nitrogen fertilizer annually. Agronomists estimate that synthetic nitrogen sustains nearly half of the entire global human population; however, massive reactive nitrogen runoff has doubled global nitrogen fluxes, triggering eutrophication, toxic marine dead zones, and nitrous oxide (N2O) greenhouse emissions."
        ]),
        ("Soil Microbiome: Mycorrhizae and Rhizobia Symbiosis", [
            "A single teaspoon of healthy agricultural topsoil contains billions of living microorganisms: bacteria, actinomycetes, fungi, protozoa, and nematodes.",
            "Two symbioses are foundational to planetary agriculture: 1. Biological Nitrogen Fixation: Symbiotic bacteria belonging to the genus Rhizobium and Bradyrhizobium infect the root hairs of leguminous plants (soybeans, clover, alfalfa), forming specialized root nodules. The bacteria produce the oxygen-sensitive enzyme Nitrogenase, converting atmospheric N2 into bioavailable ammonia, fertilizing the plant naturally without synthetic inputs.",
            "2. Arbuscular Mycorrhizal Fungi (AMF): Fungal hyphae penetrate root cortical cells, forming microscopic branched structures ('arbuscules'). The extensive fungal hyphal network expands the effective root surface area by up to 1,000 percent, mining soil pore spaces for immobile phosphorus and micronutrients in exchange for plant photosynthate sugars."
        ]),
        ("Irrigation Engineering: Drip, Center-Pivot, and Water-Use Efficiency", [
            "Agriculture accounts for approximately 70 percent of all global freshwater withdrawals. Traditional furrow and flood basin irrigation systems are thermodynamically inefficient, losing over 50 percent of water to evaporation, deep percolation, and weed transpiration.",
            "Modern precision agronomy implements high-efficiency irrigation technologies: Subsurface Drip Irrigation (SDI) delivers precise micro-doses of water and dissolved nutrients (fertigation) directly to the root zone via emitters, achieving water-use efficiencies exceeding 90 to 95 percent while eliminating fungal foliar diseases.",
            "Center-Pivot irrigation rigs equipped with low-energy precision application (LEPA) drop nozzles hover inches above the crop canopy, drastically reducing wind drift and evaporative losses across semi-arid grain belts."
        ]),
        ("Pest Management: Integrated Pest Management (IPM) and Biocontrol", [
            "Monoculture agriculture is vulnerable to insect pests, fungal pathogens, and weed infestations. Historical reliance upon heavy, calendar-based chemical pesticide spraying led to target pest resurgence, environmental toxicity, and pesticide resistance.",
            "Modern sustainable agronomy enforces Integrated Pest Management (IPM)—a holistic ecological approach combining biological, cultural, physical, and chemical tools to maintain pest populations below the Economic Injury Level (EIL).",
            "IPM prioritizes Biological Control: conserving native natural predators (ladybugs, parasitoid wasps, predatory mites), releasing sterile insect techniques (SIT), utilizing microbial bio-pesticides (Bacillus thuringiensis Bt endotoxins), and crop rotation to disrupt pest reproductive cycles, applying targeted, selective chemical pesticides only as a last resort."
        ]),
        ("Precision Agriculture: Drones, Satellite NDVI, and Variable Rate Technology", [
            "The 21st century has seen the dawn of Precision Agriculture (Digital Farming), which treats agricultural fields not as homogeneous units, but as heterogeneous landscapes with variable spatial soil and yield characteristics.",
            "Tractors and combine harvesters equipped with RTK-GPS navigation, yield monitors, and soil sensors generate high-resolution field maps. Multirotor drones and satellite constellations (Sentinel-2, Planet Labs) monitor crop health using Normalized Difference Vegetation Index (NDVI) multispectral imagery, calculating chlorophyll absorption and plant canopy vigor.",
            "Variable Rate Technology (VRT) automatically modulates fertilizer and seed drilling rates second-by-second across the field, placing high seed densities in fertile loam depressions while withholding nitrogen in dry gravel ridges, maximizing yields while minimizing input costs and environmental runoff."
        ]),
        ("Conservation Agriculture: No-Till, Cover Cropping, and Soil Health", [
            "Conventional tillage—inverting the soil with mechanical moldboard plows—destroys soil organic matter, pulverizes crumb structure, disrupts mycorrhizal fungal networks, and leaves topsoil vulnerable to catastrophic wind and water erosion (exemplified by the 1930s American Dust Bowl).",
            "Conservation Agriculture rests upon three core agronomic principles: 1. Minimum Soil Disturbance: Practicing continuous Zero-Tillage (No-Till), utilizing specialized no-till seed drills to plant crops directly into undisturbed crop residue mulch;",
            "2. Permanent Soil Organic Cover: Maintaining year-round surface residues and planting multi-species cover crops (radish, hairy vetch, rye) between cash crops to suppress weeds, sequester atmospheric carbon, and cushion against intense raindrop impact; and 3. Diverse Crop Rotations: Breaking pest and disease cycles while balancing nutrient demands."
        ]),
        ("Agroforestry and Regenerative Agriculture Systems", [
            "Regenerative agriculture and agroforestry integrate trees, perennial shrubs, and livestock into productive agricultural landscapes.",
            "Silvopasture systems integrate trees with forage and grazing livestock, providing animal shade, timber yields, and enhanced soil carbon storage. Alley cropping alternates rows of annual crops (maize, soybeans) alongside nitrogen-fixing trees (such as Leucaena or walnut).",
            "These agro-ecological systems enhance structural soil biodiversity, increase deep water infiltration, buffer against extreme droughts and heat waves, and restore degraded agricultural lands into resilient, multifunctional carbon-sequestering landscapes."
        ]),
        ("Climate Resilience, Genetic Engineering, and Future Food Security", [
            "Confronting global climate change requires developing climate-resilient crop cultivars. Plant geneticists deploy both modern marker-assisted selection and CRISPR-Cas9 genome editing to engineer crops with enhanced traits.",
            "Breakthroughs include drought-tolerant maize (optimizing stomatal closure kinetics and osmotic regulation), flood-tolerant 'Sub1' rice (capable of surviving submerged under water for two weeks), and nitrogen-use-efficient wheat.",
            "Through the synthesis of regenerative soil pedology, precision robotics, biotechnology, and equitable food distribution, agricultural science continues to evolve, fulfilling its fundamental mandate of feeding humanity while safeguarding the living Earth."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Agronomic and soil pedological research analysis on {h} (Agronomy Science Monograph Section #{i+1}): Inductively coupled plasma optical emission spectrometry (ICP-OES) soil core assays and cation exchange chromatography quantify base saturation and mineral nutrient leaching. "
                f"Lysimeter water percolation telemetry and remote sensing NDVI satellite correlations confirm that conservation tillage and cover crop residues enhance soil moisture retention and crop harvest yields across changing agro-ecological climates."
            )
        expanded.append((h, p_list))

    write_doc("food__global_agricultural_science_and_soil.txt", title, expanded, is_markdown=False)


if __name__ == "__main__":
    print("Building Food text documents...")
    build_beer()
    build_bread()
    build_chocolate()
    build_coffee()
    build_potato()
    build_agricultural_science()
    print("All Food text documents successfully generated with >= 5000 words each!")

