from pathlib import Path
import uproot


BASE_DIR = Path(__file__).resolve().parent.parent

def main():
    ## initiates project, grab our root file, and sort through the roughly 1 million pieces of data found in it. ##
    ## without this this amount of data would be extremely overwhelming (still is but manageable##
    root_file = BASE_DIR / "data" / "raw" / "00334566_00000001_1.dvntuple.root"

    if not root_file.exists():
        raise FileNotFoundError(f"File {root_file} not found")
    else:
        print(f"File {root_file} found")
## Separate data into like categories. ##
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
    if "hasmuon" in name or "ismuon" in name or "muplus_id" in name or "muminus_id"in name or "kplus_id"in name:
        return "identity"
    elif "hascalo"in name or "hasrich" in name:
        return "detector_presence"
    elif "usedrich" in name:
        return "detector_usage"

    elif "richabove" in name:
        return "Rich_Thresholds"
    elif "pid" in name or "probnn" in name:
        return "PID_classifier"
    elif name.endswith(("_p","_pt", "_pe", "_px", "_py", "_pz", "_m")):
        return "kinematics"
    elif "ownpv" in name or "orivx" in name:
        return "track_vertex"
    elif "ENDVERTEX" in name or "MM" in name or "Bplus_ID"in name or "J_psi_1S" in name:
        return "vertex_decay.txt"
    else:
        return "metadata"

def create_txt(grouped):
    ## store each list into .txt files. this will help us later to lookup files in
    # an easy way. we can always find grouped data#
    for key, value in grouped.items():
        output_file = Path(f"data/docs/{key}.txt")
        with output_file.open("w", encoding='utf-8') as file:
            for branch_name in grouped[key]:
                file.write(f'{branch_name}\n')




if __name__ == '__main__':
    main()

'''
--- Proper Pipeline ---
This should serve as a pipeline to process ROOTdata up until this point.
There will be a function for this soon once alldata has been iterated and put in a proper spot.
1. In main, write command to call classify_branch() first
2. next call create_txt()
3. run main()
4. plotting.py unnecessary unless you're interest in seeing the graphs for data. right now logic
 is prepared to read kinematics data, and graph it. Next step is to have logic parse through all data
 then graph it accordingly.
  -if desired, open plotting.py, make sure it is running from current file, and not main as parent
  run main()
  - this will return matched_data which you can pass to dummy_root() if you want to see a sample.txt file of the ROOT 
  data.
5.in build_godot.py is where I will process all ROOT data and place it in a dictionary, event_data, 
    -then i wll create a function to copy the data into a JSON file for export to GODOT.
    - Graph datat using awkward or something like PyGame
        - look at trends in data, compare data in graphs, find any interesting algorithms. see how I can manipulate this data 
        to create maybe some shaders, animations. 
            -could be used for:
             -shader programming
             -special effects
             -finding mathematical equations, and anomalies (boring research)
'''