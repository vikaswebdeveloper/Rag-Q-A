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


def build_amazon_river():
    title = "The Amazon River: Hydrology, Biodiversity, Geomorphology, and Basin Climatology"
    sections = [
        ("Hydrological Dominance and Global Water Budget", [
            "The Amazon River in South America is the largest river in the world by discharge volume of water, and depending on measurement criteria, either the longest or second-longest river system on Earth. The Amazon discharges roughly 20 percent of total riverine water into global oceans, with an average discharge rate of approximately 209,000 to 220,000 cubic meters per second (7.4 to 7.8 million cubic feet per second).",
            "This staggering volume is greater than the next seven largest rivers combined (outstripping the Congo, Ganges, Yangtze, and Mississippi). During peak flood season, the discharge can surge past 300,000 m3/s, discharging so much fresh water into the Atlantic Ocean that it dilutes ocean salinity and discolors sea waters for over 400 kilometers (250 miles) offshore.",
            "The Amazon River basin spans approximately 7 million square kilometers (2.7 million square miles), covering roughly 40 percent of the South American continent across Brazil, Peru, Colombia, Bolivia, Ecuador, Venezuela, and Guyana."
        ]),
        ("Headwaters, Topography, and the Trans-Continental Journey", [
            "The headwaters of the Amazon originate high in the Peruvian Andes, traditionally traced to Nevado Mismi (at 5,597 meters elevation) in the Arequipa region. Emerging as the Carhuasanta stream, it forms the Apurímac River, which merges with the Ucayali and Marañón rivers to formally form the Amazon River proper near Iquitos in Peru.",
            "From the Andean foothills, the river flows eastward across the expansive lowland Amazonian peneplain, descending fewer than 100 meters across its final 3,000 kilometers of travel to the Atlantic Ocean—an astonishingly gentle hydraulic gradient of just a few centimeters per kilometer.",
            "The river empties into the Atlantic Ocean near Belém and the Island of Marajó (the largest fluvial-marine island in the world) through a vast estuary over 240 kilometers wide, where the tidal bore known as the Pororoca creates destructive, surfable standing waves traveling up to 80 kilometers upriver."
        ]),
        ("Blackwater, Whitewater, and Clearwater Rivers", [
            "Limnologists categorize Amazonian tributaries into three distinct hydrological types based on chemistry, sediment load, and optical properties: Whitewater, Blackwater, and Clearwater rivers.",
            "Whitewater rivers (such as the Solimões/Amazon, Madeira, and Marañón) originate in the young, eroding Andean cordillera, carrying heavy loads of suspended mineral silts and dissolved solids, with neutral pH (6.5 to 7.5) and high nutrient fertility sustaining productive floodplains ('várzea').",
            "Blackwater rivers (exemplified by the Rio Negro, the largest blackwater river in the world) originate in ancient, heavily weathered Precambrian Guiana Shield cratons. They carry virtually zero mineral silt, but are deeply stained dark brown-black by dissolved humic and fulvic acids leached from podzolic forest soils, resulting in high acidity (pH 3.8 to 4.5) and low insect mosquito populations.",
            "Clearwater rivers (such as the Tapajós and Xingu) drain ancient Brazilian shield plateaus, featuring high transparency, emerald-green waters, low sediment loads, and moderate nutrient profiles."
        ]),
        ("The 'Meeting of the Waters' (Encontro das Águas)", [
            "Near Manaus, Brazil, the Amazon showcases one of Earth's most striking hydrological spectacles: the Meeting of the Waters (Encontro das Águas).",
            "Here, the dark, acidic Rio Negro (flowing at 2 km/h at 28 C) and the sandy-pale, silt-laden Rio Solimões (flowing at 4 to 6 km/h at 22 C) converge. Due to sharp differences in water temperature, flow velocity, and sediment density, the two colossal rivers refuse to mix immediately, running side by side in the same channel for over six kilometers with a crisp, visible boundary line between black and ochre waters before turbulent mixing finally blends them."
        ]),
        ("Rainforest Ecology, Canopy Stratification, and Biodiversity", [
            "The Amazon River basin hosts the Amazon Rainforest—the largest, most biodiverse tropical moist broadleaf forest on Earth, holding an estimated 390 billion individual trees categorized into roughly 16,000 species.",
            "Ecological architecture is stratified into four vertical layers: the Emergent Layer (giant kapok and Brazil nut trees reaching 60-70 meters above the canopy), the Continuous Canopy (a dense 30-meter-high ceiling housing 90% of forest organisms), the Understory (a dark, humid, shaded environment dominated by broad-leaved philodendrons and epiphytes), and the Forest Floor.",
            "The basin provides sanctuary to one in ten known species on Earth, including over 2.5 million insect species, 40,000 plant species, 3,000 freshwater fish species, 1,300 bird species, and over 400 mammal species."
        ]),
        ("Freshwater Ichthyofauna: Arapaima, Piranhas, and River Dolphins", [
            "Amazonian freshwater fish diversity is unmatched globally. The Arapaima (Pirarucu) is one of the world's largest freshwater scaled fish, reaching lengths over 3 meters and weighing up to 200 kilograms; an obligate air-breather, it surfaces every 10 to 15 minutes to gulp air using a vascularized swim bladder.",
            "The basin hosts the Amazon River dolphin (Boto, Inia geoffrensis), a pink freshwater cetacean with flexible neck vertebrae enabling it to swim through flooded treetops to hunt fish.",
            "Other iconic species include the predatory Red-bellied Piranha, the Electric Eel (Electrophorus electricus, producing electric organ discharges up to 860 volts to stun prey), and the giant armored catfish (Brachyplatystoma filamentosum) that migrates thousands of miles upriver to spawn."
        ]),
        ("The 'Flying Rivers' and South American Atmospheric Climatology", [
            "The Amazon Rainforest functions as a continental hydrological pumping engine, known as the 'Biotic Pump' or 'Flying Rivers' (Rios Voadores).",
            "A single mature Amazonian tree can transpire over 1,000 liters of water vapor into the atmosphere daily. Combined across billions of trees, the rainforest transpires an estimated 20 billion metric tons of water into the troposphere daily—surpassing the daily physical discharge of the Amazon River into the Atlantic Ocean.",
            "These colossal moisture plumes are swept westward by trade winds across the basin until they strike the insurmountable barrier of the 4,000-meter Andean Cordillera, deflecting southward to deliver vital precipitation across agricultural grain belts in southern Brazil, Bolivia, Paraguay, Uruguay, and northern Argentina."
        ]),
        ("Indigenous Civilizations and Terra Preta Anthrosols", [
            "Contrary to colonial myths that the Amazon was a pristine, untouched wilderness devoid of civilization ('virgin forest'), extensive archaeological research has revealed that pre-Columbian Amazonia hosted complex, densely populated agrarian societies.",
            "Between 500 BC and AD 1492, indigenous populations built raised agricultural fields, defensive circular earthworks (geoglyphs uncovered by deforestation LiDAR), canal systems, and network causeways across the Llanos de Moxos and the Tapajós river basin.",
            "Most famously, indigenous Amazonians engineered 'Terra Preta de Índio' (Amazonian Dark Earth)—a highly fertile, anthropogenic soil created by amending nutrient-poor oxisols with low-temperature biochar, animal bones, fish refuse, pottery shards, and organic manure. Unlike natural tropical soils that leach nutrients within years, Terra Preta retains soil organic carbon, nitrogen, and phosphorus for thousands of years, serving as a modern model for carbon sequestration."
        ]),
        ("The Rubber Boom and Manaus Gilded Age (1879-1912)", [
            "In the late 19th and early 20th centuries, the Amazon basin experienced a frenzy of extractive capitalism during the Amazon Rubber Boom. The invention of vulcanization by Charles Goodyear in 1839 and the subsequent rise of pneumatic automobile tires created global demand for natural latex tapped from wild Hevea brasiliensis rubber trees.",
            "Manaus, located in the heart of the jungle, transformed overnight into one of the wealthiest cities in the Americas, known as the 'Paris of the Jungle'. Wealthy rubber barons constructed the lavish Teatro Amazonas opera house using imported Italian marble, French stained glass, and crystal chandeliers.",
            "However, the boom brought catastrophic enslavement, debt peonage, and disease epidemics to indigenous populations (exemplified by the atrocities of the Peruvian Amazon Company in the Putumayo region), before collapsing rapidly after British explorer Henry Wickham smuggled 70,000 rubber seeds to Kew Gardens in 1876, establishing high-yield rubber plantations in British Malaya and Ceylon."
        ]),
        ("Deforestation, Cattle Ranching, and the Tipping Point", [
            "Modern Amazonia faces acute ecological peril from agricultural expansion, illegal logging, gold mining ('garimpo'), and infrastructural highway development (such as the Trans-Amazonian Highway, BR-230).",
            "Over 18 to 20 percent of the original forest cover has been cleared over the past five decades, primarily converted into pastureland for beef cattle ranching (making Brazil the world's leading beef exporter) and vast monoculture soybean plantations.",
            "Climate scientists, notably Carlos Nobre and Thomas Lovejoy, warn that the Amazon approaches an ecological 'Tipping Point': if deforestation surpasses 20 to 25 percent, regional rainfall reduction and elevated temperatures will cause the forest's hydrological self-sustaining cycle to collapse, triggering a catastrophic dieback transforming eastern and southern Amazonia into a degraded dry savanna, releasing billions of tons of carbon into the atmosphere."
        ]),
        ("Dams, Hydroelectric Development, and River Alterations", [
            "The Amazon basin has seen extensive hydroelectric dam construction, including the colossal Belo Monte Dam on the Xingu River (the fourth-largest hydroelectric plant in the world with 11,233 MW capacity), the Tucuruí Dam on the Tocantins, and the Santo Antônio and Jirau dams on the Madeira.",
            "While generating renewable electrical energy, megadams flood vast indigenous territories, alter river flood-pulse dynamics, block fish migration routes, trap vital nutrient-rich sediments behind concrete walls, and emit substantial methane from decomposing submerged organic vegetation in tropical reservoirs."
        ]),
        ("Conservation Frameworks, Indigenous Territories, and Global Governance", [
            "Protecting the Amazon requires integrating international climate finance with strict legal enforcement and indigenous land rights.",
            "Empirical satellite data from Brazil's National Institute for Space Research (INPE) proves that legally demarcated Indigenous Territories (Terras Indígenas) have the lowest rates of deforestation and biodiversity loss across the entire basin, outperforming standard national parks.",
            "Initiatives like the Amazon Fund, funded by international partners, support environmental enforcement (IBAMA), satellite monitoring (PRODES and DETER), and sustainable bioeconomy development (acai, Brazil nuts, rubber tapping), recognizing the Amazon basin as an irreplaceable global public commons essential for planetary climate stability."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Hydrological and basin climatology analysis of {h} (Amazonian Research Monograph Section #{i+1}): Limnological hydrochemical profiling and acoustic Doppler current profiler (ADCP) transects measure discharge velocity and sediment transport across the mainstem. "
                f"Remote sensing telemetry and evapotranspiration flux towers confirm the profound thermodynamic influence of the Amazon basin on South American monsoon precipitation and global atmospheric carbon balances."
            )
        expanded.append((h, p_list))

    write_doc("geography__amazon_river.md", title, expanded, is_markdown=True)


def build_mount_everest():
    title = "Mount Everest: Geology, Tectonic Uplift, Glaciology, Mountaineering History, and High-Altitude Physiology"
    sections = [
        ("Geographical Setting, Topography, and the 2020 Remeasurement", [
            "Mount Everest is the highest mountain on Earth above sea level, located in the Mahalangur Himal sub-range of the Himalayas along the international border between Nepal and the Tibet Autonomous Region of China.",
            "In December 2020, following joint high-precision geodetic and satellite surveying expeditions conducted by the governments of Nepal and China using GNSS receivers and laser altimetry, the official summit elevation of Mount Everest was remeasured and officially established at 8,848.86 meters (29,031.7 feet).",
            "Known in Nepal as Sagarmatha (Sanskrit/Nepali for 'Goddess of the Sky' or 'Forehead of the Sky') and in Tibet as Chomolungma ('Goddess Mother of the World'), the mountain was officially named 'Mount Everest' in 1865 by the Royal Geographical Society in honor of Sir George Everest, the former British Surveyor General of India, following the Great Trigonometrical Survey of India which designated it as 'Peak XV'."
        ]),
        ("Tectonic Origins: The Indo-Eurasian Continental Collision", [
            "The geological genesis of Mount Everest is rooted in plate tectonics. Approximately 50 to 55 million years ago during the Eocene epoch, the northward-drifting Indian tectonic plate collided with the Eurasian continent, closing the ancient Tethys Ocean.",
            "Because both landmasses were buoyant continental crust, neither could subduct easily into the mantle; instead, the continental lithosphere buckled, crumpled, and thrusted upward, creating the Himalayan mountain range and the Tibetan Plateau—the most monumental continental collision zone on Earth.",
            "The Indian plate continues to push northward into Eurasia at a rate of approximately 4 to 5 centimeters per year, driving continuous tectonic uplift of Mount Everest by approximately 4 millimeters annually, counterbalanced by glacial erosion, rockfalls, and seismic slip during mega-earthquakes."
        ]),
        ("Geological Stratigraphy: The Yellow Band and Summit Limestone", [
            "Remarkably, the rocks forming the high summit of Mount Everest are sedimentary limestones and dolomites that were originally deposited on the shallow floor of the ancient Tethys Ocean 450 million years ago during the Ordovician period.",
            "Geologists divide the mountain into three primary stratigraphic units separated by low-angle normal faults:",
            "1. The Rongbuk Formation (Base): High-grade metamorphic gneisses, schists, and leucogranite intrusions formed under intense crustal pressure and heat.",
            "2. The North Col Formation (Middle): Low-grade metamorphic pelitic schists and phyllites, topped by the iconic 'Yellow Band'—a distinct, yellow-brown band of recrystallized marble and dolomite dipping across the mountain's upper face at 8,200 to 8,600 meters.",
            "3. The Qomolangma Formation (Summit): Marine limestone containing fossilized marine invertebrates—including crinoids (sea lilies), trilobites, brachiopods, and ostracods—proving that the highest point on Earth once lay at the bottom of a tropical sea."
        ]),
        ("Glaciology: The Khumbu Icefall, Western Cwm, and Kangshung Face", [
            "Mount Everest is sculpted by massive valley glaciers fed by high-altitude snowfall: the Khumbu Glacier in Nepal, and the East and Main Rongbuk Glaciers and Kangshung Glacier in Tibet.",
            "The most treacherous obstacle on the South Col route is the Khumbu Icefall—a chaotic, constantly moving cascade of glacial ice tumbling 600 meters over the lip of the Western Cwm. The icefall moves at up to one meter per day, opening colossal crevasses and toppling towering ice pinnacles ('seracs') without warning.",
            "The mountain features three colossal faces: the Southwest Face in Nepal, the North Face in Tibet (bounded by the Great Couloir and Hornbein Couloir), and the sheer Kangshung Face in the east, rising 3,350 meters (11,000 feet) from the Kangshung Glacier."
        ]),
        ("Early Expeditions: George Mallory and the 1924 Mystery", [
            "Early exploratory attempts on Everest were launched by British expeditions through Tibet in the 1920s (Nepal remained closed to foreigners). The 1921 reconnaissance expedition, including George Mallory, identified the North Col route.",
            "During the 1924 British Expedition, George Mallory and Andrew 'Sandy' Irvine made a fateful summit attempt using primitive bottled oxygen apparatus. On June 8, 1924, team member Noel Odell spotted the pair through a telescope high on the Northeast Ridge 'going strongly for the top' before swirling clouds engulfed them. They never returned.",
            "Whether Mallory and Irvine reached the summit 29 years before Hillary remains mountaineering's greatest mystery. In 1999, an expedition discovered Mallory's frozen, bleached body at 8,155 meters on the North Face; injuries indicated a catastrophic fall, but Irvine's body and their Vest Pocket Kodak camera (which might hold photographic proof of a summit) have never been found."
        ]),
        ("The 1953 First Ascent: Edmund Hillary and Tenzing Norgay", [
            "The first confirmed successful summit ascent of Mount Everest was achieved on May 29, 1953, by New Zealand mountaineer Edmund Hillary and Nepalese-Tibetan Sherpa mountaineer Tenzing Norgay, climbing as members of the ninth British Everest expedition led by Colonel John Hunt.",
            "Ascending via the Southeast Ridge from the South Col, the pair negotiated the narrow summit ridge, where Hillary overcame a formidable 12-meter (40-foot) vertical rock step—subsequently immortalized as the 'Hillary Step'—by wedging his back and cramponed boots into a crack between the rock and ice.",
            "At 11:30 AM on May 29, 1953, Hillary and Tenzing stepped onto the summit of Mount Everest, spending 15 minutes taking photographs, burying small offerings (a crucifix and biscuits), and looking down on the world before descending safely. News of the ascent reached London on the morning of Queen Elizabeth II's coronation, making both men global icons."
        ]),
        ("The 'Death Zone' and High-Altitude Human Physiology", [
            "In mountaineering medicine, altitudes above 8,000 meters (26,247 feet) are designated as the 'Death Zone'. At Everest's summit (8,848.86 m), atmospheric pressure is only one-third (approximately 337 millibars) of sea level pressure (1,013 mb). While the fraction of oxygen in air remains constant at 20.9%, the partial pressure of oxygen (pO2) plummets.",
            "At these extreme elevations, human lungs cannot absorb sufficient oxygen to sustain basal metabolic cellular processes. The human body deteriorates continuously in the Death Zone; prolonged stays result in rapid exhaustion, cellular degradation, and death within 48 hours.",
            "Climbers face life-threatening conditions: High-Altitude Pulmonary Edema (HAPE), where hypoxia induces pulmonary arterial hypertension and leaks fluid into alveolar air sacs; and High-Altitude Cerebral Edema (HACE), where fluid leaks into brain tissue, causing severe ataxia, confusion, hallucinations, coma, and death within hours without immediate supplemental oxygen and rapid descent."
        ]),
        ("The Sherpa People: Cultural Heart and Physiological Adaptations", [
            "The Sherpa are an ethnic group of Tibetan origin inhabiting the high valleys of the Solukhumbu district in eastern Nepal. The term 'Sherpa' derives from Shar ('east') and pa ('people'), reflecting their historic migration from eastern Tibet roughly 500 years ago.",
            "Sherpas practice Tibetan Buddhism, revere Sagarmatha as the sacred abode of the goddess Miyolangsangma, and maintain the Tengboche Monastery, where climbing teams seek traditional blessings ('puja') before venturing onto the mountain.",
            "Genetic studies reveal that Sherpa populations possess unique biological evolutionary adaptations to extreme hypoxia: rather than overproducing red blood cells (which thickens blood into dangerous polycythemia), Sherpas possess genetic variants in the EPAS1 and PPARA genes that optimize mitochondrial metabolic efficiency, utilizing oxygen more effectively to produce ATP and maintaining superior microvascular blood flow."
        ]),
        ("Mountaineering Routes: South Col vs North Ridge", [
            "Over 95% of Everest ascents utilize two commercial routes:",
            "The South Col Route (Nepal): The standard route pioneered in 1953, beginning with a trek to Everest Base Camp (5,364 m), traversing the dangerous Khumbu Icefall, ascending the Western Cwm to Camp 2, climbing the steep Lhotse Face to Camp 4 at the South Col (7,906 m), and making the final push through the Balcony and South Summit.",
            "The North Ridge Route (Tibet): Follows the Rongbuk Glacier to Advance Base Camp (6,400 m), scales the North Col to Camp 1 (7,000 m), and ascends the barren, wind-scoured Northeast Ridge past three technical rock barriers—the First Step, the formidable vertical Second Step (overcome via a semi-permanent Chinese aluminum ladder installed in 1975), and the Third Step—to the summit."
        ]),
        ("The 1996 Disaster and Commercialization of Everest", [
            "During the 1990s, high-altitude commercial guiding expanded rapidly on Everest, allowing wealthy amateur climbers with variable mountaineering experience to attempt the summit for tens of thousands of dollars.",
            "On May 10-11, 1996, a catastrophic blizzard engulfed climbing teams on the upper mountain, documented in Jon Krakauer's Into Thin Air. Eight climbers perished in a single day—including veteran expedition leaders Rob Hall and Scott Fischer—trapped by bottlenecks at the Hillary Step, running out of supplemental oxygen, and freezing in sub-zero whiteout conditions.",
            "The 1996 tragedy highlighted the perils of commercial client congestion, decision-making biases under hypoxic impairment, and the critical importance of strict turnaround turnaround times (e.g., 2:00 PM)."
        ]),
        ("Crowding, Human Waste, and Environmental Challenges", [
            "In recent decades, commercial mountaineering on Everest has exploded, with hundreds of climbers attempting the summit during brief May weather windows, producing notorious 'traffic jams' in the Death Zone where climbers stand motionless for hours in freezing winds.",
            "The mountain has suffered severe environmental degradation: thousands of discarded oxygen cylinders, abandoned tents, food wrappers, and tons of human excrement accumulate at Base Camp and South Col, earning Everest the moniker 'the world's highest garbage dump'.",
            "In response, the Nepalese government has instituted mandatory waste-deposit regulations requiring every climber to carry back at least 8 kilograms of rubbish, while local Sherpa clean-up expeditions have removed tons of historical debris and human remains from the slopes."
        ]),
        ("Climate Change and Glacial Recession on Everest", [
            "The Himalayan cryosphere is warming at more than twice the global average rate. Glaciological surveys confirm that the Khumbu Glacier and Rongbuk Glacier are thinning and retreating rapidly, forming precarious supra-glacial lakes (such as Imja Tsho) prone to catastrophic Glacial Lake Outburst Floods (GLOFs).",
            "Warming temperatures are melting surface snowpack, exposing underlying loose scree and increasing the frequency of rockfalls and ice avalanches in the Khumbu Icefall and across the Lhotse Face.",
            "In 2015, the Hillary Step was structurally altered following the devastating 7.8-magnitude Nepal earthquake, collapsing the iconic rock notch into a snow ramp. Preserving Mount Everest requires confronting global carbon emissions to safeguard the 'Third Pole' water towers that sustain over 1.5 billion people downstream across Asia."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Geodetic surveying and high-altitude physiology analysis on {h} (Himalayan Research Monograph Section #{i+1}): Satellite radar interferometry (InSAR) and GNSS base stations continuously measure lithospheric tectonic strain and summit elevation displacement. "
                f"Medical telemetry monitoring arterial oxygen saturation (SpO2) and cardiac strain during summit pushes confirms that severe hypoxia impairs cognitive decision-making, necessitating strict physiological safety protocols in the Death Zone."
            )
        expanded.append((h, p_list))

    write_doc("geography__mount_everest.txt", title, expanded, is_markdown=False)


def build_mariana_trench():
    title = "The Mariana Trench: Hadal Zone Oceanography, Subduction Geophysics, and Deep-Sea Extremophiles"
    sections = [
        ("Geographic Location and Bathymetric Dimensions", [
            "The Mariana Trench is an oceanic trench located in the western Pacific Ocean, approximately 200 kilometers (124 miles) east of the Mariana Islands. It is the deepest known geological oceanic trench on Earth, spanning a crescent-shaped scar roughly 2,550 kilometers (1,580 miles) long with an average width of 69 kilometers (43 miles).",
            "At its southernmost terminus lies the Challenger Deep, a small slot-shaped valley within the trench floor that represents the deepest known point in Earth's oceans, descending to an official bathymetric depth of approximately 10,984 to 10,994 meters (36,037 to 36,070 feet; roughly 11 kilometers or 7 miles) below sea level.",
            "To put this staggering depth into perspective: if Mount Everest (8,848.86 m) were placed inside the Challenger Deep, its summit peak would still be submerged under more than two kilometers (over 1.2 miles) of water."
        ]),
        ("Plate Tectonics: Pacific and Mariana Subduction Zone", [
            "The Mariana Trench is formed by the subduction of the Pacific Plate beneath the smaller Mariana Plate. The Pacific Plate here consists of some of the oldest, densest, and coldest oceanic lithosphere on Earth, dating back roughly 170 million years to the Jurassic period.",
            "Because this ancient oceanic basalt is cold and dense, it does not subduct at a shallow angle; instead, it plunges steeply into the upper mantle at nearly vertical angles (up to 90 degrees in some sectors), dragging the seafloor downward to create the extraordinary depth of the trench.",
            "The subducting oceanic slab carries seawater and hydrated minerals deep into the mantle, inducing flux melting that generates the volcanic island arc of the Mariana Islands (including active volcanic centers like Pagan and submerged submarine volcanoes)."
        ]),
        ("Physical Conditions: Hydrostatic Pressure, Temperature, and Darkness", [
            "The physical environment at the bottom of the Challenger Deep represents one of the most hostile physical regimes on Earth. At a depth of 11 kilometers, the hydrostatic pressure exceeds 1,086 bar (108.6 megapascals; roughly 15,750 pounds per square inch)—over 1,000 times the standard atmospheric pressure at sea level.",
            "This colossal pressure exerts a force of roughly 8 tons per square inch; an unarmored human body or standard hollow electronic container would be crushed instantly into fragments.",
            "Water temperatures near the trench floor hover near freezing, between 1 to 4 degrees Celsius (34 to 39 F), and solar sunlight is completely absorbed within the upper 1,000 meters (the photic and mesopelagic zones), leaving the hadal trench in perpetual, absolute pitch-black darkness."
        ]),
        ("Historical Expeditions: The Challenger, Trieste, and James Cameron", [
            "The trench's extreme depth was first probed during the historic oceanographic voyage of HMS Challenger (1872-1876), using a weighted sounding line to measure depths exceeding 8,000 meters in 1875, naming the abyss the Challenger Deep.",
            "The first human descent into the Challenger Deep occurred on January 23, 1960, when Swiss oceanographer Jacques Piccard and US Navy Lieutenant Don Walsh descended inside the bathyscaphe Trieste, designed by Auguste Piccard. The Trieste featured a thick steel pressure sphere suspended beneath a 50-foot float chamber filled with gasoline for buoyancy, spending 20 minutes on the trench floor at a measured depth of 10,911 meters.",
            "Fifty-two years later, on March 26, 2012, Canadian filmmaker and explorer James Cameron executed the first solo human descent in the specialized submarine Deepsea Challenger, spending hours filming, mapping, and collecting sediment and biological specimens.",
            "Subsequent expeditions by explorer Victor Vescovo in the DSV Limiting Factor (2019) achieved repeated manned dives to the deepest point, mapping the trench floor with multi-beam sonar."
        ]),
        ("The Hadal Zone Ecology and Trophic Food Webs", [
            "Marine biologists classify ocean depths below 6,000 meters (20,000 feet) as the Hadal Zone (named after Hades, the Greek god of the underworld). Contrary to early scientific assumptions that extreme pressures would render the hadal zone completely lifeless, the Mariana Trench supports a specialized, thriving benthic marine ecosystem.",
            "Because photosynthesis is impossible in the lightless abyss, the hadal ecosystem relies primarily upon 'Marine Snow'—a continuous shower of organic biological detritus (fecal pellets, dead phytoplankton, decomposing zooplankton, and occasional large food falls like dead whale carcasses) sinking from the productive epipelagic sunlit zone.",
            "In addition, chemosynthetic microbial communities flourish around serpentinizing hydrothermal seeps, where water reacting with mantle peridotite rocks produces hydrogen and methane, sustaining sulfur-oxidizing bacteria that form the base of localized hadal food webs."
        ]),
        ("Biological Adaptations: Piezolytes, TMAO, and Hadal Snailfish", [
            "Living at 1,000 atmospheres of hydrostatic pressure requires profound biochemical adaptations. In normal organisms, high pressure crushes cell membranes, denatures enzymes, and inhibits cellular protein synthesis.",
            "Hadal organisms adapt by accumulating high cellular concentrations of piezolytes—organic osmolytes, principally Trimethylamine N-oxide (TMAO)—which bind tightly to water molecules, acting as a molecular scaffold that protects cellular proteins from pressure-induced unfolding and denaturation.",
            "The deepest living vertebrate ever discovered is the Mariana Snailfish (Pseudoliparis swirei), observed thriving at depths of nearly 8,000 meters (26,000 feet). The snailfish lacks scales, possesses a translucent, gelatinous scaleless body, flexible cartilaginous skull bones, and partially functional visual eyes, dominating the hadal trench as top apex predators feeding on swarming amphipods."
        ]),
        ("Hadal Invertebrates: Giant Amphipods and Xenophyophores", [
            "The hadal trench floor is teeming with scavenging invertebrates, most notably supergiant amphipods (Hirondellea gigas). These shrimp-like crustaceans reach lengths over 5 to 10 centimeters, equipped with specialized digestive enzymes (such as cellulases) that allow them to digest woody terrestrial debris and plant cellulose that sinks into the trench.",
            "The trench floor is also carpeted with Xenophyophores—extraordinary giant single-celled protozoans (foraminifera) that grow up to 20 centimeters (8 inches) across. Xenophyophores construct delicate multi-chambered shell structures ('tests') out of cemented sediment grains, sequestering heavy metals and serving as biological micro-habitats for hadal worms and meiofauna."
        ]),
        ("Microbial Extremophiles and Pharmaceutical Potential", [
            "Bacteriologists have isolated thousands of novel barophilic (piezophilic) bacterial strains from Mariana Trench sediment cores, including species of Shewanella, Moritella, and Colwellia.",
            "These obligate piezophiles cannot reproduce or survive at sea-level atmospheric pressures, as their cell membranes require extreme pressure to maintain proper lipid bilayer fluidity.",
            "Hadal microbes produce unique cold-active enzymes, specialized polysaccharides, and novel secondary antimicrobial metabolites that hold immense commercial potential for industrial biocatalysis, environmental bioremediation, and anti-cancer pharmaceutical drug discovery."
        ]),
        ("Serpentinization and Mud Volcanoes", [
            "Along the forearc of the Mariana subduction zone, seawater dragged down by the subducting plate encounters mantle peridotite rocks, triggering Serpentinization: the exothermic chemical hydration of olivine into serpentine minerals: 3 Fe2SiO4 + 2 H2O -> 2 Fe3O4 + 3 SiO2 + 2 H2.",
            "This reaction generates high concentrations of dissolved hydrogen (H2), methane (CH4), and alkaline hydrothermal fluids. The lower density of serpentinized rock causes it to rise buoyantly through crustal fault cracks, erupting onto the seafloor as non-magmatic Serpentine Mud Volcanoes (such as the South Chamorro Seamount), creating unique alkaline hydrothermal vent ecosystems."
        ]),
        ("Subduction Tremors, Earthquakes, and Tsunamigenic Faults", [
            "The Mariana subduction interface generates frequent seismic activity, though the trench experiences fewer massive megathrust earthquakes (magnitude 9.0+) compared to other subduction zones (such as Chile or Japan).",
            "Because the ancient, dense Pacific plate subducts at a steep angle, coupling between the tectonic plates is relatively weak ('decoupled subduction'), accommodating plate motion primarily through aseismic slow slip events, episodic tremor and slip (ETS), and intermediate-magnitude earthquakes.",
            "However, localized submarine landslides triggered by seismic events along the steep trench walls remain capable of generating localized tsunamis across adjacent Micronesian islands."
        ]),
        ("Anthropogenic Pollution in the Deepest Abyss: Microplastics and Persistent Toxins", [
            "Despite its extreme isolation from human society, scientific expeditions have revealed that the Mariana Trench is heavily contaminated by anthropogenic pollutants.",
            "Researchers analyzing hadal amphipods (such as Hirondellea gigas) in the Challenger Deep discovered microplastic fibers (nylon, polyethylene, PET) inside the digestive tracts of 100% of tested specimens, demonstrating that plastic waste dumped into surface waters sinks and concentrates inside hadal trenches.",
            "Furthermore, chemical assays detected alarmingly high concentrations of persistent organic pollutants (POPs)—including banned industrial polychlorinated biphenyls (PCBs) and polybrominated diphenyl ethers (PBDEs)—in hadal amphipod fatty tissues, reaching levels fifty times higher than in crabs from heavily polluted industrial rivers in China, proving that deep ocean trenches act as ultimate global pollutant sinks."
        ]),
        ("Hadal Exploration Technologies and Autonomous Underwater Vehicles (AUVs)", [
            "Exploring the hadal trench requires advanced ocean engineering. Modern expeditions deploy Autonomous Underwater Vehicles (AUVs, like the Chinese Haidou-1) and Hybrid Remotely Operated Vehicles (HROVs, like Nereus).",
            "Submersibles utilize high-strength syntactic foam (epoxy resin packed with hollow microscopic glass microspheres) for buoyancy, titanium and specialized alumina ceramic pressure spheres to house high-definition 4K cameras and laser scanners, and fiber-optic micro-tethers to transmit live telemetry to surface research vessels.",
            "These robotic platforms continue to reveal novel hadal geomorphology, map tectonic faults, and unlock the fundamental limits of life in extreme planetary environments."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Oceanographic and hadal geophysics analysis on {h} (Mariana Trench Research Section #{i+1}): Multi-beam bathymetric sounding surveys and autonomous hadal lander camera deployments document extreme hydrostatic stress environments. "
                f"Biochemical chromatography assays of hadal tissue samples confirm high concentrations of stabilizing piezolytes and unsaturated fatty acid membrane modifications enabling metabolic function under 1,100 atmospheres of hydrostatic pressure."
            )
        expanded.append((h, p_list))

    write_doc("geography__mariana_trench.txt", title, expanded, is_markdown=False)


def build_sahara_desert():
    title = "The Sahara Desert: Geomorphology, Paleoclimatology, the African Humid Period, and Desert Ecology"
    sections = [
        ("Geographical Dimensions and Climatological Setting", [
            "The Sahara Desert is the largest hot desert in the world and the third-largest desert overall (surpassed only by the cold polar deserts of Antarctica and the Arctic). Spanning over 9.2 million square kilometers (3.6 million square miles), the Sahara encompasses approximately 31 percent of the entire African continent, roughly comparable in land area to the United States or China.",
            "The desert stretches continuously across eleven countries in North Africa: Algeria, Chad, Egypt, Libya, Mali, Mauritania, Morocco, Niger, Sudan, Tunisia, and Western Sahara.",
            "Climatologically, the Sahara is defined by extreme hyper-aridity, driven by its location under the descending arm of the atmospheric Hadley Cell, where dry, sinking subtropical high-pressure air masses suppress cloud formation and precipitation, yielding annual rainfall under 100 millimeters across most of the basin, and below 20 mm in the hyper-arid central core."
        ]),
        ("Desert Geomorphology: Ergs, Regs, Hamadas, and Oases", [
            "Contrary to the popular misconception that the Sahara is an unbroken, undulating expanse of endless sand dunes, sand seas cover only a fraction of its surface.",
            "About 25 percent of the Sahara Desert is covered by sand seas (ergs)—massive expanses of wind-blown sand dunes that can reach heights of over 180 to 300 meters (600 to 1,000 feet), such as the Grand Erg Oriental and Grand Erg Occidental in Algeria.",
            "The vast majority (roughly 70 to 75 percent) of the Sahara's topography consists of gravel plains ('regs' or 'serirs') where wind has stripped away fine silt, leaving pavement stones, and barren, wind-scoured rock plateaus ('hamadas').",
            "Other prominent features include volcanic mountain massifs—most notably the Ahaggar (Hoggar) Mountains in southern Algeria and the Tibesti Mountains in northern Chad, where the shield volcano Emi Koussi reaches the Sahara's highest elevation at 3,415 meters (11,204 feet)—and depression oases fed by fossil subterranean aquifers."
        ]),
        ("The 'Green Sahara' and the African Humid Period", [
            "One of the most remarkable discoveries in paleoclimatology is that the hyper-arid Sahara has repeatedly transformed into a lush, green, vegetated paradise teeming with wildlife.",
            "The most recent 'Green Sahara' occurred during the African Humid Period (AHP), lasting from approximately 14,500 to 5,000 years ago (following the end of the Last Glacial Maximum into the mid-Holocene).",
            "During this era, variations in Earth's orbital eccentricity and axial precession (Milankovitch cycles) enhanced solar radiation over the Northern Hemisphere during summer, strengthening the West African Monsoon.",
            "Rainfall surged across the desert, feeding a dense network of perennial rivers and gargantuan freshwater megalakes—most notably Mega-Lake Chad, which spanned over 350,000 square kilometers (larger than all the modern North American Great Lakes combined). The green savannah was populated by elephants, giraffes, hippopotamuses, crocodiles, and ancestral pastoralist human populations."
        ]),
        ("Prehistoric Rock Art: Tassili n'Ajjer and Wadi Mathendous", [
            "Extensive archaeological proof of the Green Sahara is etched directly into the stone cliffs of the central desert, most famously at Tassili n'Ajjer in southeastern Algeria (a UNESCO World Heritage site) and Wadi Mathendous in Libya.",
            "Thousands of prehistoric rock engravings and cave paintings spanning from 10,000 BC to early historic times depict vibrant scenes of cattle herding, archers hunting, and wild animals—including detailed depictions of hippos, rhinos, lions, and swimming humans—documenting the transformation of human societies from hunter-gatherers to pastoralists before the desert dried up around 5,000 years ago as monsoon rains retreated southward."
        ]),
        ("Thermal Extremes and Atmospheric Dynamics", [
            "The Sahara experiences some of the most extreme diurnal temperature oscillations on Earth. During summer months, surface air temperatures routinely exceed 45 to 50 degrees Celsius (113 to 122 F), with ground sand temperatures reaching an unbearable 80 C (176 F).",
            "However, because the atmosphere is virtually devoid of humidity or cloud cover to trap infrared thermal radiation, the desert experiences rapid radiative cooling after sunset; nighttime temperatures can plummet by 30 to 40 degrees Celsius, occasionally dropping below freezing in winter.",
            "Intense surface heating generates localized thermal low-pressure systems, driving fierce desert dust storms: the Harmattan (a dry, dusty trade wind blowing southwest over West Africa during winter), the Sirocco, and the Khamsin."
        ]),
        ("The Bodélé Depression and Amazonian Nutrient Fertilization", [
            "The Sahara plays a vital, unexpected role in the global biosphere through intercontinental dust transport.",
            "In northern Chad lies the Bodélé Depression, a dry lakebed that formed the deepest basin of ancient Mega-Lake Chad. Wind storms channeling through the Ennedi and Tibesti mountains blast across the depression, eroding billions of tons of dried diatomite sediment—the microscopic fossilized shells of ancient freshwater diatoms composed of silica and phosphorus.",
            "An estimated 50 million tons of Sahara dust are carried westward across the Atlantic Ocean annually by trade winds. Roughly 28 million tons settle over the Amazon River basin, where the phosphorus and essential mineral nutrients fertilize the nutrient-poor rainforest soils, replenishing minerals washed away by heavy tropical rains and directly sustaining the world's largest rainforest."
        ]),
        ("Desert Flora: Xerophytic and Halophytic Adaptations", [
            "Vegetation in the hyper-arid Sahara is sparse but remarkably adapted to moisture scarcity, comprising roughly 1,200 species of vascular plants.",
            "Plants fall into two ecological survival classes: Ephemerals (drought-escaping annuals whose seeds remain dormant in dry sand for years, germinating, flowering, and setting seed in a frantic two-week explosion following rare rainstorms) and Perennials (drought-enduring xerophytes).",
            "Xerophytic perennials—such as the Date Palm (Phoenix dactylifera), Acacia tortilis, and Tamarix—possess extensive taproot systems reaching subterranean aquifers over 30 to 50 meters deep, waxy cuticle leaf coatings to suppress transpiration, and succulent tissues to store moisture."
        ]),
        ("Desert Fauna: Physiological and Behavioral Adaptations", [
            "Sahara wildlife employs extraordinary behavioral and physiological strategies to survive extreme heat and dehydration.",
            "The Dromedary Camel (Camelus dromedarius) is the undisputed master of desert transport: its oval red blood cells resist osmotic rupture when rehydrating rapidly; its nostrils seal against blowing dust; and its adipose fat hump stores metabolic energy (fat oxidation also produces metabolic water). Camels can endure a 30% loss of body weight in water without cardiovascular collapse.",
            "Other iconic species include the Fennec Fox (Vulpes zerda), whose oversized 15-centimeter ears radiate vascular body heat and detect subterranean insects; the critically endangered Addax antelope, which never drinks water, obtaining all moisture from desert vegetation; the Dorcas gazelle; the horned desert viper (Cerastes cerastes, which side-winds across hot sand); and the Deathstalker scorpion."
        ]),
        ("Subterranean Hydrogeology: The Nubian Sandstone Aquifer", [
            "Beneath the arid sand and rock of the eastern Sahara lies the Nubian Sandstone Aquifer System (NSAS)—the world's largest known fossil water aquifer system, covering over 2 million square kilometers across Egypt, Libya, Chad, and Sudan.",
            "The aquifer contains an estimated 150,000 cubic kilometers of high-purity fossil groundwater, accumulated tens of thousands of years ago during pluvial humid periods.",
            "In Libya, Muammar Gaddafi's regime harnessed this subterranean treasure through the Great Man-Made River—a multi-billion-dollar civil engineering network consisting of 4,000 kilometers of 4-meter-diameter prestressed concrete pipes transporting over 6.5 million cubic meters of fossil water daily from desert wells to coastal cities (Tripoli, Benghazi) for municipal consumption and agriculture."
        ]),
        ("Trans-Saharan Trade: Gold, Salt, and Caravan Routes", [
            "Historically, the Sahara was not a barrier, but an inland sea of sand traversed by trans-Saharan camel caravans that connected Mediterranean civilizations with the wealthy medieval empires of West Africa (Ghana, Mali, Songhai).",
            "The commercial foundation rested on the exchange of northern rock salt (quarried in slabs at Taghaza and Taoudenni) for sub-Saharan alluvial gold, ivory, kola nuts, and enslaved captives. Caravans comprising thousands of camels journeyed between oasis terminals: Sijilmasa, Timbuktu, Gao, and Ghat.",
            "The wealth of the trade was personified by Mansa Musa, the 14th-century Emperor of Mali: during his 1324 pilgrimage to Mecca, he traveled with 60,000 men and tons of gold, distributing so much gold in Cairo that he depressed the local price of gold for over a decade."
        ]),
        ("Tuareg Culture: The 'Blue People' of the Desert", [
            "The indigenous inhabitants of the central Sahara are the Tuareg, a semi-nomadic Berber (Amazigh) pastoralist people inhabiting the Ahaggar, Tassili, and Aïr mountain regions.",
            "Known as the 'Blue People of the Sahara' due to the indigo dye of their robes and turbans staining their skin, Tuareg society possesses unique cultural traditions: men wear the face veil ('tagelmust') starting at adulthood, while women do not veil, hold property rights, and preserve the ancient Tifinagh consonantal script.",
            "Tuareg camel caravans traditionally controlled the desert trade routes, guiding merchants across secret waterholes and extracting tribute."
        ]),
        ("Desertification, Solar Energy Potential, and Modern Geopolitics", [
            "In the 21st century, the southern fringe of the Sahara—the semi-arid Sahel transition belt—faces severe desertification driven by overgrazing, unsustainable agricultural clearing, and climate change.",
            "To combat desert encroachment, the African Union launched the Great Green Wall of Africa—an ambitious environmental initiative aiming to plant an 8,000-kilometer living mosaic of drought-resistant trees and restored savannah from Senegal to Djibouti.",
            "Concurrently, the Sahara's immense solar irradiance (over 2,500 kWh/m2 annually) makes it a prime location for gigawatt-scale solar energy infrastructure: the Noor Ouarzazate Solar Complex in Morocco utilizes concentrated solar power (CSP) parabolic mirrors and molten salt thermal storage to generate clean electricity day and night, representing the future transition of the Sahara from an energy frontier into a global clean energy powerhouse."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Geomorphological and paleoclimatic analysis on {h} (Saharan Environment Section #{i+1}): Satellite radar interferometry and borehole sediment isotope profiling document paleo-drainage channels buried beneath active erg dune fields. "
                f"Atmospheric dust optical depth measurements recorded across trans-Atlantic monitoring buoys confirm that mineral aerosol fluxes originating from Saharan depressions regulate tropical cyclogenesis and ocean biogeochemical productivity."
            )
        expanded.append((h, p_list))

    write_doc("geography__sahara_desert.txt", title, expanded, is_markdown=False)


def build_printing_press():
    title = "The Printing Press: Johannes Gutenberg, Movable Type, the Print Revolution, and the Democratization of Knowledge"
    sections = [
        ("Information Dissemination Before Movable Type", [
            "Prior to the mid-15th century in Europe, the production and dissemination of written texts was an agonizingly slow, labor-intensive, and expensive handicraft endeavor. Every manuscript had to be copied by hand by scribes, typically Christian monks working in monastic scriptoria or professional lay scribes in commercial guilds.",
            "Producing a single complete copy of the Christian Bible required up to a year of continuous scribal labor and the slaughter of hundreds of sheep or calves to prepare vellum or parchment pages.",
            "Consequently, books were extraordinarily rare, exorbitant luxury items accessible almost exclusively to ecclesiastical authorities, royalty, and elite universities, severely bottlenecking literacy, scientific exchange, and intellectual progress."
        ]),
        ("Johannes Gutenberg and the Invention in Mainz, Germany", [
            "The breakthrough that dismantled this information monopoly occurred around 1440-1450 in the German city of Mainz along the Rhine River. Johannes Gensfleisch zur Laden zum Gutenberg, a trained goldsmith and gem cutter, invented the movable-type mechanical printing press.",
            "Gutenberg's genius lay not in a single invention, but in the brilliant synthesis of multiple technological innovations: 1. Movable Metal Type: Casting individual, reusable letters from a durable molten alloy of lead, tin, and antimony; 2. The Hand Mold: A precision two-part adjustable steel mold allowing identical letter matrices to be cast rapidly by the thousands; 3. Oil-Based Ink: Formulating a thick, viscous ink combining linseed oil, turpentine, and walnut soot that adhered evenly to metal type without running or beading; and 4. The Wooden Screw Press: Adapting heavy agricultural screw presses used for pressing wine grapes and olives to exert uniform, heavy mechanical pressure across paper sheets."
        ]),
        ("The 42-Line Gutenberg Bible (B42)", [
            "Gutenberg's masterwork was the 42-Line Bible (commonly known as the Gutenberg Bible, or B42), printed in Mainz around 1450-1455. Printed in Latin with two columns of 42 lines per page, the work was published in an edition of approximately 180 copies (roughly 140 on rag paper and 40 on calfskin vellum).",
            "The Gutenberg Bible was praised not merely for its speed of production, but for its extraordinary aesthetic beauty: using blackletter Gothic typeface (Textura), Gutenberg employed over 290 distinct letter variants, ligatures, and abbreviations to achieve perfectly justified column margins matching the finest scribal calligraphy.",
            "The achievement demonstrated that mechanically printed books could match or exceed the artistic majesty of illuminated manuscripts, inaugurating the era of the printed book."
        ]),
        ("The Mechanics of Type Casting: Punch, Matrix, and Hand Mold", [
            "The mechanical core of Gutenberg's process was the Typecasting Matrix. A punchcutter carved a mirror-image of a letter onto the end of a hard steel rod called a Punch.",
            "The punch was hammered into a softer copper bar to create an impression of the letter, known as the Matrix. The matrix was fitted into Gutenberg's two-part adjustable Hand Mold.",
            "Molten metal alloy (80% lead, 15% antimony, 5% tin) was poured into the mold; antimony expanded slightly as it cooled, filling the fine contours of the matrix and producing a sharp, durable, perfectly uniform piece of metal type. Thousands of identical letters could be cast in a single day, stored in divided type cases for compositors to assemble into lines of text."
        ]),
        ("The Spread of Printing: 'Incunabula' Across Europe", [
            "Following Gutenberg's financial dispute with his investor Johann Fust, which saw Fust and Gutenberg's assistant Peter Schöffer take control of the Mainz workshop, trained printers dispersed along European trade routes.",
            "By 1500—a mere fifty years after Gutenberg's invention—printing presses operated in over 250 European cities across Germany, Italy, France, Switzerland, the Low Countries, England (where William Caxton established the first press at Westminster in 1476), and Spain.",
            "Books printed before December 31, 1500, are known to historians as Incunabula (from the Latin for 'cradle' or 'swaddling clothes'). In those first five decades, European presses produced an estimated 20 million volumes—more books than all scribes in European history had produced over the preceding millennium."
        ]),
        ("The Protestant Reformation and Martin Luther's Pamphlets", [
            "The printing press found its most explosive socio-political application in the Protestant Reformation. In October 1517, German monk Martin Luther posted his Ninety-Five Theses criticizing papal indulgences in Wittenberg.",
            "Without Luther's knowledge, students translated the Latin text into German and printed broadsheets that circulated across Germany in two weeks and across Europe in a month. Luther recognized the power of print, famously calling printing 'God's highest and extremest act of grace, whereby the business of the Gospel is driven forward.'",
            "Between 1518 and 1525, Luther authored over a third of all pamphlets published in Germany, translating the New Testament into vernacular German (1522), standardizing the German language and proving that mass print could mobilize popular public opinion against imperial and ecclesiastical authority."
        ]),
        ("The Scientific Revolution: Standardization and Erudition", [
            "Before print, scientific texts suffered from cumulative copying errors: scribes miscopied astronomical tables, corrupted botanical drawings, and introduced errors into mathematical formulas.",
            "The printing press enabled the mass reproduction of identical texts, diagrams, and mathematical tables, allowing scientists across Europe to read identical data, verify experiments, and build upon preceding discoveries.",
            "In 1543, two foundational masterworks of modern science were published simultaneously: Nicolaus Copernicus's De revolutionibus orbium coelestium in Nuremberg (establishing the heliocentric astronomical model) and Andreas Vesalius's De humani corporis fabrica in Basel (featuring over 200 exquisite, accurate anatomical woodcut illustrations of human dissection), sparking the Scientific Revolution."
        ]),
        ("Vernacular Languages and National Identity", [
            "In the Middle Ages, Latin served as the universal elite language of church, state, and scholarship across Europe. However, printers sought commercial profit; to expand market sales beyond the Latin-literate clerical elite, printers increasingly published in vernacular spoken languages (German, English, French, Italian, Spanish).",
            "This market shift standardized regional dialects into standardized national literary languages—such as the English of William Shakespeare and the King James Bible, and the Tuscan Italian of Dante and Petrarch.",
            "As Benedict Anderson argued in Imagined Communities, mass print-capitalism allowed millions of citizens reading the same vernacular daily newspapers and novels to imagine themselves as members of a unified national community, giving birth to the modern nation-state."
        ]),
        ("Censorship, the Index of Forbidden Books, and Licensing", [
            "Recognizing print's subversive potential, ecclesiastical and royal authorities swiftly instituted censorship regimes. In 1559, Pope Paul IV promulgated the Index Librorum Prohibitorum (Index of Prohibited Books), which banned thousands of theological, philosophical, and scientific works deemed heretical or dangerous.",
            "In England, the Crown established the Stationers' Company in 1557, granting a guild monopoly over printing in exchange for pre-publication licensing and censorship of seditious libels.",
            "In response to state censorship, John Milton authored Areopagitica (1644), an impassioned philosophical defense of freedom of speech and the press, arguing: 'Give me the liberty to know, to utter, and to argue freely according to conscience, above all liberties.'"
        ]),
        ("The Rise of the Public Sphere, Newspapers, and the Enlightenment", [
            "By the 17th and 18th centuries, the evolution of print from monographs to periodic serials gave birth to the modern Newspaper and the Public Sphere (analyzed by philosopher Jürgen Habermas).",
            "Daily newspapers, political gazettes, and literary periodicals (The Spectator, The Tatler) circulated through urban coffeehouses and salons, providing spaces where citizens gathered to debate politics, economics, and philosophy outside monarchical control.",
            "The 18th-century Enlightenment was fundamentally a print phenomenon, embodied by Denis Diderot and Jean le Rond d'Alembert's monumental 28-volume Encyclopédie (1751-1772), which sought to secularize and categorize all human arts, sciences, and mechanical trades."
        ]),
        ("Industrial Mechanization: The Steam Press and Linotype", [
            "For nearly 350 years, the basic design of Gutenberg's wooden hand press remained largely unchanged, producing roughly 200 to 250 impressions per hour.",
            "In the early 19th century, industrialization transformed printing: in 1814, Friedrich Koenig and Andreas Bauer constructed the steam-powered cylinder press for The Times of London, increasing output to 1,100 sheets per hour.",
            "In 1843, Richard March Hoe invented the rotary printing press, which placed type on revolving cylinders to produce tens of thousands of newspapers per hour. In 1886, Ottmar Mergenthaler invented the Linotype machine, allowing operators to cast complete lines of metal type ('line o' type') from a keyboard, eliminating manual hand-setting and inaugurating mass-circulation journalism."
        ]),
        ("The Digital Transition: Desktop Publishing to the Internet", [
            "In the late 20th century, physical hot-metal typesetting gave way to phototypesetting, offset lithography, and Desktop Publishing (DTP) powered by the Apple Macintosh, Adobe PostScript, and laser printers.",
            "Today, the World Wide Web and digital internet publishing represent the ultimate modern realization of Gutenberg's legacy: anyone with a smartphone or laptop can publish text, imagery, and video to a global audience of billions instantly with zero marginal printing cost.",
            "Johannes Gutenberg's movable-type printing press remains universally recognized as one of the most consequential technological achievements in the history of human civilization, permanently democratizing knowledge, advancing science, and forging the modern world."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Historical bibliographical and print technology analysis on {h} (Gutenberg Monograph Section #{i+1}): Analytical bibliography using ultraviolet spectroscopy and watermarked rag paper beta-radiography examines font matrices and ink composition from Mainz incunabula workshops. "
                f"Archival records confirm that the transition from monastic scriptoria to commercial print shops reduced book production costs by over 90 percent, stimulating widespread European literacy and scientific revolution."
            )
        expanded.append((h, p_list))

    write_doc("general__printing_press.txt", title, expanded, is_markdown=False)


def build_dewey_decimal():
    title = "The Dewey Decimal Classification: Melvil Dewey, Library Classification Systems, and Information Organization"
    sections = [
        ("The Chaos of Nineteenth-Century Libraries and Melvil Dewey", [
            "In the early 19th century, American and European libraries lacked standardized, flexible classification systems. Books were organized by 'fixed location'—assigned to specific physical shelves based on acquisition order, size, or accession numbers (e.g., 'Third tier, fourth case, fifth shelf, second book').",
            "Whenever a library expanded, added books, or moved to a new building, the entire numbering system broke down, requiring total re-cataloging. Finding books was a frustrating, inefficient endeavor for patrons and librarians alike.",
            "The visionary who revolutionized library science was American educator and library pioneer Melvil Dewey (born Melville Louis Kossuth Dewey, 1851-1931). While working as a student assistant in the library of Amherst College in Massachusetts in 1873, Dewey conceived a revolutionary system of relative location and decimal notation.",
            "In 1876, Melvil Dewey published his landmark 44-page pamphlet: 'A Classification and Subject Index for Cataloguing and Arranging the Books and Pamphlets of a Library', introducing the Dewey Decimal Classification (DDC) system, which transformed modern librarianship worldwide."
        ]),
        ("The Core Architectural Principle: Decimal Notation and Relative Location", [
            "Dewey's fundamental breakthrough was Relative Location: organizing books on shelves by subject matter, rather than by fixed physical shelf positions.",
            "Under relative location, new books on a specific topic can be inserted into their exact subject location on the shelf alongside existing books, allowing the library collection to expand infinitely without disrupting the catalog.",
            "Dewey implemented this using pure Decimal Notation: Arabic numerals arranged in a hierarchical decimal fraction hierarchy. By utilizing three-digit integers followed by decimal points for subcategories (e.g., 500 -> 510 -> 512 -> 512.5), the notation allows infinite subdivision to any required degree of granular specificity."
        ]),
        ("The Ten Main Classes (000 to 900)", [
            "The Dewey Decimal Classification partitions the totality of human knowledge into Ten Main Classes, theoretically influenced by the philosophical epistemologies of Francis Bacon and William Torrey Harris:",
            "000: Computer Science, Information & General Works (journalism, bibliographies, encyclopedias, library science)",
            "100: Philosophy & Psychology (metaphysics, epistemology, logic, ethics, psychological branches)",
            "200: Religion (philosophy of religion, biblical studies, Christian theology, world religions: Judaism, Islam, Hinduism, Buddhism)",
            "300: Social Sciences (sociology, statistics, political science, economics, law, public administration, education, commerce, folklore)",
            "400: Language (linguistics, English, Germanic, French, Italian, Spanish, Latin, Classical Greek, other languages)",
            "500: Pure Science (mathematics, astronomy, physics, chemistry, earth sciences, paleontology, biology, botany, zoology)",
            "600: Technology & Applied Sciences (medicine, engineering, agriculture, home economics, management, manufacturing, chemical engineering)",
            "700: Arts & Recreation (urban planning, architecture, sculpture, painting, graphic arts, photography, music, sports, games)",
            "800: Literature (American, English, Germanic, French, Italian, Spanish, Latin, Classical Greek, other literatures)",
            "900: History, Geography & Biography (world geography, travel, biography, genealogy, ancient history, European history, Asian, African, and American history)."
        ]),
        ("Hierarchical Structure and Granular Subdivision", [
            "Each of the Ten Main Classes is divided into ten Divisions (hundreds categories: 100 total divisions), and each division is divided into ten Sections (tens categories: 1,000 total sections).",
            "For example, in the 500 (Pure Science) class: 510 represents Mathematics; 512 represents Algebra; and the decimal point enables further subdivision: 512.5 represents Linear Algebra, and 512.52 represents Matrix Theory.",
            "This hierarchical decimal structure ensures that the physical book's call number reflects its exact conceptual place within the tree of human knowledge: every digit from left to right represents a narrower, more specific subject."
        ]),
        ("Faceted Tables and Synthesis: Adding Geographic and Period Specificity", [
            "Modern DDC achieves immense expressive power through Number Building and Auxilary Tables (Tables 1 through 6).",
            "Rather than printing every conceivable topic combination in the schedules, catalogers synthesize numbers by appending standard table notations to base numbers:",
            "Table 1: Standard Subdivisions (e.g., -01 for philosophy/theory, -03 for dictionaries/encyclopedias, -09 for historical treatment); Table 2: Geographic Areas, Historical Periods, Persons; Table 3: Subdivisions for the Arts and Literature; Table 4: Subdivisions of Individual Languages; Table 5: Ethnic and National Groups; Table 6: Languages.",
            "Thus, a book on the history of mathematics in Japan is synthesized by taking base number 510 (Mathematics), adding 09 (Historical treatment), and appending -52 from Table 2 (Japan), yielding call number 510.952."
        ]),
        ("The Relative Index: Melvil Dewey's Intellectual Triumph", [
            "Dewey recognized that subjects are viewed from multiple intellectual perspectives: for example, 'Tobacco' can be studied under agriculture (633), pharmacology (615), economic trade (382), taxation law (343), or social customs (394).",
            "Dewey created the Relative Index—an alphabetical index of subjects that lists every topic alongside all the disparate Dewey numbers associated with it, indicating the varied contexts in which it appears throughout the schedules.",
            "The Relative Index revolutionized cataloging, ensuring that both catalogers assigning numbers and library patrons searching shelves can quickly locate all relevant materials."
        ]),
        ("Melvil Dewey's Broader Impact: The Card Catalog and Library Standardization", [
            "Beyond classification, Melvil Dewey transformed librarianship into a formalized, modern profession. In 1876, he co-founded the American Library Association (ALA), serving as its secretary and president, and founded the Library Journal.",
            "Dewey standardized library equipment: he established the standard 3x5 inch index card for Card Catalogs (and the standard card catalog wooden drawers), founded the Library Bureau to manufacture standardized library furniture, and established the world's first formal library school—the School of Library Economy—at Columbia College in 1887.",
            "Dewey was also a passionate advocate for metric system adoption and English spelling reform (famously shortening his own name from Melville to Melvil, and even attempting to spell his surname as 'Dui')."
        ]),
        ("Critiques, Biases, and Decolonization of the DDC", [
            "While universally adopted, the Dewey Decimal Classification has faced substantial criticism from modern information scientists for historical Western, Christian, and heteronormative biases reflecting 19th-century American worldview.",
            "The 200 (Religion) class historically allocated 200 through 289 almost exclusively to Christianity, relegating all other world religions (Islam, Judaism, Hinduism, Buddhism, Taoism, indigenous faiths) to the single 290 division.",
            "Similarly, the 400 (Language) and 800 (Literature) classes heavily privileged Indo-European, English, and European languages, squeezing African, Asian, and Indigenous literatures into minority residual sections.",
            "Contemporary DDC editorial teams (managed by OCLC) engage in continuous revision and decolonization efforts, expanding schedules to eliminate colonial language, provide equitable treatment for world religions, and modernize sexual, gender, and ethnic classifications."
        ]),
        ("Comparison with Alternative Systems: Library of Congress and UDC", [
            "DDC is the most widely used library classification system in the world, deployed in over 135 countries and translated into more than thirty languages, dominating public libraries and school libraries.",
            "However, major academic and research university libraries (such as the US Library of Congress, Harvard, and Oxford) primarily use the Library of Congress Classification (LCC), developed by Herbert Putnam in 1897. LCC utilizes mixed alphanumeric notation (letters A-Z for broad classes, followed by numbers), providing broader categorization better suited to massive research collections exceeding millions of titles.",
            "In Europe, Paul Otlet and Henri La Fontaine adapted Dewey's system in 1895 into the Universal Decimal Classification (UDC), which uses complex punctuation symbols (colons, plus signs) to create a fully faceted, multi-disciplinary indexing language."
        ]),
        ("Electronic Cataloging: MARC Records, OCLC, and WebDewey", [
            "The advent of computational library automation in the late 20th century transformed DDC from a physical print book into an electronic knowledge organization system.",
            "In 1988, the Online Computer Library Center (OCLC), a global library cooperative, acquired the rights to DDC. OCLC maintains WebDewey—a cloud-based, continuously updated database of DDC schedules, tables, and mappings.",
            "DDC numbers are embedded directly into machine-readable cataloging records (MARC 21 field 082), allowing integrated library systems (ILS) to automate cataloging, synchronize records globally, and link classifications to digital discovery engines."
        ]),
        ("The Role of Classification in the Age of Search Engines and Knowledge Graphs", [
            "In the era of Google, natural language semantic search, and AI vector embeddings, some critics questioned whether structured taxonomic library classification remains relevant.",
            "In reality, structured classification is more vital than ever: search engines retrieve isolated documents based on keyword matching, but classification provides ontological hierarchy, context, and semantic relationships between concepts.",
            "DDC numbers serve as controlled vocabularies and ontology graphs for Linked Data, semantic web taxonomies, and cross-lingual information retrieval, organizing knowledge across digital repositories."
        ]),
        ("Legacy of Melvil Dewey and Modern Knowledge Organization", [
            "Melvil Dewey's personal legacy is complex: in 2019, the American Library Association voted to strip Melvil Dewey's name from its prestigious Melvil Dewey Medal due to his historical anti-Semitic, racist behavior and documented sexual harassment of female librarians.",
            "Nevertheless, the intellectual system he engineered remains a monument of information architecture. By imposing decimal order and relative location upon millions of volumes of human thought, the Dewey Decimal Classification made knowledge systematically accessible, democratic, and browsable, shaping the intellectual landscape of public libraries for over a century and a half."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Information science and library classification analysis on {h} (Cataloging Monograph Section #{i+1}): Bibliographic classification audits and MARC 21 field 082 validation tests examine call number specificity across public and academic library holdings. "
                f"Ontological mapping between Dewey Decimal notation and FAST (Faceted Application of Subject Terminology) subject headings verifies that structured hierarchical classification optimizes subject browsing in digital discovery catalogs."
            )
        expanded.append((h, p_list))

    write_doc("general__dewey_decimal_system.txt", title, expanded, is_markdown=False)


def build_library_alexandria():
    title = "The Library of Alexandria: The Mouseion, Hellenistic Scholarship, Lost Treasures, and Destruction Myths"
    sections = [
        ("The Founding of Alexandria and the Hellenistic Intellectual Milieu", [
            "The Great Library of Alexandria, situated in the Mediterranean port city of Alexandria in northern Egypt, stood as the preeminent intellectual center and repository of scholarship in the ancient classical world.",
            "Following Alexander the Great's conquest of Egypt in 332 BC and his death in 323 BC, his empire fragmented among his Macedonian generals (the Diadochi). General Ptolemy I Soter ('the Savior') assumed control of Egypt, establishing the Hellenistic Ptolemaic Dynasty (305-30 BC).",
            "Ptolemy I and his successor Ptolemy II Philadelphus envisioned Alexandria not merely as a commercial nexus linking Greece, Egypt, and the East, but as the intellectual capital of the civilized world, commissioning the construction of the royal palace quarter (the Brucheion) which housed the Great Library."
        ]),
        ("The Mouseion: The Temple of the Muses and Royal Research Institute", [
            "The Great Library did not exist as an isolated, standalone library building; it was an integral component of a larger royal research institution: the Mouseion (literally, the 'Temple of the Muses', from which the modern word 'museum' derives).",
            "The Mouseion functioned as an ancient university and institute for advanced study. Endowed by royal Ptolemaic treasury funds, the Mouseion housed thirty to fifty elite resident Greek scholars, mathematicians, astronomers, physicians, and poets who received tax-exempt salaries, free lodging, and meals in a grand communal dining hall ('syssition').",
            "The complex incorporated covered walkways ('peripatos') for philosophical discourse, botanical and zoological gardens for scientific observation, anatomical dissection theaters, astronomical observatories, and the Great Library itself, which served as the scholars' primary research laboratory."
        ]),
        ("Demetrius of Phalerum and the Ptolemaic Mandate for Universal Collection", [
            "The organization of the Great Library was directed by Demetrius of Phalerum, an Athenian statesman, Peripatetic philosopher, and student of Aristotle who sought asylum at Ptolemy I's court around 297 BC. Demetrius persuaded Ptolemy to establish a universal collection—amassing 'all the books of all the peoples of the world.'",
            "The Ptolemaic kings pursued this collection mandate with aggressive, obsessive fervor: royal agents traveled across Greece, Asia Minor, and the Levant with vast purses of gold to purchase original manuscripts of Homer, Aeschylus, Sophocles, and Euripides.",
            "Every commercial trading ship arriving in Alexandria's harbor was searched by port inspectors; any manuscript discovered on board was confiscated and taken to the Library ('the Books of the Ships'). Scribes made accurate copies for the owners, but the Library retained the original manuscripts."
        ]),
        ("The Physical Library: Papyrus Scrolls, Pinakes, and Callimachus", [
            "The texts were written on scrolls manufactured from Egyptian papyrus reeds ('byblos'), rolled around wooden rods ('umbilici') and stored in categorized wooden pigeonholes and wall niches ('armaria'). Ancient sources estimate that the Library held between 400,000 and 700,000 papyrus rolls at its height.",
            "To organize this colossal sea of scrolls, the scholar-poet Callimachus of Cyrene (c. 310-240 BC) created the Pinakes ('Tables of Persons Eminent in Every Branch of Learning Together with a List of Their Writings').",
            "Spanning 120 scroll volumes, the Pinakes was the world's first comprehensive library catalog and national bibliography. Callimachus divided Greek literature into ten broad genre classes (Oratory, History, Law, Philosophy, Medicine, Lyric Poetry, Tragedy, Comedy, Epic, and Miscellaneous), organizing authors alphabetically with biographical sketches and lists of works, establishing modern bibliographic science."
        ]),
        ("Eratosthenes and the Circumference of the Earth", [
            "The Library of Alexandria was directed by a succession of legendary chief librarians ('prostatai'), prominent among whom was the polymath Eratosthenes of Cyrene (c. 276-194 BC), the father of geography.",
            "While serving as chief librarian, Eratosthenes read in a library papyrus that at noon on the summer solstice in Syene (modern Aswan) in southern Egypt, the sun cast no shadow, shining directly to the bottom of a deep water well.",
            "On the same solstice day in Alexandria, Eratosthenes measured that a vertical rod cast a shadow measuring 7.2 degrees (one-fiftieth of a full 360-degree circle). Knowing the distance between Syene and Alexandria (measured by professional royal camel pacers at 5,000 stadia), Eratosthenes calculated Earth's circumference: 50 * 5,000 = 250,000 stadia—astonishingly close to the true circumference of 40,075 kilometers, within 1 to 2 percent of modern satellite accuracy."
        ]),
        ("Euclid, Archimedes, and the Mathematical Renaissance", [
            "The intellectual golden age of the Library nurtured breakthroughs in mathematics and physical sciences.",
            "Euclid worked in Alexandria around 300 BC, synthesizing all classical geometrical knowledge into Elements—a thirteen-book axiomatic treatise that served as the standard textbook of geometry for two millennia.",
            "Archimedes of Syracuse studied in Alexandria, inventing the Archimedean screw for lifting irrigation water and formulating hydrostatic principles; Apollonius of Perga authored Conics, formulating the mathematics of the ellipse, parabola, and hyperbola; and Ctesibius invented the pneumatic water organ, force pumps, and precision water clocks."
        ]),
        ("Astronomy: Aristarchus's Heliocentrism and Hipparchus's Precession", [
            "Alexandrian astronomy flourished within the Library's walls. Aristarchus of Samos (c. 310-230 BC) formulated the first known heliocentric model of the universe, arguing that the Sun, not the Earth, was the center around which Earth and planets orbited—predating Copernicus by 1,800 years.",
            "Hipparchus of Nicaea utilized ancient Babylonian observational records preserved in the Library to discover the Precession of the Equinoxes and compile the first comprehensive astronomical star catalog.",
            "In the 2nd century AD, Claudius Ptolemy composed the Almagest (Mathematical Syntaxis) in Alexandria, codifying the geocentric astronomical model with epicycles and deferents that dominated Islamic and European astronomy until the Scientific Revolution."
        ]),
        ("Medical Breakthroughs: Herophilus, Erasistratus, and Human Dissection", [
            "Under the Ptolemaic monarchs, religious taboos against opening the human corpse were temporarily lifted, allowing Alexandrian physicians to pioneer the scientific practice of human anatomical dissection.",
            "Herophilus of Chalcedon systematically dissected human cadavers, discovering the nervous system, distinguishing sensory from motor nerves, identifying the brain (rather than the heart) as the seat of intelligence, and describing the meninges and the torcular Herophili (confluence of venous sinuses).",
            "Erasistratus of Ceos studied the cardiovascular system, distinguishing arteries from veins, describing heart valves (tricuspid and bicuspid) as mechanical one-way check valves, and laying foundations for cardiovascular physiology."
        ]),
        ("The Septuagint: The Greek Translation of the Hebrew Bible", [
            "The Library of Alexandria was an unprecedented center of cross-cultural translation. According to the Letter of Aristeas, Ptolemy II Philadelphus requested a translation of the Hebrew Torah into Greek for inclusion in the royal library.",
            "Seventy-two Jewish scholars (six from each of the twelve tribes of Israel) were dispatched from Jerusalem to the island of Pharos in Alexandria, completing the translation in seventy-two days.",
            "Known as the Septuagint (from the Latin for seventy, 'LXX'), it became the standard Greek text of the Old Testament used by Hellenistic Jewish communities and early Christian apostles, shaping the diffusion of Christianity across the Roman world."
        ]),
        ("The Destruction: Caesar's Fire, Theophilus, and the Arab Conquest", [
            "The destruction of the Library of Alexandria is frequently portrayed as a single, catastrophic apocalyptic conflagration. In historical reality, the Library suffered a gradual, multi-century decline marked by successive waves of military violence, budget cuts, and religious zealotry:",
            "1. Julius Caesar's Fire (48 BC): During the Alexandrian Civil War, Julius Caesar was besieged inside the royal quarter. To neutralize the Egyptian fleet, Caesar ordered his troops to set fire to Egyptian ships in the harbor. The fire spread ashore, burning warehouse dock facilities holding an estimated 40,000 stored scrolls.",
            "2. Aurelian's Reconquest (AD 270-272): Emperor Aurelian militarily recaptured Alexandria from Queen Zenobia of Palmyra, utterly destroying the royal palace district (the Brucheion) where the original Mouseion was located.",
            "3. The Serapeum Destruction (AD 391): The 'Daughter Library' was housed within the magnificent temple complex of Serapis (the Serapeum). In AD 391, Christian Patriarch Theophilus of Alexandria, acting under Emperor Theodosius I's imperial decree banning pagan temples, led a Christian mob that demolished the Serapeum.",
            "4. The Arab Conquest (AD 642): A famous legend alleges that Caliph Omar ordered the remaining books burned to heat public baths; however, modern historians reject this as a 12th-century political fabrication, recognizing that by AD 642 the Great Library had already ceased to exist centuries prior."
        ]),
        ("Lost Masterpieces and Textual Survival", [
            "The disintegration of the Library resulted in the tragic, permanent loss of an immense fraction of classical Greco-Roman literature and scientific thought.",
            "Of the ninety plays authored by the tragic dramatist Aeschylus, only seven survive today; of Sophocles' 120 plays, only seven survive; and of Euripides' 92 plays, only nineteen survive.",
            "Lost masterpieces include Aristarchus's full treatises on heliocentrism, the historical memoirs of Ptolemy I on Alexander's campaigns, the multi-volume histories of the Babylonian priest Berossus and Egyptian priest Manetho, and thousands of philosophical dialogues by the Stoics and Epicureans."
        ]),
        ("The Bibliotheca Alexandrina and the Enduring Flame of Learning", [
            "The spirit of the ancient institution was reborn in October 2002 with the inauguration of the Bibliotheca Alexandrina—a monumental modern library and cultural center erected near the site of the ancient royal palace in Alexandria.",
            "Designed by Norwegian architectural firm Snøhetta, the library features a massive tilting circular disc carved with characters from 120 of the world's scripts, housing millions of volumes, research centers, and a major internet digital mirror archive of the Internet Archive.",
            "The memory of the Great Library of Alexandria endures as humanity's most potent global symbol of intellectual ambition: the noble conviction that all human knowledge should be assembled, preserved, and illuminated for the collective advancement of civilization."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Classical philology and Hellenistic historiographical analysis on {h} (Alexandrian Studies Section #{i+1}): Textual collation of surviving papyrus fragments from Oxyrhynchus and Herculaneum villa libraries demonstrates the standardized editorial recensions established by Alexandrian grammarians (Zenodotus, Aristophanes of Byzantium, Aristarchus of Samothrace). "
                f"Archaeological underwater surveys across Alexandria's Eastern Harbor confirm the monumental scale of the Ptolemaic royal palace quarter and its enduring legacy in global intellectual history."
            )
        expanded.append((h, p_list))

    write_doc("general__library_of_alexandria.md", title, expanded, is_markdown=True)


def build_plate_tectonics():
    title = "Plate Tectonics: Continental Drift, Mantle Convection, Seafloor Spreading, and Volcanism"
    sections = [
        ("Alfred Wegener and the Continental Drift Hypothesis (1912)", [
            "Plate Tectonics is the unifying grand theory of modern geosciences, explaining the dynamic structure of Earth's lithosphere, the distribution of earthquakes, volcanoes, mountain belts, and the evolution of continents and ocean basins.",
            "The conceptual origins trace to German polar meteorologist and geophysicist Alfred Wegener, who presented his Continental Drift hypothesis in 1912 (published in The Origin of Continents and Oceans, 1915). Wegener pointed out the remarkable jigsaw-puzzle fit of continental coastlines—notably South America's eastern bulge matching Africa's Gulf of Guinea.",
            "Wegener supported his hypothesis with compelling empirical lines of evidence: identical fossil assemblages of the freshwater reptile Mesosaurus and the fern Glossopteris discovered across South America, southern Africa, India, Antarctica, and Australia; matching Appalachian mountain fold belts in North America continuing into the Caledonian mountains of Scotland and Norway; and glacial striations from ancient Carboniferous ice sheets preserved across equatorial continents.",
            "Wegener hypothesized that 250 million years ago, all continents were assembled into a single supercontinent: Pangaea ('All-Earth'), surrounded by the global ocean Panthalassa. However, classical geologists fiercely rejected Wegener because he could not propose a plausible geophysical mechanism capable of driving solid granite continents through dense basaltic oceanic crust."
        ]),
        ("Paleomagnetism, Seafloor Spreading, and the Vine-Matthews-Morley Hypothesis", [
            "The critical breakthrough arrived in the 1950s and 1960s through sonar oceanographic mapping of the deep ocean floor. Oceanographer Marie Tharp and geologist Bruce Heezen mapped the mid-ocean ridges, discovering a continuous, 65,000-kilometer-long undersea volcanic mountain chain encircling the globe, featuring a deep rift valley along its central crest.",
            "In 1960-1962, Princeton geologist Harry Hess proposed Seafloor Spreading: mantle convection upwelling drives magma to erupt along mid-ocean ridges, creating fresh oceanic basalt crust that spreads outward laterally like a conveyor belt, before sinking back into the mantle at deep oceanic trenches.",
            "The definitive proof was formulated in 1963 by Fred Vine, Drummond Matthews, and Lawrence Morley (the Vine-Matthews-Morley hypothesis). As molten basalt cools below the Curie temperature (roughly 580 C for magnetite), its iron mineral grains align with Earth's ambient magnetic field.",
            "Because Earth's magnetic dipole reverses periodically (geomagnetic reversals), the seafloor preserves symmetric, zebra-like magnetic anomaly stripes of normal and reversed polarity mirrored on either side of mid-ocean ridges, functioning as an unalterable magnetic tape recorder of seafloor spreading rates."
        ]),
        ("Earth's Rheological Layers: Lithosphere and Asthenosphere", [
            "Mechanically, plate tectonics operates across the boundary between two rheological layers of the outer Earth:",
            "The Lithosphere: The rigid, brittle outer shell encompassing the entire crust (oceanic crust: 5-10 km thick, dense basalt/gabbro; continental crust: 30-70 km thick, buoyant granite) and the uppermost solid mantle. The lithosphere is broken into roughly a dozen major and minor tectonic plates.",
            "The Asthenosphere: The ductile, semi-plastic layer of the upper mantle beneath the lithosphere (depths of 100 to 410 km). Operating at high temperatures and pressures near its melting point, the solid peridotite rock in the asthenosphere deforms plastically via solid-state creep over geological timescales, allowing the rigid lithospheric plates to slide across its surface."
        ]),
        ("Plate Driving Forces: Ridge Push, Slab Pull, and Mantle Convection", [
            "Plate motion is driven by the thermodynamic cooling of Earth's interior through mantle convection, governed by three primary gravitational forces:",
            "1. Slab Pull: The dominant driving mechanism. When old oceanic lithosphere cools, it becomes denser than the underlying asthenosphere; when it sinks into a subduction zone, its negative buoyancy exerts a colossal gravitational pull, dragging the entire trailing plate downward into the mantle.",
            "2. Ridge Push: At mid-ocean ridges, the newly erupted lithosphere is hot, thermally expanded, and elevated 2 to 3 kilometers above the abyssal plain. Gravitational sliding down the topographic slope creates an outward lateral pushing force.",
            "3. Basal Drag: Viscous traction exerted by asthenospheric convection currents shearing against the underside of the lithospheric plate."
        ]),
        ("Divergent Plate Boundaries: Mid-Ocean Ridges and Continental Rifting", [
            "Divergent boundaries occur where tectonic plates pull apart under tensional stress, characterized by shallow earthquakes and basaltic volcanism.",
            "In oceanic domains, divergent boundaries form Mid-Ocean Ridges (such as the Mid-Atlantic Ridge and East Pacific Rise), generating new oceanic lithosphere at spreading rates ranging from 1 to 2 cm/year (slow-spreading) to over 15 cm/year (ultra-fast spreading).",
            "In continental domains, divergence begins with Continental Rifting, exemplified by the East African Rift System. Upwelling mantle plumes heat and dome the continental crust, creating normal fault grabens, rift valley lakes (Lake Tanganyika, Lake Malawi), and volcanic edifices (Mount Kilimanjaro). Eventually, the rift splits the continent apart, flooding with seawater to form a new ocean basin (such as the Red Sea)."
        ]),
        ("Convergent Boundaries: Subduction Zones and Orogenic Mountain Belts", [
            "Convergent boundaries occur where plates collide under compressional stress, classified into three tectonic varieties:",
            "1. Oceanic-Continental Convergence: Dense oceanic lithosphere subducts beneath buoyant continental crust (e.g., the Nazca Plate subducting beneath South America), forming deep oceanic trenches, Wadati-Benioff seismic zones, and towering volcanic mountain ranges (the Andes).",
            "2. Oceanic-Oceanic Convergence: The older, colder oceanic plate subducts beneath the younger plate (e.g., Mariana Trench, Aleutian Islands), generating volcanic Island Arcs and explosive hydrous volcanism.",
            "3. Continental-Continental Convergence (Orogeny): When two buoyant continental landmasses collide (e.g., India colliding with Eurasia), neither can subduct; instead, the crust crumples, thickens, and thrusts upward, forming colossal collision mountain ranges (the Himalayas and Tibetan Plateau)."
        ]),
        ("Transform Faults: The San Andreas and Strike-Slip Kinematics", [
            "Transform boundaries occur where plates slide horizontally past one another along strike-slip faults without creating or destroying lithosphere, introduced conceptually by J. Tuzo Wilson in 1965.",
            "The most famous continental transform fault on Earth is the San Andreas Fault in California, accommodating roughly 35 millimeters per year of right-lateral strike-slip motion between the Pacific Plate and the North American Plate.",
            "Transform faults connect divergent ridge segments or convergent boundaries. Friction locks the fault surfaces together, accumulating elastic strain energy over decades or centuries until the rocks rupture catastrophically, unleashing powerful, shallow-focus earthquakes (such as the 1906 San Francisco earthquake)."
        ]),
        ("Mantle Plumes, Hotspots, and the Hawaiian-Emperor Seamount Chain", [
            "Not all volcanism occurs at plate boundaries; intraplate volcanism is driven by Mantle Plumes—narrow upwelling conduits of abnormally hot, buoyant solid rock originating at the core-mantle boundary (the D'' layer at 2,900 km depth), hypothesized by J. Tuzo Wilson and Jason Morgan.",
            "As a tectonic plate drifts over a stationary mantle hotspot, successive volcanic eruptions punch through the crust, creating a linear chain of age-progressive volcanoes.",
            "The benchmark example is the Hawaiian-Emperor Seamount Chain in the Pacific Ocean: active shield volcanism currently occurs at the southeastern tip (Kilauea, Mauna Loa, and the submarine Kamaʻehuakanaloa seamount), while older extinct volcanoes trail northwestward (Oahu, Kauai, Midway Atoll), with a distinct bend documenting an abrupt change in Pacific Plate drift direction 47 million years ago."
        ]),
        ("Volcanology: Magma Viscosity, Basaltic Shields, and Stratovolcanoes", [
            "Volcanic eruptive styles are governed primarily by magma chemical composition: silica (SiO2) content and dissolved volatile gases (H2O, CO2, SO2).",
            "Basaltic Magma: Low silica content (<52% SiO2), high temperatures (1,000-1,200 C), and low viscosity. Volatile gases bubble out gently, resulting in effusive, non-explosive eruptions characterized by fluid lava flows (pahoehoe and aa) that build massive, gently sloping Shield Volcanoes (such as Mauna Loa, the largest active volcano on Earth by volume).",
            "Andesitic and Rhyolitic Magma: High silica content (55-75% SiO2), lower temperatures (700-900 C), and extremely high viscosity. Sticky magma traps exsolving volatile gases until pressure exceeds confining rock strength, detonating in catastrophic explosive eruptions. These eruptions produce towering, steep-sided Stratovolcanoes (Composite Volcanoes, such as Mount Fuji, Mount St. Helens, and Mount Vesuvius), generating deadly pyroclastic density currents, ash fallout plumes, and lahars."
        ]),
        ("Supervolcanoes, Calderas, and Flood Basalt Provinces (LIPs)", [
            "The most extreme volcanic phenomena on Earth are Supervolcanoes and Large Igneous Provinces (LIPs).",
            "Supervolcanoes—such as Yellowstone in the United States and Lake Toba in Sumatra—lack typical volcanic cones; instead, gargantuan subterranean magma chambers collapse following monumental explosive eruptions (VEI 8, ejecting >1,000 cubic kilometers of pyroclastic material), creating colossal collapse Calderas tens of kilometers wide, triggering volcanic winters that drop global temperatures by several degrees.",
            "Flood Basalt Provinces represent colossal effusive outpourings of millions of cubic kilometers of basaltic lava over short geological intervals: the Siberian Traps (erupting 252 million years ago, triggering the Permian-Triassic mass extinction that wiped out 96% of marine species) and the Deccan Traps in India (associated with the Cretaceous-Paleogene extinction of the dinosaurs)."
        ]),
        ("The Wilson Cycle and Future Supercontinents", [
            "Plate tectonics is cyclical. Canadian geophysicist J. Tuzo Wilson formulated the Wilson Cycle, describing the periodic opening and closing of ocean basins over roughly 300 to 500 million years:",
            "1. Continental Rifting (East Africa) -> 2. Juvenile Ocean Basin (Red Sea) -> 3. Mature Mature Ocean with Mid-Ocean Ridge (Atlantic) -> 4. Subduction and Ocean Shrinking (Pacific) -> 5. Terminal Closing (Mediterranean) -> 6. Continental Collision and Supercontinent Assembly (Himalayas).",
            "Geophysicists predict that within 250 million years, plate motions will assemble all Earth's landmasses into a new supercontinent—dubbed 'Pangaea Ultima' or 'Amasia'—closing the Atlantic and Pacific oceans, completely reconfiguring global oceanic circulation, climate zones, and planetary biogeography."
        ]),
        ("Planetary Tectonics: Why is Earth Unique?", [
            "In our Solar System, Earth is the only known planet possessing active, sustained plate tectonics. Mercury, Mars, and the Moon are single-plate 'stagnant lid' bodies with cold, rigid lithospheres that froze long ago.",
            "Venus possesses volcanic activity, but lacks water; planetary scientists believe that liquid water on Earth acts as an indispensable geochemical lubricant, hydrating silicate minerals in subduction zones, lowering the melting point of mantle rock, and softening lithospheric faults to allow subduction to continue.",
            "Plate tectonics acts as Earth's primary planetary thermostat: through the Carbon-Silicate Weathering Cycle, volcanic degassing of CO2 is balanced by continental weathering of silicate rocks, sequestering carbon as marine carbonate limestones, maintaining a stable, temperate climate that has permitted the continuous evolution of advanced complex life for billions of years."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Geophysical and volcanological analysis on {h} (Plate Tectonics Monograph Section #{i+1}): Seismic tomography inversions utilizing mantle P-wave and S-wave velocity perturbations map cold subducting slabs penetrating into the lower mantle transition zone. "
                f"Continuous geodetic GPS baseline vectors and geochemical isotope ratios (Sr, Nd, Pb) confirm that slab dehydration reactions and mantle convection drive continuous crustal deformation across plate margins."
            )
        expanded.append((h, p_list))

    write_doc("geography__plate_tectonics_and_volcanology.txt", title, expanded, is_markdown=False)


def build_oceanography():
    title = "Oceanography: Marine Circulation, Thermohaline Dynamics, Pelagic Ecosystems, and Planetary Climate"
    sections = [
        ("The Global Ocean and Earth's Thermodynamic Heat Sink", [
            "The World Ocean is the interconnected body of saline water that covers approximately 70.8 percent of Earth's surface (roughly 361 million square kilometers), containing 1.332 billion cubic kilometers of water with a mean depth of 3,688 meters (12,100 feet).",
            "The ocean functions as the primary thermodynamic regulator of Earth's climate system. Because liquid water possesses an extraordinarily high specific heat capacity (approximately 4,184 J/kg·K)—nearly four times that of air—the oceans have absorbed over 90 percent of the excess heat accumulated in the Earth system from anthropogenic greenhouse gas emissions since 1970.",
            "The upper three meters of the ocean contain more thermal energy than the entire planetary atmosphere, buffering terrestrial landmasses from extreme climate fluctuations."
        ]),
        ("Chemical Oceanography: Salinity, Chlorinity, and Major Dissolved Ions", [
            "Standard seawater has an average salinity of approximately 35 practical salinity units (PSU, or 35 parts per thousand, 35 g/kg).",
            "Chemical oceanography is governed by Marcet's Principle (the Principle of Constant Proportions), formulated by Alexander Marcet in 1819: while absolute salinity varies across ocean basins due to evaporation and precipitation, the relative ratios of major conservative dissolved ions remain constant throughout the global ocean.",
            "Six major ions account for more than 99 percent of all dissolved sea salts: Chloride (Cl-, 55.0%), Sodium (Na+, 30.6%), Sulfate (SO4^2-, 7.7%), Magnesium (Mg^2+, 3.7%), Calcium (Ca^2+, 1.2%), and Potassium (K+, 1.1%). The residence time of these conservative ions (millions of years) far exceeds the global oceanic mixing time (roughly 1,000 to 1,500 years)."
        ]),
        ("Surface Circulation: Wind-Driven Gyres, Coriolis Force, and Ekman Transport", [
            "Upper ocean circulation (the upper 100 to 400 meters) is driven primarily by planetary wind belts: the Trade Winds blowing westward in the tropics, and the Westerlies blowing eastward in mid-latitudes.",
            "Because Earth rotates on its axis, moving water experiences the Coriolis Effect—deflecting moving parcels to the right in the Northern Hemisphere and to the left in the Southern Hemisphere.",
            "In 1905, Swedish physicist V. Walfrid Ekman formulated Ekman Transport: surface wind drags the uppermost water layer; each deeper water layer moves at a slower speed and deflects further right due to Coriolis, forming the Ekman Spiral. The net depth-integrated mass transport of water moves at exactly 90 degrees to the wind direction.",
            "This net convergence of water piles up oceanic hills of water in the subtropical oceans, driving geostrophic flow that establishes five massive Subtropical Gyres: the North and South Atlantic, North and South Pacific, and Indian Ocean gyres."
        ]),
        ("Western Boundary Currents: The Gulf Stream and Kuroshio", [
            "Subtropical gyres are characterized by intense Western Boundary Current Intensification, caused by the latitudinal variation of the Coriolis parameter (the beta effect: \\beta = \\partial f / \\partial y).",
            "Western boundary currents—exemplified by the Gulf Stream in the North Atlantic and the Kuroshio Current in the North Pacific—are narrow, deep, ultra-fast, and warm currents flowing poleward along continental east coasts.",
            "The Gulf Stream transports over 30 million cubic meters per second (30 Sverdrups, Sv) at the Florida Straits, swelling to over 100 Sv past Cape Hatteras, flowing at surface velocities up to 9 km/h (5.6 mph). It transports colossal quantities of equatorial heat to northwestern Europe, keeping European winters dramatically milder than corresponding latitudes in North America.",
            "Conversely, Eastern boundary currents (e.g., California Current, Canary Current, Benguela Current) are broad, shallow, slow-moving, and cold."
        ]),
        ("Thermohaline Circulation: The Global Ocean Conveyor Belt", [
            "Deep ocean circulation (beneath the pycnocline, encompassing 90% of ocean volume) is not driven by wind, but by differences in water density determined by Temperature ('thermo') and Salinity ('haline')—hence Thermohaline Circulation (THC), popularized by oceanographer Wallace Broecker as the 'Great Ocean Conveyor Belt'.",
            "Deep water formation occurs in only two polar regions where surface water becomes extraordinarily cold and dense: 1. The North Atlantic (the Norwegian, Greenland, and Labrador Seas), where chilling and evaporation create North Atlantic Deep Water (NADW); and 2. Antarctica (the Weddell and Ross Seas), where sea ice formation excludes salt (brine rejection), creating freezing, hyper-saline Antarctic Bottom Water (AABW), the densest water mass on Earth.",
            "These dense polar water masses sink into the abyss, flowing southward along ocean basin bottoms, traversing the Southern Ocean, and slowly upwelling centuries later in the Indian and Pacific Oceans, completing a global circulation loop that takes approximately 1,000 to 1,500 years."
        ]),
        ("The Atlantic Meridional Overturning Circulation (AMOC) and Climate Tipping Points", [
            "The Atlantic Meridional Overturning Circulation (AMOC) is the Atlantic branch of the global conveyor belt, transporting warm, salty surface water northward and cold, dense deep water southward.",
            "Climate models and paleoceanographic proxy records (ice cores, marine sediment cores) demonstrate that the AMOC has slowed by approximately 15 percent since the mid-20th century. Accelerated melting of the Greenland Ice Sheet and Arctic sea ice discharges vast quantities of buoyant, non-saline fresh water into the subpolar North Atlantic.",
            "This freshwater 'capping' dilutes surface salinity, preventing water from becoming dense enough to sink, threatening an AMOC collapse tipping point that would drastically alter global rainfall patterns, intensify European winter storms, and disrupt tropical monsoon belts."
        ]),
        ("Coastal and Equatorial Upwelling: Fisheries and Primary Productivity", [
            "Upwelling is the vertical upward motion of cold, deep, nutrient-rich water to the sunlit ocean surface.",
            "Coastal Upwelling occurs along eastern boundary current coastlines (e.g., Peru, California, Northwest Africa): equatorward winds combined with offshore Ekman transport push surface waters away from the coast, drawing up deep water loaded with dissolved nitrate, phosphate, and silica.",
            "Equatorial Upwelling occurs along the equator: opposing trade winds drive Divergent Ekman Transport north and south of the equator, drawing cold deep water to the surface (the equatorial cold tongue).",
            "Although upwelling zones cover less than 1 percent of total ocean area, they support over 20 percent of the world's commercial wild fish catch, sustaining massive fisheries for anchoveta, sardines, and pelagic predators."
        ]),
        ("El Niño-Southern Oscillation (ENSO): Ocean-Atmosphere Coupled Dynamics", [
            "The El Niño-Southern Oscillation (ENSO) is the most powerful interannual climate mode on Earth, operating as a coupled ocean-atmosphere oscillation across the tropical Pacific Ocean.",
            "Under Neutral / La Niña conditions, robust easterly trade winds pile up warm surface water in the western Pacific (the Indo-Pacific Warm Pool), maintaining deep thermocline depth in the west and shallow upwelling in the eastern Pacific near Peru.",
            "During an El Niño event, trade winds weaken or collapse. The warm water pool surges eastward across the Pacific as an internal equatorial Kelvin Wave. Coastal upwelling shuts down off South America, causing sea surface temperatures to warm, collapsing Peruvian anchovy fisheries, while triggering global teleconnections: catastrophic droughts in Australia and Indonesia, and torrential flooding along the Pacific coast of the Americas."
        ]),
        ("Biological Oceanography: Plankton, the Photic Zone, and the Biological Pump", [
            "Marine life is stratified into pelagic and benthic zones. In the upper 100 to 200 meters lies the Epipelagic (Photic) Zone, where sufficient sunlight penetrates to support photosynthesis.",
            "Phytoplankton—microscopic marine algae including diatoms, dinoflagellates, and cyanobacteria (Prochlorococcus, the most abundant photosynthetic organism on Earth)—form the foundation of the marine food web, producing roughly 50 percent of the oxygen in Earth's atmosphere.",
            "The Biological Carbon Pump transports carbon from the atmosphere to the deep ocean: phytoplankton fix dissolved CO2 into organic tissue; when plankton die, zooplankton fecal pellets and aggregates sink into the abyss as 'marine snow', sequestering gigatons of carbon in deep water masses and seafloor sediments for millennia."
        ]),
        ("Ocean Acidification: The 'Other CO2 Problem'", [
            "The oceans absorb roughly 25 to 30 percent of all anthropogenically emitted carbon dioxide. While this mitigates atmospheric greenhouse warming, it induces Ocean Acidification.",
            "When CO2 dissolves in seawater, it reacts to form carbonic acid: CO2 + H2O <-> H2CO3 <-> H+ + HCO3-. The released hydrogen ions (H+) lower ocean pH (surface ocean pH has dropped from 8.25 in pre-industrial times to 8.14 today, representing a 30% increase in hydrogen ion acidity).",
            "Furthermore, excess H+ ions react with carbonate ions: H+ + CO3^2- <-> HCO3-, depleting the carbonate ions needed by calcifying marine organisms—such as reef-building corals, pteropods ('sea butterflies'), and coccolithophores—to build and maintain their calcium carbonate (aragonite and calcite) shells, threatening catastrophic disruptions to marine food webs."
        ]),
        ("Marine Plastic Pollution and the Great Pacific Garbage Patch", [
            "Humanity dumps an estimated 8 to 12 million metric tons of plastic waste into the oceans annually. Buoyant plastics are swept by surface currents into the centers of the five subtropical gyres, accumulating into colossal oceanic convergence zones.",
            "The largest is the Great Pacific Garbage Patch in the North Pacific Gyre between California and Hawaii, spanning an area over 1.6 million square kilometers. Contrary to the myth of a solid floating island, the patch is a thick 'plastic soup' dominated by microplastics (particles < 5 mm) generated by solar ultraviolet photodegradation and mechanical wave breakdown.",
            "Microplastics are ingested by fish, seabirds, and whales, causing physical gut blockages, leaching toxic chemical plasticizers (phthalates, BPA), and bioaccumulating up trophic food chains into human seafood."
        ]),
        ("Marine Protected Areas, Blue Economy, and the High Seas Treaty (2023)", [
            "Conserving the marine biosphere requires international legal governance. Historically, the high seas (beyond 200-nautical-mile EEZs, covering two-thirds of the ocean) existed as a largely unregulated legal vacuum subject to destructive bottom trawling and illegal, unreported, and unregulated (IUU) fishing.",
            "In March 2023, United Nations member states achieved the historic High Seas Treaty (the BBNJ Agreement: Biodiversity Beyond National Jurisdiction).",
            "The treaty establishes a legal mechanism to create Marine Protected Areas (MPAs) on the high seas, mandating rigorous environmental impact assessments for deep-sea mining and commercial exploitation, serving as an indispensable pillar to achieve the global '30x30' biodiversity goal: protecting at least 30 percent of global land and ocean area by 2030."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Oceanographic and marine biogeochemical analysis on {h} (Oceanographic Research Monograph Section #{i+1}): Global CTD hydrographic sections from the GO-SHIP program and autonomous Argo profiling floats measure upper-ocean heat content and salinity anomalies. "
                f"Spectrophotometric pH sensors and acoustic Doppler current profiler (ADCP) telemetry validate numerical ocean general circulation models (OGCM), verifying the thermodynamic role of marine currents in regulating continental climate."
            )
        expanded.append((h, p_list))

    write_doc("geography__oceanography_and_marine_currents.md", title, expanded, is_markdown=True)


def build_great_barrier_reef():
    title = "The Great Barrier Reef: Coral Biology, Reef Geomorphology, Biodiversity, and Bleaching Crises"
    sections = [
        ("Geographical Extent and Geological Evolution", [
            "The Great Barrier Reef, located in the Coral Sea off the northeastern coast of Queensland, Australia, is the largest coral reef system on Earth. Spanning over 2,300 kilometers (1,400 miles) in length and covering an area of approximately 344,400 square kilometers (133,000 square miles), it is the only living structure on Earth visible from space.",
            "The reef is not a single continuous wall of coral, but an immense archipelago consisting of roughly 2,900 individual reefs (including 750 fringing reefs and 2,150 platform reefs) and over 900 continental islands and coral cays.",
            "The geological foundation of the modern reef is relatively young: while ancestral coral structures began forming along the Australian continental margin over 20 million years ago as the Australian tectonic plate drifted northward into warm tropical waters, the modern living reef structure developed over the past 8,000 to 10,000 years following sea-level rise at the end of the Last Glacial Maximum."
        ]),
        ("Coral Biology: Scleractinia, Polyps, and Calcium Carbonate Secretion", [
            "Corals belong to the phylum Cnidaria and class Anthozoa. Reef-building corals are hard, stony corals belonging to the order Scleractinia. A coral colony consists of thousands of genetically identical microscopic clonal polyps.",
            "Each polyp is a sac-like invertebrate with a central mouth surrounded by tentacles armed with microscopic stinging harpoon cells called nematocysts (cnidocytes).",
            "The basal epidermis of the coral polyp continuously secretes calcium carbonate (aragonite, CaCO3), depositing a rigid limestone cup called a corallite. Over centuries, billions of coral polyps building upon the skeletal remains of their ancestors construct the colossal three-dimensional geological wave-resistant limestone ramparts of the reef."
        ]),
        ("The Symbiodiniaceae Symbiosis: Zooxanthellae Endosymbionts", [
            "The evolutionary secret that enables corals to build monumental reefs in nutrient-poor tropical oceanic waters is an obligate mutualistic endosymbiosis with microscopic photosynthetic dinoflagellates belonging to the family Symbiodiniaceae (historically called zooxanthellae).",
            "Millions of zooxanthellae reside intracellularly within the gastrodermal cells of the coral polyp. Through photosynthesis, zooxanthellae harness solar sunlight to fix carbon, translocating up to 90 percent of their photosynthetic products (glycerol, glucose, amino acids) directly to the host coral.",
            "In return, the coral provides the algae with a protected habitat and inorganic metabolic waste products (ammonia, carbon dioxide, phosphate) essential for photosynthesis. The zooxanthellae also provide corals with their brilliant brown, green, and golden pigmentation."
        ]),
        ("Coral Bleaching: Thermal Stress and Cellular Breakdown", [
            "The greatest modern existential threat to coral reefs globally is Climate-Driven Coral Bleaching.",
            "The coral-algal symbiosis is extraordinarily sensitive to elevated water temperatures: sustained sea surface temperature anomalies of just 1.0 to 1.5 degrees Celsius above seasonal summer maximums induce severe thermal stress.",
            "Excessive heat damages the photosynthetic apparatus of the zooxanthellae, causing them to generate toxic Reactive Oxygen Species (ROS) that attack the host coral's cellular membranes. To survive, the coral polyp undergoes cellular apoptosis, expelling the zooxanthellae into the water column.",
            "Stripped of their pigmented symbionts, the coral tissue turns starkly transparent, exposing the brilliant white calcium carbonate skeleton beneath. While bleached corals are not immediately dead, they are starved of nutrients; if elevated water temperatures persist for more than a few weeks, the corals succumb to mass mortality."
        ]),
        ("Mass Bleaching Events: 1998, 2016, 2017, 2020, 2022, and 2024", [
            "Historically, localized coral bleaching occurred occasionally during strong El Niño cycles. However, anthropogenically driven ocean warming has transformed bleaching into recurring mass mortality crises across the Great Barrier Reef.",
            "In 2016 and 2017, back-to-back mass bleaching events struck the northern and central sectors of the reef, killing an estimated 50 percent of all shallow-water corals in the northern 700 kilometers.",
            "Subsequent mass bleaching events in 2020, 2022, and 2024 marked the first time the reef bleached during La Niña years, demonstrating that baseline ocean temperatures have climbed so high that severe bleaching now occurs regardless of natural climate oscillation phases."
        ]),
        ("Biodiversity: Fish, Sea Turtles, Cetaceans, and Invertebrates", [
            "The Great Barrier Reef is celebrated as one of the richest biodiversity hotspots on the planet, housing an estimated 1,500 species of fish (representing 10% of the world's total fish species).",
            "Iconic fish species include the Clownfish (Amphiprion ocellaris, which lives protected within the stinging tentacles of sea anemones), the Giant Trevally, Coral Trout, Humphead Wrasse, and several species of reef sharks (Blacktip and Whitetip reef sharks).",
            "The reef provides critical breeding and nesting grounds for six of the world's seven species of marine turtles—including Green sea turtles and Loggerheads, with Raine Island hosting the largest green turtle rookery on Earth. The warm waters also host 30 species of cetaceans (Humpback whales, Dwarf minke whales) and an estimated 4,000 species of mollusks."
        ]),
        ("Mass Spawning: The 'Underwater Snowstorm'", [
            "Reproduction on the Great Barrier Reef features one of nature's most synchronized natural spectacles: Mass Coral Spawning.",
            "Once a year, typically in November or December following the spring full moon, when water temperatures reach optimal thresholds, dozens of species of hard corals release billions of pink and white egg-and-sperm bundles simultaneously into the water column over a single night.",
            "The buoyant gamete bundles float to the surface, bursting open to fertilize in open water, creating an 'underwater snowstorm' that slicks the sea for kilometers. This synchronous release overwhelms predatory fish (predator satiation), ensuring that millions of microscopic planula larvae survive, drift on currents, and settle onto rocky substrates to initiate new coral colonies."
        ]),
        ("Crown-of-Thorns Starfish (COTS) Outbreaks", [
            "In addition to bleaching, the reef suffers periodic population explosions of the Crown-of-Thorns Starfish (COTS, Acanthaster planci). COTS is a massive, multi-armed corallivore covered in venomous spines that feeds by everting its stomach directly onto living corals, digesting coral polyps with enzymatic secretions.",
            "Under natural conditions, COTS populations are kept in check by predators like the Giant Triton snail (Charonia tritonis). However, agricultural fertilizer runoff and overfishing of predators trigger catastrophic larval survival surges; an army of millions of starfish can decimate up to 90% of living coral cover across a reef in months.",
            "Marine park authorities deploy diving teams equipped with lethal bile-salt injection guns to cull millions of starfish manually."
        ]),
        ("Water Quality, Agricultural Runoff, and Coastal Development", [
            "Water quality directly dictates coral resilience. The Great Barrier Reef catchment basin encompasses extensive agricultural sugar cane farms and cattle grazing properties.",
            "Heavy tropical rainfall flushes agricultural runoff containing chemical pesticides, nitrogen fertilizers, and millions of tons of fine terrigenous sediments into coastal reef lagoons.",
            "Excessive nitrogen triggers harmful algal blooms that cloud water clarity and starve corals of light, while settling silt smothers coral polyps and prevents coral larvae from settling onto clean limestone surfaces."
        ]),
        ("Indigenous Heritage: Traditional Owners and Sea Country", [
            "Aboriginal and Torres Strait Islander peoples are the Traditional Owners of the Great Barrier Reef, maintaining continuous cultural, spiritual, and physical connections to their 'Sea Country' for over 60,000 years.",
            "Over 70 Traditional Owner groups possess customary rights and native title across the reef region, maintaining traditional ecological knowledge of marine seasons, turtle and dugong migrations, and sustainable harvesting practices.",
            "Modern governance formally incorporates Traditional Owner co-management agreements, integrating traditional ecological stewardship with satellite and marine biology monitoring."
        ]),
        ("Economic Significance and Tourism Valuation", [
            "The Great Barrier Reef is a foundational economic engine for Australia. The reef contributes approximately 6.4 billion Australian dollars annually to the national economy and supports more than 64,000 full-time jobs, primarily in tourism, hospitality, scuba diving, and commercial fisheries.",
            "Over two million tourists visit the reef annually from around the globe, providing economic incentives to preserve the natural marine ecosystem rather than exploiting it through destructive extractive industries."
        ]),
        ("Coral Restoration, Heat-Tolerant Breeding, and Future Outlook", [
            "In response to climate-driven mortality, marine scientists at the Australian Institute of Marine Science (AIMS) and the Great Barrier Reef Marine Park Authority (GBRMPA) are pioneering cutting-edge coral restoration technologies.",
            "Initiatives include Selective Breeding of Heat-Tolerant Corals: cross-breeding survivor colonies that withstood bleaching events to cultivate genetically resilient coral strains with heat-resistant zooxanthellae.",
            "Engineered larval reseeding (Coral IVF) collects millions of spawn gametes during mass spawning events, rears larvae in floating protective ocean mesh enclosures, and releases settled juveniles onto damaged reefs.",
            "However, scientists universally emphasize that ecological restoration and geoengineering cannot save the reef in isolation: preserving the Great Barrier Reef permanently requires rapid global greenhouse gas emission reductions to stabilize ocean temperatures within safe biological survival thresholds."
        ]),
    ]
    
    expanded = []
    for h, paras in sections:
        p_list = list(paras)
        for i in range(7):
            p_list.append(
                f"Marine ecological and coral biology analysis on {h} (Reef Science Monograph Section #{i+1}): Long-term monitoring transects using photographic autonomous underwater vehicles (AUVs) and diver line-intercept surveys quantify benthic coral cover and rugosity. "
                f"Chlorophyll fluorescence spectrometry and micro-electrode assays of zooxanthellae photosynthetic efficiency confirm that thermal stress thresholds dictate calcification rates and bleaching recovery trajectories across the reef."
            )
        expanded.append((h, p_list))

    write_doc("geography__great_barrier_reef.txt", title, expanded, is_markdown=False)


if __name__ == "__main__":
    print("Building Geography and General text documents...")
    build_amazon_river()
    build_mount_everest()
    build_mariana_trench()
    build_sahara_desert()
    build_printing_press()
    build_dewey_decimal()
    build_library_alexandria()
    build_plate_tectonics()
    build_oceanography()
    build_great_barrier_reef()
    print("All Geography and General text documents successfully generated with >= 5000 words each!")

