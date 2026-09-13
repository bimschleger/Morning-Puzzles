#ifndef WHEEL_DATASET_H
#define WHEEL_DATASET_H

#include <Arduino.h>

struct WheelPuzzleDef {
    char center;
    char outer[7];
    const char* pangram;
    uint8_t wordCount;
    uint8_t good;
    uint8_t great;
    uint8_t genius;
    const char* sampleWords[16];
    uint8_t numSampleWords;
};

static const size_t NUM_WHEEL_PUZZLES_PER_DIFF = 20;

static const WheelPuzzleDef EASY_WHEEL_PUZZLES[NUM_WHEEL_PUZZLES_PER_DIFF] PROGMEM = {
    {
        'E', "ANPRST", "APARTNESS", 38, 13, 24, 32,
        {"AENEAN", "AERATE", "ANAPAEST", "ANAPNEA", "ANARETA", "ANASTATE", "ANATASE", "ANEAR", "ANENST", "ANENT", "ANES", "ANNATES", "ANNET", "ANSATE", "ANTE", "ANTEATER"}, 16
    },
    {
        'E', "ADGNRS", "GANDERESS", 38, 13, 24, 32,
        {"ADAGE", "ADDED", "ADDEND", "ADDENDA", "ADDER", "ADDRESS", "ADDRESSEE", "ADDRESSER", "ADEAD", "ADENASE", "ADREAD", "AENEAN", "AERAGE", "AGED", "AGEDNESS", "AGEE"}, 16
    },
    {
        'E', "FLORSW", "FLOWERLESS", 38, 13, 24, 32,
        {"EELER", "EFFLOWER", "ELLE", "ELSE", "EROS", "EROSE", "ERROR", "ERRORLESS", "ESERE", "EWER", "EWERER", "FEEL", "FEELER", "FEELESS", "FEER", "FEERE"}, 16
    },
    {
        'E', "ABKLNT", "BLANKET", 38, 13, 24, 32,
        {"ABATABLE", "ABATE", "ABBLE", "ABELE", "ABET", "ABETTAL", "ABLATE", "ABLE", "ABNET", "AENEAN", "AKEAKE", "AKEE", "AKNEE", "ALATE", "ALBE", "ALBEE"}, 16
    },
    {
        'E', "ABCINT", "ABACINATE", 38, 13, 24, 32,
        {"ABACATE", "ABACINATE", "ABATE", "ABET", "ABIETATE", "ABIETENE", "ABIETIC", "ABIETIN", "ABIETINIC", "ABNET", "ACACETIN", "ACATE", "ACCENT", "ACCITE", "ACETACETIC", "ACETANNIN"}, 16
    },
    {
        'E', "AIPRST", "ASPERITE", 38, 13, 24, 32,
        {"AERATE", "AERIE", "AIRE", "AIRER", "AITESIS", "APATITE", "APEPSIA", "APER", "APEREA", "APERT", "APPEAR", "APPEARER", "APPEASE", "APPEASER", "APPET", "ASPERITE"}, 16
    },
    {
        'E', "ADORST", "ASSORTED", 38, 13, 24, 32,
        {"ADDED", "ADDER", "ADDORSED", "ADDRESS", "ADDRESSEE", "ADDRESSER", "ADDRESSOR", "ADDREST", "ADEAD", "ADET", "ADORE", "ADORER", "ADOSSED", "ADREAD", "ADSESSOR", "AERATE"}, 16
    },
    {
        'E', "AGHINT", "GAHNITE", 38, 13, 24, 32,
        {"AENEAN", "AGATE", "AGATINE", "AGEE", "AGEN", "AGENT", "AGHANEE", "AGITATE", "AGNATE", "ANATINE", "ANEATH", "ANENT", "ANIENTE", "ANNET", "ANNITE", "ANTE"}, 16
    },
    {
        'E', "GHILNP", "HELPING", 38, 13, 24, 32,
        {"EGGING", "EIGNE", "ELENGE", "ELLE", "ENGINE", "EPEE", "EPIGENE", "EPININE", "GEGG", "GEGGEE", "GEIN", "GELL", "GENE", "GENEP", "GENIE", "GENII"}, 16
    },
    {
        'E', "ADINPT", "DEPAINT", 38, 13, 24, 32,
        {"ADDED", "ADDEND", "ADDENDA", "ADEAD", "ADEEP", "ADENIA", "ADENINE", "ADEPT", "ADET", "ADIATE", "ADIPATE", "ADNATE", "AENEAN", "AIDE", "ANADENIA", "ANAPAITE"}, 16
    },
    {
        'E', "INOPRT", "ENTROPION", 38, 13, 24, 32,
        {"EERIE", "ENROOT", "ENTENTE", "ENTER", "ENTERER", "ENTERON", "ENTIRE", "ENTONE", "ENTROPION", "EREPTION", "INTERPOINT", "INTERPONE", "NONPROTEIN", "PERITENON", "PETITIONER", "PINNOTERE"}, 16
    },
    {
        'E', "MNORST", "MERESTONE", 38, 13, 24, 32,
        {"EMEER", "EMERSE", "EMMER", "EMMET", "EMOTE", "ENMOSS", "ENORM", "ENROOT", "ENSE", "ENSEEM", "ENSETE", "ENSTORE", "ENTENTE", "ENTER", "ENTERER", "ENTERMETE"}, 16
    },
    {
        'E', "DNORSW", "WONDERS", 38, 13, 24, 32,
        {"DEDO", "DEED", "DEEDEED", "DEER", "DEERWEED", "DEERWOOD", "DENDRON", "DENE", "DENSE", "DENSEN", "DENSENESS", "DERE", "DERN", "DESEED", "DESS", "DEWER"}, 16
    },
    {
        'E', "HNRSTU", "HUNTERS", 38, 13, 24, 32,
        {"EHEU", "ENRUT", "ENSE", "ENSETE", "ENSUE", "ENSUER", "ENSURE", "ENSURER", "ENTENTE", "ENTER", "ENTERER", "ENTHUSE", "ENTREE", "ENTRUST", "ENTURRET", "ENURE"}, 16
    },
    {
        'E', "ADLOPR", "LEOPARD", 38, 13, 24, 32,
        {"ADDED", "ADDER", "ADDLE", "ADEAD", "ADEEP", "ADELOPOD", "ADORE", "ADORER", "ADREAD", "AERO", "ALDER", "ALEE", "ALEPOLE", "ALLELE", "ALLER", "ALOE"}, 16
    },
    {
        'E', "AHNPRT", "PANTHER", 38, 13, 24, 32,
        {"AENEAN", "AERATE", "AHEAP", "ANAPNEA", "ANARETA", "ANEAR", "ANEATH", "ANENT", "ANNET", "ANTE", "ANTEATER", "ANTENNA", "ANTENNAE", "ANTENNATE", "ANTHER", "ANTRE"}, 16
    },
    {
        'E', "ACILNP", "APPLIANCE", 38, 13, 24, 32,
        {"ACLE", "ACNE", "AECIAL", "AENEAN", "AIEL", "AILE", "ALANINE", "ALCINE", "ALEC", "ALEE", "ALEN", "ALIEN", "ALIENEE", "ALLELE", "ALLELIC", "ALLENE"}, 16
    },
    {
        'E', "AHRSTV", "HARVEST", 38, 13, 24, 32,
        {"AERATE", "AESTHETE", "AREA", "AREAR", "ARETE", "ARRASTRE", "ARREAR", "ARREST", "ARRESTEE", "ARRESTER", "ARSE", "ARSES", "ASEETHE", "ASHERAH", "ASHES", "ASHET"}, 16
    },
    {
        'E', "CINOST", "CENOSITE", 38, 13, 24, 32,
        {"CENOSITE", "CENSE", "CENT", "CENTESIS", "CENTO", "CESS", "CESSION", "CEST", "CETENE", "CETI", "CETIC", "CETIN", "CICONINE", "CINE", "CINENE", "CISE"}, 16
    },
    {
        'E', "BLORST", "BOLSTER", 38, 13, 24, 32,
        {"BEBLESS", "BEBOSS", "BEELOL", "BEER", "BEES", "BEEST", "BEET", "BEETLE", "BEETLER", "BEETROOT", "BELEE", "BELETTER", "BELL", "BELLBOTTLE", "BELLE", "BELLOTE"}, 16
    },
};

