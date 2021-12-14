# ICD-9 to ICD-10 Mapping

Performs  mapping to and from ICD-9 to ICD-10.  

## Background
Diagnosis (CM) and procedure (PCS) codes is based on CMS general equivalence mappings (GEMs).

The purpose of the GEMs is to create a useful, practical, 
code to code translation reference dictionary for both code 
sets, and to offer acceptable translation alternatives wherever 
possible. For each code set, it endeavors to answer this question: 
Taking the complete meaning of a code (defined as: all correctly 
coded conditions or procedures that would be classified to a code 
based on the code title, all associated tabular instructional notes, 
and all index references that refer to a code) as a single unit, what 
are the most appropriate translation(s) to the other code set?

## Mapping
Mappings from specific concepts to more general concepts are possible; 
however, it is not possible to use mappings to add specificity when 
the original information is general.

## Flags
#### 1st Flag
The GEM provides an approximate flag (1st Flag).  The approximate flag identifies 
entries where the complete meaning of the source system code and that 
of the target system code are not considered equivalent.  

The approximate flag is 0 when the complete meaning of the source and the 
target are considered equivalent and the source and target translate only 
to each other in both GEMs files.

When the approximate flag is 1 the complete meaning of the source and the 
target are not considered equivalent.

#### 2nd Flag
The no map flag distinguishes entries where the source system code has at 
least one translation from entries where the source system code has no 
target system translation. Every effort is made to find an acceptable 
translation in the target system for every code in the source system. 
The no map flag is used only as a last resort, when there are no acceptable 
target system translation alternatives for the source system code.

#### 3rd Flag
The combination flag distinguishes entries where the source system code has 
a single (meaning “non-combination”) translation alternative(s) from entries 
where the source system has a combination alternative(s).

#### 4th Flag
A source system combination code includes diagnostic conditions or procedures 
that require more than one separate code in the target system to convey the 
equivalent amount of information. A combination code may also describe multiple 
variations of the information in either the code title or the complete meaning 
of the code. Each of these variations has its own number in the scenario field 
(the 4th flag).

#### 5th Flag
Choice lists (the 5th flag) are the method of organization for the translation 
alternatives in a combination entry. Choice lists organize the distinct 
components of the target system translation in a combination entry 
into pick lists.

## Input file format
51884  
99666  
51881  
V5877  
73025  

## Sample Data
Sample ICD-9 CM and PCS files are included.

## Resources:
https://www.cms.gov/Medicare/Coding/ICD10/2018-ICD-10-PCS-and-GEMs \
https://www.cms.gov/Medicare/Coding/ICD10/2018-ICD-10-CM-and-GEMs \
https://github.com/Ed-Nonnenmacher/ICD9-ICD10.git \
https://github.com/bhanratt/ICD9CMtoICD10CM.git


