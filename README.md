# Meirin

[**English**](https://github.com/sinsong/Meirin) | [**中文**](README_zh.md)

A attribute-based access control(ABAC) system implemention.
Project name inspired by Touhou-Project [红美铃][1].

## Install

```bash
# directly install
pip install .

# install by wheel
python -m build
pip install meirin-*.whl
```

## Usage

Start Web API server:

```bash
meirin           # through console script
python -m meirin # through module entry
```

## Document

### Web API Document

- Swagger UI http://localhost:8000/docs
- ReDoc      http://localhost:8000/redoc

## References

- [NIST ABAC guide](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-162.pdf)
- [ABAC Practice guide](https://www.nccoe.nist.gov/sites/default/files/library/sp1800/abac-nist-sp1800-3-draft-v2.pdf)
- XCAML

[1]: https://zh.moegirl.org.cn/%E7%BA%A2%E7%BE%8E%E9%93%83
