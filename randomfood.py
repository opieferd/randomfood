
import random
import re
from difflib import SequenceMatcher

import requests

print(r"""                                                        ___       ___                    .-.                            ___  
                                                       (   )     (   )                  /    \                         (   ) 
  .--.    ___  ___    .--.       .--.        .--.       | |_      | | .-.     .--.      | .`. ;    .--.     .--.     .-.| |  
 /    \  (   )(   )  /    \    /  _  \     /  _  \     (   __)    | |/   \   /    \     | |(___)  /    \   /    \   /   \ |  
;  ,-. '  | |  | |  |  .-. ;  . .' `. ;   . .' `. ;     | |       |  .-. .  |  .-. ;    | |_     |  .-. ; |  .-. ; |  .-. |  
| |  | |  | |  | |  |  | | |  | '   | |   | '   | |     | | ___   | |  | |  |  | | |   (   __)   | |  | | | |  | | | |  | |  
| |  | |  | |  | |  |  |/  |  _\_`.(___)  _\_`.(___)    | |(   )  | |  | |  |  |/  |    | |      | |  | | | |  | | | |  | |  
| |  | |  | |  | |  |  ' _.' (   ). '.   (   ). '.      | | | |   | |  | |  |  ' _.'    | |      | |  | | | |  | | | |  | |  
| '  | |  | |  ; '  |  .'.-.  | |  `\ |   | |  `\ |     | ' | |   | |  | |  |  .'.-.    | |      | '  | | | '  | | | '  | |  
'  `-' |  ' `-'  /  '  `-' /  ; '._,' '   ; '._,' '     ' `-' ;   | |  | |  '  `-' /    | |      '  `-' / '  `-' / ' `-'  /  
 `.__. |   '.__.'    `.__.'    '.___.'     '.___.'       `.__.   (___)(___)  `.__.'    (___)      `.__.'   `.__.'   `.__,'   
 ( `-' ;                                                                                                                      
  `.__.                                                                                                                      
 ___                                                       .-.                               ___                             
(   )                                      .-.            /    \                            (   )                            
 | |.-.    ___  ___      .--.      .-..   ( __)   .--.    | .`. ;    .--.    ___ .-.      .-.| |                             
 | /   \  (   )(   )    /    \    /    \  (''")  /    \   | |(___)  /    \  (   )   \    /   \ |                             
 |  .-. |  | |  | |    |  .-. ;  ' .-,  ;  | |  |  .-. ;  | |_     |  .-. ;  | ' .-. ;  |  .-. |                             
 | |  | |  | |  | |    | |  | |  | |  . |  | |  |  | | | (   __)   |  | | |  |  / (___) | |  | |                             
 | |  | |  | '  | |    | |  | |  | |  | |  | |  |  |/  |  | |      |  |/  |  | |        | |  | |                             
 | |  | |  '  `-' |    | |  | |  | |  | |  | |  |  ' _.'  | |      |  ' _.'  | |        | |  | |                             
 | '  | |   `.__. |    | '  | |  | |  ' |  | |  |  .'.-.  | |      |  .'.-.  | |        | '  | |                             
 ' `-' ;    ___ | |    '  `-' /  | `-'  '  | |  '  `-' /  | |      '  `-' /  | |        ' `-'  /                             
  `.__.    (   )' |     `.__.'   | \__.'  (___)  `.__.'  (___)      `.__.'  (___)        `.__,'                              
            ; `-' '              | |                                                                                         
             .__.'              (___)                                                                                        """)
def choose_game_mode():
    while True:
        try:
            mode = input("Do you want to play hard mode or easy mode? (hard/easy): ")
        except KeyboardInterrupt:
            print("\nBRO REALLY QUIT")
            print("imagine being scared of a food")
            return None

        mode = mode.strip().casefold()
        if mode in {"hard", "easy"}:
            return mode

        print("please choose hard or easy")


API_URL = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": "food-guess-game/1.0 (educational project) dont block me im human"
}


EXCLUDED_TITLES = {
    "food",
    "dish",
    "meal",
    "snack",
    "beverage",
    "drink",
    "cuisine",
    "recipe",
}

EXCLUDED_TITLE_PREFIXES = (
    "list of ",
    "lists of ",
)

