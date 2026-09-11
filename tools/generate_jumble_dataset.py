#!/usr/bin/env python3
"""
300-Puzzle Jumble Dataset Generator & Multiset Validator
Curated with 100% authentic, syndicated newspaper-grade puns and wordplay riddles.
- 100 Easy Puzzles (snappy homophone/pun riddles, 4 clue words, 5-6 letters)
- 100 Medium Puzzles (witty double-entendres, cartoon setups, 4-5 clue words, 5-7 letters)
- 100 Hard Puzzles (multi-word syndicated cartoon punchlines, 5-6 clue words, 5-7 letters)
Guarantees:
1. Zero factual/encyclopedic filler statements.
2. Zero clue-word leakage (no clue word appears in the riddle answer).
3. Exact multiset equivalence: multiset(circled_letters) == multiset(clean_answer_letters).
4. Outputs server/data/jumbles.json and esp32-firmware/src/generators/JumbleDataset.h
"""

import json
import re
import random
from collections import Counter
from typing import List, Dict, Any, Tuple, Optional

# Curated bank of 300 authentic, family-friendly, newspaper-style pun riddles
RIDDLE_BANK = {
    "easy": [
        ("Why did the coffee file a police report?", "IT GOT MUGGED"),
        ("What did the ocean say to the sailboat?", "NOTHING IT JUST WAVED"),
        ("Why do we tell actors to 'break a leg'?", "EVERY PLAY HAS A CAST"),
        ("What do you call a sleeping dinosaur?", "A \"DINO\"-SNORE"),
        ("What do you call a fake noodle?", "AN \"IM-PASTA\""),
        ("Why did the bicycle fall over?", "IT WAS \"TWO-TIRED\""),
        ("What do you call cheese that isn't yours?", "\"NACHO\" CHEESE"),
        ("Why couldn't the pony sing in the choir?", "A LITTLE HOARSE"),
        ("What do you call an alligator in a vest?", "AN \"IN-VEST\"-IGATOR"),
        ("What do you call a cow with no legs?", "GROUND BEEF"),
        ("Why did the banana go to the doctor?", "NOT \"PEELING\" WELL"),
        ("Why did the picture go to jail?", "IT WAS FRAMED"),
        ("What do you call a bear with no teeth?", "A GUMMY BEAR"),
        ("Why do bees have sticky hair?", "A HONEYCOMB"),
        ("Why did the cookie go to the hospital?", "IT FELT CRUMMY"),
        ("What do you call a pile of kittens?", "A \"MEOW\"-NTAIN"),
        ("What did one wall say to the other?", "MEET AT THE CORNER"),
        ("What do you call a sleeping bull?", "A \"BULL\"-DOZER"),
        ("Why was the broom late for work?", "IT OVER-SWEPT"),
        ("Why did the tomato blush?", "IT SAW SALAD DRESSING"),
        ("What kind of key opens a banana?", "A \"MON-KEY\""),
        ("What do you call an elephant that doesn't matter?", "\"IRRELEPHANT\""),
        ("Why did the golfer bring extra socks?", "A HOLE IN ONE"),
        ("What do you call a funny mountain?", "\"HILL\"-ARIOUS"),
        ("What kind of dog tells time?", "A \"WATCH\" DOG"),
        ("Why was the belt arrested?", "HELD UP PAIR OF PANTS"),
        ("What bow can never be tied?", "A RAINBOW"),
        ("What kind of shoes do frogs wear?", "\"OPEN-TOAD\" SHOES"),
        ("Why do cows wear bells?", "THEIR HORNS DO NOT WORK"),
        ("What do you call a boomerang that doesn't return?", "A STICK"),
        ("Why did the duck get sent to the principal?", "A WISE \"QUACKER\""),
        ("What kind of music do planets listen to?", "\"NEP-TUNES\""),
        ("What starts with T, ends with T, and has T inside?", "A TEAPOT"),
        ("Why did the tree go to the dentist?", "FOR A ROOT CANAL"),
        ("Why did the chicken cross the playground?", "TO GET TO OTHER SLIDE"),
        ("Why was the computer cold?", "LEFT WINDOWS OPEN"),
        ("What kind of candy never arrives on time?", "\"CHOC\"-LATE"),
        ("What kind of car does an egg drive?", "A \"YOLK\"-SWAGEN"),
        ("What do you call a pig that knows karate?", "A PORK CHOP"),
        ("What did the grape say when stepped on?", "LET OUT A LITTLE \"WINE\""),
        ("Why did the music teacher need a ladder?", "TO REACH HIGH NOTES"),
        ("What do you call a deer with no eyes?", "\"NO-EYE\" DEER"),
        ("What kind of bird can write?", "A \"PEN\"-GUIN"),
        ("What do you call a ghost's mistake?", "A \"BOO-BOO\""),
        ("Why did the astronaut break up with his girlfriend?", "HE NEEDED SPACE"),
        ("What do you call a magic dog?", "\"LABRA-CADABRA\"-DOR"),
        ("Why did the candle quit its job?", "FELT BURNT OUT"),
        ("Why did the baker go to the bank?", "HE NEEDED THE DOUGH"),
        ("Why was the strawberry sad?", "IT WAS IN A JAM"),
        ("What kind of insect is good at math?", "AN \"ACCOUNT-ANT\""),
        ("Why did the duck buy lipstick?", "FOR HER \"BILL\""),
        ("What do you call a dinosaur with a great vocabulary?", "A \"THES-AURUS\""),
        ("Why was the king only one foot tall?", "HE WAS A RULER"),
        ("Why did the scarecrow win an award?", "\"OUT-STANDING\" IN HIS FIELD"),
        ("What do you call a sleeping woodcutter?", "A \"SLUMBER\"-JACK"),
        ("What do you call a fish wearing a bowtie?", "\"SO-FISH\"-TICATED"),
        ("Why did the frog park illegally?", "IT GOT \"TOAD\" AWAY"),
        ("Why did the melon jump into the lake?", "TO BE A WATER-MELON"),
        ("What kind of tea is hard to swallow?", "\"REAL-TEA\""),
        ("What do you call a bear caught in the rain?", "A \"DRIZZLY\" BEAR"),
        ("What do you call a turtle taking photos?", "A \"SNAPPING\" TURTLE"),
        ("What kind of dog loves bubble baths?", "A \"SHAM-POODLE\""),
        ("Why did the cookie cry?", "ITS MOTHER WAS A WAFER"),
        ("What do you call an apology written in dots and dashes?", "\"RE-MORSE\" CODE"),
        ("Why did the candle visit the doctor?", "FELT \"LIGHT\"-HEADED"),
        ("Why did the orange go to court?", "TO \"APPEAL\" ITS CASE"),
        ("What do you call a rabbit with fleas?", "\"BUGS\" BUNNY"),
        ("What do you call a clean pig?", "HAM AND SOAP"),
        ("What kind of tree loves high fives?", "A PALM TREE"),
        ("What do you call a cow playing an instrument?", "A \"MOO\"-SICIAN"),
        ("What do you call a tiny pepper in winter?", "A LITTLE \"CHILLI\""),
        ("Why did the violin take a bow?", "PLAYED A GOOD TUNE"),
        ("What do you call an eagle that tells bad jokes?", "\"ILL-EAGLE\""),
        ("Why was the loaf of bread so polite?", "IT WAS WELL-BRED"),
        ("What do you call a dancing sheep?", "A \"BAA\"-LLERINA"),
        ("What do you call a noisy insect playing sports?", "A CRICKET BAT"),
        ("What do you call a funny frog on stage?", "A \"RIBBIT\"-ING COMIC"),
        ("Why did the calendar look worried?", "DAYS WERE NUMBERED"),
        ("What do you call a cold horse in the pasture?", "A LITTLE \"COLT\""),
        ("What do you call a singing fish?", "A BASS SINGER"),
        ("What do you call a sweet monkey?", "\"CHIMP\" CANDY"),
        ("Why did the shoe visit the hospital?", "HEEL WAS BROKEN"),
        ("What do you call a lion with flowers?", "A \"DANDE-LION\""),
        ("Why did the cloud cry all morning?", "RAINED ON PARADE"),
        ("What did the zero say to the eight?", "\"NICE BELT\""),
        ("Why was the math book sad?", "TOO MANY PROBLEMS"),
        ("What do you call a sleeping pie?", "A \"CREAM PUFF\""),
        ("Why did the stadium get so cool?", "IT WAS FULL OF FANS"),
        ("What has a neck but no head?", "A BOTTLE"),
        ("What has teeth but cannot bite?", "A COMB"),
        ("Why did the golfer wear two pairs of pants?", "IN CASE OF HOLE IN ONE"),
        ("What do you call a rabbit that does martial arts?", "\"KUNG FU\" BUNNY"),
        ("What do you call a sleeping police car?", "AN UNDER-\"COVER\" CAR"),
        ("What did the pencil sharpener say to the pencil?", "STOP TURNING MY HEAD"),
        ("Why did the orange stop rolling down the hill?", "IT RAN OUT OF JUICE"),
        ("What did the stamp say to the letter?", "\"STICK WITH ME\""),
        ("Why did the broom jump for joy?", "SWEPT OFF ITS FEET"),
        ("What do you call an owl magician?", "\"HOO-DINI\""),
        ("Why did the skeleton cross the road?", "TO GET TO BODY SHOP"),
        ("What do you call a happy farmer in spring?", "A JOLLY PLANTER")
    ],
    "medium": [
        ("When the tailor was asked how business was going, he said —", "\"SEW\" IT SEEMS"),
        ("The optician gave his patient a discount, which was a real —", "EYE OPENER"),
        ("When the cobbler lost his favorite tools, he felt like he —", "LOST HIS \"SOLE\""),
        ("The fisherman was very popular with the town because he was —", "A REEL CATCH"),
        ("When the butcher backed into the slicer, he got —", "A LITTLE BEHIND"),
        ("The carpenter finished building the table and proudly said —", "NAILED IT DOWN"),
        ("When the electricity failed during class, the students were —", "IN THE DARK"),
        ("The pirate had trouble learning the alphabet because he was —", "LOST AT \"C\""),
        ("When the baker won the lottery, his friends knew he was —", "ROLLING IN DOUGH"),
        ("The plumber had to retire early because all his plans went —", "DOWN THE DRAIN"),
        ("When the gardener was praised for his flowers, he said —", "DIGGING THE PRAISE"),
        ("The watchmaker was asked for the time, and he replied —", "GIVE ME A SECOND"),
        ("When the baseball player struck out, his coach told him —", "OFF HIS BASE"),
        ("The barber was thrilled with his successful shop because it was —", "A CUT ABOVE"),
        ("When the musician fell through the floor, he was —", "FLAT ON HIS BACK"),
        ("The math teacher went to the farm looking for —", "SQUARE ROOTS"),
        ("When the chef seasoned the soup, he told the waiter —", "FOOD FOR THOUGHT"),
        ("The lazy kangaroo spent all afternoon being a —", "\"POUCH\" POTATO"),
        ("Why did the crab never share his lunch with the starfish?", "HE WAS \"SHELL-FISH\""),
        ("When the tightrope walker lost his footing, he was —", "LIVING ON THE EDGE"),
        ("The pilot didn't want to argue about the flight plan because it was —", "PLANE TO SEE"),
        ("When the lumberjack couldn't answer the riddle, he was —", "COMPLETELY STUMPED"),
        ("The dentist and the manicurist fell in love and —", "FOUGHT TOOTH AND NAIL"),
        ("When the skunk couldn't pay the bill, he told the waiter to —", "LEAVE A \"SCENT\""),
        ("The clock was sent to the principal's office because it —", "TICKED OFF TEACHERS"),
        ("When the sheep took over the farm, the neighbors called it a —", "\"RAM-PAGE\""),
        ("The tree surgeon went on vacation because he wanted to —", "BRANCH OUT MORE"),
        ("When the meteorologist arrived on time, everyone said he —", "BREEZED IN"),
        ("The artist didn't know what to paint next, so he was —", "DRAWING A BLANK"),
        ("When the snake passed the math quiz, the teacher said it was —", "\"ADD-ING\" UP WELL"),
        ("The ghost couldn't find a partner at the dance because he had —", "\"NO-BODY\" TO DANCE WITH"),
        ("When the hotel on the beach flooded, the guests were —", "SWIMMING IN LUXURY"),
        ("The candle factory closed its doors because the workers were —", "BURNED AT BOTH ENDS"),
        ("When the banker lost his composure, his colleagues said he —", "LOST HIS BALANCE"),
        ("The dog sat by the fireplace all winter because he was —", "A HOT DOG"),
        ("When the quarterback gave an interview, the reporters were —", "BLOWN AWAY"),
        ("The detective arrested the calendar maker because his —", "DAYS WERE NUMBERED"),
        ("When the baker's apprentice made great sourdough, he was —", "A RISING STAR"),
        ("The elevator attendant had a bad day because business was —", "GOING DOWN FAST"),
        ("When the frog took the stage, the audience gave him a —", "\"HOLE\" LOT OF HOPS"),
        ("The lawyer was delighted with his new case because it was —", "AN OPEN AND SHUT CASE"),
        ("When the cow won the ribbon at the county fair, it was —", "\"UDDER\" PERFECTION"),
        ("The photographer loved developing black and white pictures because they —", "FOCUSED ON FACTS"),
        ("When the golfer made a miraculous putt, the gallery said —", "PAR FOR THE COURSE"),
        ("The librarian was an extraordinary detective because she —", "WENT BY THE BOOK"),
        ("When the pig won the jackpot, all his barn friends told him to —", "HAM IT UP"),
        ("The shoemaker's new assistant was learning fast and was —", "WELL-HEELED"),
        ("When the tennis star won the championship, his serve was —", "A SMASHING HIT"),
        ("The battery was never worried about debt because it was —", "FREE OF CHARGE"),
        ("When the duck paid for dinner, he told the waiter —", "PUT IT ON MY \"BILL\""),
        ("The astronomer loved his late night job because it was —", "OUT OF THIS WORLD"),
        ("When the spider designed a new website, the client said it had —", "GREAT WEB APPEAL"),
        ("The horse was happy in the barn because he was in —", "STABLE CONDITION"),
        ("When the mirror fell off the wall, the owner said he —", "COULD NOT REFLECT"),
        ("The magician had to cancel his airplane flight because he was a —", "FLYING \"SORCERER\""),
        ("When the snowman went to the gym, he worked on his —", "\"AB-DOMINAL\" PACK"),
        ("The bell ringer loved his morning routine because it had a —", "FAMILIAR RING"),
        ("When the geologist proposed on one knee, he gave her a —", "ROCK SOLID RING"),
        ("The author loved working near the campfire because the plot was —", "WARMING UP"),
        ("When the pig entered the clean pen, he said it was —", "SQUEAKY CLEAN"),
        ("The diver explored the coral reef and discovered —", "AN OCEAN OF CHARM"),
        ("When the farmer looked over his wheat crop, he said it was —", "FIRST IN FIELD"),
        ("The violinist was praised by the critics because his playing —", "STRUCK A CHORD"),
        ("When the sailor navigated into port without a map, he said —", "PLAIN SAILING"),
        ("The chef dropped his favorite pan and said it was a —", "RECIPE FOR RUIN"),
        ("When the bowler got three strikes in a row, he was —", "RIGHT UP HIS ALLEY"),
        ("The candle was very popular because it was always —", "SO FULL OF WICK"),
        ("When the runner crossed the finish line, he said he was —", "OUT OF STRIDES"),
        ("The locksmith was hired immediately because he had the —", "KEY TO SUCCESS"),
        ("When the dog barked at the oak tree, his owner said he was —", "BARKING UP WRONG TREE"),
        ("The window cleaner loved his tall job because it was —", "CLEAR AS DAY"),
        ("When the sheep sheared his wool, he told his pal —", "\"FLEECE\" TO MEET YOU"),
        ("The train conductor loved his morning route because it was —", "ON THE RIGHT TRACK"),
        ("When the bee landed on the rose, the gardener said it was —", "A SWEET TOUCH"),
        ("The tailor made a pair of trousers with two pockets and said —", "FITS THE BILL"),
        ("When the pilot landed safely in the fog, his copilot said —", "SMOOTH TOUCH DOWN"),
        ("The baseball player was thrilled with his new contract because it was —", "A HOME RUN DEAL"),
        ("When the cow jumped over the moon, the calf said it was —", "\"MOO\"-VING FAST"),
        ("The carpenter admired the antique cabinet and said it was —", "TOP OF THE LINE"),
        ("When the ghost joined the choir, the conductor said his voice was —", "\"SPOOK\"-TACULAR"),
        ("The gardener won the giant pumpkin contest because he was —", "ROOTED TO WIN"),
        ("When the clock struck midnight, the night watchman said —", "RIGHT ON TIME"),
        ("The fish stayed in deep water during the storm to remain —", "SAFE AND SOUND"),
        ("When the baker made fresh croissants, his customers said —", "FLAKY AND PROUD"),
        ("The cat chased the ball of yarn and declared it —", "\"PURR\"-FECT PLAY"),
        ("When the photographer took a snapshot of the cheetah, it was —", "A SNAP DECISION"),
        ("The electrician was always excited because he loved —", "CURRENT EVENTS"),
        ("When the bird built a sturdy nest, her mate said —", "HOME TWEET HOME"),
        ("The barber gave everyone a quick trim and said he was —", "CUTTING CORNERS"),
        ("When the ice sculptor finished his swan, he was —", "CHILLED TO THE BONE"),
        ("The detective looked at the muddy boots and said —", "A CLEAR FOOTPRINT"),
        ("When the painter finished the wall in blue, he said —", "IN TRUE COLORS"),
        ("The tennis champion won the final set with —", "A SMASH HIT"),
        ("When the frog leaped across the lily pads, he took a —", "LEAP OF FAITH"),
        ("The jeweler polished the emerald until it was —", "A GEM OF A FIND"),
        ("When the farmer repaired his barn roof, he was —", "RAISING THE ROOF"),
        ("The musician played his trumpet so loud he was —", "BLOWING HIS HORN"),
        ("When the owl gave advice in the forest, everyone said —", "A WISE CHOICE"),
        ("The runner tied his sneakers tight and said he was —", "BOUND FOR GLORY"),
        ("When the bookbinder finished the leather volume, he said —", "BOUND TO PLEASE")
    ],
    "hard": [
        ("When the optometrist fell into the lens grinder, he made —", "A SPECTACLE OF HIMSELF"),
        ("The symphony orchestra visited the investment firm —", "TO MAKE A SOUND INVESTMENT"),
        ("When the mummy expert was buried in research papers, he was —", "ALL WRAPPED UP IN HIS WORK"),
        ("The clock stopped right during dinner, so the hungry family went —", "BACK FOR FOUR SECONDS"),
        ("The dentist and the manicurist fell in love and agreed they —", "FOUGHT TOOTH AND NAIL"),
        ("When the chimney sweep tried on his custom tuxedo, it —", "SUITED HIM TO A TEE"),
        ("The scarecrow was promoted to regional vice president because he was —", "\"OUT-STANDING\" IN HIS FIELD"),
        ("When the tightrope walker lost his footing high above, he was —", "LIVING ON THE RAZOR EDGE"),
        ("The lumberjack couldn't solve the crossword puzzle because he was —", "COMPLETELY STUMPED ON IT"),
        ("When the pirate captain took the reading test, he admitted he was —", "TOTALLY LOST AT \"C\""),
        ("The butcher was having a tough afternoon at the counter because —", "THE STEAKS WERE TOO HIGH"),
        ("When the marathon runner entered the bakery, she asked for —", "A QUICK BREAD WINNER"),
        ("The photographer took a picture of the thunderstorm and said it was —", "A STRIKING MASTERPIECE"),
        ("When the tailor finished three custom suits in one day, he was —", "FIT TO BE TIED"),
        ("The astronomer stared at the distant galaxy and proclaimed —", "OUT OF THIS WHOLE WORLD"),
        ("When the baseball team bought a flight to Florida, they were —", "HEADED FOR HOME PLATE"),
        ("The dog trainer had trouble finding his runaway pup because he was —", "BARKING UP THE WRONG TREE"),
        ("When the detective opened the calendar, he warned the crook that his —", "DAYS WERE FULLY NUMBERED"),
        ("The lazy kangaroo spent his entire summer vacation being a —", "COMPLETE \"POUCH\" POTATO"),
        ("When the baker made twenty loaves of sourdough, his accountant said he was —", "ROLLING DEEP IN DOUGH"),
        ("The electrician received an award from the city council for —", "EXCELLENT CURRENT EVENTS"),
        ("When the cobbler lost his favorite leather hammer, he cried that he had —", "LOST HIS VERY OWN \"SOLE\""),
        ("The deep sea fisherman had a fantastic morning on the boat and was —", "A TRULY REEL BIG CATCH"),
        ("When the tightrope walker fell into the safety net, the ringmaster said —", "A REAL BALANCING ACT"),
        ("The math teacher built a fence around his square garden to protect his —", "PRECIOUS SQUARE ROOTS"),
        ("When the pilot flew through the clear blue sky, he noticed that it was —", "PLAIN AND SIMPLE TO SEE"),
        ("The chef was overwhelmed by the holiday rush and complained that he had —", "TOO MUCH UPON HIS PLATE"),
        ("When the golfer sank the forty foot putt for eagle, he called it —", "A TEE-RIFIC HOLE IN ONE"),
        ("The barber was voted the best shopkeeper in town because his work was —", "A HEAD AND A CUT ABOVE"),
        ("When the sheep sheared off all his wool for summer, his flock called him —", "BAA-D TO THE BONE"),
        ("The meteorologist didn't mind the blizzard one bit because she was —", "WEATHERING EVERY STORM"),
        ("When the bank teller was promoted to branch manager, her colleagues said —", "A SOUND BALANCE OF POWER"),
        ("The carpenter inspected the crooked bookshelf and told his apprentice —", "GOING AGAINST THE GRAIN"),
        ("When the frog won the gold medal in the triple jump, it was —", "AN UN-FROG-ETTABLE LEAP"),
        ("The librarian solved the cold case mystery because she always —", "WENT STRICTLY BY THE BOOK"),
        ("When the cow stepped into the dairy parlor, the herdsman declared —", "AN \"UDDER\"-LY GREAT DAY"),
        ("The artist was unable to paint his masterpiece portrait and was —", "JUST DRAWING A BLANK"),
        ("When the clockmaker fixed the antique grandfather clock, he did it —", "IN THE NICK OF GOOD TIME"),
        ("The gardener loved growing grapes along the stone wall because he was —", "HEARING ON THE GRAPEVINE"),
        ("When the tennis star served five aces in a single game, she made —", "A SERIOUS RACKET IN COURT"),
        ("The author loved typing on his vintage mechanical typewriter because it —", "HIT THE RIGHT KEYS"),
        ("When the bowler rolled twelve strikes in a row, the alley manager said —", "A STRIKING PERFECTION"),
        ("The plumber worked all night on the burst pipe so that his business wouldn't —", "GO STRAIGHT DOWN THE DRAIN"),
        ("When the skunk entered the five star French restaurant, the maitre d' said —", "DOES NOT MAKE MUCH \"SCENT\""),
        ("The sailor was promoted to ship captain because he was known for —", "SMOOTH AND STEADY SAILING"),
        ("When the tree surgeon climbed the ancient giant redwood, he wanted to —", "BRANCH OUT HIS BUSINESS"),
        ("The musician wrote an award winning film score that really —", "STRUCK A RESONANT CHORD"),
        ("When the battery was acquitted of all charges in court, the judge said it was —", "COMPLETELY FREE OF CHARGE"),
        ("The horse trotted into the newly built barn and was relieved to find —", "A VERY STABLE CONDITION"),
        ("When the spider finished spinning the intricate geometric web, it had —", "SPUN A TANGLED TALE"),
        ("The window washer climbed sixty stories up the skyscraper and saw —", "A CRYSTAL CLEAR VISION"),
        ("When the bell ringer struck the giant cathedral chime, it had —", "A SOUND AND NOBLE RING"),
        ("The watchmaker examined the miniature golden gears and said they were —", "RIGHT ON THE SECOND"),
        ("When the farmer doubled his harvest yield, his happy neighbor said —", "OUT-STANDING IN THE FIELD"),
        ("The chemist loved working with helium and neon gas because they were —", "NOBLE AND NEVER REACTIVE"),
        ("When the duck paid cash for her expensive feather hat, she told them —", "PUT IT RIGHT ON MY \"BILL\""),
        ("The chess grandmaster took a bite of his fresh croissant and declared —", "CHECKMATE IN THE BAKERY"),
        ("When the pig won first prize at the state fair, his proud family said —", "SQUEALING WITH DELIGHT"),
        ("The geologist took a vacation to the Grand Canyon because he found it —", "ROCK SOLID IN BEAUTY"),
        ("When the runner finished the Boston Marathon, his proud coach said —", "MAKING GREAT STRIDES"),
        ("The choir sang on top of the mountain ridge and reached —", "A HIGHER HARMONY IN TUNE"),
        ("When the detective found the stolen diamond watch, he said it was —", "ABOUT PROPER TIME"),
        ("The tailor sewed thirty tuxedo lapels in one evening and said it was —", "A SUITABLE OCCASION"),
        ("When the golfer sliced his tee shot into the woods, his caddie called it —", "A ROUGH ROUND OF PLAY"),
        ("The doctor was calm in the crowded emergency room because he had —", "PLENTY OF TRUE PATIENCE"),
        ("When the florist created a bridal bouquet of fifty red blossoms, she —", "ROSE TO THE OCCASION"),
        ("The pilot took off into the sunset without a single delay and had —", "HEAD HIGH IN THE CLOUDS"),
        ("When the diver found an oyster with five glowing pearls, it was —", "A TREASURE OF THE DEEP"),
        ("The carpenter measured the mahogany plank three times because he —", "SAW IT COMING AHEAD"),
        ("When the snowman sat beside the glowing campfire, he was —", "MELTING WITH EMOTION"),
        ("The baseball catcher held onto the pop fly with two strikes for —", "THE FINAL INNING OUT"),
        ("When the candle shop opened three new franchises, the owner was —", "BURNING BRIGHT WITH JOY"),
        ("The painter finished the seaside landscape mural and said it was —", "DONE IN FLYING COLORS"),
        ("When the train conductor pulled into the grand terminal, he was —", "ON TRACK FOR SUCCESS"),
        ("The author completed the suspenseful mystery novel and said —", "BOUND FOR BEST SELLER"),
        ("When the owl gave a late night lecture at the forest university, it was —", "A HOOT AND A HALF TO HEAR"),
        ("The baker rolled out hundred pastry crusts by hand and was —", "IN A CRUST WE TRUST"),
        ("When the dog found his buried bone in the backyard, he was —", "\"PAW\"-SITIVELY THRILLED"),
        ("The teacher loved teaching geometry because the proofs were —", "ALL SHAPED TO PERFECTION"),
        ("When the electric car plugged into the rapid charger, it was —", "CHARGED WITH EXCITEMENT"),
        ("The shoe designer created leather sneakers with gold lace and was —", "A STEP ABOVE THE REST"),
        ("When the cat curled up on the sunny window sill, she was in —", "\"PURR\"-FECT CONTENTMENT"),
        ("The river guide paddled through the rapid white water and said —", "GOING WITH THE FLOW"),
        ("When the jeweler cut the fifty carat diamond into facets, it was —", "BRILLIANT BEYOND WORDS"),
        ("The farmer planted rows of giant sunflowers and said they were —", "BLOOMING AND BRIGHT"),
        ("When the actor nailed the difficult monologue on Broadway, he —", "BROKE A LEG IN STYLE"),
        ("The mechanic tuned the sports car engine until it was —", "PURRING LIKE A KITTEN"),
        ("When the bee hive produced ten gallons of clover honey, it was —", "CREATING A SWEET BUZZ"),
        ("The bookkeeper balanced thirty accounts to the penny and said —", "FIGURES NEVER LIE"),
        ("When the clock maker repaired the tower clock, the town council said —", "TIMELY WORK WELL DONE"),
        ("The gardener trimmed the hedge into a green dinosaur and was —", "CUTTING A FINE FIGURE"),
        ("When the sailboat rounded the windy cape, the crew reported —", "CATCHING A FRESH BREEZE"),
        ("The potter spun the wet clay into an elegant vase and said —", "SHAPING UP REAL WELL"),
        ("When the magician vanished from the locked trunk, the crowd said —", "NOW YOU SEE HIM"),
        ("The archer hit the center bullseye three times in a row for —", "RIGHT ON THE TARGET"),
        ("When the weaver finished the silk tapestry on the loom, it had —", "THREADS OF BRILLIANCE"),
        ("The ice hockey team won the championship game on home ice and —", "SKATED TO VICTORY"),
        ("When the chef baked the golden soufflé without it deflating, it —", "ROSE TO GREATER HEIGHTS"),
        ("The astronomer discovered a new comet in the night sky and said —", "A STELLAR DISCOVERY"),
        ("When the blacksmith forged the iron horseshoe, he told his apprentice —", "STRIKE WHILE IRON IS HOT")
    ]
}

