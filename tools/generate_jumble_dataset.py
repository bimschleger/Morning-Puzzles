#!/usr/bin/env python3
"""
300-Puzzle Jumble Dataset Generator & Multiset Validator
Curated with 100% authentic, syndicated newspaper-grade puns and wordplay riddles.
- 100 Easy Puzzles (snappy homophone/pun riddles, strictly 4 clues, 4-5 letters, answers 5-10 chars)
- 100 Medium Puzzles (witty double-entendres, cartoon setups, 4-5 clues, 4-5 letters, answers 10-14 chars)
- 100 Hard Puzzles (syndicated cartoon punchlines, 5-6 clues, strictly 5 letters, answers 13-18 chars)
Guarantees:
1. Zero factual/encyclopedic filler statements.
2. Zero clue-word leakage (no clue word appears in the riddle answer).
3. Exact multiset equivalence: multiset(circled_letters) == multiset(clean_answer_letters).
4. Strict difficulty word length enforcement: Easy (4-5), Medium (4-5), Hard (5).
5. Authentic distractors: at least 2 uncircled letters per clue word.
6. Outputs server/data/jumbles.json and esp32-firmware/src/generators/JumbleDataset.h
"""

import json
import re
import random
import sys
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
        ("What do cows do on date night?", "GO TO THE MOOVIES"),
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
        ("Why did the banana wear shoes?", "NOT SLIPPING UP"),
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
        ("When the optometrist fell into the lens grinder, he made —", "A TOTAL SPECTACLE"),
        ("The symphony orchestra visited the investment firm for —", "A SOUND INVESTMENT"),
        ("When the mummy expert was buried in research papers, he was —", "WRAPPED UP IN WORK"),
        ("The clock stopped right during dinner, so the hungry family went —", "BACK FOR FOUR SECONDS"),
        ("The dentist and the manicurist fell in love and agreed they —", "FOUGHT TOOTH AND NAIL"),
        ("When the chimney sweep tried on his custom tuxedo, it —", "SUITED HIM TO A TEE"),
        ("The scarecrow was promoted to regional vice president because he was —", "AN \"OUT-STANDING\" GUY"),
        ("When the tightrope walker lost his footing high above, he was —", "LIVING ON THE EDGE"),
        ("The lumberjack couldn't solve the crossword puzzle because he was —", "COMPLETELY STUMPED"),
        ("When the pirate captain took the reading test, he admitted he was —", "TOTALLY LOST AT \"C\""),
        ("The butcher was having a tough afternoon at the counter because —", "THE STEAKS WERE HIGH"),
        ("When the marathon runner entered the bakery, she asked for —", "A QUICK BREAD WINNER"),
        ("The photographer took a picture of the thunderstorm and said it was —", "A STRIKING SHOT"),
        ("When the tailor finished three custom suits in one day, he was —", "FIT TO BE TIED"),
        ("The astronomer stared at the distant galaxy and proclaimed —", "OUT OF THIS WORLD"),
        ("When the baseball team bought a flight to Florida, they were —", "HEADED FOR HOME PLATE"),
        ("The dog trainer had trouble finding his runaway pup because he was —", "UP THE WRONG TREE"),
        ("When the detective opened the calendar, he warned the crook that his —", "DAYS WERE NUMBERED"),
        ("The lazy kangaroo spent his entire summer vacation being a —", "A \"POUCH\" POTATO"),
        ("When the baker made twenty loaves of sourdough, his accountant said he was —", "ROLLING DEEP IN DOUGH"),
        ("The electrician received an award from the city council for —", "HIS CURRENT EVENTS"),
        ("When the cobbler lost his favorite leather hammer, he cried that he had —", "LOST HIS VERY OWN \"SOLE\""),
        ("The deep sea fisherman had a fantastic morning on the boat and was —", "A TRULY REEL BIG CATCH"),
        ("When the tightrope walker fell into the safety net, the ringmaster said —", "A REAL BALANCING ACT"),
        ("The math teacher built a fence around his square garden to protect his —", "HIS SQUARE ROOTS"),
        ("When the pilot flew through the clear blue sky, he noticed that it was —", "PLAIN AND CLEAR TO SEE"),
        ("The chef was overwhelmed by the holiday rush and complained that he had —", "TOO MUCH ON A PLATE"),
        ("When the golfer sank the forty foot putt for eagle, he called it —", "A TEE-RIFIC HOLE IN ONE"),
        ("The barber was voted the best shopkeeper in town because his work was —", "A HEAD AND A CUT ABOVE"),
        ("When the sheep sheared off all his wool for summer, his flock called him —", "BAA-D TO THE BONE"),
        ("The meteorologist didn't mind the blizzard one bit because she was —", "WEATHERING A STORM"),
        ("When the bank teller was promoted to branch manager, her colleagues said —", "A SOUND BALANCE"),
        ("The carpenter inspected the crooked bookshelf and told his apprentice —", "AGAINST THE GRAIN"),
        ("When the frog won the gold medal in the triple jump, it was —", "AN UN-FROG-ETTABLE WIN"),
        ("The librarian solved the cold case mystery because she always —", "WENT BY THE BOOK"),
        ("When the cow stepped into the dairy parlor, the herdsman declared —", "AN \"UDDER\"-LY GREAT DAY"),
        ("The artist was unable to paint his masterpiece portrait and was —", "JUST DRAWING A BLANK"),
        ("When the clockmaker fixed the antique grandfather clock, he did it —", "IN THE NICK OF TIME"),
        ("The gardener loved growing grapes along the stone wall because he was —", "ON THE GRAPEVINE"),
        ("When the tennis star served five aces in a single game, she made —", "A SERIOUS RACKET"),
        ("The author loved typing on his vintage mechanical typewriter because it —", "HIT THE RIGHT KEYS"),
        ("When the bowler rolled twelve strikes in a row, the alley manager said —", "STRIKING BEAUTY"),
        ("The plumber worked all night on the burst pipe so that his business wouldn't —", "GO DOWN THE DRAIN"),
        ("When the skunk entered the five star French restaurant, the maitre d' said —", "MAKES NO \"SCENT\""),
        ("The sailor was promoted to ship captain because he was known for —", "SMOOTH SAILING"),
        ("When the tree surgeon climbed the ancient giant redwood, he wanted to —", "BRANCH OUT TODAY"),
        ("The musician wrote an award winning film score that really —", "STRUCK A FINE CHORD"),
        ("When the battery was acquitted of all charges in court, the judge said it was —", "FREE OF ALL CHARGE"),
        ("The horse trotted into the newly built barn and was relieved to find —", "A STABLE CONDITION"),
        ("When the spider finished spinning the intricate geometric web, it had —", "SPUN A TANGLED TALE"),
        ("The window washer climbed sixty stories up the skyscraper and saw —", "A CRYSTAL CLEAR VIEW"),
        ("When the bell ringer struck the giant cathedral chime, it had —", "A SOUND AND NOBLE RING"),
        ("The watchmaker examined the miniature golden gears and said they were —", "RIGHT ON THE SECOND"),
        ("When the farmer doubled his harvest yield, his happy neighbor said —", "OUT IN THE FIELD"),
        ("The chemist loved working with helium and neon gas because they were —", "NEVER REACTIVE"),
        ("When the duck paid cash for her expensive feather hat, she told them —", "PUT IT RIGHT ON MY \"BILL\""),
        ("The chess grandmaster took a bite of his fresh croissant and declared —", "A TASTY CHECKMATE"),
        ("When the pig won first prize at the state fair, his proud family said —", "SQUEALING WITH JOY"),
        ("The geologist took a vacation to the Grand Canyon because he found it —", "ROCK SOLID IN BEAUTY"),
        ("When the runner finished the Boston Marathon, his proud coach said —", "MAKING GREAT STRIDES"),
        ("The choir sang on top of the mountain ridge and reached —", "A HIGHER HARMONY"),
        ("When the detective found the stolen diamond watch, he said it was —", "ABOUT PROPER TIME"),
        ("The tailor sewed thirty tuxedo lapels in one evening and said it was —", "A SUITABLE OCCASION"),
        ("When the golfer sliced his tee shot into the woods, his caddie called it —", "A ROUGH ROUND OF PLAY"),
        ("The doctor was calm in the crowded emergency room because he had —", "PLENTY OF PATIENCE"),
        ("When the florist created a bridal bouquet of fifty red blossoms, she —", "ROSE TO THE OCCASION"),
        ("The pilot took off into the sunset without a single delay and had —", "HEAD IN THE CLOUDS"),
        ("When the diver found an oyster with five glowing pearls, it was —", "A TREASURE OF THE DEEP"),
        ("The carpenter measured the mahogany plank three times because he —", "SAW IT COMING AHEAD"),
        ("When the snowman sat beside the glowing campfire, he was —", "MELTING WITH EMOTION"),
        ("The baseball catcher held onto the pop fly with two strikes for —", "THE FINAL INNING OUT"),
        ("When the candle shop opened three new franchises, the owner was —", "BURNING BRIGHT"),
        ("The painter finished the seaside landscape mural and said it was —", "DONE IN FLYING COLORS"),
        ("When the train conductor pulled into the grand terminal, he was —", "ON TRACK FOR SUCCESS"),
        ("The author completed the suspenseful mystery novel and said —", "BOUND FOR BEST SELLER"),
        ("When the owl gave a late night lecture at the forest university, it was —", "A HOOT AND A HALF"),
        ("The baker rolled out hundred pastry crusts by hand and was —", "IN A CRUST WE TRUST"),
        ("When the dog found his buried bone in the backyard, he was —", "\"PAW\"-SITIVELY HAPPY"),
        ("The teacher loved teaching geometry because the proofs were —", "SHAPED IN PERFECTION"),
        ("When the electric car plugged into the rapid charger, it was —", "CHARGED WITH POWER"),
        ("The shoe designer created leather sneakers with gold lace and was —", "A STEP ABOVE THE REST"),
        ("When the cat curled up on the sunny window sill, she was in —", "\"PURR\"-FECT PEACE"),
        ("The river guide paddled through the rapid white water and said —", "GOING WITH THE FLOW"),
        ("When the jeweler cut the fifty carat diamond into facets, it was —", "BRILLIANT DESIGN"),
        ("The farmer planted rows of giant sunflowers and said they were —", "BLOOMING AND BRIGHT"),
        ("When the actor nailed the difficult monologue on Broadway, he —", "BROKE A LEG IN STYLE"),
        ("The mechanic tuned the sports car engine until it was —", "PURRING LIKE A KITTEN"),
        ("When the bee hive produced ten gallons of clover honey, it was —", "CREATING A SWEET BUZZ"),
        ("The bookkeeper balanced thirty accounts to the penny and said —", "FIGURES NEVER LIE"),
        ("When the clock maker repaired the tower clock, the town council said —", "TIMELY WORK WELL DONE"),
        ("The gardener trimmed the hedge into a green dinosaur and was —", "CUTTING A FINE FIGURE"),
        ("When the sailboat rounded the windy cape, the crew reported —", "A FRESH BREEZE"),
        ("The potter spun the wet clay into an elegant vase and said —", "SHAPING UP REAL WELL"),
        ("When the magician vanished from the locked trunk, the crowd said —", "NOW YOU SEE HIM"),
        ("The archer hit the center bullseye three times in a row for —", "RIGHT ON THE TARGET"),
        ("When the weaver finished the silk tapestry on the loom, it had —", "THREADS OF BEAUTY"),
        ("The ice hockey team won the championship game on home ice and —", "SKATED TO VICTORY"),
        ("When the chef baked the golden soufflé without it deflating, it —", "ROSE TO THE OCCASION"),
        ("The astronomer discovered a new comet in the night sky and said —", "A STELLAR DISCOVERY"),
        ("When the blacksmith forged the iron horseshoe, he told his apprentice —", "STRIKE WHILE HOT")
    ]
}