FOOD_DESCRIPTION_MARKERS = (
    "food",
    "dish",
    "cuisine",
    "meal",
    "ingredient",
    "sauce",
    "dessert",
    "beverage",
    "bread",
    "meat",
    "seafood",
    "fish",
    "fruit",
    "vegetable",
    "grain",
    "noodle",
    "rice",
    "cake",
    "drink",
    "snack",
    "cheese",
    "soup",
    "stew",
)

NON_FOOD_DESCRIPTION_MARKERS = (
    "television",
    "tv series",
    "television series",
    "film",
    "movie",
    "book",
    "novel",
    "magazine",
    "album",
    "song",
    "video game",
    "restaurant",
    "company",
    "brand",
    "chain",
    "chef",
    "cookbook",
    "program",
    "show",
    "festival",
    "industry",
    "history",
    "culture",
    "science",
    "technology",
    "policy",
    "law",
)

COMMON_FOODS = (
    "pizza",
    "burger",
    "hot dog",
    "french fries",
    "sandwich",
    "taco",
    "burrito",
    "quesadilla",
    "nachos",
    "spaghetti",
    "lasagna",
    "macaroni and cheese",
    "ravioli",
    "ramen",
    "fried rice",
    "sushi",
    "curry",
    "chicken soup",
    "tomato soup",
    "chili",
    "steak",
    "fried chicken",
    "roast chicken",
    "meatloaf",
    "meatballs",
    "bacon",
    "sausage",
    "scrambled eggs",
    "omelette",
    "pancake",
    "waffle",
    "french toast",
    "oatmeal",
    "cereal",
    "toast",
    "bagel",
    "pasta salad",
    "caesar salad",
    "coleslaw",
    "mashed potato",
    "baked potato",
    "potato salad",
    "onion rings",
    "garlic bread",
    "cornbread",
    "bread",
    "white rice",
    "beans",
    "soup",
    "hummus",
    "falafel",
    "guacamole",
    "salsa",
    "apple",
    "banana",
    "orange",
    "strawberry",
    "grape",
    "watermelon",
    "pineapple",
    "mango",
    "peach",
    "pear",
    "cherry",
    "blueberry",
    "raspberry",
    "carrot",
    "broccoli",
    "spinach",
    "lettuce",
    "tomato",
    "cucumber",
    "pickle",
    "popcorn",
    "potato chip",
    "pretzel",
    "peanut butter",
    "peanut",
    "almond",
    "yogurt",
    "cheese",
    "ice cream",
    "chocolate",
    "cookie",
    "brownie",
    "cake",
    "doughnut",
    "pie",
    "cheesecake",
    "pudding",
    "jelly",
    "jam",
    "apple sauce",
    "ketchup",
    "mayonnaise",
    "mustard",
    "hot chocolate",
    "coffee",
    "tea",
    "lemonade",
)


def get_wikitext(session, page):
    params = {
        "action": "parse",
        "page": page,
        "prop": "wikitext",
        "format": "json",
    }

    response = session.get(
        API_URL,
        headers=HEADERS,
        params=params,
        timeout=10,
    )

    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After", "a few")
        raise requests.HTTPError(
            f"wiki is being stupid and rate limited you. Try again in {retry_after} seconds."
        )

    response.raise_for_status()
    data = response.json()
    if "error" in data:
        raise requests.HTTPError(
            f"Wiki is stupid and sent API error: {data['error'].get('info', 'unknown error')}"
        )

    try:
        return data["parse"]["wikitext"]["*"]
    except KeyError as error:
        raise requests.HTTPError(
            f"Wiki returned no wikitextfor {page!r}."
        ) from error


def get_top_level_links(wikitext):
    links = []
    link_pattern = re.compile(r"^\* +\[\[:?([^|\]#]+)")
    for line in wikitext.splitlines():
        match = link_pattern.match(line)
        if match:
            links.append(match.group(1).strip())
    return links


def get_food_descriptions(session, foods):
    if not foods:
        return {}

    params = {
        "action": "query",
        "prop": "extracts",
        "titles": "|".join(foods),
        "exintro": "1",
        "explaintext": "1",
        "redirects": "1",
        "format": "json",
    }
    response = session.get(
        API_URL,
        headers=HEADERS,
        params=params,
        timeout=10,
    )

    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After", "a few")
        raise requests.HTTPError(
            f"wiki is being stupid and rate limited you. Try again in {retry_after} seconds."
        )

    response.raise_for_status()
    data = response.json()
    if "error" in data:
        raise requests.HTTPError(
            f"Wiki is stupid and sentAPI error: {data['error'].get('info', 'unknown error')}"
        )

    descriptions = {}
    for page in data["query"]["pages"].values():
        description = page.get("extract", "").strip()
        if description:
            descriptions[page["title"]] = description
    return descriptions


