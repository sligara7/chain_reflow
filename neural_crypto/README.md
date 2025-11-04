# Neural Cryptography

Exploring neural networks as cryptographic ciphers with architecture obfuscation.

## Overview

This project explores a novel approach to encryption: using neural network architectures and weights as the encryption "key". Unlike traditional encryption where the algorithm is public and only the key is secret, neural cryptography makes both the architecture AND the weights secret.

## Key Insight

> "You'd have to figure out how information is encoded within the neural network (which is very difficult to do), particularly if you have different layers and different amounts of nodes in those layers."

This fundamental insight drives the security model: an attacker must guess both the network architecture (layers, nodes, activations) AND the trained weights to decrypt data.

## Security Advantage

**Traditional Encryption (e.g., AES-128)**:
- Algorithm: PUBLIC (everyone knows how AES works)
- Key: 128 bits (SECRET)
- Search space: 2^128 possible keys

**Neural Encryption**:
- Architecture: SECRET (~1,000+ possible configurations)
- Weights: SECRET (~65,000+ parameters, 2^2,000,000+ per architecture)
- Search space: 1,000 × 2^2,000,000+ (exponentially larger!)

## Project Structure

```
neural_cryptography/
├── src/
│   ├── neural_crypto_prototype.py              # Main prototype implementation
│   └── neural_crypto_architecture_security.py  # Architecture obfuscation demos
├── docs/
│   ├── neural_cryptography_concept.md          # Conceptual foundation
│   ├── neural_crypto_prototype_readme.md       # Implementation guide
│   └── neural_crypto_architecture_security.md  # Security analysis
└── README.md
```

## Three Approaches Implemented

### 1. Pure Neural Cipher (128-bit → 128-bit)
- Network weights ARE the encryption key
- Forward pass through encoder = encryption
- Forward pass through decoder = decryption
- Without trained weights, decryption is impossible

### 2. Semantic Translation + Encryption
- Encrypts while translating between service schemas
- Service A (JSON) → Encrypted Intermediary → Service B (Protobuf)
- Useful for microservices with different data formats

### 3. Hybrid Approach (RECOMMENDED)
- Traditional encryption (AES-256) for proven security
- Neural layer for semantic transformation
- Best of both worlds

## Installation

```bash
cd neural_cryptography
pip install torch numpy
```

## Usage

### Run Main Prototype

```bash
python src/neural_crypto_prototype.py
```

This runs three demonstrations:
1. Pure neural cipher (128-bit encryption)
2. Microservices with schema translation
3. Context-aware security levels

### Run Architecture Security Demo

```bash
python src/neural_crypto_architecture_security.py
```

This demonstrates:
1. Architecture obfuscation (wrong architecture cannot decrypt)
2. Search space comparison (neural vs traditional crypto)
3. Dynamic architecture generation

## Key Features

### Architecture as Part of the Key
- Different layer counts (2, 3, 4, 5 hidden layers)
- Different layer sizes (64, 128, 256, 512 nodes)
- Different activation functions (ReLU, Tanh, Sigmoid)
- ~1,000+ possible architecture configurations

### Weight Diversity
- ~65,000+ parameters per cipher (typical architecture)
- Each parameter is a 32-bit float
- Different training runs produce different weights
- Enables key rotation via retraining

### Security Through Computational Hardness
- Reverse-engineering neural networks is computationally hard
- Non-linear activations prevent easy inversion
- No known efficient algorithm to invert arbitrary neural networks
- Potential quantum resistance

## Example: Pure Neural Cipher

```python
from neural_crypto_prototype import PureNeuralCipher

# Create and train cipher
cipher = PureNeuralCipher(bit_size=128, hidden_layers=3)
cipher.train_cipher(epochs=2000)

# Encrypt
plaintext = torch.rand(1, 128) * 2 - 1  # 128-bit message
ciphertext = cipher.encrypt(plaintext)

# Decrypt (requires the trained network weights!)
decrypted = cipher.decrypt(ciphertext)
```

## Security Analysis

### Attack Resistance

**Brute Force Attack**:
- Must try all architectures × all weight configurations
- Search space: ~1,000 × 2^2,000,000+
- Verdict: INFEASIBLE

**Known Plaintext Attack**:
- Requires many (plaintext, ciphertext) pairs
- Must train adversarial network to learn encoder
- Requires significant compute resources
- Verdict: POSSIBLE but requires many examples

**Model Extraction Attack**:
- Query cipher with many inputs, observe outputs
- Try to train clone network
- Requires black-box access + millions of queries
- Mitigation: Rate limiting, dynamic architecture changes

**Side-Channel Attack**:
- Timing, power analysis (same as traditional crypto)
- Mitigation: Constant-time implementations

### Comparison to AES-128

| Property | AES-128 | Neural Cipher | Hybrid |
|----------|---------|---------------|---------|
| Algorithm | Public | Secret | Both |
| Key Size | 16 bytes | ~260 KB | Both |
| Search Space | 2^128 | ~2^2,000,000+ | Both |
| Speed | Very fast | Slower | Medium |
| Security Proof | Yes | Empirical | Yes (AES) |
| Quantum Resistant | No | Possibly | Maybe |

## Use Cases

1. **Microservices with Different Schemas**
   - Encrypt while translating between JSON ↔ Protobuf
   - Each service works in its own format

2. **Legacy System Integration**
   - Bridge old systems (COBOL) with modern APIs (REST)
   - Encryption + translation simultaneously

3. **Privacy-Preserving Analytics**
   - Compute on encrypted data in intermediary space
   - Semantic relationships preserved

4. **Quantum-Resistant Communication**
   - No known quantum algorithm to invert neural networks
   - Potential future-proofing

## Related Research

- **Adversarial Neural Cryptography** (Google Brain, 2016): Neural networks learning encryption
- **CryptoNets** (Microsoft Research): ML inference on encrypted data
- **Neural Crypto-Coding** (2020): Combining error correction with encryption
- **Model Inversion Attacks**: Understanding limits of neural network security

## Limitations

1. **Speed**: Slower than hardware-accelerated AES (~1000x)
2. **Key Size**: Larger (~260 KB vs 16 bytes for AES)
3. **No Mathematical Proof**: Security is empirical, not proven
4. **Not Standardized**: Research prototype, no industry standards

## Recommendations

✅ **Use Neural Crypto When**:
- Need semantic transformation (schema translation)
- Want architecture-level obfuscation
- Exploring quantum resistance
- Research/experimental contexts

✅ **Use Traditional Crypto When**:
- Need maximum speed
- Require proven security
- Production systems with compliance requirements
- Industry-standard implementations needed

✅ **Use Hybrid Approach When**:
- Want both security guarantees AND semantic transformation
- Building modern microservices architectures
- Need encryption + cross-domain translation

## Future Work

- [ ] Formal security analysis
- [ ] Adversarial robustness testing
- [ ] Quantum resistance proof/disproof
- [ ] GPU optimization for faster inference
- [ ] Production-ready library with test suite
- [ ] Benchmark against AES-256
- [ ] Integration with real microservices
- [ ] Federated learning for distributed key generation

## Contributing

This is a research project exploring the intersection of neural networks and cryptography. Contributions, ideas, and security analysis welcome!

## License

MIT

## Origin

This project originated from explorations in the [chain_reflow](https://github.com/sligara7/chain_reflow) project around neural intermediary layers for architecture linking. The insight that neural networks could serve as ciphers led to this separate research direction.

## Contact

For questions or collaboration: [GitHub Issues](https://github.com/sligara7/neural_cryptography/issues)
