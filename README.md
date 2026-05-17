# Higgs Boson Event Visualizer
A particle physics analysis and visualization project built with  **Python**, **C++**, and **ROOT**.
This project explores CERN Open Data to analyze collision events and create visualizations inspired by Higgs Boson event reconstruction.

## Overview
The goal of this project is to:
- load and inspect CERN Open Data
- process particle collission events with ROOT and C++ data in python
- visualize event distributions and detector-style representations
- identify patterns that may correspond to Higgs boson decay signatures

## Why this project?
This project is designed to combine:
- scientific computing
- data analysis
- high-energy physics concepts
- ROOT-based workflows
- Python visualization
- C++ performance and structure

It is intended as both a learning project an portfolio piece.

## Planned Features
- ROOT file loading and inspection
- C++ event processing utilities
- Python based analysis scripts
- Histograms and event-level plots
- Detector style visualizations
- Higgs candidate selection workflows
- Interactive dashboards and visual exploration tools

## Tech Stack
- Python
- C++
- ROOT
- NumPy
- Matplotlib
- Plotly
- Uproot
- Jupyter

## Data Source

This project will use publicly available CERN Open Data samples.
Specific datasets and analysis examples will be added as the project develops.


## Project Structure 

A typical structure for this repository may look like:

## Getting Started 

### Prerequisites
- Python 3.x
- ROOT
- A C++ compiler
- Git

## Setup
Clone the repository:
bash git clone https://github.com/BEEFISH502/Higgsboson.git cd higgsboson


Set up your Python environment:
bash python -m venv .venv


Install Python dependencies:
bash pip install -r requirements.txt


## Roadmap

- [ ] create pull request
- [ ] bash pip install requirements.txt
- [ ] run download_raw.py: download root data from CERN Open Data website
- [ ] if not docs in "data" / "docs": run main.py
- [ ] this step is up to you:
    - [ ] run build.godot.py: builds event data (nested lists of data)
    - [ ] run plotting.py: plots data in simple bar graphs: can print per particle
    - [ ] run render3d.py: plots 3d visualizations of particle interactions
    - [ ] run particles.py: creates particle objects 


## Notes

plotting.py is pretty static at the present, not many cariables available to change best to run as is and visualize data.

render_3d.py is more versatile, try changing the variables and amount of events it plots.
 - curvature amount
 - curve_offset
 - event_index

particles.py most versatile, creates a class with object Particle. you may access particles and their data sets fairly easily.
particles: bplus, jpsi, kplus, muplus, muminus
data: id, p, pt, px, py, pz, e, mass, id, name, momentum, start location (x, y, z), and for bplus and jpsi  end (x, y, z)
access them as such bplus.id

bplus.id returns a list of ids for particle bplus: access each event like bplus.id[0]
additionally you may print bplus by itself and it should return a formatted list
"Particle: bplus.name
 ID: bplus.id
 Momentum: bplus.momentum: px, py, pz"
 P: bplus.p
 PT: bplus.pt
 Mass: plus.mass
 Energy: bplus.e
 Start: bplus.start: x, y, z
 Enb: x, y, z
"

I would love to go in-depth with the meaning of this data and how it fits together; however, that would take an exoberent amount of time.
i will try to explain in a nut shell.
Start = bplus origin vertex (this is where the bplus particle originates in the collision event)
bbplus end = the end vertex and the origin vertex of the particle j_psi
j_psi end = end vertex of jpsi and origin vertex of muplus, muminus, kplus.
this is the order of decay between the particles.

momentum is the the direction and magnitude of the particles movement

id = positively charged or negatively charged particle

you will need event[0] for all verticles to succesfully track the movement of one whole event. 

that's it in a nutshell, to learn more about these particles there are tons of information out there to help with this:) 
this is all you need to know to get started with my program.


This project is being developed as an educational and portfolio-friendly exploration of particle physics data analysis.

## License

