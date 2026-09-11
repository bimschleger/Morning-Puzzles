#!/usr/bin/env python3
"""
300-Puzzle Jumble Dataset Generator & Multiset Validator
Generates 100 Easy, 100 Medium, 100 Hard puzzles where:
- Each puzzle has 4 to 6 clean, common vocabulary words.
- Designation of circled letter indices strictly matches the multiset
  of characters in the riddle answer:
  multiset(circled_letters) == multiset(clean_answer_letters)
- Outputs server/data/jumbles.json and esp32-firmware/src/generators/JumbleDataset.h
"""

import json
import re
import random
from collections import Counter
from typing import List, Dict, Any, Tuple, Optional

# Curated bank of 300 clever, family-friendly, newspaper-style pun riddles
# (100 Easy, 100 Medium, 100 Hard)
RIDDLE_BANK = {
    "easy": [
        ("Why did the coffee file a police report?", "IT GOT MUGGED"),
        ("What did the ocean say to the sailboat?", "NOTHING IT JUST WAVED"),
        ("Why do we tell actors to 'break a leg'?", "EVERY PLAY HAS A CAST"),
        ("What do you call a sleeping dinosaur?", "A DINO SNORE"),
        ("Why was the math book always sad?", "TOO MANY PROBLEMS"),
        ("Why can't a leopard hide anywhere?", "ALWAYS SPOTTED"),
        ("What do you call a factory that makes good products?", "SATISFACTORY"),
        ("Why did the tomato blush?", "IT SAW THE SALAD"),
        ("What kind of key opens a banana?", "A MONKEY"),
        ("Why did the golfer bring two pairs of pants?", "IN CASE OF A HOLE"),
        ("What do you call a fake noodle?", "AN IMPASTA"),
        ("Why did the picture go to jail?", "IT WAS FRAMED"),
        ("What do you call a bear with no teeth?", "A GUMMY BEAR"),
        ("Why do bees have sticky hair?", "HONEYCOMB"),
        ("Why was Cinderella bad at soccer?", "RAN FROM THE BALL"),
        ("What do elves learn in kindergarten?", "ELF ALPHABET"),
        ("Why did the scarecrow win an award?", "OUT IN HIS FIELD"),
        ("What do you call a pile of kittens?", "A MEOWTAIN"),
        ("Why couldn't the pony sing in the choir?", "A LITTLE HOARSE"),
        ("What did one wall say to the other?", "MEET AT THE CORNER"),
        ("What do you call cheese that isn't yours?", "NACHO CHEESE"),
        ("Why did the skeleton not go to the party?", "NO BODY TO GO WITH"),
        ("What do you call a sleeping bull?", "A BULLDOZER"),
        ("Why did the stadium get so hot?", "ALL THE FANS LEFT"),
        ("What kind of tree fits in your hand?", "A PALM TREE"),
        ("Why do birds fly south for winter?", "TOO FAR TO WALK"),
        ("What did the zero say to the eight?", "NICE BELT"),
        ("Why was the broom late for work?", "SWEPT IN"),
        ("What do you call an alligator in a vest?", "AN INVESTIGATOR"),
        ("Why did the banana go to the doctor?", "NOT PEELING WELL"),
        ("What runs all around a backyard without moving?", "A FENCE"),
        ("What has hands but cannot clap?", "A CLOCK"),
        ("What building has the most stories?", "A LIBRARY"),
        ("Why did the boy eat his homework?", "PIECE OF CAKE"),
        ("What gets wetter the more it dries?", "A TOWEL"),
        ("Why did the cookie visit the nurse?", "FELT CRUMMY"),
        ("What kind of room has no doors or windows?", "A MUSHROOM"),
        ("What goes up but never comes down?", "YOUR AGE"),
        ("What can you catch but never throw?", "A COLD"),
        ("Why do fish live in salt water?", "PEPPER MAKES SNEEZE"),
        ("What has one eye but cannot see?", "A NEEDLE"),
        ("What has legs but does not walk?", "A TABLE"),
        ("Why did the orange stop rolling down the hill?", "RAN OUT OF JUICE"),
        ("What kind of dog tells time?", "A WATCH DOG"),
        ("What do you call an elephant that doesn't matter?", "IRRELEPHANT"),
        ("Why did the bicycle fall over?", "IT WAS TWO TIRED"),
        ("What bow cannot be tied?", "A RAINBOW"),
        ("What kind of shoes do frogs wear?", "OPEN TOAD"),
        ("Why did the baseball player wear armor?", "IN THE CAGE"),
        ("What sits in a corner and travels the world?", "A STAMP"),
        ("Why do cows wear bells?", "HORNS DONT WORK"),
        ("What has a neck but no head?", "A BOTTLE"),
        ("What do you call a boomerang that doesn't work?", "A STICK"),
        ("Why did the duck get sent to the principal?", "WISE QUACKER"),
        ("What kind of music do planets like?", "NEPTUNES"),
        ("What starts with T, ends with T, and has T in it?", "A TEAPOT"),
        ("Why was the belt arrested?", "HELD UP PANTS"),
        ("What has teeth but cannot bite?", "A COMB"),
        ("Why did the tree go to the dentist?", "ROOT CANAL"),
        ("What has a thumb and four fingers but is not alive?", "A GLOVE"),
        ("Why did the chicken cross the playground?", "TO THE SLIDE"),
        ("What do you call a sleeping pie?", "A CREAM PUFF"),
        ("Why was the computer cold?", "LEFT WINDOWS OPEN"),
        ("What do you call a funny mountain?", "HILL ARIOUS"),
        ("What kind of candy never arrives on time?", "CHOC LATE"),
        ("Why did the turtle cross the road?", "SHELL PHONE"),
        ("What has words but never speaks?", "A BOOK"),
        ("What kind of car does an egg drive?", "A YOLKSWAGEN"),
        ("Why did the lamp get turned on?", "BRIGHT IDEA"),
        ("What do you call a pig that knows karate?", "PORK CHOP"),
        ("Why did the melon jump into the lake?", "WATER MELON"),
        ("What is brown, hairy, and wears sunglasses?", "COOL COCONUT"),
        ("Why do fish swim in schools?", "CANNOT WALK"),
        ("What has head, tail, is brown, and has no legs?", "A PENNY"),
        ("Why did the music teacher need a ladder?", "HIGH NOTES"),
        ("What do you call a cow with two legs?", "LEAN BEEF"),
        ("What kind of coat is best put on wet?", "PAINT COAT"),
        ("Why was the shoe late?", "TIED UP"),
        ("What travels around the world staying in one spot?", "A STAMP"),
        ("What do you call a deer with no eyes?", "NO EYE DEER"),
        ("Why did the dog sit in the shade?", "HOT DOG"),
        ("What kind of bird can write?", "A PEN GUIN"),
        ("What do you call a ghost's mistake?", "A BOO BOO"),
        ("Why did the astronaut break up with his girlfriend?", "NEEDED SPACE"),
        ("What do you call a magic dog?", "LABRACADABRADOR"),
        ("Why did the candle quit its job?", "BURNT OUT"),
        ("What has four wheels and flies?", "A GARBAGE TRUCK"),
        ("Why did the baker go to the bank?", "NEEDED DOUGH"),
        ("What kind of cup doesn't hold water?", "CUPCAKE"),
        ("Why did the farmer ride a donkey?", "HORSE TIRED"),
        ("What do you call a sheep with no legs?", "A CLOUD"),
        ("Why was the strawberry sad?", "IN A JAM"),
        ("What kind of insect is good at math?", "AN ACCOUNTANT"),
        ("Why did the guitar get upset?", "FRET NOT"),
        ("What do you call a happy farmer?", "JOLLY PLANTER"),
        ("Why did the duck buy lipstick?", "FOR HER BILL"),
        ("What has a heart of stone?", "AN ARTICHOKE"),
        ("Why did the painter go to school?", "MORE COLOR"),
        ("What do you call a dinosaur with great vocabulary?", "THESAURUS"),
        ("Why was the king only one foot tall?", "A RULER")
    ],
    "medium": [
        ("Why couldn't the skeleton cross the road?", "HAD NO GUTS TO DO IT"),
        ("What do you call a magician on a plane?", "FLYING SORCERER"),
        ("Why did the stadium roof leak?", "TOO MANY HOLES IN IT"),
        ("What did the grape say when it was stepped on?", "JUST LET OUT WINE"),
        ("Why did the invisible man turn down the job?", "COULD NOT SEE HIMSELF"),
        ("What do you call a lazy baby kangaroo?", "A POUCH POTATO"),
        ("Why did the crab never share his food?", "HE WAS SHELLFISH"),
        ("What do you call a snowman with a six pack?", "AN ABDOMINAL SNOWMAN"),
        ("Why did the clock get sent to detention?", "TICKED OFF TEACHER"),
        ("What do you call an owl that does magic?", "HOO DINI"),
        ("Why did the chef get kicked out of the kitchen?", "BEAT THE EGGS"),
        ("What kind of shoes do spies wear?", "SNEAKERS ALL DAY"),
        ("Why do bananas use sunscreen?", "THEY PEEL IN SUN"),
        ("What do you call a belt made of watches?", "A WAIST OF TIME"),
        ("Why did the detective go to bed?", "TO SLEEP ON CASE"),
        ("What kind of tea is hard to swallow?", "REALITY CHECK"),
        ("Why did the barber win the marathon?", "HE TOOK A SHORT CUT"),
        ("What do you call a bear caught in the rain?", "A DRIZZLY BEAR"),
        ("Why did the spider get a job in web design?", "GREAT WEB SKILLS"),
        ("What did the stamp say to the envelope?", "STICK WITH ME"),
        ("Why was the broom happy at home?", "SWEPT OFF ITS FEET"),
        ("What do you call a turtle taking photos?", "A SNAPPING TURTLE"),
        ("Why did the tree take a nap?", "FOR WOODEN REST"),
        ("What kind of dog loves bubble baths?", "A SHAMPOODLE"),
        ("Why did the cookie cry all night?", "MOTHER WAS A WAFER"),
        ("What do you call an artistic cat?", "A CLAW DRAWING"),
        ("Why did the tomato fail the driving test?", "RAN THROUGH RED LIGHT"),
        ("What do you call a fish wearing a bowtie?", "SO FISH TICATED"),
        ("Why did the math teacher bring graph paper?", "PLOTTING A PLAN"),
        ("What do you call an apology written in dots?", "RE MORSE CODE"),
        ("Why did the golfer wear three socks?", "GOT A HOLE IN ONE"),
        ("What kind of water cannot freeze?", "HOT WATER BOILS"),
        ("Why did the candle visit the doctor?", "FELT LIGHT HEADED"),
        ("What do you call a funny prank in the kitchen?", "A SILLY WHISK"),
        ("Why did the mirror look away?", "SAW RIGHT THROUGH"),
        ("What do you call a sleeping woodcutter?", "A SLUMBER JACK"),
        ("Why did the gardener plant lightbulbs?", "FOR POWER PLANTS"),
        ("What kind of tie does a pig wear?", "A PIG TIE"),
        ("Why did the pirate join the gym?", "FOR STRONG ARMS"),
        ("What do you call a duck that steals?", "A ROBBER DUCK"),
        ("Why did the orange go to court?", "APPEAL THE CASE"),
        ("What do you call a rabbit with fleas?", "BUGS BUNNY"),
        ("Why did the pencil get sharpeners dizzy?", "SPUN IN CIRCLES"),
        ("What kind of key has no teeth?", "A PIANO KEY"),
        ("Why was the blanket so warm and cozy?", "COVERED IN LOVE"),
        ("What do you call a bird that kicks high?", "A NINJA CHICKEN"),
        ("Why did the flashlight run away?", "OUT OF BATTERIES"),
        ("What do you call a clean pig?", "HAM AND SOAP"),
        ("Why did the river take music lessons?", "IMPROVE CURRENT"),
        ("What kind of tree loves high fives?", "A PALM TREE"),
        ("Why did the chef add sugar to the stew?", "SWEETEN THE DEAL"),
        ("What do you call a cow playing an instrument?", "A MOO SICIAN"),
        ("Why did the cloud stay in school?", "TO GET A DEGREE"),
        ("What do you call a tiny pepper?", "A LITTLE CHILLI"),
        ("Why did the violin take a bow?", "PLAYED GREAT TUNE"),
        ("What do you call a running train?", "A CONDUCTOR"),
        ("Why did the lemon fail the math test?", "SOUR OVER NUMBERS"),
        ("What do you call a flying bagel?", "PLAIN ON WINGS"),
        ("Why did the sailor bring a pencil?", "TO DRAW WATER"),
        ("What do you call an eagle that tells jokes?", "AN ILL EAGLE"),
        ("Why was the bread so polite to guests?", "WELL BRED FOLK"),
        ("What do you call a frozen dog?", "A CHILLY PUP"),
        ("Why did the painter wear two coats?", "HOUSE WAS COLD"),
        ("What do you call a dancing sheep?", "A BAALERINA"),
        ("Why did the watch take a day off?", "NEEDED TIME OUT"),
        ("What do you call a rabbit that knows martial arts?", "KUNG FU BUNNY"),
        ("Why did the onion cry during dinner?", "CHOPPED IN HALF"),
        ("What do you call a noisy insect?", "A CRICKET BAT"),
        ("Why did the shoe visit the hospital?", "HEEL WAS BROKEN"),
        ("What do you call a sleeping police car?", "A SNOOZE PATROL"),
        ("Why did the sponge work so hard?", "SOAKED UP KNOWLEDGE"),
        ("What do you call a funny frog?", "A RIBBITING COMIC"),
        ("Why did the calendar look worried?", "DAYS WERE NUMBERED"),
        ("What do you call a cold horse?", "A SHIVERING COLT"),
        ("Why did the wheel go to therapy?", "FELT BALANCED OUT"),
        ("What do you call a singing fish?", "A BASS SINGER"),
        ("Why did the lamp blush so red?", "SAW LIGHT BULB"),
        ("What do you call an alligator with maps?", "A NAVIGATOR"),
        ("Why did the door go to the doctor?", "HAD SQUEAKY JOINTS"),
        ("What do you call a cat on ice?", "COOL CAT SKATER"),
        ("Why did the farmer wear overalls?", "READY FOR HARVEST"),
        ("What do you call a royal bird?", "HER MAJESTY OWL"),
        ("Why did the compass spin around?", "LOST ITS BEARING"),
        ("What do you call a sweet monkey?", "CHIMP CANDY"),
        ("Why did the rope untie itself?", "TOO KNOTTY TO STAY"),
        ("What do you call a dog in summer?", "SUNNY RETRIEVER"),
        ("Why did the bell ring so loud?", "TO MAKE NOISE"),
        ("What do you call a dancing bear?", "BALLOON DANCER"),
        ("Why did the window close down?", "DRAFTY WEATHER"),
        ("What do you call a sleeping volcano?", "DORMANT CRATER"),
        ("Why did the bridge cross the river?", "TO REACH OTHER SIDE"),
        ("What do you call a smart horse?", "CLEVER TROTTER"),
        ("Why did the spoon leave the bowl?", "FINISHED SOUP"),
        ("What do you call a laughing flower?", "A CHUCKLING ROSE"),
        ("Why did the book stay on the shelf?", "BOOKED FOR DAY"),
        ("What do you call a quick rabbit?", "RAPID HOPPER"),
        ("Why did the clock tick backwards?", "REWIND TIME"),
        ("What do you call a sweet lion?", "DANDELION ROAR"),
        ("Why did the cloud cry all morning?", "RAINED ON PARADE"),
        ("What do you call a shiny beetle?", "GLOWING BUG")
    ],
    "hard": [
        ("Why did the archaeologist carry a magnifying glass?", "LOOKING FOR ANCIENT CLUES"),
        ("What do you call an astronomer who loves dessert?", "A MILKY WAY EXPLORER"),
        ("Why did the symphony orchestra visit the bank?", "TO MAKE A SOUND INVESTMENT"),
        ("What did the grandfather clock say to the watch?", "YOU HAVE TOO MUCH FREE TIME"),
        ("Why was the librarian so good at detective work?", "SHE WENT BY THE BOOK"),
        ("What do you call a dinosaur that smashes cars?", "TYRANNOSAURUS WRECKS"),
        ("Why did the submarine surface in the middle of winter?", "FOR A CHILLING EXPEDITION"),
        ("What do you call an artist who paints with vegetables?", "A CREATIVE SALAD MAKER"),
        ("Why did the mathematician build a campfire in winter?", "HE NEEDED DEGREES TO WARM UP"),
        ("What did the lighthouse say during the heavy storm?", "GUIDING THROUGH DARK WAVES"),
        ("Why did the newspaper reporter run through the forest?", "CHASING DOWN BREAKING NEWS"),
        ("What do you call a knight who won a spelling bee?", "CHAMPION OF NOBLE WORDS"),
        ("Why did the computer programmer go into farming?", "HE WANTED BETTER HARDWARE"),
        ("What do you call a penguin who loves detective novels?", "AN ICE COLD SLEUTH"),
        ("Why was the chemistry professor always so confident?", "ALL REACTIONS PROVED RIGHT"),
        ("What did the locomotive say to the mountain tunnel?", "CLEARING A DIRECT TRACK"),
        ("Why did the theater director hire an electrician?", "LIGHTING UP DRAMATIC SCENES"),
        ("What do you call an architect who builds sandcastles?", "SHORELINE MASTER CRAFTER"),
        ("Why did the deep sea diver carry an encyclopedia?", "EXPLORING DEEPER WISDOM"),
        ("What did the compass needle tell the explorer?", "POINTING TOWARD TRUE NORTH"),
        ("Why did the airline pilot become a landscape gardener?", "CRAVED SMOOTH LANDINGS"),
        ("What do you call a chef who won an Olympic gold medal?", "WORLD CLASS SKILLET MASTER"),
        ("Why was the history museum open until midnight?", "BRINGING PAST NIGHTS TO LIFE"),
        ("What did the telescope say to the distant nebula?", "EXPANDING COSMIC VISION"),
        ("Why did the mechanical watch refuse to run down?", "DRIVEN BY INNER SPRINGS"),
        ("What do you call a violinist playing on a sailboat?", "SAILING WITH SMOOTH NOTES"),
        ("Why did the botany scientist talk to the oak tree?", "NATURAL BRANCHES"),
        ("What did the canyon echo shout to the mountain top?", "REPEAT THE GRAND CHORUS"),
        ("Why did the geologist study the active volcano?", "SEEKING SOLID GROUND WORK"),
        ("What do you call a dolphin with an acoustic guitar?", "AN OCEAN SOUND CREATOR"),
        ("Why was the royal palace garden so well guarded?", "PROTECTING NOBLE BLOSSOMS"),
        ("What did the steam engine whistle say to the train station?", "ROLLING DOWN IRON RAILS"),
        ("Why did the electrical engineer carry extra fuses?", "PREVENTING SHORT CIRCUITS"),
        ("What do you call a marathon runner who loves poetry?", "MAKING STRIDES IN RHYME"),
        ("Why did the clockmaker work late in his workshop?", "CRAFTING ACCURATE SECONDS"),
        ("What did the captain say when entering the harbor?", "DROPPING HEAVY ANCHORS"),
        ("Why was the meteorologist so calm during hurricanes?", "WEATHERING EVERY STORM"),
        ("What do you call an inventor who makes flying bikes?", "A SKY HIGH INNOVATOR"),
        ("Why did the woodworker polish the mahogany table?", "SMOOTHING GRAIN PATTERNS"),
        ("What did the astronomer write in his observation journal?", "MAPPING GALAXY SECRETS"),
        ("Why did the classical choir sing on the mountain peak?", "REACHING ELEVATED HARMONY"),
        ("What do you call a locksmith who solves mystery riddles?", "UNLOCKING ANCIENT CODES"),
        ("Why did the sailboat captain navigate by constellations?", "GUIDED BY BRIGHT STARS"),
        ("What did the detective conclude at the crime museum?", "FOLLOWING FRESH FOOTPRINTS"),
        ("Why did the watchmaker inspect the golden gears?", "KEEPING TIMELY BALANCE"),
        ("What do you call an athlete who writes epic novels?", "RUNNING OUT OF CHAPTERS"),
        ("Why did the wildlife photographer hike into the jungle?", "CAPTURING HIDDEN NATURE"),
        ("What did the orchestra conductor tell the violin section?", "BRING FORTH PURE STRINGS"),
        ("Why was the solar panel engineer smiling all afternoon?", "CHARGING ON SUNNY RAYS"),
        ("What do you call a chess grandmaster who loves baking?", "CHECKMATING SWEET PASTRY"),
        ("Why did the mountain climber pack a warm thermos?", "WARMING ICY ELEVATIONS"),
        ("What did the treasure hunter find inside the sunken ship?", "GOLDEN COINS AND GEMS"),
        ("Why did the aerospace team test rocket thrusters?", "BLASTING BEYOND ORBITS"),
        ("What do you call a gardener who cultivates rare orchids?", "BLOOMING BOTANICAL TALENT"),
        ("Why did the deep space probe broadcast digital signals?", "CONNECTING DISTANT WORLDS"),
        ("What did the royal herald proclaim from the castle tower?", "HEAR YE NOBLE CITIZENS"),
        ("Why was the antique restoration expert so patient?", "PRESERVING TIMELESS ART"),
        ("What do you call a surfer who rides enormous tidal waves?", "MASTERING OCEAN SURGES"),
        ("Why did the civil engineer reinforce the suspension bridge?", "SPANNING HEAVY TRAFFIC"),
        ("What did the paleontologist discover beneath the sandstone?", "ANCIENT FOSSIL MATRIX"),
        ("Why did the wind turbine engineer climb the tall tower?", "HARNESSING BREEZY GUSTS"),
        ("What do you call a painter whose colors illuminate the dark?", "GLOWING CANVAS ARTIST"),
        ("Why was the clockwork automaton so astonishing to watch?", "MOVING WITH GEAR PRECISION"),
        ("What did the arctic explorer log in his expedition journal?", "CROSSING FROZEN GLACIERS"),
        ("Why did the master potter shape clay on the turning wheel?", "CREATING SMOOTH VESSELS"),
        ("What do you call a poet who sings under the starry night?", "RHYMING MOONLIT VERSES"),
        ("Why did the deep sea submarine explore the oceanic trench?", "SURVEYING ABYSS DEPTHS"),
        ("What did the forest ranger notice near the mountain creek?", "CLEAR BUBBLING CURRENTS"),
        ("Why was the master weaver inspecting the silk loom?", "INTRICATE PATTERNS"),
        ("What do you call a cartographer who maps the solar system?", "CHARTING PLANETARY PATHS"),
        ("Why did the railway conductor inspect the steel switches?", "ENSURING SECURE TRANSIT"),
        ("What did the botanist discover inside the tropical canopy?", "VIBRANT FLORA DIVERSITY"),
        ("Why was the stone mason carving intricate marble pillars?", "CRAFTING ENDURING MARBLES"),
        ("What do you call an explorer who travels by dog sled?", "CROSSING NORTHERN TRAILS"),
        ("Why did the audio engineer tune the studio acoustics?", "BALANCING FREQUENCY TONES"),
        ("What did the diamond cutter examine through the loupe?", "PERFECT SPARKLING FACETS"),
        ("Why was the telescope mirror polished with silver compound?", "REFLECTING STELLAR BEAMS"),
        ("What do you call a sailor who navigates without a compass?", "STEERING BY NIGHT STARS"),
        ("Why did the bookbinder sew the leather binding by hand?", "CRAFTING DURABLE FOLIOS"),
        ("What did the master chef reveal at the grand banquet?", "FEAST FIT FOR ROYALTY"),
        ("Why was the steam turbine running at maximum efficiency?", "GENERATING CLEAN KILOWATTS"),
        ("What do you call an author who writes about clockwork realms?", "TIME TRAVELING STORYTELLER"),
        ("Why did the alpine ski patrol test emergency beacons?", "SAFEGUARDING SNOW PEAKS"),
        ("What did the archaeologist unearth beside the river bank?", "ANCIENT POTTERY SHARDS"),
        ("Why was the glassblower shaping molten crystal tubes?", "CREATING LUMINOUS SPHERES"),
        ("What do you call an inventor who crafts acoustic musical gear?", "HARMONIC SOUND CREATOR"),
        ("Why did the oceanographer sample the deep coral reef?", "PROTECTING MARINE LIFE"),
        ("What did the bell ringer announce across the city square?", "STRIKING TWELVE OCLOCK"),
        ("Why was the landscape architect planting cedar groves?", "DESIGNING MAJESTIC PARKS"),
        ("What do you call an astronomer tracking binary star orbits?", "MAPPING TWIN CELESTIALS"),
        ("Why did the aviation crew inspect the propeller blades?", "BALANCING AIR ROTATION"),
        ("What did the lighthouse keeper record during the gale?", "WARNING SIGNAL FLASHING"),
        ("Why was the master calligrapher grinding dark ink sticks?", "FLOWING BRUSHSTROKE ART"),
        ("What do you call a mountaineer standing atop the highest ridge?", "CONQUERING STEEP CRAGS"),
        ("Why did the mineralogist shine ultraviolet light on quartz?", "DISCOVERING FLUORESCENCE"),
        ("What did the clockmaker engrave inside the brass movement?", "TIMELESS CRAFT ACCURACY"),
        ("Why was the garden greenhouse maintaining tropical moisture?", "NOURISHING EXOTIC FERNS"),
        ("What do you call a philosopher who studies the night sky?", "CONTEMPLATING INFINITY"),
        ("Why did the stage lighting technician adjust the spotlight beam?", "ILLUMINATING MAIN ACTORS"),
        ("What did the ancient mariner declare when sighting land?", "SAFE HARBOR AHEAD")
    ]
}

