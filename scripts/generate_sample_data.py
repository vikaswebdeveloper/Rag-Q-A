import csv
from pathlib import Path

# Ensure directory exists
data_dir = Path("data")
data_dir.mkdir(parents=True, exist_ok=True)

# 1. History - Apollo 11
(data_dir / "history__apollo_11.txt").write_text(
"""Apollo 11

== Overview ==
Apollo 11 was the American spaceflight that first landed humans on the Moon. Commander Neil Armstrong and Lunar Module Pilot Buzz Aldrin landed the Apollo Lunar Module Eagle on July 20, 1969, at 20:17 UTC. Armstrong became the first person to step onto the lunar surface six hours and 39 minutes later, on July 21 at 02:56 UTC. Aldrin joined him 19 minutes later.

== Mission Details ==
They spent about two and a quarter hours together outside the spacecraft, collecting 47.5 pounds (21.5 kg) of lunar material to bring back to Earth. Command Module Pilot Michael Collins flew the Command Module Columbia alone in lunar orbit while they were on the Moon's surface. Armstrong and Aldrin spent 21 hours, 36 minutes on the lunar surface at a site they named Tranquility Base before lifting off to rejoin Columbia.

== Landing and Return ==
Apollo 11 was launched by a Saturn V rocket from Kennedy Space Center on Merritt Island, Florida, on July 16, 1969. The spacecraft splashed down safely in the Pacific Ocean on July 24 after more than eight days in space. Armstrong's first step was broadcast on live TV to a worldwide audience of at least 650 million viewers.
""",
    encoding="utf-8",
)

# 2. History - Vikings
(data_dir / "history__vikings.txt").write_text(
"""The Vikings

== Origins and Society ==
The Vikings were seafaring Norse people from southern Scandinavia who from the late 8th to late 11th centuries raided, pirated, traded, and settled throughout parts of Europe. They spoke Old Norse and worshipped Norse gods such as Odin, Thor, and Freyja before gradually converting to Christianity.

== Seafaring and Longships ==
The hallmark of Viking mobility was the longship, characterized by a slender and flexible wooden hull, a shallow draft, and symmetrical ends. This design allowed Viking expeditions to navigate deep ocean waters as well as shallow rivers, enabling surprise inland raids across Britain, Ireland, France, and eastern Europe.

== Exploration and Settlements ==
Led by explorers such as Erik the Red and Leif Erikson, the Norse established settlements in Iceland and Greenland, and became the first known Europeans to reach North America at L'Anse aux Meadows in Newfoundland around the year 1000.
""",
    encoding="utf-8",
)

# 3. History - Roman Empire (Markdown)
(data_dir / "history__roman_empire.md").write_text(
"""# The Roman Empire

## From Republic to Empire
The Roman Empire was the post-Republican period of ancient Rome. It began in 27 BC when the Roman Senate granted Octavian the title of Augustus, establishing the Principate. Augustus initiated the Pax Romana, a two-century period of relative internal peace and stability across the Mediterranean basin.

## Architecture and Engineering
Roman engineering produced monumental structures, including aqueducts, amphitheaters, and extensive paved roads. The Colosseum in Rome, completed in 80 AD under Emperor Titus, could hold over 50,000 spectators for gladiatorial contests and public spectacles. Concrete made with pozzolana volcanic ash enabled massive domes like that of the Pantheon.

## Decline and Legacy
In 395 AD, the empire permanently split into the Western Roman Empire and the Eastern Roman (Byzantine) Empire. The Western Empire collapsed in 476 AD when Romulus Augustulus was deposed, while the Eastern Empire persisted until the fall of Constantinople in 1453. Roman law, Latin language roots, and administrative systems remain fundamental to modern Western civilization.
""",
    encoding="utf-8",
)

# 4. History - Industrial Revolution
(data_dir / "history__industrial_revolution.txt").write_text(
"""The Industrial Revolution

== First Industrial Revolution ==
The Industrial Revolution was the transition to new manufacturing processes in Great Britain, continental Europe, and the United States, that occurred during the period from around 1760 to about 1840. It marked a major turning point in history, transitioning from agrarian hand-production methods to machines, new chemical manufacturing, and iron production processes.

== Steam Power and Textiles ==
The development of the Watt steam engine by James Watt in 1776 provided a reliable and flexible source of mechanical power. Powered textile machinery such as the spinning jenny and the power loom dramatically increased production efficiency in British cotton mills, centered in Lancashire.

== Social and Economic Impact ==
Urbanization accelerated as millions of workers migrated from rural villages to factory cities like Manchester and Birmingham. The rise of industrial capitalism led to new social classes, the labor union movement, and extensive legislative reforms regarding child labor and working hours.
""",
    encoding="utf-8",
)