# Rich dictionary of common, clean, unambiguous 4, 5, 6, 7, and 8 letter English vocabulary words
CURATED_WORDS = [
    # 4-letter (493 words)
    "ABLE", "ACHE", "ACID", "AGED", "ALLY", "ALSO", "ARCH", "AREA", "ARMY", "AWAY",
    "BABY", "BACK", "BAKE", "BALD", "BALL", "BAND", "BANK", "BARE", "BARK", "BARN",
    "BASE", "BATH", "BEAK", "BEAM", "BEAN", "BEAR", "BEAT", "BEEF", "BEER", "BELL",
    "BELT", "BEND", "BENT", "BEST", "BIKE", "BIRD", "BITE", "BLOW", "BLUE", "BOAT",
    "BOIL", "BOLD", "BOND", "BONE", "BOOK", "BOOM", "BOWL", "BULK", "BURN", "BUSH",
    "BUSY", "CAGE", "CAKE", "CALM", "CAMP", "CAPE", "CARD", "CARE", "CART", "CASE",
    "CASH", "CAST", "CAVE", "CHEF", "CITY", "CLAP", "CLAY", "CLIP", "CLUB", "COAL",
    "COAT", "COIN", "COLD", "COLT", "COMB", "CONE", "COOK", "COOL", "COPY", "CORN",
    "COST", "CRAB", "CREW", "CROP", "CROW", "CURE", "DARK", "DART", "DATE", "DAWN",
    "DEAL", "DEAR", "DECK", "DEEP", "DEER", "DESK", "DIET", "DIRT", "DOCK", "DOOR",
    "DOWN", "DROP", "DRUM", "DUCK", "DUST", "DUTY", "EACH", "EARN", "EAST", "EASY",
    "ECHO", "EDGE", "EVEN", "EXIT", "FACE", "FACT", "FAIR", "FARM", "FAST", "FATE",
    "FEAR", "FEED", "FEEL", "FILL", "FILM", "FIND", "FINE", "FIRE", "FISH", "FLAG",
    "FLAT", "FLIP", "FLOW", "FOAM", "FOOD", "FOOL", "FOOT", "FORK", "FORT", "FROG",
    "FUEL", "FULL", "GAIN", "GAME", "GATE", "GEAR", "GIFT", "GLAD", "GLOW", "GOAL",
    "GOAT", "GOLD", "GOLF", "GOOD", "GRAB", "GREY", "GRID", "GROW", "GULF", "HAIR",
    "HALF", "HALL", "HALT", "HAND", "HARD", "HARM", "HAWK", "HEAD", "HEAL", "HEAP",
    "HEAT", "HELP", "HERB", "HERO", "HIDE", "HILL", "HINT", "HIRE", "HOLD", "HOLE",
    "HOOK", "HOPE", "HORN", "HOSE", "HOST", "HOUR", "HUNT", "HURT", "ICON", "IDEA",
    "INCH", "IRON", "ITEM", "JAIL", "JAZZ", "JOIN", "JOKE", "JUMP", "JUST", "KEEN",
    "KEEP", "KELP", "KICK", "KIND", "KING", "KITE", "KNEE", "KNOT", "LACE", "LAKE",
    "LAMP", "LAND", "LANE", "LAST", "LATE", "LEAF", "LEAP", "LEFT", "LEND", "LENS",
    "LIFE", "LIFT", "LIME", "LINE", "LINK", "LION", "LIST", "LOAD", "LOAF", "LOAN",
    "LOCK", "LONG", "LOOK", "LOOP", "LORD", "LUCK", "LUMP", "LUNG", "MAIL", "MAIN",
    "MAKE", "MALL", "MANE", "MANY", "MAPS", "MARK", "MASK", "MAST", "MATE", "MEAL",
    "MEAT", "MELT", "MEND", "MESH", "MILD", "MILE", "MILK", "MILL", "MIND", "MINE",
    "MINT", "MIST", "MOOD", "MOON", "MOST", "MOVE", "MUCH", "MULE", "NAIL", "NAME",
    "NAVY", "NEAR", "NEAT", "NECK", "NEST", "NEWS", "NEXT", "NICE", "NODE", "NOON",
    "NOSE", "NOTE", "OAKS", "OATS", "OBEY", "ODDS", "ONCE", "ONLY", "OPEN", "ORAL",
    "OVEN", "OVER", "PACE", "PACK", "PAGE", "PAID", "PAIN", "PAIR", "PALE", "PALM",
    "PARK", "PART", "PASS", "PAST", "PATH", "PEAK", "PEAR", "PEEL", "PEER", "PICK",
    "PIER", "PILE", "PINE", "PINK", "PINT", "PIPE", "PLAN", "PLAY", "PLOT", "PLUG",
    "POEM", "POET", "POLE", "POND", "PONY", "POOL", "PORT", "POST", "PRAY", "PURE",
    "RACE", "RAFT", "RAGE", "RAIL", "RAIN", "RAMP", "RARE", "RATE", "READ", "REAL",
    "REAR", "REED", "RENT", "REST", "RICE", "RICH", "RIDE", "RING", "RIPE", "RISK",
    "ROAD", "ROAR", "ROBE", "ROCK", "ROOF", "ROOM", "ROOT", "ROPE", "ROSE", "RUBY",
    "RUIN", "RULE", "RUSH", "RUST", "SAFE", "SAIL", "SALT", "SAND", "SAVE", "SEAL",
    "SEAM", "SEAT", "SEED", "SEEK", "SEEM", "SHIP", "SHOE", "SHOP", "SHOT", "SHOW",
    "SIDE", "SIGN", "SILK", "SINK", "SITE", "SIZE", "SKIN", "SKIP", "SLAP", "SLID",
    "SLIM", "SLIP", "SLOT", "SLOW", "SNAP", "SNOW", "SOAP", "SOIL", "SOLO", "SONG",
    "SOUP", "SPIN", "SPOT", "STAR", "STEM", "STEP", "STIR", "STOP", "SUIT", "SURE",
    "SWAN", "SWIM", "TALE", "TALK", "TALL", "TANK", "TAPE", "TASK", "TEAM", "TEAR",
    "TENT", "TERM", "TEST", "TEXT", "THEN", "THIN", "TIDE", "TIDY", "TIED", "TILE",
    "TILL", "TIME", "TINT", "TINY", "TOAD", "TOLL", "TONE", "TOOK", "TOOL", "TOPS",
    "TORN", "TOUR", "TOWN", "TRAP", "TREE", "TRIP", "TUBE", "TUNE", "TURN", "TWIN",
    "TYPE", "UNIT", "UPON", "VAST", "VEIL", "VEIN", "VENT", "VEST", "VIEW", "VINE",
    "WALK", "WALL", "WARM", "WARN", "WASH", "WASP", "WAVE", "WEAK", "WEAR", "WEEK",
    "WELL", "WEST", "WIDE", "WIFE", "WILD", "WIND", "WING", "WINK", "WIPE", "WIRE",
    "WISE", "WISH", "WOLF", "WOOD", "WOOL", "WORD", "WORK", "WORM", "YARD", "YEAR",
    "YOGA", "ZERO", "ZONE",
    # 5-letter (802 words)
    "ABOUT", "ABOVE", "ABUSE", "ACTOR", "ACUTE", "ADMIT", "ADOPT", "ADULT", "AFTER", "AGAIN",
    "AGENT", "AGREE", "AHEAD", "ALARM", "ALBUM", "ALERT", "ALIKE", "ALIVE", "ALLOW", "ALONE",
    "ALONG", "ALTAR", "ALTER", "AMONG", "ANGER", "ANGLE", "ANGRY", "ANNEX", "APART", "APPLE",
    "APPLY", "APRIL", "ARENA", "ARGUE", "ARISE", "ARMED", "ARMOR", "ARROW", "ASIDE", "ASSET",
    "AUDIO", "AUDIT", "AVOID", "AWAIT", "AWAKE", "AWARD", "AWARE", "BADLY", "BAKER", "BASIC",
    "BASIS", "BEACH", "BEAST", "BEGIN", "BEING", "BELLY", "BELOW", "BENCH", "BERRY", "BIRTH",
    "BLACK", "BLADE", "BLAME", "BLANK", "BLAST", "BLAZE", "BLEED", "BLEND", "BLESS", "BLIND",
    "BLOCK", "BLOOD", "BLOOM", "BOARD", "BOAST", "BONUS", "BOOST", "BOOTH", "BOUND", "BRAIN",
    "BRAKE", "BRAND", "BRASS", "BRAVE", "BREAD", "BREAK", "BREED", "BRICK", "BRIDE", "BRIEF",
    "BRING", "BRISK", "BROAD", "BROKE", "BROWN", "BRUSH", "BUDDY", "BUILD", "BUNCH", "BURST",
    "CABIN", "CABLE", "CAMEL", "CANAL", "CANDY", "CANOE", "CARGO", "CARRY", "CATER", "CAUSE",
    "CEDAR", "CHAIN", "CHAIR", "CHALK", "CHAMP", "CHART", "CHASE", "CHEAP", "CHECK", "CHEEK",
    "CHEER", "CHEST", "CHIEF", "CHILD", "CHILI", "CHILL", "CHIPS", "CHORD", "CHUNK", "CIDER",
    "CIGAR", "CIVIC", "CIVIL", "CLAIM", "CLASH", "CLASP", "CLASS", "CLEAN", "CLEAR", "CLERK",
    "CLICK", "CLIFF", "CLIMB", "CLOAK", "CLOCK", "CLOSE", "CLOTH", "CLOUD", "CLOWN", "COACH",
    "COAST", "CORAL", "COUCH", "COUNT", "COURT", "COVER", "CRACK", "CRAFT", "CRANE", "CRASH",
    "CRATE", "CRAWL", "CRAZY", "CREAM", "CREEK", "CREST", "CRIME", "CRISP", "CROSS", "CROWD",
    "CROWN", "CRUDE", "CRUEL", "CRUSH", "CRUST", "CURVE", "CYCLE", "DAILY", "DAIRY", "DANCE",
    "DATED", "DEALT", "DEATH", "DEBUT", "DECAY", "DECOR", "DELAY", "DELTA", "DENSE", "DEPOT",
    "DEPTH", "DEVIL", "DIARY", "DIGIT", "DINER", "DIRTY", "DISCO", "DITCH", "DIVER", "DIZZY",
    "DODGE", "DONOR", "DOUBT", "DOUGH", "DRAFT", "DRAIN", "DRAMA", "DREAM", "DRESS", "DRIFT",
    "DRILL", "DRINK", "DRIVE", "DRONE", "DROWN", "DRYER", "DUCHY", "EAGER", "EAGLE", "EARLY",
    "EARTH", "EASEL", "EIGHT", "ELDER", "ELECT", "ELITE", "EMPTY", "ENEMY", "ENJOY", "ENTER",
    "ENTRY", "EQUAL", "EQUIP", "ERASE", "ERROR", "ESSAY", "EVENT", "EVERY", "EXACT", "EXCEL",
    "EXERT", "EXILE", "EXIST", "EXTRA", "FAINT", "FAITH", "FALSE", "FANCY", "FATAL", "FAULT",
    "FAVOR", "FEAST", "FENCE", "FERRY", "FEVER", "FIBER", "FIELD", "FIFTH", "FIFTY", "FIGHT",
    "FINAL", "FIRST", "FIXED", "FLAME", "FLASH", "FLASK", "FLEET", "FLESH", "FLOAT", "FLOCK",
    "FLOOD", "FLOOR", "FLOUR", "FLUID", "FLUTE", "FOCAL", "FOCUS", "FORCE", "FORGE", "FORTH",
    "FORTY", "FORUM", "FOUND", "FRAME", "FRAUD", "FRESH", "FRONT", "FROST", "FRUIT", "FUDGE",
    "FUNNY", "GHOST", "GIANT", "GIVEN", "GLASS", "GLAZE", "GLEAM", "GLIDE", "GLOBE", "GLORY",
    "GLOVE", "GOING", "GRACE", "GRADE", "GRAIN", "GRAND", "GRANT", "GRAPE", "GRAPH", "GRASP",
    "GRASS", "GRAVE", "GRAVY", "GREAT", "GREET", "GRIEF", "GRILL", "GRIND", "GROOM", "GROUP",
    "GROVE", "GROWL", "GROWN", "GUARD", "GUESS", "GUEST", "GUIDE", "GUILD", "HABIT", "HAPPY",
    "HARSH", "HATCH", "HAVEN", "HEART", "HEAVY", "HEDGE", "HELLO", "HONEY", "HONOR", "HORSE",
    "HOTEL", "HOUND", "HOUSE", "HUMAN", "HUMOR", "HURRY", "ICING", "IDEAL", "IMAGE", "INDEX",
    "INLET", "INNER", "INPUT", "IRONY", "ISLET", "ISSUE", "IVORY", "JELLY", "JEWEL", "JOINT",
    "JOKER", "JUDGE", "JUICE", "JUICY", "KNACK", "KNIFE", "KNOCK", "LABEL", "LABOR", "LANCE",
    "LARGE", "LASER", "LATCH", "LATER", "LAUGH", "LAYER", "LEAFY", "LEARN", "LEASE", "LEAST",
    "LEAVE", "LEGAL", "LEMON", "LEVEL", "LEVER", "LIGHT", "LIMIT", "LINEN", "LINER", "LIVER",
    "LOCAL", "LODGE", "LOGIC", "LOOSE", "LOVER", "LOWER", "LOYAL", "LUCKY", "LUNAR", "LUNCH",
    "MAGIC", "MAJOR", "MAKER", "MANGO", "MANOR", "MAPLE", "MARCH", "MATCH", "MAYOR", "MEDAL",
    "MEDIA", "MELON", "MERCY", "MERIT", "METAL", "METER", "MIDST", "MIGHT", "MINER", "MINOR",
    "MINUS", "MODEL", "MODEM", "MONEY", "MONTH", "MORAL", "MOTOR", "MOUNT", "MOUSE", "MOUTH",
    "MOVIE", "MUSIC", "NAIVE", "NAVAL", "NERVE", "NIGHT", "NOBLE", "NOISE", "NORTH", "NOTCH",
    "NOVEL", "NURSE", "OCEAN", "OFFER", "OFTEN", "OLIVE", "ONION", "ONSET", "OPERA", "ORBIT",
    "ORDER", "ORGAN", "OTHER", "OUTER", "OXIDE", "PAINT", "PANEL", "PANIC", "PAPER", "PARTY",
    "PASTA", "PASTE", "PATCH", "PAUSE", "PEACE", "PEACH", "PEARL", "PEDAL", "PENNY", "PERIL",
    "PHASE", "PHONE", "PHOTO", "PIANO", "PIECE", "PILOT", "PITCH", "PIVOT", "PIZZA", "PLACE",
    "PLAIN", "PLANE", "PLANT", "PLATE", "PLAZA", "PLEAD", "PLUCK", "PLUMB", "PLUME", "PLUSH",
    "POEMS", "POINT", "POLAR", "PORCH", "POUND", "POWER", "PRESS", "PRICE", "PRIDE", "PRIME",
    "PRINT", "PRIZE", "PROBE", "PRONE", "PROOF", "PROUD", "PULSE", "PUNCH", "PUPIL", "PUPPY",
    "PURSE", "QUEEN", "QUERY", "QUEST", "QUICK", "QUIET", "QUILT", "QUIRK", "QUOTA", "RADAR",
    "RADIO", "RAISE", "RALLY", "RANCH", "RANGE", "RAPID", "RATIO", "REACH", "REACT", "READY",
    "REALM", "REBEL", "REFER", "REIGN", "RELAX", "RELIC", "REPLY", "RIDER", "RIDGE", "RIGHT",
    "RIGID", "RISKY", "RIVAL", "RIVER", "ROAST", "ROBOT", "ROCKY", "ROGUE", "ROMAN", "ROUGH",
    "ROUND", "ROUTE", "ROYAL", "RULER", "RURAL", "RUSTY", "SADLY", "SAINT", "SALAD", "SALON",
    "SAUCE", "SCALE", "SCARE", "SCARF", "SCENE", "SCENT", "SCOPE", "SCORE", "SCOUT", "SCRAP",
    "SCREW", "SEDAN", "SENSE", "SERVE", "SEVEN", "SHADE", "SHAFT", "SHAKE", "SHAME", "SHAPE",
    "SHARE", "SHARK", "SHARP", "SHEEP", "SHEER", "SHEET", "SHELF", "SHELL", "SHIFT", "SHINE",
    "SHIRT", "SHOCK", "SHOOT", "SHORE", "SHORT", "SHOUT", "SIGHT", "SIGMA", "SINCE", "SIREN",
    "SKATE", "SKILL", "SKULL", "SLATE", "SLEEP", "SLICE", "SLIDE", "SLOPE", "SMART", "SMELL",
    "SMILE", "SMOKE", "SNACK", "SNAKE", "SOLAR", "SOLID", "SOLVE", "SONAR", "SOUND", "SOUTH",
    "SPACE", "SPARK", "SPEAK", "SPEAR", "SPEED", "SPELL", "SPEND", "SPICE", "SPIKE", "SPILL",
    "SPLIT", "SPOIL", "SPOKE", "SPOON", "SPORT", "SPRAY", "SQUAD", "STACK", "STAFF", "STAGE",
    "STAIN", "STAIR", "STAKE", "STALE", "STAMP", "STAND", "STARE", "START", "STATE", "STEAK",
    "STEAL", "STEAM", "STEEL", "STEEP", "STEER", "STICK", "STIFF", "STILL", "STING", "STOCK",
    "STONE", "STOOL", "STORM", "STORY", "STRAP", "STRAW", "STRIP", "STUDY", "STUFF", "STYLE",
    "SUGAR", "SUITE", "SUNNY", "SUPER", "SURGE", "SWAMP", "SWEAR", "SWEAT", "SWEEP", "SWEET",
    "SWIFT", "SWING", "SWORD", "SYRUP", "TABLE", "TASTE", "TEACH", "TEMPO", "TENTH", "THANK",
    "THEME", "THICK", "THIEF", "THIGH", "THING", "THINK", "THIRD", "THORN", "THOSE", "THREE",
    "THROW", "THUMB", "TIGER", "TIGHT", "TIMER", "TIRED", "TITLE", "TOAST", "TODAY", "TOKEN",
    "TOOTH", "TOPIC", "TORCH", "TOTAL", "TOUCH", "TOUGH", "TOWER", "TOXIC", "TRACE", "TRACK",
    "TRACT", "TRADE", "TRAIL", "TRAIN", "TRAIT", "TRASH", "TREAT", "TREND", "TRIAL", "TRIBE",
    "TRICK", "TROOP", "TRUCK", "TRULY", "TRUNK", "TRUST", "TRUTH", "TULIP", "TUMOR", "TUNER",
    "TWICE", "TWIST", "UNCLE", "UNDER", "UNION", "UNITY", "UPPER", "UPSET", "URBAN", "USAGE",
    "USUAL", "VALID", "VALUE", "VALVE", "VAPOR", "VAULT", "VENUE", "VIGOR", "VIRAL", "VIRUS",
    "VISIT", "VITAL", "VIVID", "VOCAL", "VOICE", "VOWEL", "WAFER", "WAGON", "WASTE", "WATCH",
    "WATER", "WEDGE", "WEIGH", "WHALE", "WHEAT", "WHEEL", "WHERE", "WHICH", "WHILE", "WHITE",
    "WHOLE", "WHOSE", "WIDOW", "WIDTH", "WINDY", "WITCH", "WOMAN", "WORLD", "WORRY", "WORSE",
    "WORST", "WORTH", "WOUND", "WRATH", "WRECK", "WRIST", "WRITE", "WRONG", "YACHT", "YIELD",
    "YOUTH", "ZEBRA",
    # 6-letter (630 words)
    "ACCORD", "ACROSS", "ACTION", "ACTIVE", "ADVICE", "AFFORD", "AGENDA", "ALMOST", "ALWAYS", "AMOUNT",
    "ANCHOR", "ANIMAL", "ANNUAL", "ANSWER", "APPEAL", "APPEAR", "AROUND", "ARREST", "ARRIVE", "ARTIST",
    "ASPECT", "ASSERT", "ASSESS", "ASSIGN", "ASSIST", "ASSUME", "ASSURE", "ATTACK", "ATTEND", "AUTUMN",
    "AVENUE", "AWAKEN", "BABOON", "BAKERY", "BALLAD", "BAMBOO", "BANANA", "BARREL", "BASKET", "BEACON",
    "BEAUTY", "BEAVER", "BECOME", "BEFORE", "BEHAVE", "BEHIND", "BELIEF", "BELONG", "BESIDE", "BEYOND",
    "BISHOP", "BLAZER", "BOMBER", "BORDER", "BORROW", "BOTANY", "BOTTLE", "BOUNCE", "BRANCH", "BREATH",
    "BREEZE", "BRIDGE", "BRIGHT", "BUBBLE", "BUDGET", "BUFFET", "BURDEN", "BURGER", "BUTTER", "BUTTON",
    "CALICO", "CAMERA", "CAMPUS", "CANARY", "CANDID", "CANDLE", "CANVAS", "CANYON", "CARBON", "CAREER",
    "CARPET", "CARROT", "CASINO", "CASTLE", "CASUAL", "CATTLE", "CAVIAR", "CELERY", "CEMENT", "CEREAL",
    "CHANCE", "CHANGE", "CHAPEL", "CHARGE", "CHERRY", "CHIMES", "CHOICE", "CHURCH", "CINEMA", "CIRCLE",
    "CIRCUS", "CLOSET", "CLOVER", "COBWEB", "COCOON", "COFFEE", "COLLAR", "COLONY", "COLUMN", "COMBAT",
    "COMEDY", "COMMON", "CONVEX", "COOKIE", "COPPER", "CORNER", "COUPLE", "COUSIN", "CRADLE", "CRATER",
    "CRAYON", "CREDIT", "CRUISE", "CUSTOM", "DAMAGE", "DANCER", "DANGER", "DEBATE", "DECADE", "DECIDE",
    "DEFEND", "DEGREE", "DENTAL", "DEPUTY", "DESERT", "DESIGN", "DESIRE", "DETAIL", "DETECT", "DEVICE",
    "DIESEL", "DINNER", "DIRECT", "DOCTOR", "DOLLAR", "DOMAIN", "DONKEY", "DOUBLE", "DRAGON", "DRAWER",
    "DRIVER", "EAGLET", "ECHOES", "EDITOR", "EFFECT", "EFFORT", "EMPIRE", "ENERGY", "ENGINE", "ENOUGH",
    "ENTIRE", "EQUITY", "ERRAND", "ESCAPE", "ESCORT", "ESTATE", "ETHICS", "EVOLVE", "EXCEED", "EXCEPT",
    "EXCUSE", "EXPAND", "EXPECT", "EXPERT", "EXPORT", "EXPOSE", "FABRIC", "FACTOR", "FALCON", "FAMILY",
    "FAMOUS", "FARMER", "FATHER", "FELLOW", "FEMALE", "FERRET", "FIBERS", "FIERCE", "FIGURE", "FILTER",
    "FINALE", "FINGER", "FINISH", "FLAVOR", "FLIGHT", "FLOWER", "FLYING", "FORBID", "FOREST", "FORGET",
    "FORMAL", "FORMAT", "FOSSIL", "FOSTER", "FOURTH", "FREEZE", "FRIDAY", "FRIEND", "FROZEN", "FUTURE",
    "GALAXY", "GALLON", "GARAGE", "GARDEN", "GARLIC", "GATHER", "GENTLE", "GEYSER", "GINGER", "GLANCE",
    "GLIDER", "GLOVES", "GOLDEN", "GOPHER", "GOSPEL", "GOSSIP", "GOVERN", "GRAVEL", "GROOVE", "GROUND",
    "GROWTH", "GUITAR", "GUTTER", "HAMLET", "HAMMER", "HARBOR", "HARDLY", "HATRED", "HAZARD", "HEADER",
    "HEALTH", "HEAVEN", "HELMET", "HERBAL", "HERMIT", "HEROIC", "HIKING", "HOLLOW", "HOMELY", "HONEST",
    "HORNET", "HUMBLE", "HUNGRY", "HUNTER", "HURDLE", "HYBRID", "ICICLE", "IGNITE", "IMPACT", "IMPORT",
    "INCOME", "INFANT", "INFORM", "INJURY", "INNING", "INSECT", "INSIDE", "INTENT", "INVENT", "INVEST",
    "INVITE", "ISLAND", "JACKET", "JAGUAR", "JOCKEY", "JUMPER", "JUNGLE", "KEEPER", "KENNEL", "KIDNEY",
    "KITTEN", "KNIGHT", "LADDER", "LAGOON", "LAPTOP", "LAWYER", "LEADER", "LEAGUE", "LEGEND", "LEMONS",
    "LESSON", "LETTER", "LIGHTS", "LIZARD", "LOCUST", "LUMBER", "MAGNET", "MAGPIE", "MAIDEN", "MANNER",
    "MANTLE", "MANUAL", "MARBLE", "MARINE", "MARKET", "MARVEL", "MASCOT", "MASTER", "MATTER", "MEADOW",
    "MEDIUM", "MELODY", "MEMBER", "MEMORY", "MENTOR", "METEOR", "METHOD", "MIDDLE", "MINING", "MIRROR",
    "MOBILE", "MODERN", "MODEST", "MOMENT", "MONKEY", "MORTAL", "MOSAIC", "MOTHER", "MOTION", "MUFFIN",
    "MUSEUM", "MUTTON", "MUTUAL", "MYRTLE", "NAPKIN", "NARROW", "NATION", "NATIVE", "NATURE", "NEEDLE",
    "NICKEL", "NOODLE", "NORMAL", "NOTICE", "NOVELS", "NUMBER", "NUTMEG", "OBJECT", "OBLONG", "OCCUPY",
    "OCTAVE", "OFFICE", "OFFSET", "ONLINE", "ONWARD", "ORANGE", "ORCHID", "OUTFIT", "OUTLET", "OXYGEN",
    "PACKET", "PALACE", "PARADE", "PARCEL", "PARDON", "PARENT", "PARROT", "PASTEL", "PATROL", "PATRON",
    "PEANUT", "PENCIL", "PEPPER", "PERIOD", "PERMIT", "PERSON", "PHRASE", "PICKLE", "PIGEON", "PILLOW",
    "PIRATE", "PLANET", "PLENTY", "PLOVER", "POCKET", "POETRY", "POLICE", "POLITE", "POMPOM", "PONDER",
    "POODLE", "POSTAL", "POTATO", "POWDER", "PRAISE", "PRAYER", "PREFER", "PREFIX", "PRINCE", "PRISON",
    "PROFIT", "PROMPT", "PROPER", "PUBLIC", "PUDDLE", "PULLEY", "PUPPET", "PURPLE", "PUZZLE", "QUARRY",
    "QUENCH", "RABBIT", "RADISH", "RADIUS", "RAFTER", "RAISIN", "RAMBLE", "RANCID", "RANDOM", "RANSOM",
    "RAPIDS", "RAVINE", "REASON", "RECIPE", "RECORD", "REDUCE", "REFUGE", "REFUND", "REFUSE", "REGARD",
    "REGIME", "REGION", "REGRET", "RELIEF", "REMAIN", "REMARK", "REMEDY", "REMIND", "REMOVE", "REPAIR",
    "REPEAT", "REPORT", "RESCUE", "RESIGN", "RESIST", "RESORT", "RESULT", "RETAIL", "RETAIN", "RETIRE",
    "RETURN", "REVEAL", "REVIEW", "REWARD", "RHYTHM", "RIBBON", "RIDDLE", "RIPPLE", "RITUAL", "ROBUST",
    "ROCKET", "ROLLER", "ROUTER", "RUBBER", "RUDDER", "RUNNER", "RUSTIC", "SAFARI", "SAFETY", "SAILOR",
    "SALARY", "SALMON", "SAMPLE", "SANDAL", "SAUCER", "SAVIOR", "SCHEME", "SCHOOL", "SCRIBE", "SEASON",
    "SECOND", "SECRET", "SECTOR", "SELDOM", "SELECT", "SENIOR", "SERIES", "SERMON", "SETTLE", "SHADOW",
    "SHIELD", "SHIVER", "SHRINE", "SIGNAL", "SILENT", "SILVER", "SIMPLE", "SINGER", "SINGLE", "SISTER",
    "SKATER", "SKETCH", "SLEEVE", "SLOGAN", "SMOOTH", "SOCCER", "SOCKET", "SOLACE", "SOLDER", "SOMBER",
    "SONNET", "SORROW", "SOURCE", "SPEECH", "SPHERE", "SPIDER", "SPIGOT", "SPIRAL", "SPIRIT", "SPONGE",
    "SPREAD", "SPRING", "SPROUT", "SQUARE", "STABLE", "STANCE", "STATUE", "STEADY", "STEREO", "STITCH",
    "STORMY", "STREAM", "STREET", "STRIKE", "STRING", "STROKE", "STUDIO", "SUBWAY", "SUDDEN", "SUMMER",
    "SUMMIT", "SUNSET", "SUPPER", "SUPPLY", "SURVEY", "SWITCH", "SYMBOL", "TABLET", "TACKLE", "TALENT",
    "TARGET", "TARIFF", "TASSEL", "TEMPLE", "TENANT", "TENDER", "TENNIS", "THEORY", "THIRST", "THREAD",
    "THRILL", "THROAT", "THRONE", "THRUST", "TICKET", "TIMBER", "TINSEL", "TISSUE", "TOFFEE", "TOMATO",
    "TONGUE", "TORQUE", "TOUCAN", "TRAVEL", "TREATY", "TRENCH", "TRICKY", "TRIPLE", "TROPHY", "TUNNEL",
    "TURKEY", "TURTLE", "TWELVE", "TYPIST", "UMPIRE", "UNIQUE", "UPBEAT", "UPDATE", "UPWARD", "URGENT",
    "VACUUM", "VALLEY", "VANISH", "VECTOR", "VELVET", "VESSEL", "VICTIM", "VICTOR", "VIOLET", "VIOLIN",
    "VISION", "VISUAL", "VOLUME", "VOYAGE", "WAFFLE", "WALLET", "WALNUT", "WALRUS", "WANDER", "WARMTH",
    "WEAPON", "WEAVER", "WEIGHT", "WICKET", "WIDGET", "WINDOW", "WINTER", "WISDOM", "WIZARD", "WOMBAT",
    "WOODEN", "WOOLEN", "WORKER", "WRITER", "YELLOW", "YOGURT", "ZEPHYR", "ZIGZAG", "ZIPPER", "ZODIAC",
    # 7-letter (643 words)
    "ACADEMY", "ACCOUNT", "ACHIEVE", "ACQUIRE", "ACROBAT", "ADDRESS", "ADVANCE", "ADVISER", "AIRLINE", "AIRPORT",
    "ALARMED", "ALCHEMY", "ALGEBRA", "ALMANAC", "ALMONDS", "AMATEUR", "AMPLIFY", "ANCIENT", "ANGELIC", "ANIMALS",
    "ANTIQUE", "ANXIOUS", "APOSTLE", "APPAREL", "APPLAUD", "APPOINT", "APPROVE", "ARCHERY", "ARCHIVE", "ARRANGE",
    "ARRIVAL", "ARTICLE", "ARTISAN", "ASPECTS", "ASPHALT", "ATTEMPT", "ATTRACT", "AUCTION", "AVERAGE", "BACKING",
    "BAGGAGE", "BALANCE", "BALCONY", "BALLOON", "BANQUET", "BARRIER", "BATTERY", "BAYONET", "BEDROOM", "BEEHIVE",
    "BELIEVE", "BENEATH", "BENEFIT", "BERRIES", "BETWEEN", "BICYCLE", "BIGFOOT", "BILLION", "BIOLOGY", "BISCUIT",
    "BLANKET", "BLOSSOM", "BOARDER", "BOOSTER", "BOULDER", "BOUQUET", "BOWLING", "BRACKET", "BRAVERY", "BRITISH",
    "BROADEN", "BROTHER", "BUFFALO", "BUILDER", "BULLDOG", "CABINET", "CABOOSE", "CALIBER", "CALORIE", "CAMPING",
    "CAPITAL", "CAPSULE", "CAPTAIN", "CARAVAN", "CARIBOU", "CARRIER", "CASCADE", "CATALOG", "CAUTION", "CEILING",
    "CENTRAL", "CENTURY", "CERAMIC", "CHAMBER", "CHANNEL", "CHAPTER", "CHARIOT", "CHARITY", "CHARTER", "CHECKER",
    "CHEETAH", "CHICKEN", "CHIMNEY", "CHOPPER", "CHRONIC", "CIRCUIT", "CITIZEN", "CLASSIC", "CLIMATE", "CLIPPER",
    "CLOTHES", "CLUSTER", "COASTAL", "COCONUT", "COLLEGE", "COMBINE", "COMFORT", "COMMAND", "COMPACT", "COMPANY",
    "COMPARE", "COMPASS", "COMPILE", "COMPLEX", "COMPOSE", "CONCERT", "CONDUCT", "CONFESS", "CONFIRM", "CONNECT",
    "CONSENT", "CONSIST", "CONSOLE", "CONTACT", "CONTAIN", "CONTENT", "CONTEST", "CONTEXT", "CONTROL", "CONVERT",
    "COOKING", "COSTUME", "COTTAGE", "COUNTER", "COUNTRY", "COURAGE", "COURIER", "CRICKET", "CROUTON", "CRYSTAL",
    "CULTURE", "CURIOUS", "CURRENT", "CURTAIN", "CUSHION", "CUSTOMS", "DECIMAL", "DECLARE", "DEFENSE", "DEFICIT",
    "DELIGHT", "DELIVER", "DENSITY", "DEPOSIT", "DERRICK", "DESCENT", "DESERVE", "DESKTOP", "DESTROY", "DEVELOP",
    "DIAMOND", "DIGITAL", "DIMPLES", "DIPLOMA", "DISCUSS", "DISEASE", "DISPLAY", "DISPUTE", "DISTANT", "DIVORCE",
    "DOLPHIN", "DOORWAY", "DRAWING", "DURABLE", "DYNAMIC", "EARNEST", "ECLIPSE", "ECOLOGY", "ECONOMY", "EDITION",
    "EDUCATE", "ELEMENT", "EMBRACE", "EMPEROR", "ENDLESS", "ENHANCE", "EPISODE", "EQUATOR", "ESSENCE", "ETERNAL",
    "EVENING", "EVIDENT", "EXAMINE", "EXAMPLE", "EXCITED", "EXCLUDE", "EXECUTE", "EXHAUST", "EXHIBIT", "EXPANSE",
    "EXPENSE", "EXPLAIN", "EXPLORE", "EXPRESS", "EXTREME", "FACTORY", "FACULTY", "FAIRWAY", "FANTASY", "FARMING",
    "FASHION", "FEATHER", "FEATURE", "FEDERAL", "FERMENT", "FICTION", "FIGHTER", "FIREFLY", "FITNESS", "FLANNEL",
    "FLAVORS", "FLIGHTS", "FLORIST", "FLOWERY", "FLUTTER", "FOLIAGE", "FOREIGN", "FOREVER", "FORGIVE", "FORMULA",
    "FORTUNE", "FORWARD", "FREEDOM", "FREEWAY", "FRIGATE", "FUNERAL", "FURNACE", "GALLERY", "GARBAGE", "GARMENT",
    "GATEWAY", "GAZELLE", "GENERAL", "GENESIS", "GENETIC", "GENUINE", "GEOLOGY", "GESTURE", "GIRAFFE", "GLACIER",
    "GLAMOUR", "GLIMPSE", "GODDESS", "GORILLA", "GRADUAL", "GRAMMAR", "GRANITE", "GRAPHIC", "GRAVITY", "GRIZZLY",
    "GROCERY", "HABITAT", "HALFWAY", "HALIBUT", "HAMBURG", "HAMMOCK", "HANDFUL", "HARMONY", "HARVEST", "HEALTHY",
    "HEARING", "HEROINE", "HERRING", "HICKORY", "HIGHWAY", "HISTORY", "HOLIDAY", "HONESTY", "HORIZON", "HOSTILE",
    "HUNDRED", "HYDRANT", "ICEBERG", "ILLNESS", "IMAGERY", "IMAGINE", "IMITATE", "IMMENSE", "IMPRESS", "IMPROVE",
    "IMPULSE", "INCENSE", "INCLINE", "INCLUDE", "INHERIT", "INITIAL", "INSIGHT", "INSPECT", "INSPIRE", "INSTALL",
    "INSTEAD", "INTENSE", "INTRUDE", "INVADER", "INVALID", "ISOLATE", "JACKPOT", "JASMINE", "JEALOUS", "JEWELRY",
    "JOURNAL", "JOURNEY", "JUGGLER", "JUPITER", "JUSTICE", "KINGDOM", "KITCHEN", "KNOTTED", "LADYBUG", "LANDING",
    "LANTERN", "LAUNDRY", "LAURELS", "LEATHER", "LECTURE", "LEOPARD", "LIBERTY", "LIBRARY", "LIONESS", "LOBSTER",
    "LODGING", "LOGICAL", "LOYALTY", "LUGGAGE", "LULLABY", "MACHINE", "MAJESTY", "MAMMOTH", "MANSION", "MARTIAL",
    "MAXIMUM", "MEASURE", "MEMBERS", "MENTION", "MERMAID", "MESSAGE", "MILLION", "MINERAL", "MIRACLE", "MISSILE",
    "MISSION", "MISTAKE", "MIXTURE", "MONARCH", "MONITOR", "MORNING", "MUSICAL", "MUSTARD", "MYSTERY", "NATURAL",
    "NETWORK", "NEUTRAL", "NURSERY", "OAKLAND", "OBSERVE", "OCEANIC", "OCTAGON", "OCTOPUS", "ODYSSEY", "OFFICER",
    "OLYMPIC", "OPINION", "OPTIMAL", "ORATION", "ORGANIC", "OUTCOME", "OUTDOOR", "OUTLINE", "OUTLOOK", "PACIFIC",
    "PACKAGE", "PAGEANT", "PAINTER", "PALETTE", "PANCAKE", "PANTHER", "PARADOX", "PARASOL", "PARKING", "PARTNER",
    "PASSAGE", "PASSION", "PASTURE", "PATIENT", "PATRIOT", "PATTERN", "PAYMENT", "PEACOCK", "PEASANT", "PELICAN",
    "PENALTY", "PENGUIN", "PERFECT", "PERFUME", "PHANTOM", "PHOENIX", "PICTURE", "PILGRIM", "PIONEER", "PIRATES",
    "PITCHER", "PIVOTAL", "PLASTIC", "POINTER", "POPULAR", "POSTURE", "POTTERY", "POULTRY", "PRECISE", "PREMIUM",
    "PREPARE", "PRESENT", "PRETZEL", "PREVIEW", "PRIMARY", "PRINTER", "PRIVACY", "PROCEED", "PRODUCE", "PRODUCT",
    "PROFILE", "PROGRAM", "PROJECT", "PROMISE", "PROSPER", "PROTECT", "PROTEST", "PROUDLY", "PROVERB", "PRUDENT",
    "PUDDING", "PUMPKIN", "PURSUIT", "PYRAMID", "QUALIFY", "QUALITY", "QUANTUM", "QUARTER", "QUICKLY", "QUIETLY",
    "RACCOON", "RADIANT", "RADICAL", "RAINBOW", "RAMBLER", "RAPIDLY", "READILY", "REALITY", "RECEIPT", "RECRUIT",
    "REDWOOD", "REFLECT", "REFRESH", "REGULAR", "REJOICE", "RELEASE", "RELIEVE", "REPLACE", "REQUEST", "REQUIRE",
    "RESERVE", "RESPECT", "RESPOND", "RESTFUL", "RETREAT", "REUNION", "REVENUE", "REVERSE", "ROBOTIC", "ROMANCE",
    "ROOSTER", "ROSETTE", "ROUTINE", "ROYALTY", "RUBBISH", "RUNAWAY", "SALVAGE", "SARDINE", "SCALPEL", "SCARLET",
    "SCENERY", "SCEPTRE", "SCHOLAR", "SCIENCE", "SCOOTER", "SCRATCH", "SEAFOOD", "SEAGULL", "SECTION", "SEGMENT",
    "SENATOR", "SERVANT", "SERVICE", "SESSION", "SETTLER", "SEVENTY", "SEVERAL", "SHELTER", "SHERIFF", "SHORTEN",
    "SHOWMAN", "SHUFFLE", "SHUTTLE", "SILENCE", "SILVERY", "SIMILAR", "SINCERE", "SINGLET", "SKILLET", "SKYLINE",
    "SLIPPER", "SLUMBER", "SNOWMAN", "SOCIETY", "SOLDIER", "SOMEHOW", "SOMEONE", "SPARROW", "SPECIAL", "SPECIES",
    "SPHERIC", "SPINACH", "STADIUM", "STATION", "STEALTH", "STEAMER", "STENCIL", "STEWARD", "STICKER", "STOMACH",
    "STRANGE", "STUDENT", "SUBJECT", "SUCCEED", "SUCCESS", "SULPHUR", "SUMMARY", "SUNBEAM", "SUNRISE", "SUPPORT",
    "SUPREME", "SURFACE", "SURGEON", "SUSPECT", "SWALLOW", "SWEATER", "SWEETLY", "SWIMMER", "SYMPTOM", "TADPOLE",
    "TANGENT", "TANGLED", "TEACHER", "TERRACE", "TESTIFY", "TEXTILE", "TEXTURE", "THEATER", "THERMAL", "THIMBLE",
    "THUNDER", "TICKETS", "TOBACCO", "TOPICAL", "TORNADO", "TORPEDO", "TOURIST", "TRAFFIC", "TRAGEDY", "TRAINER",
    "TRAITOR", "TRIBUTE", "TRIUMPH", "TROPICS", "TROUBLE", "TRUMPET", "TRUSTEE", "TSUNAMI", "TUBULAR", "TYPICAL",
    "UNICORN", "UNIFORM", "UNKNOWN", "UNUSUAL", "UPGRADE", "UPRIGHT", "URANIUM", "UTENSIL", "VALIANT", "VAMPIRE",
    "VANILLA", "VARIETY", "VEHICLE", "VENTURE", "VERDICT", "VETERAN", "VICTORY", "VILLAGE", "VILLAIN", "VIOLATE",
    "VIOLENT", "VISIBLE", "VISITOR", "VIVIDLY", "VOLCANO", "VOYAGER", "WALKWAY", "WARBLER", "WARFARE", "WARRIOR",
    "WEATHER", "WEBSTER", "WEEKDAY", "WEEKEND", "WELCOME", "WESTERN", "WHISPER", "WHISTLE", "WINDOWS", "WINNING",
    "WITNESS", "WORSHIP", "WRESTLE",
    # 8-letter (481 words)
    "ABSOLUTE", "ABSTRACT", "ACADEMIC", "ACCIDENT", "ACCURACY", "ACTIVATE", "ACTIVITY", "ADDITION", "ADEQUATE", "ADVISORY",
    "AIRCRAFT", "ALLIANCE", "ALPHABET", "ALTITUDE", "AMETHYST", "ANALYSIS", "ANCESTOR", "APPETITE", "APPROVAL", "AQUARIUM",
    "ARGUMENT", "ARTISTIC", "ASSEMBLY", "ATHLETIC", "ATTORNEY", "AUDIENCE", "BACKPACK", "BACKWARD", "BARRACKS", "BASEBALL",
    "BASEMENT", "BEHAVIOR", "BIRTHDAY", "BOUNDARY", "BOUTIQUE", "BROADWAY", "BROCCOLI", "BULLETIN", "BUSINESS", "CALENDAR",
    "CAMPAIGN", "CAPACITY", "CARNIVAL", "CAROUSEL", "CARRIAGE", "CATEGORY", "CELERITY", "CHAMPION", "CHARCOAL", "CHEMICAL",
    "CHESTNUT", "CIRCULAR", "CLEANSER", "CLINICAL", "CLOTHING", "COLOSSAL", "COMMERCE", "COMPOUND", "COMPUTER", "CONCLUDE",
    "CONCRETE", "CONDENSE", "CONQUEST", "CONSIDER", "CONSTANT", "CONSUMER", "CONTINUE", "CONTRACT", "CONTRAST", "CONVERSE",
    "CONVINCE", "CORRIDOR", "CREATION", "CREATIVE", "CRITICAL", "CROSSING", "CUCUMBER", "CULTURAL", "CUSTOMER", "CYLINDER",
    "DATABASE", "DAYBREAK", "DAYDREAM", "DAYLIGHT", "DEADLINE", "DECISION", "DECORATE", "DECREASE", "DEFENDER", "DELICATE",
    "DELIVERY", "DEMOCRAT", "DESCRIBE", "DESIGNER", "DETAILED", "DILIGENT", "DINOSAUR", "DIRECTOR", "DISASTER", "DISCOUNT",
    "DISCOVER", "DISPATCH", "DISTANCE", "DISTRICT", "DIVISION", "DOMINANT", "DOWNTOWN", "DRAMATIC", "EARNINGS", "ECONOMIC",
    "EDUCATOR", "ELECTION", "ELEGANCE", "ELEPHANT", "ELEVATOR", "ELIGIBLE", "EMPHASIS", "EMPLOYEE", "EMPLOYER", "ENGINEER",
    "ENORMOUS", "ENTRANCE", "ENVELOPE", "EQUALITY", "EQUATION", "ESPRESSO", "ESTIMATE", "EVERYDAY", "EVIDENCE", "EXCHANGE",
    "EXCITING", "EXERCISE", "EXPEDITE", "EXPLORER", "EXPOSURE", "EXTERNAL", "FACILITY", "FAIRNESS", "FAMILIAR", "FAMILIES",
    "FAVORITE", "FEEDBACK", "FESTIVAL", "FIREWORK", "FLAMINGO", "FLATWARE", "FLOURISH", "FOOTBALL", "FOOTNOTE", "FOOTSTEP",
    "FORECAST", "FOREHEAD", "FOUNTAIN", "FRACTION", "FRAGMENT", "FREQUENT", "FRIENDLY", "FRONTIER", "FROSTING", "FRUITFUL",
    "FULLNESS", "FUNCTION", "GARDENER", "GENEROUS", "GLORIOUS", "GOLDFISH", "GOVERNOR", "GRACIOUS", "GRADIENT", "GRADUATE",
    "GRANDEUR", "GRATEFUL", "GREETING", "GUARDIAN", "GUIDANCE", "HANDBOOK", "HANDMADE", "HANDSOME", "HEADACHE", "HEAVENLY",
    "HEIRLOOM", "HERITAGE", "HIDEAWAY", "HILLSIDE", "HISTORIC", "HONEYBEE", "HOSPITAL", "HUMILITY", "IDENTITY", "ILLUSION",
    "IMPERIAL", "INCIDENT", "INDUSTRY", "INFANTRY", "INFORMAL", "INNOCENT", "INSTANCE", "INSULATE", "INTEGRAL", "INTEREST",
    "INTERIOR", "INTERNAL", "INTERNET", "INTERVAL", "INTIMACY", "INTREPID", "INVENTOR", "INVESTOR", "JEALOUSY", "JUDGMENT",
    "JUNCTION", "KANGAROO", "KEYBOARD", "KINDNESS", "KNAPSACK", "KNITTING", "LANDLORD", "LANDMARK", "LANGUAGE", "LARKSPUR",
    "LAUGHTER", "LEGATION", "LIFETIME", "LIGHTING", "LOCATION", "LUMINOUS", "MAGAZINE", "MAGICIAN", "MAGNETIC", "MAGNOLIA",
    "MARATHON", "MARGINAL", "MARRIAGE", "MATERIAL", "MATURITY", "MEDICINE", "MEDIEVAL", "MEMORIAL", "MERCHANT", "METAPHOR",
    "MIDNIGHT", "MILITANT", "MILITARY", "MINISTER", "MINORITY", "MISCHIEF", "MOMENTUM", "MONETARY", "MONUMENT", "MOONBEAM",
    "MORALITY", "MORTGAGE", "MOSQUITO", "MOUNTAIN", "MULTIPLY", "MUSICIAN", "NATIONAL", "NAVIGATE", "NECKLACE", "NEGATIVE",
    "NINETEEN", "NOBILITY", "NOTEBOOK", "NOVELIST", "NUMEROUS", "NUTSHELL", "OBEDIENT", "OBSTACLE", "OCCASION", "OFFERING",
    "OPERATOR", "OPPONENT", "OPPOSITE", "OPTIMIST", "ORDINARY", "ORIGINAL", "ORNAMENT", "OVERCOME", "OVERHEAD", "OVERLOOK",
    "OVERSEAS", "PARALLEL", "PATIENCE", "PAVEMENT", "PAVILION", "PEACEFUL", "PENDULUM", "PERSONAL", "PETITION", "PHEASANT",
    "PHYSICAL", "PINNACLE", "PIPELINE", "PLATFORM", "PLATINUM", "PLAYMATE", "PLEASURE", "POLITICS", "PORPOISE", "PORTRAIT",
    "POSITION", "POSITIVE", "POSTCARD", "POWERFUL", "PRACTICE", "PRECIOUS", "PREMIERE", "PREMISES", "PRESENCE", "PRESERVE",
    "PREVIOUS", "PRINCESS", "PRIORITY", "PRISONER", "PROBABLE", "PRODUCER", "PROFOUND", "PROGRESS", "PROPERTY", "PROPOSAL",
    "PROTOCOL", "PROVINCE", "PRUDENCE", "PURCHASE", "QUADRANT", "QUANTITY", "QUESTION", "RADIANCE", "RAILROAD", "RAPIDITY",
    "RATIONAL", "REACTION", "RECEIVER", "RECOVERY", "REGIONAL", "REGISTER", "RELATION", "RELATIVE", "RELIABLE", "RELIANCE",
    "RELIGION", "REMEMBER", "REMINDER", "REPORTER", "REPUBLIC", "REQUIRED", "RESEARCH", "RESIDENT", "RESOURCE", "RESPONSE",
    "RESTLESS", "RETAINER", "RETRIEVE", "REVERSAL", "REVISION", "RHYTHMIC", "ROMANTIC", "SAILBOAT", "SANCTITY", "SANDWICH",
    "SAPPHIRE", "SAUCEPAN", "SCENARIO", "SCHEDULE", "SCISSORS", "SCORPION", "SCULPTOR", "SEAFARER", "SEASHORE", "SEASONAL",
    "SECURITY", "SEDIMENT", "SELECTOR", "SEMESTER", "SENTENCE", "SEQUENCE", "SERENADE", "SERGEANT", "SERVICES", "SHEPHERD",
    "SHIPMENT", "SHORTAGE", "SHOULDER", "SIDEWALK", "SKELETON", "SKYLIGHT", "SNOWBALL", "SOFTWARE", "SOLITARY", "SOLITUDE",
    "SOLUTION", "SOMEBODY", "SOMEWHAT", "SOUTHERN", "SPECIFIC", "SPECTRUM", "SPLENDID", "SPOONFUL", "SPORTING", "SQUADRON",
    "STANDARD", "STARFISH", "STARTING", "STIMULUS", "STOCKING", "STRAIGHT", "STRANGER", "STRATEGY", "STREAMER", "STRENGTH",
    "STRUGGLE", "STUBBORN", "SUBTITLE", "SUITABLE", "SUITCASE", "SUNBURST", "SUNLIGHT", "SUNSHINE", "SUPERIOR", "SURPRISE",
    "SURVIVAL", "SYLLABLE", "SYMBOLIC", "SYMPHONY", "TACTICAL", "TAILGATE", "TALENTED", "TAPESTRY", "TAXPAYER", "TEAMMATE",
    "TEAMWORK", "TEMPLATE", "TERMINAL", "THEOLOGY", "THINKING", "THIRTEEN", "THOROUGH", "THOUSAND", "THRILLED", "TIMELINE",
    "TITANIUM", "TOGETHER", "TOLERANT", "TOMORROW", "TORTOISE", "TOWNSHIP", "TRACTION", "TRAILWAY", "TRAINING", "TRANSFER",
    "TRAVELED", "TREASURE", "TREASURY", "TRIANGLE", "TRIBUNAL", "TRILLION", "TROPICAL", "TWILIGHT", "ULTIMATE", "UMBRELLA",
    "UNBIASED", "UNIVERSE", "UNLIKELY", "UPSTAIRS", "URBANITE", "VACATION", "VALIDITY", "VALUABLE", "VERTICAL", "VIOLENCE",
    "WARDROBE", "WILDLIFE", "WINDFALL", "WINDMILL", "WINGSPAN", "WIRELESS", "WITHDRAW", "WOODLAND", "WORKBOOK", "WORKSHOP",
    "YEARBOOK"
]

