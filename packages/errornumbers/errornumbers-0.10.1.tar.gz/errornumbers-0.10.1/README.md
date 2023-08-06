# Error Numbers library for python  
  
## Installatie  
  
- Installatie via [pip](https://phoenixnap.com/kb/install-pip-windows) (eenvoudigste manier)  
  - Open een terminal. (Kan via Pycharm (Alt + F12) of manueel via de zoekbalk in windows).  
  - gebruik het command `pip install errornumbers`.  
- Manuele installatie  
  - Download [errornumbers.py](https://github.com/aap007freak/errornumbers/blob/master/errornumbers.py) van deze github repository.  
  - Zet ze in dezelfde map als je python scripts; je kan de bestanden nu gebruiken.  
  
  
## Gebruik  
  
Vanboven in elke python file waarin je deze package wilt gebruiken, moet je volgende lijn zetten:  
  
```python  
from errornumbers import ErrorNumber  
```  
  
Heel de library draait rond het object *ErrorNumber*. Je kan deze aanmaken op deze manier:  
  
  
```python  
#ErrorNumber met absolute fout  
my_error_number = ErrorNumber(waarde, absolute_fout)  
#ErrorNumber met relatieve fout  
my_error_number = ErrorNumber(waarde, relatieve_fout, relative=True)  
```  
  
  
Een ErrorNumber object heeft drie variabelen; value, absolute_error en relative_error. De waarde en fout van een ErrorNumber zijn steeds reëel.  
 Je kan ze op onderstaande manier opvragen.  
  
```python  
#Maak een ErrorNumber  
my_error_number = ErrorNumber(5, 0.1)  
  
print(my_error_number.value)  
#prints 5  
print(my_error_number.absolute_error)  
#prints 0.1  
print(my_error_number.relative_error)  
#prints 0.02  
  
#Wanneer je het hele object print:  
print(my_error_number)  
#prints [value=5; error=0.1; relative_error=0.02]  
  
```  
  
  
ErrorNumbers zijn **immutable**. Dit betekent dat je de waarde van een ErrorNumber niet kan veranderen. Wanneer je aan de hand van een functie een ErrorNumber bewerkt, geeft die functie een nieuwe ErrorNumber terug en wordt de originele ErrorNumber behouden.  
  
```python  
#Maak een ErrorNumber  
original_error_number = ErrorNumber(5, 0.1)  
#plus 5  
new_error_number = original_error_number + 5  
  
print(original_error_number)  
#prints [value=5; error=0.1; relative_error=0.02]  
print(new_error_number)  
#prints [value=10; error=0.1; relative_error=0.02]  
```  
Als je een bestaande operatie (zoals +, -, ... ) op twee ErrorNumbers uitvoert, dan worden de fouten automatisch meegepropageerd.   
Als er een ander type wordt doorgegeven, dan wordt de variabele als een constante beschouwd (zonder fout dus).    
  
Functie | Afkorting | Beschrijving  
--- | --- | ---  
`.plus(other_errornumber)` | + | telt een ErrorNumber bij een andere ErrorNumber op.    
`.plusc(constant)` | + | telt bij een Errornumber een constante op  
`.minus(other_errornumber)` | - | trekt een ErrorNumber van een andere ErrorNumber af  
`.minusc(constant)` | - | trekt een constante van een ErrorNumber af  
`.times(other_errornumber)` | * | vermenigvuldigt een ErrorNumber met een andere ErrorNumber  
`.timesc(constant)` | * | vermenigvuldigt een ErrorNumber met een constante  
`.divided_by(other_errornumber)` | / | deelt een ErrorNumber door een andere ErrorNumber  
`.divided_byc(constant)` | / | deelt een ErrorNumber door een constante  
`.inverse()` |  | inverteert een ErrorNumber  
`.squared()` |  | geeft het kwadraat van een ErrorNumber  
`.cubed()` |  | geeft de derde macht van een ErrorNumber  
`.to_the(constant)` | ** | geeft de n-de macht van een ErrorNumber  
  
  
Goniometrische en andere bewerkingen kunnen ook gebruikt wordt, mits ze eerst geïmporteerd worden  
  
```python  
from errornumbers import sin, exp  
```  
  
Een lijstje met functies die geïmporteerd moeten worden voor gebruik staan hieronder.  
Functie | Beschrijving  
--- | ---  
`sin(errornumber)` |neemt de sinus van een ErrorNumber*.  
`cos(errornumber)` | neemt de cosinus van een ErrorNumber*  
`tan(errornumber)` | neemt de tangens van een ErrorNumber*  
`cot(errornumber)` | neemt de cotangens van een ErrorNumber*  
`exp(errornumber)` | verheft e tot errornumber  
`expbase(errornumber, base)` | verheft een base tot het errornumber  
`from_non_reproducible(list)` | berekent een waarde met fout = 3 * SF uit niet-reproduceerbare metingen.
  
*** *goniometrische formules verwachten steeds een argument in radialen*  
  
Het is niet bijster moeilijk om zelf custom functies van ErrorNumbers te schrijven met custom foutenpropagatie.
## Over het import statement  
  
Python laat het toe om import statements een andere naam te geven, dit om je code te verkorten.  
  
Bijvoorbeeld:  
  
```python  
from errornumbers import ErrorNumber as EN  
  
my_error_number = EN(5, 0.1)  
  
from errornumbers import sin as s  
  
print( s(my_error_number) )  
```  
  
Ook kan je heel de package in 1 keer importen met het commando `from errornumbers import *`.  
Dan kan je alle functies en het ErrorNumber object direct in je scripts gebruiken  
  
```python  
from errornumbers import *  
  
my_error_number = ErrorNumber(0.1, 0.1, relative=True)  
```  
  
## Voorbeeld  
  
### brekingsindex van een prisma  
  
We kunnen aan de hand van de tophoek ![\alpha](https://latex.codecogs.com/svg.latex?\space\alpha) en de deviatiehoek ![\delta](https://latex.codecogs.com/svg.latex?d) van een prisma de brekingsindex bepalen met de formule  
  
![\frac{\sin{\frac{\alpha + d}{2}}}{\sin{\frac{\alpha}{2}}}](https://latex.codecogs.com/svg.latex?\Large&space;n=\frac{\sin{\frac{\alpha+d}{2}}}{\sin{\frac{\alpha}{2}}})  
  
```Python  
from errornumbers import ErrorNumber as EN  
from errornumbers import sin  
import math  
  
#in degrees  
alpha = EN(60, 0.5)  
delta = EN(40, 1.2)  
  
radian_alpha = alpha * math.pi / 180  
radian_delta = delta * math.pi / 180  
  
  
numerator = sin( (radian_alpha + radian_delta) / 2)  
denominator = sin(radian_alpha/ 2)  
  
n = numerator / denominator  
  
n_degrees = n * 180 / math.pi  
print(n)  
  
```  
  
  
## Contributing / Opmerkingen  
- English version will follow soon  
- Not every method has been tested