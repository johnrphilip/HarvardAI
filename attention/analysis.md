# Analysis


# Sentence: The dog and the [MASK] played together in the yard. 
- Looking at a sentence with a compound subject
- It's interesting the first layer is very noisy, with lots of shades all over, compared to the early patterns detected with the sample sentences. 

## Layer 1, Head 11

<img width="715" alt="image" src="https://github.com/johnrphilip/HarvardAI/assets/96958726/b7b296f2-a4fa-4578-89e0-d89bd320055f">

### This image seems to be paying attention to the article noun pair:
- (the -> dog)
### While also looking at the confusing verb-adverb relationship of:
- (played -> together)


## Layer 2, Head 2
<img width="708" alt="image" src="https://github.com/johnrphilip/HarvardAI/assets/96958726/06cbaba2-229b-494c-8f57-1dadea0b0218">

### Still not paying attention to the noun-verb relationship fully (lighter shade) but attention again placed on:
- article -> noun pattern repeating attention but now with (the [MASK])
- still perhaps trying to figure out the noun-verb pattern and showing more attention again to the
- verb -> adjective (played -> together)


## Layer 2, Head 5
<img width="703" alt="image" src="https://github.com/johnrphilip/HarvardAI/assets/96958726/42afbf7f-a11d-4fa6-9456-1d5fdbab230b">

### Looking at reverse relationships (the word before)
- Seems to really be coming along with understanding "the" relationships:
- Strong colour with (the - [CLS]) indicating that 'the' has caught the attention of the special classificaiton token. (and -> the) has strong attention as well along with (the - in)


## Layer 3, Head 1
<img width="711" alt="image" src="https://github.com/johnrphilip/HarvardAI/assets/96958726/495c684f-16f4-4df6-bfcb-368e46679bc4">

### Here a pattern seems to have been identified, with a clear diagonal line of attention. Similar diagonal attention bars found at L3.H10, 

## Layer 3, Head 7
<img width="725" alt="image" src="https://github.com/johnrphilip/HarvardAI/assets/96958726/00ab237e-2399-446e-bd17-34e9c063dd0a">

- The model seems to be paying attention to the words themselves with lots of noise all over. This may be looking at larger/broader contexts of meaning for the words:
- (dog -> dog), (played -> played), (in -> in)


## Layer 4, Head 10
<img width="708" alt="image" src="https://github.com/johnrphilip/HarvardAI/assets/96958726/ec1cf538-1c76-4b83-a284-df8fab9ff8ab">

- Again strong attention placed on determinant -> noun patterns. It still may be confusing/weighing how played together works. I still haven't seen a focus between dog and played or mask and played. 


## Layer 10, Head 5
<img width="656" alt="image" src="https://github.com/johnrphilip/HarvardAI/assets/96958726/4ff24d2c-b34e-4e4c-a6ea-7be17971d83e">
## Attention may have revealed the compound subject pattern here. A similar focus on only this pattern was found in L10.H7, L11.H6, 
- [MASK -> dog]

## Layer 11, Head 12
<img width="704" alt="image" src="https://github.com/johnrphilip/HarvardAI/assets/96958726/9020e5ac-9988-4ebc-9e06-ef43845318d2">

Following the MASK-dog attention a lot of attention heads start looking at patterns with "played". Similar vertical attention bars under played found in L11.H7, L11.H11


# Final Thoughts

While recognizing that attention heads are noisy and somewhat elusive from human interpretation, I am wondering if BERT never fully detected the pattern between the compound subject and the verb, as I didn't see any distinct focus colours between them (perhaps because it was a weird compound subject and verb-adverb (played together). My analysis does discuss patterns shown specifically between the two subjects, demonstrating article-noun attention, and a lot of attention around the verb-adverb played together. 