# 5. History - Ancient Egypt
(data_dir / "history__ancient_egypt.txt").write_text(
"""Ancient Egypt

== The Nile and Civilization ==
Ancient Egypt was a civilization of ancient North Africa, concentrated along the lower reaches of the Nile River, situated in the place that is now the country of Egypt. Egyptian civilization coalesced around 3100 BC with the political unification of Upper and Lower Egypt under the first pharaoh, Narmer.

== Monumental Architecture ==
During the Old Kingdom, pharaohs constructed massive pyramid complexes as royal tombs. The Great Pyramid of Giza, built for Pharaoh Khufu around 2560 BC, was the tallest human-made structure in the world for over 3,800 years.

== Culture and Writing ==
The Egyptians developed hieroglyphic script, written on papyrus scrolls and carved onto stone temple walls. Their religious beliefs centered on the afterlife, leading to elaborate mummification practices and the Book of the Dead.
""",
    encoding="utf-8",
)

# 6. Science - DNA (Markdown)
(data_dir / "science__dna.md").write_text(
"""# Deoxyribonucleic Acid

## Structure of the Molecule
Deoxyribonucleic acid (DNA) is a polymer composed of two polynucleotide chains that coil around each other to form a double helix. The structure was discovered in 1953 by James Watson and Francis Crick, building on experimental X-ray diffraction data collected by Rosalind Franklin and Maurice Wilkins.

## Nitrogenous Bases
The information in DNA is stored as a code made up of four chemical bases: adenine (A), guanine (G), cytosine (C), and thymine (T). Under the base pairing rules, adenine always pairs with thymine (A-T) via two hydrogen bonds, and guanine always pairs with cytosine (G-C) via three hydrogen bonds.

## Function in Inheritance
DNA sequences encode instructions for synthesizing proteins through transcription into messenger RNA (mRNA) and translation on ribosomes. When cells divide, DNA replicates with high fidelity, passing genetic instructions from generation to generation.
""",
    encoding="utf-8",
)

# 7. Science - Earthquakes
(data_dir / "science__earthquakes.txt").write_text(
"""Earthquakes

== Causes and Mechanisms ==
An earthquake is the shaking of the surface of the Earth resulting from a sudden release of energy in the Earth's lithosphere that creates seismic waves. Most naturally occurring earthquakes are related to the tectonic nature of the Earth, caused by the sudden rupture of geological faults. The point inside the Earth where the rupture begins is called the hypocenter or focus; the point directly above it on the surface is the epicenter.

== Seismic Waves ==
Seismic waves are recorded by instruments called seismographs. Primary waves (P-waves) are compressional waves that travel fastest through both solids and liquids. Secondary waves (S-waves) are shear waves that arrive second and only propagate through solids. Surface waves arrive last and typically cause the greatest ground shaking and structural damage.

== Measurement and Magnitude ==
The Richter scale was developed in 1935 by Charles F. Richter to quantify the energy released by earthquakes. Today, scientists primarily use the Moment Magnitude Scale (Mw), which measures the seismic moment based on the area of the fault rupture and the average slip distance.
""",
    encoding="utf-8",
)

# 8. Science - Photosynthesis (Markdown)
(data_dir / "science__photosynthesis.md").write_text(
"""# Photosynthesis

## The Light-Driven Reaction
Photosynthesis is a biological process used by plants, algae, and certain bacteria to convert light energy into chemical energy stored in glucose. The overall chemical equation is: 6CO2 + 6H2O + light -> C6H12O6 + 6O2.

## Chloroplasts and Chlorophyll
In green plants, photosynthesis occurs within specialized cellular organelles called chloroplasts. The green pigment chlorophyll absorbs blue and red wavelengths of sunlight while reflecting green light, which gives plant foliage its characteristic color.

## Light and Dark Stages
Photosynthesis occurs in two phases: the light-dependent reactions in the thylakoid membranes, which generate ATP and NADPH while releasing oxygen, and the light-independent Calvin cycle in the stroma, which uses ATP and NADPH to fix carbon dioxide into sugars.
""",
    encoding="utf-8",
)

# 9. Science - Quantum Mechanics
(data_dir / "science__quantum_mechanics.txt").write_text(
"""Quantum Mechanics

== Historical Foundations ==
Quantum mechanics is a fundamental theory in physics that provides a description of the physical properties of nature at the scale of atoms and subatomic particles. It arose in the early 20th century when classical physics failed to explain black-body radiation and the photoelectric effect. In 1900, Max Planck proposed that electromagnetic energy is emitted in discrete packets called quanta.

== Wave-Particle Duality and Uncertainty ==
Louis de Broglie proposed that matter exhibits both wave-like and particle-like characteristics. Werner Heisenberg formulated the Uncertainty Principle in 1927, stating that the position and momentum of a particle cannot both be precisely measured at the same time.

== The Wave Equation ==
Erwin Schrödinger introduced the wave equation in 1926 to describe the quantum state of a physical system. The square of the wave function's amplitude represents the probability density of finding a particle in a given region of space.
""",
    encoding="utf-8",
)