def is_edible_food_from_description(title, description):
    title_lower = title.casefold()
    if (
        title_lower in EXCLUDED_TITLES
        or title_lower.startswith(EXCLUDED_TITLE_PREFIXES)
        or "(disambiguation)" in title_lower
    ):
        return False

    description = description.casefold()
    if not description:
        return False

    introduction = re.split(r"(?<=[.!?])\s+", description, maxsplit=1)[0]
    if any(
        re.search(rf"\b{re.escape(marker)}\b", introduction)
        for marker in NON_FOOD_DESCRIPTION_MARKERS
    ):
        return False

    return any(
        re.search(rf"\b{re.escape(marker)}\b", introduction)
        for marker in FOOD_DESCRIPTION_MARKERS
    )


def get_random_food(session, mode):
    if mode == "easy":
        return random.choice(COMMON_FOODS)

    prepared_foods = get_wikitext(session, "Lists of prepared foods")
    list_pages = [
        title
        for title in get_top_level_links(prepared_foods)
        if title.casefold().startswith("list of ")
    ]
    if not list_pages:
        raise ValueError("Wiki is being stupid and returned no prepared food lists.")

    selected_list = random.choice(list_pages)
    list_wikitext = get_wikitext(session, selected_list)
    pages = get_top_level_links(list_wikitext)
    foods = [
        title
        for title in pages
        if title.casefold() not in EXCLUDED_TITLES
    ]
    random.shuffle(foods)
    foods = foods[:20]
    descriptions = get_food_descriptions(session, foods)

    for food in foods:
        if is_edible_food_from_description(
            food,
            descriptions.get(food, ""),
        ):
            return food

    raise ValueError("Wiki is being stupid and did not return an edible food.")


def get_food_description(session, food):
    params = {
        "action": "query",
        "prop": "extracts",
        "titles": food,
        "exintro": "1",
        "explaintext": "1",
        "redirects": "1",
        "format": "json",
    }

    response = session.get(
        API_URL,
        headers=HEADERS,
        params=params,
        timeout=10,
    )
    response.raise_for_status()

    pages = response.json()["query"]["pages"]
    page = next(iter(pages.values()))
    description = page.get("extract", "").strip()

    if not description:
        raise ValueError(f"Wikipedia has no description for {food!r}.")

    return description


def normalize_guess(guess):
    return re.sub(r"[^a-z]", "", guess.casefold())


def is_correct_guess(guess, food):
    normalized_guess = normalize_guess(guess)
    normalized_food = normalize_guess(food)
    if not normalized_guess or not normalized_food:
        return False

    if normalized_guess == normalized_food:
        return True

    return SequenceMatcher(None, normalized_guess, normalized_food).ratio() >= 0.8


def get_food_hints(session, food):
    description = get_food_description(session, food)
    sentences = re.split(r"(?<=[.!?])\s+", description)
    food_lower = food.casefold()

    safe_sentences = []
    seen_sentences = set()
    for sentence in sentences:
        sentence = sentence.strip()
        normalized_sentence = sentence.casefold()
        if (
            sentence
            and food_lower not in normalized_sentence
            and normalized_sentence not in seen_sentences
        ):
            safe_sentences.append(sentence)
            seen_sentences.add(normalized_sentence)

    if len(safe_sentences) >= 2:
        return tuple(random.sample(safe_sentences, 2))

    first_hint = safe_sentences[0] if safe_sentences else ""

    redacted_description = re.sub(
        re.escape(food),
        "this food",
        description,
        flags=re.IGNORECASE,
    ).strip()
    if not first_hint and redacted_description and redacted_description.casefold() != food_lower:
        first_hint = redacted_description

    if not first_hint:
        first_hint = (
            "the food has a description, but this clue had no hints that "
            "wouldnt give it away. sorry :("
        )

    second_hint = (
        "the food has a description, but this clue had no hints that "
                    "wouldnt give it away. sorry :("
    )
    return first_hint, second_hint


def guess_food():
    game_mode = choose_game_mode()
    if game_mode is None:
        return

    failed_hard_rounds = 0
    streak = 0

    with requests.Session() as session:
        while True:
            try:
                food = get_random_food(session, game_mode)

            except (requests.RequestException, ValueError) as error:
                print(f"Wiki is being stupid and request failed: {error}")

                try:
                    try_again = input("try again? (y/n): ").strip().casefold()
                except KeyboardInterrupt:
                    print("\nBRO REALLY QUIT")
                    print("imagine being scared of a food")
                    return

                if try_again == "y":
                    continue

                print("\nBRO REALLY QUIT")
                print("imagine being scared of a food")
                return

            print("\nWiki chose a food.")
            print("good luck... youll need it hehehehe >:3")

            try:
                first_hint, second_hint = get_food_hints(session, food)
                print(f"hint: {first_hint}")

            except (requests.RequestException, ValueError):
                first_hint = second_hint = None
                print("the food has a description, but this clue had no hints that "
                      "wouldnt give it away. sorry :(")

            try:
                guess = input("guess the food: ").strip().casefold()

            except KeyboardInterrupt:
                print("\nBRO REALLY QUIT")
                print("imagine being scared of a food")
                return

            if guess == "skip":
                continue

            if guess == "test":
                print("\n--- Wikipedia: Test ---")

                try:
                    print(get_food_description(session, "Test"))

                except (requests.RequestException, ValueError):
                    print("this word has no description")

                return

            if is_correct_guess(guess, food):
                streak += 1
                print("ur a smart cookie u got it")
                print("\n--- Wikipedia ---")

                try:
                    print(get_food_description(session, food))

                except (requests.RequestException, ValueError):
                    print("this food has no description")

                if streak > 1:
                    print(f"~~~ nice u got {streak} right in a row!!! 🔥~~~")

                try:
                    keep_playing = input("keep playing? (y/n): ").strip().casefold()
                except KeyboardInterrupt:
                    print("\nBRO REALLY QUIT")
                    print("imagine being scared of a food")
                    return

                if keep_playing != "y":
                    if keep_playing == "n":
                        print("ok bye")
                    else:
                        print("\nBRO REALLY QUIT")
                        print("imagine being scared of a food")
                    return

                failed_hard_rounds = 0
                continue

            print("nope u stupid")
            print("you have one more attempt")

            if second_hint is not None:
                print(f"hint: {second_hint}")
            else:
                print("the food has a description, but this clue had no hints that "
                      "wouldnt give it away. sorry :(")

            try:
                second_guess = input("guess the food: ").strip().casefold()

            except KeyboardInterrupt:
                print("\nBRO REALLY QUIT")
                print("imagine being scared of a food")
                return

            if second_guess == "skip":
                continue

            if is_correct_guess(second_guess, food):
                streak += 1
                print("ur a smart cookie u got it")
                print("\n--- Wikipedia ---")

                try:
                    print(get_food_description(session, food))

                except (requests.RequestException, ValueError):
                    print("this food has no description")

                if streak > 1:
                    print(f"~~~ nice u got {streak} right in a row!!! 🔥~~~")

                try:
                    keep_playing = input("keep playing? (y/n): ").strip().casefold()
                except KeyboardInterrupt:
                    print("\nBRO REALLY QUIT")
                    print("imagine being scared of a food")
                    return

                if keep_playing != "y":
                    if keep_playing == "n":
                        print("ok bye")
                    else:
                        print("\nBRO REALLY QUIT")
                        print("imagine being scared of a food")
                    return

                failed_hard_rounds = 0
                continue

            print("nope u stupid")
            print(f"the food was: {food}")
            lost_streak = streak > 0
            if lost_streak:
                print(" LMAO U LOST UR STREAK")
            streak = 0

            if game_mode == "hard":
                failed_hard_rounds += 1
                if failed_hard_rounds == 5:
                    try:
                        switch_to_easy = input(
                            "ur doing terrible do u want to switch to easy mode (y/n)"
                        ).strip().casefold()
                    except KeyboardInterrupt:
                        print("\nBRO REALLY QUIT")
                        print("imagine being scared of a food")
                        return

                    if switch_to_easy == "y":
                        game_mode = "easy"
                    failed_hard_rounds = 0

            try:
                keep_playing = input("keep playing? (y/n): ").strip().casefold()

            except KeyboardInterrupt:
                print("\nBRO REALLY QUIT")
                print("imagine being scared of a food")
                return

            if keep_playing != "y":
                print("\nBRO REALLY QUIT")
                print("imagine being scared of a food")
                return

            if lost_streak:
                game_mode = choose_game_mode()
                if game_mode is None:
                    return

guess_food()