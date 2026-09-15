#ifndef WORD_SEARCH_DATASET_H
#define WORD_SEARCH_DATASET_H

#include <Arduino.h>
#include "WordSearchGen.h"

struct ThemeDef {
    const char* name;
    const char* words[12];
};

static const size_t NUM_WS_THEMES_PER_DIFF = 50;

static const ThemeDef EASY_THEMES[NUM_WS_THEMES_PER_DIFF] PROGMEM = {
    {
        "Farm Animals",
        {"HORSE", "SHEEP", "CHICK", "DUCKS", "GOATS", "CALVES", "PONY", "MULES", "LLAMA", "BUNNY", "TURKEY", "PIGLET"}
    },
    {
        "Breakfast",
        {"TOAST", "BACON", "BAGEL", "JUICE", "MILKS", "CREPE", "WAFFLE", "FRUIT", "JELLY", "BUTTER", "CEREAL", "MUFFIN"}
    },
    {
        "Colors",
        {"BLACK", "WHITE", "GREEN", "AMBER", "BROWN", "PURPLE", "SILVER", "YELLOW", "ORANGE", "VIOLET", "BRONZE", "GOLDEN"}
    },
    {
        "Sweet Treats",
        {"CANDY", "DONUT", "FUDGE", "JELLY", "MINTS", "PASTRY", "COOKIE", "TAFFY", "SUNDAE", "SUGAR", "SWEETS", "WAFER"}
    },
    {
        "Weather",
        {"CLOUDS", "FROST", "STORMS", "SUNNY", "RAINS", "SNOWY", "WINDS", "SLEET", "BREEZE", "CHILLY", "SHOWER", "WARMTH"}
    },
    {
        "Playground",
        {"SWINGS", "SLIDES", "SEESAW", "CLIMB", "HOOPS", "BALLS", "BENCH", "GAMES", "CHASE", "TUNNEL", "RINGS", "VAULT"}
    },
    {
        "Pets at Home",
        {"PUPPY", "KITTEN", "PARROT", "FERRET", "LIZARD", "CANARY", "TURTLE", "POODLE", "RABBIT", "BEAGLE", "GECKO", "FELINE"}
    },
    {
        "Garden Blooms",
        {"TULIPS", "DAISY", "ROSES", "ORCHID", "PANSY", "LILIES", "LOTUS", "CLOVER", "VIOLET", "POPPY", "PEONY", "BLOOM"}
    },
    {
        "Shapes & Math",
        {"SQUARE", "CIRCLE", "VERTEX", "SPHERE", "PRISM", "ANGLES", "POINTS", "SHAPES", "CURVES", "SECTOR", "CUBES", "CONES"}
    },
    {
        "Clothing",
        {"SHIRTS", "PANTS", "JACKET", "SOCKS", "SCARF", "GLOVES", "BOOTS", "SHOES", "DRESS", "BELTS", "VESTS", "HOODIE"}
    },
    {
        "Ocean Creatures",
        {"SHARKS", "WHALES", "SEALS", "URCHIN", "CRABS", "SQUIDS", "OTTERS", "CLAMS", "CORALS", "SHRIMP", "WALRUS", "SALMON"}
    },
    {
        "Camping Trip",
        {"TENTS", "CABIN", "TRAILS", "WOODS", "FLASKS", "BOOTS", "FLAME", "HIKING", "ROPES", "FLARES", "FOREST", "PACKS"}
    },
    {
        "Forest Trees",
        {"CEDARS", "BIRCH", "MAPLES", "WILLOW", "PINES", "SPRUCE", "WALNUT", "POPLAR", "TIMBER", "GROVE", "BRANCH", "LEAVES"}
    },
    {
        "Friendly Bugs",
        {"BEETLE", "CICADA", "WEEVIL", "SPIDER", "MOTHS", "HORNET", "MANTIS", "WASPS", "APHID", "DRAGON", "LOCUST", "FLEAS"}
    },
    {
        "Flying Birds",
        {"EAGLES", "ROBINS", "FALCON", "HAWKS", "DOVES", "RAVENS", "PARROT", "HERONS", "FINCH", "CANARY", "OSPREY", "PIGEON"}
    },
    {
        "In the Kitchen",
        {"SPOONS", "FORKS", "KNIVES", "PLATES", "BOWLS", "GLASS", "APRONS", "POTS", "MIXERS", "KETTLE", "DISHES", "LADLE"}
    },
    {
        "Sports & Play",
        {"SOCCER", "TENNIS", "HOCKEY", "RUGBY", "SKATER", "SWIMS", "SURFER", "TRACKS", "BOXING", "SKIING", "ROWING", "GOLFER"}
    },
    {
        "Beach Day",
        {"SANDS", "WAVES", "TIDES", "SHELLS", "TOWELS", "SHORES", "COASTS", "DUNES", "DRIFTS", "WATERS", "SURFS", "SPLASH"}
    },
    {
        "Circus Fun",
        {"CLOWNS", "TIGERS", "RINGS", "MAGICS", "HOOPS", "STILTS", "TRICKS", "PARADE", "CHEERS", "SHOWS", "LIGHTS", "JUGGLE"}
    },
    {
        "Fruit Basket",
        {"APPLES", "BANANA", "ORANGE", "CHERRY", "GRAPES", "MANGOS", "LEMONS", "PEACHY", "MELONS", "BERRY", "PAPAYA", "GUAVA"}
    },
    {
        "Vegetable Patch",
        {"CARROT", "RADISH", "TOMATO", "POTATO", "ONIONS", "PEPPER", "CELERY", "GARLIC", "BEANS", "TURNIP", "SQUASH", "GREENS"}
    },
    {
        "School Days",
        {"PENCIL", "ERASER", "RULERS", "DESKS", "BOOKS", "CHALKS", "RECESS", "LUNCH", "PAPERS", "PAINTS", "STUDY", "LESSON"}
    },
    {
        "Cozy Bedroom",
        {"PILLOW", "SHEETS", "CLOSET", "LAMPS", "ALARMS", "MIRROR", "QUILTS", "DUVET", "DRAPES", "CARPET", "STAND", "CHEST"}
    },
    {
        "Clean Bathroom",
        {"TOWELS", "SOAPS", "BRUSH", "SINKS", "FAUCET", "DRAINS", "SPONGE", "LOTION", "MIRROR", "BUBBLE", "SHOWER", "RINSE"}
    },
    {
        "Family Members",
        {"MOTHER", "FATHER", "SISTER", "COUSIN", "UNCLES", "NIECES", "NEPHEW", "FAMILY", "PARENT", "INFANT", "BABIES", "ELDER"}
    },
    {
        "Community Helpers",
        {"DOCTOR", "NURSES", "POLICE", "BAKERS", "PILOTS", "FARMER", "CHEFS", "JUDGES", "ARTIST", "DRIVER", "CLERKS", "GUARDS"}
    },
    {
        "Vehicles & Rides",
        {"TRUCKS", "TRAINS", "PLANES", "BOATS", "CANOES", "SUBWAY", "WAGONS", "FERRY", "CARTS", "GLIDER", "MOTOR", "YACHT"}
    },
    {
        "Picnic Outdoors",
        {"BASKET", "NAPKIN", "CHEESE", "BREADS", "DRINKS", "CRISPS", "SALADS", "COOLER", "SNACKS", "PLATES", "FRUITS", "SWEETS"}
    },
    {
        "Toolbox",
        {"HAMMER", "SCREWS", "NAILS", "DRILLS", "PLIERS", "WRENCH", "LEVELS", "CHISEL", "RULERS", "VISES", "MALLET", "BLADES"}
    },
    {
        "Castle Realm",
        {"KINGS", "QUEENS", "KNIGHT", "PRINCE", "CASTLE", "SHIELD", "SWORDS", "CROWNS", "TOWERS", "GUARDS", "THRONE", "PALACE"}
    },
    {
        "Birthday Bash",
        {"CANDLE", "RIBBON", "GAMES", "MUSICS", "DANCES", "CARDS", "CROWDS", "SMILES", "TREATS", "GIFTS", "PARTY", "FAVORS"}
    },
    {
        "Space Voyage",
        {"MOONS", "STARS", "PLANET", "COMETS", "ROCKET", "ORBITS", "METEOR", "CRATER", "COSMOS", "LUNAR", "SOLAR", "PROBES"}
    },
    {
        "Happy Feelings",
        {"JOYFUL", "CALMLY", "BRAVE", "SILLY", "PROUD", "CHEERY", "SMILES", "KINDLY", "SWEET", "MERRY", "GENTLE", "LAUGHS"}
    },
    {
        "Airport Travel",
        {"TICKET", "PILOTS", "PLANES", "RUNWAY", "TRAVEL", "GATES", "FLIGHT", "RADARS", "ENGINE", "CABINS", "WINGS", "CARGO"}
    },
    {
        "Jungle Trek",
        {"MONKEY", "TIGERS", "PARROT", "TOUCAN", "SNAKES", "JAGUAR", "LIANAS", "JUNGLE", "RIVERS", "BAMBOO", "CANOPY", "OCELOT"}
    },
    {
        "Treehouse",
        {"LADDER", "ROPES", "PLANKS", "SECRET", "SHACKS", "BRANCH", "SHADOW", "CLIMBS", "PERCH", "NESTLE", "POSTS", "WOODEN"}
    },
    {
        "Ice Cream Parlor",
        {"SCOOPS", "WAFFLE", "CONES", "CHERRY", "SYRUPS", "SUNDAE", "FLOATS", "SHAKES", "GELATO", "BOWLS", "FLAVOR", "CREAMY"}
    },
    {
        "Musical Sounds",
        {"GUITAR", "VIOLIN", "DRUMS", "PIANOS", "FLUTES", "HARPS", "BANJOS", "CELLOS", "ORGANS", "BUGLES", "HORNS", "CHORDS"}
    },
    {
        "Winter Cold",
        {"SLEDS", "MITTEN", "SCARFS", "ICICLE", "SKATES", "IGLOOS", "FROSTY", "POLARS", "DRIFTS", "BOOTS", "COATS", "TUNDRA"}
    },
    {
        "Spring Awakening",
        {"PUDDLE", "SPROUT", "SEEDS", "BREEZE", "ROBINS", "BLOOMS", "MEADOW", "GROWTH", "GREENS", "NESTS", "FLOWER", "SUNNY"}
    },
    {
        "Autumn Harvest",
        {"ACORNS", "LEAVES", "SQUASH", "CIDERS", "BARNS", "RAKES", "BALES", "CRISPY", "AMBERS", "CROPS", "FIELDS", "BASKET"}
    },
    {
        "Summer Sunshine",
        {"POOLS", "TOWELS", "SUNNY", "CRABS", "FLOATS", "DIVING", "SURFS", "PICNIC", "SHADES", "COOLER", "SPLASH", "BEACH"}
    },
    {
        "Desert Sands",
        {"CAMELS", "CACTUS", "DUNES", "OASIS", "PALMS", "GECKOS", "VIPERS", "SANDS", "COBRAS", "MIRAGE", "CANYON", "LIZARD"}
    },
    {
        "River Rapids",
        {"CANOES", "PADDLE", "RAPIDS", "RIVERS", "STREAM", "TROUTS", "OTTERS", "SHORES", "DRIFTS", "ROCKYS", "WATERS", "KAYAKS"}
    },
    {
        "Sci-Fi World",
        {"FLYING", "SAUCER", "ALIENS", "CRATER", "LASERS", "ROBOTS", "RADARS", "PROBES", "CLOAKS", "GALAXY", "CYBORG", "WARPS"}
    },
    {
        "Cozy Cabin",
        {"TEAPOT", "QUILTS", "CHAIRS", "PORCH", "HEARTH", "CANDLE", "PANTRY", "KETTLE", "NOOKS", "TIMBER", "LOGS", "STOVE"}
    },
    {
        "Super Heroes",
        {"FLIGHT", "SPEEDY", "SHIELD", "LASERS", "POWERS", "FORCES", "HEROES", "CLOAKS", "ENERGY", "VISION", "BLASTS", "CAPES"}
    },
    {
        "City Streets",
        {"STREET", "BRIDGE", "TOWERS", "PARKS", "STATUE", "SQUARE", "CORNER", "ALLEYS", "PLAZAS", "CLOCKS", "AVENUE", "MARKET"}
    },
    {
        "Wizards & Magic",
        {"WANDS", "POTION", "CLOAKS", "CHARMS", "SPELLS", "SCROLL", "WIZARD", "BROOMS", "SPARKS", "MYSTIC", "CASTS", "CURSE"}
    },
    {
        "Backyard Garden",
        {"LAWNS", "HOSES", "MOWERS", "FENCES", "PATIOS", "BENCH", "GRILLS", "TREES", "GRASSY", "WEEDS", "SHADES", "GARDEN"}
    },
};