# 10. Science - Solar System
(data_dir / "science__solar_system.txt").write_text(
"""The Solar System

== Composition and Scale ==
The Solar System consists of the Sun and the astronomical objects bound to it by gravity. It formed 4.6 billion years ago from the gravitational collapse of a giant interstellar molecular cloud. The vast majority of the system's mass is in the Sun, with Jupiter holding most of the remaining mass.

== The Eight Planets ==
There are eight recognized planets: four inner terrestrial planets (Mercury, Venus, Earth, Mars) composed primarily of rock and metal, and four outer giant planets (Jupiter, Saturn, Uranus, Neptune). Jupiter and Saturn are gas giants composed mainly of hydrogen and helium, while Uranus and Neptune are ice giants containing water, ammonia, and methane ices.

== Minor Bodies ==
Between Mars and Jupiter lies the asteroid belt. Beyond Neptune lies the Kuiper belt and the scattered disc, populated by dwarf planets like Pluto, Makemake, and Eris, as well as short-period comets.
""",
    encoding="utf-8",
)

# 11. Food - Potato
(data_dir / "food__potato.txt").write_text(
"""The Potato

== Botanical Profile ==
The potato is a starchy root vegetable native to the Americas, a tuber of the plant Solanum tuberosum. The potato belongs to the nightshade family Solanaceae, alongside tomatoes, peppers, and eggplants.

== Origin and Spread ==
Potatoes were first domesticated by indigenous Andean civilizations in the region of modern-day southern Peru and northwestern Bolivia between 8,000 and 5,000 BC. Spanish conquistadors introduced the tuber to Europe in the second half of the 16th century. Initially regarded with suspicion, it became a staple crop by the 18th century, significantly boosting population growth.

== Culinary and Nutritional Value ==
Potatoes are a rich source of carbohydrates, predominantly starch, and provide significant amounts of vitamin C, vitamin B6, and potassium. They are prepared in countless ways, including boiling, baking, mashing, frying, and roasting.
""",
    encoding="utf-8",
)

# 12. Food - Beer (both .txt and .md to test dropCopies duplicate handling!)
(data_dir / "food__beer.txt").write_text(
"""Beer Brewing and Traditions

== Core Ingredients ==
Beer is one of the oldest and most widely consumed alcoholic drinks in the world. Traditional brewing uses four primary ingredients: water, a fermentable starch source (most commonly malted barley), brewer's yeast, and hops for bitterness and aroma.

== The Brewing Process ==
Brewing begins with mashing, where crushed malt is steeped in hot water to activate enzymes that convert starches into fermentable sugars, creating a liquid called wort. The wort is boiled with hops in a kettle, cooled, and aerated before yeast is added to initiate fermentation.

== Ales versus Lagers ==
Beers are broadly categorized into ales and lagers based on yeast strains and fermentation temperature. Ales use top-fermenting Saccharomyces cerevisiae at warmer temperatures (15-24 C), producing fruity esters. Lagers use bottom-fermenting Saccharomyces pastorianus at cooler temperatures (7-13 C), producing crisp, clean flavors.
""",
    encoding="utf-8",
)

(data_dir / "food__beer.md").write_text(
"""# Beer Brewing and Traditions

## Core Ingredients
Beer is one of the oldest and most widely consumed alcoholic drinks in the world. Traditional brewing uses four primary ingredients: water, a fermentable starch source (most commonly malted barley), brewer's yeast, and hops for bitterness and aroma.

## The Brewing Process
Brewing begins with mashing, where crushed malt is steeped in hot water to activate enzymes that convert starches into fermentable sugars, creating a liquid called wort. The wort is boiled with hops in a kettle, cooled, and aerated before yeast is added to initiate fermentation.

## Ales versus Lagers
Beers are broadly categorized into ales and lagers based on yeast strains and fermentation temperature. Ales use top-fermenting Saccharomyces cerevisiae at warmer temperatures (15-24 C), producing fruity esters. Lagers use bottom-fermenting Saccharomyces pastorianus at cooler temperatures (7-13 C), producing crisp, clean flavors.
""",
    encoding="utf-8",
)

# 13. Food - Coffee
(data_dir / "food__coffee.txt").write_text(
"""Coffee

== Cultivation and Varieties ==
Coffee is a beverage brewed from the roasted seeds of Coffea plants, primarily Coffea arabica and Coffea canephora (robusta). Arabica accounts for about 60-70% of world production and offers nuanced aromatic profiles, while robusta provides higher bitterness, body, and caffeine content.

== Origin and Global History ==
Coffee drinking originated in the Sufi monasteries of 15th-century Yemen, using beans imported from the Ethiopian highlands. By the 16th century, coffee houses flourished in Cairo, Istanbul, and Damascus, eventually spreading to Venice, London, and Paris in the 17th century.

== Roasting and Preparation ==
Raw green coffee beans undergo roasting at temperatures between 180 and 240 C, triggering the Maillard reaction and caramelization that develop characteristic aromas. Methods such as espresso, pour-over, French press, and cold brew extract soluble compounds with varying brew ratios and grind sizes.
""",
    encoding="utf-8",
)

