def word_matcher(word, entry):
        if entry == word: # Normal Search for upper case and leading or ending blankspaces
            # print("100% match") 
            return True

        else: # Complex Search by accuracy method
            '''
            1. This one compares letters of both word and entry and get the accuracy of commoness. 
            2. It also tries to guess the entry by adding a whitespace if the entry has a letter less types in between but rest is correct.
            3. If the user typed correctly the word but added few letters at last then it will decrease the accuracy/match% by the amount of letters added.
            
            (TO ADD)    
            4. If the user entered some random letters at the start but then typed everything 
            correctly then it will decrease accuracy by the amount of letters added.
            5. Fix for 'word' if enterd 'worf' then it recognises but for 'worfd' it can't.
            '''

            def chk(word,entry):
                common = 0
                try:
                    bigger = max(len(entry),len(word))
                    for i in range(bigger):
                        # print(word[i], entry[i])
                        if word[i] == entry[i]: common += 1
                        elif i < bigger-1: # guessing if one or 2 letters are wrong
                            if len(word) != len(entry): entry = entry[:i]+' '+entry[i:]
                except IndexError: pass
                except: pass
                return common, bigger
            (common, bigger) = chk(word, entry)
            match = 100 * common/bigger
            
            if bigger-common < 3 and match > 70: # Pass criterial unique letters < 3 and match > 70%
                return True # Pass
            else: 
                return False # Fail


if __name__ == "__main__":
    word = "word".strip().lower()
    print(word)

    entry = input("Enter word : ").lower().strip()
    print(entry)

    print(word_matcher(word, entry))
    