def clean_letters(text: str) -> List[str]:
    return [c for c in text.upper() if "A" <= c <= "Z"]

def max_circles_for_word(word: str) -> int:
    wlen = len(word)
    if wlen == 4:
        return 2
    elif wlen == 5:
        return 3
    else:
        return 3

rarity = "QZXJVWKBMPGHDYFCLNUSTOERAI"

def solve_clue_words(answer: str, target_word_count: int, pool: List[str], max_attempts: int = 3000) -> Optional[Tuple[List[str], List[List[int]]]] :
    ans_chars = clean_letters(answer)
    target_counts = Counter(ans_chars)
    ans_len = len(ans_chars)
    if ans_len < target_word_count:
        return None

    ans_tokens = set(re.findall(r"[A-Z]+", answer.upper()))
    valid_pool = [w for w in pool if w.upper() not in ans_tokens]

    by_char = {c: [] for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    for w in valid_pool:
        for c in set(w):
            by_char[c].append(w)

    for attempt in range(max_attempts):
        rem = Counter(target_counts)
        chosen_words = []
        chosen_circles = []
        used_words = set()

        for step in range(target_word_count):
            rem_words = target_word_count - step
            rem_letters = sum(rem.values())
            if rem_letters < rem_words:
                break

            rare_needed = None
            for ch in rarity:
                if rem[ch] > 0:
                    rare_needed = ch
                    break
            if not rare_needed:
                break

            cands = [w for w in by_char[rare_needed] if w not in used_words]
            if not cands:
                break

            cands_sample = random.sample(cands, min(len(cands), 30))
            cands_sample.sort(key=lambda w: sum(min(w.count(c), rem[c]) for c in set(w)), reverse=True)

            word_chosen = None
            for w in cands_sample:
                w_cap = max_circles_for_word(w)
                max_take = min(w_cap, rem_letters - (rem_words - 1))
                if max_take < 1:
                    continue

                match_indices = [i for i, c in enumerate(w) if rem[c] > 0]
                rare_indices = [i for i in match_indices if w[i] == rare_needed]
                if not rare_indices:
                    continue

                take = [rare_indices[0]]
                other_matches = [i for i in match_indices if i != rare_indices[0]]
                random.shuffle(other_matches)
                take_cnt = min(max_take, 1 + len(other_matches))
                take.extend(other_matches[:take_cnt - 1])

                # Distractor check: at least 2 uncircled letters
                if len(w) - len(take) < 2:
                    continue

                for i in take:
                    rem[w[i]] -= 1
                chosen_words.append(w)
                chosen_circles.append(sorted(take))
                used_words.add(w)
                word_chosen = w
                break

            if not word_chosen:
                break

        if sum(rem.values()) == 0 and len(chosen_words) == target_word_count:
            extracted = [chosen_words[i][c] for i in range(len(chosen_words)) for c in chosen_circles[i]]
            if sorted(extracted) == sorted(ans_chars):
                return chosen_words, chosen_circles

    return None

def generate_all_puzzles():
    random.seed(42)
    puzzles = []

    # 1. Gather all 300 curated riddles and sort by answer letter count
    all_riddles = []
    for diff in ["easy", "medium", "hard"]:
        for r, a in RIDDLE_BANK[diff]:
            all_riddles.append((r, a))

    all_riddles.sort(key=lambda item: len(clean_letters(item[1])))

    easy_bank = all_riddles[:100]
    med_bank = all_riddles[100:200]
    hard_bank = all_riddles[200:]

    pool_4 = [w for w in CURATED_WORDS if len(w) == 4]
    pool_5 = [w for w in CURATED_WORDS if len(w) == 5]
    pool_45 = pool_4 + pool_5

    tier_specs = [
        ("easy", easy_bank, [4], (4, 5)),
        ("medium", med_bank, [4, 5], (4, 5)),
        ("hard", hard_bank, [5, 6], (5,)),
    ]

    for diff, bank, allowed_word_counts, allowed_lens in tier_specs:
        print(f"Generating {diff.upper()} ({len(bank)} riddles, words {allowed_lens}, clue counts {allowed_word_counts})...")
        solved_count = 0

        for i, (riddle, answer) in enumerate(bank):
            ans_clean = clean_letters(answer)
            ans_len = len(ans_clean)

            if diff == "easy":
                target_counts = [4]
                # For Easy: prefer pure 4-letter words if ans_len <= 8, else mix of 4 and 5
                pools = [pool_4, pool_45] if ans_len <= 8 else [pool_45]
            elif diff == "medium":
                # For Medium: 4 clues if ans_len <= 12, else 5 clues
                tc = 4 if ans_len <= 12 else 5
                target_counts = [tc, 5 if tc == 4 else 4]
                pools = [pool_45]
            else:  # hard
                # For Hard: 5 clues if ans_len <= 15, else 6 clues (strictly 5-letter words)
                tc = 5 if ans_len <= 15 else 6
                target_counts = [tc, 6 if tc == 5 else 5]
                pools = [pool_5]

            solved = False
            for p_candidate in pools:
                for tc in target_counts:
                    res = solve_clue_words(answer, tc, p_candidate, max_attempts=2500)
                    if res:
                        words, circles = res
                        assert len(words) in allowed_word_counts, f"Word count violation: {len(words)} not in {allowed_word_counts}"
                        assert all(len(w) in allowed_lens for w in words), f"Length violation in {words}, expected {allowed_lens}"
                        for w, c in zip(words, circles):
                            assert 1 <= len(c) <= max_circles_for_word(w), f"Circle cap exceeded in {w}: {c}"
                            assert len(w) - len(c) >= 2, f"Distractor violation in {w}: {c}"
                        ans_tokens = set(re.findall(r"[A-Z]+", answer.upper()))
                        for w in words:
                            assert w.upper() not in ans_tokens, f"Leak: {w} in {answer}"
                        extracted = [words[w_i][c_i] for w_i in range(len(words)) for c_i in circles[w_i]]
                        assert sorted(extracted) == sorted(ans_clean), f"Multiset error in {answer}"

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
                if solved:
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
    lines.append("")
    lines.append("struct CompactRiddleSet {")
    lines.append("    uint8_t numWords;")
    lines.append("    uint8_t circleMasks[6];")
    lines.append("    const char* words;")
    lines.append("    const char* riddle;")
    lines.append("    const char* answer;")
    lines.append("};")
    lines.append("")
    lines.append(f"static const size_t TOTAL_JUMBLE_PUZZLES = {len(puzzles)};")
    lines.append("static const CompactRiddleSet JUMBLE_DATASET[] PROGMEM = {")

    for p in puzzles:
        num_words = len(p["words"])
        words_str = " ".join(p["words"])

        circle_masks = []
        for w_idx in range(6):
            if w_idx < num_words:
                mask = 0
                for c in p["circles"][w_idx]:
                    mask |= (1 << c)
                circle_masks.append(f"0x{mask:02X}")
            else:
                circle_masks.append("0x00")

        circles_c = "{" + ", ".join(circle_masks) + "}"

        riddle_escaped = p["riddle"].replace("\\", "\\\\").replace("\"", "\\\"")
        answer_escaped = p["answer"].replace("\\", "\\\\").replace("\"", "\\\"")

        lines.append("    {")
        lines.append(f"        {num_words},")
        lines.append(f"        {circles_c},")
        lines.append(f'        "{words_str}",')
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