# 14. Food - Bread (Markdown)
(data_dir / "food__bread.md").write_text(
"""# The Craft of Bread

## History of Leavened Bread
Bread is one of the oldest human-made foods, dating back more than 14,000 years to Natufian hunter-gatherer sites in Jordan. The earliest leavened breads arose in ancient Egypt, where bakers captured wild airborne yeasts to ferment wet wheat doughs.

## Flour, Gluten, and Fermentation
Wheat flour contains two main proteins, glutenin and gliadin, which bond when mixed with water to form an elastic network called gluten. During fermentation, yeast converts simple carbohydrates into carbon dioxide gas, which gets trapped in the gluten matrix, expanding the loaf.

## Sourdough and Wild Fermentation
Sourdough bread relies on a symbiotic culture of wild yeasts and lactic acid bacteria (LAB). The bacteria produce lactic and acetic acids, giving sourdough its distinct tang and extending shelf life by inhibiting mold growth.
""",
    encoding="utf-8",
)

# 15. Food - Chocolate
(data_dir / "food__chocolate.txt").write_text(
"""Chocolate

== The Cacao Tree ==
Chocolate is prepared from the fruit seeds of Theobroma cacao, an evergreen tree native to the tropical rainforests of Central and South America. The tree produces large pods containing 20 to 50 cacao beans encased in sweet white pulp.

== Mesoamerican Origins ==
The Olmecs and Mayans were the first to cultivate cacao around 1500 BC. They consumed it as a bitter, frothy beverage mixed with chili peppers, water, and cornmeal, considering it a sacred gift from the gods. The Aztecs used cacao beans as currency and served chocolate drinks to nobility and warriors.

== Modern Manufacturing ==
Harvested cacao beans are fermented for five to seven days and sun-dried before roasting. The nibs are ground into chocolate liquor, which can be pressed into cocoa butter and cocoa powder, or conched with sugar and milk to make modern eating chocolate.
""",
    encoding="utf-8",
)

# 16. Health - Caffeine
(data_dir / "health__caffeine.txt").write_text(
"""Caffeine and Human Health

== Pharmacological Action ==
Caffeine is a central nervous system stimulant of the methylxanthine class. It is the world's most widely consumed psychoactive substance. Caffeine acts primarily as an antagonist of adenosine receptors in the brain, blocking adenosine from signaling tiredness and promoting alertness and vigilance.

== Cardiovascular and Metabolic Effects ==
Consumption of moderate caffeine amounts (up to 400 mg per day for healthy adults, equivalent to about four standard cups of brewed coffee) is associated with enhanced cognitive performance, increased metabolic rate, and improved endurance during athletic activity. It can cause transient elevations in blood pressure and heart rate.

== Sleep and Withdrawal ==
Caffeine has a half-life of approximately 5 to 6 hours in healthy adults. Consuming it late in the day can disrupt sleep architecture, reducing slow-wave deep sleep and total sleep duration. Abrupt cessation in habitual consumers often leads to withdrawal symptoms including headache, fatigue, and irritability lasting 2 to 9 days.
""",
    encoding="utf-8",
)

# 17. Health - Sleep Hygiene (Markdown)
(data_dir / "health__sleep_hygiene.md").write_text(
"""# Sleep Hygiene

## The Biological Clock
The human sleep-wake cycle is governed by the circadian rhythm, an internal 24-hour biological clock centered in the suprachiasmatic nucleus (SCN) of the hypothalamus. The SCN synchronizes hormonal releases, body temperature, and alertness based on environmental light exposure.

## Light and Melatonin
Darkness stimulates the pineal gland to synthesize and secrete melatonin, a hormone that promotes drowsiness. Exposure to blue-wavelength light emitted by smartphones, tablets, and LED fixtures late in the evening suppresses melatonin production, delaying sleep onset.

## Environmental and Behavioral Guidelines
Effective sleep hygiene recommendations include maintaining a consistent sleep schedule seven days a week, keeping the bedroom cool (around 18 C / 65 F), dark, and quiet, avoiding large meals and alcohol close to bedtime, and reserving the bed exclusively for sleep and intimacy.
""",
    encoding="utf-8",
)

# 18. Health - Cardiovascular System
(data_dir / "health__cardiovascular_system.txt").write_text(
"""The Cardiovascular System

== Anatomy of the Heart ==
The human heart is a muscular organ located slightly left of the thoracic midline. It contains four chambers: the right atrium and right ventricle, which manage pulmonary circulation, and the left atrium and left ventricle, which power systemic circulation throughout the entire body.

== Vascular Network ==
The vascular system comprises arteries, arterioles, capillaries, venules, and veins. Arteries carry oxygenated blood away from the left ventricle under high pressure, while veins return deoxygenated blood back toward the right atrium under lower pressure, aided by one-way valves.

== Aerobic Exercise and Heart Health ==
Regular aerobic physical activity strengthens the myocardium, enhances ventricular stroke volume, and reduces resting heart rate. Epidemiological studies demonstrate that at least 150 minutes of moderate-intensity aerobic exercise per week lowers the risk of coronary artery disease, stroke, and hypertension.
""",
    encoding="utf-8",
)

