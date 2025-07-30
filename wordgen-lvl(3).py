#!/usr/bin/env python3

import argparse
import itertools

SYMBOLS = list("!@#$%^&*()_+-=[]{}|:;\"'<>,.?/~")
NUMBERS = [str(i) for i in range(0, 10001)]  # 0 to 10000

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