# Rich pool of common 5, 6, and 7 letter everyday words
WORD_POOL = [
    # 5-letter
    "ABOUT", "ABOVE", "ACTOR", "ADMIT", "ADULT", "AFTER", "AGAIN", "AGENT", "AGREE", "AHEAD",
    "ALARM", "ALBUM", "ALERT", "ALIEN", "ALIGN", "ALIKE", "ALIVE", "ALLOW", "ALONE", "ALONG",
    "ALTER", "AMONG", "ANGEL", "ANGER", "ANGLE", "ANGRY", "ANKLE", "APART", "APPLE", "APPLY",
    "ARENA", "ARGUE", "ARISE", "ARMOR", "ARROW", "ASIDE", "ASSET", "AUDIO", "AUDIT", "AVOID",
    "AWAIT", "AWAKE", "AWARD", "AWARE", "BADGE", "BASIC", "BASIS", "BATCH", "BEACH", "BEARD",
    "BEAST", "BEGIN", "BEING", "BELOW", "BENCH", "BIRTH", "BLACK", "BLADE", "BLAME", "BLANK",
    "BLAST", "BLEED", "BLEND", "BLESS", "BLIND", "BLOCK", "BLOOD", "BLOOM", "BOARD", "BOAST",
    "BONUS", "BOOST", "BOUND", "BRAIN", "BRAND", "BRASS", "BRAVE", "BREAD", "BREAK", "BREED",
    "BRICK", "BRIDE", "BRIEF", "BRING", "BROAD", "BROWN", "BRUSH", "BUDDY", "BUILD", "BUNCH",
    "BURST", "CABIN", "CABLE", "CAMEL", "CANAL", "CANDY", "CARGO", "CARRY", "CARVE", "CATCH",
    "CAUSE", "CEASE", "CHAIN", "CHAIR", "CHALK", "CHAMP", "CHAOS", "CHARM", "CHART", "CHASE",
    "CHEAP", "CHECK", "CHEEK", "CHEER", "CHEST", "CHIEF", "CHILD", "CHILL", "CHINA", "CHIPS",
    "CHOIR", "CHOKE", "CHORD", "CHOSE", "CHUNK", "CIVIL", "CLAIM", "CLAMP", "CLASH", "CLASS",
    "CLEAN", "CLEAR", "CLERK", "CLICK", "CLIFF", "CLIMB", "CLOCK", "CLONE", "CLOSE", "CLOTH",
    "CLOUD", "COACH", "COAST", "COLON", "COLOR", "COMET", "COMIC", "CORAL", "COUCH", "COUGH",
    "COUNT", "COURT", "COVER", "CRACK", "CRAFT", "CRANE", "CRASH", "CRAWL", "CRAZY", "CREAM",
    "CREEK", "CREEP", "CRIME", "CRISP", "CROSS", "CROWD", "CROWN", "CRUSH", "CRUST", "CURSE",
    "CURVE", "CYCLE", "DAILY", "DAIRY", "DANCE", "DEATH", "DEBUT", "DELAY", "DELTA", "DENSE",
    "DEPOT", "DEPTH", "DEVIL", "DIARY", "DIRTY", "DISCO", "DITCH", "DIVER", "DIZZY", "DODGE",
    "DONOR", "DOUBT", "DOUGH", "DRAFT", "DRAIN", "DRAMA", "DRANK", "DRAWN", "DREAM", "DRESS",
    "DRIFT", "DRILL", "DRINK", "DRIVE", "DRONE", "DROOP", "DROWN", "DRUNK", "DUMMY", "EAGER",
    "EAGLE", "EARLY", "EARTH", "ELBOW", "ELDER", "ELECT", "EMPTY", "ENEMY", "ENJOY", "ENTER",
    "ENTRY", "EQUAL", "EQUIP", "ERROR", "ESSAY", "EVENT", "EVERY", "EXACT", "EXCEL", "EXERT",
    "EXIST", "EXTRA", "FAINT", "FAITH", "FALSE", "FANCY", "FATAL", "FAULT", "FAVOR", "FEAST",
    "FENCE", "FEVER", "FIBER", "FIELD", "FIERCE", "FIFTH", "FIGHT", "FINAL", "FIRST", "FLAME",
    "FLASH", "FLASK", "FLEET", "FLESH", "FLIGHT", "FLOAT", "FLOCK", "FLOOD", "FLOOR", "FLOUR",
    "FLOWN", "FLUID", "FLUTE", "FOCUS", "FORCE", "FORGE", "FORTH", "FORTY", "FORUM", "FOUND",
    "FRAME", "FRANK", "FRAUD", "FRESH", "FRONT", "FROST", "FROZE", "FRUIT", "GIANT", "GIVEN",
    "GLASS", "GLAZE", "GLOBE", "GLORY", "GLOVE", "GRACE", "GRADE", "GRAIN", "GRAND", "GRANT",
    "GRAPE", "GRAPH", "GRASP", "GRASS", "GRAVE", "GRAVY", "GREAT", "GREED", "GREEN", "GREET",
    "GRIEF", "GRILL", "GRIND", "GROOM", "GROUP", "GROVE", "GUARD", "GUESS", "GUEST", "GUIDE",
    "GUILD", "GUILT", "HABIT", "HANDY", "HAPPY", "HARDY", "HARSH", "HASTE", "HAVEN", "HEART",
    "HEAVY", "HEDGE", "HELLO", "HONOR", "HORSE", "HOTEL", "HOUSE", "HUMAN", "HUMOR", "HURRY",
    "IDEAL", "IMAGE", "INDEX", "INNER", "INPUT", "IRONY", "ISSUE", "JELLY", "JEWEL", "JOINT",
    "JUDGE", "JUICE", "JUMBO", "KNIFE", "KNOCK", "LABEL", "LABOR", "LARGE", "LASER", "LATCH",
    "LATER", "LAUGH", "LAYER", "LEARN", "LEASE", "LEAST", "LEMON", "LEVEL", "LIGHT", "LIMIT",
    "LINEN", "LIVER", "LOCAL", "LODGE", "LOGIC", "LOVER", "LOYAL", "LUCKY", "LUNAR", "LUNCH",
    "MAGIC", "MAJOR", "MAKER", "MANOR", "MAPLE", "MARCH", "MARRY", "MATCH", "MAYOR", "MEDAL",
    "MEDIA", "MERCY", "MERIT", "METAL", "METER", "MIDST", "MIGHT", "MINER", "MINOR", "MODEL",
    "MODEM", "MONEY", "MONTH", "MORAL", "MOTOR", "MOUNT", "MOUSE", "MOUTH", "MOVIE", "MUSIC",
    "NAIVE", "NERVE", "NIGHT", "NOBLE", "NOISE", "NORTH", "NOTED", "NOVEL", "NURSE", "OCEAN",
    "OFFER", "OFTEN", "ONION", "OPERA", "ORBIT", "ORDER", "ORGAN", "OTHER", "OUTER", "OWNER",
    "OXIDE", "OZONE", "PAINT", "PANEL", "PANIC", "PAPER", "PARTY", "PASTA", "PATCH", "PAUSE",
    "PEACE", "PEACH", "PEARL", "PEDAL", "PENNY", "PHASE", "PHONE", "PHOTO", "PIANO", "PILOT",
    "PINCH", "PITCH", "PIZZA", "PLACE", "PLAIN", "PLANE", "PLANK", "PLANT", "PLATE", "PLAZA",
    "PLEAD", "PLENTY", "PLUG", "PLUME", "POINT", "POLAR", "PORCH", "POUND", "POWER", "PRICE",
    "PRIDE", "PRIME", "PRINT", "PRIOR", "PRIZE", "PROBE", "PROUD", "PROVE", "PULSE", "PUNCH",
    "PUPIL", "PURSE", "QUEEN", "QUERY", "QUEST", "QUICK", "QUIET", "QUOTA", "QUOTE", "RADAR",
    "RADIO", "RAISE", "RALLY", "RANCH", "RANGE", "RAPID", "RATIO", "REACH", "REACT", "READY",
    "REALM", "REBEL", "REFER", "REIGN", "RELAX", "RELIC", "REPLY", "RIDER", "RIDGE", "RIGHT",
    "RIGID", "RISKY", "RIVAL", "RIVER", "ROAST", "ROBOT", "ROCKY", "ROGUE", "ROMAN", "ROUGH",
    "ROUND", "ROUTE", "ROYAL", "RULER", "RURAL", "RUSTY", "SADLY", "SAINT", "SALAD", "SALON",
    "SAUCE", "SCALE", "SCARE", "SCARF", "SCENE", "SCENT", "SCOPE", "SCORE", "SCOUT", "SCRAP",
    "SCREW", "SEDAN", "SENSE", "SERVE", "SEVEN", "SHADE", "SHADOW", "SHAFT", "SHAKE", "SHAME",
    "SHAPE", "SHARE", "SHARK", "SHARP", "SHEEP", "SHEER", "SHEET", "SHELF", "SHELL", "SHIFT",
    "SHINE", "SHIRT", "SHOCK", "SHOOT", "SHORE", "SHORT", "SHOUT", "SIGHT", "SIGMA", "SILENT",
    "SILVER", "SINCE", "SIREN", "SKATE", "SKILL", "SKULL", "SLATE", "SLEEP", "SLICE", "SLIDE",
    "SLOPE", "SMART", "SMELL", "SMILE", "SMOKE", "SNACK", "SNAKE", "SOLAR", "SOLID", "SOLVE",
    "SONAR", "SOUND", "SOUTH", "SPACE", "SPARK", "SPEAK", "SPEAR", "SPEED", "SPELL", "SPEND",
    "SPHERE", "SPICE", "SPIKE", "SPILL", "SPIN", "SPIRIT", "SPLIT", "SPOIL", "SPOKE", "SPOON",
    "SPORT", "SPRAY", "SPREAD", "SPRING", "SQUAD", "STACK", "STAFF", "STAGE", "STAIN", "STAIR",
    "STAKE", "STALE", "STAMP", "STAND", "STARE", "START", "STATE", "STEAK", "STEAL", "STEAM",
    "STEEL", "STEEP", "STEER", "STICK", "STIFF", "STILL", "STING", "STOCK", "STONE", "STOOL",
    "STORM", "STORY", "STRAP", "STRAW", "STRIP", "STUDY", "STUFF", "STYLE", "SUGAR", "SUITE",
    "SUMMER", "SUMMIT", "SUNNY", "SUPER", "SURGE", "SWAMP", "SWEAR", "SWEAT", "SWEEP", "SWEET",
    "SWIFT", "SWING", "SWORD", "TABLE", "TASTE", "TEACH", "TEMPO", "TENTH", "THANK", "THEME",
    "THICK", "THIEF", "THIGH", "THING", "THINK", "THIRD", "THORN", "THOSE", "THREE", "THROW",
    "THUMB", "TIGER", "TIGHT", "TIMER", "TIRED", "TITLE", "TOAST", "TODAY", "TOKEN", "TOOTH",
    "TOPIC", "TORCH", "TOTAL", "TOUCH", "TOUGH", "TOWER", "TOXIC", "TRACE", "TRACK", "TRACT",
    "TRADE", "TRAIL", "TRAIN", "TRAIT", "TRASH", "TREAT", "TREND", "TRIAL", "TRIBE", "TRICK",
    "TROOP", "TRUCK", "TRULY", "TRUNK", "TRUST", "TRUTH", "TULIP", "TUMOR", "TUNER", "TUNNEL",
    "TWICE", "TWIST", "UNCLE", "UNDER", "UNION", "UNITY", "UPPER", "UPSET", "URBAN", "USAGE",
    "USUAL", "VALID", "VALLEY", "VALUE", "VALVE", "VAPOR", "VAULT", "VENUE", "VIGOR", "VIRAL",
    "VIRUS", "VISIT", "VITAL", "VIVID", "VOCAL", "VOICE", "VOWEL", "WAFER", "WAGON", "WASTE",
    "WATCH", "WATER", "WEDGE", "WEIGH", "WHALE", "WHEAT", "WHEEL", "WHERE", "WHICH", "WHILE",
    "WHITE", "WHOLE", "WHOSE", "WIDOW", "WIDTH", "WINDY", "WITCH", "WOMAN", "WORLD", "WORRY",
    "WORSE", "WORST", "WORTH", "WOUND", "WRATH", "WRECK", "WRIST", "WRITE", "WRONG", "YACHT",
    "YIELD", "YOUTH", "ZEBRA",
    # 6-letter
    "ACTION", "ACTIVE", "ANIMAL", "ANSWER", "ATTACK", "BOTTLE", "BOUNCE", "BRANCH", "BRIDGE",
    "BRIGHT", "BUTTON", "CAMERA", "CANDLE", "CARPET", "CASTLE", "CATTLE", "CHANCE", "CHANGE",
    "CHARGE", "CHOICE", "CIRCLE", "CLOVER", "COFFEE", "COPPER", "CORNER", "CREDIT", "CUSTOM",
    "DAMAGE", "DANGER", "DECIDE", "DESERT", "DEVICE", "DINNER", "DIRECT", "DOCTOR", "DOLLAR",
    "DOMAIN", "DOUBLE", "DRAGON", "DRAWER", "DRIVER", "ENGINE", "ENOUGH", "ESCAPE", "EXCUSE",
    "EXPERT", "FABRIC", "FAMILY", "FAMOUS", "FARMER", "FATHER", "FELLOW", "FINGER", "FINISH",
    "FLAVOR", "FLIGHT", "FLOWER", "FOREST", "FORTUNE", "FRIEND", "FROZEN", "FUTURE", "GARDEN",
    "GATHER", "GENTLE", "GLANCE", "GOLDEN", "GUITAR", "HAMMER", "HARBOR", "HEALTH", "HEAVEN",
    "HEROIC", "HONEST", "HUNGRY", "HUNTER", "IMPACT", "INSECT", "INSIDE", "ISLAND", "JACKET",
    "JOCKEY", "JUNGLE", "KITTEN", "KNIGHT", "LADDER", "LANTERN", "LAWYER", "LEADER", "LESSON",
    "LETTER", "LIZARD", "LUMBER", "MAGNET", "MANNER", "MARBLE", "MARKET", "MASTER", "MEADOW",
    "MEMORY", "MIDDLE", "MIRROR", "MODERN", "MONKEY", "MOMENT", "MORTAL", "MOTHER", "MOTION",
    "MUSEUM", "NATION", "NATURE", "NEEDLE", "NORMAL", "NOTICE", "NUMBER", "ORANGE", "ORCHID",
    "PACKET", "PALACE", "PARADE", "PARENT", "PASTEL", "PEPPER", "PERSON", "PLANET", "POCKET",
    "POLITE", "POTATO", "POWDER", "PRAISE", "PRAYER", "PRINCE", "PRISON", "PROFIT", "PROMISE",
    "PUBLIC", "PUDDLE", "PUPPET", "PURPLE", "PUZZLE", "RABBIT", "RADISH", "RECORD", "REGION",
    "RESCUE", "REWARD", "RIBBON", "RIDDLE", "RITUAL", "ROCKET", "RUNNER", "SAILOR", "SAMPLE",
    "SEASON", "SECRET", "SECTOR", "SELDOM", "SERIES", "SETTLE", "SHADOW", "SHIELD", "SILENT",
    "SILVER", "SIMPLE", "SISTER", "SKETCH", "SMOOTH", "SOCCER", "SOCKET", "SORROW", "SPEECH",
    "SPHERE", "SPIDER", "SPIRIT", "SPRING", "SQUARE", "STATUE", "STREET", "STRIKE", "STRING",
    "SUMMER", "SUMMIT", "SUNSET", "SWITCH", "SYMBOL", "TALENT", "TARGET", "TEMPLE", "TENDER",
    "TENNIS", "THEORY", "THIRST", "THREAD", "THROAT", "TIMBER", "TOMATO", "TONGUE", "TORQUE",
    "TRAVEL", "TREATY", "TUNNEL", "TURTLE", "TWELVE", "UNIQUE", "VALLEY", "VESSEL", "VIOLIN",
    "VISION", "VOLUME", "VOYAGE", "WALLET", "WANDER", "WARMTH", "WEAPON", "WEIGHT", "WHISPER",
    "WINDOW", "WINTER", "WIZARD", "YELLOW",
    # 7-letter
    "AIRPORT", "ALPHABET", "BALLOON", "BICYCLE", "BLANKET", "CABINET", "CAPTAIN", "CHIMNEY",
    "COMPASS", "CRYSTAL", "DIAMOND", "DOLPHIN", "FEATHER", "FIREFLY", "FORTUNE", "GIRAFFE",
    "GLACIER", "HARMONY", "HOLIDAY", "HORIZON", "JOURNEY", "KINGDOM", "LANTERN", "LEOPARD",
    "LUGGAGE", "MACHINE", "MAJESTY", "MORNING", "MYSTERY", "NOTEBOOK", "OCTOPUS", "PAINTER",
    "PANTHER", "PEACOCK", "PENGUIN", "PICTURE", "PIRATES", "RAINBOW", "SEAFOOD", "SOLDIER",
    "SPARROW", "STATION", "SUNSHINE", "THEATER", "THUNDER", "TRAFFIC", "TREASURE", "UNICORN",
    "VAMPIRE", "VILLAGE", "VOLCANO", "WARRIOR", "WEATHER", "WHISTLE", "WINDFALL"
]