# 19. Health - Immune System
(data_dir / "health__immune_system.txt").write_text(
"""The Immune System

== Innate versus Adaptive Immunity ==
The human immune system defends the host against pathogens through two interrelated arms: innate immunity and adaptive immunity. Innate immunity provides immediate, non-specific barrier defenses including skin, mucous membranes, stomach acid, and phagocytes like neutrophils and macrophages.

== Cellular and Humoral Adaptive Response ==
Adaptive immunity develops antigen-specific responses with immunological memory. T lymphocytes mature in the thymus and manage cell-mediated immunity, destroying infected host cells. B lymphocytes develop in the bone marrow and differentiate into plasma cells that produce targeted antibodies (immunoglobulins).

== Vaccination and Herd Immunity ==
Vaccines expose the immune system to harmless antigens (inactivated viruses, protein subunits, or mRNA), stimulating antibody production and memory cell formation without causing full clinical disease. When a high proportion of a population is vaccinated, herd immunity protects individuals who cannot be immunized.
""",
    encoding="utf-8",
)

# 20. Health - Nutrition Basics
(data_dir / "health__nutrition_basics.txt").write_text(
"""Principles of Nutrition

== Macronutrients ==
Human nutrition requires three primary macronutrients to provide metabolic energy: carbohydrates (4 kcal/g), proteins (4 kcal/g), and fats (9 kcal/g). Carbohydrates provide readily accessible glucose; proteins supply essential amino acids for tissue synthesis; and fats support cellular membrane integrity and hormone production.

== Micronutrients ==
Micronutrients include vitamins and dietary minerals required in small quantities for metabolic function. Water-soluble vitamins (B-complex and vitamin C) must be replenished frequently, whereas fat-soluble vitamins (A, D, E, and K) accumulate in liver and adipose tissue. Essential minerals include iron for hemoglobin synthesis and calcium for bone mineralization.

== Dietary Fiber and Water ==
Dietary fiber promotes digestive motility, feeds beneficial gut microbiota, and aids in blood glucose regulation. Adequate water intake (2 to 3 liters per day for typical adults) is essential for cellular homeostasis, thermoregulation, and waste excretion.
""",
    encoding="utf-8",
)

# 21. Geography - Mount Everest
(data_dir / "geography__mount_everest.txt").write_text(
"""Mount Everest

== Geography and Elevation ==
Mount Everest is Earth's highest mountain above sea level, located in the Mahalangur Himal sub-range of the Himalayas. The international border between Nepal and the Tibet Autonomous Region of China runs across its summit point. Its official elevation was remeasured by Nepalese and Chinese authorities in 2020 at 8,848.86 meters (29,031.7 feet).

== First Ascents ==
The first confirmed successful ascent of Mount Everest occurred on May 29, 1953, by Sir Edmund Hillary of New Zealand and Tenzing Norgay, a Sherpa mountaineer of Nepal, climbing the Southeast Ridge route as part of the ninth British Everest expedition led by John Hunt.

== Environmental Conditions and the Death Zone ==
Altitudes above 8,000 meters (26,000 feet) on Everest are known as the Death Zone. At this elevation, atmospheric pressure drops to roughly one-third of sea level value, preventing the human body from acclimatizing and necessitating the use of supplemental bottled oxygen for the vast majority of climbers.
""",
    encoding="utf-8",
)

# 22. Geography - Amazon River (Markdown)
(data_dir / "geography__amazon_river.md").write_text(
"""# The Amazon River

## Discharge and Hydrology
The Amazon River in South America is the largest river by discharge volume of water in the world, responsible for roughly 20 percent of the total riverine discharge into global oceans. Its average discharge is approximately 209,000 cubic meters per second (7,381,000 cu ft/s).

## Basin and Rainforest
The Amazon basin covers approximately 7,000,000 square kilometers (2,700,000 sq mi), spanning Brazil, Peru, Colombia, Bolivia, Ecuador, Venezuela, and Guyana. The basin is blanketed by the Amazon rainforest, the world's largest tropical rainforest, recognized for extraordinary biodiversity housing one in ten known species on Earth.

## Source and Course
The most distant source of the Amazon was confirmed in the Peruvian Andes on the Nevado Mismi peak. The river flows generally eastward across northern South America before emptying through a vast estuary into the Atlantic Ocean.
""",
    encoding="utf-8",
)

# 23. Geography - Sahara Desert
(data_dir / "geography__sahara_desert.txt").write_text(
"""The Sahara Desert

== Extent and Topography ==
The Sahara is the largest hot desert in the world and the third-largest desert overall, smaller only than the cold deserts of Antarctica and the Arctic. It spans approximately 9,200,000 square kilometers (3,600,000 sq mi), encompassing much of North Africa from the Atlantic Ocean to the Red Sea.

== Landscapes: Ergs and Regs ==
Contrary to the popular stereotype of endless sand dunes, sand seas known as ergs cover only about 25 percent of the Sahara. The remainder consists of gravel-strewn plains (regs), bare rocky plateaus (hamadas), and volcanic mountain ranges such as the Tibesti and Ahaggar Mountains.

== Climate and Oases ==
The Sahara experiences a hyper-arid climate with mean annual precipitation under 100 millimeters across most of its interior. Deep aquifers sustain scattered oases, where date palm cultivation and settled communities have existed along trans-Saharan caravan trade routes for millennia.
""",
    encoding="utf-8",
)

