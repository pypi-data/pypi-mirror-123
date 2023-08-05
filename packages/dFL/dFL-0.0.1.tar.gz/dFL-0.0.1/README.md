

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">Decentralized Federated Learning</h3>

  <p align="center">
    This project aims to build a blockchain based decentralized federated learning
    <br />
  </p>
  <br />

  <p align="center">
  <img src="images/sys_arch.jpg" alt="System Archeticture" width="700" height="500">
  <br />
  </p>
  
</p>


 

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
Recently, Federated Learning (FL) has gained tremendous traction as it has the ability to provide a privacy-preserving mechanism to train Machine Learning models on hidden data. However, most of today's FL systems are centralized, in which a centralized server is typically used to build the global FL model. 


<p align="center">
  <img src="images/exchanged_blocks.png" alt="Number of exchanged blocks" width="500" height="400">
  <br />
</p>

<!-- GETTING STARTED -->
## Getting Started

The following instructions will show you how to setup and installed required packages.

### Prerequisites

The only requirements is to have python3 and pip installed in your machine.

### Installation

1. Download and Install MongoDB Comunity Server from [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)

2. Clone the repo, move to the project directory
  ```sh
  git clone https://github.com/a-dirir/decentralized_FL.git

  cd decentralized_FL
```
#### Installation for Windows
3. Install virtualenv.
  ```sh
  py -m pip install --user virtualenv
```
   
4. Create and activate an environment called dfl
  ```sh
  py -m venv dfl

  .\dfl\Scripts\activate
```
5. Install python packeges using pip
  ```sh
  pip install -r requirements.txt
```
#### Installation for Unix/macOs
3. Install virtualenv.
  ```sh
  python3 -m pip install --user virtualenv
```
   
4. Create and activate an environment called dfl
  ```sh
  python3 -m venv dfl

  source dfl/bin/activate
```
5. Install python packeges using pip
  ```sh
  pip install -r requirements.txt
```





<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact
Ahmed Mukhtar Dirir -  ahmed.m.dirir@gmail.com




