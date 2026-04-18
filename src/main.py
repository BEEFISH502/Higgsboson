from pathlib import Path
import uproot

def main():
    ## initiates project, grab our root file, and sort through the rough 1 million pieces of data found in it. ##
    ## without this this amount of data would be extremely overwhelming (still is but manageable##
    root_file = Path("data/raw/00334566_00000001_1.dvntuple.root")

    if not root_file.exists():
        raise FileNotFoundError(f"File {root_file} not found")
    else:
        print(f"File {root_file} found")
## Seperate data into like categories. ##
    grouped = {
        "Identity": [],
        "Detector Presence": [],
        "Detector Usage": [],
        "RICH Thresholds": [],
        "PID_classifier": [],
        "Kinematics": [],
        "Track_Vertex": [],
        "other": [],
    }
    with uproot.open(root_file) as file:
        for key in file.keys():
            tree = file[key]

            if not isinstance(tree, uproot.TTree):
                print(" Skipping non-tree object")
                continue

            for branch in tree.branches:
                category = classify_branch(branch)
                grouped[category].append(branch.name)
                print(f"{branch.name} is in {category}")





def classify_branch(branch):
    ## how we are classifying each item in the ROOT file ##
    name = branch.name.lower()
    ## .lower() to minimize incosistencies ##
    if "hasmuon" in name or "ismuon" in name:
        return "Identity"
    elif "hascalo"in name or "hasrich" in name:
        return "Detector Presence"
    elif "usedrich" in name:
        return "Detector Usage"

    elif "richabove" in name:
        return "RICH Thresholds"
    elif "pid" in name or "probnn" in name:
        return "PID_classifier"
    elif name.endswith(("_p","_pt", "_pe", "_px", "_py", "_pz", "_m")):
        return "Kinematics"
    elif "ownpv" in name or "orivx" in name:
        return "Track_Vertex"
    else:
        return "other"

def create_txt(grouped):
    ## store each list into .txt files. this will help us later to lookup files iin an easy way. we can always find grouped data#
    for key, value in grouped.items():
        output_file = Path(f"data/docs/{key}.txt")
        with output_file.open("w", encoding='utf-8') as file:
            for branch_name in grouped[key]:
                file.write(f'{branch_name}\n')

if __name__ == '__main__':
    main()