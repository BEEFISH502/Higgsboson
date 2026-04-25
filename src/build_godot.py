import json
from pathlib import Path
import uproot


BASE_DIR = Path(__file__).resolve().parent.parent
def lookup_files(doc_path: Path = BASE_DIR / "data" / "docs"):
    ## this function is going to load all of our .txt files we made for simple lookup through our ROOT data.
    ## there are functions within upROOT that already slice data for us, but for educational purposes i
    ## decided to implement my own lookup function.
    input_files = {
        ## basically what we'll get here is a dictionary of all the items we want in each specific category
        "kinematics": BASE_DIR / "data" / "docs" / "kinematics.txt",
        "identity": BASE_DIR / "data" / "docs" / "identity.txt",
        "detector_presence": BASE_DIR / "data" / "docs" / "detector_presence.txt",
        "pid_classifier": BASE_DIR / "data" / "docs" / "pid_classifier.txt",
        "rich_thresholds": BASE_DIR / "data" / "docs" / "rich_thresholds.txt",
        "track_vertex": BASE_DIR / "data" / "docs" / "track_vertex.txt",
        "vertex_decay": BASE_DIR / "data" / "docs" / "vertex_decay.txt",
        "detector_usage": BASE_DIR / "data" / "docs" / "detector_usage.txt",
    }
    data ={
    }
    for key, input_file in input_files.items():

        if not input_file.exists():
            print(f'File {input_file} Not found')
            continue
        else:
            print(f'File {input_file} found')

        with input_file.open() as file:
            data[key] = [line.strip() for line in file]
    return data

def load_root(data, root_path: Path = BASE_DIR / "data" / "raw" / "00334566_00000001_1.dvntuple.root"):
    matched_data  = {}
    ## here we are going to match actual root data with our dictionary, by category, then each array of data accordingly
    with uproot.open(root_path) as file:
        for key in file.keys():
            tree = file[key]
            if not isinstance (tree, uproot.TTree):
                continue
            for branch in tree.branches:
                branch_name = branch.name.lower()
                for category, value in data.items():
                    wanted = {name.lower()for name in value}
                    if branch_name in wanted:
                        matched_data.setdefault(category, {})
                        matched_data[category][branch.name] = branch.array()
    return matched_data

def update_data(matched_data, event_data):
    #here we'll go a step further and break down the arrays into separate particles and their arrays
    # then also get everything ready to pass to our big nested dictionary.
    for category, category_data in matched_data.items():
        if category not in event_data:
            continue

        for branch_name, value in category_data.items():
            for particle_name, particle_fields in event_data[category].items():
                particle_prefix = f"{particle_name}_"

                if branch_name.startswith(particle_prefix):
                    field_name = branch_name[len(particle_prefix):]
                    if field_name in particle_fields:
                        particle_fields[field_name] = value
                    elif branch_name in particle_fields:
                        particle_fields[branch_name] = value
    return event_data