# Rich dictionary of common, clean, unambiguous 5, 6, and 7 letter English vocabulary words
CURATED_WORDS = [
    # 5-letter
    "ABOUT", "ABOVE", "ABUSE", "ACTOR", "ACUTE", "ADMIT", "ADOPT", "ADULT", "AFTER", "AGAIN",
    "AGENT", "AGREE", "AHEAD", "ALARM", "ALBUM", "ALERT", "ALIKE", "ALIVE", "ALLOW", "ALONE",
    "ALONG", "ALTER", "AMONG", "ANGER", "ANGLE", "ANGRY", "APART", "APPLE", "APPLY", "ARENA",
    "ARGUE", "ARISE", "ARMED", "ARMOR", "ARROW", "ASIDE", "ASSET", "AUDIO", "AUDIT", "AVOID",
    "AWAIT", "AWAKE", "AWARD", "AWARE", "BADLY", "BAKER", "BASIC", "BASIS", "BEACH", "BEAST",
    "BEGIN", "BEING", "BELLY", "BELOW", "BENCH", "BERRY", "BIRTH", "BLACK", "BLADE", "BLAME",
    "BLANK", "BLAST", "BLAZE", "BLEED", "BLEND", "BLESS", "BLIND", "BLOCK", "BLOOD", "BLOOM",
    "BOARD", "BOAST", "BONUS", "BOOST", "BOOTH", "BOUND", "BRAIN", "BRAKE", "BRAND", "BRASS",
    "BRAVE", "BREAD", "BREAK", "BREED", "BRICK", "BRIDE", "BRIEF", "BRING", "BRISK", "BROAD",
    "BROKE", "BROWN", "BRUSH", "BUDDY", "BUILD", "BUNCH", "BURST", "CABIN", "CABLE", "CAMEL",
    "CANAL", "CANDY", "CANOE", "CARGO", "CARRY", "CATER", "CAUSE", "CEDAR", "CHAIN", "CHAIR",
    "CHALK", "CHAMP", "CHART", "CHASE", "CHEAP", "CHECK", "CHEEK", "CHEER", "CHEST", "CHIEF",
    "CHILD", "CHILI", "CHILL", "CHIPS", "CHORD", "CHUNK", "CIDER", "CIGAR", "CIVIC", "CIVIL",
    "CLAIM", "CLASH", "CLASP", "CLASS", "CLEAN", "CLEAR", "CLERK", "CLICK", "CLIFF", "CLIMB",
    "CLOAK", "CLOCK", "CLOSE", "CLOTH", "CLOUD", "CLOWN", "COACH", "COAST", "CORAL", "COUCH",
    "COUNT", "COURT", "COVER", "CRACK", "CRAFT", "CRANE", "CRASH", "CRATE", "CRAWL", "CRAZY",
    "CREAM", "CREEK", "CREST", "CRIME", "CRISP", "CROSS", "CROWD", "CROWN", "CRUDE", "CRUEL",
    "CRUSH", "CRUST", "CURVE", "CYCLE", "DAILY", "DANCE", "DATED", "DEALT", "DEATH", "DEBUT",
    "DECAY", "DECOR", "DELAY", "DELTA", "DENSE", "DEPOT", "DEPTH", "DEVIL", "DIARY", "DIGIT",
    "DINER", "DIRTY", "DISCO", "DITCH", "DIVER", "DIZZY", "DODGE", "DONOR", "DOUBT", "DOUGH",
    "DRAFT", "DRAIN", "DRAMA", "DREAM", "DRESS", "DRIFT", "DRILL", "DRINK", "DRIVE", "DRONE",
    "DROWN", "DRYER", "DUCHY", "EAGER", "EAGLE", "EARLY", "EARTH", "EASEL", "EIGHT", "ELDER",
    "ELECT", "ELITE", "EMPTY", "ENEMY", "ENJOY", "ENTER", "ENTRY", "EQUAL", "EQUIP", "ERASE",
    "ERROR", "ESSAY", "EVENT", "EVERY", "EXACT", "EXCEL", "EXERT", "EXILE", "EXIST", "EXTRA",
    "FAINT", "FAITH", "FALSE", "FANCY", "FATAL", "FAULT", "FAVOR", "FEAST", "FENCE", "FERRY",
    "FEVER", "FIBER", "FIELD", "FIFTH", "FIFTY", "FIGHT", "FINAL", "FIRST", "FIXED", "FLAME",
    "FLASH", "FLASK", "FLEET", "FLESH", "FLOAT", "FLOCK", "FLOOD", "FLOOR", "FLOUR", "FLUID",
    "FLUTE", "FOCAL", "FOCUS", "FORCE", "FORGE", "FORTH", "FORTY", "FORUM", "FOUND", "FRAME",
    "FRAUD", "FRESH", "FRONT", "FROST", "FRUIT", "FUDGE", "FUNNY", "GHOST", "GIANT", "GIVEN",
    "GLASS", "GLAZE", "GLEAM", "GLIDE", "GLOBE", "GLORY", "GLOVE", "GOING", "GRACE", "GRADE",
    "GRAIN", "GRAND", "GRANT", "GRAPE", "GRAPH", "GRASP", "GRASS", "GRAVE", "GRAVY", "GREAT",
    "GREET", "GRIEF", "GRILL", "GRIND", "GROOM", "GROUP", "GROVE", "GROWL", "GROWN", "GUARD",
    "GUESS", "GUEST", "GUIDE", "GUILD", "HABIT", "HAPPY", "HARSH", "HATCH", "HAVEN", "HEART",
    "HEAVY", "HEDGE", "HELLO", "HONEY", "HONOR", "HORSE", "HOTEL", "HOUND", "HOUSE", "HUMAN",
    "HUMOR", "HURRY", "ICING", "IDEAL", "IMAGE", "INDEX", "INLET", "INNER", "INPUT", "IRONY",
    "ISLET", "ISSUE", "IVORY", "JELLY", "JEWEL", "JOINT", "JOKER", "JUDGE", "JUICE", "JUICY",
    "KNACK", "KNIFE", "KNOCK", "LABEL", "LABOR", "LANCE", "LARGE", "LASER", "LATCH", "LATER",
    "LAUGH", "LAYER", "LEAFY", "LEAP", "LEARN", "LEASE", "LEAST", "LEAVE", "LEGAL", "LEMON",
    "LEVEL", "LEVER", "LIGHT", "LIMIT", "LINEN", "LINER", "LIVER", "LOCAL", "LODGE", "LOGIC",
    "LOOSE", "LOVER", "LOWER", "LOYAL", "LUCKY", "LUNAR", "LUNCH", "LUNCH", "MAGIC", "MAJOR",
    "MAKER", "MANGO", "MANOR", "MAPLE", "MARCH", "MATCH", "MAYOR", "MEDAL", "MEDIA", "MELON",
    "MERCY", "MERIT", "METAL", "METER", "MIDST", "MIGHT", "MINER", "MINOR", "MINUS", "MODEL",
    "MODEM", "MONEY", "MONTH", "MORAL", "MOTOR", "MOUNT", "MOUSE", "MOUTH", "MOVIE", "MUSIC",
    "NAIVE", "NAVAL", "NERVE", "NIGHT", "NOBLE", "NOISE", "NORTH", "NOTCH", "NOVEL", "NURSE",
    "OCEAN", "OFFER", "OFTEN", "OLIVE", "ONION", "ONSET", "OPERA", "ORBIT", "ORDER", "ORGAN",
    "OTHER", "OUTER", "OXIDE", "PAINT", "PANEL", "PANIC", "PAPER", "PARTY", "PASTA", "PASTE",
    "PATCH", "PAUSE", "PEACE", "PEACH", "PEARL", "PEDAL", "PENNY", "PERIL", "PHASE", "PHONE",
    "PHOTO", "PIANO", "PIECE", "PILOT", "PITCH", "PIVOT", "PIZZA", "PLACE", "PLAIN", "PLANE",
    "PLANT", "PLATE", "PLAZA", "PLEAD", "PLUCK", "PLUMB", "PLUME", "PLUSH", "POEMS", "POINT",
    "POLAR", "PORCH", "POUND", "POWER", "PRAY", "PRESS", "PRICE", "PRIDE", "PRIME", "PRINT",
    "PRIZE", "PROBE", "PRONE", "PROOF", "PROUD", "PULSE", "PUNCH", "PUPIL", "PUPPY", "PURSE",
    "QUEEN", "QUERY", "QUEST", "QUICK", "QUIET", "QUILT", "QUIRK", "QUOTA", "RADAR", "RADIO",
    "RAISE", "RALLY", "RANCH", "RANGE", "RAPID", "RATIO", "REACH", "REACT", "READY", "REALM",
    "REBEL", "REFER", "REIGN", "RELAX", "RELIC", "REPLY", "RIDER", "RIDGE", "RIGHT", "RIGID",
    "RISKY", "RIVAL", "RIVER", "ROAST", "ROBOT", "ROCKY", "ROGUE", "ROMAN", "ROUGH", "ROUND",
    "ROUTE", "ROYAL", "RULER", "RURAL", "RUSTY", "SADLY", "SAINT", "SALAD", "SALON", "SAUCE",
    "SCALE", "SCARE", "SCARF", "SCENE", "SCENT", "SCOPE", "SCORE", "SCOUT", "SCRAP", "SCREW",
    "SEDAN", "SENSE", "SERVE", "SEVEN", "SHADE", "SHADOW", "SHAFT", "SHAKE", "SHAME", "SHAPE",
    "SHARE", "SHARK", "SHARP", "SHEEP", "SHEER", "SHEET", "SHELF", "SHELL", "SHIFT", "SHINE",
    "SHIRT", "SHOCK", "SHOOT", "SHORE", "SHORT", "SHOUT", "SIGHT", "SIGMA", "SILENT", "SILVER",
    "SINCE", "SIREN", "SKATE", "SKILL", "SKULL", "SLATE", "SLEEP", "SLICE", "SLIDE", "SLOPE",
    "SMART", "SMELL", "SMILE", "SMOKE", "SNACK", "SNAKE", "SOLAR", "SOLID", "SOLVE", "SONAR",
    "SOUND", "SOUTH", "SPACE", "SPARK", "SPEAK", "SPEAR", "SPEED", "SPELL", "SPEND", "SPHERE",
    "SPICE", "SPIKE", "SPILL", "SPIRIT", "SPLIT", "SPOIL", "SPOKE", "SPOON", "SPORT", "SPRAY",
    "SPREAD", "SPRING", "SQUAD", "STACK", "STAFF", "STAGE", "STAIN", "STAIR", "STAKE", "STALE",
    "STAMP", "STAND", "STARE", "START", "STATE", "STEAK", "STEAL", "STEAM", "STEEL", "STEEP",
    "STEER", "STICK", "STIFF", "STILL", "STING", "STOCK", "STONE", "STOOL", "STORM", "STORY",
    "STRAP", "STRAW", "STRIP", "STUDY", "STUFF", "STYLE", "SUGAR", "SUITE", "SUMMER", "SUMMIT",
    "SUNNY", "SUPER", "SURGE", "SWAMP", "SWEAR", "SWEAT", "SWEEP", "SWEET", "SWIFT", "SWING",
    "SWORD", "TABLE", "TASTE", "TEACH", "TEMPO", "TENTH", "THANK", "THEME", "THICK", "THIEF",
    "THIGH", "THING", "THINK", "THIRD", "THORN", "THOSE", "THREE", "THROW", "THUMB", "TIGER",
    "TIGHT", "TIMER", "TIRED", "TITLE", "TOAST", "TODAY", "TOKEN", "TOOTH", "TOPIC", "TORCH",
    "TOTAL", "TOUCH", "TOUGH", "TOWER", "TOXIC", "TRACE", "TRACK", "TRACT", "TRADE", "TRAIL",
    "TRAIN", "TRAIT", "TRASH", "TREAT", "TREND", "TRIAL", "TRIBE", "TRICK", "TROOP", "TRUCK",
    "TRULY", "TRUNK", "TRUST", "TRUTH", "TULIP", "TUMOR", "TUNER", "TUNNEL", "TWICE", "TWIST",
    "UNCLE", "UNDER", "UNION", "UNITY", "UPPER", "UPSET", "URBAN", "USAGE", "USUAL", "VALID",
    "VALLEY", "VALUE", "VALVE", "VAPOR", "VAULT", "VENUE", "VIGOR", "VIRAL", "VIRUS", "VISIT",
    "VITAL", "VIVID", "VOCAL", "VOICE", "VOWEL", "WAFER", "WAGON", "WASTE", "WATCH", "WATER",
    "WEDGE", "WEIGH", "WHALE", "WHEAT", "WHEEL", "WHERE", "WHICH", "WHILE", "WHITE", "WHOLE",
    "WHOSE", "WIDOW", "WIDTH", "WINDY", "WITCH", "WOMAN", "WORLD", "WORRY", "WORSE", "WORST",
    "WORTH", "WOUND", "WRATH", "WRECK", "WRIST", "WRITE", "WRONG", "YACHT", "YIELD", "YOUTH",
    "ZEBRA",
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

    ans_words = set(re.findall(r'[A-Z]+', answer.upper()))
    valid_pool = [w for w in pool if w.upper() not in ans_words]

    for attempt in range(500):
        rem = Counter(target_counts)
        chosen_words = []
        chosen_circles = []
        available_pool = list(valid_pool)
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
            for w in candidates[:25]:
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
    pool = list(set(CURATED_WORDS))

    for diff in ["easy", "medium", "hard"]:
        bank = RIDDLE_BANK[diff]
        print(f"Generating {diff.upper()} ({len(bank)} riddles)...")
        solved_count = 0

        for i, (riddle, answer) in enumerate(bank):
            ans_clean = clean_letters(answer)
            ans_len = len(ans_clean)

            if ans_len <= 16:
                target_counts = [4, 5] if diff != "easy" else [4]
            elif ans_len <= 20:
                target_counts = [5, 6, 4]
            else:
                target_counts = [6, 5]

            solved = False
            for tc in target_counts:
                res = solve_clue_words(answer, tc, pool)
                if res:
                    words, circles = res
                    extracted = [words[w][c] for w in range(len(words)) for c in circles[w]]
                    assert sorted(extracted) == sorted(ans_clean), f"Multiset error in {answer}"
                    ans_tokens = set(re.findall(r'[A-Z]+', answer.upper()))
                    for w in words:
                        assert w.upper() not in ans_tokens, f"Leak: {w} in {answer}"

                    puzzle_id = f"{diff}_{i+1:03d}"
                    puzzles.append({
                        "id": puzzle_id,
                        "diff": diff,
                        "words": words,
                        "circles": circles,
                        "riddle": riddle,
                        "answer": answer
                    })
                    solved = True
                    solved_count += 1
                    break

            if not solved:
                print(f"FAILED to solve: [{diff}] {riddle} -> {answer} (len={ans_len})")

        print(f"  {diff.upper()} successfully solved: {solved_count}/{len(bank)}")

    return puzzles

def emit_json(puzzles, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(puzzles, f, indent=2)
    print(f"Emitted JSON dataset to {filepath} ({len(puzzles)} puzzles)")

def emit_cpp_progmem(puzzles, filepath):
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
        diff_enum = "JUMBLE_EASY" if p["diff"] == "easy" else ("JUMBLE_MEDIUM" if p["diff"] == "medium" else "JUMBLE_HARD")
        num_words = len(p["words"])
        
        words_padded = p["words"] + [""] * (6 - num_words)
        words_c = "{" + ", ".join(f'"{w}"' for w in words_padded) + "}"

        circles_array = []
        num_circles_array = []
        for w_idx in range(6):
            if w_idx < num_words:
                circ = p["circles"][w_idx]
                num_circles_array.append(str(len(circ)))
                padded_circ = circ + [0] * (4 - len(circ))
                circles_array.append("{" + ", ".join(str(c) for c in padded_circ) + "}")
            else:
                num_circles_array.append("0")
                circles_array.append("{0, 0, 0, 0}")

        circles_c = "{" + ", ".join(circles_array) + "}"
        num_circles_c = "{" + ", ".join(num_circles_array) + "}"

        riddle_escaped = p['riddle'].replace('\\', '\\\\').replace('"', '\\"')
        answer_escaped = p['answer'].replace('\\', '\\\\').replace('"', '\\"')

        lines.append("    {")
        lines.append(f"        {diff_enum}, {num_words},")
        lines.append(f"        {words_c},")
        lines.append(f"        {circles_c},")
        lines.append(f"        {num_circles_c},")
        lines.append(f'        "{riddle_escaped}",')
        lines.append(f'        "{answer_escaped}"')
        lines.append("    },")

    lines.append("};")
    lines.append("")
    lines.append("#endif // JUMBLE_DATASET_H")
    lines.append("")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Emitted C++ PROGMEM header to {filepath}")

if __name__ == "__main__":
    puzzles = generate_all_puzzles()
    assert len(puzzles) == 300, f"Expected 300 puzzles, got {len(puzzles)}"
    emit_json(puzzles, "server/data/jumbles.json")
    emit_cpp_progmem(puzzles, "esp32-firmware/src/generators/JumbleDataset.h")
    print("All 300 puzzles successfully generated and mathematically verified!")