def clean_letters(text: str) -> List[str]:
    return [c for c in text.upper() if 'A' <= c <= 'Z']

rarity = 'QZXJVWKBMPGHDYFCLNUSTOERAI'

def solve_clue_words(answer: str, target_word_count: int, pool: List[str]) -> Optional[Tuple[List[str], List[List[int]]]]:
    ans_chars = clean_letters(answer)
    target_counts = Counter(ans_chars)
    ans_len = len(ans_chars)
    if ans_len < target_word_count:
        return None

    for attempt in range(400):
        rem = Counter(target_counts)
        chosen_words = []
        chosen_circles = []
        available_pool = list(pool)
        random.shuffle(available_pool)

        while len(chosen_words) < target_word_count:
            rem_words = target_word_count - len(chosen_words)
            rem_letters = sum(rem.values())
            if rem_letters < rem_words:
                break

            max_take = min(4, rem_letters - (rem_words - 1))
            min_take = 1

            rare_needed = None
            for ch in rarity:
                if rem[ch] > 0:
                    rare_needed = ch
                    break
            if not rare_needed:
                for ch, cnt in rem.items():
                    if cnt > 0:
                        rare_needed = ch
                        break
            if not rare_needed:
                break

            candidates = [w for w in available_pool if rare_needed in w]
            if not candidates:
                break
            random.shuffle(candidates)
            candidates.sort(key=lambda w: sum(min(w.count(c), rem[c]) for c in set(w)), reverse=True)

            found = False
            for w in candidates[:20]:
                matched = []
                for idx, ch in enumerate(w):
                    if rem[ch] > 0:
                        matched.append(idx)
                        if len(matched) == max_take:
                            break
                if len(matched) >= min_take:
                    for idx in matched:
                        rem[w[idx]] -= 1
                    chosen_words.append(w)
                    chosen_circles.append(matched)
                    available_pool.remove(w)
                    found = True
                    break
            if not found:
                break

        if sum(rem.values()) == 0 and len(chosen_words) == target_word_count:
            extracted = [chosen_words[i][c] for i in range(len(chosen_words)) for c in chosen_circles[i]]
            if sorted(extracted) == sorted(ans_chars):
                return chosen_words, chosen_circles

    return None