static const ThemeDef MEDIUM_THEMES[NUM_WS_THEMES_PER_DIFF] PROGMEM = {
    {
        "Coffee Culture",
        {"ESPRESSO", "BARISTA", "ROAST", "CARAMEL", "BREW", "AROMA", "STEEP", "POUROVER", "DRIPPER", "FROTH", "BEANS", "GRINDER"}
    },
    {
        "Solar System",
        {"PLANETS", "JUPITER", "MERCURY", "NEPTUNE", "METEOR", "GALAXY", "ASTEROID", "ORBIT", "CRATER", "ECLIPSE", "STAR", "VENUS"}
    },
    {
        "National Parks",
        {"CANYON", "GEYSER", "VALLEY", "REDWOOD", "GLACIER", "BOULDER", "SUMMIT", "TRAIL", "FOREST", "MEADOW", "PEAK", "TERRAIN"}
    },
    {
        "Detective Mystery",
        {"SLEUTH", "CIPHER", "SUSPECT", "ALIBI", "SHADOW", "MYSTERY", "PUZZLE", "CLUE", "WITNESS", "INSPECT", "SECRET", "HINT"}
    },
    {
        "Baking Kitchen",
        {"DOUGH", "PRETZEL", "CINNAMON", "VANILLA", "NUTMEG", "FLOUR", "BATTER", "PASTRY", "BRIOCHE", "ROLL", "YEAST", "CRUST"}
    },
    {
        "Marine Biology",
        {"DOLPHIN", "OCTOPUS", "JELLY", "ANEMONE", "CORAL", "LOBSTER", "MOLLUSK", "MANATEE", "PLANKTON", "SEAHORSE", "WHALE", "TURTLE"}
    },
    {
        "Classical Music",
        {"SYMPHONY", "CONCERTO", "SONATA", "MAESTRO", "QUARTET", "OVERTURE", "CHORD", "HARMONY", "MELODY", "VIOLIN", "PIANO", "TEMPO"}
    },
    {
        "Woodworking",
        {"HARDWOOD", "CHISEL", "JOINERY", "SHAPER", "BLADE", "TIMBER", "DOWEL", "PLANE", "VARNISH", "GRAIN", "ROUTER", "GROOVE"}
    },
    {
        "Board Games",
        {"CARD", "CHECKERS", "DOMINOES", "STRATEGY", "SPINNER", "ROLL", "SHUFFLE", "DICE", "PAWN", "TACTIC", "PLAYER", "TILES"}
    },
    {
        "Architecture",
        {"COLUMN", "FACADE", "ARCHWAY", "CAPITAL", "ROTUNDA", "BALCONY", "DOME", "PILLAR", "CORRIDOR", "VAULT", "ARCH", "PARAPET"}
    },
    {
        "Road Trip",
        {"HIGHWAY", "MOTORWAY", "ROADSIDE", "LUGGAGE", "JOURNEY", "COMPASS", "TOURIST", "MILE", "CRUISE", "SCENIC", "ROUTE", "CARAVAN"}
    },
    {
        "Photography",
        {"APERTURE", "SHUTTER", "EXPOSURE", "FOCUS", "PORTRAIT", "DARKROOM", "CONTRAST", "LIGHT", "TRIPOD", "LENS", "FLASH", "FRAMING"}
    },
    {
        "Botany & Flora",
        {"BLOSSOM", "FOLIAGE", "SEEDLING", "NUTRIENT", "STAMEN", "PETAL", "LEAF", "CONIFER", "ROOT", "BRANCH", "STEM", "FLORA"}
    },
    {
        "Desert Life",
        {"MEERKAT", "SCORPION", "SAGUARO", "COYOTE", "SAND", "ARID", "DUNE", "OASIS", "CANYON", "VIPER", "MINERAL", "REPTILE"}
    },
    {
        "Rainforest",
        {"CANOPY", "TROPICS", "JAGUAR", "FROG", "HUMID", "MONSOON", "VINE", "PARROT", "TOUCAN", "FOREST", "ORCHID", "MOSS"}
    },
    {
        "Winter Sports",
        {"LUGE", "BIATHLON", "CURLING", "BOBSLED", "SLALOM", "SKATE", "GLIDE", "RINK", "SNOW", "DOWNHILL", "SKIER", "BLIZZARD"}
    },
    {
        "Aviation",
        {"AIRPLANE", "AVIATOR", "ALTITUDE", "RADAR", "PILOT", "TERMINAL", "WING", "FUSELAGE", "COCKPIT", "FLIGHT", "LANDING", "RUNWAY"}
    },
    {
        "Mountain Peaks",
        {"RIDGE", "ALPINIST", "SUMMIT", "CREVASSE", "GLACIER", "SNOW", "SLOPE", "CLIFF", "ALTITUDE", "CLIMBER", "ASCENT", "PLATEAU"}
    },
    {
        "Cinema & Film",
        {"DIRECTOR", "PRODUCER", "PREMIERE", "SCENE", "FEATURE", "ACTOR", "COSTUME", "LIGHT", "FILM", "THEATER", "CINEMA", "STUDIO"}
    },
    {
        "Medieval Lore",
        {"FORTRESS", "BALLISTA", "CATAPULT", "CROSSBOW", "GATE", "BASTION", "CRUSADER", "KNIGHT", "ARMOR", "SHIELD", "LANCE", "CASTLE"}
    },
    {
        "Gemstones",
        {"DIAMOND", "SAPPHIRE", "EMERALD", "AMETHYST", "QUARTZ", "PERIDOT", "JADE", "GARNET", "TOPAZ", "OPAL", "CRYSTAL", "RUBY"}
    },
    {
        "Ocean Voyage",
        {"CLIPPER", "SCHOONER", "MARINER", "NAVIGATE", "COMPASS", "NAUTICAL", "HARBOR", "HORIZON", "SAIL", "VOYAGE", "HELM", "CAPTAIN"}
    },
    {
        "Bakery Treats",
        {"MUFFIN", "BAGUETTE", "ECLAIR", "MACARON", "TURNOVER", "SCONE", "LOAF", "CUPCAKE", "TART", "DANISH", "STRUDEL", "BREAD"}
    },
    {
        "Urban Transit",
        {"METRO", "COMMUTER", "TRANSFER", "STATION", "TROLLEY", "SUBWAY", "RAILCAR", "PLATFORM", "TRAIN", "EXPRESS", "TRACK", "TERMINUS"}
    },
    {
        "Craft Brewing",
        {"FERMENT", "BREWERY", "ALEHOUSE", "MALT", "BARREL", "FLAVOR", "HOPS", "CASK", "BEER", "DRAFT", "PILSNER", "STOUT"}
    },
    {
        "Tropical Isle",
        {"CORAL", "LAGOON", "ATOLL", "COCONUT", "HAMMOCK", "BREEZE", "TROPICAL", "ISLAND", "SHORE", "SUNNY", "PALM", "BEACH"}
    },
    {
        "Archaeology",
        {"ARTIFACT", "RELIC", "EXCAVATE", "TRENCH", "MONUMENT", "PYRAMID", "ANCIENT", "SITE", "POTTERY", "RUIN", "PHARAOH", "FOSSIL"}
    },
    {
        "Science Lab",
        {"REAGENT", "BEAKER", "TESTTUBE", "PIPETTE", "COMPOUND", "MOLECULE", "ELEMENT", "REACTION", "CRYSTAL", "FORMULA", "ACID", "SOLVENT"}
    },
    {
        "Vintage Cars",
        {"ROADSTER", "MOTOR", "COUPE", "SEDAN", "CHASSIS", "EXHAUST", "IGNITION", "RADIATOR", "GEARBOX", "CLUTCH", "VINTAGE", "TIRE"}
    },
    {
        "World Rivers",
        {"AMAZON", "COLORADO", "DANUBE", "RHINE", "YANGTZE", "MEKONG", "GANGES", "NILE", "ESTUARY", "DELTA", "RIVER", "STREAM"}
    },
    {
        "Mythology",
        {"CENTAUR", "MINOTAUR", "CERBERUS", "PEGASUS", "CYCLOPS", "OLYMPUS", "GORGON", "HERO", "NEPTUNE", "TITAN", "GODS", "LEGEND"}
    },
    {
        "Fitness & Gym",
        {"BARBELL", "DUMBBELL", "WORKOUT", "AEROBIC", "LIFT", "STRENGTH", "CARDIO", "STRETCH", "IRON", "TRAINING", "STAMINA", "FITNESS"}
    },
    {
        "Library Room",
        {"ARCHIVE", "CATALOG", "ALCOVE", "EDITION", "VOLUME", "CHAPTER", "READING", "BOOK", "JOURNAL", "PAGE", "BINDING", "BOOKCASE"}
    },
    {
        "Wildlife Park",
        {"ANTELOPE", "BUFFALO", "CHEETAH", "ELEPHANT", "FLAMINGO", "GORILLA", "HYENA", "IMPALA", "LEOPARD", "MEERKAT", "LION", "ZEBRA"}
    },
    {
        "Symphony Hall",
        {"WOODWIND", "TROMBONE", "BASSOON", "TIMPANI", "BRASS", "VIBRATO", "ALLEGRO", "CHOIR", "MAESTRO", "ENSEMBLE", "CONCERT", "OVERTURE"}
    },
    {
        "Tea Ceremony",
        {"INFUSER", "EARLGREY", "OOLONG", "LEAF", "JASMINE", "TEACUP", "INFUSION", "HERBAL", "STEEP", "MATCHA", "KETTLE", "BREW"}
    },
    {
        "Winter Cabin",
        {"FIREWOOD", "SNOWSHOE", "CHIMNEY", "KINDLING", "THERMAL", "FLANNEL", "FROST", "BLANKET", "HEARTH", "CABIN", "SNOW", "WINTER"}
    },
    {
        "Rugged Coast",
        {"CLIFF", "HEADLAND", "TIDEPOOL", "BARRIER", "SEAGULL", "REEF", "MARINA", "SURF", "COASTAL", "WAVE", "SHORE", "CURRENT"}
    },
    {
        "Culinary Arts",
        {"SAUTE", "POACH", "BRAISE", "SIMMER", "SEASON", "JULIENNE", "ROAST", "GARNISH", "MARINADE", "CHEF", "REDUCE", "BAKE"}
    },
    {
        "Volcanoes",
        {"MAGMA", "CALDERA", "ERUPTION", "VOLCANIC", "OBSIDIAN", "PUMICE", "VENT", "CINDER", "TEPHRA", "BASALT", "CRATER", "LAVA"}
    },
    {
        "Clean Energy",
        {"SUNLIGHT", "TURBINE", "WINDMILL", "BIOFUEL", "SOLAR", "STORAGE", "INVERTER", "GRID", "POWER", "PANEL", "ELECTRIC", "WATT"}
    },
    {
        "Rivers & Lakes",
        {"WATER", "OXBOW", "STREAM", "RIVER", "FLOW", "RAPIDS", "CHANNEL", "LAKE", "SHORE", "CURRENT", "BASIN", "POND"}
    },
    {
        "Forest Ecology",
        {"MUSHROOM", "SOIL", "MYCELIUM", "MOSS", "CANOPY", "WOODLAND", "HABITAT", "SEED", "FERN", "ROOT", "BARK", "TREE"}
    },
    {
        "Horology",
        {"PENDULUM", "CLOCK", "DIAL", "WATCH", "CHIME", "BALANCE", "QUARTZ", "SUNDIAL", "GEAR", "HOUR", "SPRING", "TICK"}
    },
    {
        "Printing Press",
        {"TYPESET", "FONT", "WOODCUT", "PRINTING", "PLATE", "PAGE", "ENGRAVE", "PRESS", "TYPE", "FOLIO", "PAPER", "IMPRINT"}
    },
    {
        "Castles & Moats",
        {"KEEP", "BRIDGE", "BARBICAN", "RAMPART", "GATE", "DUNGEON", "TURRET", "CITADEL", "MOAT", "WALL", "TOWER", "BASTION"}
    },
    {
        "Space Science",
        {"UNIVERSE", "NEBULA", "TELESCOP", "SPECTRA", "STAR", "LIGHT", "ORBIT", "QUANTUM", "ATOM", "MOON", "PAYLOAD", "COSMOS"}
    },
    {
        "Farmstead",
        {"TRACTOR", "SILO", "HARVEST", "PASTURE", "BARN", "GRANARY", "CORN", "ORCHARD", "CROP", "PLOW", "FIELD", "WHEAT"}
    },
    {
        "Carnival Midway",
        {"CAROUSEL", "FERRIS", "RIDE", "POPCORN", "SHOW", "FUNHOUSE", "PRIZE", "ARCADE", "TENT", "TICKET", "CLOWN", "GAME"}
    },
    {
        "Cellular Biology",
        {"BACTERIA", "PATHOGEN", "ORGANISM", "ANTIBODY", "IMMUNITY", "VACCINE", "CELL", "GENE", "CULTURE", "MEMBRANE", "ENZYME", "PROTEIN"}
    },
};

