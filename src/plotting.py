from pathlib import Path
import uproot
import awkward
import matplotlib.pyplot as plt

## set Base_dir for clean reusability ##
BASE_DIR = Path(__file__).resolve().parent.parent


def get_kinematics(doc_path: Path = BASE_DIR / "data" / "docs" / "Kinematics.txt"):
    ## calling our initial .txt file for easy uproot lookup ##
    if not doc_path.exists():
        print(f"File {doc_path} not found")
    else:
        print(f"File {doc_path} initialized")
    with doc_path.open() as file:
        kinematics_data = []
        for item in file:
            kinematics_data.append(item.strip())
    return kinematics_data

def get_root(kinematics_data, root_path: Path = BASE_DIR / "data" / "raw" / "00334566_00000001_1.dvntuple.root"):
    ## get our initial root data and loop through it. save look up time ##
    ## return dictionary of actual root data; arrays ##
    if not root_path.exists():
        raise FileNotFoundError(f"File {root_path} not found")
    else:
        print(f"File {root_path} found")
    matched_data = {}

    wanted = {name.lower() for name in kinematics_data}

    with (uproot.open(root_path) as file):
        for key in file.keys():
            tree = file[key]
            if not isinstance(tree, uproot.TTree):
                continue

            for branch in tree.branches:
                if branch.name.lower() in wanted:
                    matched_data[branch.name] = branch.array()
    return matched_data

def plot_kinematics(kinematics_data):
    ## the fun stuff, plot our data so we can actually see what we're dealing with ##
    root_data = get_root(kinematics_data)
    if not root_data:
        print("No data found")
        return
    else:
        print('Data Found. Inititalizing graphs')

    n_plots = len(root_data)
    if n_plots == 0:
        print(f'No data to record. Please check file and try again')
        return

    cols = 3
    rows = (n_plots + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(12, 4 * rows))
    axes = axes.flatten()

    for ax, (branch_name, values) in zip(axes, root_data.items()):
        flat_values = awkward.flatten(values, axis=None)
        hist_values = awkward.to_numpy(flat_values)
        ax.hist(hist_values, bins=50, edgecolor ="black")
        ax.set_title(branch_name)
        ax.set_xlabel(branch_name)
        ax.set_ylabel("Entries")
        ax.grid(True, linestyle='--', alpha=0.4)

    for ax in axes[n_plots:]:
        ax.set_visible(False)

    plt.tight_layout()
    plt.show()


def main():
    kinematics_data = get_kinematics()
    plot_kinematics(kinematics_data)

main()

