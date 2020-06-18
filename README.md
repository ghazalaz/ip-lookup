# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

Implementation of binary trie and binary search algorithms for ip lookup including:
  # 1: BINARY TREE
  # 2: COMPLETE BT
  # 3: DISJOINT BT 
  # 4: PREFIX LENGTH BINARY SEARCH WITH MARKERS
  # 5: PREFIX LENGTH BINARY SEARCH WITH EXPANSION 
  # 6: PREFIX RANGE BINARY SEARCH

### How do I get set up? ###
  Install mininet 
  Install ryu controller
  Run mininet using command:
  sudo mn --custom topology.py --topo mytopo  --controller remote --pre config --mac
  Run controller using command:
  PYTHONPATH=. <path-to-ryu-manager> <path-to-ip-lookup.py> <path-to-ofctl_rest.py>