static const ThemeDef HARD_THEMES[NUM_WS_THEMES_PER_DIFF] PROGMEM = {
    {
        "Paleontology",
        {"FOSSILS", "DINOSAUR", "CARNIVORE", "EXCAVATE", "SEDIMENT", "SKELETON", "PREHISTOR", "AMMONITE", "PTEROSAUR", "JURASSIC", "HERBIVORE", "BONES"}
    },
    {
        "Renaissance Art",
        {"MASTERWORK", "PERSPECT", "SCULPTURE", "APPRENTICE", "PORTRAIT", "WORKSHOP", "FLORENCE", "FRESCO", "CANVAS", "GALLERY", "STUDIO", "PALETTE"}
    },
    {
        "Oceanography",
        {"TRENCH", "BATHYSCAPH", "ECOSYSTEM", "SUBMARINE", "CURRENT", "ABYSSAL", "BENTHIC", "PLANKTON", "CRUSTACEAN", "MARINELIFE", "SEABED", "VOYAGE"}
    },
    {
        "Astrophysics",
        {"EXOPLANET", "CONSTELL", "GRAVITY", "TELESCOPE", "SUPERNOVA", "RADIATION", "STARBURST", "CELESTIAL", "MAGNETIC", "NEBULA", "PULSAR", "BLACKHOLE"}
    },
    {
        "Atmospheric Science",
        {"STRATOSPHE", "TROPOSPHER", "BAROMETER", "ANEMOMETER", "TURBULENCE", "WEATHER", "HUMIDITY", "CYCLONE", "PRESSURE", "TORNADO", "CLIMATE", "BREEZE"}
    },
    {
        "Cryptography",
        {"ENCRYPTION", "DECRYPTION", "ALGORITHM", "CIPHERTEXT", "SIGNATURE", "KEYPAIR", "BLOCKCHAIN", "HASHVALUE", "PRIVATEKEY", "SECRETKEY", "CIPHER", "DIGITAL"}
    },
    {
        "Ancient Civilizations",
        {"BABYLON", "HIEROGLYPH", "SARCOPHAG", "ZIGGURAT", "CUNEIFORM", "ARCHAEOLOG", "PAPYRUS", "CENTURION", "GLADIATOR", "PYRAMID", "EMPIRE", "AQUEDUCT"}
    },
    {
        "Neurobiology",
        {"SYNAPSE", "CEREBELLUM", "DENDRITE", "NEURON", "CORTICAL", "BRAINSTEM", "NEUROPATHY", "PLASTICITY", "AXONAL", "RECEPTOR", "REFLEX", "MEMORY"}
    },
    {
        "Classical Mythology",
        {"PROMETHEUS", "EPIMETHEUS", "ANDROMEDA", "LABYRINTH", "PERSEPHONE", "MINOTAUR", "POLYPHEMUS", "MYTHOLOGY", "HEPHAESTUS", "AGAMEMNON", "HERCULES", "OLYMPUS"}
    },
    {
        "World Literature",
        {"PROTAGON", "ANTAGONIST", "METAPHOR", "SOLILOQUY", "NARRATIVE", "LITERATURE", "POETRY", "DRAMATURGY", "SYMBOLISM", "FORESHADOW", "STANZA", "HYPERBOLE"}
    },
    {
        "Maritime History",
        {"IRONCLAD", "PRIVATEER", "BATTLESHIP", "BUCCANEER", "NAVIGATION", "FLAGSHIP", "MERCHANT", "ADMIRALTY", "SEAFARER", "FRIGATE", "SAILOR", "HARBOR"}
    },
    {
        "Volcanology",
        {"MAGMATIC", "CALDERA", "ERUPTION", "VOLCANO", "FUMAROLE", "SEISMOLOGY", "CRATER", "OBSIDIAN", "BASALTIC", "ASHCLOUD", "LAVAFLOW", "TEPHRA"}
    },
    {
        "Botany & Taxonomy",
        {"ANGIOSPERM", "GYMNOSPERM", "CHLOROPHYL", "FLOWER", "HERBARIUM", "TAXONOMY", "SEEDLING", "POLLEN", "GERMINATE", "BRYOPHYTE", "FOLIAGE", "PLANTS"}
    },
    {
        "Architecture Styles",
        {"BRUTALIST", "NEOGOTHIC", "NEOCLASSIC", "CANTILEVER", "COLONNADE", "ROMANESQUE", "PILLAR", "ARCHWAY", "BAROQUE", "FACADE", "CATHEDRAL", "ROTUNDA"}
    },
    {
        "Modern Philosophy",
        {"EXISTENCE", "PHILOSOPHY", "DETERMIN", "METAPHYSIC", "EMPIRICISM", "PHENOMENON", "RATIONAL", "LOGICAL", "PRAGMATIC", "ETHICAL", "CONCEPT", "MORALITY"}
    },
    {
        "Culinary Techniques",
        {"CARAMEL", "FERMENT", "EMULSIFY", "CONFIT", "REDUCTION", "GASTRONOMY", "FLAMBE", "MACERATE", "PASTEURIZE", "BLANCH", "SEASON", "MARINADE"}
    },
    {
        "Geomorphology",
        {"SEDIMENT", "ALLUVIAL", "EROSION", "CONTINENT", "METAMORPH", "TECTONIC", "STRATA", "FAULTLINE", "WEATHERING", "BEDROCK", "CANYON", "PLATEAU"}
    },
    {
        "Entomology",
        {"CHRYSALIS", "EXOSKELETO", "ANTENNA", "MANDIBLE", "ARTHROPOD", "PHEROMONE", "CARAPACE", "COCOON", "INSECT", "BEETLE", "LARVAE", "WINGS"}
    },
    {
        "Linguistics",
        {"MORPHOLOGY", "PHONOLOGY", "SYNTACTIC", "SEMANTIC", "ETYMOLOGY", "CONSONANT", "DIPHTHONG", "LANGUAGE", "GRAMMAR", "ALPHABET", "DIALECT", "VOWELS"}
    },
    {
        "Microbiology",
        {"ANTIBIOTIC", "PROKARYOTE", "EUKARYOTE", "MICROSCOPE", "PETRIDISH", "PATHOGENIC", "ENDOSPORE", "MICROBIAL", "BACTERIA", "ORGANISM", "VIRUS", "CELLULAR"}
    },
    {
        "Medieval Warfare",
        {"SIEGETOWER", "BROADSWORD", "BATTLE", "CHAINMAIL", "CROSSBOW", "BARRICADE", "STRONGHOLD", "WARHAMMER", "CATAPULT", "LONGBOW", "ARMOR", "KNIGHT"}
    },
    {
        "Cinematic Arts",
        {"SCREENPLAY", "STORYBOARD", "SOUNDTRACK", "COMPOSITOR", "FILMMAKER", "DOCUMENT", "ANIMATION", "DIRECTOR", "SCENARIO", "PROJECTOR", "ACTOR", "CINEMA"}
    },
    {
        "Space Exploration",
        {"SPACECRAFT", "ASTRONAUT", "COSMONAUT", "PROPULSION", "LAUNCHPAD", "SPACEPROBE", "ROCKET", "ORBITAL", "SATELLITE", "PAYLOAD", "LANDER", "MISSION"}
    },
    {
        "Meteorological Wonders",
        {"WATERSPOUT", "SUPERCELL", "TORNADO", "HURRICANE", "LIGHTNING", "DOWNBURST", "WHITEOUT", "THUNDER", "BLIZZARD", "MONSOON", "STORMS", "CYCLONE"}
    },
    {
        "Cartography",
        {"TOPOGRAPHY", "LATITUDE", "LONGITUDE", "CARTOGRAPH", "HEMISPHERE", "COORDINATE", "ELEVATION", "COMPASS", "MAPPING", "SCALE", "MERIDIAN", "ORIENTEER"}
    },
    {
        "Musical Mastery",
        {"ORCHESTRA", "HARPSICHOR", "POLYPHONIC", "TIMPANI", "CONCERTO", "HARMONY", "MELODIC", "PERCUSSION", "CONDUCTOR", "CADENZA", "SYMPHONY", "TEMPO"}
    },
    {
        "Glaciology",
        {"ICEBERG", "PERMAFROST", "GLACIATION", "MORAINE", "SUBGLACIAL", "CREVASSE", "POLARCAP", "PACKICE", "FROST", "TUNDRA", "GLACIER", "SNOWFIELD"}
    },
    {
        "Horology Science",
        {"ESCAPEMENT", "TOURBILLON", "CHRONOMETR", "TIMEPIECE", "PENDULUM", "MAINSPRING", "MECHANISM", "OSCILLATE", "REGULATOR", "BALANCE", "MOVEMENT", "STOPWATCH"}
    },
    {
        "Marine Ecology",
        {"BIODIVERSE", "PLANKTON", "CONSERVE", "MANGROVE", "ESTUARY", "INTERTIDAL", "AQUATIC", "BIOMASS", "CORALREEF", "HABITAT", "OCEAN", "SEAGRASS"}
    },
    {
        "Optics & Light",
        {"REFRACTION", "DIFFRACT", "SPECTRUM", "PHOTONIC", "CHROMATIC", "PRISM", "ILLUMINATE", "MAGNIFIER", "REFLECTION", "OPTICAL", "LENSES", "LASERS"}
    },
    {
        "Genetics & DNA",
        {"CHROMOSOME", "NUCLEOTIDE", "MUTATION", "REPLICATE", "GENOMIC", "EPIGENETIC", "INHERIT", "GENETICS", "HELIX", "SEQUENCE", "CELLULAR", "HEREDITY"}
    },
    {
        "Acoustics & Sound",
        {"FREQUENCY", "REVERB", "RESONANCE", "DECIBEL", "ULTRASONIC", "WAVELENGTH", "INFRASONIC", "HARMONIC", "AMPLITUDE", "DIFFUSION", "SPECTRUM", "ACOUSTIC"}
    },
    {
        "Forestry Management",
        {"FORESTRY", "ARBORICULT", "TIMBERLAND", "OVERSTORY", "UNDERSTORY", "WOODLAND", "CANOPY", "SAPLING", "HARDWOOD", "PRESERVE", "SEEDTREE", "WILDLIFE"}
    },
    {
        "Metallurgy",
        {"FURNACE", "ANNEALING", "FORGING", "TEMPERING", "ALLOYSTEEL", "HARDENING", "EXTRUSION", "FOUNDRY", "SMELTING", "METALS", "CASTING", "INGOT"}
    },
    {
        "Ancient Rome",
        {"COLOSSEUM", "GLADIATOR", "CENTURION", "LEGION", "PATRICIAN", "PRAETORIAN", "AQUEDUCT", "CONSULATE", "REPUBLIC", "SENATE", "TRIBUNAL", "EMPEROR"}
    },
    {
        "Ornithology",
        {"PLUMAGE", "MIGRATION", "ORNITHOLOG", "INCUBATE", "PASSERINE", "TALONS", "FEATHERS", "TERRITORY", "RAPTOR", "CLUTCH", "FLIGHT", "SPECIES"}
    },
    {
        "Theoretical Physics",
        {"RELATIVITY", "QUANTUM", "SINGULAR", "PARTICLE", "SPACETIME", "GRAVITON", "COLLIDER", "UNIVERSE", "HIGGSBOSON", "ENERGY", "MATTER", "DIMENSION"}
    },
    {
        "Desert Landscapes",
        {"BADLANDS", "SANDSTONE", "PLATEAU", "DUNES", "CANYON", "ARROYO", "SAVANNA", "EROSION", "DESERT", "MIRAGE", "OASIS", "BOULDER"}
    },
    {
        "Printmaking",
        {"WOODBLOCK", "LITHOGRAPH", "INTAGLIO", "ENGRAVING", "AQUATINT", "ETCHING", "IMPRESSION", "WOODCUT", "PRINTMAKER", "STENCIL", "INKSTONE", "PAPER"}
    },
    {
        "Wilderness Survival",
        {"BUSHCRAFT", "SHELTER", "NAVIGATION", "FIRECRAFT", "FORAGING", "FIRSTAID", "CANTEEN", "SURVIVAL", "COMPASS", "PROVISION", "WILDERNESS", "BACKPACK"}
    },
    {
        "Deep Ocean Trenches",
        {"MARIANA", "HADALZONE", "DEEPSEA", "VENTPIPE", "SUBDUCTION", "PRESSURE", "ABYSSAL", "TRENCH", "OCEANBED", "SEAMOUNTS", "BATHYAL", "WATERS"}
    },
    {
        "Historical Expeditions",
        {"EXPEDITION", "VOYAGING", "EXPLORER", "DISCOVERY", "FRONTIER", "JOURNEY", "PATHFINDER", "CARAVAN", "NAVIGATOR", "COMPASS", "ADVENTURE", "PASSAGE"}
    },
    {
        "Prehistoric Mammals",
        {"MAMMOTH", "MASTODON", "SABERTOOTH", "FOSSILS", "PLEISTOCEN", "HERBIVORE", "PREHISTOR", "CARNIVORE", "ANCIENT", "BEASTS", "TUSKS", "EXTINCT"}
    },
    {
        "Biochemistry",
        {"METABOLISM", "AMINOACID", "GLYCOLYSIS", "PEPTIDE", "SYNTHESIS", "NUCLEIC", "CATALYSIS", "PHOSPHATE", "PROTEIN", "ENZYME", "MOLECULE", "ORGANIC"}
    },
    {
        "Epic Poetry",
        {"HEXAMETER", "ALLITERATE", "STANZA", "APOSTROPHE", "INVOCATION", "LEGEND", "RHAPSODIST", "MYTHIC", "STROPHES", "BALLAD", "CANTOS", "HEROIC"}
    },
    {
        "Subterranean Caves",
        {"STALACTITE", "STALAGMITE", "SPELEOTHEM", "SPELUNKING", "FLOWSTONE", "CAVERN", "GROTTO", "PASSAGE", "SINKHOLE", "LIMESTONE", "CHAMBER", "BEDROCK"}
    },
    {
        "Ecology & Biomes",
        {"BIOSPHERE", "BIODIVERSE", "RAINFOREST", "SAVANNAH", "TUNDRA", "ECOLOGY", "FOODCHAIN", "POPULATION", "HABITAT", "ECOSYSTEM", "PRAIRIE", "WETLAND"}
    },
    {
        "Space Robotics",
        {"AUTONOMOUS", "ROBOTIC", "ROVERWHEEL", "TELEMETRY", "SOLARPANEL", "ALGORITHM", "SPACEPROBE", "ACTUATOR", "PAYLOAD", "LANDER", "SENSOR", "AVIONICS"}
    },
    {
        "Renaissance Philosophy",
        {"HUMANISM", "NEOPLATON", "INDIVIDUAL", "SECULAR", "RENAISSAN", "REASON", "SCHOLASTIC", "RATIONAL", "PHILOSOPHY", "THINKER", "LOGIC", "IDEAS"}
    },
    {
        "Weather Extremes",
        {"MICROBURST", "HEATWAVE", "BLIZZARD", "COLDFRONT", "DUSTDEVIL", "THUNDER", "HURRICANE", "CYCLONE", "MONSOON", "DOWNPOUR", "GALEFORCE", "TORRENT"}
    },
};

inline const ThemeDef* getWordSearchPool(WordSearchDifficulty diff, size_t& outCount) {
    outCount = NUM_WS_THEMES_PER_DIFF;
    switch (diff) {
        case WS_EASY:
            return EASY_THEMES;
        case WS_HARD:
            return HARD_THEMES;
        case WS_MEDIUM:
        default:
            return MEDIUM_THEMES;
    }
}

#endif // WORD_SEARCH_DATASET_H
