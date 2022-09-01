from cicada.liberprimus import LiberPrimus

for i, page in enumerate(LiberPrimus):
    for word in page.replace("\n", "").split(" "):
        if len(word) >= 13:
            first_letter_idx = page.replace("\n", "").find(word)
            print(i, len(word), first_letter_idx, word)
