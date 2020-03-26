# Tools  

## cert_for_pip.py  
Download MITM CA Certificate and add configuration to pip.ini   
  
Usage: python cert_for_pip.py [external website address (default: google.com)]   
Assumption: python 2.x or 3.x installed via Anaconda  
To do this behind the MITM proxy, only minimal packages are used as pip is not actully useful before this step.  
