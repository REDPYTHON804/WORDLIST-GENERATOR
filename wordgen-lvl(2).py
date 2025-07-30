#!/usr/bin/env python3

import argparse
import itertools

SYMBOLS = list("!@#$%^&*()_+-=[]{}|:;\"'<>,.?/~")

NUMBERS = list(set([
    # 0–10
    *map(str, range(0, 11)),

    # Palindromic numbers
    '101','111','121','131','141','151','161','171','181','191',
    '202','212','222','232','242','252','262','272','282','292',
    '303','313','323','333','343','353','363','373','383','393',
    '404','414','424','434','444','454','464','474','484','494',
    '505','515','525','535','545','555','565','575','585','595',
    '606','616','626','636','646','656','666','676','686','696',
    '707','717','727','737','747','757','767','777','787','797',
    '808','818','828','838','848','858','868','878','888','898',
    '909','919','929','939','949','959','969','979','989','999',

    # Repeating/double/triple
    '11','22','33','44','55','66','77','88','99',
    '111','222','333','444','555','666','777','888','999',

    # Prime (near 100)
    '97','101','103','107','109','113','127','131','137','139','149',

    # Special patterns
    '123','234','345','456','567','678','789','890',
    '321','432','543','654','765','876','987',
    '369','420','505','606','707','808','909',

    # Mirrored/pattern
    '121','232','343','454','565','676','787','898',

    # Common 4-digit codes
    '1001','1212','1313','1414','1515','1999','2002',
    '2112','2121','2222','2323','2424','2525','3003','3131',
    '3333','4004','4040','4141','4444','5050','5252','5555',
    '5656','6006','6060','6666','7007','7171','7777','8008',
    '8080','8888','9009','9090','9119','9211','9292','9393',
    '9494','9595','9696','9797','9898','9999',

    # Repeated patterns
    '1122','2233','3344','4455','5566','6677','7788',
    '8899','9900','1234','4321','6789','9876','2468',
    '1357','1020','2020',

    # Angel/lucky numbers
    '1111','2222','3333','4444','5555','6666','7777','8888','9999',
    '1212','1313','1414','1515','1717','1818','1919','2020',

    # Mobile-like patterns
    '0311','0321','0333','0345','0300','0301','0302','0312',
    '0340','0355','0366','0399','0400','0420','0444','0500',
    '0515','0606','0707','0808','0900','0911','0922','0933',
    '0944','0955','0966','0977','0988','0999'
]))


def parse_args():
    parser = argparse.ArgumentParser(description="🐉 Kali Wordlist Generator – ULTRA Mutator")

    # Target fields
    parser.add_argument("-u", help="Username")
    parser.add_argument("-f", help="Full name")
    parser.add_argument("-n", help="Nickname")
    parser.add_argument("-p", help="Pet name")
    parser.add_argument("-s", help="School")
    parser.add_argument("-c", help="City")
    parser.add_argument("-y", help="Birth year")
    parser.add_argument("-d", help="Birth date (e.g. 17061995)")
    parser.add_argument("-a", help="Partner name")
    parser.add_argument("-l", help="Lucky number")
    parser.add_argument("-k", help="Custom keywords (comma-separated)")

    # Options
    parser.add_argument("-min", type=int, default=6, help="Minimum length")
    parser.add_argument("-max", type=int, default=16, help="Maximum length")
    parser.add_argument("-o", help="Output filename", default="ultra_wordlist.txt")
    parser.add_argument("-strong", action="store_true", help="Enable full symbol/number injection")

    return parser.parse_args()

def collect_words(args):
    words = []
    for key, val in vars(args).items():
        if val and key not in ["o", "min", "max", "strong"]:
            if key == "k":
                words.extend([x.strip() for x in val.split(",")])
            else:
                words.append(val)
    return words

def case_variants(word):
    return set([
        word.lower(),
        word.upper(),
        word.capitalize(),
        ''.join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(word)])
    ])

def inject_symbols(word, min_len, max_len):
    injected = set()
    for i in range(1, len(word)):
        for s in SYMBOLS:
            candidate = word[:i] + s + word[i:]
            if min_len <= len(candidate) <= max_len:
                injected.add(candidate)
    return injected

def inject_numbers(word, min_len, max_len):
    injected = set()
    for num in NUMBERS:
        # Optimize: skip if too long
        if len(word) + len(num) > max_len:
            continue
        injected.update([
            num + word,
            word + num
        ])
    return injected

def suffix_combos(word, min_len, max_len):
    combos = set()
    for sym in SYMBOLS:
        for num in NUMBERS:
            part = f"{sym}{num}"
            if len(word) + len(part) > max_len:
                continue
            variants = [
                word + part,
                part + word,
                word[:len(word)//2] + part + word[len(word)//2:]
            ]
            for v in variants:
                if min_len <= len(v) <= max_len:
                    combos.add(v)
    return combos

def generate(words, min_len, max_len, strong):
    print(f"[+] Generating wordlist ({min_len}-{max_len}) with strong={strong}...")
    wordlist = set()

    for i in range(1, 3):
        for combo in itertools.permutations(words, i):
            base = ''.join(combo)
            for variant in case_variants(base):
                if min_len <= len(variant) <= max_len:
                    wordlist.add(variant)

                if strong:
                    wordlist.update(inject_symbols(variant, min_len, max_len))
                    wordlist.update(inject_numbers(variant, min_len, max_len))
                    wordlist.update(suffix_combos(variant, min_len, max_len))

    return sorted(wordlist)

def save(wordlist, filename):
    with open(filename, "w") as f:
        for w in wordlist:
            f.write(w + "\n")
    print(f"\n[✓] Saved: {filename} ({len(wordlist)} entries)")
    print("[Preview]")
    print("\n".join(wordlist[:10]) + "\n...")

if __name__ == "__main__":
    args = parse_args()
    words = collect_words(args)

    if not words:
        print("[-] No input provided. Use -h.")
    else:
        final_list = generate(words, args.min, args.max, args.strong)
        save(final_list, args.o)
