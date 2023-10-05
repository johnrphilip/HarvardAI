# Analysis


# Sentence: The dog and the [MASK] played together in the yard. 
- Looking at a sentence with a compound subject
- It's interesting the first layer is very noisy with lots of shades all over, compared to the early patterns detected with the sample sentences. 

## Layer 1, Head 11

<img width="715" alt="image" src="https://github.com/johnrphilip/HarvardAI/assets/96958726/b7b296f2-a4fa-4578-89e0-d89bd320055f">

### This image seems to be paying attention to the article noun pair:
- (the -> dog)
### While also looking at the confusing verb adverb relationship of:
- (played -> together)


## Layer 2, Head 2
<img width="708" alt="image" src="https://github.com/johnrphilip/HarvardAI/assets/96958726/06cbaba2-229b-494c-8f57-1dadea0b0218">

### Still not paying attention to the noun-verb relationship fully (lighter shade) but attention again placed on:
- article -> noun pattern repeating attention but now with (the [MASK])
- still perhaps trying to figure out the noun-verb pattern and showing more attention again on the
- verb -> adjective (played -> together)


## Layer 2, Head 5
<img width="703" alt="image" src="https://github.com/johnrphilip/HarvardAI/assets/96958726/42afbf7f-a11d-4fa6-9456-1d5fdbab230b">

### Looking at reverse relationships (the word before)
- Seems to really be coming along with understanding "the" relationships:
- Strong colour with (the - [CLS]








### Later 1, Head 11
- (up -> picked), (from -> [MASK]), 
  
- <img width="610" alt="image" src="https://github.com/johnrphilip/HarvardAI/assets/96958726/fd1c33f3-b38b-4594-9c1d-f474f422f8a3">




## This layer seems to demonstrate looking at relationships of the word following the focus word:

- ("." -> [SEP]), (picked -> up), (the -> table)
### Layer 1, Head 11
Attention_Layer1_Head11
![image](https://github.com/johnrphilip/HarvardAI/assets/96958726/003991df-7505-41ee-8a93-c784b4c41772)

#### Punctuation and [SEP}
- In this image you can see attention patterns between Punctuation "." and [SEP].
- The model may be using boundary and structural information to predict the mask.


#### Phrasal Verb or DO
- There is attention between "picked" and "up"
- This recognition may be for the phrasal verb "picked up", or it could be interpreting it as a direct object.

#### Article-Noun Pair
- Here you can see attention being placed between the and article and a noun
- This recognition may be important for ultimately understanding the mask which works within an article noun relationship. 

## This layer seems to be looking at the relationship of words before the focus word:

### Later 1, Head 3
- (up -> picked), (from -> [MASK]), 
  
- <img width="610" alt="image" src="https://github.com/johnrphilip/HarvardAI/assets/96958726/fd1c33f3-b38b-4594-9c1d-f474f422f8a3">

#### Phrasal Verb or DO  (up -> picked)
- Similar as above but perhaps looking backwards within the phrasal verb relationship

#### Adjective Prepositional Phrase
- Here the attention could be looking at the start of the preposition looking back at the noun it modifies




TODO

Example Sentences:
- TODO
- TODO

## Layer TODO, Head TODO

TODO

Example Sentences:
- TODO
- TODO




[Title](<Then I picked up a [MASK] from the table.>)

Attention_Layer3_Head1.png

Attention_Layer1_Head11
![image](https://github.com/johnrphilip/HarvardAI/assets/96958726/003991df-7505-41ee-8a93-c784b4c41772)