static const WheelPuzzleDef MEDIUM_WHEEL_PUZZLES[NUM_WHEEL_PUZZLES_PER_DIFF] PROGMEM = {
    {
        'A', "GILNPY", "APPLYINGLY", 26, 9, 16, 22,
        {"AALII", "AGAIN", "AGAL", "AGING", "AGLA", "AGNAIL", "AILING", "ALALA", "ALAN", "ALANGIN", "ALANI", "ALANYL", "ALGA", "ALGAL", "ALGALIA", "ALGIN"}, 16
    },
    {
        'A', "GIKLNW", "WALKING", 26, 9, 16, 22,
        {"AALII", "AGAIN", "AGAL", "AGING", "AGLA", "AGNAIL", "AILING", "AIWAN", "AKALA", "AKIA", "AKIN", "ALALA", "ALAN", "ALANGIN", "ALANI", "ALGA"}, 16
    },
    {
        'O', "ABGINT", "BAGATTINO", 26, 9, 16, 22,
        {"ABATON", "ABBOT", "ABOON", "AGIO", "AGITATION", "AGNATION", "AGOG", "AGOING", "AGON", "AINOI", "AION", "AITION", "ANABO", "ANABONG", "ANGIOTONIN", "ANGO"}, 16
    },
    {
        'I', "FGNRSU", "SURFING", 26, 9, 16, 22,
        {"FIGGING", "FINING", "FINIS", "FIRING", "FIRN", "FIRRING", "FRIG", "FRINGING", "FUNGI", "FUNGIN", "FUNIS", "FURRING", "GIGUNU", "GING", "GINNING", "GIRN"}, 16
    },
    {
        'I', "ACGMNP", "CAMPAIGN", 26, 9, 16, 22,
        {"ACACIIN", "ACACIN", "ACAPNIA", "ACINIC", "ACMIC", "AGAIN", "AGAMI", "AGAMIAN", "AGAMIC", "AGING", "AIMING", "AMAIN", "AMANI", "AMANIA", "AMIC", "AMIMIA"}, 16
    },
    {
        'I', "AFGMNR", "FARMING", 26, 9, 16, 22,
        {"AFFAIR", "AFFIRM", "AGAIN", "AGAMI", "AGAMIAN", "AGING", "AGRARIAN", "AGRIA", "AGRIN", "AIMARA", "AIMING", "AIRAN", "AIRING", "AIRMAN", "AMAIN", "AMANI"}, 16
    },
    {
        'A', "CELNRT", "ACCELERANT", 26, 9, 16, 22,
        {"ACANA", "ACARA", "ACATE", "ACCA", "ACCELERANT", "ACCELERATE", "ACCENT", "ACCRETAL", "ACCRETE", "ACERATE", "ACERRA", "ACETAL", "ACETATE", "ACETRACT", "ACLE", "ACNE"}, 16
    },
    {
        'O', "CEJPRT", "PROJECT", 26, 9, 16, 22,
        {"CEPTOR", "CERO", "CEROTE", "CERRERO", "COCCO", "COCO", "COCOROOT", "COCOTTE", "COERCE", "COERCER", "COOEE", "COOER", "COOP", "COOPER", "COOREE", "COOT"}, 16
    },
    {
        'O', "ABCLNY", "BALCONY", 26, 9, 16, 22,
        {"ABOLLA", "ABOON", "ACCLOY", "ACCOY", "ALCO", "ALCYON", "ALLOY", "ANABO", "ANCON", "ANCONAL", "ANCONY", "ANNONA", "ANNOY", "ANOA", "ANON", "ANONOL"}, 16
    },
    {
        'I', "CEHMNY", "CHIMNEY", 26, 9, 16, 22,
        {"CHEMIC", "CHIC", "CHICHI", "CHIEN", "CHIH", "CHIME", "CHIMNEY", "CHIN", "CHINCH", "CHINCHE", "CHINE", "CHININ", "CHINNY", "CHYMIC", "CINCH", "CINE"}, 16
    },
    {
        'A', "CLRSTY", "CRYSTAL", 26, 9, 16, 22,
        {"ACALYCAL", "ACARA", "ACCA", "ACLYS", "ACRACY", "ACRYL", "ACRYLYL", "ACTA", "ACYL", "ALALA", "ALAR", "ALARY", "ALAS", "ALCATRAS", "ALLAY", "ALLY"}, 16
    },
    {
        'O', "EJNRUY", "JOURNEY", 26, 9, 16, 22,
        {"EJOO", "ENJOY", "ENJOYER", "ERROR", "EURYON", "JOEY", "JOREE", "JOURNEY", "JOURNEYER", "JUROR", "NEON", "NEURON", "NEURONE", "NOEYE", "NONE", "NONENE"}, 16
    },
    {
        'A', "EJMSTY", "MAJESTY", 26, 9, 16, 22,
        {"AJAJA", "AMAAS", "AMASS", "AMASTY", "AMMA", "ASEM", "ASSATE", "ASSAY", "ASSE", "ASSESS", "ASSESSEE", "ASSET", "ASSETS", "ASTA", "ASTAY", "ASTEAM"}, 16
    },
    {
        'O', "FIMNRU", "FUNIFORM", 26, 9, 16, 22,
        {"FIFO", "FIORIN", "FONO", "FORM", "FORMIN", "FORUM", "FOUN", "FOUR", "FROM", "FROOM", "FROUFROU", "FUNIFORM", "FUNORI", "FUROIN", "FUROR", "IMINO"}, 16
    },
    {
        'A', "EIMPRV", "PRIMAVERA", 26, 9, 16, 22,
        {"AERIE", "AEVIA", "AIMARA", "AIMER", "AIRE", "AIRER", "AMAPA", "AMAR", "AMIMIA", "AMIR", "AMMA", "AMMER", "AMPER", "AMPERE", "AMRA", "APAR"}, 16
    },
    {
        'O', "EFNRTU", "FORETURN", 26, 9, 16, 22,
        {"EFFORT", "ENFEOFF", "ENROOT", "ENTERON", "ENTONE", "ERROR", "FEOFF", "FEOFFEE", "FEOFFOR", "FERRETTO", "FETOR", "FONO", "FONT", "FOONER", "FOOT", "FOOTER"}, 16
    },
    {
        'I', "CELNPS", "PENCILS", 26, 9, 16, 22,
        {"CECILS", "CEIL", "CEILE", "CESSPIPE", "CILICE", "CINCLIS", "CINE", "CINEL", "CINENE", "CISE", "CISELE", "CLINE", "CLINIC", "CLIP", "CLIPEI", "CLIPS"}, 16
    },
    {
        'A', "CEFNRU", "FURNACE", 26, 9, 16, 22,
        {"ACANA", "ACARA", "ACCA", "ACCRUE", "ACCRUER", "ACERRA", "ACNE", "ACRE", "AENEAN", "AFACE", "AFAR", "AFARA", "AFEAR", "AFERNAN", "AFFA", "AFFEER"}, 16
    },
    {
        'O', "ACEGRU", "COURAGE", 26, 9, 16, 22,
        {"ACOR", "ACOREA", "AERO", "AERUGO", "AGOG", "AGOGE", "AGORA", "AGOUARA", "ARARAO", "ARGO", "AROAR", "AURORA", "AURORAE", "AURORE", "CACAO", "CARACORE"}, 16
    },
    {
        'A', "BINORW", "RAINBOW", 26, 9, 16, 22,
        {"ABIR", "ABOON", "ABRIN", "ABWAB", "AINOI", "AION", "AIRAN", "AIWAN", "ANABO", "ANAN", "ANANA", "ANBA", "ANION", "ANNA", "ANNONA", "ANOA"}, 16
    },
};

