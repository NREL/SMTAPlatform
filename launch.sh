# To launch the example simualtion: 
helics_broker -f 2 --localport=33000 &
python phasor.py  > PhasorLOG.txt & 
python emt.py > EMTLOG.txt & 