## CDFTPY: Python package for performing classical denisty functional theory calculations for molecular liquids 
#### Marat Valiev and Gennady Chuev
___

[comment]: <> (Simulates inhomogenous molecular liquid system in the presence of)

[comment]: <> (Lennard-Jones &#40;LJ&#41; solute particle)

[comment]: <> (In this release only RISM solver is provided.)

[comment]: <> (The program can be ran as)

[comment]: <> (    rism <input_file>)
    
[comment]: <> (The input file is of the following form)

[comment]: <> (    <solute>)

[comment]: <> (    # site   sigma&#40;Angs&#41;  eps&#40;kj/mol&#41;    charge&#40;e&#41;)

[comment]: <> (    Na       2.16         1.4755         1.0)

[comment]: <> (    <simulation>)

[comment]: <> (    temp 300)

[comment]: <> (    solvent 2site)

[comment]: <> (    tol 1.0E-7)

[comment]: <> (    max_iter 100 )
    
[comment]: <> (It contains two sections: _\<solute\>_ and _\<simulation\>_.)

[comment]: <> (The _\<solute\>_ section specifies solute parameters: name, LJ parameters)

[comment]: <> (and charge.)

[comment]: <> (The _\<simulation\>_ section describes general parameters of the system)

[comment]: <> (    temp 300       - temperature in K &#40;in this case 300K&#41;)

[comment]: <> (    solvent 2site  - solvent model &#40;in this case two site water model&#41;)

[comment]: <> (    tol 1.0E-7     - tolerance for convergence &#40;1.0E-7 in this case&#41;)

[comment]: <> (    max_iter 100   - maximum number of iterations &#40;100 in this case&#41;)
    
[comment]: <> (Upon successfull the program will generate RDF files &#40;with)

[comment]: <> (extension rdf&#41;. )

[comment]: <> (In particular, )

[comment]: <> (for the example provided above the following rdf files will be generated)

[comment]: <> (    NaH.rdf		NaO.rdf	 )
    
[comment]: <> (The rdf files contains two column - distance &#40;r&#41; and RDF g&#40;r&#41;. E.g.)

[comment]: <> (    # r        g&#40;r&#41;)

[comment]: <> (    0.005      0.0)

[comment]: <> (    0.015      7.973e-10)

[comment]: <> (    0.025      2.395e-09)

[comment]: <> (    0.035      4.797e-09)

[comment]: <> (    0.045      8.01e-09)

[comment]: <> (    0.055      1.204e-08)

[comment]: <> (    ....)


[comment]: <> (#### Available solvent models:)

[comment]: <> (    2site)
    
[comment]: <> (    Kippi M. Dyer, John S. Perkyns, George Stell, )

[comment]: <> (    and B. Montgomery Pettitt,Mol Phys. 2009 ; 107&#40;4-6&#41;: 423–431. doi:10.1080/00268970902845313.)

#### References:

Gennady N Chuev, Marina V Fedotova and Marat Valiev,
 Renormalized site density functional theory,
 J. Stat. Mech. (2021) 033205

Chuev GN, Fedotova MV, Valiev M. 
Chemical bond effects in classical site density 
functional theory of inhomogeneous molecular liquids. 
J Chem Phys. 2020 Jan 31;152(4):041101. doi: 10.1063/1.5139619. PMID: 32007044.

Marat Valiev and Gennady N Chuev,
 Site density models of inhomogeneous classical molecular liquids,
 J. Stat. Mech. (2018) 093201
 
 