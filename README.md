# Secure Communication Client-Server Project

This repository contains a comprehensive collection of implementations and resources for a secure client-server communication system and cryptanalysis laboratory. It is intended to centralize practical materials, implementation phases, and attack methodologies for learning cybersecurity concepts.

## Contents

### Project Overview

An educational client-server architecture built in Python using TCP sockets. The client dynamically selects cryptographic algorithms and parameters, while the server decrypts and processes incoming messages.

### Network & Protocol Architecture

The communication relies on standard Python sockets supporting local execution or distributed virtual machine setups. All messages follow a structured JSON protocol defining the algorithm, parameters, keys, and ciphertext.

### Cryptographic Algorithms

Implementation of classical ciphers including Caesar, Substitution, Vigenère, Playfair, and Hill. Modern symmetric algorithms such as AES-128 and AES-256 with multiple operating modes (ECB, CBC, CTR). Asymmetric cryptography covering RSA and Diffie-Hellman key exchange. Modern cryptographic hash functions including SHA-256 and SHA-3 with digital signatures.

### Cryptanalysis & Network Interception

Practical attack methodologies and packet analysis techniques using Wireshark and tcpdump. Demonstrations cover frequency analysis, brute-force attacks, dictionary attacks, known-plaintext analysis, ECB pattern leakage, and replay attacks.

### Project Structure

A clean directory layout separating classical, symmetric, asymmetric, and hashing modules from network handlers, unit tests, and examples.

### Useful Resources

Reference material, official documentation for Python Sockets, AES, RSA, Wireshark, and network analysis tools.
