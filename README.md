# Hybrid Differential Evolution & IMDE for Job Shop Scheduling (JSSP)

## 📌 Introduction
This repository contains an implementation of **Differential Evolution (DE)** and **Improved Mutation Differential Evolution (IMDE)** for solving the **Job Shop Scheduling Problem (JSSP)**. The project compares different DE strategies and the IMDE approach to optimize scheduling efficiency and minimize makespan.

## 🚀 Features
- Implementation of **Classic Differential Evolution (DE)**
- Implementation of **Improved Mutation Differential Evolution (IMDE)**
- Supports different mutation strategies: `DE/rand/1`, `DE/best/1`, `DE/rand-to-best/1`
- Repair mechanism to ensure valid job sequences
- Evaluation of makespan for different test instances
- Statistical comparison of results
- Outputs saved in CSV and text format

## 📂 Project Structure
```
📦 Hybrid-DE-IMDE-JSSP
├── 📁 data                    # Folder containing JSSP instances
├── 📁 result for classic      # Results of Classic DE experiments
├── 📁 result for imde         # Results of IMDE experiments
├── 📜 Classic DE.py           # Classic Differential Evolution implementation
├── 📜 imde.py                 # IMDE implementation
├── 📜 results_summary.csv     # Final results summary
├── 📜 results_summary.txt     # Text summary of results
└── 📜 README.md               # Project documentation
```

## 🛠️ Installation
To run this project, make sure you have Python installed along with the required dependencies:

```sh
pip install numpy pandas
```

## 📌 How to Run
### Running Classic DE
```sh
python Classic\ DE.py
```
### Running IMDE
```sh
python imde.py
```

The results will be stored in `results_summary.csv` and `results_summary.txt`.

## 📊 Results Analysis
- The program tests different **mutation strategies** for DE.
- The **IMDE approach** introduces an archive-based mutation mechanism to improve results.
- Statistical analysis is performed on multiple test instances to evaluate performance.

## 📧 Contact
For any inquiries or collaboration, feel free to reach out:
📩 Email: [emad.k50000@gmail.com](mailto:emad.k50000@gmail.com)

## ⭐ Contribute
Feel free to fork this repository, submit issues, or contribute via pull requests.

---
🔹 **Developed by Emad K.** | 🔹 **Open Source & Research-Oriented**