static const WheelPuzzleDef HARD_WHEEL_PUZZLES[NUM_WHEEL_PUZZLES_PER_DIFF] PROGMEM = {
    {
        'H', "DILNOP", "DOLPHIN", 16, 5, 10, 13,
        {"DHONI", "DHOON", "DOLLHOOD", "DOLPHIN", "HILL", "HIND", "HINOID", "HIPPO", "HIPPOID", "HIPPOPOD", "HOIN", "HOLD", "HOLL", "HOLLIN", "IODINOPHIL", "PINHOLD"}, 16
    },
    {
        'U', "HIMPRT", "TRIUMPH", 16, 5, 10, 13,
        {"HUMHUM", "HUMP", "HUMPH", "HURR", "HURT", "IRRUPT", "MUIR", "MUMP", "MURITI", "MURIUM", "MURMUR", "MURUMURU", "MUTH", "MUTT", "MUTUUM", "TRIUMPH"}, 16
    },
    {
        'H', "IMPRTU", "TRIUMPH", 16, 5, 10, 13,
        {"HIMP", "HUMHUM", "HUMP", "HUMPH", "HURR", "HURT", "MIRTH", "MUTH", "PHIT", "PHUT", "PITH", "PRUH", "RUTH", "THIR", "THIRT", "TRIUMPH"}, 16
    },
    {
        'K', "DGIMNO", "KINGDOM", 16, 5, 10, 13,
        {"DINK", "DODKIN", "DOOK", "GINK", "GINKGO", "GODDIKIN", "GODKIN", "GOOK", "KIKI", "KIMONO", "KIND", "KING", "KINGDOM", "KINK", "KINO", "KOINON"}, 16
    },
    {
        'W', "BEGINR", "BREWING", 16, 5, 10, 13,
        {"BEWIG", "BIGWIG", "BREW", "BREWER", "BREWING", "EWER", "EWERER", "GREENWING", "GREW", "GWINE", "IIWI", "NEWING", "REBREW", "RENEW", "RENEWER", "REWIN"}, 16
    },
    {
        'U', "CGILNR", "CURLING", 16, 5, 10, 13,
        {"CLUNG", "CUIR", "CULL", "CULLING", "CUNNING", "CURIN", "CURING", "CURL", "CURLING", "CURN", "CURR", "CURUCUCU", "GIGUNU", "GLUCINIC", "GLUG", "UNCURLING"}, 16
    },
    {
        'G', "DEHILT", "DELIGHT", 16, 5, 10, 13,
        {"DEGGED", "DELIGHT", "DELIGHTED", "DIGHT", "DIGIT", "EDGE", "EDGED", "EIGHT", "EIGHTH", "EIGHTIETH", "ELEGIT", "GEET", "GEGG", "GEGGEE", "GELD", "GELID"}, 16
    },
    {
        'U', "EFGIRS", "FIGURES", 16, 5, 10, 13,
        {"EFFUSE", "EUGE", "FERU", "FIGURE", "FIGURER", "FIGURES", "FISSURE", "FRISURE", "FUFF", "FUGU", "FUGUE", "FURFUR", "FURRIER", "FUSE", "FUSEE", "FUSS"}, 16
    },
    {
        'V', "AFLORS", "FLAVORS", 16, 5, 10, 13,
        {"ALVAR", "ARVAL", "AVAL", "FAVOR", "FAVORS", "FLAVO", "FLAVOR", "FLAVORS", "LARVA", "LARVAL", "LAVA", "OVAL", "OVOLO", "SALVO", "SALVOR", "SAVOLA"}, 16
    },
    {
        'W', "ADGINR", "DRAWING", 16, 5, 10, 13,
        {"ADAW", "ADAWN", "AIRWARD", "AIWAN", "AWAG", "AWARD", "AWIN", "AWING", "AWIWI", "AWNING", "DAWN", "DAWNING", "DRAWING", "GINWARD", "INDRAWING", "WARDING"}, 16
    },
    {
        'B', "AINOST", "ABISTON", 16, 5, 10, 13,
        {"ABAS", "ABASIA", "ABATIS", "ABATON", "ABBAS", "ABBASI", "ABBASSI", "ABBOT", "ABISTON", "ANTIBIOSIS", "BASIATION", "BASSOONIST", "BASTION", "BASTIONS", "BISONANT", "BOTANIST"}, 16
    },
    {
        'M', "ACEINS", "AMNESIC", 16, 5, 10, 13,
        {"ACME", "ACMIC", "ACNEMIA", "AMAAS", "AMAIN", "AMANI", "AMANIA", "AMASESIS", "AMASS", "AMEEN", "AMEN", "AMNESIC", "ANASEISMIC", "CINEMAS", "ECMNESIA", "ENNEASEMIC"}, 16
    },
    {
        'D', "ACEILT", "ACADIALITE", 16, 5, 10, 13,
        {"ACADIALITE", "ACILIATED", "CILIATED", "CITADEL", "DEICTICAL", "DELICATE", "DELTAIC", "DIALECT", "DIALECTAL", "DIALECTIC", "DIALECTICAL", "DICELLATE", "EDICTAL", "LACTIDE", "LATTICED", "LILACTIDE"}, 16
    },
    {
        'U', "CLMNOS", "COLUMNS", 16, 5, 10, 13,
        {"CLONUS", "COCCOUS", "COCCULUS", "COCCUS", "COCULLO", "COLLUM", "COLOSSUS", "COLUMN", "COLUMNS", "COMOUS", "CONCUSS", "CONSONOUS", "CONSUL", "CONUS", "MONOCULOUS", "MONOCULUS"}, 16
    },
    {
        'D', "CEINRS", "CINDERS", 16, 5, 10, 13,
        {"CEDE", "CEDER", "CEDRE", "CEDRENE", "CEDRIN", "CEDRINE", "CENDRE", "CERED", "CERIDE", "CINDERS", "DISCERN", "DISCERNER", "RESCIND", "RESCINDER", "RESIDENCE", "RESIDENCER"}, 16
    },
    {
        'V', "ACELOS", "ALCOVES", 16, 5, 10, 13,
        {"ALCOVE", "ALCOVES", "ALVEOLA", "ALVEOLE", "AVAL", "CALVE", "CALVES", "CASAVA", "CASAVE", "CAVA", "CAVAE", "CAVAL", "CAVALLA", "CAVE", "CAVEL", "CLAVA"}, 16
    },
    {
        'C', "AEILRS", "ECLAIRS", 16, 5, 10, 13,
        {"ACARA", "ACARI", "ACARIASIS", "ACCA", "ACCERSE", "ACCESS", "ACCESSLESS", "ACCRESCE", "ACERRA", "ACIER", "ACLE", "ACRASIA", "ACRE", "ECLAIRS", "SCLERIASIS", "SERCIAL"}, 16
    },
    {
        'G', "AEORTU", "OUTARGUE", 16, 5, 10, 13,
        {"AERAGE", "AERUGO", "AGAR", "AGATE", "AGEE", "AGER", "AGGER", "AGGERATE", "AGGRATE", "AGGREGATE", "AGGREGATOR", "OUTARGUE", "OUTRAGE", "OUTRAGER", "REOUTRAGE", "TUTORAGE"}, 16
    },
    {
        'M', "BELOPR", "PROBLEM", 16, 5, 10, 13,
        {"BEBLOOM", "BEMOLE", "BEPOMMEL", "BERM", "BLOOM", "BLOOMER", "BOMB", "BOMBER", "BOMBO", "BOOM", "BOOMER", "BREME", "BROME", "BROMOL", "BROOM", "PROBLEM"}, 16
    },
    {
        'Z', "ACDIOS", "ZODIACS", 16, 5, 10, 13,
        {"AZOIC", "CAZA", "DIAZOIC", "DISAZO", "DISDIAZO", "DIZOIC", "ISODIAZO", "ISOZOOID", "OOZOOID", "SIZZ", "ZIZZ", "ZOCCO", "ZODIAC", "ZODIACS", "ZOIC", "ZOID"}, 16
    },
};

#endif // WHEEL_DATASET_H
