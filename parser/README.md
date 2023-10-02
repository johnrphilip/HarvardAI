# Natural Language Parsing with NLTK

## Overview
This project demonstrates the use of the Natural Language Toolkit (NLTK) to parse English sentences based on predefined grammar rules. It showcases the ability to break down sentences into their grammatical components, such as noun phrases and verb phrases, and to identify the structure of sentences.

## What It Demonstrates
- **Grammar Definition**: The project defines grammar rules for terminals and non-terminals, allowing the parser to recognize various sentence structures.
- **Sentence Parsing**: It parses given sentences based on the defined grammar rules and identifies the hierarchical structure of grammatical components within the sentences.
- **Noun Phrase Chunking**: The project extracts noun phrase chunks from the parsed sentences, providing insights into the main subjects and objects within the sentences.
- **Handling Multiple Adjectives**: The grammar rules are designed to handle noun phrases with multiple adjectives, demonstrating the flexibility and adaptability of the parser.

## How the Code Works
1. **Grammar Rules Definition**: The code defines terminals and non-terminals representing various parts of speech and sentence structures.
2. **Parsing**: Using NLTK’s `ChartParser`, the code parses input sentences based on the defined grammar rules, generating parse trees that represent the grammatical structure of the sentences.
3. **Noun Phrase Chunking**: The code traverses the generated parse trees to extract and list all noun phrase chunks within the sentences.
4. **Preprocessing**: The input sentences are preprocessed by converting all characters to lowercase and removing any word that does not contain at least one alphabetic character.
5. **Main Execution**: The code can be executed with a sentence as an input, either through command-line argument or standard input, and it outputs the parse tree and the noun phrase chunks of the input sentence.

## Usage
To run the code with a sentence from a file:
```shell
python3 parser.py <filename>


## Output Samples:

        S     
   _____|___   
  NP        VP
  |         |  
  N         V 
  |         |  
holmes     sat

                                    S                                             
  __________________________________|______                                        
 |                                         VP                                     
 |              ___________________________|______________                         
 |             |                           |              VP                      
 |             |                           |     _________|___                     
 |             VP                          |    |             NP                  
 |    _________|______________             |    |     ________|___                 
 |   |         |              PP           |    |    |            PP              
 |   |         |           ___|_____       |    |    |     _______|_____           
 NP  |         NP         |         NP     |    |    NP   |             NP        
 |   |    _____|_____     |         |      |    |    |    |    _________|______    
 N   V  Det   Adj    N    P         N     Conj  V    N    P  Det       Adj     N  
 |   |   |     |     |    |         |      |    |    |    |   |         |      |   
 i  had  a  country walk  on     thursday and  came home  in  a      dreadful mess

Noun Phrase Chunks
i
a country walk
thursday
home
a dreadful mess

Noun Phrase Chunks
              S                                                           
  ____________|______________________                                      
 |                                   VP                                   
 |             ______________________|_________________________            
 |            VP                                               |          
 |    ________|________________                                |           
 |   |                         NP                              |          
 |   |                _________|______________                 |           
 |   |               NP                       |                |          
 |   |    ___________|_______________         |                |           
 |   |   |          AdjP             |        |                |          
 |   |   |     ______|____           |        |                |           
 |   |   |    |          AdjP        |        PP               PP         
 |   |   |    |       ____|____      |     ___|___          ___|___        
 NP  |   |    |      |        AdjP   |    |       NP       |       NP     
 |   |   |    |      |         |     |    |    ___|___     |    ___|___    
 N   V  Det  Adj    Adj       Adj    N    P  Det      N    P  Det      N  
 |   |   |    |      |         |     |    |   |       |    |   |       |   
 i  had  a  little moist      red  paint  in the     palm  of  my     hand

Noun Phrase Chunks
i
a little moist red paint
the palm
my hand
                                  S                                           
  ________________________________|_______                                     
 |                                        VP                                  
 |                                 _______|________________________________    
 |                                VP                                       |  
 |          ______________________|_______                                 |   
 |         |                          RelClause                            |  
 |         |                 _____________|_______________                 |   
 |         |                |                             VP               |  
 |         |                |                     ________|___             |   
 |         |                NP                   |            PP           |  
 |         |             ___|_____________       |     _______|___         |   
 NP        VP           NP        |       NP     VP   |           NP      AdvP
 |     ____|___      ___|___      |       |      |    |        ___|___     |   
 N   Adv       V   Det      N    Conj     N      V    P      Det      N   Adv 
 |    |        |    |       |     |       |      |    |       |       |    |   
she never     said  a      word until     we    were  at     the     door here

Noun Phrase Chunks
she
a word
we
the door