def generate_all_puzzles():
    puzzles = []
    diff_targets = {
        "easy": 4,     # exactly 4 words for easy
        "medium": 4,   # 4 words (or 5 if needed)
        "hard": 5      # 5 or 6 words for hard
    }

    print("Generating and mathematically verifying 300 Jumble puzzles...")

    for diff in ["easy", "medium", "hard"]:
        items = RIDDLE_BANK[diff]
        print(f"Processing {len(items)} {diff.upper()} riddles...")
        
        for idx, (riddle, answer) in enumerate(items):
            ans_clean = clean_letters(answer)
            ans_len = len(ans_clean)

            # Determine best word count: 4, 5, or 6
            if diff == "easy":
                preferred_counts = [4, 5]
            elif diff == "medium":
                preferred_counts = [4, 5, 6] if ans_len >= 13 else [4, 5]
            else:
                preferred_counts = [5, 6, 4] if ans_len >= 14 else [4, 5, 6]

            solution = None
            for w_count in preferred_counts:
                solution = solve_clue_words(answer, w_count, WORD_POOL)
                if solution:
                    break

            if not solution:
                # Try any word count from 4 to 6
                for w_count in [4, 5, 6]:
                    solution = solve_clue_words(answer, w_count, WORD_POOL)
                    if solution:
                        break

            assert solution is not None, f"Failed to fit words for [{diff}] '{riddle}' -> '{answer}'"

            words, circles = solution

            # Verification assertions
            extracted_letters = []
            for w, circ in zip(words, circles):
                for c_idx in circ:
                    assert 0 <= c_idx < len(w), f"Circle index out of bounds in {w}"
                    extracted_letters.append(w[c_idx])
            assert sorted(extracted_letters) == sorted(ans_clean), f"Multiset mismatch for {answer}"

            puzzle_obj = {
                "id": f"{diff}_{idx+1:03d}",
                "diff": diff,
                "words": words,
                "circles": circles,
                "riddle": riddle,
                "answer": answer
            }
            puzzles.append(puzzle_obj)

    print(f"Successfully verified all {len(puzzles)} puzzles!")

    # Write server/data/jumbles.json
    json_path = "server/data/jumbles.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(puzzles, f, indent=2)
    print(f"Saved master dataset to {json_path} ({len(puzzles)} puzzles)")

    # Generate esp32-firmware/src/generators/JumbleDataset.h
    cpp_header_path = "esp32-firmware/src/generators/JumbleDataset.h"
    generate_cpp_header(puzzles, cpp_header_path)
    print(f"Generated ESP32 PROGMEM dataset header at {cpp_header_path}")

