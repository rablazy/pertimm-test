<!-- GETTING STARTED -->
<a id="readme-top"></a>

## Status
![GitHub CI](https://github.com/rablazy/pertimm-test/actions/workflows/ci.yml/badge.svg)

### Installation

_Short guide to installation._

1. Create and enable virtualenv with python3.x, I used python3.11
   ```sh
   python3.11 -m venv ve311
   source ve311/bin/activate
   ```
2. Install requirements
   ```sh
   cd maze_solver/
   pip install -r requirements.txt
   ```
3. Check url in urls.py

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage
1. Maze solver is run through command line.<br/>
   <br/>To find the first possible solution:
   ```sh
   python3.11 main.py --solve simple
   ```
   <br/>To find all possible solutions:
   ```sh
   python3.11 main.py --solve all
   ```
2. To run tests.<br/>
   ```sh
   pytest -s
   ```
3. To run tests with coverage.<br/>
   ```sh
   pytest -s --cov --cov-report=html:coverage
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

