[한국어 문서](./README_ko.md)

# KoAEDA

Using Korean Language AEDA Easily

# Install

```zsh
  $ pip install koaeda

  $ sudo apt-get install g++ openjdk-8-jdk python3-dev python3-pip curl

  $ bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
```

# How to use

## Basic use

```python
  from koaeda import AEDA

  ko_aeda = AEDA()

  text = "이 주변에 맛집이 어디 있나요?"

  result = ko_aeda(text)

  print(result)
  >> 이 ?  주변에  : 맛집이 ;  어디 있나요?
```

## Include Special tokens

if you want not to aeda some words, Try this.

```python
  from koaeda import AEDA

  ko_aeda = AEDA()
  ko_aeda_special = AEDA(special_tokens=["[SEP]"])
  text = "이 주변에 맛집이 어디 있나요? [SEP] 그 맛집은 맛있나요?"

  result = ko_aeda(text)
  result_special = ko_aeda_special

  print(result)
  >> 이 ?  주변에  : 맛집이 ;  어디 있나요? [ : SEP ? ] 그 :  맛집은 :  맛있나요?

  print(result_special)
  >> 이 주변에 맛집이 어디 있나요 ? ?  : [SEP] 그 맛집은 !  ;  맛있나요?
```