def update_root(data, root_path: Path = BASE_DIR / "data" / "raw" / "00334566_00000001_1.dvntuple.root"):
    #the big mama load ALL ROOT data, and save into a GIANT dictionary. will probably be using event_data to plot
    ## information once it is ready.
    matched_data = load_root(data, root_path)
    event_data = {
        "identity": {
           "muplus": {
               "hasMuon": None,
               "isMuon": None,
               "ID": None,
           },
           "muminus": {
               "hasMuon": None,
               "isMuon": None,
               "ID": None,
           },
           "Kplus": {
               "hasMuon": None,
               "isMuon": None,
               "ID": None,
           },
       },
        "detector_presence": {
            "muplus": {
                "hasCalo": None,
                "hasRich": None,
            },
            "muminus": {
                "hasCalo": None,
                "hasRich": None,
            },
            "Kplus": {
                "hasCalo": None,
                "hasRich": None,
            },
        },
        "detector_usage": {
            "muplus": {
                "UsedRichAerogel": None,
                "UsedRich1Gas": None,
                "UsedRich2Gas": None,
            },
            "muminus": {
                "UsedRichAerogel": None,
                "UsedRich1Gas": None,
                "UsedRich2Gas": None,
            },
            "Kplus": {
                "UsedRichAerogel": None,
                "UsedRich1Gas": None,
                "UsedRich2Gas": None,
            },
        },
        "rich_thresholds": {
            "muplus": {
                "RichAboveElThres": None,
                "RichAboveMuThres": None,
                "RichAbovePiThres":None,
                "RichAboveKaThres": None,
                "RichAbovePrThres": None,
            },
            "muminus": {
                "RichAboveElThres": None,
                "RichAboveMuThres": None,
                "RichAbovePiThres": None,
                "RichAboveKaThres": None,
                "RichAbovePrThres": None,
            },
            "Kplus": {
                "RichAboveElThres": None,
                "RichAboveMuThres": None,
                "RichAbovePiThres": None,
                "RichAboveKaThres": None,
                "RichAbovePrThres": None,
            },
        },
        "pid_classifier": {
            "muplus": {
                "PIDe": None,
                "PIDmu": None,
                "PIDK": None,
                "PIDp": None,
                "PIDd": None,
                "ProbNNe": None,
                "ProbNNk": None,
                "ProbNNp": None,
                "ProbNNpi": None,
                "ProbNNmu": None,
                "ProbNNd": None,
                "ProbNNghost": None,
                "MC12TuneV2_ProbNNe": None,
                "MC12TuneV2_ProbNNmu": None,
                "MC12TuneV2_ProbNNpi": None,
                "MC12TuneV2_ProbNNk": None,
                "MC12TuneV2_ProbNNp": None,
                "MC12TuneV2_ProbNNghost": None,
                "MC12TuneV3_ProbNNe": None,
                "MC12TuneV3_ProbNNmu": None,
                "MC12TuneV3_ProbNNpi": None,
                "MC12TuneV3_ProbNNk": None,
                "MC12TuneV3_ProbNNp":None,
                "MC12TuneV3_ProbNNghost": None,
                "MC12TuneV4_ProbNNe": None,
                "MC12TuneV4_ProbNNmu": None,
                "MC12TuneV4_ProbNNpi": None,
                "MC12TuneV4_ProbNNk": None,
                "MC12TuneV4_ProbNNp": None,
                "MC12TuneV4_ProbNNghost": None,
                "MC15TuneV1_ProbNNe": None,
                "MC15TuneV1_ProbNNmu": None,
                "MC15TuneV1_ProbNNpi": None,
                "MC15TuneV1_ProbNNk": None,
                "MC15TuneV1_ProbNNp": None,
                "MC15TuneV1_ProbNNghost": None,

            },
            "muminus": {
                "PIDe": None,
                "PIDmu": None,
                "PIDK": None,
                "PIDp": None,
                "PIDd": None,
                "ProbNNe": None,
                "ProbNNk": None,
                "ProbNNp": None,
                "ProbNNpi": None,
                "ProbNNmu": None,
                "ProbNNd": None,
                "ProbNNghost": None,
                "MC12TuneV2_ProbNNe": None,
                "MC12TuneV2_ProbNNmu": None,
                "MC12TuneV2_ProbNNpi": None,
                "MC12TuneV2_ProbNNk": None,
                "MC12TuneV2_ProbNNp": None,
                "MC12TuneV2_ProbNNghost": None,
                "MC12TuneV3_ProbNNe": None,
                "MC12TuneV3_ProbNNmu": None,
                "MC12TuneV3_ProbNNpi": None,
                "MC12TuneV3_ProbNNk": None,
                "MC12TuneV3_ProbNNp": None,
                "MC12TuneV3_ProbNNghost": None,
                "MC12TuneV4_ProbNNe": None,
                "MC12TuneV4_ProbNNmu": None,
                "MC12TuneV4_ProbNNpi": None,
                "MC12TuneV4_ProbNNk": None,
                "MC12TuneV4_ProbNNp": None,
                "MC12TuneV4_ProbNNghost": None,
                "MC15TuneV1_ProbNNe": None,
                "MC15TuneV1_ProbNNmu": None,
                "MC15TuneV1_ProbNNpi": None,
                "MC15TuneV1_ProbNNk": None,
                "MC15TuneV1_ProbNNp": None,
                "MC15TuneV1_ProbNNghost": None,
            },
            "Kplus": {
                "PIDe": None,
                "PIDmu": None,
                "PIDK": None,
                "PIDp": None,
                "PIDd": None,
                "ProbNNe": None,
                "ProbNNk": None,
                "ProbNNp": None,
                "ProbNNpi": None,
                "ProbNNmu": None,
                "ProbNNd": None,
                "ProbNNghost": None,
                "MC12TuneV2_ProbNNe": None,
                "MC12TuneV2_ProbNNmu": None,
                "MC12TuneV2_ProbNNpi": None,
                "MC12TuneV2_ProbNNk": None,
                "MC12TuneV2_ProbNNp": None,
                "MC12TuneV2_ProbNNghost": None,
                "MC12TuneV3_ProbNNe": None,
                "MC12TuneV3_ProbNNmu": None,
                "MC12TuneV3_ProbNNpi": None,
                "MC12TuneV3_ProbNNk": None,
                "MC12TuneV3_ProbNNp": None,
                "MC12TuneV3_ProbNNghost": None,
                "MC12TuneV4_ProbNNe": None,
                "MC12TuneV4_ProbNNmu": None,
                "MC12TuneV4_ProbNNpi": None,
                "MC12TuneV4_ProbNNk": None,
                "MC12TuneV4_ProbNNp": None,
                "MC12TuneV4_ProbNNghost": None,
                "MC15TuneV1_ProbNNe": None,
                "MC15TuneV1_ProbNNmu": None,
                "MC15TuneV1_ProbNNpi": None,
                "MC15TuneV1_ProbNNk": None,
                "MC15TuneV1_ProbNNp": None,
                "MC15TuneV1_ProbNNghost": None,
            },
        },
        "kinematics": {
            "Bplus": {
                "P": None,
                "PT": None,
                "PE": None,
                "PX": None,
                "PY": None,
                "PZ": None,
                "M": None,
            },
            "J_psi_1S": {
                "P": None,
                "PT": None,
                "PE": None,
                "PX": None,
                "PY": None,
                "PZ": None,
                "M": None,
            },
            "muplus": {
                "P": None,
                "PT": None,
                "PE": None,
                "PX": None,
                "PY": None,
                "PZ": None,
                "M": None,
            },
            "muminus": {
                "P": None,
                "PT": None,
                "PE": None,
                "PX": None,
                "PY": None,
                "PZ": None,
                "M": None,
            },
            "Kplus": {
                "P": None,
                "PT": None,
                "PE": None,
                "PX": None,
                "PY": None,
                "PZ": None,
                "M": None,
            },
        },
        "track_vertex": {
            "Bplus":{
                "OWNPV_X": None,
                "OWNPV_Y": None,
                "OWNPV_Z": None,
                "OWNPV_XERR": None,
                "OWNPV_YERR": None,
                "OWNPV_ZERR": None,
                "OWNPV_CHI2": None,
                "OWNPV_NDOF": None,
                "OWNPV_COV_": None,
                "IP_OWNPV": None,
                "IPCHI2_OWNPV": None,
                "FD_OWNPV": None,
                "FD_CHI2_OWNPV": None,
                "DIRA_OWNPV": None,
            },
            "J_psi_1S": {
                "OWNPV_X": None,
                "OWNPV_Y": None,
                "OWNPV_Z": None,
                "OWNPV_XERR": None,
                "OWNPV_YERR": None,
                "OWNPV_ZERR": None,
                "OWNPV_CHI2": None,
                "OWNPV_NDOF": None,
                "OWNPV_COV_": None,
                "IP_OWNPV": None,
                "IPCHI2_OWNPV": None,
                "FD_OWNPV": None,
                "FD_CHI2_OWNPV": None,
                "DIRA_OWNPV": None,
                "ORIVX_X": None,
                "ORIVX_Y": None,
                "ORIVX_XERR": None,
                "ORIVX_YERR": None,
                "ORIVX_ZERR": None,
                "ORIVX_CHI2": None,
                "ORIVX_NDOF": None,
                "ORIVX_COV_": None,
                "FD_ORIVX": None,
                "FD_CHI2_ORIVX": None,
                "DIRA_ORIVX": None,
            },
            "muplus": {
                "OWNPV_X": None,
                "OWNPV_Y": None,
                "OWNPV_Z": None,
                "OWNPV_XERR": None,
                "OWNPV_YERR": None,
                "OWNPV_ZERR": None,
                "OWNPV_CHI2": None,
                "OWNPV_NDOF": None,
                "OWNPV_COV_": None,
                "IP_OWNPV": None,
                "IPCHI2_OWNPV": None,
                "ORIVX_X": None,
                "ORIVX_Y": None,
                "ORIVX_XERR": None,
                "ORIVX_YERR": None,
                "ORIVX_ZERR": None,
                "ORIVX_CHI2": None,
                "ORIVX_NDOF": None,
                "ORIVX_COV_": None,
            },
            "muminus": {
                "OWNPV_X": None,
                "OWNPV_Y": None,
                "OWNPV_Z": None,
                "OWNPV_XERR": None,
                "OWNPV_YERR": None,
                "OWNPV_ZERR": None,
                "OWNPV_CHI2": None,
                "OWNPV_NDOF": None,
                "OWNPV_COV_": None,
                "IP_OWNPV": None,
                "IPCHI2_OWNPV": None,
                "ORIVX_X": None,
                "ORIVX_Y": None,
                "ORIVX_XERR": None,
                "ORIVX_YERR": None,
                "ORIVX_ZERR": None,
                "ORIVX_CHI2": None,
                "ORIVX_NDOF": None,
                "ORIVX_COV_": None,
            },
            "Kplus": {
                "OWNPV_X": None,
                "OWNPV_Y": None,
                "OWNPV_Z": None,
                "OWNPV_XERR": None,
                "OWNPV_YERR": None,
                "OWNPV_ZERR": None,
                "OWNPV_CHI2": None,
                "OWNPV_NDOF": None,
                "OWNPV_COV_": None,
                "IP_OWNPV": None,
                "IPCHI2_OWNPV": None,
                "ORIVX_X": None,
                "ORIVX_Y": None,
                "ORIVX_XERR": None,
                "ORIVX_YERR": None,
                "ORIVX_ZERR": None,
                "ORIVX_CHI2": None,
                "ORIVX_NDOF": None,
                "ORIVX_COV_": None,
            },
        },
            "vertex_decay": {
                "Bplus": {
                    "ENDVERTEX_X": None,
                    "ENDVERTEX_Y": None,
                    "ENDVERTEX_Z": None,
                    "ENDVERTEX_XERR": None,
                    "ENDVERTEX_YERR": None,
                    "ENDVERTEX_ZERR": None,
                    "ENDVERTEX_CHI2": None,
                    "ENDVERTEX_NDOF": None,
                    "ENDVERTEX_COV_": None,
                    "MM": None,
                    "MMERR": None,
                    "ID": None,
                },
                "J_psi_1S": {
                    "ENDVERTEX_X": None,
                    "ENDVERTEX_Y": None,
                    "ENDVERTEX_Z": None,
                    "ENDVERTEX_XERR": None,
                    "ENDVERTEX_YERR": None,
                    "ENDVERTEX_ZERR": None,
                    "ENDVERTEX_CHI2": None,
                    "ENDVERTEX_NDOF": None,
                    "ENDVERTEX_COV_": None,
                    "MM": None,
                    "MMERR": None,
                    "ID": None,
                },
            },

        }

    metadata = {
        "nCandidate": None,
        "totCandidates": None,
        "EventInSequence": None,
        "runNumber": None,
        "eventNumber": None,
        "BCID": None,
        "BCType": None,
        "OdinTCK": None,
        "L0DUTCK": None,
        "HLT1TCK": None,
        "HLT2TCK": None,
        "GpsTime": None,
        "Polarity": None,
        "IntegratedLuminosity": None,
        "IntegratedLuminosityErr": None,
    }
    updated_event_data = update_data(matched_data, event_data)
    return updated_event_data
## be careful with this dict, you can see everything and I MEAN EVERYTHING, millions upon millions of data in here,
## (I printed a full JSON just for funsies and it took about 2 hours made a .json file over 8GB an counting
## and ultimately was pretty useless, kind of cool to see though.)
## I'll be using equations, and print specific events into .json files that are much smaller.
##Again, upROOT already has functions for this but for educational purposes I decided to do things manually
## so i could get better with Python, and I thought it would be better this way for a portfolio project.
##also it's none of your conCERN. (i swear that'll be the only pun, please dont walk away things are just getting good:)


def create_godot():
    pass


def get_root(root_path: Path = BASE_DIR / "data" / "raw" / "00334566_00000001_1.dvntuple.root"):
    data = lookup_files(BASE_DIR / "data" / "docs")
    root = update_root(data, root_path)
    return root

def main():
    root = get_root()


if __name__ == '__main__':
    main()
