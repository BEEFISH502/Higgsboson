from pathlib import Path
import uproot
import awkward
import matplotlib.pyplot as plt
import build_godot as godot

## set Base_dir for clean reusability ##
BASE_DIR = Path(__file__).resolve().parent.parent

def load_plotting_data():
    root = godot.get_root()
    return root



def plot_histograms(particle_data, particle_name):
    ## the fun stuff, plot our data so we can actually see what we're dealing with ##
    if not particle_data:
        print("No data found")
        return
    else:
        print('Data Found. Inititalizing graphs')

    plot_items = []
    for field_name, values in particle_data.items():
        if values is None:
            continue
        plot_items.append((field_name, values))

    n_plots = len(plot_items)

    if n_plots == 0:
        print(f'No data to record. Please check file and try again')
        return
## keep data clean and only package a certain amount of event in one graph,so we don'thave an endless scrolling screen
    cols = 3
    max_plots_per_page = 40
    for page_number, start in enumerate(range(0, len(plot_items), max_plots_per_page), start=1):
        page_items = plot_items[start:start + max_plots_per_page]
        rows = (n_plots + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(12, 4 * rows))

        if n_plots == 1:
            axes = [axes]
        else: axes = axes.flatten()
## name x and y axis
        for ax, (field_name, values) in zip(axes,page_items):
            flat_values = awkward.flatten(values, axis=None)
            hist_values = awkward.to_numpy(flat_values)
            ax.hist(hist_values, bins=50, edgecolor ="black")
            ax.set_title(f'{field_name}')
            ax.set_xlabel(field_name)
            ax.set_ylabel("Entries")
            ax.grid(True, linestyle='--', alpha=0.4)

        for ax in axes[n_plots:]:
            ax.set_visible(False)
#render graphs anda window then display
        fig.suptitle(f'{particle_name} histograms -- page {page_number}', fontsize=16)
        plt.tight_layout()
        plt.show()


def main():
    root_data = load_plotting_data()
    print("Available Categories: ")
    for category in root_data:
        print(f"- {category}")

    selected_category = input("Enter a category: ").strip()
    if selected_category not in root_data:
        print(f"Invalid category. Please try again.")
        return

    category_data = root_data[selected_category]

    print(f'Available particles: ')
    for particle in category_data:
        print(f'- {particle}')

    selected_particle = input('Enter a particle: ').strip()

    if selected_particle not in category_data:
        print('Invalid particle. Please try again.')
        return
    particle_data = category_data[selected_particle]
    plot_histograms(particle_data, selected_particle)


if __name__ == '__main__':
    main()

