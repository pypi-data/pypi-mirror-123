# Caribe 

>This python library takes trinidadian dialect and converts it to standard english.
Future updates would include the conversion of other caribbean dialects to standard english and additional natural language processing methods.

____
## Installation
Use the below command to install package/library
```
pip install Caribe 

```
____
 ## Usage
 > Sample 1: Checks the dialect input against existing known phrases before decoding the sentence into a more standardized version of English language. A corrector is used to check and fix small grammatical errors.
```python
# Sample 1
import Caribe as cb
from Caribe import trinidad_decode, trinidad_decode_split, caribe_corrector

sentence = "Ah wah mi modda phone"
standard = cb.phrase_decode(sentence)
standard = cb.trinidad_decode(standard)
fixed = cb.caribe_corrector(standard)
print(fixed) #Output: I want my mother phone

```
>Sample 2: Checks the dialect input against existing known phrases
```python
# Sample 2 
import Caribe as cb
from Caribe import trinidad_decode, trinidad_decode_split, caribe_corrector

sentence = "Waz de scene"
standard = cb.phrase_decode(sentence)

print(standard) # Outputs: How are you

```
>Sample 3: Checks the sentence for any grammatical errors or incomplete words and corrects it.
```python
#Sample 3
import Caribe as cb
from Caribe import trinidad_decode, trinidad_decode_split, caribe_corrector

sentence = "I am playin fotball outsde"
standard = cb.caribe_corrector(sentence)

print(standard) # Outputs: I am playing football outside

```
>Sample 4: Makes parts of speech tagging on dialect words.
```python
#Sample 4
import Caribe as cb
from Caribe import trinidad_decode, trinidad_decode_split, caribe_corrector

sentence = "wat iz de time there"
analyse = cb.nlp()
output = analyse.caribe_pos(sentence)

print(output) # Outputs: ["('wat', 'PRON')", "('iz', 'VERB')", "('de', 'DET')", "('time', 'NOUN')", "('there', 'ADV')"]

```
>Sample 5: Remove punctuation marks.
```python
#Sample 5
import Caribe as cb
from Caribe import trinidad_decode, trinidad_decode_split, caribe_corrector

sentence = "My aunt, Shelly is a lawyer!"
analyse = cb.remove_signs(sentence)


print(analyse) # Outputs: My aunt Shelly is a lawyer

```
---
- ## Additional Information
    - `trinidad_decode()` : Decodes the sentence as a whole string.
    - `trinidad_decode_split()`: Decodes the sentence word by word.
    - `phrase_decode()`: Decodes the sentence against known dialect phrases.
    - `caribe_corrector()`: Corrects grammatical errors in a sentence.
    - `trinidad_encode()`: Encodes a sentence to trinidadian dialect.
    - `caribe_pos()`: Generates parts of speech tagging on dialect.
    - `pos_report()`: Generates parts of speech tagging on english words.
    - `remove_signs()`: Takes any sentence and remove inefficient punctuation marks. 

---
- ## File Encodings on NLP datasets
Caribe introduces file encoding (Beta) in version 0.1.0. This allows a dataset or any supported filetype to be creolised in trinidad dialect.

- ### Usage of File Encodings:
```python
import Caribe as cb

convert = cb.file_encode("test.txt", "text")
# Generates a translated text file
convert = cb.file_encode("test.json", "json")
# Generates a translated json file
convert = cb.file_encode("test.csv", "csv")
# Generates a translated csv file

```

---
- ## Contact 
For any concerns, issues with this library or want to become a collaborator to this project.

Email: keston.smith@my.uwi.edu 
___