def generate_cpp_header(puzzles: List[Dict[str, Any]], out_path: str):
    diff_map = {"easy": "JUMBLE_EASY", "medium": "JUMBLE_MEDIUM", "hard": "JUMBLE_HARD"}

    lines = []
    lines.append("#ifndef JUMBLE_DATASET_H")
    lines.append("#define JUMBLE_DATASET_H")
    lines.append("")
    lines.append("#include <Arduino.h>")
    lines.append('#include "JumbleGen.h"')
    lines.append("")
    lines.append("struct CompactRiddleSet {")
    lines.append("    JumbleDifficulty diff;")
    lines.append("    uint8_t numWords;")
    lines.append("    const char* words[6];")
    lines.append("    uint8_t circles[6][4];")
    lines.append("    uint8_t numCircles[6];")
    lines.append("    const char* riddle;")
    lines.append("    const char* answer;")
    lines.append("};")
    lines.append("")
    lines.append(f"static const size_t TOTAL_JUMBLE_PUZZLES = {len(puzzles)};")
    lines.append("static const CompactRiddleSet JUMBLE_DATASET[] PROGMEM = {")

    for p in puzzles:
        diff_enum = diff_map[p["diff"]]
        num_words = len(p["words"])
        # Words array padded to 6
        words_c = [f'"{w}"' for w in p["words"]] + ['""'] * (6 - num_words)
        words_str = "{" + ", ".join(words_c) + "}"

        # Circles array [6][4] padded with 0
        circles_c = []
        num_circles_c = []
        for i in range(6):
            if i < num_words:
                c_list = p["circles"][i]
                num_circles_c.append(str(len(c_list)))
                padded = [str(c) for c in c_list] + ["0"] * (4 - len(c_list))
                circles_c.append("{" + ", ".join(padded) + "}")
            else:
                num_circles_c.append("0")
                circles_c.append("{0, 0, 0, 0}")

        circles_str = "{" + ", ".join(circles_c) + "}"
        num_circles_str = "{" + ", ".join(num_circles_c) + "}"

        escaped_riddle = p["riddle"].replace('"', '\\"')
        escaped_answer = p["answer"].replace('"', '\\"')

        lines.append("    {")
        lines.append(f"        {diff_enum}, {num_words},")
        lines.append(f"        {words_str},")
        lines.append(f"        {circles_str},")
        lines.append(f"        {num_circles_str},")
        lines.append(f'        "{escaped_riddle}",')
        lines.append(f'        "{escaped_answer}"')
        lines.append("    },")

    lines.append("};")
    lines.append("")
    lines.append("#endif // JUMBLE_DATASET_H")
    lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    generate_all_puzzles()