# 24. Geography - Great Barrier Reef
(data_dir / "geography__great_barrier_reef.txt").write_text(
"""The Great Barrier Reef

== Physical Extent ==
The Great Barrier Reef is the world's largest coral reef system, composed of over 2,900 individual reefs and 900 islands stretching for over 2,300 kilometers (1,400 miles) over an area of approximately 344,400 square kilometers. The reef is located in the Coral Sea, off the coast of Queensland, Australia.

== Ecological Significance ==
The reef was designated a UNESCO World Heritage Site in 1981. It supports an astonishing diversity of marine life, including 1,500 species of fish, 400 species of hard corals, 4,000 species of mollusks, and six of the world's seven species of marine turtles.

== Conservation and Threats ==
The Great Barrier Reef faces critical environmental challenges from climate-change-induced marine heatwaves, which cause widespread coral bleaching by expelling photosynthetic zooxanthellae from coral tissues. Crown-of-thorns starfish outbreaks and agricultural runoff also impact reef health.
""",
    encoding="utf-8",
)

# 25. Geography - Mariana Trench
(data_dir / "geography__mariana_trench.txt").write_text(
"""The Mariana Trench

== Geological Setting ==
The Mariana Trench is located in the western Pacific Ocean, approximately 200 kilometers east of the Mariana Islands. It is an oceanic trench formed by subduction, where the Pacific Plate is pushed beneath the smaller Mariana Plate. It is the deepest oceanic trench on Earth.

== Challenger Deep ==
The deepest point in the trench, known as the Challenger Deep, reaches a maximum depth of approximately 10,994 meters (36,070 feet) below sea level. At this depth, hydrostatic pressure exceeds 1,086 bar (over 15,700 psi), roughly 1,000 times standard atmospheric pressure at sea level.

== Exploration History ==
The first human descent to the bottom of Challenger Deep was accomplished in January 1960 by Jacques Piccard and Don Walsh inside the bathyscaphe Trieste. In March 2012, Canadian filmmaker James Cameron made the first solo descent in the submersible Deepsea Challenger.
""",
    encoding="utf-8",
)

# 26. Technology - Kubernetes
(data_dir / "technology__kubernetes.txt").write_text(
"""Kubernetes

== Origins and History ==
Kubernetes (often abbreviated as K8s) is an open-source container orchestration platform designed to automate deploying, scaling, and operating application containers. It was originally designed by Google engineers Joe Beda, Brendan Burns, and Craig McLuckie, drawing heavily from Google's internal Borg cluster management system. Kubernetes was first announced by Google in mid-2014 and the v1.0 release was launched on July 21, 2015. Google partnered with the Linux Foundation to form the Cloud Native Computing Foundation (CNCF) and donated Kubernetes as its seed technology.

== Core Architectural Components ==
A Kubernetes cluster consists of control plane nodes and worker nodes. The control plane manages cluster state via the kube-apiserver, etcd (a consistent distributed key-value store), kube-scheduler (assigning pods to nodes), and kube-controller-manager.

== Pods and Workloads ==
The basic execution unit in Kubernetes is a Pod, which encapsulates one or more co-located containers sharing network namespaces and storage volumes. Higher-level controllers like Deployments, StatefulSets, and DaemonSets manage pod replicas, zero-downtime rolling updates, and self-healing.
""",
    encoding="utf-8",
)

# 27. Technology - Internet History (Markdown)
(data_dir / "technology__internet_history.md").write_text(
"""# History of the Internet

## ARPANET and Packet Switching
The foundation of the Internet began in the late 1960s with ARPANET, funded by the US Department of Defense's Advanced Research Projects Agency (DARPA). It pioneered packet switching networks, replacing circuit-switched telephone lines. The first host-to-host message was transmitted between UCLA and Stanford Research Institute on October 29, 1969.

## TCP/IP Standardization
In the 1970s, computer scientists Vinton Cerf and Robert Kahn designed the Transmission Control Protocol (TCP) and Internet Protocol (IP). On January 1, 1983, known as Flag Day, ARPANET formally adopted TCP/IP as its standard communications protocol, establishing the technical foundation of the global Internet.

## The World Wide Web
In 1989, British computer scientist Tim Berners-Lee invented the World Wide Web at CERN to facilitate information sharing among physicists. He authored the first web browser, HTTP protocol, HTML markup language, and URL addressing system, publishing the first website on August 6, 1991.
""",
    encoding="utf-8",
)

# 28. Technology - Python Language
(data_dir / "technology__python_language.txt").write_text(
"""The Python Programming Language

== Inception and Philosophy ==
Python is a high-level, interpreted, general-purpose programming language conceived in the late 1980s by Dutch programmer Guido van Rossum at Centrum Wiskunde & Informatica (CWI) in the Netherlands. It was first released in February 1991. The language philosophy emphasizes code readability, summarized in "The Zen of Python" (PEP 20): "Beautiful is better than ugly. Explicit is better than implicit. Simple is better than complex."

== Type System and Design ==
Python features dynamic typing and automatic reference-counted garbage collection with a cyclic detector. It supports multiple programming paradigms, including structured, object-oriented, and functional programming.

== Growth and Ecosystem ==
Python has achieved widespread popularity across data science, machine learning, web development, and scientific computing. Popular libraries include NumPy, Pandas, PyTorch, TensorFlow, FastAPI, and Django.
""",
    encoding="utf-8",
)

