# CrunchbaseAPI
a full-featured API library to allow downloading and presenting organization and people data from Crunchbase

## Quick Start
```get_orgs``` function to query organization data using Crunchbase API
```get_ppl``` function to query people data using Crunchbase API
```python
import cbapi
test_ppl = cbapi.get_ppl(name="Jordan", types="investor")
test_orgs = cbapi.get_orgs(name="tech", types="investor", locations="New York")
```

## Installation
Install cbapi using pip:
```python
pip install git+https://github.com/JordanWang-1998/cbapi.git
```

## Requirements
* pandas
* requests
