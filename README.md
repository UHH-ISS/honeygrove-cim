# honeygrove-cim

## Quickstart Guide

### EK Stack
* **TODO**

### CIM Endpoint
* Clone the repository or download and unzip it
* Optional: Setup a virtualenv to contain the required dependencies
  ```shell
  $ python3 -m venv .venv
  $ source .venv/bin/activate
  ```
* Install the required python dependencies
  ```shell
  $ pip3 install --upgrade -r requirements.txt
  ```
* Install [`broker`](https://github.com/zeek/broker) and the python bindings to communicate with a CIM
* Create the log directory for the cim endpoint
  ```shell
  $ mkdir -p /var/honeygrove/cim/logs
  ```
* Edit the configuration file to fit your needs
  ```shell
  $ $EDITOR honeygrove_cim/config.py
  ```
* Start the CIM endpoint and verify everything works as expected
  ```shell
  $ ./honeygrove-cim.sh
  ```

## Contributors

Honeygrove was initially developed as a bachelor project of the [IT-Security and Security Management](https://www.inf.uni-hamburg.de/inst/ab/snp/home.html) working group at Universität Hamburg and subsequently improved.

Contributors that agreed to be named are:

* [Arne Büngener](https://github.com/4rne)
* Alexandra Lindt
* [Adrian Miska](https://github.com/AdrianMiska)
* [Frieder Uhlig](https://github.com/Moshtart)
* [Julian 4goettma](https://github.com/4goettma)