# 29. Technology - Relational Databases
(data_dir / "technology__relational_databases.txt").write_text(
"""Relational Databases

== Codd's Relational Model ==
The relational database model was proposed in 1970 by Edgar F. Codd in his seminal paper "A Relational Model of Data for Large Shared Data Banks". Codd introduced the mathematical foundation of relations (tables), tuples (rows), and attributes (columns), freeing applications from physical storage representations.

== SQL and ACID Properties ==
Structured Query Language (SQL) was developed at IBM by Donald Chamberlin and Raymond Boyce in the early 1970s to manipulate data in relational systems. Relational engines enforce ACID transaction guarantees: Atomicity, Consistency, Isolation, and Durability, ensuring reliability under concurrent workloads and system crashes.

== Prominent Implementations ==
Leading open-source relational database management systems include PostgreSQL and MySQL. PostgreSQL is renowned for standards compliance, extensible types, foreign keys, and complex indexing mechanisms.
""",
    encoding="utf-8",
)

# 30. Technology - Artificial Intelligence (Markdown)
(data_dir / "technology__artificial_intelligence.md").write_text(
"""# Artificial Intelligence

## The Dartmouth Workshop
The field of Artificial Intelligence (AI) was formally founded as an academic discipline at the Dartmouth Summer Research Project on Artificial Intelligence in 1956, organized by John McCarthy, Marvin Minsky, Nathaniel Rochester, and Claude Shannon. McCarthy coined the term "artificial intelligence" in the conference proposal.

## AI Winters and Resurgence
The discipline endured several cycles of optimism followed by funding cuts, known as "AI winters," notably in the mid-1970s and late 1980s when early symbolic systems failed to scale to real-world ambiguity. Resurgence occurred in the 2010s driven by deep learning, graphical processing units (GPUs), and vast training datasets.

## Modern Large Language Models
Recent breakthroughs in deep learning stem from the Transformer architecture introduced by Vaswani et al. in 2017. Transformers leverage self-attention mechanisms to process sequential textual data in parallel, powering modern large language models capable of comprehension, code synthesis, and reasoning.
""",
    encoding="utf-8",
)

# 31. General - Dewey Decimal System
(data_dir / "general__dewey_decimal_system.txt").write_text(
"""The Dewey Decimal Classification

== Creation by Melvil Dewey ==
The Dewey Decimal Classification (DDC) is a proprietary library classification system first published in the United States by Melvil Dewey in 1876. Dewey introduced relative location and relative index concepts, allowing new books to be inserted into a library collection according to subject matter rather than fixed shelf locations.

== Ten Main Classes ==
The DDC organizes human knowledge into ten broad classes, numbered 000 through 900:
000 - Computer science, information & general works
100 - Philosophy & psychology
200 - Religion
300 - Social sciences
400 - Language
500 - Pure science
600 - Technology & applied science
700 - Arts & recreation
800 - Literature
900 - History & geography

== Notation and Hierarchy ==
Each class is subdivided into ten divisions, and each division into ten sections. Decimal points are introduced after three digits to allow endless hierarchical expansion for specialized subjects.
""",
    encoding="utf-8",
)

# 32. General - Printing Press
(data_dir / "general__printing_press.txt").write_text(
"""The Printing Press

== Gutenberg's Invention ==
Around 1440 in Mainz, Germany, goldsmith Johannes Gutenberg invented the mechanical movable-type printing press. His innovation integrated durable lead-tin alloy type pieces, an oil-based printing ink, and an adjustable wooden screw press adapted from agricultural wine presses.

== The Gutenberg Bible ==
Gutenberg's major masterpiece was the 42-Line Bible, completed around 1455. Printed in Latin with Gothic blackletter script, approximately 180 copies were produced on paper and fine calfskin vellum, admired for their typographic consistency and artistic layout.

== Socio-Cultural Revolution ==
The rapid spread of printing presses across Europe catalyzed the Printing Revolution, drastically lowering the cost of books, expanding literacy beyond ecclesiastical elites, and accelerating the spread of the Protestant Reformation and the Scientific Revolution.
""",
    encoding="utf-8",
)

# 33. General - Library of Alexandria (Markdown)
(data_dir / "general__library_of_alexandria.md").write_text(
"""# The Great Library of Alexandria

## Founding and Vision
The Great Library of Alexandria in Egypt was one of the largest and most significant libraries of the ancient world. Established under the patronage of the Ptolemaic dynasty in the 3rd century BC, probably initiated by Ptolemy I Soter or his son Ptolemy II Philadelphus, it was conceived as an ambitious universal research center intended to house all recorded human knowledge.

## The Mouseion and Scholars
The library formed part of a larger research institution called the Mouseion (Shrine of the Muses). Renowned scholars worked there, including Eratosthenes, who calculated the Earth's circumference, Callimachus, who compiled the first comprehensive catalog (Pinakes), and Euclid, who codified geometry.

## Destruction and Dispersal
The decline of the Library of Alexandria was gradual rather than a single cataclysmic fire. Parts were damaged during Julius Caesar's siege in 48 BC, again during Aurelian's recapture of Alexandria in the 270s AD, and under decree by Coptic Pope Theophilus in 391 AD.
""",
    encoding="utf-8",
)

# 34. Food - CSV Table
csv_path = data_dir / "food__nutritional_data.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Food Item", "Serving Size", "Calories", "Protein (g)", "Carbohydrates (g)", "Fat (g)", "Fiber (g)"])
    items = [
        ["Apple", "100g", 52, 0.3, 14.0, 0.2, 2.4],
        ["Banana", "100g", 89, 1.1, 23.0, 0.3, 2.6],
        ["Broccoli", "100g", 34, 2.8, 7.0, 0.4, 2.6],
        ["Chicken Breast", "100g", 165, 31.0, 0.0, 3.6, 0.0],
        ["Egg", "1 large (50g)", 72, 6.3, 0.4, 4.8, 0.0],
        ["Oatmeal", "100g cooked", 71, 2.5, 12.0, 1.5, 1.7],
        ["Salmon", "100g", 208, 20.0, 0.0, 13.0, 0.0],
        ["Almonds", "28g (1 oz)", 164, 6.0, 6.1, 14.2, 3.5],
        ["Brown Rice", "100g cooked", 112, 2.6, 24.0, 0.9, 1.8],
        ["Greek Yogurt", "100g", 59, 10.0, 3.6, 0.4, 0.0],
        ["Spinach", "100g", 23, 2.9, 3.6, 0.4, 2.2],
        ["Sweet Potato", "100g", 86, 1.6, 20.0, 0.1, 3.0],
    ]
    for row in items:
        writer.writerow(row)

# 35. Science - Excel Table (.xlsx)
import openpyxl
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Elements"
ws.append(["Atomic Number", "Element", "Symbol", "Atomic Mass", "Standard State", "Melting Point (K)"])
elements = [
    [1, "Hydrogen", "H", 1.008, "Gas", 14.01],
    [2, "Helium", "He", 4.0026, "Gas", 0.95],
    [6, "Carbon", "C", 12.011, "Solid", 3823.0],
    [7, "Nitrogen", "N", 14.007, "Gas", 63.15],
    [8, "Oxygen", "O", 15.999, "Gas", 54.36],
    [11, "Sodium", "Na", 22.990, "Solid", 370.87],
    [12, "Magnesium", "Mg", 24.305, "Solid", 923.0],
    [13, "Aluminum", "Al", 26.982, "Solid", 933.47],
    [14, "Silicon", "Si", 28.085, "Solid", 1687.0],
    [26, "Iron", "Fe", 55.845, "Solid", 1811.0],
    [29, "Copper", "Cu", 63.546, "Solid", 1357.77],
    [79, "Gold", "Au", 196.97, "Solid", 1337.33],
]
for elem in elements:
    ws.append(elem)
wb.save(data_dir / "science__chemical_elements.xlsx")

# 36. Technology - PowerPoint Presentation (.pptx)
from pptx import Presentation
prs = Presentation()
prs.core_properties.title = "Cloud Computing Architecture"

slide_layout = prs.slide_layouts[0]
slide1 = prs.slides.add_slide(slide_layout)
slide1.shapes.title.text = "Cloud Computing Models"
slide1.placeholders[1].text = "An Introduction to IaaS, PaaS, and SaaS Architectures."

slide_layout1 = prs.slide_layouts[1]
slide2 = prs.slides.add_slide(slide_layout1)
slide2.shapes.title.text = "Service Models"
slide2.placeholders[1].text = "Infrastructure as a Service (IaaS): Virtualized computing resources over the internet.\nPlatform as a Service (PaaS): Hardware and software tools over the internet.\nSoftware as a Service (SaaS): Complete software applications accessible via web browsers."

prs.save(data_dir / "technology__cloud_computing.pptx")

# 37. Health - Word Document (.docx)
import docx
doc = docx.Document()
doc.add_heading("Medical Terminology Guide", level=0)
doc.add_heading("Basic Prefixes and Roots", level=1)
doc.add_paragraph("Cardio refers to the heart, while neuro relates to nerves and the nervous system.")
doc.add_paragraph("Hepato refers to the liver, and nephro pertains to the kidneys.")
doc.add_heading("Diagnostic Procedures", level=1)
doc.add_paragraph("Electrocardiogram (ECG or EKG) records the electrical signals in the heart to detect heart conditions.")
doc.add_paragraph("Magnetic Resonance Imaging (MRI) uses a magnetic field and computer-generated radio waves to create detailed images of organs.")
doc.save(data_dir / "health__medical_terms.docx")

print(f"Generated {len(list(data_dir.iterdir()))} documents in {data_dir}.")

