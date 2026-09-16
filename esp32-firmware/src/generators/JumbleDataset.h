#ifndef JUMBLE_DATASET_H
#define JUMBLE_DATASET_H

#include <Arduino.h>

struct CompactRiddleSet {
    uint8_t numWords;
    uint8_t circleMasks[6];
    const char* words;
    const char* riddle;
    const char* answer;
};

static const size_t TOTAL_JUMBLE_PUZZLES = 300;
static const CompactRiddleSet JUMBLE_DATASET[] PROGMEM = {
    {
        4,
        {0x3A, 0x35, 0x03, 0x10, 0x00, 0x00},
        "KINGDOM MAGNET GUEST SHOUT",
        "Why did the coffee file a police report?",
        "IT GOT MUGGED"
    },
    {
        5,
        {0x17, 0x0F, 0x1B, 0x1E, 0x0C, 0x00},
        "JOURNEY VISIT WEIGHT STAND SETTLE",
        "What did the ocean say to the sailboat?",
        "NOTHING IT JUST WAVED"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x56, 0x10, 0x00},
        "TRAVEL PALACE CHASE MYSTERY PRIDE",
        "Why do we tell actors to 'break a leg'?",
        "EVERY PLAY HAS A CAST"
    },
    {
        4,
        {0x1B, 0x0F, 0x02, 0x08, 0x00, 0x00},
        "SOLDIER ORANGE UNIQUE TOWER",
        "What do you call a sleeping dinosaur?",
        "A \"DINO\"-SNORE"
    },
    {
        4,
        {0x0F, 0x15, 0x04, 0x01, 0x00, 0x00},
        "ANIMAL ALPHABET VISIT THINK",
        "What do you call a fake noodle?",
        "AN \"IM-PASTA\""
    },
    {
        4,
        {0x0F, 0x0F, 0x1E, 0x10, 0x00, 0x00},
        "DRAWER TWIST KITTEN REGION",
        "Why did the bicycle fall over?",
        "IT WAS \"TWO-TIRED\""
    },
    {
        4,
        {0x0F, 0x1D, 0x06, 0x10, 0x00, 0x00},
        "CHANCE SPEECH WHOLE SPACE",
        "What do you call cheese that isn't yours?",
        "\"NACHO\" CHEESE"
    },
    {
        4,
        {0x0F, 0x0F, 0x1B, 0x10, 0x00, 0x00},
        "THEATER SAILOR LOVER EVENT",
        "Why couldn't the pony sing in the choir?",
        "A LITTLE HOARSE"
    },
    {
        4,
        {0x0F, 0x0F, 0x1E, 0x03, 0x00, 0x00},
        "VISION TARGET LANTERN NOBLE",
        "What do you call an alligator in a vest?",
        "AN \"IN-VEST\"-IGATOR"
    },
    {
        4,
        {0x0F, 0x0F, 0x01, 0x04, 0x00, 0x00},
        "BREED DOUGH FROZEN WINDY",
        "What do you call a cow with no legs?",
        "GROUND BEEF"
    },
    {
        4,
        {0x1D, 0x0F, 0x1E, 0x12, 0x00, 0x00},
        "WALLET PENGUIN POLITE ANGLE",
        "Why did the banana go to the doctor?",
        "NOT \"PEELING\" WELL"
    },
    {
        4,
        {0x0F, 0x0F, 0x12, 0x01, 0x00, 0x00},
        "WAFER MASTER ORCHID DECAY",
        "Why did the picture go to jail?",
        "IT WAS FRAMED"
    },
    {
        4,
        {0x0F, 0x1E, 0x04, 0x10, 0x00, 0x00},
        "MARBLE IMAGE TRULY APPLY",
        "What do you call a bear with no teeth?",
        "A GUMMY BEAR"
    },
    {
        4,
        {0x1B, 0x1B, 0x02, 0x04, 0x00, 0x00},
        "BOUNCE HARMONY PENNY VOYAGE",
        "Why do bees have sticky hair?",
        "A HONEYCOMB"
    },
    {
        4,
        {0x0F, 0x1D, 0x15, 0x01, 0x00, 0x00},
        "TIMER FORUM CRYSTAL LOYAL",
        "Why did the cookie go to the hospital?",
        "IT FELT CRUMMY"
    },
    {
        4,
        {0x17, 0x4E, 0x01, 0x04, 0x00, 0x00},
        "MEADOW RAINBOW TRAIN SUNNY",
        "What do you call a pile of kittens?",
        "A \"MEOW\"-NTAIN"
    },
    {
        4,
        {0x0F, 0x17, 0x2E, 0x1C, 0x00, 0x00},
        "HARMONY ROCKET GENTLE KITTEN",
        "What did one wall say to the other?",
        "MEET AT THE CORNER"
    },
    {
        4,
        {0x0F, 0x27, 0x04, 0x10, 0x00, 0x00},
        "BLAZE LEOPARD SQUAD GUILD",
        "What do you call a sleeping bull?",
        "A \"BULL\"-DOZER"
    },
    {
        4,
        {0x0F, 0x2B, 0x03, 0x08, 0x00, 0x00},
        "PIVOT WEATHER STAIR QUERY",
        "Why was the broom late for work?",
        "IT OVER-SWEPT"
    },
    {
        5,
        {0x1D, 0x0F, 0x1D, 0x35, 0x05, 0x00},
        "WHISTLE DANGER SOLDIER ANSWER SMART",
        "Why did the tomato blush?",
        "IT SAW SALAD DRESSING"
    },
    {
        4,
        {0x0F, 0x01, 0x04, 0x10, 0x00, 0x00},
        "MONKEY EARLY PRAY PARTY",
        "What kind of key opens a banana?",
        "A \"MON-KEY\""
    },
    {
        4,
        {0x0F, 0x3A, 0x05, 0x02, 0x00, 0x00},
        "PAINTER FEATHER RURAL CLAIM",
        "What do you call an elephant that doesn't matter?",
        "\"IRRELEPHANT\""
    },
    {
        4,
        {0x2B, 0x17, 0x08, 0x20, 0x00, 0x00},
        "HORIZON LANTERN DRONE NATURE",
        "Why did the golfer bring extra socks?",
        "A HOLE IN ONE"
    },
    {
        4,
        {0x0F, 0x1B, 0x01, 0x10, 0x00, 0x00},
        "HOLIDAY RITUAL SLEEP FINAL",
        "What do you call a funny mountain?",
        "\"HILL\"-ARIOUS"
    },
    {
        4,
        {0x1E, 0x1A, 0x02, 0x08, 0x00, 0x00},
        "SHADOW SWEAT ICING DODGE",
        "What kind of dog tells time?",
        "A \"WATCH\" DOG"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x1B, 0x10, 0x00},
        "ALPHABET PIRATES UPSET FOUND ADULT",
        "Why was the belt arrested?",
        "HELD UP PAIR OF PANTS"
    },
    {
        4,
        {0x0F, 0x03, 0x02, 0x02, 0x00, 0x00},
        "BROWN ANIMAL RAPID VIGOR",
        "What bow can never be tied?",
        "A RAINBOW"
    },
    {
        4,
        {0x0F, 0x1B, 0x33, 0x10, 0x00, 0x00},
        "PANTHER HONEST SEAFOOD BLEED",
        "What kind of shoes do frogs wear?",
        "\"OPEN-TOAD\" SHOES"
    },
    {
        5,
        {0x0F, 0x0F, 0x35, 0x1E, 0x2C, 0x00},
        "WHISTLE NOTEBOOK KINGDOM NORTH WARRIOR",
        "Why do cows wear bells?",
        "THEIR HORNS DO NOT WORK"
    },
    {
        4,
        {0x07, 0x04, 0x08, 0x08, 0x00, 0x00},
        "STACK THICK SNACK ROCKET",
        "What do you call a boomerang that doesn't return?",
        "A STICK"
    },
    {
        4,
        {0x0F, 0x27, 0x0E, 0x10, 0x00, 0x00},
        "SQUARE WEATHER TRICK SNACK",
        "Why did the duck get sent to the principal?",
        "A WISE \"QUACKER\""
    },
    {
        4,
        {0x0F, 0x0C, 0x10, 0x02, 0x00, 0x00},
        "UPSET LANTERN JOURNEY PEDAL",
        "What kind of music do planets listen to?",
        "\"NEP-TUNES\""
    },
    {
        4,
        {0x55, 0x02, 0x01, 0x02, 0x00, 0x00},
        "ALPHABET BOTTLE TREATY STRING",
        "What starts with T, ends with T, and has T inside?",
        "A TEAPOT"
    },
    {
        4,
        {0x0F, 0x1E, 0x66, 0x04, 0x00, 0x00},
        "TRAFFIC VOLCANO HORIZON CHAIN",
        "Why did the tree go to the dentist?",
        "FOR A ROOT CANAL"
    },
    {
        5,
        {0x0F, 0x17, 0x0F, 0x33, 0x08, 0x00},
        "TIGER THEATER SOLDIER ROCKET MAYOR",
        "Why did the chicken cross the playground?",
        "TO GET TO OTHER SLIDE"
    },
    {
        4,
        {0x0F, 0x0F, 0x0F, 0x38, 0x00, 0x00},
        "WINDOW FLOWER STEEP WEAPON",
        "Why was the computer cold?",
        "LEFT WINDOWS OPEN"
    },
    {
        4,
        {0x0F, 0x03, 0x04, 0x04, 0x00, 0x00},
        "LATCH CHOICE PHONE CREST",
        "What kind of candy never arrives on time?",
        "\"CHOC\"-LATE"
    },
    {
        4,
        {0x17, 0x17, 0x03, 0x10, 0x00, 0x00},
        "WEAPON SNACK GLORY SADLY",
        "What kind of car does an egg drive?",
        "A \"YOLK\"-SWAGEN"
    },
    {
        4,
        {0x1D, 0x16, 0x02, 0x01, 0x00, 0x00},
        "PEACOCK JOKER CHAMP PUPPET",
        "What do you call a pig that knows karate?",
        "A PORK CHOP"
    },
    {
        5,
        {0x0F, 0x0F, 0x1E, 0x2E, 0x02, 0x00},
        "WALLET INLET SUITE BOTTLE STAIR",
        "What did the grape say when stepped on?",
        "LET OUT A LITTLE \"WINE\""
    },
    {
        4,
        {0x0F, 0x0F, 0x0F, 0x0F, 0x00, 0x00},
        "ORANGE TIGHT THOSE CHEER",
        "Why did the music teacher need a ladder?",
        "TO REACH HIGH NOTES"
    },
    {
        4,
        {0x0F, 0x1A, 0x04, 0x10, 0x00, 0x00},
        "NEEDLE MEMORY THEORY WORRY",
        "What do you call a deer with no eyes?",
        "\"NO-EYE\" DEER"
    },
    {
        4,
        {0x0F, 0x0A, 0x02, 0x08, 0x00, 0x00},
        "PENGUIN CABINET HUNTER PAINTER",
        "What kind of bird can write?",
        "A \"PEN\"-GUIN"
    },
    {
        4,
        {0x72, 0x01, 0x01, 0x02, 0x00, 0x00},
        "NOTEBOOK BOAST ACTOR VOLCANO",
        "What do you call a ghost's mistake?",
        "A \"BOO-BOO\""
    },
    {
        4,
        {0x0F, 0x2E, 0x1E, 0x01, 0x00, 0x00},
        "ESCAPE SPEECH TENDER DRIFT",
        "Why did the astronaut break up with his girlfriend?",
        "HE NEEDED SPACE"
    },
    {
        4,
        {0x0F, 0x1E, 0x1E, 0x0B, 0x00, 0x00},
        "BOARD MARBLE PARADE CANDY",
        "What do you call a magic dog?",
        "\"LABRA-CADABRA\"-DOR"
    },
    {
        4,
        {0x0F, 0x0F, 0x0D, 0x40, 0x00, 0x00},
        "BOTTLE FUTURE LINER WEATHER",
        "Why did the candle quit its job?",
        "FELT BURNT OUT"
    },
    {
        4,
        {0x0F, 0x0F, 0x33, 0x33, 0x00, 0x00},
        "ENOUGH HEDGE HEALTH DECIDE",
        "Why did the baker go to the bank?",
        "HE NEEDED THE DOUGH"
    },
    {
        4,
        {0x17, 0x0F, 0x0A, 0x20, 0x00, 0x00},
        "MAJESTY AWAIT STAIN HEAVEN",
        "Why was the strawberry sad?",
        "IT WAS IN A JAM"
    },
    {
        4,
        {0x1B, 0x1B, 0x0E, 0x10, 0x00, 0x00},
        "CAPTAIN UNICORN LANTERN LEARN",
        "What kind of insect is good at math?",
        "AN \"ACCOUNT-ANT\""
    },
    {
        4,
        {0x1D, 0x0F, 0x01, 0x02, 0x00, 0x00},
        "HARBOR FIREFLY LOYAL CLOAK",
        "Why did the duck buy lipstick?",
        "FOR HER \"BILL\""
    },
    {
        4,
        {0x0F, 0x3A, 0x01, 0x01, 0x00, 0x00},
        "THEATER TREASURE UPSET SOUTH",
        "What do you call a dinosaur with a great vocabulary?",
        "A \"THES-AURUS\""
    },
    {
        4,
        {0x17, 0x0F, 0x03, 0x04, 0x00, 0x00},
        "WEATHER LASER RURAL VIRAL",
        "Why was the king only one foot tall?",
        "HE WAS A RULER"
    },
    {
        6,
        {0x1E, 0x17, 0x0F, 0x0F, 0x1D, 0x04},
        "PENGUIN DOLPHIN INSIDE STAND DRIFT SAILOR",
        "Why did the scarecrow win an award?",
        "\"OUT-STANDING\" IN HIS FIELD"
    },
    {
        4,
        {0x0F, 0x0F, 0x19, 0x04, 0x00, 0x00},
        "MAJESTY BLACK SHARK ACUTE",
        "What do you call a sleeping woodcutter?",
        "A \"SLUMBER\"-JACK"
    },
    {
        4,
        {0x0F, 0x1B, 0x1D, 0x04, 0x00, 0x00},
        "CHASE SOLDIER THIEF FATAL",
        "What do you call a fish wearing a bowtie?",
        "\"SO-FISH\"-TICATED"
    },
    {
        4,
        {0x0F, 0x2B, 0x17, 0x08, 0x00, 0x00},
        "AWAIT TARGET TODAY SALON",
        "Why did the frog park illegally?",
        "IT GOT \"TOAD\" AWAY"
    },
    {
        4,
        {0x1B, 0x17, 0x0F, 0x23, 0x00, 0x00},
        "RAINBOW MEADOW TWELVE TONGUE",
        "Why did the melon jump into the lake?",
        "TO BE A WATER-MELON"
    },
    {
        4,
        {0x0F, 0x02, 0x02, 0x08, 0x00, 0x00},
        "ALTER FARMER NERVE SHORT",
        "What kind of tea is hard to swallow?",
        "\"REAL-TEA\""
    },
    {
        4,
        {0x0F, 0x0F, 0x0D, 0x10, 0x00, 0x00},
        "LIZARD ZEBRA READY GLORY",
        "What do you call a bear caught in the rain?",
        "A \"DRIZZLY\" BEAR"
    },
    {
        4,
        {0x0F, 0x0F, 0x1E, 0x1A, 0x00, 0x00},
        "PIRATES PASTEL PENGUIN PLANT",
        "What do you call a turtle taking photos?",
        "A \"SNAPPING\" TURTLE"
    },
    {
        4,
        {0x0F, 0x2E, 0x03, 0x04, 0x00, 0x00},
        "SELDOM SMOOTH PALACE BRAVE",
        "What kind of dog loves bubble baths?",
        "A \"SHAM-POODLE\""
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x1B, 0x05, 0x00},
        "WEATHER WARRIOR SHAME FOREST THIGH",
        "Why did the cookie cry?",
        "ITS MOTHER WAS A WAFER"
    },
    {
        4,
        {0x2E, 0x0F, 0x09, 0x08, 0x00, 0x00},
        "PROMISE DECOR EXPERT SHIRT",
        "What do you call an apology written in dots and dashes?",
        "\"RE-MORSE\" CODE"
    },
    {
        4,
        {0x1E, 0x0F, 0x17, 0x15, 0x00, 0x00},
        "VILLAGE HEDGE THEATER FUDGE",
        "Why did the candle visit the doctor?",
        "FELT \"LIGHT\"-HEADED"
    },
    {
        4,
        {0x1B, 0x17, 0x0F, 0x15, 0x00, 0x00},
        "PIRATES ALPHABET SECTOR SHORE",
        "Why did the orange go to court?",
        "TO \"APPEAL\" ITS CASE"
    },
    {
        4,
        {0x1D, 0x13, 0x08, 0x01, 0x00, 0x00},
        "BONUS BUDDY AMONG GUIDE",
        "What do you call a rabbit with fleas?",
        "\"BUGS\" BUNNY"
    },
    {
        4,
        {0x1D, 0x17, 0x01, 0x04, 0x00, 0x00},
        "DIAMOND PANTHER SOLAR CHASE",
        "What do you call a clean pig?",
        "HAM AND SOAP"
    },
    {
        4,
        {0x0F, 0x13, 0x02, 0x08, 0x00, 0x00},
        "TEMPLE ALPHABET GRAPE INSECT",
        "What kind of tree loves high fives?",
        "A PALM TREE"
    },
    {
        4,
        {0x0F, 0x1E, 0x04, 0x02, 0x00, 0x00},
        "ANIMAL DISCO MEADOW NOISE",
        "What do you call a cow playing an instrument?",
        "A \"MOO\"-SICIAN"
    },
    {
        4,
        {0x0F, 0x1E, 0x4E, 0x02, 0x00, 0x00},
        "CHILI CATTLE VILLAGE LINEN",
        "What do you call a tiny pepper in winter?",
        "A LITTLE \"CHILLI\""
    },
    {
        4,
        {0x0F, 0x0F, 0x1B, 0x07, 0x00, 0x00},
        "LEOPARD TONGUE DELAY AUDIO",
        "Why did the violin take a bow?",
        "PLAYED A GOOD TUNE"
    },
    {
        4,
        {0x1E, 0x03, 0x02, 0x04, 0x00, 0x00},
        "VILLAGE GENTLE ALIVE THEORY",
        "What do you call an eagle that tells bad jokes?",
        "\"ILL-EAGLE\""
    },
    {
        4,
        {0x1D, 0x0F, 0x1D, 0x10, 0x00, 0x00},
        "WHISTLE DRAWER LABEL SOLVE",
        "Why was the loaf of bread so polite?",
        "IT WAS WELL-BRED"
    },
    {
        4,
        {0x1E, 0x5C, 0x05, 0x02, 0x00, 0x00},
        "CABINET VILLAGE APART CRISP",
        "What do you call a dancing sheep?",
        "A \"BAA\"-LLERINA"
    },
    {
        4,
        {0x0F, 0x0F, 0x0C, 0x02, 0x00, 0x00},
        "ATTACK BRICK SOCKET PEDAL",
        "What do you call a noisy insect playing sports?",
        "A CRICKET BAT"
    },
    {
        4,
        {0x0F, 0x3C, 0x1D, 0x0E, 0x00, 0x00},
        "RAINBOW RABBIT MAGIC VOICE",
        "What do you call a funny frog on stage?",
        "A \"RIBBIT\"-ING COMIC"
    },
    {
        4,
        {0x0F, 0x0F, 0x0F, 0x1D, 0x00, 0x00},
        "DRAWER NUMBER DESERT EVERY",
        "Why did the calendar look worried?",
        "DAYS WERE NUMBERED"
    },
    {
        4,
        {0x0F, 0x1E, 0x03, 0x04, 0x00, 0x00},
        "CATTLE POLITE LEVEL RELAX",
        "What do you call a cold horse in the pasture?",
        "A LITTLE \"COLT\""
    },
    {
        4,
        {0x0F, 0x1D, 0x05, 0x04, 0x00, 0x00},
        "RAINBOW BLESS SIGMA CHAIN",
        "What do you call a singing fish?",
        "A BASS SINGER"
    },
    {
        4,
        {0x0F, 0x1D, 0x01, 0x04, 0x00, 0x00},
        "MACHINE PANIC YIELD CIDER",
        "What do you call a sweet monkey?",
        "\"CHIMP\" CANDY"
    },
    {
        4,
        {0x17, 0x1B, 0x35, 0x02, 0x00, 0x00},
        "WEATHER NOTEBOOK STRIKE SLIDE",
        "Why did the shoe visit the hospital?",
        "HEEL WAS BROKEN"
    },
    {
        4,
        {0x17, 0x1E, 0x10, 0x08, 0x00, 0x00},
        "DIAMOND CANDLE FROZEN GLANCE",
        "What do you call a lion with flowers?",
        "A \"DANDE-LION\""
    },
    {
        4,
        {0x0F, 0x1B, 0x35, 0x11, 0x00, 0x00},
        "PAINTER REWARD DIAMOND DANCE",
        "Why did the cloud cry all morning?",
        "RAINED ON PARADE"
    },
    {
        4,
        {0x1D, 0x03, 0x01, 0x10, 0x00, 0x00},
        "CABINET LETTER THEME SCORE",
        "What did the zero say to the eight?",
        "\"NICE BELT\""
    },
    {
        4,
        {0x0F, 0x0F, 0x1E, 0x16, 0x00, 0x00},
        "NOTEBOOK SYMBOL NORMAL SPOIL",
        "Why was the math book sad?",
        "TOO MANY PROBLEMS"
    },
    {
        4,
        {0x0F, 0x16, 0x0C, 0x01, 0x00, 0x00},
        "CAMERA GRASP STUFF FIXED",
        "What do you call a sleeping pie?",
        "A \"CREAM PUFF\""
    },
    {
        4,
        {0x17, 0x0F, 0x0F, 0x2C, 0x00, 0x00},
        "WINDFALL FATAL FLOUR VESSEL",
        "Why did the stadium get so cool?",
        "IT WAS FULL OF FANS"
    },
    {
        4,
        {0x27, 0x01, 0x04, 0x08, 0x00, 0x00},
        "BLANKET TOTAL FRONT SECTOR",
        "What has a neck but no head?",
        "A BOTTLE"
    },
    {
        4,
        {0x03, 0x01, 0x04, 0x04, 0x00, 0x00},
        "BASIC COMPASS TEMPO GLORY",
        "What has teeth but cannot bite?",
        "A COMB"
    },
    {
        5,
        {0x0F, 0x2E, 0x17, 0x33, 0x04, 0x00},
        "FINISH MACHINE NEEDLE SEAFOOD SPOON",
        "Why did the golfer wear two pairs of pants?",
        "IN CASE OF HOLE IN ONE"
    },
    {
        4,
        {0x19, 0x5C, 0x13, 0x02, 0x00, 0x00},
        "BLANK PENGUIN FUNNY TULIP",
        "What do you call a rabbit that does martial arts?",
        "\"KUNG FU\" BUNNY"
    },
    {
        4,
        {0x0F, 0x0F, 0x0F, 0x13, 0x00, 0x00},
        "VENUE RECORD RADAR CROWN",
        "What do you call a sleeping police car?",
        "AN UNDER-\"COVER\" CAR"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x1B, 0x04, 0x00},
        "HARMONY PENGUIN SOUND DIRTY FUTURE",
        "What did the pencil sharpener say to the pencil?",
        "STOP TURNING MY HEAD"
    },
    {
        4,
        {0x0F, 0x1B, 0x1B, 0x38, 0x00, 0x00},
        "JOURNEY FORTUNE CABINET POLITE",
        "Why did the orange stop rolling down the hill?",
        "IT RAN OUT OF JUICE"
    },
    {
        4,
        {0x0F, 0x0F, 0x05, 0x10, 0x00, 0x00},
        "WHISTLE KITTEN MACHINE MYSTERY",
        "What did the stamp say to the letter?",
        "\"STICK WITH ME\""
    },
    {
        4,
        {0x0F, 0x0F, 0x33, 0x0D, 0x00, 0x00},
        "SWIFT STEEP POCKET FIFTH",
        "Why did the broom jump for joy?",
        "SWEPT OFF ITS FEET"
    },
    {
        4,
        {0x33, 0x02, 0x01, 0x02, 0x00, 0x00},
        "DOLPHIN KINGDOM ORGAN UNION",
        "What do you call an owl magician?",
        "\"HOO-DINI\""
    },
    {
        4,
        {0x1E, 0x17, 0x1B, 0x13, 0x00, 0x00},
        "NOTEBOOK POTATO DOUGH SYMBOL",
        "Why did the skeleton cross the road?",
        "TO GET TO BODY SHOP"
    },
    {
        4,
        {0x1B, 0x17, 0x3C, 0x10, 0x00, 0x00},
        "JOURNEY ALPHABET VALLEY EIGHT",
        "What do you call a happy farmer in spring?",
        "A JOLLY PLANTER"
    },
    {
        4,
        {0x0F, 0x0F, 0x08, 0x01, 0x00, 0x00},
        "SWEET TIMER BLESS SPREAD",
        "When the tailor was asked how business was going, he said —",
        "\"SEW\" IT SEEMS"
    },
    {
        4,
        {0x0F, 0x15, 0x04, 0x10, 0x00, 0x00},
        "PRONE EVERY STEEP CYCLE",
        "The optician gave his patient a discount, which was a real —",
        "EYE OPENER"
    },
    {
        4,
        {0x1E, 0x0F, 0x06, 0x08, 0x00, 0x00},
        "WHISTLE LESSON BLOOM VIGOR",
        "When the cobbler lost his favorite tools, he felt like he —",
        "LOST HIS \"SOLE\""
    },
    {
        4,
        {0x1E, 0x2E, 0x01, 0x20, 0x00, 0x00},
        "FEATHER GLACIER CRANE SUMMER",
        "The fisherman was very popular with the town because he was —",
        "A REEL CATCH"
    },
    {
        4,
        {0x1E, 0x1E, 0x0F, 0x10, 0x00, 0x00},
        "CABINET SHIELD DELTA EIGHT",
        "When the butcher backed into the slicer, he got —",
        "A LITTLE BEHIND"
    },
    {
        4,
        {0x0F, 0x1E, 0x1A, 0x01, 0x00, 0x00},
        "WINDFALL HOLIDAY MAGNET TOUGH",
        "The carpenter finished building the table and proudly said —",
        "NAILED IT DOWN"
    },
    {
        4,
        {0x1E, 0x0E, 0x02, 0x08, 0x00, 0x00},
        "MARKET WIDTH ENOUGH FIGHT",
        "When the electricity failed during class, the students were —",
        "IN THE DARK"
    },
    {
        4,
        {0x0F, 0x01, 0x01, 0x04, 0x00, 0x00},
        "CATTLE SOLVE LOWER FRONT",
        "The pirate had trouble learning the alphabet because he was —",
        "LOST AT \"C\""
    },
    {
        4,
        {0x1E, 0x1E, 0x1E, 0x18, 0x00, 0x00},
        "MORNING ENOUGH FLIGHT GUILD",
        "When the baker won the lottery, his friends knew he was —",
        "ROLLING IN DOUGH"
    },
    {
        4,
        {0x0F, 0x1D, 0x0D, 0x01, 0x00, 0x00},
        "RAINBOW WIDTH DRONE ELECT",
        "The plumber had to retire early because all his plans went —",
        "DOWN THE DRAIN"
    },
    {
        4,
        {0x0F, 0x0F, 0x0F, 0x2D, 0x00, 0x00},
        "PANTHER RIDGE SIGHT ENGINE",
        "When the gardener was praised for his flowers, he said —",
        "DIGGING THE PRAISE"
    },
    {
        4,
        {0x0F, 0x0F, 0x27, 0x02, 0x00, 0x00},
        "DEVICE MANGO ESCAPE WORST",
        "The watchmaker was asked for the time, and he replied —",
        "GIVE ME A SECOND"
    },
    {
        4,
        {0x0F, 0x1E, 0x08, 0x01, 0x00, 0x00},
        "BASIS THOSE TRAFFIC FEATHER",
        "When the baseball player struck out, his coach told him —",
        "OFF HIS BASE"
    },
    {
        4,
        {0x17, 0x07, 0x02, 0x10, 0x00, 0x00},
        "ACTIVE ABOUT SUNSHINE PLUME",
        "The barber was thrilled with his successful shop because it was —",
        "A CUT ABOVE"
    },
    {
        4,
        {0x0F, 0x0F, 0x16, 0x03, 0x00, 0x00},
        "BLANKET STOCK THINK FANCY",
        "When the musician fell through the floor, he was —",
        "FLAT ON HIS BACK"
    },
    {
        4,
        {0x0F, 0x1E, 0x06, 0x02, 0x00, 0x00},
        "TORQUE TREASURE CUSTOM POUND",
        "The math teacher went to the farm looking for —",
        "SQUARE ROOTS"
    },
    {
        4,
        {0x0F, 0x0F, 0x1A, 0x15, 0x00, 0x00},
        "ROUGH TOOTH SHADOW FIFTH",
        "When the chef seasoned the soup, he told the waiter —",
        "FOOD FOR THOUGHT"
    },
    {
        4,
        {0x0F, 0x0F, 0x03, 0x02, 0x00, 0x00},
        "OCTOPUS PHOTO PAUSE AUDIO",
        "The lazy kangaroo spent all afternoon being a —",
        "\"POUCH\" POTATO"
    },
    {
        4,
        {0x0F, 0x17, 0x0F, 0x09, 0x00, 0x00},
        "WHISTLE FEATHER HELLO SENSE",
        "Why did the crab never share his lunch with the starfish?",
        "HE WAS \"SHELL-FISH\""
    },
    {
        4,
        {0x0F, 0x0F, 0x0F, 0x32, 0x00, 0x00},
        "VIOLIN ENGINE GENTLE THUNDER",
        "When the tightrope walker lost his footing, he was —",
        "LIVING ON THE EDGE"
    },
    {
        4,
        {0x0F, 0x1B, 0x01, 0x10, 0x00, 0x00},
        "PLANET STREET OFFER GATHER",
        "The pilot didn't want to argue about the flight plan because it was —",
        "PLANE TO SEE"
    },
    {
        5,
        {0x0F, 0x0F, 0x1E, 0x1B, 0x40, 0x00},
        "TEMPLE CUSTOM SELDOM PLUME JOURNEY",
        "When the lumberjack couldn't answer the riddle, he was —",
        "COMPLETELY STUMPED"
    },
    {
        5,
        {0x0F, 0x0F, 0x1B, 0x17, 0x48, 0x00},
        "FLIGHT HOUND THROAT ADOPT CAPTAIN",
        "The dentist and the manicurist fell in love and —",
        "FOUGHT TOOTH AND NAIL"
    },
    {
        4,
        {0x17, 0x17, 0x05, 0x10, 0x00, 0x00},
        "ACTIVE NEEDLE STAKE SNAKE",
        "When the skunk couldn't pay the bill, he told the waiter to —",
        "LEAVE A \"SCENT\""
    },
    {
        5,
        {0x1E, 0x0F, 0x0F, 0x2B, 0x08, 0x00},
        "PEACOCK SKETCH FIFTH CHARGE CREDIT",
        "The clock was sent to the principal's office because it —",
        "TICKED OFF TEACHERS"
    },
    {
        4,
        {0x1E, 0x02, 0x02, 0x01, 0x00, 0x00},
        "DAMAGE LEOPARD GRAPH POLAR",
        "When the sheep took over the farm, the neighbors called it a —",
        "\"RAM-PAGE\""
    },
    {
        4,
        {0x0F, 0x0F, 0x1E, 0x02, 0x00, 0x00},
        "HARBOR MOUNT SECTOR PRIZE",
        "The tree surgeon went on vacation because he wanted to —",
        "BRANCH OUT MORE"
    },
    {
        4,
        {0x1E, 0x0D, 0x01, 0x10, 0x00, 0x00},
        "PRIZE BLEND DOUBLE DRAWER",
        "When the meteorologist arrived on time, everyone said he —",
        "BREEZED IN"
    },
    {
        4,
        {0x0F, 0x0F, 0x1C, 0x05, 0x00, 0x00},
        "WINDFALL BLANKET SHARK GLANCE",
        "The artist didn't know what to paint next, so he was —",
        "DRAWING A BLANK"
    },
    {
        4,
        {0x0F, 0x0F, 0x0B, 0x08, 0x00, 0x00},
        "WINDFALL PLEAD GUILD BRIDGE",
        "When the snake passed the math quiz, the teacher said it was —",
        "\"ADD-ING\" UP WELL"
    },
    {
        5,
        {0x1E, 0x1D, 0x0F, 0x17, 0x02, 0x00},
        "RAINBOW WITCH DONOR TODAY NEEDLE",
        "The ghost couldn't find a partner at the dance because he had —",
        "\"NO-BODY\" TO DANCE WITH"
    },
    {
        5,
        {0x0E, 0x1B, 0x0F, 0x5C, 0x04, 0x00},
        "EXIST GROWL MINUS CHIMNEY THUNDER",
        "When the hotel on the beach flooded, the guests were —",
        "SWIMMING IN LUXURY"
    },
    {
        4,
        {0x0F, 0x0F, 0x0F, 0x1D, 0x00, 0x00},
        "BUTTON HARBOR DENSE DRONE",
        "The candle factory closed its doors because the workers were —",
        "BURNED AT BOTH ENDS"
    },
    {
        4,
        {0x0F, 0x0F, 0x1B, 0x05, 0x00, 0x00},
        "CABINET HONEST STEAL LASER",
        "When the banker lost his composure, his colleagues said he —",
        "LOST HIS BALANCE"
    },
    {
        4,
        {0x17, 0x01, 0x02, 0x01, 0x00, 0x00},
        "GHOST DIAMOND MORAL ANGLE",
        "The dog sat by the fireplace all winter because he was —",
        "A HOT DOG"
    },
    {
        4,
        {0x3A, 0x07, 0x01, 0x01, 0x00, 0x00},
        "RAINBOW LAWYER YELLOW WEIGHT",
        "When the quarterback gave an interview, the reporters were —",
        "BLOWN AWAY"
    },
    {
        4,
        {0x0F, 0x0F, 0x0F, 0x1B, 0x00, 0x00},
        "REWARD NUMBER DESERT READY",
        "The detective arrested the calendar maker because his —",
        "DAYS WERE NUMBERED"
    },
    {
        4,
        {0x0F, 0x1D, 0x03, 0x08, 0x00, 0x00},
        "STRING SPRING AGAIN CLEAN",
        "When the baker's apprentice made great sourdough, he was —",
        "A RISING STAR"
    },
    {
        4,
        {0x0F, 0x0F, 0x23, 0x09, 0x00, 0x00},
        "WINDFALL STAGE GOLDEN FAVOR",
        "The elevator attendant had a bad day because business was —",
        "GOING DOWN FAST"
    },
    {
        4,
        {0x1D, 0x0F, 0x0B, 0x03, 0x00, 0x00},
        "OCTOPUS SHELF HONOR FLASK",
        "When the frog took the stage, the audience gave him a —",
        "\"HOLE\" LOT OF HOPS"
    },
    {
        5,
        {0x0F, 0x0F, 0x17, 0x2B, 0x02, 0x00},
        "CAPTAIN SUNSHINE HEAVEN DOMAIN ENJOY",
        "The lawyer was delighted with his new case because it was —",
        "AN OPEN AND SHUT CASE"
    },
    {
        4,
        {0x0F, 0x1E, 0x3C, 0x19, 0x00, 0x00},
        "PICTURE MODERN THUNDER FIBER",
        "When the cow won the ribbon at the county fair, it was —",
        "\"UDDER\" PERFECTION"
    },
    {
        4,
        {0x0F, 0x0F, 0x0F, 0x14, 0x00, 0x00},
        "SEAFOOD FOUND DOCTOR INSECT",
        "The photographer loved developing black and white pictures because they —",
        "FOCUSED ON FACTS"
    },
    {
        4,
        {0x0F, 0x0F, 0x17, 0x0E, 0x00, 0x00},
        "OCTOPUS SPHERE FARMER HURRY",
        "When the golfer made a miraculous putt, the gallery said —",
        "PAR FOR THE COURSE"
    },
    {
        4,
        {0x1B, 0x0F, 0x15, 0x11, 0x00, 0x00},
        "WEATHER NOTEBOOK BLOCK BADLY",
        "The librarian was an extraordinary detective because she —",
        "WENT BY THE BOOK"
    },
    {
        4,
        {0x0F, 0x01, 0x02, 0x08, 0x00, 0x00},
        "IMPACT TOUCH THUMB SCOUT",
        "When the pig won the jackpot, all his barn friends told him to —",
        "HAM IT UP"
    },
    {
        4,
        {0x0F, 0x1E, 0x08, 0x04, 0x00, 0x00},
        "WHEEL NEEDLE SKULL POLAR",
        "The shoemaker's new assistant was learning fast and was —",
        "WELL-HEELED"
    },
    {
        4,
        {0x1B, 0x0F, 0x1A, 0x01, 0x00, 0x00},
        "MACHINE STING LAUGH SMELL",
        "When the tennis star won the championship, his serve was —",
        "A SMASHING HIT"
    },
    {
        4,
        {0x1D, 0x33, 0x07, 0x02, 0x00, 0x00},
        "GIRAFFE FEATHER RECORD DONOR",
        "The battery was never worried about debt because it was —",
        "FREE OF CHARGE"
    },
    {
        4,
        {0x0F, 0x1D, 0x1C, 0x06, 0x00, 0x00},
        "BUTTON PROMISE JELLY LINEN",
        "When the duck paid for dinner, he told the waiter —",
        "PUT IT ON MY \"BILL\""
    },
    {
        4,
        {0x0F, 0x1B, 0x0F, 0x12, 0x00, 0x00},
        "WHISTLE DOCTOR FLOUR OTHER",
        "The astronomer loved his late night job because it was —",
        "OUT OF THIS WORLD"
    },
    {
        4,
        {0x0F, 0x17, 0x0F, 0x09, 0x00, 0x00},
        "WEATHER ALPHABET BREED PENGUIN",
        "When the spider designed a new website, the client said it had —",
        "GREAT WEB APPEAL"
    },
    {
        4,
        {0x0F, 0x0F, 0x0F, 0x1C, 0x00, 0x00},
        "CABINET SOLDIER TENNIS RATIO",
        "The horse was happy in the barn because he was in —",
        "STABLE CONDITION"
    },
    {
        4,
        {0x0F, 0x0F, 0x17, 0x0B, 0x00, 0x00},
        "TENDER FORTUNE CLOVER LUNCH",
        "When the mirror fell off the wall, the owner said he —",
        "COULD NOT REFLECT"
    },
    {
        4,
        {0x0F, 0x0F, 0x1B, 0x0C, 0x00, 0x00},
        "FINGER CRYSTAL REBEL GLORY",
        "The magician had to cancel his airplane flight because he was a —",
        "FLYING \"SORCERER\""
    },
    {
        4,
        {0x17, 0x17, 0x0D, 0x0A, 0x00, 0x00},
        "KINGDOM ALPHABET BEACH NORMAL",
        "When the snowman went to the gym, he worked on his —",
        "\"AB-DOMINAL\" PACK"
    },
    {
        4,
        {0x0F, 0x17, 0x07, 0x20, 0x00, 0x00},
        "ANIMAL GLACIER FIREFLY MYSTERY",
        "The bell ringer loved his morning routine because it had a —",
        "FAMILIAR RING"
    },
    {
        4,
        {0x0F, 0x0F, 0x3C, 0x10, 0x00, 0x00},
        "KINGDOM SOLDIER UNICORN DONOR",
        "When the geologist proposed on one knee, he gave her a —",
        "ROCK SOLID RING"
    },
    {
        4,
        {0x0F, 0x1A, 0x08, 0x02, 0x00, 0x00},
        "RAINBOW SWAMP PENGUIN MUSEUM",
        "The author loved working near the campfire because the plot was —",
        "WARMING UP"
    },
    {
        4,
        {0x0F, 0x0F, 0x1A, 0x10, 0x00, 0x00},
        "QUEEN SNACK CLOAK ROCKY",
        "When the pig entered the clean pen, he said it was —",
        "SQUEAKY CLEAN"
    },
    {
        4,
        {0x0F, 0x0F, 0x17, 0x06, 0x00, 0x00},
        "MANNER COACH FEATHER PROFIT",
        "The diver explored the coral reef and discovered —",
        "AN OCEAN OF CHARM"
    },
    {
        4,
        {0x0F, 0x17, 0x0D, 0x01, 0x00, 0x00},
        "FRIEND ISLAND DRIFT TEACH",
        "When the farmer looked over his wheat crop, he said it was —",
        "FIRST IN FIELD"
    },
    {
        4,
        {0x1B, 0x0F, 0x0E, 0x04, 0x00, 0x00},
        "SKETCH ORCHID GUARD ELDER",
        "The violinist was praised by the critics because his playing —",
        "STRUCK A CHORD"
    },
    {
        4,
        {0x2D, 0x0F, 0x26, 0x01, 0x00, 0x00},
        "PENGUIN ISLAND WINDFALL LEAP",
        "When the sailor navigated into port without a map, he said —",
        "PLAIN SAILING"
    },
    {
        4,
        {0x0F, 0x0F, 0x1D, 0x02, 0x00, 0x00},
        "PRINCE REFER UNICORN ARISE",
        "The chef dropped his favorite pan and said it was a —",
        "RECIPE FOR RUIN"
    },
    {
        4,
        {0x0F, 0x0F, 0x3A, 0x16, 0x00, 0x00},
        "PIRATES LIGHT WHISTLE QUERY",
        "When the bowler got three strikes in a row, he was —",
        "RIGHT UP HIS ALLEY"
    },
    {
        4,
        {0x53, 0x0F, 0x0B, 0x08, 0x00, 0x00},
        "WINDFALL FLOCK SOCKET MINUS",
        "The candle was very popular because it was always —",
        "SO FULL OF WICK"
    },
    {
        4,
        {0x1B, 0x0F, 0x0E, 0x10, 0x00, 0x00},
        "SOLDIER FORTUNE GUEST CREST",
        "When the runner crossed the finish line, he said he was —",
        "OUT OF STRIDES"
    },
    {
        4,
        {0x0F, 0x17, 0x15, 0x02, 0x00, 0x00},
        "SOCKET STUDY EXCUSE BEING",
        "The locksmith was hired immediately because he had the —",
        "KEY TO SUCCESS"
    },
    {
        5,
        {0x0F, 0x17, 0x39, 0x2B, 0x03, 0x00},
        "RAINBOW POWDER BLANKET GUITAR GRAPE",
        "When the dog barked at the oak tree, his owner said he was —",
        "BARKING UP WRONG TREE"
    },
    {
        4,
        {0x33, 0x1B, 0x01, 0x04, 0x00, 0x00},
        "LEOPARD CANDY STAND TRASH",
        "The window cleaner loved his tall job because it was —",
        "CLEAR AS DAY"
    },
    {
        4,
        {0x17, 0x66, 0x0F, 0x2A, 0x00, 0x00},
        "TOMATO JOURNEY FLEET RESCUE",
        "When the sheep sheared his wool, he told his pal —",
        "\"FLEECE\" TO MEET YOU"
    },
    {
        4,
        {0x0F, 0x0F, 0x0F, 0x16, 0x00, 0x00},
        "ROCKET TARGET TENTH THIGH",
        "The train conductor loved his morning route because it was —",
        "ON THE RIGHT TRACK"
    },
    {
        4,
        {0x0F, 0x0F, 0x09, 0x10, 0x00, 0x00},
        "WEATHER HOUSE TRACE DRIVE",
        "When the bee landed on the rose, the gardener said it was —",
        "A SWEET TOUCH"
    },
    {
        4,
        {0x6A, 0x1D, 0x06, 0x08, 0x00, 0x00},
        "ALPHABET SHIFT RITUAL CABLE",
        "The tailor made a pair of trousers with two pockets and said —",
        "FITS THE BILL"
    },
    {
        4,
        {0x0F, 0x17, 0x2D, 0x0B, 0x00, 0x00},
        "WOUND TOMATO ORCHID HORSE",
        "When the pilot landed safely in the fog, his copilot said —",
        "SMOOTH TOUCH DOWN"
    },
    {
        4,
        {0x0F, 0x36, 0x0B, 0x20, 0x00, 0x00},
        "MODERN PANTHER LUNAR LEOPARD",
        "The baseball player was thrilled with his new contract because it was —",
        "A HOME RUN DEAL"
    },
    {
        4,
        {0x33, 0x6A, 0x09, 0x04, 0x00, 0x00},
        "VOLCANO KINGDOM SHAFT RITUAL",
        "When the cow jumped over the moon, the calf said it was —",
        "\"MOO\"-VING FAST"
    },
    {
        4,
        {0x0F, 0x0F, 0x16, 0x01, 0x00, 0x00},
        "POLITE TENTH WHOLE FLOCK",
        "The carpenter admired the antique cabinet and said it was —",
        "TOP OF THE LINE"
    },
    {
        4,
        {0x0F, 0x0F, 0x23, 0x08, 0x00, 0x00},
        "SOCKET APART TUNNEL THROW",
        "When the ghost joined the choir, the conductor said his voice was —",
        "\"SPOOK\"-TACULAR"
    },
    {
        4,
        {0x0F, 0x1B, 0x0A, 0x08, 0x00, 0x00},
        "WINTER DOCTOR LOVER OPERA",
        "The gardener won the giant pumpkin contest because he was —",
        "ROOTED TO WIN"
    },
    {
        4,
        {0x0F, 0x0F, 0x0C, 0x01, 0x00, 0x00},
        "MOTHER REIGN POINT TIMBER",
        "When the clock struck midnight, the night watchman said —",
        "RIGHT ON TIME"
    },
    {
        4,
        {0x0F, 0x35, 0x32, 0x02, 0x00, 0x00},
        "SEAFOOD DIAMOND ISLAND QUILT",
        "The fish stayed in deep water during the storm to remain —",
        "SAFE AND SOUND"
    },
    {
        4,
        {0x1E, 0x17, 0x1E, 0x01, 0x00, 0x00},
        "CLOAK PARENT BUDDY FATAL",
        "When the baker made fresh croissants, his customers said —",
        "FLAKY AND PROUD"
    },
    {
        4,
        {0x0F, 0x17, 0x07, 0x10, 0x00, 0x00},
        "PURPLE CRYSTAL FLAME NUMBER",
        "The cat chased the ball of yarn and declared it —",
        "\"PURR\"-FECT PLAY"
    },
    {
        4,
        {0x17, 0x0F, 0x1B, 0x08, 0x00, 0x00},
        "CAPTAIN INSIDE SOUND FRIEND",
        "When the photographer took a snapshot of the cheetah, it was —",
        "A SNAP DECISION"
    },
    {
        4,
        {0x0F, 0x0F, 0x3C, 0x08, 0x00, 0x00},
        "CURVE ENTER LANTERN CRUST",
        "The electrician was always excited because he loved —",
        "CURRENT EVENTS"
    },
    {
        4,
        {0x1B, 0x0F, 0x13, 0x18, 0x00, 0x00},
        "WEATHER MOTHER MOUSE STREET",
        "When the bird built a sturdy nest, her mate said —",
        "HOME TWEET HOME"
    },
    {
        4,
        {0x0F, 0x0F, 0x17, 0x11, 0x00, 0x00},
        "TONGUE INSECT CRUST CATER",
        "The barber gave everyone a quick trim and said he was —",
        "CUTTING CORNERS"
    },
    {
        4,
        {0x0F, 0x17, 0x3C, 0x36, 0x00, 0x00},
        "BOTTLE DOLPHIN MACHINE NEEDLE",
        "When the ice sculptor finished his swan, he was —",
        "CHILLED TO THE BONE"
    },
    {
        4,
        {0x0F, 0x0F, 0x0F, 0x15, 0x00, 0x00},
        "AIRPORT FORTUNE OCEAN TALENT",
        "The detective looked at the muddy boots and said —",
        "A CLEAR FOOTPRINT"
    },
    {
        4,
        {0x0F, 0x3C, 0x07, 0x10, 0x00, 0x00},
        "SECTOR SAILOR ROUND STRING",
        "When the painter finished the wall in blue, he said —",
        "IN TRUE COLORS"
    },
    {
        4,
        {0x0F, 0x1A, 0x02, 0x02, 0x00, 0x00},
        "MASTER RADISH THIGH WHALE",
        "The tennis champion won the final set with —",
        "A SMASH HIT"
    },
    {
        4,
        {0x0F, 0x3A, 0x03, 0x10, 0x00, 0x00},
        "ALPHABET GIRAFFE OTHER AWAKE",
        "When the frog leaped across the lily pads, he took a —",
        "LEAP OF FAITH"
    },
    {
        4,
        {0x0F, 0x33, 0x0C, 0x10, 0x00, 0x00},
        "DAMAGE GIRAFFE STONE JUDGE",
        "The jeweler polished the emerald until it was —",
        "A GEM OF A FIND"
    },
    {
        4,
        {0x0F, 0x0F, 0x0F, 0x22, 0x00, 0x00},
        "FINGER SHORT RATIO BOTTLE",
        "When the farmer repaired his barn roof, he was —",
        "RAISING THE ROOF"
    },
    {
        4,
        {0x1D, 0x0F, 0x19, 0x0B, 0x00, 0x00},
        "RAINBOW SWING LAUGH HONOR",
        "The musician played his trumpet so loud he was —",
        "BLOWING HIS HORN"
    },
    {
        4,
        {0x17, 0x1E, 0x06, 0x01, 0x00, 0x00},
        "SHADOW TWICE DECIDE ISSUE",
        "When the owl gave advice in the forest, everyone said —",
        "A WISE CHOICE"
    },
    {
        4,
        {0x0F, 0x2D, 0x17, 0x02, 0x00, 0x00},
        "DOUBLE FINGER ROYAL COMPASS",
        "The runner tied his sneakers tight and said he was —",
        "BOUND FOR GLORY"
    },
    {
        4,
        {0x0F, 0x0F, 0x17, 0x02, 0x00, 0x00},
        "NOTEBOOK DOUBLE PASTEL PLANE",
        "When the bookbinder finished the leather volume, he said —",
        "BOUND TO PLEASE"
    },
    {
        5,
        {0x0F, 0x1E, 0x1D, 0x0F, 0x32, 0x00},
        "COMPASS WHISTLE COFFEE LEASE SAMPLE",
        "When the optometrist fell into the lens grinder, he made —",
        "A SPECTACLE OF HIMSELF"
    },
    {
        6,
        {0x1D, 0x0F, 0x0F, 0x1B, 0x1D, 0x09},
        "ACTIVE NOTEBOOK STAKE SELDOM MOMENT NATURE",
        "The symphony orchestra visited the investment firm —",
        "TO MAKE A SOUND INVESTMENT"
    },
    {
        6,
        {0x0F, 0x0F, 0x17, 0x17, 0x2D, 0x02},
        "WINDFALL WHISPER PEACOCK PLUCK AIRPORT BLAST",
        "When the mummy expert was buried in research papers, he was —",
        "ALL WRAPPED UP IN HIS WORK"
    },
    {
        5,
        {0x1B, 0x3C, 0x15, 0x1B, 0x15, 0x00},
        "NOTEBOOK PEACOCK STOCK FRAUD FOREST",
        "The clock stopped right during dinner, so the hungry family went —",
        "BACK FOR FOUR SECONDS"
    },
    {
        5,
        {0x0F, 0x0F, 0x1B, 0x17, 0x24, 0x00},
        "FLIGHT HOUND THROAT ADOPT SUNSET",
        "The dentist and the manicurist fell in love and agreed they —",
        "FOUGHT TOOTH AND NAIL"
    },
    {
        4,
        {0x0F, 0x0F, 0x1B, 0x16, 0x00, 0x00},
        "MEDIA THEATER STATUE NOISE",
        "When the chimney sweep tried on his custom tuxedo, it —",
        "SUITED HIM TO A TEE"
    },
    {
        6,
        {0x0F, 0x0F, 0x0F, 0x0F, 0x39, 0x02},
        "GOLDEN SUNSHINE TENTH FINISH HOLIDAY PITCH",
        "The scarecrow was promoted to regional vice president because he was —",
        "\"OUT-STANDING\" IN HIS FIELD"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x1B, 0x2D, 0x00},
        "HORIZON LIZARD EVENT DRAGON TONGUE",
        "When the tightrope walker lost his footing high above, he was —",
        "LIVING ON THE RAZOR EDGE"
    },
    {
        6,
        {0x0F, 0x0F, 0x1D, 0x0F, 0x1E, 0x04},
        "SIMPLE TEMPLE THUNDER YELLOW DOCTOR SHELL",
        "The lumberjack couldn't solve the crossword puzzle because he was —",
        "COMPLETELY STUMPED ON IT"
    },
    {
        4,
        {0x1D, 0x1E, 0x0F, 0x18, 0x00, 0x00},
        "CRYSTAL BALLOON TOTAL ADULT",
        "When the pirate captain took the reading test, he admitted he was —",
        "TOTALLY LOST AT \"C\""
    },
    {
        5,
        {0x0F, 0x0F, 0x1B, 0x35, 0x33, 0x00},
        "WEATHER STRIKE SOCKET ENOUGH HEALTH",
        "The butcher was having a tough afternoon at the counter because —",
        "THE STEAKS WERE TOO HIGH"
    },
    {
        5,
        {0x1E, 0x0F, 0x0F, 0x17, 0x02, 0x00},
        "SQUARE WANDER BRICK KNIFE WEAPON",
        "When the marathon runner entered the bakery, she asked for —",
        "A QUICK BREAD WINNER"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x2B, 0x39, 0x00},
        "MARKET PIRATES ICING GENTLE SUNSET",
        "The photographer took a picture of the thunderstorm and said it was —",
        "A STRIKING MASTERPIECE"
    },
    {
        4,
        {0x0F, 0x2D, 0x09, 0x10, 0x00, 0x00},
        "BOTTLE FRIEND INSECT SHOOT",
        "When the tailor finished three custom suits in one day, he was —",
        "FIT TO BE TIED"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x17, 0x0D, 0x00},
        "WHISTLE FELLOW THROW WOUND TROOP",
        "The astronomer stared at the distant galaxy and proclaimed —",
        "OUT OF THIS WHOLE WORLD"
    },
    {
        5,
        {0x0F, 0x0F, 0x17, 0x17, 0x11, 0x00},
        "MORTAL LEOPARD FEATHER HEDGE DELTA",
        "When the baseball team bought a flight to Florida, they were —",
        "HEADED FOR HOME PLATE"
    },
    {
        6,
        {0x0F, 0x0F, 0x1B, 0x0F, 0x1B, 0x01},
        "WARRIOR KITTEN NUMBER PRONE HEDGE GUITAR",
        "The dog trainer had trouble finding his runaway pup because he was —",
        "BARKING UP THE WRONG TREE"
    },
    {
        6,
        {0x1D, 0x0F, 0x0F, 0x36, 0x1D, 0x04},
        "WINDFALL LUMBER LEADER MYSTERY EVERY FAULT",
        "When the detective opened the calendar, he warned the crook that his —",
        "DAYS WERE FULLY NUMBERED"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x0F, 0x1A, 0x00},
        "TOMATO OCTOPUS PUPPET CLOTH THREE",
        "The lazy kangaroo spent his entire summer vacation being a —",
        "COMPLETE \"POUCH\" POTATO"
    },
    {
        5,
        {0x0F, 0x0F, 0x17, 0x1E, 0x0C, 0x00},
        "PENGUIN REGION DOLPHIN ROUND VALID",
        "When the baker made twenty loaves of sourdough, his accountant said he was —",
        "ROLLING DEEP IN DOUGH"
    },
    {
        6,
        {0x0F, 0x1B, 0x0F, 0x0F, 0x36, 0x44},
        "EXCUSE TRAVEL SECRET LETTER GENTLE LANTERN",
        "The electrician received an award from the city council for —",
        "EXCELLENT CURRENT EVENTS"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x27, 0x0C, 0x00},
        "VESSEL WHISTLE YELLOW NOTEBOOK GLORY",
        "When the cobbler lost his favorite leather hammer, he cried that he had —",
        "LOST HIS VERY OWN \"SOLE\""
    },
    {
        5,
        {0x1B, 0x0F, 0x1D, 0x0F, 0x09, 0x00},
        "ALPHABET BICYCLE TARGET CRUEL LANTERN",
        "The deep sea fisherman had a fantastic morning on the boat and was —",
        "A TRULY REEL BIG CATCH"
    },
    {
        5,
        {0x0F, 0x0F, 0x1B, 0x0F, 0x04, 0x00},
        "CABINET GLANCE CAPTAIN LEARN LANTERN",
        "When the tightrope walker fell into the safety net, the ringmaster said —",
        "A REAL BALANCING ACT"
    },
    {
        5,
        {0x0F, 0x17, 0x1E, 0x56, 0x1C, 0x00},
        "TORQUE PICTURE TREASURE FORTUNE LESSON",
        "The math teacher built a fence around his square garden to protect his —",
        "PRECIOUS SQUARE ROOTS"
    },
    {
        5,
        {0x1D, 0x0F, 0x0F, 0x0F, 0x0D, 0x00},
        "PROMISE PASTEL NEEDLE SILENT LUNAR",
        "When the pilot flew through the clear blue sky, he noticed that it was —",
        "PLAIN AND SIMPLE TO SEE"
    },
    {
        5,
        {0x0F, 0x1E, 0x1D, 0x17, 0x58, 0x00},
        "MACHINE DOLPHIN OCTOPUS UNIQUE WHISTLE",
        "The chef was overwhelmed by the holiday rush and complained that he had —",
        "TOO MUCH UPON HIS PLATE"
    },
    {
        5,
        {0x0F, 0x0F, 0x1B, 0x17, 0x14, 0x00},
        "FEATHER HORIZON NOTICE NEEDLE SPIKE",
        "When the golfer sank the forty foot putt for eagle, he called it —",
        "A TEE-RIFIC HOLE IN ONE"
    },
    {
        5,
        {0x0F, 0x17, 0x0F, 0x17, 0x04, 0x00},
        "HEAVEN CABINET DATED AUDIO WEATHER",
        "The barber was voted the best shopkeeper in town because his work was —",
        "A HEAD AND A CUT ABOVE"
    },
    {
        4,
        {0x39, 0x0F, 0x17, 0x01, 0x00, 0x00},
        "ALPHABET NOTEBOOK DEBUT OLIVE",
        "When the sheep sheared off all his wool for summer, his flock called him —",
        "BAA-D TO THE BONE"
    },
    {
        5,
        {0x0F, 0x1D, 0x0F, 0x17, 0x0F, 0x00},
        "HEAVEN WARRIOR MYSTERY REGION ENTER",
        "The meteorologist didn't mind the blizzard one bit because she was —",
        "WEATHERING EVERY STORM"
    },
    {
        5,
        {0x0F, 0x17, 0x1B, 0x0F, 0x17, 0x00},
        "ANSWER ALPHABET NOTEBOOK DECOR FORTUNE",
        "When the bank teller was promoted to branch manager, her colleagues said —",
        "A SOUND BALANCE OF POWER"
    },
    {
        5,
        {0x0F, 0x0F, 0x3A, 0x0F, 0x0F, 0x00},
        "REGION GIANT MORNING STAGE GATHER",
        "The carpenter inspected the crooked bookshelf and told his apprentice —",
        "GOING AGAINST THE GRAIN"
    },
    {
        5,
        {0x17, 0x0F, 0x0F, 0x2B, 0x2C, 0x00},
        "ALPHABET BLANKET TONGUE FEATHER JOURNEY",
        "When the frog won the gold medal in the triple jump, it was —",
        "AN UN-FROG-ETTABLE LEAP"
    },
    {
        6,
        {0x0F, 0x0F, 0x0F, 0x1D, 0x13, 0x18},
        "WHISTLE NOTEBOOK ROCKET BOTTLE BELLY FIFTY",
        "The librarian solved the cold case mystery because she always —",
        "WENT STRICTLY BY THE BOOK"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x6C, 0x10, 0x00},
        "DANGER LEADER TRADE JOURNEY FIFTY",
        "When the cow stepped into the dairy parlor, the herdsman declared —",
        "AN \"UDDER\"-LY GREAT DAY"
    },
    {
        5,
        {0x0F, 0x0F, 0x17, 0x3A, 0x02, 0x00},
        "JUNGLE WINDFALL BLANKET CRYSTAL FARMER",
        "The artist was unable to paint his masterpiece portrait and was —",
        "JUST DRAWING A BLANK"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x1D, 0x07, 0x00},
        "KINGDOM MOTION HONEST CREDIT OFTEN",
        "When the clockmaker fixed the antique grandfather clock, he did it —",
        "IN THE NICK OF GOOD TIME"
    },
    {
        6,
        {0x0F, 0x0F, 0x0F, 0x0F, 0x27, 0x04},
        "HEAVEN AIRPORT ENGINE GENTLE ENOUGH WORST",
        "The gardener loved growing grapes along the stone wall because he was —",
        "HEARING ON THE GRAPEVINE"
    },
    {
        6,
        {0x0F, 0x1E, 0x1E, 0x1E, 0x1B, 0x04},
        "SOCKET PICTURE PAINTER TREASURE ROGUE MERCY",
        "When the tennis star served five aces in a single game, she made —",
        "A SERIOUS RACKET IN COURT"
    },
    {
        4,
        {0x0F, 0x1D, 0x17, 0x13, 0x00, 0x00},
        "STRIKE KNIGHT THEATER HEAVY",
        "The author loved typing on his vintage mechanical typewriter because it —",
        "HIT THE RIGHT KEYS"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x35, 0x1C, 0x00},
        "SOCKET PAINTER FINGER THEATER WARRIOR",
        "When the bowler rolled twelve strikes in a row, the alley manager said —",
        "A STRIKING PERFECTION"
    },
    {
        6,
        {0x0F, 0x0F, 0x0F, 0x0F, 0x1E, 0x0C},
        "WARRIOR DIGIT DANGER HONEST GHOST BOTTLE",
        "The plumber worked all night on the burst pipe so that his business wouldn't —",
        "GO STRAIGHT DOWN THE DRAIN"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x0F, 0x17, 0x00},
        "SKETCH MOMENT THUNDER CANDLE SCORE",
        "When the skunk entered the five star French restaurant, the maitre d' said —",
        "DOES NOT MAKE MUCH \"SCENT\""
    },
    {
        6,
        {0x0F, 0x0F, 0x1D, 0x1D, 0x72, 0x05},
        "DIAMOND GOLDEN SUNSHINE TREATY HARMONY SHIELD",
        "The sailor was promoted to ship captain because he was known for —",
        "SMOOTH AND STEADY SAILING"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x0F, 0x17, 0x00},
        "CABINET BURST SUNSHINE HONEST SHIRT",
        "When the tree surgeon climbed the ancient giant redwood, he wanted to —",
        "BRANCH OUT HIS BUSINESS"
    },
    {
        5,
        {0x1E, 0x0F, 0x0F, 0x17, 0x17, 0x00},
        "PEACOCK SHOCK TRUNK STRIKE DRAIN",
        "The musician wrote an award winning film score that really —",
        "STRUCK A RESONANT CHORD"
    },
    {
        6,
        {0x0F, 0x0F, 0x2B, 0x1E, 0x39, 0x12},
        "MORTAL PEACOCK GLACIER THEORY FIREFLY LEAFY",
        "When the battery was acquitted of all charges in court, the judge said it was —",
        "COMPLETELY FREE OF CHARGE"
    },
    {
        5,
        {0x0F, 0x1E, 0x1B, 0x0F, 0x17, 0x00},
        "VOLCANO CABINET SOLDIER TREATY ENTRY",
        "The horse trotted into the newly built barn and was relieved to find —",
        "A VERY STABLE CONDITION"
    },
    {
        4,
        {0x0F, 0x0F, 0x0F, 0x35, 0x00, 0x00},
        "PLANET GENTLE SALAD THUNDER",
        "When the spider finished spinning the intricate geometric web, it had —",
        "SPUN A TANGLED TALE"
    },
    {
        5,
        {0x0F, 0x1E, 0x0F, 0x1E, 0x0E, 0x00},
        "VIOLIN BICYCLE LANTERN TREASURE GRASP",
        "The window washer climbed sixty stories up the skyscraper and saw —",
        "A CRYSTAL CLEAR VISION"
    },
    {
        5,
        {0x0F, 0x0F, 0x1E, 0x35, 0x44, 0x00},
        "DOUBLE REGION ISLAND DIAMOND PENGUIN",
        "When the bell ringer struck the giant cathedral chime, it had —",
        "A SOUND AND NOBLE RING"
    },
    {
        4,
        {0x0F, 0x0F, 0x0F, 0x36, 0x00, 0x00},
        "STRING HEDGE HONEST ACTION",
        "The watchmaker examined the miniature golden gears and said they were —",
        "RIGHT ON THE SECOND"
    },
    {
        6,
        {0x1E, 0x17, 0x0F, 0x1E, 0x1D, 0x20},
        "PENGUIN DOLPHIN INSIDE WINDFALL TREATY CARPET",
        "When the farmer doubled his harvest yield, his happy neighbor said —",
        "OUT-STANDING IN THE FIELD"
    },
    {
        6,
        {0x0F, 0x0F, 0x0F, 0x0F, 0x27, 0x10},
        "DEVICE TRAVEL BLANKET CORNER NEEDLE STALE",
        "The chemist loved working with helium and neon gas because they were —",
        "NOBLE AND NEVER REACTIVE"
    },
    {
        5,
        {0x0F, 0x0F, 0x1E, 0x1B, 0x09, 0x00},
        "BRIGHT LIMIT DOLPHIN UNITY TRUTH",
        "When the duck paid cash for her expensive feather hat, she told them —",
        "PUT IT RIGHT ON MY \"BILL\""
    },
    {
        5,
        {0x0F, 0x1D, 0x39, 0x0F, 0x1E, 0x00},
        "KITTEN MONKEY ALPHABET CHEER MERCY",
        "The chess grandmaster took a bite of his fresh croissant and declared —",
        "CHECKMATE IN THE BAKERY"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x0F, 0x2D, 0x00},
        "EQUAL WHISTLE NIGHT GLIDE TALENT",
        "When the pig won first prize at the state fair, his proud family said —",
        "SQUEALING WITH DELIGHT"
    },
    {
        5,
        {0x0F, 0x0F, 0x1B, 0x1D, 0x10, 0x00},
        "BLANKET ROCKET SOLDIER UNITY MOTHER",
        "The geologist took a vacation to the Grand Canyon because he found it —",
        "ROCK SOLID IN BEAUTY"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x0F, 0x18, 0x00},
        "STRIKE KINGDOM DAMAGE GREET CHEST",
        "When the runner finished the Boston Marathon, his proud coach said —",
        "MAKING GREAT STRIDES"
    },
    {
        5,
        {0x0F, 0x0F, 0x36, 0x36, 0x1B, 0x00},
        "MORNING GATHER SUNSHINE WEATHER IRONY",
        "The choir sang on top of the mountain ridge and reached —",
        "A HIGHER HARMONY IN TUNE"
    },
    {
        4,
        {0x0F, 0x1D, 0x1D, 0x13, 0x00, 0x00},
        "TIMBER AIRPORT EXPERT TORQUE",
        "When the detective found the stolen diamond watch, he said it was —",
        "ABOUT PROPER TIME"
    },
    {
        5,
        {0x0F, 0x1B, 0x0F, 0x17, 0x04, 0x00},
        "CABINET CAPTAIN LESSON UNICORN FROST",
        "The tailor sewed thirty tuxedo lapels in one evening and said it was —",
        "A SUITABLE OCCASION"
    },
    {
        5,
        {0x1D, 0x0F, 0x3C, 0x17, 0x02, 0x00},
        "LEOPARD HUNGRY SEAFOOD DRYER TUNER",
        "When the golfer sliced his tee shot into the woods, his caddie called it —",
        "A ROUGH ROUND OF PLAY"
    },
    {
        5,
        {0x0F, 0x1D, 0x0F, 0x2D, 0x0F, 0x00},
        "PAINTER PICTURE ENTRY THEORY FLEET",
        "The doctor was calm in the crowded emergency room because he had —",
        "PLENTY OF TRUE PATIENCE"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x35, 0x02, 0x00},
        "THEATER INSECT OCTOPUS SECTOR LOWER",
        "When the florist created a bridal bouquet of fifty red blossoms, she —",
        "ROSE TO THE OCCASION"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x33, 0x07, 0x00},
        "GLACIER THUNDER SHIELD DOLPHIN HEDGE",
        "The pilot took off into the sunset without a single delay and had —",
        "HEAD HIGH IN THE CLOUDS"
    },
    {
        5,
        {0x1D, 0x0F, 0x17, 0x1D, 0x14, 0x00},
        "AIRPORT FEATHER THUNDER SHEER SCENE",
        "When the diver found an oyster with five glowing pearls, it was —",
        "A TREASURE OF THE DEEP"
    },
    {
        4,
        {0x0F, 0x0F, 0x0F, 0x1B, 0x00, 0x00},
        "MEADOW SWITCH AGAIN NOTCH",
        "The carpenter measured the mahogany plank three times because he —",
        "SAW IT COMING AHEAD"
    },
    {
        5,
        {0x17, 0x0F, 0x1B, 0x0F, 0x09, 0x00},
        "WHISTLE MOTION MORNING GENTLE LAYER",
        "When the snowman sat beside the glowing campfire, he was —",
        "MELTING WITH EMOTION"
    },
    {
        5,
        {0x1E, 0x17, 0x0F, 0x1E, 0x08, 0x00},
        "PENGUIN FLIGHT NATION JOINT SCENT",
        "The baseball catcher held onto the pop fly with two strikes for —",
        "THE FINAL INNING OUT"
    },
    {
        5,
        {0x0F, 0x1D, 0x0F, 0x5C, 0x2D, 0x00},
        "JOURNEY WEIGHT BIRTH CABINET HUNGRY",
        "When the candle shop opened three new franchises, the owner was —",
        "BURNING BRIGHT WITH JOY"
    },
    {
        5,
        {0x0F, 0x0F, 0x55, 0x1D, 0x44, 0x00},
        "GOLDEN FIREFLY CHIMNEY STOOL PENGUIN",
        "The painter finished the seaside landscape mural and said it was —",
        "DONE IN FLYING COLORS"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x0F, 0x04, 0x00},
        "SOCKET FORTUNE CAUSE SCREW MANNER",
        "When the train conductor pulled into the grand terminal, he was —",
        "ON TRACK FOR SUCCESS"
    },
    {
        5,
        {0x1D, 0x0F, 0x1D, 0x0F, 0x09, 0x00},
        "BALLOON BREED THUNDER FOREST SEASON",
        "The author completed the suspenseful mystery novel and said —",
        "BOUND FOR BEST SELLER"
    },
    {
        5,
        {0x0F, 0x17, 0x1B, 0x3C, 0x1A, 0x00},
        "THEATER HARMONY ALPHABET SEAFOOD STAND",
        "When the owl gave a late night lecture at the forest university, it was —",
        "A HOOT AND A HALF TO HEAR"
    },
    {
        4,
        {0x0F, 0x0F, 0x17, 0x1A, 0x00, 0x00},
        "WINTER CASTLE TREASURE FUTURE",
        "The baker rolled out hundred pastry crusts by hand and was —",
        "IN A CRUST WE TRUST"
    },
    {
        5,
        {0x1B, 0x0F, 0x1B, 0x33, 0x1C, 0x00},
        "VAMPIRE WHISTLE LEADER TREATY SKILL",
        "When the dog found his buried bone in the backyard, he was —",
        "\"PAW\"-SITIVELY THRILLED"
    },
    {
        6,
        {0x0F, 0x0F, 0x0F, 0x0F, 0x17, 0x02},
        "ALPHABET LEOPARD SEAFOOD DIRECT NOTICE STICK",
        "The teacher loved teaching geometry because the proofs were —",
        "ALL SHAPED TO PERFECTION"
    },
    {
        6,
        {0x0F, 0x0F, 0x0F, 0x0F, 0x3C, 0x04},
        "EXTRA WEATHER CHIMNEY ENGINE SKETCH RIDDLE",
        "When the electric car plugged into the rapid charger, it was —",
        "CHARGED WITH EXCITEMENT"
    },
    {
        5,
        {0x0F, 0x1D, 0x0F, 0x1D, 0x02, 0x00},
        "SERVE ALPHABET BOTTLE SWEET LEGAL",
        "The shoe designer created leather sneakers with gold lace and was —",
        "A STEP ABOVE THE REST"
    },
    {
        5,
        {0x1D, 0x1D, 0x17, 0x17, 0x15, 0x00},
        "FARMER PICTURE NOTICE TENDER TUNER",
        "When the cat curled up on the sunny window sill, she was in —",
        "\"PURR\"-FECT CONTENTMENT"
    },
    {
        4,
        {0x0F, 0x17, 0x1B, 0x36, 0x00, 0x00},
        "WEIGHT WHISTLE FLIGHT MOTION",
        "The river guide paddled through the rapid white water and said —",
        "GOING WITH THE FLOW"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x0F, 0x1B, 0x00},
        "RAINBOW WINDFALL ROBOT BELLY STUDY",
        "When the jeweler cut the fifty carat diamond into facets, it was —",
        "BRILLIANT BEYOND WORDS"
    },
    {
        5,
        {0x0F, 0x1B, 0x0F, 0x3A, 0x04, 0x00},
        "RABBIT MORNING GOING FLIGHT FUDGE",
        "The farmer planted rows of giant sunflowers and said they were —",
        "BLOOMING AND BRIGHT"
    },
    {
        4,
        {0x0F, 0x0F, 0x3A, 0x33, 0x00, 0x00},
        "BLANKET STRIKE JOCKEY GENTLE",
        "When the actor nailed the difficult monologue on Broadway, he —",
        "BROKE A LEG IN STYLE"
    },
    {
        5,
        {0x1E, 0x0F, 0x1B, 0x47, 0x06, 0x00},
        "BLANKET KNIGHT PICTURE TREASURE PIECE",
        "The mechanic tuned the sports car engine until it was —",
        "PURRING LIKE A KITTEN"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x1E, 0x48, 0x00},
        "WIZARD ZEBRA USAGE SCENT FORTUNE",
        "When the bee hive produced ten gallons of clover honey, it was —",
        "CREATING A SWEET BUZZ"
    },
    {
        4,
        {0x0F, 0x0F, 0x66, 0x26, 0x00, 0x00},
        "SILVER FINGER TREASURE NEEDLE",
        "The bookkeeper balanced thirty accounts to the penny and said —",
        "FIGURES NEVER LIE"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x1B, 0x14, 0x00},
        "YELLOW WINDOW TWELVE ROCKET SYMBOL",
        "When the clock maker repaired the tower clock, the town council said —",
        "TIMELY WORK WELL DONE"
    },
    {
        5,
        {0x0F, 0x1E, 0x39, 0x39, 0x0C, 0x00},
        "GIRAFFE PENGUIN TRAFFIC CABINET ACUTE",
        "The gardener trimmed the hedge into a green dinosaur and was —",
        "CUTTING A FINE FIGURE"
    },
    {
        5,
        {0x1B, 0x0F, 0x0F, 0x0F, 0x2D, 0x00},
        "FROZEN CABINET CHARGE GENTLE SPHERE",
        "When the sailboat rounded the windy cape, the crew reported —",
        "CATCHING A FRESH BREEZE"
    },
    {
        5,
        {0x0F, 0x0F, 0x3C, 0x17, 0x08, 0x00},
        "WHISPER PURPLE VILLAGE NEEDLE URBAN",
        "The potter spun the wet clay into an elegant vase and said —",
        "SHAPING UP REAL WELL"
    },
    {
        4,
        {0x0F, 0x17, 0x26, 0x10, 0x00, 0x00},
        "WHISPER MONKEY JOURNEY ENEMY",
        "When the magician vanished from the locked trunk, the crowd said —",
        "NOW YOU SEE HIM"
    },
    {
        4,
        {0x0F, 0x0F, 0x0F, 0x0F, 0x00, 0x00},
        "GATHER REGION THORN TENTH",
        "The archer hit the center bullseye three times in a row for —",
        "RIGHT ON THE TARGET"
    },
    {
        5,
        {0x1B, 0x1D, 0x0F, 0x0F, 0x1A, 0x00},
        "ALPHABET CABINET SOLDIER REFER STAIR",
        "When the weaver finished the silk tapestry on the loom, it had —",
        "THREADS OF BRILLIANCE"
    },
    {
        4,
        {0x0F, 0x1B, 0x17, 0x52, 0x00, 0x00},
        "ACTIVE TRAVEL STOCK HOLIDAY",
        "The ice hockey team won the championship game on home ice and —",
        "SKATED TO VICTORY"
    },
    {
        5,
        {0x0F, 0x0F, 0x17, 0x1D, 0x33, 0x00},
        "TARGET REGION THEATER SPHERE SEAFOOD",
        "When the chef baked the golden soufflé without it deflating, it —",
        "ROSE TO GREATER HEIGHTS"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x1B, 0x02, 0x00},
        "TRAVEL SOLDIER CRYSTAL EASEL RIVAL",
        "The astronomer discovered a new comet in the night sky and said —",
        "A STELLAR DISCOVERY"
    },
    {
        5,
        {0x0F, 0x0F, 0x0F, 0x17, 0x1B, 0x00},
        "WHISTLE KITTEN HORIZON SOLDIER ENTER",
        "When the blacksmith forged the iron horseshoe, he told his apprentice —",
        "STRIKE WHILE IRON IS HOT"
    },
};

#endif // JUMBLE_DATASET_H
