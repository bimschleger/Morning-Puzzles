#ifndef JUMBLE_DATASET_H
#define JUMBLE_DATASET_H

#include <Arduino.h>
#include "JumbleGen.h"

struct CompactRiddleSet {
    JumbleDifficulty diff;
    uint8_t numWords;
    const char* words[6];
    uint8_t circles[6][4];
    uint8_t numCircles[6];
    const char* riddle;
    const char* answer;
};

static const size_t TOTAL_JUMBLE_PUZZLES = 300;
static const CompactRiddleSet JUMBLE_DATASET[] PROGMEM = {
    {
        JUMBLE_EASY, 4,
        {"KINGDOM", "MAGNET", "GUEST", "SHOUT", "", ""},
        {{1, 3, 4, 5}, {0, 2, 4, 5}, {0, 1, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "Why did the coffee file a police report?",
        "IT GOT MUGGED"
    },
    {
        JUMBLE_EASY, 5,
        {"JOURNEY", "VISIT", "WEIGHT", "STAND", "SETTLE", ""},
        {{0, 1, 2, 4}, {0, 1, 2, 3}, {0, 1, 3, 4}, {1, 2, 3, 4}, {2, 3, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "What did the ocean say to the sailboat?",
        "NOTHING IT JUST WAVED"
    },
    {
        JUMBLE_EASY, 5,
        {"TRAVEL", "PALACE", "CHASE", "MYSTERY", "PRIDE", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 4, 6}, {4, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "Why do we tell actors to 'break a leg'?",
        "EVERY PLAY HAS A CAST"
    },
    {
        JUMBLE_EASY, 4,
        {"SOLDIER", "ORANGE", "UNIQUE", "TOWER", "", ""},
        {{0, 1, 3, 4}, {0, 1, 2, 3}, {1, 0, 0, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "What do you call a sleeping dinosaur?",
        "A \"DINO\"-SNORE"
    },
    {
        JUMBLE_EASY, 4,
        {"ANIMAL", "ALPHABET", "VISIT", "THINK", "", ""},
        {{0, 1, 2, 3}, {0, 2, 4, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 3, 1, 1, 0, 0},
        "What do you call a fake noodle?",
        "AN \"IM-PASTA\""
    },
    {
        JUMBLE_EASY, 4,
        {"DRAWER", "TWIST", "KITTEN", "REGION", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 3, 4}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "Why did the bicycle fall over?",
        "IT WAS \"TWO-TIRED\""
    },
    {
        JUMBLE_EASY, 4,
        {"CHANCE", "SPEECH", "WHOLE", "SPACE", "", ""},
        {{0, 1, 2, 3}, {0, 2, 3, 4}, {1, 2, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "What do you call cheese that isn't yours?",
        "\"NACHO\" CHEESE"
    },
    {
        JUMBLE_EASY, 4,
        {"THEATER", "SAILOR", "LOVER", "EVENT", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "Why couldn't the pony sing in the choir?",
        "A LITTLE HOARSE"
    },
    {
        JUMBLE_EASY, 4,
        {"VISION", "TARGET", "LANTERN", "NOBLE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 3, 4}, {0, 1, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 2, 0, 0},
        "What do you call an alligator in a vest?",
        "AN \"IN-VEST\"-IGATOR"
    },
    {
        JUMBLE_EASY, 4,
        {"BREED", "DOUGH", "FROZEN", "WINDY", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 0, 0, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "What do you call a cow with no legs?",
        "GROUND BEEF"
    },
    {
        JUMBLE_EASY, 4,
        {"WALLET", "PENGUIN", "POLITE", "ANGLE", "", ""},
        {{0, 2, 3, 4}, {0, 1, 2, 3}, {1, 2, 3, 4}, {1, 4, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 2, 0, 0},
        "Why did the banana go to the doctor?",
        "NOT \"PEELING\" WELL"
    },
    {
        JUMBLE_EASY, 4,
        {"WAFER", "MASTER", "ORCHID", "DECAY", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 4, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "Why did the picture go to jail?",
        "IT WAS FRAMED"
    },
    {
        JUMBLE_EASY, 4,
        {"MARBLE", "IMAGE", "TRULY", "APPLY", "", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 4}, {2, 0, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "What do you call a bear with no teeth?",
        "A GUMMY BEAR"
    },
    {
        JUMBLE_EASY, 4,
        {"BOUNCE", "HARMONY", "PENNY", "VOYAGE", "", ""},
        {{0, 1, 3, 4}, {0, 1, 3, 4}, {1, 0, 0, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "Why do bees have sticky hair?",
        "A HONEYCOMB"
    },
    {
        JUMBLE_EASY, 4,
        {"TIMER", "FORUM", "CRYSTAL", "LOYAL", "", ""},
        {{0, 1, 2, 3}, {0, 2, 3, 4}, {0, 2, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "Why did the cookie go to the hospital?",
        "IT FELT CRUMMY"
    },
    {
        JUMBLE_EASY, 4,
        {"MEADOW", "RAINBOW", "TRAIN", "SUNNY", "", ""},
        {{0, 1, 2, 4}, {1, 2, 3, 6}, {0, 0, 0, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "What do you call a pile of kittens?",
        "A \"MEOW\"-NTAIN"
    },
    {
        JUMBLE_EASY, 4,
        {"HARMONY", "ROCKET", "GENTLE", "KITTEN", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 4}, {1, 2, 3, 5}, {2, 3, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "What did one wall say to the other?",
        "MEET AT THE CORNER"
    },
    {
        JUMBLE_EASY, 4,
        {"BLAZE", "LEOPARD", "SQUAD", "GUILD", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 5}, {2, 0, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "What do you call a sleeping bull?",
        "A \"BULL\"-DOZER"
    },
    {
        JUMBLE_EASY, 4,
        {"PIVOT", "WEATHER", "STAIR", "QUERY", "", ""},
        {{0, 1, 2, 3}, {0, 1, 3, 5}, {0, 1, 0, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "Why was the broom late for work?",
        "IT OVER-SWEPT"
    },
    {
        JUMBLE_EASY, 5,
        {"WHISTLE", "DANGER", "SOLDIER", "ANSWER", "SMART", ""},
        {{0, 2, 3, 4}, {0, 1, 2, 3}, {0, 2, 3, 4}, {0, 2, 4, 5}, {0, 2, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "Why did the tomato blush?",
        "IT SAW SALAD DRESSING"
    },
    {
        JUMBLE_EASY, 4,
        {"MONKEY", "EARLY", "PRAY", "PARTY", "", ""},
        {{0, 1, 2, 3}, {0, 0, 0, 0}, {2, 0, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 1, 1, 1, 0, 0},
        "What kind of key opens a banana?",
        "A \"MON-KEY\""
    },
    {
        JUMBLE_EASY, 4,
        {"PAINTER", "FEATHER", "RURAL", "CLAIM", "", ""},
        {{0, 1, 2, 3}, {1, 3, 4, 5}, {0, 2, 0, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "What do you call an elephant that doesn't matter?",
        "\"IRRELEPHANT\""
    },
    {
        JUMBLE_EASY, 4,
        {"HORIZON", "LANTERN", "DRONE", "NATURE", "", ""},
        {{0, 1, 3, 5}, {0, 1, 2, 4}, {3, 0, 0, 0}, {5, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "Why did the golfer bring extra socks?",
        "A HOLE IN ONE"
    },
    {
        JUMBLE_EASY, 4,
        {"HOLIDAY", "RITUAL", "SLEEP", "FINAL", "", ""},
        {{0, 1, 2, 3}, {0, 1, 3, 4}, {0, 0, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "What do you call a funny mountain?",
        "\"HILL\"-ARIOUS"
    },
    {
        JUMBLE_EASY, 4,
        {"SHADOW", "SWEAT", "ICING", "DODGE", "", ""},
        {{1, 2, 3, 4}, {1, 3, 4, 0}, {1, 0, 0, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 3, 1, 1, 0, 0},
        "What kind of dog tells time?",
        "A \"WATCH\" DOG"
    },
    {
        JUMBLE_EASY, 5,
        {"ALPHABET", "PIRATES", "UPSET", "FOUND", "ADULT", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {4, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "Why was the belt arrested?",
        "HELD UP PAIR OF PANTS"
    },
    {
        JUMBLE_EASY, 4,
        {"BROWN", "ANIMAL", "RAPID", "VIGOR", "", ""},
        {{0, 1, 2, 3}, {0, 1, 0, 0}, {1, 0, 0, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 2, 1, 1, 0, 0},
        "What bow can never be tied?",
        "A RAINBOW"
    },
    {
        JUMBLE_EASY, 4,
        {"PANTHER", "HONEST", "SEAFOOD", "BLEED", "", ""},
        {{0, 1, 2, 3}, {0, 1, 3, 4}, {0, 1, 4, 5}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "What kind of shoes do frogs wear?",
        "\"OPEN-TOAD\" SHOES"
    },
    {
        JUMBLE_EASY, 5,
        {"WHISTLE", "NOTEBOOK", "KINGDOM", "NORTH", "WARRIOR", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 4, 5}, {1, 2, 3, 4}, {2, 3, 5, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 3, 0},
        "Why do cows wear bells?",
        "THEIR HORNS DO NOT WORK"
    },
    {
        JUMBLE_EASY, 4,
        {"STACK", "THICK", "SNACK", "ROCKET", "", ""},
        {{0, 1, 2, 0}, {2, 0, 0, 0}, {3, 0, 0, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {3, 1, 1, 1, 0, 0},
        "What do you call a boomerang that doesn't return?",
        "A STICK"
    },
    {
        JUMBLE_EASY, 4,
        {"SQUARE", "WEATHER", "TRICK", "SNACK", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 5}, {1, 2, 3, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "Why did the duck get sent to the principal?",
        "A WISE \"QUACKER\""
    },
    {
        JUMBLE_EASY, 4,
        {"UPSET", "LANTERN", "JOURNEY", "PEDAL", "", ""},
        {{0, 1, 2, 3}, {2, 3, 0, 0}, {4, 0, 0, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 2, 1, 1, 0, 0},
        "What kind of music do planets listen to?",
        "\"NEP-TUNES\""
    },
    {
        JUMBLE_EASY, 4,
        {"ALPHABET", "BOTTLE", "TREATY", "STRING", "", ""},
        {{0, 2, 4, 6}, {1, 0, 0, 0}, {0, 0, 0, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 1, 1, 1, 0, 0},
        "What starts with T, ends with T, and has T inside?",
        "A TEAPOT"
    },
    {
        JUMBLE_EASY, 4,
        {"TRAFFIC", "VOLCANO", "HORIZON", "CHAIN", "", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 4}, {1, 2, 5, 6}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "Why did the tree go to the dentist?",
        "FOR A ROOT CANAL"
    },
    {
        JUMBLE_EASY, 5,
        {"TIGER", "THEATER", "SOLDIER", "ROCKET", "MAYOR", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 2, 3}, {0, 1, 4, 5}, {3, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "Why did the chicken cross the playground?",
        "TO GET TO OTHER SLIDE"
    },
    {
        JUMBLE_EASY, 4,
        {"WINDOW", "FLOWER", "STEEP", "WEAPON", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {3, 4, 5, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "Why was the computer cold?",
        "LEFT WINDOWS OPEN"
    },
    {
        JUMBLE_EASY, 4,
        {"LATCH", "CHOICE", "PHONE", "CREST", "", ""},
        {{0, 1, 2, 3}, {0, 1, 0, 0}, {2, 0, 0, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 2, 1, 1, 0, 0},
        "What kind of candy never arrives on time?",
        "\"CHOC\"-LATE"
    },
    {
        JUMBLE_EASY, 4,
        {"WEAPON", "SNACK", "GLORY", "SADLY", "", ""},
        {{0, 1, 2, 4}, {0, 1, 2, 4}, {0, 1, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "What kind of car does an egg drive?",
        "A \"YOLK\"-SWAGEN"
    },
    {
        JUMBLE_EASY, 4,
        {"PEACOCK", "JOKER", "CHAMP", "PUPPET", "", ""},
        {{0, 2, 3, 4}, {1, 2, 4, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 3, 1, 1, 0, 0},
        "What do you call a pig that knows karate?",
        "A PORK CHOP"
    },
    {
        JUMBLE_EASY, 5,
        {"WALLET", "INLET", "SUITE", "BOTTLE", "STAIR", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 3, 4}, {1, 2, 3, 5}, {1, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "What did the grape say when stepped on?",
        "LET OUT A LITTLE \"WINE\""
    },
    {
        JUMBLE_EASY, 4,
        {"ORANGE", "TIGHT", "THOSE", "CHEER", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 0, 0},
        "Why did the music teacher need a ladder?",
        "TO REACH HIGH NOTES"
    },
    {
        JUMBLE_EASY, 4,
        {"NEEDLE", "MEMORY", "THEORY", "WORRY", "", ""},
        {{0, 1, 2, 3}, {1, 3, 4, 0}, {2, 0, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 3, 1, 1, 0, 0},
        "What do you call a deer with no eyes?",
        "\"NO-EYE\" DEER"
    },
    {
        JUMBLE_EASY, 4,
        {"PENGUIN", "CABINET", "HUNTER", "PAINTER", "", ""},
        {{0, 1, 2, 3}, {1, 3, 0, 0}, {1, 0, 0, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 2, 1, 1, 0, 0},
        "What kind of bird can write?",
        "A \"PEN\"-GUIN"
    },
    {
        JUMBLE_EASY, 4,
        {"NOTEBOOK", "BOAST", "ACTOR", "VOLCANO", "", ""},
        {{1, 4, 5, 6}, {0, 0, 0, 0}, {0, 0, 0, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 1, 1, 1, 0, 0},
        "What do you call a ghost's mistake?",
        "A \"BOO-BOO\""
    },
    {
        JUMBLE_EASY, 4,
        {"ESCAPE", "SPEECH", "TENDER", "DRIFT", "", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 5}, {1, 2, 3, 4}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "Why did the astronaut break up with his girlfriend?",
        "HE NEEDED SPACE"
    },
    {
        JUMBLE_EASY, 4,
        {"BOARD", "MARBLE", "PARADE", "CANDY", "", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 4}, {1, 2, 3, 4}, {0, 1, 3, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "What do you call a magic dog?",
        "\"LABRA-CADABRA\"-DOR"
    },
    {
        JUMBLE_EASY, 4,
        {"BOTTLE", "FUTURE", "LINER", "WEATHER", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 3, 0}, {6, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "Why did the candle quit its job?",
        "FELT BURNT OUT"
    },
    {
        JUMBLE_EASY, 4,
        {"ENOUGH", "HEDGE", "HEALTH", "DECIDE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 4, 5}, {0, 1, 4, 5}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 0, 0},
        "Why did the baker go to the bank?",
        "HE NEEDED THE DOUGH"
    },
    {
        JUMBLE_EASY, 4,
        {"MAJESTY", "AWAIT", "STAIN", "HEAVEN", "", ""},
        {{0, 1, 2, 4}, {0, 1, 2, 3}, {1, 3, 0, 0}, {5, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "Why was the strawberry sad?",
        "IT WAS IN A JAM"
    },
    {
        JUMBLE_EASY, 4,
        {"CAPTAIN", "UNICORN", "LANTERN", "LEARN", "", ""},
        {{0, 1, 3, 4}, {0, 1, 3, 4}, {1, 2, 3, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "What kind of insect is good at math?",
        "AN \"ACCOUNT-ANT\""
    },
    {
        JUMBLE_EASY, 4,
        {"HARBOR", "FIREFLY", "LOYAL", "CLOAK", "", ""},
        {{0, 2, 3, 4}, {0, 1, 2, 3}, {0, 0, 0, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "Why did the duck buy lipstick?",
        "FOR HER \"BILL\""
    },
    {
        JUMBLE_EASY, 4,
        {"THEATER", "TREASURE", "UPSET", "SOUTH", "", ""},
        {{0, 1, 2, 3}, {1, 3, 4, 5}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "What do you call a dinosaur with a great vocabulary?",
        "A \"THES-AURUS\""
    },
    {
        JUMBLE_EASY, 4,
        {"WEATHER", "LASER", "RURAL", "VIRAL", "", ""},
        {{0, 1, 2, 4}, {0, 1, 2, 3}, {0, 1, 0, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "Why was the king only one foot tall?",
        "HE WAS A RULER"
    },
    {
        JUMBLE_EASY, 6,
        {"PENGUIN", "DOLPHIN", "INSIDE", "STAND", "DRIFT", "SAILOR"},
        {{1, 2, 3, 4}, {0, 1, 2, 4}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 3, 4}, {2, 0, 0, 0}},
        {4, 4, 4, 4, 4, 1},
        "Why did the scarecrow win an award?",
        "\"OUT-STANDING\" IN HIS FIELD"
    },
    {
        JUMBLE_EASY, 4,
        {"MAJESTY", "BLACK", "SHARK", "ACUTE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 3, 4, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "What do you call a sleeping woodcutter?",
        "A \"SLUMBER\"-JACK"
    },
    {
        JUMBLE_EASY, 4,
        {"CHASE", "SOLDIER", "THIEF", "FATAL", "", ""},
        {{0, 1, 2, 3}, {0, 1, 3, 4}, {0, 2, 3, 4}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "What do you call a fish wearing a bowtie?",
        "\"SO-FISH\"-TICATED"
    },
    {
        JUMBLE_EASY, 4,
        {"AWAIT", "TARGET", "TODAY", "SALON", "", ""},
        {{0, 1, 2, 3}, {0, 1, 3, 5}, {0, 1, 2, 4}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "Why did the frog park illegally?",
        "IT GOT \"TOAD\" AWAY"
    },
    {
        JUMBLE_EASY, 4,
        {"RAINBOW", "MEADOW", "TWELVE", "TONGUE", "", ""},
        {{0, 1, 3, 4}, {0, 1, 2, 4}, {0, 1, 2, 3}, {0, 1, 5, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "Why did the melon jump into the lake?",
        "TO BE A WATER-MELON"
    },
    {
        JUMBLE_EASY, 4,
        {"ALTER", "FARMER", "NERVE", "SHORT", "", ""},
        {{0, 1, 2, 3}, {1, 0, 0, 0}, {1, 0, 0, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 1, 1, 1, 0, 0},
        "What kind of tea is hard to swallow?",
        "\"REAL-TEA\""
    },
    {
        JUMBLE_EASY, 4,
        {"LIZARD", "ZEBRA", "READY", "GLORY", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 3, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "What do you call a bear caught in the rain?",
        "A \"DRIZZLY\" BEAR"
    },
    {
        JUMBLE_EASY, 4,
        {"PIRATES", "PASTEL", "PENGUIN", "PLANT", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 3, 4}, {1, 3, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "What do you call a turtle taking photos?",
        "A \"SNAPPING\" TURTLE"
    },
    {
        JUMBLE_EASY, 4,
        {"SELDOM", "SMOOTH", "PALACE", "BRAVE", "", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 5}, {0, 1, 0, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "What kind of dog loves bubble baths?",
        "A \"SHAM-POODLE\""
    },
    {
        JUMBLE_EASY, 5,
        {"WEATHER", "WARRIOR", "SHAME", "FOREST", "THIGH", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 2, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "Why did the cookie cry?",
        "ITS MOTHER WAS A WAFER"
    },
    {
        JUMBLE_EASY, 4,
        {"PROMISE", "DECOR", "EXPERT", "SHIRT", "", ""},
        {{1, 2, 3, 5}, {0, 1, 2, 3}, {0, 3, 0, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "What do you call an apology written in dots and dashes?",
        "\"RE-MORSE\" CODE"
    },
    {
        JUMBLE_EASY, 4,
        {"VILLAGE", "HEDGE", "THEATER", "FUDGE", "", ""},
        {{1, 2, 3, 4}, {0, 1, 2, 3}, {0, 1, 2, 4}, {0, 2, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "Why did the candle visit the doctor?",
        "FELT \"LIGHT\"-HEADED"
    },
    {
        JUMBLE_EASY, 4,
        {"PIRATES", "ALPHABET", "SECTOR", "SHORE", "", ""},
        {{0, 1, 3, 4}, {0, 1, 2, 4}, {0, 1, 2, 3}, {0, 2, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "Why did the orange go to court?",
        "TO \"APPEAL\" ITS CASE"
    },
    {
        JUMBLE_EASY, 4,
        {"BONUS", "BUDDY", "AMONG", "GUIDE", "", ""},
        {{0, 2, 3, 4}, {0, 1, 4, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 3, 1, 1, 0, 0},
        "What do you call a rabbit with fleas?",
        "\"BUGS\" BUNNY"
    },
    {
        JUMBLE_EASY, 4,
        {"DIAMOND", "PANTHER", "SOLAR", "CHASE", "", ""},
        {{0, 2, 3, 4}, {0, 1, 2, 4}, {0, 0, 0, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "What do you call a clean pig?",
        "HAM AND SOAP"
    },
    {
        JUMBLE_EASY, 4,
        {"TEMPLE", "ALPHABET", "GRAPE", "INSECT", "", ""},
        {{0, 1, 2, 3}, {0, 1, 4, 0}, {1, 0, 0, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 3, 1, 1, 0, 0},
        "What kind of tree loves high fives?",
        "A PALM TREE"
    },
    {
        JUMBLE_EASY, 4,
        {"ANIMAL", "DISCO", "MEADOW", "NOISE", "", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 4}, {2, 0, 0, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "What do you call a cow playing an instrument?",
        "A \"MOO\"-SICIAN"
    },
    {
        JUMBLE_EASY, 4,
        {"CHILI", "CATTLE", "VILLAGE", "LINEN", "", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 4}, {1, 2, 3, 6}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "What do you call a tiny pepper in winter?",
        "A LITTLE \"CHILLI\""
    },
    {
        JUMBLE_EASY, 4,
        {"LEOPARD", "TONGUE", "DELAY", "AUDIO", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 1, 2, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "Why did the violin take a bow?",
        "PLAYED A GOOD TUNE"
    },
    {
        JUMBLE_EASY, 4,
        {"VILLAGE", "GENTLE", "ALIVE", "THEORY", "", ""},
        {{1, 2, 3, 4}, {0, 1, 0, 0}, {1, 0, 0, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 2, 1, 1, 0, 0},
        "What do you call an eagle that tells bad jokes?",
        "\"ILL-EAGLE\""
    },
    {
        JUMBLE_EASY, 4,
        {"WHISTLE", "DRAWER", "LABEL", "SOLVE", "", ""},
        {{0, 2, 3, 4}, {0, 1, 2, 3}, {0, 2, 3, 4}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "Why was the loaf of bread so polite?",
        "IT WAS WELL-BRED"
    },
    {
        JUMBLE_EASY, 4,
        {"CABINET", "VILLAGE", "APART", "CRISP", "", ""},
        {{1, 2, 3, 4}, {2, 3, 4, 6}, {0, 2, 0, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "What do you call a dancing sheep?",
        "A \"BAA\"-LLERINA"
    },
    {
        JUMBLE_EASY, 4,
        {"ATTACK", "BRICK", "SOCKET", "PEDAL", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {2, 3, 0, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "What do you call a noisy insect playing sports?",
        "A CRICKET BAT"
    },
    {
        JUMBLE_EASY, 4,
        {"RAINBOW", "RABBIT", "MAGIC", "VOICE", "", ""},
        {{0, 1, 2, 3}, {2, 3, 4, 5}, {0, 2, 3, 4}, {1, 2, 3, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "What do you call a funny frog on stage?",
        "A \"RIBBIT\"-ING COMIC"
    },
    {
        JUMBLE_EASY, 4,
        {"DRAWER", "NUMBER", "DESERT", "EVERY", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 3, 4}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 0, 0},
        "Why did the calendar look worried?",
        "DAYS WERE NUMBERED"
    },
    {
        JUMBLE_EASY, 4,
        {"CATTLE", "POLITE", "LEVEL", "RELAX", "", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 4}, {0, 1, 0, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "What do you call a cold horse in the pasture?",
        "A LITTLE \"COLT\""
    },
    {
        JUMBLE_EASY, 4,
        {"RAINBOW", "BLESS", "SIGMA", "CHAIN", "", ""},
        {{0, 1, 2, 3}, {0, 2, 3, 4}, {0, 2, 0, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "What do you call a singing fish?",
        "A BASS SINGER"
    },
    {
        JUMBLE_EASY, 4,
        {"MACHINE", "PANIC", "YIELD", "CIDER", "", ""},
        {{0, 1, 2, 3}, {0, 2, 3, 4}, {0, 0, 0, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "What do you call a sweet monkey?",
        "\"CHIMP\" CANDY"
    },
    {
        JUMBLE_EASY, 4,
        {"WEATHER", "NOTEBOOK", "STRIKE", "SLIDE", "", ""},
        {{0, 1, 2, 4}, {0, 1, 3, 4}, {0, 2, 4, 5}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "Why did the shoe visit the hospital?",
        "HEEL WAS BROKEN"
    },
    {
        JUMBLE_EASY, 4,
        {"DIAMOND", "CANDLE", "FROZEN", "GLANCE", "", ""},
        {{0, 1, 2, 4}, {1, 2, 3, 4}, {4, 0, 0, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "What do you call a lion with flowers?",
        "A \"DANDE-LION\""
    },
    {
        JUMBLE_EASY, 4,
        {"PAINTER", "REWARD", "DIAMOND", "DANCE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 3, 4}, {0, 2, 4, 5}, {0, 4, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 2, 0, 0},
        "Why did the cloud cry all morning?",
        "RAINED ON PARADE"
    },
    {
        JUMBLE_EASY, 4,
        {"CABINET", "LETTER", "THEME", "SCORE", "", ""},
        {{0, 2, 3, 4}, {0, 1, 0, 0}, {0, 0, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 2, 1, 1, 0, 0},
        "What did the zero say to the eight?",
        "\"NICE BELT\""
    },
    {
        JUMBLE_EASY, 4,
        {"NOTEBOOK", "SYMBOL", "NORMAL", "SPOIL", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 3, 4}, {1, 2, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "Why was the math book sad?",
        "TOO MANY PROBLEMS"
    },
    {
        JUMBLE_EASY, 4,
        {"CAMERA", "GRASP", "STUFF", "FIXED", "", ""},
        {{0, 1, 2, 3}, {1, 2, 4, 0}, {2, 3, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 3, 2, 1, 0, 0},
        "What do you call a sleeping pie?",
        "A \"CREAM PUFF\""
    },
    {
        JUMBLE_EASY, 4,
        {"WINDFALL", "FATAL", "FLOUR", "VESSEL", "", ""},
        {{0, 1, 2, 4}, {0, 1, 2, 3}, {0, 1, 2, 3}, {2, 3, 5, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "Why did the stadium get so cool?",
        "IT WAS FULL OF FANS"
    },
    {
        JUMBLE_EASY, 4,
        {"BLANKET", "TOTAL", "FRONT", "SECTOR", "", ""},
        {{0, 1, 2, 5}, {0, 0, 0, 0}, {2, 0, 0, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 1, 1, 1, 0, 0},
        "What has a neck but no head?",
        "A BOTTLE"
    },
    {
        JUMBLE_EASY, 4,
        {"BASIC", "COMPASS", "TEMPO", "GLORY", "", ""},
        {{0, 1, 0, 0}, {0, 0, 0, 0}, {2, 0, 0, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {2, 1, 1, 1, 0, 0},
        "What has teeth but cannot bite?",
        "A COMB"
    },
    {
        JUMBLE_EASY, 5,
        {"FINISH", "MACHINE", "NEEDLE", "SEAFOOD", "SPOON", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 5}, {0, 1, 2, 4}, {0, 1, 4, 5}, {2, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "Why did the golfer wear two pairs of pants?",
        "IN CASE OF HOLE IN ONE"
    },
    {
        JUMBLE_EASY, 4,
        {"BLANK", "PENGUIN", "FUNNY", "TULIP", "", ""},
        {{0, 3, 4, 0}, {2, 3, 4, 6}, {0, 1, 4, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {3, 4, 3, 1, 0, 0},
        "What do you call a rabbit that does martial arts?",
        "\"KUNG FU\" BUNNY"
    },
    {
        JUMBLE_EASY, 4,
        {"VENUE", "RECORD", "RADAR", "CROWN", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "What do you call a sleeping police car?",
        "AN UNDER-\"COVER\" CAR"
    },
    {
        JUMBLE_EASY, 5,
        {"HARMONY", "PENGUIN", "SOUND", "DIRTY", "FUTURE", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {2, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "What did the pencil sharpener say to the pencil?",
        "STOP TURNING MY HEAD"
    },
    {
        JUMBLE_EASY, 4,
        {"JOURNEY", "FORTUNE", "CABINET", "POLITE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 3, 4}, {0, 1, 3, 4}, {3, 4, 5, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "Why did the orange stop rolling down the hill?",
        "IT RAN OUT OF JUICE"
    },
    {
        JUMBLE_EASY, 4,
        {"WHISTLE", "KITTEN", "MACHINE", "MYSTERY", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "What did the stamp say to the letter?",
        "\"STICK WITH ME\""
    },
    {
        JUMBLE_EASY, 4,
        {"SWIFT", "STEEP", "POCKET", "FIFTH", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 4, 5}, {0, 2, 3, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "Why did the broom jump for joy?",
        "SWEPT OFF ITS FEET"
    },
    {
        JUMBLE_EASY, 4,
        {"DOLPHIN", "KINGDOM", "ORGAN", "UNION", "", ""},
        {{0, 1, 4, 5}, {1, 0, 0, 0}, {0, 0, 0, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 1, 1, 1, 0, 0},
        "What do you call an owl magician?",
        "\"HOO-DINI\""
    },
    {
        JUMBLE_EASY, 4,
        {"NOTEBOOK", "POTATO", "DOUGH", "SYMBOL", "", ""},
        {{1, 2, 3, 4}, {0, 1, 2, 4}, {0, 1, 3, 4}, {0, 1, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "Why did the skeleton cross the road?",
        "TO GET TO BODY SHOP"
    },
    {
        JUMBLE_EASY, 4,
        {"JOURNEY", "ALPHABET", "VALLEY", "EIGHT", "", ""},
        {{0, 1, 3, 4}, {0, 1, 2, 4}, {2, 3, 4, 5}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "What do you call a happy farmer in spring?",
        "A JOLLY PLANTER"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"SWEET", "TIMER", "BLESS", "SPREAD", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "When the tailor was asked how business was going, he said —",
        "\"SEW\" IT SEEMS"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"PRONE", "EVERY", "STEEP", "CYCLE", "", ""},
        {{0, 1, 2, 3}, {0, 2, 4, 0}, {2, 0, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 3, 1, 1, 0, 0},
        "The optician gave his patient a discount, which was a real —",
        "EYE OPENER"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"WHISTLE", "LESSON", "BLOOM", "VIGOR", "", ""},
        {{1, 2, 3, 4}, {0, 1, 2, 3}, {1, 2, 0, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "When the cobbler lost his favorite tools, he felt like he —",
        "LOST HIS \"SOLE\""
    },
    {
        JUMBLE_MEDIUM, 4,
        {"FEATHER", "GLACIER", "CRANE", "SUMMER", "", ""},
        {{1, 2, 3, 4}, {1, 2, 3, 5}, {0, 0, 0, 0}, {5, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "The fisherman was very popular with the town because he was —",
        "A REEL CATCH"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"CABINET", "SHIELD", "DELTA", "EIGHT", "", ""},
        {{1, 2, 3, 4}, {1, 2, 3, 4}, {0, 1, 2, 3}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "When the butcher backed into the slicer, he got —",
        "A LITTLE BEHIND"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"WINDFALL", "HOLIDAY", "MAGNET", "TOUGH", "", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 4}, {1, 3, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "The carpenter finished building the table and proudly said —",
        "NAILED IT DOWN"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"MARKET", "WIDTH", "ENOUGH", "FIGHT", "", ""},
        {{1, 2, 3, 4}, {1, 2, 3, 0}, {1, 0, 0, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 3, 1, 1, 0, 0},
        "When the electricity failed during class, the students were —",
        "IN THE DARK"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"CATTLE", "SOLVE", "LOWER", "FRONT", "", ""},
        {{0, 1, 2, 3}, {0, 0, 0, 0}, {0, 0, 0, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 1, 1, 1, 0, 0},
        "The pirate had trouble learning the alphabet because he was —",
        "LOST AT \"C\""
    },
    {
        JUMBLE_MEDIUM, 4,
        {"MORNING", "ENOUGH", "FLIGHT", "GUILD", "", ""},
        {{1, 2, 3, 4}, {1, 2, 3, 4}, {1, 2, 3, 4}, {3, 4, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 2, 0, 0},
        "When the baker won the lottery, his friends knew he was —",
        "ROLLING IN DOUGH"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"RAINBOW", "WIDTH", "DRONE", "ELECT", "", ""},
        {{0, 1, 2, 3}, {0, 2, 3, 4}, {0, 2, 3, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "The plumber had to retire early because all his plans went —",
        "DOWN THE DRAIN"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"PANTHER", "RIDGE", "SIGHT", "ENGINE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 3, 5}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 0, 0},
        "When the gardener was praised for his flowers, he said —",
        "DIGGING THE PRAISE"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"DEVICE", "MANGO", "ESCAPE", "WORST", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 5}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "The watchmaker was asked for the time, and he replied —",
        "GIVE ME A SECOND"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"BASIS", "THOSE", "TRAFFIC", "FEATHER", "", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 4}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "When the baseball player struck out, his coach told him —",
        "OFF HIS BASE"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"ACTIVE", "ABOUT", "SUNSHINE", "PLUME", "", ""},
        {{0, 1, 2, 4}, {0, 1, 2, 0}, {1, 0, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 3, 1, 1, 0, 0},
        "The barber was thrilled with his successful shop because it was —",
        "A CUT ABOVE"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"BLANKET", "STOCK", "THINK", "FANCY", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 4, 0}, {0, 1, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 2, 0, 0},
        "When the musician fell through the floor, he was —",
        "FLAT ON HIS BACK"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"TORQUE", "TREASURE", "CUSTOM", "POUND", "", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 4}, {1, 2, 0, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "The math teacher went to the farm looking for —",
        "SQUARE ROOTS"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"ROUGH", "TOOTH", "SHADOW", "FIFTH", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 3, 4, 0}, {0, 2, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 3, 0, 0},
        "When the chef seasoned the soup, he told the waiter —",
        "FOOD FOR THOUGHT"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"OCTOPUS", "PHOTO", "PAUSE", "AUDIO", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 0, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "The lazy kangaroo spent all afternoon being a —",
        "\"POUCH\" POTATO"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"WHISTLE", "FEATHER", "HELLO", "SENSE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 2, 3}, {0, 3, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 2, 0, 0},
        "Why did the crab never share his lunch with the starfish?",
        "HE WAS \"SHELL-FISH\""
    },
    {
        JUMBLE_MEDIUM, 4,
        {"VIOLIN", "ENGINE", "GENTLE", "THUNDER", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {1, 4, 5, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "When the tightrope walker lost his footing, he was —",
        "LIVING ON THE EDGE"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"PLANET", "STREET", "OFFER", "GATHER", "", ""},
        {{0, 1, 2, 3}, {0, 1, 3, 4}, {0, 0, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "The pilot didn't want to argue about the flight plan because it was —",
        "PLANE TO SEE"
    },
    {
        JUMBLE_MEDIUM, 5,
        {"TEMPLE", "CUSTOM", "SELDOM", "PLUME", "JOURNEY", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 3, 4}, {0, 1, 3, 4}, {6, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "When the lumberjack couldn't answer the riddle, he was —",
        "COMPLETELY STUMPED"
    },
    {
        JUMBLE_MEDIUM, 5,
        {"FLIGHT", "HOUND", "THROAT", "ADOPT", "CAPTAIN", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 1, 2, 4}, {3, 6, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "The dentist and the manicurist fell in love and —",
        "FOUGHT TOOTH AND NAIL"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"ACTIVE", "NEEDLE", "STAKE", "SNAKE", "", ""},
        {{0, 1, 2, 4}, {0, 1, 2, 4}, {0, 2, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "When the skunk couldn't pay the bill, he told the waiter to —",
        "LEAVE A \"SCENT\""
    },
    {
        JUMBLE_MEDIUM, 5,
        {"PEACOCK", "SKETCH", "FIFTH", "CHARGE", "CREDIT", ""},
        {{1, 2, 3, 4}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 5}, {3, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "The clock was sent to the principal's office because it —",
        "TICKED OFF TEACHERS"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"DAMAGE", "LEOPARD", "GRAPH", "POLAR", "", ""},
        {{1, 2, 3, 4}, {1, 0, 0, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 1, 1, 1, 0, 0},
        "When the sheep took over the farm, the neighbors called it a —",
        "\"RAM-PAGE\""
    },
    {
        JUMBLE_MEDIUM, 4,
        {"HARBOR", "MOUNT", "SECTOR", "PRIZE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 3, 4}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "The tree surgeon went on vacation because he wanted to —",
        "BRANCH OUT MORE"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"PRIZE", "BLEND", "DOUBLE", "DRAWER", "", ""},
        {{1, 2, 3, 4}, {0, 2, 3, 0}, {0, 0, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 3, 1, 1, 0, 0},
        "When the meteorologist arrived on time, everyone said he —",
        "BREEZED IN"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"WINDFALL", "BLANKET", "SHARK", "GLANCE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {2, 3, 4, 0}, {0, 2, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 2, 0, 0},
        "The artist didn't know what to paint next, so he was —",
        "DRAWING A BLANK"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"WINDFALL", "PLEAD", "GUILD", "BRIDGE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "When the snake passed the math quiz, the teacher said it was —",
        "\"ADD-ING\" UP WELL"
    },
    {
        JUMBLE_MEDIUM, 5,
        {"RAINBOW", "WITCH", "DONOR", "TODAY", "NEEDLE", ""},
        {{1, 2, 3, 4}, {0, 2, 3, 4}, {0, 1, 2, 3}, {0, 1, 2, 4}, {1, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "The ghost couldn't find a partner at the dance because he had —",
        "\"NO-BODY\" TO DANCE WITH"
    },
    {
        JUMBLE_MEDIUM, 5,
        {"EXIST", "GROWL", "MINUS", "CHIMNEY", "THUNDER", ""},
        {{1, 2, 3, 0}, {0, 1, 3, 4}, {0, 1, 2, 3}, {2, 3, 4, 6}, {2, 0, 0, 0}, {0, 0, 0, 0}},
        {3, 4, 4, 4, 1, 0},
        "When the hotel on the beach flooded, the guests were —",
        "SWIMMING IN LUXURY"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"BUTTON", "HARBOR", "DENSE", "DRONE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 3, 4}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 0, 0},
        "The candle factory closed its doors because the workers were —",
        "BURNED AT BOTH ENDS"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"CABINET", "HONEST", "STEAL", "LASER", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 2, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 2, 0, 0},
        "When the banker lost his composure, his colleagues said he —",
        "LOST HIS BALANCE"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"GHOST", "DIAMOND", "MORAL", "ANGLE", "", ""},
        {{0, 1, 2, 4}, {0, 0, 0, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 1, 1, 1, 0, 0},
        "The dog sat by the fireplace all winter because he was —",
        "A HOT DOG"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"RAINBOW", "LAWYER", "YELLOW", "WEIGHT", "", ""},
        {{1, 3, 4, 5}, {0, 1, 2, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 3, 1, 1, 0, 0},
        "When the quarterback gave an interview, the reporters were —",
        "BLOWN AWAY"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"REWARD", "NUMBER", "DESERT", "READY", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 0, 0},
        "The detective arrested the calendar maker because his —",
        "DAYS WERE NUMBERED"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"STRING", "SPRING", "AGAIN", "CLEAN", "", ""},
        {{0, 1, 2, 3}, {0, 2, 3, 4}, {0, 1, 0, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "When the baker's apprentice made great sourdough, he was —",
        "A RISING STAR"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"WINDFALL", "STAGE", "GOLDEN", "FAVOR", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 5, 0}, {0, 3, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 2, 0, 0},
        "The elevator attendant had a bad day because business was —",
        "GOING DOWN FAST"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"OCTOPUS", "SHELF", "HONOR", "FLASK", "", ""},
        {{0, 2, 3, 4}, {0, 1, 2, 3}, {0, 1, 3, 0}, {0, 1, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 2, 0, 0},
        "When the frog took the stage, the audience gave him a —",
        "\"HOLE\" LOT OF HOPS"
    },
    {
        JUMBLE_MEDIUM, 5,
        {"CAPTAIN", "SUNSHINE", "HEAVEN", "DOMAIN", "ENJOY", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 3, 5}, {1, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "The lawyer was delighted with his new case because it was —",
        "AN OPEN AND SHUT CASE"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"PICTURE", "MODERN", "THUNDER", "FIBER", "", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 4}, {2, 3, 4, 5}, {0, 3, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "When the cow won the ribbon at the county fair, it was —",
        "\"UDDER\" PERFECTION"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"SEAFOOD", "FOUND", "DOCTOR", "INSECT", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {2, 4, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 2, 0, 0},
        "The photographer loved developing black and white pictures because they —",
        "FOCUSED ON FACTS"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"OCTOPUS", "SPHERE", "FARMER", "HURRY", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {1, 2, 3, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "When the golfer made a miraculous putt, the gallery said —",
        "PAR FOR THE COURSE"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"WEATHER", "NOTEBOOK", "BLOCK", "BADLY", "", ""},
        {{0, 1, 3, 4}, {0, 1, 2, 3}, {0, 2, 4, 0}, {0, 4, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 2, 0, 0},
        "The librarian was an extraordinary detective because she —",
        "WENT BY THE BOOK"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"IMPACT", "TOUCH", "THUMB", "SCOUT", "", ""},
        {{0, 1, 2, 3}, {0, 0, 0, 0}, {1, 0, 0, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 1, 1, 1, 0, 0},
        "When the pig won the jackpot, all his barn friends told him to —",
        "HAM IT UP"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"WHEEL", "NEEDLE", "SKULL", "POLAR", "", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 4}, {3, 0, 0, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "The shoemaker's new assistant was learning fast and was —",
        "WELL-HEELED"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"MACHINE", "STING", "LAUGH", "SMELL", "", ""},
        {{0, 1, 3, 4}, {0, 1, 2, 3}, {1, 3, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "When the tennis star won the championship, his serve was —",
        "A SMASHING HIT"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"GIRAFFE", "FEATHER", "RECORD", "DONOR", "", ""},
        {{0, 2, 3, 4}, {0, 1, 4, 5}, {0, 1, 2, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "The battery was never worried about debt because it was —",
        "FREE OF CHARGE"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"BUTTON", "PROMISE", "JELLY", "LINEN", "", ""},
        {{0, 1, 2, 3}, {0, 2, 3, 4}, {2, 3, 4, 0}, {1, 2, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 2, 0, 0},
        "When the duck paid for dinner, he told the waiter —",
        "PUT IT ON MY \"BILL\""
    },
    {
        JUMBLE_MEDIUM, 4,
        {"WHISTLE", "DOCTOR", "FLOUR", "OTHER", "", ""},
        {{0, 1, 2, 3}, {0, 1, 3, 4}, {0, 1, 2, 3}, {1, 4, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 2, 0, 0},
        "The astronomer loved his late night job because it was —",
        "OUT OF THIS WORLD"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"WEATHER", "ALPHABET", "BREED", "PENGUIN", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 2, 3}, {0, 3, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 2, 0, 0},
        "When the spider designed a new website, the client said it had —",
        "GREAT WEB APPEAL"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"CABINET", "SOLDIER", "TENNIS", "RATIO", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {2, 3, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "The horse was happy in the barn because he was in —",
        "STABLE CONDITION"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"TENDER", "FORTUNE", "CLOVER", "LUNCH", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 3, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "When the mirror fell off the wall, the owner said he —",
        "COULD NOT REFLECT"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"FINGER", "CRYSTAL", "REBEL", "GLORY", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {2, 3, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 2, 0, 0},
        "The magician had to cancel his airplane flight because he was a —",
        "FLYING \"SORCERER\""
    },
    {
        JUMBLE_MEDIUM, 4,
        {"KINGDOM", "ALPHABET", "BEACH", "NORMAL", "", ""},
        {{0, 1, 2, 4}, {0, 1, 2, 4}, {0, 2, 3, 0}, {1, 3, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 2, 0, 0},
        "When the snowman went to the gym, he worked on his —",
        "\"AB-DOMINAL\" PACK"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"ANIMAL", "GLACIER", "FIREFLY", "MYSTERY", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 2, 0}, {5, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "The bell ringer loved his morning routine because it had a —",
        "FAMILIAR RING"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"KINGDOM", "SOLDIER", "UNICORN", "DONOR", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {2, 3, 4, 5}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "When the geologist proposed on one knee, he gave her a —",
        "ROCK SOLID RING"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"RAINBOW", "SWAMP", "PENGUIN", "MUSEUM", "", ""},
        {{0, 1, 2, 3}, {1, 3, 4, 0}, {3, 0, 0, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 3, 1, 1, 0, 0},
        "The author loved working near the campfire because the plot was —",
        "WARMING UP"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"QUEEN", "SNACK", "CLOAK", "ROCKY", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 3, 4, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "When the pig entered the clean pen, he said it was —",
        "SQUEAKY CLEAN"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"MANNER", "COACH", "FEATHER", "PROFIT", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {1, 2, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 2, 0, 0},
        "The diver explored the coral reef and discovered —",
        "AN OCEAN OF CHARM"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"FRIEND", "ISLAND", "DRIFT", "TEACH", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 4}, {0, 2, 3, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "When the farmer looked over his wheat crop, he said it was —",
        "FIRST IN FIELD"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"SKETCH", "ORCHID", "GUARD", "ELDER", "", ""},
        {{0, 1, 3, 4}, {0, 1, 2, 3}, {1, 2, 3, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "The violinist was praised by the critics because his playing —",
        "STRUCK A CHORD"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"PENGUIN", "ISLAND", "WINDFALL", "LEAP", "", ""},
        {{0, 2, 3, 5}, {0, 1, 2, 3}, {1, 2, 5, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "When the sailor navigated into port without a map, he said —",
        "PLAIN SAILING"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"PRINCE", "REFER", "UNICORN", "ARISE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 3, 4}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "The chef dropped his favorite pan and said it was a —",
        "RECIPE FOR RUIN"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"PIRATES", "LIGHT", "WHISTLE", "QUERY", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 3, 4, 5}, {1, 2, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "When the bowler got three strikes in a row, he was —",
        "RIGHT UP HIS ALLEY"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"WINDFALL", "FLOCK", "SOCKET", "MINUS", "", ""},
        {{0, 1, 4, 6}, {0, 1, 2, 3}, {0, 1, 3, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "The candle was very popular because it was always —",
        "SO FULL OF WICK"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"SOLDIER", "FORTUNE", "GUEST", "CREST", "", ""},
        {{0, 1, 3, 4}, {0, 1, 2, 3}, {1, 2, 3, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "When the runner crossed the finish line, he said he was —",
        "OUT OF STRIDES"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"SOCKET", "STUDY", "EXCUSE", "BEING", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 4}, {0, 2, 4, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "The locksmith was hired immediately because he had the —",
        "KEY TO SUCCESS"
    },
    {
        JUMBLE_MEDIUM, 5,
        {"RAINBOW", "POWDER", "BLANKET", "GUITAR", "GRAPE", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 4}, {0, 3, 4, 5}, {0, 1, 3, 5}, {0, 1, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "When the dog barked at the oak tree, his owner said he was —",
        "BARKING UP WRONG TREE"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"LEOPARD", "CANDY", "STAND", "TRASH", "", ""},
        {{0, 1, 4, 5}, {0, 1, 3, 4}, {0, 0, 0, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 1, 1, 0, 0},
        "The window cleaner loved his tall job because it was —",
        "CLEAR AS DAY"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"TOMATO", "JOURNEY", "FLEET", "RESCUE", "", ""},
        {{0, 1, 2, 4}, {1, 2, 5, 6}, {0, 1, 2, 3}, {1, 3, 5, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "When the sheep sheared his wool, he told his pal —",
        "\"FLEECE\" TO MEET YOU"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"ROCKET", "TARGET", "TENTH", "THIGH", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "The train conductor loved his morning route because it was —",
        "ON THE RIGHT TRACK"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"WEATHER", "HOUSE", "TRACE", "DRIVE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 3, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "When the bee landed on the rose, the gardener said it was —",
        "A SWEET TOUCH"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"ALPHABET", "SHIFT", "RITUAL", "CABLE", "", ""},
        {{1, 3, 5, 6}, {0, 2, 3, 4}, {1, 2, 0, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "The tailor made a pair of trousers with two pockets and said —",
        "FITS THE BILL"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"WOUND", "TOMATO", "ORCHID", "HORSE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 4}, {0, 2, 3, 5}, {0, 1, 3, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "When the pilot landed safely in the fog, his copilot said —",
        "SMOOTH TOUCH DOWN"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"MODERN", "PANTHER", "LUNAR", "LEOPARD", "", ""},
        {{0, 1, 2, 3}, {1, 2, 4, 5}, {0, 1, 3, 0}, {5, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "The baseball player was thrilled with his new contract because it was —",
        "A HOME RUN DEAL"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"VOLCANO", "KINGDOM", "SHAFT", "RITUAL", "", ""},
        {{0, 1, 4, 5}, {1, 3, 5, 6}, {0, 3, 0, 0}, {2, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "When the cow jumped over the moon, the calf said it was —",
        "\"MOO\"-VING FAST"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"POLITE", "TENTH", "WHOLE", "FLOCK", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "The carpenter admired the antique cabinet and said it was —",
        "TOP OF THE LINE"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"SOCKET", "APART", "TUNNEL", "THROW", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 5, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "When the ghost joined the choir, the conductor said his voice was —",
        "\"SPOOK\"-TACULAR"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"WINTER", "DOCTOR", "LOVER", "OPERA", "", ""},
        {{0, 1, 2, 3}, {0, 1, 3, 4}, {1, 3, 0, 0}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "The gardener won the giant pumpkin contest because he was —",
        "ROOTED TO WIN"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"MOTHER", "REIGN", "POINT", "TIMBER", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {2, 3, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "When the clock struck midnight, the night watchman said —",
        "RIGHT ON TIME"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"SEAFOOD", "DIAMOND", "ISLAND", "QUILT", "", ""},
        {{0, 1, 2, 3}, {0, 2, 4, 5}, {1, 4, 5, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "The fish stayed in deep water during the storm to remain —",
        "SAFE AND SOUND"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"CLOAK", "PARENT", "BUDDY", "FATAL", "", ""},
        {{1, 2, 3, 4}, {0, 1, 2, 4}, {1, 2, 3, 4}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "When the baker made fresh croissants, his customers said —",
        "FLAKY AND PROUD"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"PURPLE", "CRYSTAL", "FLAME", "NUMBER", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 2, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "The cat chased the ball of yarn and declared it —",
        "\"PURR\"-FECT PLAY"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"CAPTAIN", "INSIDE", "SOUND", "FRIEND", "", ""},
        {{0, 1, 2, 4}, {0, 1, 2, 3}, {0, 1, 3, 4}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "When the photographer took a snapshot of the cheetah, it was —",
        "A SNAP DECISION"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"CURVE", "ENTER", "LANTERN", "CRUST", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {2, 3, 4, 5}, {3, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "The electrician was always excited because he loved —",
        "CURRENT EVENTS"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"WEATHER", "MOTHER", "MOUSE", "STREET", "", ""},
        {{0, 1, 3, 4}, {0, 1, 2, 3}, {0, 1, 4, 0}, {3, 4, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 2, 0, 0},
        "When the bird built a sturdy nest, her mate said —",
        "HOME TWEET HOME"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"TONGUE", "INSECT", "CRUST", "CATER", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {0, 4, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 2, 0, 0},
        "The barber gave everyone a quick trim and said he was —",
        "CUTTING CORNERS"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"BOTTLE", "DOLPHIN", "MACHINE", "NEEDLE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 4}, {2, 3, 4, 5}, {1, 2, 4, 5}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 0, 0},
        "When the ice sculptor finished his swan, he was —",
        "CHILLED TO THE BONE"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"AIRPORT", "FORTUNE", "OCEAN", "TALENT", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "The detective looked at the muddy boots and said —",
        "A CLEAR FOOTPRINT"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"SECTOR", "SAILOR", "ROUND", "STRING", "", ""},
        {{0, 1, 2, 3}, {2, 3, 4, 5}, {0, 1, 2, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "When the painter finished the wall in blue, he said —",
        "IN TRUE COLORS"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"MASTER", "RADISH", "THIGH", "WHALE", "", ""},
        {{0, 1, 2, 3}, {1, 3, 4, 0}, {1, 0, 0, 0}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 3, 1, 1, 0, 0},
        "The tennis champion won the final set with —",
        "A SMASH HIT"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"ALPHABET", "GIRAFFE", "OTHER", "AWAKE", "", ""},
        {{0, 1, 2, 3}, {1, 3, 4, 5}, {0, 1, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "When the frog leaped across the lily pads, he took a —",
        "LEAP OF FAITH"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"DAMAGE", "GIRAFFE", "STONE", "JUDGE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 4, 5}, {2, 3, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "The jeweler polished the emerald until it was —",
        "A GEM OF A FIND"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"FINGER", "SHORT", "RATIO", "BOTTLE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {1, 5, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 2, 0, 0},
        "When the farmer repaired his barn roof, he was —",
        "RAISING THE ROOF"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"RAINBOW", "SWING", "LAUGH", "HONOR", "", ""},
        {{0, 2, 3, 4}, {0, 1, 2, 3}, {0, 3, 4, 0}, {0, 1, 3, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 3, 0, 0},
        "The musician played his trumpet so loud he was —",
        "BLOWING HIS HORN"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"SHADOW", "TWICE", "DECIDE", "ISSUE", "", ""},
        {{0, 1, 2, 4}, {1, 2, 3, 4}, {1, 2, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "When the owl gave advice in the forest, everyone said —",
        "A WISE CHOICE"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"DOUBLE", "FINGER", "ROYAL", "COMPASS", "", ""},
        {{0, 1, 2, 3}, {0, 2, 3, 5}, {0, 1, 2, 4}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "The runner tied his sneakers tight and said he was —",
        "BOUND FOR GLORY"
    },
    {
        JUMBLE_MEDIUM, 4,
        {"NOTEBOOK", "DOUBLE", "PASTEL", "PLANE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {1, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "When the bookbinder finished the leather volume, he said —",
        "BOUND TO PLEASE"
    },
    {
        JUMBLE_HARD, 5,
        {"COMPASS", "WHISTLE", "COFFEE", "LEASE", "SAMPLE", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 4}, {0, 2, 3, 4}, {0, 1, 2, 3}, {1, 4, 5, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 3, 0},
        "When the optometrist fell into the lens grinder, he made —",
        "A SPECTACLE OF HIMSELF"
    },
    {
        JUMBLE_HARD, 6,
        {"ACTIVE", "NOTEBOOK", "STAKE", "SELDOM", "MOMENT", "NATURE"},
        {{0, 2, 3, 4}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 2, 3, 4}, {0, 3, 0, 0}},
        {4, 4, 4, 4, 4, 2},
        "The symphony orchestra visited the investment firm —",
        "TO MAKE A SOUND INVESTMENT"
    },
    {
        JUMBLE_HARD, 6,
        {"WINDFALL", "WHISPER", "PEACOCK", "PLUCK", "AIRPORT", "BLAST"},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 2, 4}, {0, 2, 3, 5}, {1, 0, 0, 0}},
        {4, 4, 4, 4, 4, 1},
        "When the mummy expert was buried in research papers, he was —",
        "ALL WRAPPED UP IN HIS WORK"
    },
    {
        JUMBLE_HARD, 5,
        {"NOTEBOOK", "PEACOCK", "STOCK", "FRAUD", "FOREST", ""},
        {{0, 1, 3, 4}, {2, 3, 4, 5}, {0, 2, 4, 0}, {0, 1, 3, 4}, {0, 2, 4, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 4, 3, 0},
        "The clock stopped right during dinner, so the hungry family went —",
        "BACK FOR FOUR SECONDS"
    },
    {
        JUMBLE_HARD, 5,
        {"FLIGHT", "HOUND", "THROAT", "ADOPT", "SUNSET", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 1, 2, 4}, {2, 5, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "The dentist and the manicurist fell in love and agreed they —",
        "FOUGHT TOOTH AND NAIL"
    },
    {
        JUMBLE_HARD, 4,
        {"MEDIA", "THEATER", "STATUE", "NOISE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {1, 2, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "When the chimney sweep tried on his custom tuxedo, it —",
        "SUITED HIM TO A TEE"
    },
    {
        JUMBLE_HARD, 6,
        {"GOLDEN", "SUNSHINE", "TENTH", "FINISH", "HOLIDAY", "PITCH"},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 3, 4, 5}, {1, 0, 0, 0}},
        {4, 4, 4, 4, 4, 1},
        "The scarecrow was promoted to regional vice president because he was —",
        "\"OUT-STANDING\" IN HIS FIELD"
    },
    {
        JUMBLE_HARD, 5,
        {"HORIZON", "LIZARD", "EVENT", "DRAGON", "TONGUE", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 2, 3, 5}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "When the tightrope walker lost his footing high above, he was —",
        "LIVING ON THE RAZOR EDGE"
    },
    {
        JUMBLE_HARD, 6,
        {"SIMPLE", "TEMPLE", "THUNDER", "YELLOW", "DOCTOR", "SHELL"},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 3, 4}, {0, 1, 2, 3}, {1, 2, 3, 4}, {2, 0, 0, 0}},
        {4, 4, 4, 4, 4, 1},
        "The lumberjack couldn't solve the crossword puzzle because he was —",
        "COMPLETELY STUMPED ON IT"
    },
    {
        JUMBLE_HARD, 4,
        {"CRYSTAL", "BALLOON", "TOTAL", "ADULT", "", ""},
        {{0, 2, 3, 4}, {1, 2, 3, 4}, {0, 1, 2, 3}, {3, 4, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 2, 0, 0},
        "When the pirate captain took the reading test, he admitted he was —",
        "TOTALLY LOST AT \"C\""
    },
    {
        JUMBLE_HARD, 5,
        {"WEATHER", "STRIKE", "SOCKET", "ENOUGH", "HEALTH", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 2, 4, 5}, {0, 1, 4, 5}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "The butcher was having a tough afternoon at the counter because —",
        "THE STEAKS WERE TOO HIGH"
    },
    {
        JUMBLE_HARD, 5,
        {"SQUARE", "WANDER", "BRICK", "KNIFE", "WEAPON", ""},
        {{1, 2, 3, 4}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {1, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "When the marathon runner entered the bakery, she asked for —",
        "A QUICK BREAD WINNER"
    },
    {
        JUMBLE_HARD, 5,
        {"MARKET", "PIRATES", "ICING", "GENTLE", "SUNSET", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 5}, {0, 3, 4, 5}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "The photographer took a picture of the thunderstorm and said it was —",
        "A STRIKING MASTERPIECE"
    },
    {
        JUMBLE_HARD, 4,
        {"BOTTLE", "FRIEND", "INSECT", "SHOOT", "", ""},
        {{0, 1, 2, 3}, {0, 2, 3, 5}, {0, 3, 0, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 2, 1, 0, 0},
        "When the tailor finished three custom suits in one day, he was —",
        "FIT TO BE TIED"
    },
    {
        JUMBLE_HARD, 5,
        {"WHISTLE", "FELLOW", "THROW", "WOUND", "TROOP", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {0, 2, 3, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 3, 0},
        "The astronomer stared at the distant galaxy and proclaimed —",
        "OUT OF THIS WHOLE WORLD"
    },
    {
        JUMBLE_HARD, 5,
        {"MORTAL", "LEOPARD", "FEATHER", "HEDGE", "DELTA", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 2, 4}, {0, 4, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "When the baseball team bought a flight to Florida, they were —",
        "HEADED FOR HOME PLATE"
    },
    {
        JUMBLE_HARD, 6,
        {"WARRIOR", "KITTEN", "NUMBER", "PRONE", "HEDGE", "GUITAR"},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 1},
        "The dog trainer had trouble finding his runaway pup because he was —",
        "BARKING UP THE WRONG TREE"
    },
    {
        JUMBLE_HARD, 6,
        {"WINDFALL", "LUMBER", "LEADER", "MYSTERY", "EVERY", "FAULT"},
        {{0, 2, 3, 4}, {0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 4, 5}, {0, 2, 3, 4}, {2, 0, 0, 0}},
        {4, 4, 4, 4, 4, 1},
        "When the detective opened the calendar, he warned the crook that his —",
        "DAYS WERE FULLY NUMBERED"
    },
    {
        JUMBLE_HARD, 5,
        {"TOMATO", "OCTOPUS", "PUPPET", "CLOTH", "THREE", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {1, 3, 4, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 3, 0},
        "The lazy kangaroo spent his entire summer vacation being a —",
        "COMPLETE \"POUCH\" POTATO"
    },
    {
        JUMBLE_HARD, 5,
        {"PENGUIN", "REGION", "DOLPHIN", "ROUND", "VALID", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {1, 2, 3, 4}, {2, 3, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "When the baker made twenty loaves of sourdough, his accountant said he was —",
        "ROLLING DEEP IN DOUGH"
    },
    {
        JUMBLE_HARD, 6,
        {"EXCUSE", "TRAVEL", "SECRET", "LETTER", "GENTLE", "LANTERN"},
        {{0, 1, 2, 3}, {0, 1, 3, 4}, {0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 4, 5}, {2, 6, 0, 0}},
        {4, 4, 4, 4, 4, 2},
        "The electrician received an award from the city council for —",
        "EXCELLENT CURRENT EVENTS"
    },
    {
        JUMBLE_HARD, 5,
        {"VESSEL", "WHISTLE", "YELLOW", "NOTEBOOK", "GLORY", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 5}, {2, 3, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "When the cobbler lost his favorite leather hammer, he cried that he had —",
        "LOST HIS VERY OWN \"SOLE\""
    },
    {
        JUMBLE_HARD, 5,
        {"ALPHABET", "BICYCLE", "TARGET", "CRUEL", "LANTERN", ""},
        {{0, 1, 3, 4}, {0, 1, 2, 3}, {0, 2, 3, 4}, {0, 1, 2, 3}, {0, 3, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "The deep sea fisherman had a fantastic morning on the boat and was —",
        "A TRULY REEL BIG CATCH"
    },
    {
        JUMBLE_HARD, 5,
        {"CABINET", "GLANCE", "CAPTAIN", "LEARN", "LANTERN", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 1, 2, 3}, {2, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "When the tightrope walker fell into the safety net, the ringmaster said —",
        "A REAL BALANCING ACT"
    },
    {
        JUMBLE_HARD, 5,
        {"TORQUE", "PICTURE", "TREASURE", "FORTUNE", "LESSON", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 4}, {1, 2, 3, 4}, {1, 2, 4, 6}, {2, 3, 4, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 3, 0},
        "The math teacher built a fence around his square garden to protect his —",
        "PRECIOUS SQUARE ROOTS"
    },
    {
        JUMBLE_HARD, 5,
        {"PROMISE", "PASTEL", "NEEDLE", "SILENT", "LUNAR", ""},
        {{0, 2, 3, 4}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 3, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 3, 0},
        "When the pilot flew through the clear blue sky, he noticed that it was —",
        "PLAIN AND SIMPLE TO SEE"
    },
    {
        JUMBLE_HARD, 5,
        {"MACHINE", "DOLPHIN", "OCTOPUS", "UNIQUE", "WHISTLE", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 4}, {0, 2, 3, 4}, {0, 1, 2, 4}, {3, 4, 6, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 3, 0},
        "The chef was overwhelmed by the holiday rush and complained that he had —",
        "TOO MUCH UPON HIS PLATE"
    },
    {
        JUMBLE_HARD, 5,
        {"FEATHER", "HORIZON", "NOTICE", "NEEDLE", "SPIKE", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 1, 2, 4}, {2, 4, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "When the golfer sank the forty foot putt for eagle, he called it —",
        "A TEE-RIFIC HOLE IN ONE"
    },
    {
        JUMBLE_HARD, 5,
        {"HEAVEN", "CABINET", "DATED", "AUDIO", "WEATHER", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 2, 3}, {0, 1, 2, 4}, {2, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "The barber was voted the best shopkeeper in town because his work was —",
        "A HEAD AND A CUT ABOVE"
    },
    {
        JUMBLE_HARD, 4,
        {"ALPHABET", "NOTEBOOK", "DEBUT", "OLIVE", "", ""},
        {{0, 3, 4, 5}, {0, 1, 2, 3}, {0, 1, 2, 4}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 1, 0, 0},
        "When the sheep sheared off all his wool for summer, his flock called him —",
        "BAA-D TO THE BONE"
    },
    {
        JUMBLE_HARD, 5,
        {"HEAVEN", "WARRIOR", "MYSTERY", "REGION", "ENTER", ""},
        {{0, 1, 2, 3}, {0, 2, 3, 4}, {0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 2, 3}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "The meteorologist didn't mind the blizzard one bit because she was —",
        "WEATHERING EVERY STORM"
    },
    {
        JUMBLE_HARD, 5,
        {"ANSWER", "ALPHABET", "NOTEBOOK", "DECOR", "FORTUNE", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 3, 4}, {0, 1, 2, 3}, {0, 1, 2, 4}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "When the bank teller was promoted to branch manager, her colleagues said —",
        "A SOUND BALANCE OF POWER"
    },
    {
        JUMBLE_HARD, 5,
        {"REGION", "GIANT", "MORNING", "STAGE", "GATHER", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 3, 4, 5}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "The carpenter inspected the crooked bookshelf and told his apprentice —",
        "GOING AGAINST THE GRAIN"
    },
    {
        JUMBLE_HARD, 5,
        {"ALPHABET", "BLANKET", "TONGUE", "FEATHER", "JOURNEY", ""},
        {{0, 1, 2, 4}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 5}, {2, 3, 5, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 3, 0},
        "When the frog won the gold medal in the triple jump, it was —",
        "AN UN-FROG-ETTABLE LEAP"
    },
    {
        JUMBLE_HARD, 6,
        {"WHISTLE", "NOTEBOOK", "ROCKET", "BOTTLE", "BELLY", "FIFTY"},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 3, 4}, {0, 1, 4, 0}, {3, 4, 0, 0}},
        {4, 4, 4, 4, 3, 2},
        "The librarian solved the cold case mystery because she always —",
        "WENT STRICTLY BY THE BOOK"
    },
    {
        JUMBLE_HARD, 5,
        {"DANGER", "LEADER", "TRADE", "JOURNEY", "FIFTY", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {2, 3, 5, 6}, {4, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "When the cow stepped into the dairy parlor, the herdsman declared —",
        "AN \"UDDER\"-LY GREAT DAY"
    },
    {
        JUMBLE_HARD, 5,
        {"JUNGLE", "WINDFALL", "BLANKET", "CRYSTAL", "FARMER", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {1, 3, 4, 5}, {1, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "The artist was unable to paint his masterpiece portrait and was —",
        "JUST DRAWING A BLANK"
    },
    {
        JUMBLE_HARD, 5,
        {"KINGDOM", "MOTION", "HONEST", "CREDIT", "OFTEN", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 3, 4}, {0, 1, 2, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 3, 0},
        "When the clockmaker fixed the antique grandfather clock, he did it —",
        "IN THE NICK OF GOOD TIME"
    },
    {
        JUMBLE_HARD, 6,
        {"HEAVEN", "AIRPORT", "ENGINE", "GENTLE", "ENOUGH", "WORST"},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 5}, {2, 0, 0, 0}},
        {4, 4, 4, 4, 4, 1},
        "The gardener loved growing grapes along the stone wall because he was —",
        "HEARING ON THE GRAPEVINE"
    },
    {
        JUMBLE_HARD, 6,
        {"SOCKET", "PICTURE", "PAINTER", "TREASURE", "ROGUE", "MERCY"},
        {{0, 1, 2, 3}, {1, 2, 3, 4}, {1, 2, 3, 4}, {1, 2, 3, 4}, {0, 1, 3, 4}, {2, 0, 0, 0}},
        {4, 4, 4, 4, 4, 1},
        "When the tennis star served five aces in a single game, she made —",
        "A SERIOUS RACKET IN COURT"
    },
    {
        JUMBLE_HARD, 4,
        {"STRIKE", "KNIGHT", "THEATER", "HEAVY", "", ""},
        {{0, 1, 2, 3}, {0, 2, 3, 4}, {0, 1, 2, 4}, {0, 1, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "The author loved typing on his vintage mechanical typewriter because it —",
        "HIT THE RIGHT KEYS"
    },
    {
        JUMBLE_HARD, 5,
        {"SOCKET", "PAINTER", "FINGER", "THEATER", "WARRIOR", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 4, 5}, {2, 3, 4, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 3, 0},
        "When the bowler rolled twelve strikes in a row, the alley manager said —",
        "A STRIKING PERFECTION"
    },
    {
        JUMBLE_HARD, 6,
        {"WARRIOR", "DIGIT", "DANGER", "HONEST", "GHOST", "BOTTLE"},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 3, 4}, {2, 3, 0, 0}},
        {4, 4, 4, 4, 4, 2},
        "The plumber worked all night on the burst pipe so that his business wouldn't —",
        "GO STRAIGHT DOWN THE DRAIN"
    },
    {
        JUMBLE_HARD, 5,
        {"SKETCH", "MOMENT", "THUNDER", "CANDLE", "SCORE", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "When the skunk entered the five star French restaurant, the maitre d' said —",
        "DOES NOT MAKE MUCH \"SCENT\""
    },
    {
        JUMBLE_HARD, 6,
        {"DIAMOND", "GOLDEN", "SUNSHINE", "TREATY", "HARMONY", "SHIELD"},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 3, 4}, {0, 2, 3, 4}, {1, 4, 5, 6}, {0, 2, 0, 0}},
        {4, 4, 4, 4, 4, 2},
        "The sailor was promoted to ship captain because he was known for —",
        "SMOOTH AND STEADY SAILING"
    },
    {
        JUMBLE_HARD, 5,
        {"CABINET", "BURST", "SUNSHINE", "HONEST", "SHIRT", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "When the tree surgeon climbed the ancient giant redwood, he wanted to —",
        "BRANCH OUT HIS BUSINESS"
    },
    {
        JUMBLE_HARD, 5,
        {"PEACOCK", "SHOCK", "TRUNK", "STRIKE", "DRAIN", ""},
        {{1, 2, 3, 4}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 2, 4}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "The musician wrote an award winning film score that really —",
        "STRUCK A RESONANT CHORD"
    },
    {
        JUMBLE_HARD, 6,
        {"MORTAL", "PEACOCK", "GLACIER", "THEORY", "FIREFLY", "LEAFY"},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 5}, {1, 2, 3, 4}, {0, 3, 4, 5}, {1, 4, 0, 0}},
        {4, 4, 4, 4, 4, 2},
        "When the battery was acquitted of all charges in court, the judge said it was —",
        "COMPLETELY FREE OF CHARGE"
    },
    {
        JUMBLE_HARD, 5,
        {"VOLCANO", "CABINET", "SOLDIER", "TREATY", "ENTRY", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 4}, {0, 1, 3, 4}, {0, 1, 2, 3}, {0, 1, 2, 4}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "The horse trotted into the newly built barn and was relieved to find —",
        "A VERY STABLE CONDITION"
    },
    {
        JUMBLE_HARD, 4,
        {"PLANET", "GENTLE", "SALAD", "THUNDER", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 4, 5}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 0, 0},
        "When the spider finished spinning the intricate geometric web, it had —",
        "SPUN A TANGLED TALE"
    },
    {
        JUMBLE_HARD, 5,
        {"VIOLIN", "BICYCLE", "LANTERN", "TREASURE", "GRASP", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 4}, {0, 1, 2, 3}, {1, 2, 3, 4}, {1, 2, 3, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 3, 0},
        "The window washer climbed sixty stories up the skyscraper and saw —",
        "A CRYSTAL CLEAR VISION"
    },
    {
        JUMBLE_HARD, 5,
        {"DOUBLE", "REGION", "ISLAND", "DIAMOND", "PENGUIN", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 3, 4}, {0, 2, 4, 5}, {2, 6, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "When the bell ringer struck the giant cathedral chime, it had —",
        "A SOUND AND NOBLE RING"
    },
    {
        JUMBLE_HARD, 4,
        {"STRING", "HEDGE", "HONEST", "ACTION", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 4, 5}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 0, 0},
        "The watchmaker examined the miniature golden gears and said they were —",
        "RIGHT ON THE SECOND"
    },
    {
        JUMBLE_HARD, 6,
        {"PENGUIN", "DOLPHIN", "INSIDE", "WINDFALL", "TREATY", "CARPET"},
        {{1, 2, 3, 4}, {0, 1, 2, 4}, {0, 1, 2, 3}, {1, 2, 3, 4}, {0, 2, 3, 4}, {5, 0, 0, 0}},
        {4, 4, 4, 4, 4, 1},
        "When the farmer doubled his harvest yield, his happy neighbor said —",
        "OUT-STANDING IN THE FIELD"
    },
    {
        JUMBLE_HARD, 6,
        {"DEVICE", "TRAVEL", "BLANKET", "CORNER", "NEEDLE", "STALE"},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 5}, {4, 0, 0, 0}},
        {4, 4, 4, 4, 4, 1},
        "The chemist loved working with helium and neon gas because they were —",
        "NOBLE AND NEVER REACTIVE"
    },
    {
        JUMBLE_HARD, 5,
        {"BRIGHT", "LIMIT", "DOLPHIN", "UNITY", "TRUTH", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 3, 4}, {0, 1, 3, 4}, {0, 3, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "When the duck paid cash for her expensive feather hat, she told them —",
        "PUT IT RIGHT ON MY \"BILL\""
    },
    {
        JUMBLE_HARD, 5,
        {"KITTEN", "MONKEY", "ALPHABET", "CHEER", "MERCY", ""},
        {{0, 1, 2, 3}, {0, 2, 3, 4}, {0, 3, 4, 5}, {0, 1, 2, 3}, {1, 2, 3, 4}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "The chess grandmaster took a bite of his fresh croissant and declared —",
        "CHECKMATE IN THE BAKERY"
    },
    {
        JUMBLE_HARD, 5,
        {"EQUAL", "WHISTLE", "NIGHT", "GLIDE", "TALENT", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 3, 5}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "When the pig won first prize at the state fair, his proud family said —",
        "SQUEALING WITH DELIGHT"
    },
    {
        JUMBLE_HARD, 5,
        {"BLANKET", "ROCKET", "SOLDIER", "UNITY", "MOTHER", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 2, 3, 4}, {4, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "The geologist took a vacation to the Grand Canyon because he found it —",
        "ROCK SOLID IN BEAUTY"
    },
    {
        JUMBLE_HARD, 5,
        {"STRIKE", "KINGDOM", "DAMAGE", "GREET", "CHEST", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {3, 4, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "When the runner finished the Boston Marathon, his proud coach said —",
        "MAKING GREAT STRIDES"
    },
    {
        JUMBLE_HARD, 5,
        {"MORNING", "GATHER", "SUNSHINE", "WEATHER", "IRONY", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 4, 5}, {1, 2, 4, 5}, {0, 1, 3, 4}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "The choir sang on top of the mountain ridge and reached —",
        "A HIGHER HARMONY IN TUNE"
    },
    {
        JUMBLE_HARD, 4,
        {"TIMBER", "AIRPORT", "EXPERT", "TORQUE", "", ""},
        {{0, 1, 2, 3}, {0, 2, 3, 4}, {0, 2, 3, 4}, {0, 1, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "When the detective found the stolen diamond watch, he said it was —",
        "ABOUT PROPER TIME"
    },
    {
        JUMBLE_HARD, 5,
        {"CABINET", "CAPTAIN", "LESSON", "UNICORN", "FROST", ""},
        {{0, 1, 2, 3}, {0, 1, 3, 4}, {0, 1, 2, 3}, {0, 1, 2, 4}, {2, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "The tailor sewed thirty tuxedo lapels in one evening and said it was —",
        "A SUITABLE OCCASION"
    },
    {
        JUMBLE_HARD, 5,
        {"LEOPARD", "HUNGRY", "SEAFOOD", "DRYER", "TUNER", ""},
        {{0, 2, 3, 4}, {0, 1, 2, 3}, {2, 3, 4, 5}, {0, 1, 2, 4}, {1, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "When the golfer sliced his tee shot into the woods, his caddie called it —",
        "A ROUGH ROUND OF PLAY"
    },
    {
        JUMBLE_HARD, 5,
        {"PAINTER", "PICTURE", "ENTRY", "THEORY", "FLEET", ""},
        {{0, 1, 2, 3}, {0, 2, 3, 4}, {0, 1, 2, 3}, {0, 2, 3, 5}, {0, 1, 2, 3}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "The doctor was calm in the crowded emergency room because he had —",
        "PLENTY OF TRUE PATIENCE"
    },
    {
        JUMBLE_HARD, 5,
        {"THEATER", "INSECT", "OCTOPUS", "SECTOR", "LOWER", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 4, 5}, {1, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "When the florist created a bridal bouquet of fifty red blossoms, she —",
        "ROSE TO THE OCCASION"
    },
    {
        JUMBLE_HARD, 5,
        {"GLACIER", "THUNDER", "SHIELD", "DOLPHIN", "HEDGE", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 4, 5}, {0, 1, 2, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 3, 0},
        "The pilot took off into the sunset without a single delay and had —",
        "HEAD HIGH IN THE CLOUDS"
    },
    {
        JUMBLE_HARD, 5,
        {"AIRPORT", "FEATHER", "THUNDER", "SHEER", "SCENE", ""},
        {{0, 2, 3, 4}, {0, 1, 2, 3}, {0, 1, 2, 4}, {0, 2, 3, 4}, {2, 4, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "When the diver found an oyster with five glowing pearls, it was —",
        "A TREASURE OF THE DEEP"
    },
    {
        JUMBLE_HARD, 4,
        {"MEADOW", "SWITCH", "AGAIN", "NOTCH", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 0, 0},
        "The carpenter measured the mahogany plank three times because he —",
        "SAW IT COMING AHEAD"
    },
    {
        JUMBLE_HARD, 5,
        {"WHISTLE", "MOTION", "MORNING", "GENTLE", "LAYER", ""},
        {{0, 1, 2, 4}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 1, 2, 3}, {0, 3, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "When the snowman sat beside the glowing campfire, he was —",
        "MELTING WITH EMOTION"
    },
    {
        JUMBLE_HARD, 5,
        {"PENGUIN", "FLIGHT", "NATION", "JOINT", "SCENT", ""},
        {{1, 2, 3, 4}, {0, 1, 2, 4}, {0, 1, 2, 3}, {1, 2, 3, 4}, {3, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "The baseball catcher held onto the pop fly with two strikes for —",
        "THE FINAL INNING OUT"
    },
    {
        JUMBLE_HARD, 5,
        {"JOURNEY", "WEIGHT", "BIRTH", "CABINET", "HUNGRY", ""},
        {{0, 1, 2, 3}, {0, 2, 3, 4}, {0, 1, 2, 3}, {2, 3, 4, 6}, {0, 2, 3, 5}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "When the candle shop opened three new franchises, the owner was —",
        "BURNING BRIGHT WITH JOY"
    },
    {
        JUMBLE_HARD, 5,
        {"GOLDEN", "FIREFLY", "CHIMNEY", "STOOL", "PENGUIN", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 4, 6}, {0, 2, 3, 4}, {2, 6, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "The painter finished the seaside landscape mural and said it was —",
        "DONE IN FLYING COLORS"
    },
    {
        JUMBLE_HARD, 5,
        {"SOCKET", "FORTUNE", "CAUSE", "SCREW", "MANNER", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {2, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "When the train conductor pulled into the grand terminal, he was —",
        "ON TRACK FOR SUCCESS"
    },
    {
        JUMBLE_HARD, 5,
        {"BALLOON", "BREED", "THUNDER", "FOREST", "SEASON", ""},
        {{0, 2, 3, 4}, {0, 1, 2, 3}, {0, 2, 3, 4}, {0, 1, 2, 3}, {0, 3, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "The author completed the suspenseful mystery novel and said —",
        "BOUND FOR BEST SELLER"
    },
    {
        JUMBLE_HARD, 5,
        {"THEATER", "HARMONY", "ALPHABET", "SEAFOOD", "STAND", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 3, 4}, {2, 3, 4, 5}, {1, 3, 4, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 3, 0},
        "When the owl gave a late night lecture at the forest university, it was —",
        "A HOOT AND A HALF TO HEAR"
    },
    {
        JUMBLE_HARD, 4,
        {"WINTER", "CASTLE", "TREASURE", "FUTURE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {1, 3, 4, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "The baker rolled out hundred pastry crusts by hand and was —",
        "IN A CRUST WE TRUST"
    },
    {
        JUMBLE_HARD, 5,
        {"VAMPIRE", "WHISTLE", "LEADER", "TREATY", "SKILL", ""},
        {{0, 1, 3, 4}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 1, 4, 5}, {2, 3, 4, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 3, 0},
        "When the dog found his buried bone in the backyard, he was —",
        "\"PAW\"-SITIVELY THRILLED"
    },
    {
        JUMBLE_HARD, 6,
        {"ALPHABET", "LEOPARD", "SEAFOOD", "DIRECT", "NOTICE", "STICK"},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {1, 0, 0, 0}},
        {4, 4, 4, 4, 4, 1},
        "The teacher loved teaching geometry because the proofs were —",
        "ALL SHAPED TO PERFECTION"
    },
    {
        JUMBLE_HARD, 6,
        {"EXTRA", "WEATHER", "CHIMNEY", "ENGINE", "SKETCH", "RIDDLE"},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {2, 3, 4, 5}, {2, 0, 0, 0}},
        {4, 4, 4, 4, 4, 1},
        "When the electric car plugged into the rapid charger, it was —",
        "CHARGED WITH EXCITEMENT"
    },
    {
        JUMBLE_HARD, 5,
        {"SERVE", "ALPHABET", "BOTTLE", "SWEET", "LEGAL", ""},
        {{0, 1, 2, 3}, {0, 2, 3, 4}, {0, 1, 2, 3}, {0, 2, 3, 4}, {1, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "The shoe designer created leather sneakers with gold lace and was —",
        "A STEP ABOVE THE REST"
    },
    {
        JUMBLE_HARD, 5,
        {"FARMER", "PICTURE", "NOTICE", "TENDER", "TUNER", ""},
        {{0, 2, 3, 4}, {0, 2, 3, 4}, {0, 1, 2, 4}, {0, 1, 2, 4}, {0, 2, 4, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 3, 0},
        "When the cat curled up on the sunny window sill, she was in —",
        "\"PURR\"-FECT CONTENTMENT"
    },
    {
        JUMBLE_HARD, 4,
        {"WEIGHT", "WHISTLE", "FLIGHT", "MOTION", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 3, 4}, {1, 2, 4, 5}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 0, 0},
        "The river guide paddled through the rapid white water and said —",
        "GOING WITH THE FLOW"
    },
    {
        JUMBLE_HARD, 5,
        {"RAINBOW", "WINDFALL", "ROBOT", "BELLY", "STUDY", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "When the jeweler cut the fifty carat diamond into facets, it was —",
        "BRILLIANT BEYOND WORDS"
    },
    {
        JUMBLE_HARD, 5,
        {"RABBIT", "MORNING", "GOING", "FLIGHT", "FUDGE", ""},
        {{0, 1, 2, 3}, {0, 1, 3, 4}, {0, 1, 2, 3}, {1, 3, 4, 5}, {2, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "The farmer planted rows of giant sunflowers and said they were —",
        "BLOOMING AND BRIGHT"
    },
    {
        JUMBLE_HARD, 4,
        {"BLANKET", "STRIKE", "JOCKEY", "GENTLE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 3, 4, 5}, {0, 1, 4, 5}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 0, 0},
        "When the actor nailed the difficult monologue on Broadway, he —",
        "BROKE A LEG IN STYLE"
    },
    {
        JUMBLE_HARD, 5,
        {"BLANKET", "KNIGHT", "PICTURE", "TREASURE", "PIECE", ""},
        {{1, 2, 3, 4}, {0, 1, 2, 3}, {0, 1, 3, 4}, {0, 1, 2, 6}, {1, 2, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "The mechanic tuned the sports car engine until it was —",
        "PURRING LIKE A KITTEN"
    },
    {
        JUMBLE_HARD, 5,
        {"WIZARD", "ZEBRA", "USAGE", "SCENT", "FORTUNE", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 3, 4}, {3, 6, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "When the bee hive produced ten gallons of clover honey, it was —",
        "CREATING A SWEET BUZZ"
    },
    {
        JUMBLE_HARD, 4,
        {"SILVER", "FINGER", "TREASURE", "NEEDLE", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {1, 2, 5, 6}, {1, 2, 5, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "The bookkeeper balanced thirty accounts to the penny and said —",
        "FIGURES NEVER LIE"
    },
    {
        JUMBLE_HARD, 5,
        {"YELLOW", "WINDOW", "TWELVE", "ROCKET", "SYMBOL", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {2, 4, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "When the clock maker repaired the tower clock, the town council said —",
        "TIMELY WORK WELL DONE"
    },
    {
        JUMBLE_HARD, 5,
        {"GIRAFFE", "PENGUIN", "TRAFFIC", "CABINET", "ACUTE", ""},
        {{0, 1, 2, 3}, {1, 2, 3, 4}, {0, 3, 4, 5}, {0, 3, 4, 5}, {2, 3, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 2, 0},
        "The gardener trimmed the hedge into a green dinosaur and was —",
        "CUTTING A FINE FIGURE"
    },
    {
        JUMBLE_HARD, 5,
        {"FROZEN", "CABINET", "CHARGE", "GENTLE", "SPHERE", ""},
        {{0, 1, 3, 4}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 2, 3, 5}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "When the sailboat rounded the windy cape, the crew reported —",
        "CATCHING A FRESH BREEZE"
    },
    {
        JUMBLE_HARD, 5,
        {"WHISPER", "PURPLE", "VILLAGE", "NEEDLE", "URBAN", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {2, 3, 4, 5}, {0, 1, 2, 4}, {3, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "The potter spun the wet clay into an elegant vase and said —",
        "SHAPING UP REAL WELL"
    },
    {
        JUMBLE_HARD, 4,
        {"WHISPER", "MONKEY", "JOURNEY", "ENEMY", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 4}, {1, 2, 5, 0}, {4, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 3, 1, 0, 0},
        "When the magician vanished from the locked trunk, the crowd said —",
        "NOW YOU SEE HIM"
    },
    {
        JUMBLE_HARD, 4,
        {"GATHER", "REGION", "THORN", "TENTH", "", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 0, 0},
        "The archer hit the center bullseye three times in a row for —",
        "RIGHT ON THE TARGET"
    },
    {
        JUMBLE_HARD, 5,
        {"ALPHABET", "CABINET", "SOLDIER", "REFER", "STAIR", ""},
        {{0, 1, 3, 4}, {0, 2, 3, 4}, {0, 1, 2, 3}, {0, 1, 2, 3}, {1, 3, 4, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 3, 0},
        "When the weaver finished the silk tapestry on the loom, it had —",
        "THREADS OF BRILLIANCE"
    },
    {
        JUMBLE_HARD, 4,
        {"ACTIVE", "TRAVEL", "STOCK", "HOLIDAY", "", ""},
        {{0, 1, 2, 3}, {0, 1, 3, 4}, {0, 1, 2, 4}, {1, 4, 6, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 3, 0, 0},
        "The ice hockey team won the championship game on home ice and —",
        "SKATED TO VICTORY"
    },
    {
        JUMBLE_HARD, 5,
        {"TARGET", "REGION", "THEATER", "SPHERE", "SEAFOOD", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {0, 2, 3, 4}, {0, 1, 4, 5}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "When the chef baked the golden soufflé without it deflating, it —",
        "ROSE TO GREATER HEIGHTS"
    },
    {
        JUMBLE_HARD, 5,
        {"TRAVEL", "SOLDIER", "CRYSTAL", "EASEL", "RIVAL", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 3, 4}, {1, 0, 0, 0}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 1, 0},
        "The astronomer discovered a new comet in the night sky and said —",
        "A STELLAR DISCOVERY"
    },
    {
        JUMBLE_HARD, 5,
        {"WHISTLE", "KITTEN", "HORIZON", "SOLDIER", "ENTER", ""},
        {{0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 3}, {0, 1, 2, 4}, {0, 1, 3, 4}, {0, 0, 0, 0}},
        {4, 4, 4, 4, 4, 0},
        "When the blacksmith forged the iron horseshoe, he told his apprentice —",
        "STRIKE WHILE IRON IS HOT"
    },
};

#endif // JUMBLE_DATASET_H
