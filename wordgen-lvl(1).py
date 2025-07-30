#!/usr/bin/env python3

import argparse
import itertools

# Full symbol set & numbers
SYMBOLS = list("!@#$%^&*()_+-=[]{}|:;\"'<>,.?/~")
NUMBERS = [str(i) for i in range(10)]

def parse_args():
    parser = argparse.ArgumentParser(description="🐉 Kali Wordlist Generator – Ultra Mutation Mode")

    # Target details
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
    parser.add_argument("-k", help="Custom words (comma-separated)")

    # Generation options
    parser.add_argument("-min", type=int, default=6, help="Minimum password length")
    parser.add_argument("-max", type=int, default=16, help="Maximum password length")
    parser.add_argument("-o", help="Output file", default="ultra_wordlist.txt")
    parser.add_argument("-strong", action="store_true", help="Enable full strong mutation")

    return parser.parse_args()

def collect_words(args):
    words = []
    for key, val in vars(args).items():
        if val and key not in ["o", "min", "max", "strong"]:
            if key == "k":
                words.extend([w.strip() for w in val.split(",")])
            else:
                words.append(val)
    return words

def case_variants(word):
    return set([
        word.lower(),
        word.upper(),
        word.capitalize(),
        word[0].lower() + word[1:].capitalize() if len(word) > 1 else word.lower(),
        ''.join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(word)]),  # AlTeRnAtInG
    ])

def inject_symbols(word, min_len, max_len):
    injected = set()
    for i in range(1, len(word)):
        for s in SYMBOLS:
            candidate = word[:i] + s + word[i:]
            if min_len <= len(candidate) <= max_len:
                injected.add(candidate)
    return injected

def suffix_combos(word, min_len, max_len):
    combos = set()
    for sym in SYMBOLS:
        for num in NUMBERS:
            variants = [
                word + sym,
                sym + word,
                word + num,
                num + word,
                word + sym + num,
                sym + word + num,
                num + word + sym,
            ]
            for v in variants:
                if min_len <= len(v) <= max_len:
                    combos.add(v)
    return combos

def generate(words, min_len, max_len, strong):
    print(f"[+] Generating wordlist ({min_len}-{max_len}) with strong={strong} ...")
    wordlist = set()

    for i in range(1, 3):  # Combine 1 and 2 elements
        for combo in itertools.permutations(words, i):
            base = ''.join(combo)
            for variant in case_variants(base):
                if min_len <= len(variant) <= max_len:
                    wordlist.add(variant)

                if strong:
                    # Inject symbols in positions
                    wordlist.update(inject_symbols(variant, min_len, max_len))
                    # Add suffixes, prefixes, combinations
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
        print("[-] No input provided. Use -h for help.")
    else:
        final = generate(words, args.min, args.max, args.strong)
        save(final, args.o)
