import random
from typing import List
from copy import deepcopy
from konlpy.tag import Mecab


def morphs_except_specialToken(text, morph_func, special_tokens):
    text_list = text.split()
    morph_list = []
    for word in text_list:
        if word in special_tokens:
            morph_list.extend([word, " "])
        else:
            words = morph_func(word)
            morph_list.extend([*words, " "])
    morph_list.pop()  # delete last space
    return morph_list


class AEDA:
    def __init__(
        self,
        special_tokens=["[SEP]", "[CLS]"],
        punc_ratio=0.3,
        random_punc=True,
        punc_list=[".", ",", ";", ":", "?", "!"],
    ):
        self.tag = Mecab()
        self.special_tokens = special_tokens
        self.punc_ratio = punc_ratio
        self.random_punc = random_punc
        self.punc_list = punc_list

    def __call__(self, *args, **kwds):
        return self.aeda(*args, **kwds)

    def aeda(self, text: str, add_special_tokens: List[str] = []) -> str:
        special_tokens = deepcopy(self.special_tokens) + add_special_tokens
        punc_ratio = self.punc_ratio

        morph_list = morphs_except_specialToken(text, self.tag.morphs, special_tokens)

        aug_word_index_list = [
            index for index in range(len(morph_list)) if morph_list[index] != " "
        ]
        punc_num = (
            random.randint(1, int(punc_ratio * len(aug_word_index_list) + 1))
            if self.random_punc
            else int(punc_ratio * len(aug_word_index_list) + 1)
        )

        aug_word_index_list = random.sample(aug_word_index_list, punc_num)

        for index in range(len(morph_list)):
            if index in aug_word_index_list:
                aug = " " + random.choice(self.punc_list) + " "
                if random.random() < 0.5:
                    morph_list.insert(index, aug)
                else:
                    morph_list.insert(index + 1, aug)

        return "".join(morph_list)


text = "이 주변에 맛집이 어디 있나요? [SEP] 그 맛집은 맛있나요?"

aeda = AEDA()
for i in range(10):
    print(aeda(text))
