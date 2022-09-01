# Author: Ahmed Adel Attia  
# Date: DATE SUBMITTED

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize

class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()
        
    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """
        try:
            sounds = self._pronunciations[word][0]
            n_syl = 0
            for s in sounds:
                if s[-1].isdigit():
                    n_syl += 1
            return n_syl
        except KeyError:
            return 1    

    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """
        
        try:
            sounds_a = self._pronunciations[a]
            sounds_b = self._pronunciations[b]
        except KeyError:
            return False

        if not sounds_a[0][0][-1].isdigit():
            sounds_a = [s[1:] for s in sounds_a]


        if not sounds_b[0][-1].isdigit():
            sounds_b = [s[1:] for s in sounds_b]

        rhyme = False
        
        for s_a in sounds_a:
            for s_b in sounds_b:
                min_len = min(len(s_a), len(s_b))
                slice_to_compare_a = s_a[-min_len:]
                slice_to_compare_b = s_b[-min_len:]
                if slice_to_compare_a == slice_to_compare_b:
                    rhyme = True
        return rhyme
    
    #Extra Credit Functions
                        
    def guess_syllables(self, word):
        """refence: https://www.howmanysyllables.com/syllable_rules/howtocountsyllables, The Written Method Rules"
        This function passes the hidden and public tests when used instead of num_syllables"""
        vowels = ["a", 'e', 'i', 'o', 'u']
        dipthongs_tripthongs = ["au", "oy", "oo"]
        n_syl = 0
        
        for v in vowels:
            if v in word:
                n_syl+=word.count(v)
                
        for d in dipthongs_tripthongs:
            if d in word:
                n_syl-word.count(d)
                
        if word[-1] == 'e':
            n_syl-=1
            
        if "y" in word:
            y_idx = word.index("y")
            if word[y_idx-1] not in vowels:
                if y_idx < len(word) -1:
                    if word[y_idx-1] not in vowels:
                        n_syl+=1
                else:
                        n_syl+=1
                    
                
        if word[-2:] == 'le':
            if word[-3] not in vowels:
                n_syl+=1
                
        return n_syl
            
    def apostrophe_tokenize(self, line):
        """
        I noticed that the pronunciation dictionary contained entries to "doesn't", "can't", "don't", "wouldn't"..., etc. The problem is that
        word_tokenize splits these words into "does" and "n't". Actually, aside from this bug/feature, word_tokenize doesn't do anything different from
        string.split(" "), other than output periods and commas separately (which I actually had to remove before calling tokenize). So, the solution is 
        to simply split the string using the delimiter " ".
        This function passes the hidden and public tests when used instead of num_syllables
        """
        line = line.split(" ")
        return line

    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other (and not the A
        lines).

        (English professors may disagree with this definition, but that's what
        we're using here.)
        """
        text = text.strip()
        lines = text.split("\n")
        
        if len(lines) !=5 :
            return False
        
        # lines_dict = {}
        last_words = []
        for i,line in enumerate(lines):
            # lines_dict[str(i)] = {"string": line, "last_word": word_tokenize(line)[-1]}
            line = line.translate(line.maketrans("", "", ".,':;!?"))
            last_words.append(word_tokenize(line)[-1])
        if self.rhymes(last_words[0], last_words[1]) and self.rhymes(last_words[0], last_words[4]):
            if self.rhymes(last_words[2], last_words[3]):
                return True
        
        return False
            
            
        
        

if __name__ == "__main__":
    ld = LimerickDetector()
    print(ld.guess_syllables("letter"))
    exit()
    buffer = ""
    inline = " "
    while inline != "":
        buffer += "%s\n" % inline
        inline = input()
        

    ld = LimerickDetector()
    print("%s\n-----------\n%s" % (buffer.strip(), ld.is_limerick(buffer)))
