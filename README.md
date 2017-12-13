# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)
Implementation of binary trie and binary search algorithms for ip lookup

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions
Setup:
Install mininet 
Install ryu controller
Run mininet using command:
sudo mn --custom topology.py --topo mytopo  --controller remote --pre config --mac
Run controller using command:
PYTHONPATH=. <path-to-ryu-manager> <path-to-ip-lookup.py> <path-to-ofctl_rest.py>


### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact
