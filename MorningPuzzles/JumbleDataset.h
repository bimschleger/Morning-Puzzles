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
        {0x19, 0x13, 0x15, 0x14, 0x00, 0x00},
        "MOVIE GUILD GHOST MIGHT",
        "Why did the coffee file a police report?",
        "IT GOT MUGGED"
    },
    {
        6,
        {0x0D, 0x0D, 0x0B, 0x0E, 0x0D, 0x0B},
        "JOINT GIVEN WOUND SHADE TRUTH STRIP",
        "What did the ocean say to the sailboat?",
        "NOTHING IT JUST WAVED"
    },
    {
        6,
        {0x0D, 0x13, 0x05, 0x1A, 0x07, 0x0B},
        "LEAVE CHEAP YEAR STORY EASEL SEDAN",
        "Why do we tell actors to 'break a leg'?",
        "EVERY PLAY HAS A CAST"
    },
    {
        4,
        {0x0D, 0x03, 0x07, 0x0A, 0x00, 0x00},
        "DRAIN NOON ONSET DEAR",
        "What do you call a sleeping dinosaur?",
        "A \"DINO\"-SNORE"
    },
    {
        4,
        {0x0B, 0x0B, 0x09, 0x02, 0x00, 0x00},
        "STAMP PANIC ARENA RAPID",
        "What do you call a fake noodle?",
        "AN \"IM-PASTA\""
    },
    {
        5,
        {0x07, 0x0E, 0x15, 0x16, 0x08, 0x00},
        "SWEAR AWAIT THIRD WORST WRATH",
        "Why did the bicycle fall over?",
        "IT WAS \"TWO-TIRED\""
    },
    {
        4,
        {0x16, 0x0B, 0x15, 0x09, 0x00, 0x00},
        "THOSE HAVEN CYCLE SCENE",
        "What do you call cheese that isn't yours?",
        "\"NACHO\" CHEESE"
    },
    {
        5,
        {0x1A, 0x16, 0x0C, 0x0D, 0x06, 0x00},
        "SHEER SLOPE SAIL STATE MATCH",
        "Why couldn't the pony sing in the choir?",
        "A LITTLE HOARSE"
    },
    {
        5,
        {0x19, 0x1A, 0x05, 0x15, 0x07, 0x00},
        "GROVE UNION STIR TRAIT ARISE",
        "What do you call an alligator in a vest?",
        "AN \"IN-VEST\"-IGATOR"
    },
    {
        4,
        {0x13, 0x1C, 0x07, 0x08, 0x00, 0x00},
        "BREED ROGUE FENCE WIDOW",
        "What do you call a cow with no legs?",
        "GROUND BEEF"
    },
    {
        5,
        {0x19, 0x13, 0x1A, 0x15, 0x0A, 0x00},
        "GROWN PIANO ELITE LANCE HEAL",
        "Why did the banana go to the doctor?",
        "NOT \"PEELING\" WELL"
    },
    {
        4,
        {0x07, 0x0A, 0x13, 0x0D, 0x00, 0x00},
        "WRIST STEM DELTA STAFF",
        "Why did the picture go to jail?",
        "IT WAS FRAMED"
    },
    {
        4,
        {0x0D, 0x0E, 0x16, 0x02, 0x00, 0x00},
        "BLAME IMAGE FERRY BUILD",
        "What do you call a bear with no teeth?",
        "A GUMMY BEAR"
    },
    {
        4,
        {0x09, 0x19, 0x07, 0x0C, 0x00, 0x00},
        "BOOM HONEY CANDY TROOP",
        "Why do bees have sticky hair?",
        "A HONEYCOMB"
    },
    {
        4,
        {0x15, 0x0B, 0x1C, 0x1C, 0x00, 0x00},
        "TIMER FLAME JUICY ROUTE",
        "Why did the cookie go to the hospital?",
        "IT FELT CRUMMY"
    },
    {
        4,
        {0x0B, 0x0D, 0x03, 0x09, 0x00, 0x00},
        "AWAIT MONTH NAME OTHER",
        "What do you call a pile of kittens?",
        "A \"MEOW\"-NTAIN"
    },
    {
        5,
        {0x13, 0x1A, 0x0E, 0x16, 0x0E, 0x00},
        "MANOR FORTH SCENE GREAT STEEP",
        "What did one wall say to the other?",
        "MEET AT THE CORNER"
    },
    {
        4,
        {0x0D, 0x16, 0x13, 0x08, 0x00, 0x00},
        "BLAZE FLUID LOVER BONE",
        "What do you call a sleeping bull?",
        "A \"BULL\"-DOZER"
    },
    {
        4,
        {0x16, 0x15, 0x16, 0x0C, 0x00, 0x00},
        "FEVER WHITE SPORT WEST",
        "Why was the broom late for work?",
        "IT OVER-SWEPT"
    },
    {
        6,
        {0x19, 0x1A, 0x1A, 0x07, 0x07, 0x0E},
        "STRAW AGENT RIGID SEDAN SALON CRASH",
        "Why did the tomato blush?",
        "IT SAW SALAD DRESSING"
    },
    {
        4,
        {0x0D, 0x0A, 0x04, 0x02, 0x00, 0x00},
        "MAKER MANY MANGO LOCAL",
        "What kind of key opens a banana?",
        "A \"MON-KEY\""
    },
    {
        4,
        {0x15, 0x1A, 0x15, 0x0A, 0x00, 0x00},
        "PLANE THORN ISLET ARMED",
        "What do you call an elephant that doesn't matter?",
        "\"IRRELEPHANT\""
    },
    {
        4,
        {0x0E, 0x06, 0x0C, 0x1C, 0x00, 0x00},
        "CHAIN SOLO TONE STONE",
        "Why did the golfer bring extra socks?",
        "A HOLE IN ONE"
    },
    {
        4,
        {0x07, 0x07, 0x16, 0x02, 0x00, 0x00},
        "SHARP OLIVE CRUEL FILL",
        "What do you call a funny mountain?",
        "\"HILL\"-ARIOUS"
    },
    {
        4,
        {0x1A, 0x16, 0x14, 0x02, 0x00, 0x00},
        "THROW MAGIC MEDIA STRAW",
        "What kind of dog tells time?",
        "A \"WATCH\" DOG"
    },
    {
        6,
        {0x07, 0x0E, 0x19, 0x0E, 0x13, 0x05},
        "PLEAD APRIL ADOPT SHADE OFTEN SQUAD",
        "Why was the belt arrested?",
        "HELD UP PAIR OF PANTS"
    },
    {
        4,
        {0x1A, 0x07, 0x01, 0x08, 0x00, 0x00},
        "BROWN BOARD ALIKE AUDIO",
        "What bow can never be tied?",
        "A RAINBOW"
    },
    {
        5,
        {0x0D, 0x07, 0x05, 0x1A, 0x0C, 0x00},
        "DEPOT SHEET TONE CAUSE GROOM",
        "What kind of shoes do frogs wear?",
        "\"OPEN-TOAD\" SHOES"
    },
    {
        5,
        {0x1C, 0x05, 0x0D, 0x13, 0x1A, 0x00},
        "PIVOT TIME GHOST HOUSE MOVIE",
        "What do cows do on date night?",
        "GO TO THE MOOVIES"
    },
    {
        4,
        {0x09, 0x03, 0x04, 0x02, 0x00, 0x00},
        "TASK SCARE STAIR TIME",
        "What do you call a boomerang that doesn't return?",
        "A STICK"
    },
    {
        4,
        {0x07, 0x0E, 0x19, 0x13, 0x00, 0x00},
        "QUICK SWEAR SHARK ACUTE",
        "Why did the duck get sent to the principal?",
        "A WISE \"QUACKER\""
    },
    {
        4,
        {0x0D, 0x0C, 0x0C, 0x01, 0x00, 0x00},
        "SUPER HUNT VENUE EQUIP",
        "What kind of music do planets listen to?",
        "\"NEP-TUNES\""
    },
    {
        4,
        {0x13, 0x06, 0x04, 0x04, 0x00, 0x00},
        "OPERA STEAM RATE FEAST",
        "What starts with T, ends with T, and has T inside?",
        "A TEAPOT"
    },
    {
        5,
        {0x0B, 0x0B, 0x0E, 0x03, 0x05, 0x00},
        "FATAL CLOTH WRONG ROOF ORAL",
        "Why did the tree go to the dentist?",
        "FOR A ROOT CANAL"
    },
    {
        6,
        {0x19, 0x15, 0x0B, 0x15, 0x1A, 0x18},
        "HEDGE SOLID TOKEN OUTER DEPOT ORBIT",
        "Why did the chicken cross the playground?",
        "TO GET TO OTHER SLIDE"
    },
    {
        5,
        {0x1A, 0x07, 0x1A, 0x0B, 0x0E, 0x00},
        "SWEEP SWIFT FLOOD FORTH ANNEX",
        "Why was the computer cold?",
        "LEFT WINDOWS OPEN"
    },
    {
        4,
        {0x1A, 0x0B, 0x02, 0x04, 0x00, 0x00},
        "NOTCH ACUTE BLUE TREND",
        "What kind of candy never arrives on time?",
        "\"CHOC\"-LATE"
    },
    {
        4,
        {0x13, 0x16, 0x0E, 0x14, 0x00, 0x00},
        "AWAKE CLOCK MANGO RISKY",
        "What kind of car does an egg drive?",
        "A \"YOLK\"-SWAGEN"
    },
    {
        4,
        {0x1C, 0x19, 0x05, 0x10, 0x00, 0x00},
        "SHOCK POLAR PLOT EARTH",
        "What do you call a pig that knows karate?",
        "A PORK CHOP"
    },
    {
        6,
        {0x0E, 0x19, 0x1A, 0x0C, 0x15, 0x0E},
        "TOWER EAGLE PLANT RAIL TRUST RATIO",
        "What did the grape say when stepped on?",
        "LET OUT A LITTLE \"WINE\""
    },
    {
        6,
        {0x0E, 0x0B, 0x16, 0x0D, 0x05, 0x12},
        "NIGHT HARSH TOOTH CHEER TENT CRUST",
        "Why did the music teacher need a ladder?",
        "TO REACH HIGH NOTES"
    },
    {
        4,
        {0x16, 0x16, 0x06, 0x04, 0x00, 0x00},
        "TREND ENEMY POET STEAK",
        "What do you call a deer with no eyes?",
        "\"NO-EYE\" DEER"
    },
    {
        4,
        {0x1C, 0x07, 0x02, 0x04, 0x00, 0x00},
        "GRAPE GUILD INNER BUNCH",
        "What kind of bird can write?",
        "A \"PEN\"-GUIN"
    },
    {
        4,
        {0x0D, 0x05, 0x02, 0x02, 0x00, 0x00},
        "BROAD BROWN BOOK BOLD",
        "What do you call a ghost's mistake?",
        "A \"BOO-BOO\""
    },
    {
        5,
        {0x1A, 0x0B, 0x07, 0x0A, 0x09, 0x00},
        "SHEEP DATED DECAY KEEN SUPER",
        "Why did the astronaut break up with his girlfriend?",
        "HE NEEDED SPACE"
    },
    {
        5,
        {0x0D, 0x0D, 0x07, 0x1A, 0x0D, 0x00},
        "CABLE BLADE RADAR POLAR APART",
        "What do you call a magic dog?",
        "\"LABRA-CADABRA\"-DOR"
    },
    {
        4,
        {0x07, 0x19, 0x1C, 0x0E, 0x00, 0x00},
        "BLEND FRONT COURT QUOTA",
        "Why did the candle quit its job?",
        "FELT BURNT OUT"
    },
    {
        6,
        {0x19, 0x13, 0x1A, 0x16, 0x1C, 0x04},
        "HEDGE THOSE SHADE HOUND SPEED PUNCH",
        "Why did the baker go to the bank?",
        "HE NEEDED THE DOUGH"
    },
    {
        4,
        {0x19, 0x0E, 0x0E, 0x05, 0x00, 0x00},
        "JOINT SWAMP VISIT AWAKE",
        "Why was the strawberry sad?",
        "IT WAS IN A JAM"
    },
    {
        4,
        {0x07, 0x0E, 0x07, 0x16, 0x00, 0x00},
        "COUCH MATCH ANNEX STAIN",
        "What kind of insect is good at math?",
        "AN \"ACCOUNT-ANT\""
    },
    {
        4,
        {0x15, 0x05, 0x15, 0x05, 0x00, 0x00},
        "BROKE HILL REFER INLET",
        "Why did the duck buy lipstick?",
        "FOR HER \"BILL\""
    },
    {
        4,
        {0x13, 0x0E, 0x1A, 0x04, 0x00, 0x00},
        "SHAKE BURST QUOTA DEAR",
        "What do you call a dinosaur with a great vocabulary?",
        "A \"THES-AURUS\""
    },
    {
        4,
        {0x13, 0x1A, 0x06, 0x1A, 0x00, 0x00},
        "AWARE FLASH PURE WATER",
        "Why was the king only one foot tall?",
        "HE WAS A RULER"
    },
    {
        5,
        {0x1C, 0x13, 0x05, 0x19, 0x09, 0x00},
        "TULIP SPORT PINT GRAIN UNION",
        "Why did the banana wear shoes?",
        "NOT SLIPPING UP"
    },
    {
        4,
        {0x0D, 0x13, 0x13, 0x0E, 0x00, 0x00},
        "JOKER BASIC ALBUM CRUST",
        "What do you call a sleeping woodcutter?",
        "A \"SLUMBER\"-JACK"
    },
    {
        5,
        {0x19, 0x1C, 0x1C, 0x09, 0x12, 0x00},
        "DEATH CRAFT VOICE STAIN BONUS",
        "What do you call a fish wearing a bowtie?",
        "\"SO-FISH\"-TICATED"
    },
    {
        5,
        {0x07, 0x05, 0x19, 0x0E, 0x12, 0x00},
        "AWAIT GOAT DIRTY STOOL RIGHT",
        "Why did the frog park illegally?",
        "IT GOT \"TOAD\" AWAY"
    },
    {
        5,
        {0x0E, 0x07, 0x0B, 0x13, 0x16, 0x00},
        "GROWL TABLE MORAL ELECT SENSE",
        "Why did the melon jump into the lake?",
        "TO BE A WATER-MELON"
    },
    {
        4,
        {0x16, 0x11, 0x01, 0x02, 0x00, 0x00},
        "ALTAR EAGLE AREA GAME",
        "What kind of tea is hard to swallow?",
        "\"REAL-TEA\""
    },
    {
        4,
        {0x1C, 0x15, 0x13, 0x15, 0x00, 0x00},
        "DIZZY BRIDE DRAMA APRIL",
        "What do you call a bear caught in the rain?",
        "A \"DRIZZLY\" BEAR"
    },
    {
        5,
        {0x19, 0x15, 0x07, 0x1C, 0x0D, 0x00},
        "PLANT PASTE GRAND FINAL UNITY",
        "What do you call a turtle taking photos?",
        "A \"SNAPPING\" TURTLE"
    },
    {
        4,
        {0x19, 0x07, 0x13, 0x03, 0x00, 0x00},
        "MAPLE PHOTO SALAD OAKS",
        "What kind of dog loves bubble baths?",
        "A \"SHAM-POODLE\""
    },
    {
        6,
        {0x16, 0x0D, 0x0B, 0x07, 0x0B, 0x15},
        "ARROW WHITE MOUTH SHEEP FATAL STARE",
        "Why did the cookie cry?",
        "ITS MOTHER WAS A WAFER"
    },
    {
        4,
        {0x19, 0x1C, 0x1C, 0x12, 0x00, 0x00},
        "METER CIDER DISCO TEMPO",
        "What do you call an apology written in dots and dashes?",
        "\"RE-MORSE\" CODE"
    },
    {
        5,
        {0x1A, 0x0E, 0x19, 0x16, 0x1C, 0x00},
        "HEDGE WHILE DEATH PEDAL SHAFT",
        "Why did the candle visit the doctor?",
        "FELT \"LIGHT\"-HEADED"
    },
    {
        5,
        {0x16, 0x0D, 0x0B, 0x07, 0x0E, 0x00},
        "STEEP SCOPE SINCE LEAFY FATAL",
        "Why did the orange go to court?",
        "TO \"APPEAL\" ITS CASE"
    },
    {
        4,
        {0x05, 0x11, 0x0A, 0x13, 0x00, 0x00},
        "BUSY BADLY FUDGE UNION",
        "What do you call a rabbit with fleas?",
        "\"BUGS\" BUNNY"
    },
    {
        4,
        {0x0D, 0x1A, 0x0E, 0x04, 0x00, 0x00},
        "HUMAN SPEND ROAST BOARD",
        "What do you call a clean pig?",
        "HAM AND SOAP"
    },
    {
        4,
        {0x19, 0x19, 0x14, 0x04, 0x00, 0x00},
        "PLUME APPLE ROAST FORTH",
        "What kind of tree loves high fives?",
        "A PALM TREE"
    },
    {
        4,
        {0x16, 0x07, 0x05, 0x0A, 0x00, 0x00},
        "WOMAN COAST SAIL PANIC",
        "What do you call a cow playing an instrument?",
        "A \"MOO\"-SICIAN"
    },
    {
        5,
        {0x1C, 0x1C, 0x06, 0x1C, 0x11, 0x00},
        "DEATH SLICE MILL GRILL LEAST",
        "What do you call a tiny pepper in winter?",
        "A LITTLE \"CHILLI\""
    },
    {
        5,
        {0x07, 0x07, 0x1C, 0x07, 0x19, 0x00},
        "POLAR AGENT HOUND TODAY ESSAY",
        "Why did the violin take a bow?",
        "PLAYED A GOOD TUNE"
    },
    {
        4,
        {0x0C, 0x09, 0x1C, 0x08, 0x00, 0x00},
        "RAGE LATE SKILL RELAX",
        "What do you call an eagle that tells bad jokes?",
        "\"ILL-EAGLE\""
    },
    {
        5,
        {0x13, 0x19, 0x13, 0x1C, 0x02, 0x00},
        "SWEAT WORLD BRAVE STALE DISCO",
        "Why was the loaf of bread so polite?",
        "IT WAS WELL-BRED"
    },
    {
        4,
        {0x0D, 0x0E, 0x13, 0x09, 0x00, 0x00},
        "BRIEF PLANT ALTER ALTAR",
        "What do you call a dancing sheep?",
        "A \"BAA\"-LLERINA"
    },
    {
        4,
        {0x15, 0x0D, 0x09, 0x07, 0x00, 0x00},
        "BRICK EXACT CART TRACK",
        "What do you call a noisy insect playing sports?",
        "A CRICKET BAT"
    },
    {
        5,
        {0x0D, 0x07, 0x07, 0x07, 0x0D, 0x00},
        "BRAIN BRING MINOR CIGAR CLOTH",
        "What do you call a funny frog on stage?",
        "A \"RIBBIT\"-ING COMIC"
    },
    {
        6,
        {0x13, 0x0B, 0x0D, 0x13, 0x0E, 0x02},
        "SWEAR BUDDY MONEY DECAY GREET CASH",
        "Why did the calendar look worried?",
        "DAYS WERE NUMBERED"
    },
    {
        4,
        {0x07, 0x0E, 0x0E, 0x09, 0x00, 0x00},
        "CLEAN STILL FLOAT TINT",
        "What do you call a cold horse in the pasture?",
        "A LITTLE \"COLT\""
    },
    {
        4,
        {0x0D, 0x06, 0x16, 0x1C, 0x00, 0x00},
        "BRASS SIGN DRAIN GUESS",
        "What do you call a singing fish?",
        "A BASS SINGER"
    },
    {
        4,
        {0x0D, 0x0C, 0x1C, 0x05, 0x00, 0x00},
        "ADMIT COPY RANCH CIDER",
        "What do you call a sweet monkey?",
        "\"CHIMP\" CANDY"
    },
    {
        5,
        {0x07, 0x1A, 0x0D, 0x03, 0x05, 0x00},
        "WHEEL BREAK LABEL NODE STEER",
        "Why did the shoe visit the hospital?",
        "HEEL WAS BROKEN"
    },
    {
        4,
        {0x13, 0x15, 0x0B, 0x04, 0x00, 0x00},
        "IDEAL DRAMA ENJOY POND",
        "What do you call a lion with flowers?",
        "A \"DANDE-LION\""
    },
    {
        5,
        {0x1A, 0x07, 0x19, 0x0E, 0x0C, 0x00},
        "OPERA DRAIN ASIDE PENNY SPOIL",
        "Why did the cloud cry all morning?",
        "RAINED ON PARADE"
    },
    {
        4,
        {0x09, 0x16, 0x18, 0x08, 0x00, 0x00},
        "BENT UNCLE DEVIL THIEF",
        "What did the zero say to the eight?",
        "\"NICE BELT\""
    },
    {
        5,
        {0x0D, 0x0E, 0x16, 0x16, 0x0B, 0x00},
        "ROBOT POEMS EMPTY PLANT SOUND",
        "Why was the math book sad?",
        "TOO MANY PROBLEMS"
    },
    {
        4,
        {0x0D, 0x16, 0x06, 0x09, 0x00, 0x00},
        "MERCY MAPLE SAFE FORUM",
        "What do you call a sleeping pie?",
        "A \"CREAM PUFF\""
    },
    {
        5,
        {0x1A, 0x15, 0x0B, 0x07, 0x0D, 0x00},
        "ALLOW FINAL STIFF FAITH ABUSE",
        "Why did the stadium get so cool?",
        "IT WAS FULL OF FANS"
    },
    {
        4,
        {0x0E, 0x0C, 0x04, 0x02, 0x00, 0x00},
        "TABLE OFTEN NOTE ROCKY",
        "What has a neck but no head?",
        "A BOTTLE"
    },
    {
        4,
        {0x03, 0x01, 0x01, 0x04, 0x00, 0x00},
        "ABOUT MONTH COLT STORM",
        "What has teeth but cannot bite?",
        "A COMB"
    },
    {
        6,
        {0x0B, 0x1A, 0x07, 0x0E, 0x15, 0x06},
        "CHILI KNIFE SNAKE LINER OLIVE FOOT",
        "Why did the golfer wear two pairs of pants?",
        "IN CASE OF HOLE IN ONE"
    },
    {
        4,
        {0x1C, 0x15, 0x13, 0x0A, 0x00, 0x00},
        "TRUNK BEGIN UNITY GULF",
        "What do you call a rabbit that does martial arts?",
        "\"KUNG FU\" BUNNY"
    },
    {
        5,
        {0x0E, 0x0D, 0x0D, 0x0D, 0x0E, 0x00},
        "CURVE DANCE CREAM ALONE FERRY",
        "What do you call a sleeping police car?",
        "AN UNDER-\"COVER\" CAR"
    },
    {
        6,
        {0x1A, 0x07, 0x0E, 0x15, 0x1C, 0x14},
        "POEMS PRIDE AGENT TENTH TODAY MOUNT",
        "What did the pencil sharpener say to the pencil?",
        "STOP TURNING MY HEAD"
    },
    {
        5,
        {0x0D, 0x1A, 0x07, 0x0E, 0x1A, 0x00},
        "JOINT CRAFT COAST OUTER AUDIO",
        "Why did the orange stop rolling down the hill?",
        "IT RAN OUT OF JUICE"
    },
    {
        4,
        {0x1A, 0x13, 0x0E, 0x0A, 0x00, 0x00},
        "TWIST CHEEK TIMER HINT",
        "What did the stamp say to the letter?",
        "\"STICK WITH ME\""
    },
    {
        5,
        {0x1A, 0x0B, 0x19, 0x15, 0x15, 0x00},
        "SWEEP STUFF SWIFT FLEET OLIVE",
        "Why did the broom jump for joy?",
        "SWEPT OFF ITS FEET"
    },
    {
        4,
        {0x16, 0x0A, 0x02, 0x08, 0x00, 0x00},
        "THIRD LION LOOSE VAPOR",
        "What do you call an owl magician?",
        "\"HOO-DINI\""
    },
    {
        5,
        {0x07, 0x07, 0x07, 0x13, 0x07, 0x00},
        "BOOTH DEPOT GHOST STORY TOTAL",
        "Why did the skeleton cross the road?",
        "TO GET TO BODY SHOP"
    },
    {
        5,
        {0x16, 0x16, 0x0E, 0x19, 0x04, 0x00},
        "ENJOY DEPOT SOLAR LOYAL CARRY",
        "What do you call a happy farmer in spring?",
        "A JOLLY PLANTER"
    },
    {
        4,
        {0x0F, 0x26, 0x11, 0x20, 0x00, 0x00},
        "SWITCH REMOVE SOLVE CHIMES",
        "When the tailor was asked how business was going, he said —",
        "\"SEW\" IT SEEMS"
    },
    {
        4,
        {0x1D, 0x32, 0x01, 0x08, 0x00, 0x00},
        "EXPERT MONKEY NURSE DIVER",
        "The optician gave his patient a discount, which was a real —",
        "EYE OPENER"
    },
    {
        4,
        {0x07, 0x3A, 0x16, 0x10, 0x00, 0x00},
        "SHELL FOSSIL HOTEL MINUS",
        "When the cobbler lost his favorite tools, he felt like he —",
        "LOST HIS \"SOLE\""
    },
    {
        4,
        {0x33, 0x07, 0x24, 0x01, 0x00, 0x00},
        "CHANCE ALERT MARKET AVENUE",
        "The fisherman was very popular with the town because he was —",
        "A REEL CATCH"
    },
    {
        4,
        {0x1D, 0x39, 0x31, 0x09, 0x00, 0x00},
        "TABLET HAMLET AROUND IGNITE",
        "When the butcher backed into the slicer, he got —",
        "A LITTLE BEHIND"
    },
    {
        4,
        {0x2E, 0x0E, 0x27, 0x20, 0x00, 0x00},
        "MEADOW WIDOW TINSEL GARDEN",
        "The carpenter finished building the table and proudly said —",
        "NAILED IT DOWN"
    },
    {
        4,
        {0x16, 0x1C, 0x22, 0x02, 0x00, 0x00},
        "THINK BRAND HERMIT CRUEL",
        "When the electricity failed during class, the students were —",
        "IN THE DARK"
    },
    {
        4,
        {0x2E, 0x08, 0x10, 0x08, 0x00, 0x00},
        "ESCORT TABLET FEAST TOTAL",
        "The pirate had trouble learning the alphabet because he was —",
        "LOST AT \"C\""
    },
    {
        4,
        {0x2B, 0x1E, 0x1A, 0x32, 0x00, 0x00},
        "GLIDER ENOUGH CHILI COUSIN",
        "When the baker won the lottery, his friends knew he was —",
        "ROLLING IN DOUGH"
    },
    {
        4,
        {0x0F, 0x2B, 0x38, 0x02, 0x00, 0x00},
        "WANDER HORNET GLIDER FIXED",
        "The plumber had to retire early because all his plans went —",
        "DOWN THE DRAIN"
    },
    {
        4,
        {0x2E, 0x36, 0x36, 0x2B, 0x00, 0x00},
        "SPIRIT AGENDA RESIGN HIKING",
        "When the gardener was praised for his flowers, he said —",
        "DIGGING THE PRAISE"
    },
    {
        4,
        {0x36, 0x36, 0x15, 0x14, 0x00, 0x00},
        "DEVICE REMAIN AMONG INSIDE",
        "The watchmaker was asked for the time, and he replied —",
        "GIVE ME A SECOND"
    },
    {
        4,
        {0x1B, 0x0E, 0x06, 0x04, 0x00, 0x00},
        "SOMBER BISHOP AFFORD BRANCH",
        "When the baseball player struck out, his coach told him —",
        "OFF HIS BASE"
    },
    {
        4,
        {0x35, 0x07, 0x01, 0x10, 0x00, 0x00},
        "OCTAVE CABIN UPWARD OPERA",
        "The barber was thrilled with his successful shop because it was —",
        "A CUT ABOVE"
    },
    {
        4,
        {0x1A, 0x1E, 0x15, 0x2C, 0x00, 0x00},
        "SHOCK MOBILE FEAST REASON",
        "When the musician fell through the floor, he was —",
        "FLAT ON HIS BACK"
    },
    {
        4,
        {0x1B, 0x0D, 0x25, 0x20, 0x00, 0x00},
        "TORQUE STARE STEREO FLOWER",
        "The math teacher went to the farm looking for —",
        "SQUARE ROOTS"
    },
    {
        4,
        {0x3C, 0x2E, 0x19, 0x07, 0x00, 0x00},
        "ENOUGH MOTHER DEPOT OFFICE",
        "When the chef seasoned the soup, he told the waiter —",
        "FOOD FOR THOUGHT"
    },
    {
        4,
        {0x2E, 0x1C, 0x05, 0x0C, 0x00, 0x00},
        "LAPTOP SOUTH CLOSET GROOVE",
        "The lazy kangaroo spent all afternoon being a —",
        "\"POUCH\" POTATO"
    },
    {
        4,
        {0x27, 0x3A, 0x1A, 0x07, 0x00, 0x00},
        "FELLOW PHRASE CLASH SHINE",
        "Why did the crab never share his lunch with the starfish?",
        "HE WAS \"SHELL-FISH\""
    },
    {
        4,
        {0x1D, 0x0D, 0x0F, 0x3C, 0x00, 0x00},
        "VIOLET NIGHT ENGINE CREDIT",
        "When the tightrope walker lost his footing, he was —",
        "LIVING ON THE EDGE"
    },
    {
        4,
        {0x1C, 0x13, 0x0B, 0x02, 0x00, 0x00},
        "SHAPE ELITE STONE WORSE",
        "The pilot didn't want to argue about the flight plan because it was —",
        "PLANE TO SEE"
    },
    {
        5,
        {0x35, 0x0D, 0x33, 0x33, 0x09, 0x00},
        "CUSTOM PLUME PLENTY DEGREE TRULY",
        "When the lumberjack couldn't answer the riddle, he was —",
        "COMPLETELY STUMPED"
    },
    {
        5,
        {0x2B, 0x07, 0x33, 0x2B, 0x16, 0x00},
        "GOLDEN THING FOURTH ANNUAL PATROL",
        "The dentist and the manicurist fell in love and —",
        "FOUGHT TOOTH AND NAIL"
    },
    {
        4,
        {0x1D, 0x1E, 0x03, 0x10, 0x00, 0x00},
        "TRAVEL GLANCE SERVE HATRED",
        "When the skunk couldn't pay the bill, he told the waiter to —",
        "LEAVE A \"SCENT\""
    },
    {
        5,
        {0x3A, 0x2B, 0x3C, 0x19, 0x11, 0x00},
        "SOCKET RADISH MODEST CLIFF COPPER",
        "The clock was sent to the principal's office because it —",
        "TICKED OFF TEACHERS"
    },
    {
        4,
        {0x2B, 0x04, 0x02, 0x04, 0x00, 0x00},
        "MAGPIE ANGRY GRAND BEACH",
        "When the sheep took over the farm, the neighbors called it a —",
        "\"RAM-PAGE\""
    },
    {
        4,
        {0x2B, 0x07, 0x0F, 0x0C, 0x00, 0x00},
        "RAMBLE MOTOR ORCHID MOUNT",
        "The tree surgeon went on vacation because he wanted to —",
        "BRANCH OUT MORE"
    },
    {
        4,
        {0x17, 0x1C, 0x04, 0x20, 0x00, 0x00},
        "BREEZE MAIDEN MONEY CHARGE",
        "When the meteorologist arrived on time, everyone said he —",
        "BREEZED IN"
    },
    {
        4,
        {0x3C, 0x36, 0x1B, 0x10, 0x00, 0x00},
        "ONWARD HIKING BALLAD CLEAN",
        "The artist didn't know what to paint next, so he was —",
        "DRAWING A BLANK"
    },
    {
        4,
        {0x0F, 0x3C, 0x1C, 0x02, 0x00, 0x00},
        "UPWARD ENGINE PUDDLE FLOAT",
        "When the snake passed the math quiz, the teacher said it was —",
        "\"ADD-ING\" UP WELL"
    },
    {
        5,
        {0x0B, 0x1D, 0x13, 0x1B, 0x1A, 0x00},
        "WINDY BEYOND TENTH DOCTOR OCEAN",
        "The ghost couldn't find a partner at the dance because he had —",
        "\"NO-BODY\" TO DANCE WITH"
    },
    {
        4,
        {0x2E, 0x1D, 0x39, 0x0F, 0x00, 0x00},
        "OXYGEN WALRUS MEDIUM INSIDE",
        "When the hotel on the beach flooded, the guests were —",
        "SWIMMING IN LUXURY"
    },
    {
        4,
        {0x35, 0x2B, 0x1B, 0x2E, 0x00, 0x00},
        "ROBUST BOUNCE THREAD SUDDEN",
        "The candle factory closed its doors because the workers were —",
        "BURNED AT BOTH ENDS"
    },
    {
        4,
        {0x1B, 0x1B, 0x19, 0x16, 0x00, 0x00},
        "BOUNCE THREAD STILL VISUAL",
        "When the banker lost his composure, his colleagues said he —",
        "LOST HIS BALANCE"
    },
    {
        4,
        {0x0F, 0x08, 0x04, 0x04, 0x00, 0x00},
        "GATHER WOODEN PROOF BROWN",
        "The dog sat by the fireplace all winter because he was —",
        "A HOT DOG"
    },
    {
        4,
        {0x33, 0x1C, 0x08, 0x04, 0x00, 0x00},
        "NARROW ALWAYS GLOBE JELLY",
        "When the quarterback gave an interview, the reporters were —",
        "BLOWN AWAY"
    },
    {
        4,
        {0x2E, 0x0F, 0x3C, 0x3A, 0x00, 0x00},
        "ANSWER BEAUTY COMEDY LEADER",
        "The detective arrested the calendar maker because his —",
        "DAYS WERE NUMBERED"
    },
    {
        4,
        {0x2E, 0x16, 0x15, 0x10, 0x00, 0x00},
        "SINGER PASTA RUSTIC SPORT",
        "When the baker's apprentice made great sourdough, he was —",
        "A RISING STAR"
    },
    {
        4,
        {0x2D, 0x1E, 0x34, 0x03, 0x00, 0x00},
        "ONWARD IGNITE RESIGN FORGET",
        "The elevator attendant had a bad day because business was —",
        "GOING DOWN FAST"
    },
    {
        4,
        {0x17, 0x13, 0x0E, 0x1A, 0x00, 0x00},
        "POODLE FLESH SHOOT FEAST",
        "When the frog took the stage, the audience gave him a —",
        "\"HOLE\" LOT OF HOPS"
    },
    {
        5,
        {0x1D, 0x3A, 0x39, 0x0B, 0x12, 0x00},
        "PASTEL QUENCH EXPAND SAINT RADIO",
        "The lawyer was delighted with his new case because it was —",
        "AN OPEN AND SHUT CASE"
    },
    {
        4,
        {0x2B, 0x2B, 0x2D, 0x16, 0x00, 0x00},
        "PERIOD REFUND FACTOR SENIOR",
        "When the cow won the ribbon at the county fair, it was —",
        "\"UDDER\" PERFECTION"
    },
    {
        4,
        {0x39, 0x0B, 0x0F, 0x0E, 0x00, 0x00},
        "DIRECT FANCY FOSSIL BOUNCE",
        "The photographer loved developing black and white pictures because they —",
        "FOCUSED ON FACTS"
    },
    {
        4,
        {0x1B, 0x2B, 0x2E, 0x32, 0x00, 0x00},
        "SPROUT HEROIC RAFTER PRAYER",
        "When the golfer made a miraculous putt, the gallery said —",
        "PAR FOR THE COURSE"
    },
    {
        4,
        {0x17, 0x2E, 0x35, 0x01, 0x00, 0x00},
        "WOODEN SKETCH BOTANY BONUS",
        "The librarian was an extraordinary detective because she —",
        "WENT BY THE BOOK"
    },
    {
        4,
        {0x1E, 0x10, 0x20, 0x08, 0x00, 0x00},
        "CAMPUS BRIGHT ASSIST BRAIN",
        "When the pig won the jackpot, all his barn friends told him to —",
        "HAM IT UP"
    },
    {
        4,
        {0x0B, 0x16, 0x26, 0x10, 0x00, 0x00},
        "WHILE PLEAD SLEEVE OFFSET",
        "The shoemaker's new assistant was learning fast and was —",
        "WELL-HEELED"
    },
    {
        4,
        {0x27, 0x39, 0x0B, 0x02, 0x00, 0x00},
        "MASCOT STRING HABIT CHERRY",
        "When the tennis star won the championship, his serve was —",
        "A SMASHING HIT"
    },
    {
        4,
        {0x0D, 0x1A, 0x33, 0x0A, 0x00, 0x00},
        "EAGER PEACH FACTOR CRAFT",
        "The battery was never worried about debt because it was —",
        "FREE OF CHARGE"
    },
    {
        4,
        {0x0D, 0x3A, 0x2D, 0x0A, 0x00, 0x00},
        "BLIND CUSTOM PULLEY SISTER",
        "When the duck paid for dinner, he told the waiter —",
        "PUT IT ON MY \"BILL\""
    },
    {
        4,
        {0x1D, 0x0B, 0x3A, 0x15, 0x00, 0x00},
        "WALRUS SHOOT STUDIO FRONT",
        "The astronomer loved his late night job because it was —",
        "OUT OF THIS WORLD"
    },
    {
        4,
        {0x27, 0x36, 0x19, 0x13, 0x00, 0x00},
        "LAWYER DEBATE GRAPE PASTA",
        "When the spider designed a new website, the client said it had —",
        "GREAT WEB APPEAL"
    },
    {
        4,
        {0x3A, 0x36, 0x1E, 0x34, 0x00, 0x00},
        "CARBON INSIDE NOTICE RETAIL",
        "The horse was happy in the barn because he was in —",
        "STABLE CONDITION"
    },
    {
        4,
        {0x1A, 0x35, 0x2D, 0x36, 0x00, 0x00},
        "CRUDE FALCON LOCUST ROCKET",
        "When the mirror fell off the wall, the owner said he —",
        "COULD NOT REFLECT"
    },
    {
        4,
        {0x2D, 0x0D, 0x39, 0x15, 0x00, 0x00},
        "GEYSER REFER OFFICE LUNAR",
        "The magician had to cancel his airplane flight because he was a —",
        "FLYING \"SORCERER\""
    },
    {
        4,
        {0x1A, 0x19, 0x17, 0x29, 0x00, 0x00},
        "CLOAK CLIMB NAPKIN ACCORD",
        "When the snowman went to the gym, he worked on his —",
        "\"AB-DOMINAL\" PACK"
    },
    {
        4,
        {0x0F, 0x1B, 0x0E, 0x04, 0x00, 0x00},
        "FARMER GARLIC FINISH FORUM",
        "The bell ringer loved his morning routine because it had a —",
        "FAMILIAR RING"
    },
    {
        4,
        {0x1B, 0x2D, 0x33, 0x10, 0x00, 0x00},
        "COOKIE GLIDER NOVELS MAJOR",
        "When the geologist proposed on one knee, he gave her a —",
        "ROCK SOLID RING"
    },
    {
        4,
        {0x0E, 0x1C, 0x21, 0x02, 0x00, 0x00},
        "SWING CHAMP GUITAR BUFFET",
        "The author loved working near the campfire because the plot was —",
        "WARMING UP"
    },
    {
        4,
        {0x0F, 0x35, 0x16, 0x02, 0x00, 0x00},
        "SQUARE KENNEL DECAY GALAXY",
        "When the pig entered the clean pen, he said it was —",
        "SQUEAKY CLEAN"
    },
    {
        4,
        {0x1B, 0x36, 0x0B, 0x0D, 0x00, 0x00},
        "NORMAL CHANCE CRAFT ALONE",
        "The diver explored the coral reef and discovered —",
        "AN OCEAN OF CHARM"
    },
    {
        4,
        {0x13, 0x35, 0x0D, 0x09, 0x00, 0x00},
        "DRIFT FINALE SHIFT INSIDE",
        "When the farmer looked over his wheat crop, he said it was —",
        "FIRST IN FIELD"
    },
    {
        4,
        {0x2E, 0x27, 0x15, 0x08, 0x00, 0x00},
        "SOCKET HARBOR SQUAD PITCH",
        "The violinist was praised by the critics because his playing —",
        "STRUCK A CHORD"
    },
    {
        4,
        {0x35, 0x15, 0x1A, 0x06, 0x00, 0x00},
        "NAPKIN GLASS FINALE CLIFF",
        "When the sailor navigated into port without a map, he said —",
        "PLAIN SAILING"
    },
    {
        4,
        {0x2B, 0x1B, 0x0E, 0x18, 0x00, 0x00},
        "PIGEON FIERCE FORUM SHORE",
        "The chef dropped his favorite pan and said it was a —",
        "RECIPE FOR RUIN"
    },
    {
        4,
        {0x2D, 0x3C, 0x36, 0x0B, 0x00, 0x00},
        "PULLEY BRIGHT PHRASE AUDIT",
        "When the bowler got three strikes in a row, he was —",
        "RIGHT UP HIS ALLEY"
    },
    {
        4,
        {0x36, 0x19, 0x13, 0x05, 0x00, 0x00},
        "PILLOW SHOCK FLAVOR FRUIT",
        "The candle was very popular because it was always —",
        "SO FULL OF WICK"
    },
    {
        4,
        {0x27, 0x0E, 0x0E, 0x22, 0x00, 0x00},
        "EDITOR STUFF FOSSIL MOMENT",
        "When the runner crossed the finish line, he said he was —",
        "OUT OF STRIDES"
    },
    {
        4,
        {0x3C, 0x36, 0x0C, 0x18, 0x00, 0x00},
        "ROCKET JOCKEY TRUST GUESS",
        "The locksmith was hired immediately because he had the —",
        "KEY TO SUCCESS"
    },
    {
        5,
        {0x39, 0x1B, 0x27, 0x35, 0x30, 0x00},
        "WRITER NAPKIN RUBBER PIGEON CHANGE",
        "When the dog barked at the oak tree, his owner said he was —",
        "BARKING UP WRONG TREE"
    },
    {
        4,
        {0x2B, 0x3A, 0x04, 0x02, 0x00, 0x00},
        "CANDLE ALWAYS SCRAP HATRED",
        "The window cleaner loved his tall job because it was —",
        "CLEAR AS DAY"
    },
    {
        4,
        {0x3A, 0x2E, 0x1D, 0x26, 0x00, 0x00},
        "HELMET CELERY FACTOR COUPLE",
        "When the sheep sheared his wool, he told his pal —",
        "\"FLEECE\" TO MEET YOU"
    },
    {
        4,
        {0x35, 0x2E, 0x0F, 0x23, 0x00, 0x00},
        "KNIGHT REGRET HORNET CARPET",
        "The train conductor loved his morning route because it was —",
        "ON THE RIGHT TRACK"
    },
    {
        4,
        {0x19, 0x1C, 0x2D, 0x02, 0x00, 0x00},
        "WHOSE MATCH AMOUNT DELTA",
        "When the bee landed on the rose, the gardener said it was —",
        "A SWEET TOUCH"
    },
    {
        4,
        {0x1D, 0x13, 0x19, 0x04, 0x00, 0x00},
        "BUTTER SHELL FAMILY CHIEF",
        "The tailor made a pair of trousers with two pockets and said —",
        "FITS THE BILL"
    },
    {
        4,
        {0x2B, 0x0F, 0x2E, 0x16, 0x00, 0x00},
        "WOODEN MUTTON ECHOES TOOTH",
        "When the pilot landed safely in the fog, his copilot said —",
        "SMOOTH TOUCH DOWN"
    },
    {
        4,
        {0x2E, 0x33, 0x26, 0x04, 0x00, 0x00},
        "RANDOM HERBAL SOURCE SERMON",
        "The baseball player was thrilled with his new contract because it was —",
        "A HOME RUN DEAL"
    },
    {
        4,
        {0x17, 0x39, 0x14, 0x04, 0x00, 0x00},
        "VISION FORMAT ALONG TUNER",
        "When the cow jumped over the moon, the calf said it was —",
        "\"MOO\"-VING FAST"
    },
    {
        4,
        {0x0F, 0x1D, 0x29, 0x02, 0x00, 0x00},
        "POLICE HUNTER FOREST FORGE",
        "The carpenter admired the antique cabinet and said it was —",
        "TOP OF THE LINE"
    },
    {
        4,
        {0x2D, 0x33, 0x12, 0x0C, 0x00, 0x00},
        "ROCKET SPIRAL CAMPUS SPOON",
        "When the ghost joined the choir, the conductor said his voice was —",
        "\"SPOOK\"-TACULAR"
    },
    {
        4,
        {0x17, 0x0E, 0x1A, 0x02, 0x00, 0x00},
        "WIDGET ENTRY ROBOT BOTANY",
        "The gardener won the giant pumpkin contest because he was —",
        "ROOTED TO WIN"
    },
    {
        4,
        {0x36, 0x19, 0x07, 0x01, 0x00, 0x00},
        "TIMBER THING THIRD OFFICE",
        "When the clock struck midnight, the night watchman said —",
        "RIGHT ON TIME"
    },
    {
        4,
        {0x1E, 0x0F, 0x15, 0x08, 0x00, 0x00},
        "SUDDEN SAFARI SENIOR PLENTY",
        "The fish stayed in deep water during the storm to remain —",
        "SAFE AND SOUND"
    },
    {
        4,
        {0x1A, 0x39, 0x3A, 0x11, 0x00, 0x00},
        "BLANK OCCUPY HAZARD FOUND",
        "When the baker made fresh croissants, his customers said —",
        "FLAKY AND PROUD"
    },
    {
        4,
        {0x1B, 0x2B, 0x0E, 0x01, 0x00, 0x00},
        "UPBEAT PREFER STYLE CRANE",
        "The cat chased the ball of yarn and declared it —",
        "\"PURR\"-FECT PLAY"
    },
    {
        4,
        {0x35, 0x2B, 0x19, 0x18, 0x00, 0x00},
        "PRAISE ONWARD CRUISE SPRING",
        "When the photographer took a snapshot of the cheetah, it was —",
        "A SNAP DECISION"
    },
    {
        4,
        {0x1D, 0x1A, 0x2E, 0x12, 0x00, 0x00},
        "SURVEY TRACT RETURN LEGEND",
        "The electrician was always excited because he loved —",
        "CURRENT EVENTS"
    },
    {
        4,
        {0x15, 0x17, 0x1B, 0x22, 0x00, 0x00},
        "WHERE TOMATO METEOR CHURCH",
        "When the bird built a sturdy nest, her mate said —",
        "HOME TWEET HOME"
    },
    {
        4,
        {0x2D, 0x2E, 0x3C, 0x18, 0x00, 0x00},
        "REGION SOCCER HONEST SHOUT",
        "The barber gave everyone a quick trim and said he was —",
        "CUTTING CORNERS"
    },
    {
        4,
        {0x27, 0x3A, 0x0F, 0x2D, 0x00, 0x00},
        "BEHIND STITCH ONLINE EVOLVE",
        "When the ice sculptor finished his swan, he was —",
        "CHILLED TO THE BONE"
    },
    {
        4,
        {0x33, 0x1B, 0x1D, 0x32, 0x00, 0x00},
        "PARROT FILTER CARROT SLOGAN",
        "The detective looked at the muddy boots and said —",
        "A CLEAR FOOTPRINT"
    },
    {
        4,
        {0x1E, 0x19, 0x16, 0x09, 0x00, 0x00},
        "SECOND STOOL CIRCUS THORN",
        "When the painter finished the wall in blue, he said —",
        "IN TRUE COLORS"
    },
    {
        4,
        {0x0B, 0x1A, 0x0A, 0x02, 0x00, 0x00},
        "SHAME FAITH ASSIST CARGO",
        "The tennis champion won the final set with —",
        "A SMASH HIT"
    },
    {
        4,
        {0x39, 0x16, 0x13, 0x04, 0x00, 0x00},
        "POSTAL CHIEF FORGE CRAYON",
        "When the frog leaped across the lily pads, he took a —",
        "LEAP OF FAITH"
    },
    {
        4,
        {0x0D, 0x3A, 0x07, 0x04, 0x00, 0x00},
        "MANGO PARADE OFFSET SWITCH",
        "The jeweler polished the emerald until it was —",
        "A GEM OF A FIND"
    },
    {
        4,
        {0x0F, 0x15, 0x17, 0x34, 0x00, 0x00},
        "SINGER HEART FORBID FLOWER",
        "When the farmer repaired his barn roof, he was —",
        "RAISING THE ROOF"
    },
    {
        4,
        {0x2E, 0x07, 0x0F, 0x0D, 0x00, 0x00},
        "GROWTH NOBLE LIGHTS NOISE",
        "The musician played his trumpet so loud he was —",
        "BLOWING HIS HORN"
    },
    {
        4,
        {0x36, 0x2B, 0x05, 0x10, 0x00, 0x00},
        "SWITCH CINEMA ONSET RUDDER",
        "When the owl gave advice in the forest, everyone said —",
        "A WISE CHOICE"
    },
    {
        4,
        {0x2E, 0x17, 0x0B, 0x14, 0x00, 0x00},
        "FORBID YOGURT FLOUR SENIOR",
        "The runner tied his sneakers tight and said he was —",
        "BOUND FOR GLORY"
    },
    {
        4,
        {0x15, 0x1B, 0x1C, 0x19, 0x00, 0x00},
        "BLEND PASTEL RESULT OBLONG",
        "When the bookbinder finished the leather volume, he said —",
        "BOUND TO PLEASE"
    },
    {
        5,
        {0x66, 0x2D, 0x4B, 0x1B, 0x31, 0x00},
        "IMPERIAL HOSTILE FEDERAL FORECAST CANVAS",
        "When the optometrist fell into the lens grinder, he made —",
        "A SPECTACLE OF HIMSELF"
    },
    {
        6,
        {0xC3, 0xB2, 0x59, 0x35, 0x3C, 0x28},
        "VACATION SKELETON TEAMMATE DISEASE AVENUE ADVISORY",
        "The symphony orchestra visited the investment firm —",
        "TO MAKE A SOUND INVESTMENT"
    },
    {
        6,
        {0xC5, 0xB1, 0x1D, 0x1B, 0xD8, 0x08},
        "POWERFUL SIDEWALK RIPPLE HEARING SQUADRON DECIDE",
        "When the mummy expert was buried in research papers, he was —",
        "ALL WRAPPED UP IN HIS WORK"
    },
    {
        5,
        {0xAA, 0x1B, 0x53, 0xA9, 0x30, 0x00},
        "HANDBOOK BOUNCE OFFICER FAIRNESS CAMPUS",
        "The clock stopped right during dinner, so the hungry family went —",
        "BACK FOR FOUR SECONDS"
    },
    {
        5,
        {0x2D, 0x6A, 0x3A, 0x55, 0x14, 0x00},
        "GOLDFISH FASHION THROAT FUNCTION COUNTRY",
        "The dentist and the manicurist fell in love and agreed they —",
        "FOUGHT TOOTH AND NAIL"
    },
    {
        4,
        {0xE2, 0x93, 0x71, 0x0E, 0x00, 0x00},
        "HANDSOME HERITAGE DEPOSIT RITUAL",
        "When the chimney sweep tried on his custom tuxedo, it —",
        "SUITED HIM TO A TEE"
    },
    {
        6,
        {0xD2, 0xE8, 0xD1, 0x1B, 0x3C, 0x08},
        "CLOTHING THOUSAND DECISION FESTIVAL POSITIVE MOBILE",
        "The scarecrow was promoted to regional vice president because he was —",
        "\"OUT-STANDING\" IN HIS FIELD"
    },
    {
        5,
        {0x3A, 0x4E, 0xC9, 0x53, 0x78, 0x00},
        "HORIZON INVADER HERITAGE GENERAL PRUDENT",
        "When the tightrope walker lost his footing high above, he was —",
        "LIVING ON THE RAZOR EDGE"
    },
    {
        6,
        {0xE4, 0xA6, 0x95, 0x96, 0x4B, 0x02},
        "SYMBOLIC AMETHYST PRUDENCE SPOONFUL STUDENT HONEST",
        "The lumberjack couldn't solve the crossword puzzle because he was —",
        "COMPLETELY STUMPED ON IT"
    },
    {
        4,
        {0x0F, 0x35, 0x68, 0x49, 0x00, 0x00},
        "LOYALTY LOCUST SUBTITLE ACROBAT",
        "When the pirate captain took the reading test, he admitted he was —",
        "TOTALLY LOST AT \"C\""
    },
    {
        5,
        {0x59, 0x74, 0x36, 0x27, 0x5C, 0x00},
        "WORKSHOP CATEGORY CHEETAH ETHICS ACHIEVE",
        "The butcher was having a tough afternoon at the counter because —",
        "THE STEAKS WERE TOO HIGH"
    },
    {
        5,
        {0xE4, 0x47, 0x2D, 0x2B, 0x08, 0x00},
        "REQUIRED RAINBOW BACKING NATIVE GROUND",
        "When the marathon runner entered the bakery, she asked for —",
        "A QUICK BREAD WINNER"
    },
    {
        5,
        {0x4D, 0x99, 0x3A, 0x1D, 0x36, 0x00},
        "PARKING MEDICINE FAIRNESS INSTANCE UTENSIL",
        "The photographer took a picture of the thunderstorm and said it was —",
        "A STRIKING MASTERPIECE"
    },
    {
        4,
        {0x33, 0x1B, 0x22, 0x04, 0x00, 0x00},
        "BELIEF DIGITAL STUDIO COTTAGE",
        "When the tailor finished three custom suits in one day, he was —",
        "FIT TO BE TIED"
    },
    {
        5,
        {0x4E, 0x1B, 0x87, 0x3C, 0x19, 0x00},
        "POWERFUL SOFTWARE THOROUGH BULLDOG FABRIC",
        "The astronomer stared at the distant galaxy and proclaimed —",
        "OUT OF THIS WHOLE WORLD"
    },
    {
        5,
        {0x93, 0xAA, 0xA3, 0xC9, 0x11, 0x00},
        "DAYDREAM HOSPITAL HANDSOME HONEYBEE FREEDOM",
        "When the baseball team bought a flight to Florida, they were —",
        "HEADED FOR HOME PLATE"
    },
    {
        6,
        {0x47, 0x59, 0xA5, 0x1E, 0x2D, 0x02},
        "WEATHER KNITTING URBANITE REPORT GINGER SHADOW",
        "The dog trainer had trouble finding his runaway pup because he was —",
        "BARKING UP THE WRONG TREE"
    },
    {
        6,
        {0xAA, 0xC6, 0x27, 0xD2, 0x55, 0x80},
        "SNOWBALL DESCRIBE FEMALE GRANDEUR LAUNDRY DELIVERY",
        "When the detective opened the calendar, he warned the crook that his —",
        "DAYS WERE FULLY NUMBERED"
    },
    {
        5,
        {0x1E, 0xD2, 0x35, 0x27, 0x13, 0x00},
        "COMPUTER APPETITE PELICAN THEOLOGY CONSOLE",
        "The lazy kangaroo spent his entire summer vacation being a —",
        "COMPLETE \"POUCH\" POTATO"
    },
    {
        5,
        {0x78, 0xCC, 0x35, 0x1E, 0x06, 0x00},
        "DOLPHIN ENGINEER DILIGENT CONDUCT GLOVES",
        "When the baker made twenty loaves of sourdough, his accountant said he was —",
        "ROLLING DEEP IN DOUGH"
    },
    {
        6,
        {0xCA, 0x5A, 0x65, 0x3A, 0xB8, 0x09},
        "EXERCISE TRAVELED CONNECT FLUTTER VIOLENCE NATURAL",
        "The electrician received an award from the city council for —",
        "EXCELLENT CURRENT EVENTS"
    },
    {
        5,
        {0x2E, 0x47, 0x2D, 0xD2, 0x06, 0x00},
        "INVESTOR WORKSHOP HILLSIDE JEALOUSY ESSENCE",
        "When the cobbler lost his favorite leather hammer, he cried that he had —",
        "LOST HIS VERY OWN \"SOLE\""
    },
    {
        5,
        {0x4B, 0xB8, 0xAC, 0x4E, 0x06, 0x00},
        "TRIBUNAL LAUGHTER UNLIKELY PEACEFUL ALCHEMY",
        "The deep sea fisherman had a fantastic morning on the boat and was —",
        "A TRULY REEL BIG CATCH"
    },
    {
        5,
        {0x33, 0x96, 0x3A, 0xD2, 0x04, 0x00},
        "ALGEBRA INTEGRAL BALANCE MAGNETIC FLATWARE",
        "When the tightrope walker fell into the safety net, the ringmaster said —",
        "A REAL BALANCING ACT"
    },
    {
        5,
        {0x66, 0x1B, 0x71, 0x3C, 0x61, 0x00},
        "EQUATION COMPUTER SEAFARER FOSTER SENATOR",
        "The math teacher built a fence around his square garden to protect his —",
        "PRECIOUS SQUARE ROOTS"
    },
    {
        5,
        {0x63, 0x17, 0x71, 0x8B, 0x49, 0x00},
        "MILLION PLEASURE PHEASANT DAYLIGHT ECLIPSE",
        "When the pilot flew through the clear blue sky, he noticed that it was —",
        "PLAIN AND SIMPLE TO SEE"
    },
    {
        5,
        {0x55, 0x4D, 0x35, 0xC6, 0x68, 0x00},
        "OPTIMIST PROPOSAL HEIRLOOM CHESTNUT SEQUENCE",
        "The chef was overwhelmed by the holiday rush and complained that he had —",
        "TOO MUCH UPON HIS PLATE"
    },
    {
        5,
        {0x65, 0x3C, 0x0F, 0xAA, 0x24, 0x00},
        "HEROINE REFLECT ENTIRE FAVORITE FRONTIER",
        "When the golfer sank the forty foot putt for eagle, he called it —",
        "A TEE-RIFIC HOLE IN ONE"
    },
    {
        5,
        {0x66, 0x3A, 0x1D, 0x96, 0x08, 0x00},
        "OVERHEAD DATABASE ANCHOR ADDITION MONUMENT",
        "The barber was voted the best shopkeeper in town because his work was —",
        "A HEAD AND A CUT ABOVE"
    },
    {
        4,
        {0x1D, 0x6A, 0x66, 0x10, 0x00, 0x00},
        "DEBATE HONEYBEE THOUSAND DEPUTY",
        "When the sheep sheared off all his wool for summer, his flock called him —",
        "BAA-D TO THE BONE"
    },
    {
        5,
        {0x2B, 0x59, 0x53, 0x59, 0x78, 0x00},
        "VETERAN WESTERN MONETARY HERRING NURSERY",
        "The meteorologist didn't mind the blizzard one bit because she was —",
        "WEATHERING EVERY STORM"
    },
    {
        5,
        {0x0F, 0x56, 0x47, 0x65, 0x3C, 0x00},
        "POWERFUL UNBIASED RADIANCE FASHION JEALOUS",
        "When the bank teller was promoted to branch manager, her colleagues said —",
        "A SOUND BALANCE OF POWER"
    },
    {
        5,
        {0x33, 0xE8, 0xCC, 0x1D, 0x5A, 0x00},
        "RELIGION KNITTING MAGNOLIA OCTAGON PHEASANT",
        "The carpenter inspected the crooked bookshelf and told his apprentice —",
        "GOING AGAINST THE GRAIN"
    },
    {
        5,
        {0xA6, 0x33, 0xA3, 0x99, 0x2A, 0x00},
        "ALPHABET GRADUATE FLATWARE NINETEEN CATEGORY",
        "When the frog won the gold medal in the triple jump, it was —",
        "AN UN-FROG-ETTABLE LEAP"
    },
    {
        6,
        {0x71, 0x3A, 0x2D, 0x71, 0x2B, 0x40},
        "WORKSHOP CRICKET LIBERTY BALCONY TYPIST PLAYMATE",
        "The librarian solved the cold case mystery because she always —",
        "WENT STRICTLY BY THE BOOK"
    },
    {
        5,
        {0x8D, 0x87, 0x27, 0xA4, 0x24, 0x00},
        "GARDENER TALENTED ADEQUATE TREASURY HUNGRY",
        "When the cow stepped into the dairy parlor, the herdsman declared —",
        "AN \"UDDER\"-LY GREAT DAY"
    },
    {
        5,
        {0x2D, 0x74, 0x69, 0x47, 0x01, 0x00},
        "JOURNAL SIDEWALK BACKING INTEGRAL STREAMER",
        "The artist was unable to paint his masterpiece portrait and was —",
        "JUST DRAWING A BLANK"
    },
    {
        5,
        {0x1B, 0x59, 0x72, 0x33, 0x26, 0x00},
        "KNITTING CONFIRM DILIGENT DOLPHIN ROOSTER",
        "When the clockmaker fixed the antique grandfather clock, he did it —",
        "IN THE NICK OF GOOD TIME"
    },
    {
        6,
        {0x6C, 0x39, 0x2D, 0x65, 0x74, 0x08},
        "REVISION PARENT ALGEBRA GRADIENT PANTHER METHOD",
        "The gardener loved growing grapes along the stone wall because he was —",
        "HEARING ON THE GRAPEVINE"
    },
    {
        6,
        {0xD2, 0xB1, 0xB8, 0x4D, 0x2E, 0x08},
        "SKELETON CARRIAGE GRACIOUS TITANIUM NURSERY STEREO",
        "When the tennis star served five aces in a single game, she made —",
        "A SERIOUS RACKET IN COURT"
    },
    {
        4,
        {0x96, 0x3A, 0x1B, 0x85, 0x00, 0x00},
        "SKYLIGHT BRIGHT HERITAGE SCHEDULE",
        "The author loved typing on his vintage mechanical typewriter because it —",
        "HIT THE RIGHT KEYS"
    },
    {
        5,
        {0x4B, 0x33, 0xC3, 0xA3, 0x29, 0x00},
        "PARKING FRACTION CONDENSE TRILLION NOVELIST",
        "When the bowler rolled twelve strikes in a row, the alley manager said —",
        "A STRIKING PERFECTION"
    },
    {
        6,
        {0x33, 0xB8, 0x53, 0x2B, 0xE8, 0x30},
        "WARDROBE TRAINING SHORTAGE THUNDER LANDLORD DISPATCH",
        "The plumber worked all night on the burst pipe so that his business wouldn't —",
        "GO STRAIGHT DOWN THE DRAIN"
    },
    {
        5,
        {0x6A, 0x69, 0xB4, 0x56, 0x63, 0x00},
        "NECKLACE CUSTOMS ENORMOUS SUNSHINE EDUCATE",
        "When the skunk entered the five star French restaurant, the maitre d' said —",
        "DOES NOT MAKE MUCH \"SCENT\""
    },
    {
        6,
        {0x87, 0x1B, 0x69, 0xC5, 0x3A, 0x03},
        "MAGNOLIA HOLIDAY DISTANT ASSEMBLY LIONESS SORROW",
        "The sailor was promoted to ship captain because he was known for —",
        "SMOOTH AND STEADY SAILING"
    },
    {
        5,
        {0x69, 0x66, 0x56, 0x1E, 0xD2, 0x00},
        "BISCUIT UNBIASED SOUTHERN FASHION FULLNESS",
        "When the tree surgeon climbed the ancient giant redwood, he wanted to —",
        "BRANCH OUT HIS BUSINESS"
    },
    {
        5,
        {0x47, 0x63, 0x2D, 0x53, 0x69, 0x00},
        "KNOTTED CHAPTER AUCTION URBANITE ADDRESS",
        "The musician wrote an award winning film score that really —",
        "STRUCK A RESONANT CHORD"
    },
    {
        6,
        {0xC6, 0x1D, 0x1E, 0x39, 0x27, 0x14},
        "IMPERIAL GROCERY MOTHER LAWYER REFLECT TOFFEE",
        "When the battery was acquitted of all charges in court, the judge said it was —",
        "COMPLETELY FREE OF CHARGE"
    },
    {
        5,
        {0x66, 0x93, 0xE2, 0x4B, 0xA5, 0x00},
        "RELATIVE SOMEBODY CALENDAR INSTANCE ORNAMENT",
        "The horse trotted into the newly built barn and was relieved to find —",
        "A VERY STABLE CONDITION"
    },
    {
        4,
        {0x47, 0x69, 0x2D, 0x3C, 0x00, 0x00},
        "PALETTE STRENGTH LANDMARK PEANUT",
        "When the spider finished spinning the intricate geometric web, it had —",
        "SPUN A TANGLED TALE"
    },
    {
        5,
        {0x55, 0x65, 0xCC, 0x66, 0x1A, 0x00},
        "VACATION SKYLINE POLITICS FLATWARE PATRIOT",
        "The window washer climbed sixty stories up the skyscraper and saw —",
        "A CRYSTAL CLEAR VISION"
    },
    {
        5,
        {0x3C, 0xAA, 0x36, 0x2A, 0x62, 0x00},
        "ALGEBRA UNBIASED CALENDAR INSULATE VOLCANO",
        "When the bell ringer struck the giant cathedral chime, it had —",
        "A SOUND AND NOBLE RING"
    },
    {
        4,
        {0x6C, 0x1D, 0x69, 0x3C, 0x00, 0x00},
        "TOGETHER HISTORY DISTANCE HEROINE",
        "The watchmaker examined the miniature golden gears and said they were —",
        "RIGHT ON THE SECOND"
    },
    {
        6,
        {0xCC, 0x33, 0x4D, 0x3C, 0x0F, 0x02},
        "CLOTHING SHUTTLE DETAILED FRIEND FINISH SUBJECT",
        "When the farmer doubled his harvest yield, his happy neighbor said —",
        "OUT-STANDING IN THE FIELD"
    },
    {
        6,
        {0xA9, 0x99, 0x33, 0x78, 0x66, 0x08},
        "RECEIVER ACTIVATE BETWEEN TORNADO ANCIENT ISOLATE",
        "The chemist loved working with helium and neon gas because they were —",
        "NOBLE AND NEVER REACTIVE"
    },
    {
        5,
        {0x4B, 0xC5, 0x2D, 0x2D, 0x48, 0x00},
        "BILLION MATURITY POLITICS GATHER ILLUSION",
        "When the duck paid cash for her expensive feather hat, she told them —",
        "PUT IT RIGHT ON MY \"BILL\""
    },
    {
        5,
        {0x5A, 0x74, 0x5C, 0x6A, 0x66, 0x00},
        "CRICKET PANCAKE THIMBLE BENEATH PHYSICAL",
        "The chess grandmaster took a bite of his fresh croissant and declared —",
        "CHECKMATE IN THE BAKERY"
    },
    {
        5,
        {0x1D, 0x27, 0x39, 0x5A, 0x1E, 0x00},
        "QUANTITY WIDGET STRUGGLE THRILLED SHIELD",
        "When the pig won first prize at the state fair, his proud family said —",
        "SQUEALING WITH DELIGHT"
    },
    {
        5,
        {0xB1, 0xD1, 0x4D, 0x2E, 0x04, 0x00},
        "YEARBOOK UNBIASED CONTROL POSITIVE FOREIGN",
        "The geologist took a vacation to the Grand Canyon because he found it —",
        "ROCK SOLID IN BEAUTY"
    },
    {
        5,
        {0xE8, 0xF0, 0x2E, 0x6C, 0x0A, 0x00},
        "LANDMARK FRAGMENT STRAIGHT PASSAGE MINISTER",
        "When the runner finished the Boston Marathon, his proud coach said —",
        "MAKING GREAT STRIDES"
    },
    {
        5,
        {0x1D, 0xC6, 0x8E, 0xD4, 0x33, 0x00},
        "INTIMACY CARRIAGE SHOULDER SUNSHINE HYDRANT",
        "The choir sang on top of the mountain ridge and reached —",
        "A HIGHER HARMONY IN TUNE"
    },
    {
        4,
        {0x33, 0x39, 0x27, 0x49, 0x00, 0x00},
        "BATTERY MIXTURE POINTER TORPEDO",
        "When the detective found the stolen diamond watch, he said it was —",
        "ABOUT PROPER TIME"
    },
    {
        5,
        {0x47, 0x6C, 0x1D, 0x1A, 0x0A, 0x00},
        "OBSTACLE SECTION SOCIETY MANUAL PIRATE",
        "The tailor sewed thirty tuxedo lapels in one evening and said it was —",
        "A SUITABLE OCCASION"
    },
    {
        5,
        {0x5A, 0x63, 0x33, 0x53, 0x20, 0x00},
        "SPOONFUL GLORIOUS HAZARD FACTORY MEASURE",
        "When the golfer sliced his tee shot into the woods, his caddie called it —",
        "A ROUGH ROUND OF PLAY"
    },
    {
        5,
        {0x47, 0xD2, 0xC9, 0x4E, 0xE2, 0x00},
        "APPETITE QUANTITY FUNCTION RELIEVE DESIGNER",
        "The doctor was calm in the crowded emergency room because he had —",
        "PLENTY OF TRUE PATIENCE"
    },
    {
        5,
        {0x6A, 0xD8, 0x35, 0x5C, 0x40, 0x00},
        "CHRONIC REACTION SHELTER PERSONAL SUPERIOR",
        "When the florist created a bridal bouquet of fifty red blossoms, she —",
        "ROSE TO THE OCCASION"
    },
    {
        5,
        {0x1D, 0xD8, 0x8E, 0x74, 0x0D, 0x00},
        "DILIGENT RESEARCH THOUSAND FLIGHTS HONEYBEE",
        "The pilot took off into the sunset without a single delay and had —",
        "HEAD HIGH IN THE CLOUDS"
    },
    {
        5,
        {0x2B, 0x17, 0x35, 0x72, 0x22, 0x00},
        "PORTRAIT SHELTER FEDERAL LECTURE DEVICE",
        "When the diver found an oyster with five glowing pearls, it was —",
        "A TREASURE OF THE DEEP"
    },
    {
        4,
        {0x6C, 0xC5, 0x3A, 0x1E, 0x00, 0x00},
        "TOWNSHIP MAGNOLIA EDUCATOR REASON",
        "The carpenter measured the mahogany plank three times because he —",
        "SAW IT COMING AHEAD"
    },
    {
        5,
        {0x9A, 0x5A, 0xD8, 0x56, 0x28, 0x00},
        "TWILIGHT IMMENSE FLAMINGO KITCHEN PLATFORM",
        "When the snowman sat beside the glowing campfire, he was —",
        "MELTING WITH EMOTION"
    },
    {
        5,
        {0xC6, 0xD1, 0x35, 0x2B, 0x10, 0x00},
        "CLOTHING TWILIGHT FAIRNESS NATION PICTURE",
        "The baseball catcher held onto the pop fly with two strikes for —",
        "THE FINAL INNING OUT"
    },
    {
        5,
        {0x55, 0x74, 0x5C, 0x63, 0xB8, 0x00},
        "JUNCTION BOWLING RUBBISH GRAVITY FLOURISH",
        "When the candle shop opened three new franchises, the owner was —",
        "BURNING BRIGHT WITH JOY"
    },
    {
        5,
        {0x5A, 0xE1, 0xC5, 0x5A, 0x81, 0x00},
        "DILIGENT SOMEBODY FOOTBALL UNICORN ELEVATOR",
        "The painter finished the seaside landscape mural and said it was —",
        "DONE IN FLYING COLORS"
    },
    {
        5,
        {0xE1, 0xAC, 0x35, 0x94, 0x06, 0x00},
        "KANGAROO SOFTWARE COCONUT ANCESTOR ASSERT",
        "When the train conductor pulled into the grand terminal, he was —",
        "ON TRACK FOR SUCCESS"
    },
    {
        5,
        {0x66, 0xC3, 0x5C, 0xD2, 0x81, 0x00},
        "LOBSTER DESCRIBE RESTFUL POWERFUL SAUCEPAN",
        "The author completed the suspenseful mystery novel and said —",
        "BOUND FOR BEST SELLER"
    },
    {
        5,
        {0x5C, 0x33, 0x66, 0x53, 0x2C, 0x00},
        "FEATHER THEOLOGY PHEASANT OAKLAND SEAFOOD",
        "When the owl gave a late night lecture at the forest university, it was —",
        "A HOOT AND A HALF TO HEAR"
    },
    {
        4,
        {0x56, 0x17, 0x3A, 0x98, 0x00, 0x00},
        "SANDWICH TISSUE NURSERY DISTRICT",
        "The baker rolled out hundred pastry crusts by hand and was —",
        "IN A CRUST WE TRUST"
    },
    {
        5,
        {0x2B, 0x59, 0x17, 0x39, 0xC8, 0x00},
        "VALIDITY WRESTLE PIRATE HOMELY WINDFALL",
        "When the dog found his buried bone in the backyard, he was —",
        "\"PAW\"-SITIVELY THRILLED"
    },
    {
        6,
        {0x2B, 0x17, 0x2D, 0x3C, 0x0F, 0x02},
        "PRESENCE TOPICAL HILLSIDE BROADEN FEATHER REACTION",
        "The teacher loved teaching geometry because the proofs were —",
        "ALL SHAPED TO PERFECTION"
    },
    {
        6,
        {0x87, 0x56, 0xB4, 0xE2, 0xD2, 0x01},
        "EXCHANGE SWEATER SEDIMENT STOCKING DISPATCH HARBOR",
        "When the electric car plugged into the rapid charger, it was —",
        "CHARGED WITH EXCITEMENT"
    },
    {
        5,
        {0x5C, 0x2E, 0x4D, 0x36, 0x08, 0x00},
        "ELEVATOR UPBEAT STEALTH DESERT CULTURAL",
        "The shoe designer created leather sneakers with gold lace and was —",
        "A STEP ABOVE THE REST"
    },
    {
        5,
        {0x1D, 0x69, 0x87, 0x33, 0x8C, 0x00},
        "COMPUTER FORTUNE CONSTANT RETURN AMETHYST",
        "When the cat curled up on the sunny window sill, she was in —",
        "\"PURR\"-FECT CONTENTMENT"
    },
    {
        4,
        {0xB2, 0x53, 0xB1, 0x1E, 0x00, 0x00},
        "TWILIGHT WHISTLE GOLDFISH COLONY",
        "The river guide paddled through the rapid white water and said —",
        "GOING WITH THE FLOW"
    },
    {
        5,
        {0x4E, 0x71, 0x2D, 0x17, 0x2E, 0x00},
        "STEWARD BALLOON RELIABLE DISPLAY CRAYON",
        "When the jeweler cut the fifty carat diamond into facets, it was —",
        "BRILLIANT BEYOND WORDS"
    },
    {
        5,
        {0x17, 0x2B, 0x5A, 0x3A, 0x01, 0x00},
        "THIMBLE BOUNDARY FLAMINGO DRAGON DIAMOND",
        "The farmer planted rows of giant sunflowers and said they were —",
        "BLOOMING AND BRIGHT"
    },
    {
        4,
        {0x4E, 0x3C, 0x96, 0x4D, 0x00, 0x00},
        "SKILLET YEARBOOK RELIGION SWEETLY",
        "When the actor nailed the difficult monologue on Broadway, he —",
        "BROKE A LEG IN STYLE"
    },
    {
        5,
        {0x8D, 0x55, 0x39, 0x72, 0x09, 0x00},
        "LARKSPUR THINKING PAINTER VILLAGE INSULATE",
        "The mechanic tuned the sports car engine until it was —",
        "PURRING LIKE A KITTEN"
    },
    {
        5,
        {0x5A, 0x35, 0x56, 0xE4, 0x03, 0x00},
        "MAGAZINE BREEZE SWEATER MAGNETIC SURFACE",
        "When the bee hive produced ten gallons of clover honey, it was —",
        "CREATING A SWEET BUZZ"
    },
    {
        4,
        {0x6C, 0xAC, 0x0F, 0x62, 0x00, 0x00},
        "PRESERVE OFFERING UNLIKELY VENTURE",
        "The bookkeeper balanced thirty accounts to the penny and said —",
        "FIGURES NEVER LIE"
    },
    {
        5,
        {0x3A, 0x39, 0xC6, 0x96, 0x50, 0x00},
        "SWEETLY YELLOW SKELETON HEIRLOOM BOULDER",
        "When the clock maker repaired the tower clock, the town council said —",
        "TIMELY WORK WELL DONE"
    },
    {
        5,
        {0x53, 0xC5, 0x55, 0x1D, 0x06, 0x00},
        "EARNINGS THINKING FORTUNE FICTION FUNCTION",
        "The gardener trimmed the hedge into a green dinosaur and was —",
        "CUTTING A FINE FIGURE"
    },
    {
        5,
        {0xD8, 0x33, 0x4B, 0x5C, 0x4B, 0x00},
        "MAGAZINE SCRIBE GENETIC FEATHER FIGHTER",
        "When the sailboat rounded the windy cape, the crew reported —",
        "CATCHING A FRESH BREEZE"
    },
    {
        5,
        {0x3C, 0x55, 0x66, 0x72, 0x04, 0x00},
        "TRAILWAY PIPELINE HERITAGE CLOTHES BOUTIQUE",
        "The potter spun the wet clay into an elegant vase and said —",
        "SHAPING UP REAL WELL"
    },
    {
        4,
        {0x17, 0xC3, 0x07, 0x40, 0x00, 0x00},
        "WOOLEN EMPHASIS HUNDRED BALCONY",
        "When the magician vanished from the locked trunk, the crowd said —",
        "NOW YOU SEE HIM"
    },
    {
        4,
        {0xD8, 0x6C, 0x4B, 0x33, 0x00, 0x00},
        "SHORTAGE REGIONAL THIRTEEN TOGETHER",
        "The archer hit the center bullseye three times in a row for —",
        "RIGHT ON THE TARGET"
    },
    {
        5,
        {0x4E, 0x17, 0x63, 0x72, 0xB0, 0x00},
        "OBEDIENT TEACHER FLOURISH TOPICAL SUPERIOR",
        "When the weaver finished the silk tapestry on the loom, it had —",
        "THREADS OF BRILLIANCE"
    },
    {
        4,
        {0x9A, 0x2B, 0x78, 0x32, 0x00, 0x00},
        "ACTIVITY SKATER KNOTTED BAMBOO",
        "The ice hockey team won the championship game on home ice and —",
        "SKATED TO VICTORY"
    },
    {
        5,
        {0x2D, 0x1D, 0x78, 0x1D, 0x59, 0x00},
        "STRANGER TOGETHER BROTHER HEROIC EPISODE",
        "When the chef baked the golden soufflé without it deflating, it —",
        "ROSE TO GREATER HEIGHTS"
    },
    {
        5,
        {0x53, 0x66, 0x4E, 0x74, 0x01, 0x00},
        "RETRIEVE CALENDAR CRYSTAL PROJECT SUNBEAM",
        "The astronomer discovered a new comet in the night sky and said —",
        "A STELLAR DISCOVERY"
    },
    {
        5,
        {0x17, 0x36, 0xF0, 0x3A, 0x9C, 0x00},
        "TWILIGHT THINKING SOUTHERN BLOSSOM SHORTAGE",
        "When the blacksmith forged the iron horseshoe, he told his apprentice —",
        "STRIKE WHILE IRON IS HOT"
    },
};

#endif // JUMBLE_DATASET_H
