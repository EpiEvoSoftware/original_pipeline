import matplotlib.pyplot as plt
import pandas as pd
import argparse


## Draw the distribution trajectory: 
eff_size = pd.read_csv("/Users/px54/Documents/TB_software/covid_test/strain_trajectory.txt", header=None, names=range(5))
eff_size = pd.concat([pd.DataFrame({i: [1] for i in range(5)}), eff_size]).reset_index(drop=True)

eff_size_normalized = eff_size.div(eff_size.sum(axis=1), axis=0)

eff_size_normalized

ax = eff_size_normalized.plot(kind='area', stacked=True, figsize=(10, 6), cmap='viridis')

plt.xlabel('Generations')
plt.ylabel('Proportion of strain')
plt.title('Change of the Proportion of Different strains Through Time')
plt.ylim(0, 1)
plt.xlim(0, 360)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.tight_layout()
plt.show()


## Draw the SEIR trajectory
seir = pd.read_csv("/Users/px54/Documents/TB_software/covid_test/SIR_trajectory.txt", header=None, names=["S", "E", "I", "R"])
#eff_size = pd.concat([pd.DataFrame({i: [1] for i in range(10)}), eff_size]).reset_index(drop=True)
seir
ax = seir.plot(kind='line', figsize=(10, 6), cmap='viridis')

plt.xlabel('Generations')
plt.ylabel('number of hosts')
plt.title('SEIR Trajectory')
plt.ylim(0, 10000)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.tight_layout()

plt.show()


def main():
    parser = argparse.ArgumentParser(description='Time the fastas.')
    parser.add_argument('-wk_dir', action='store',dest='wk_dir', required=True)

    args = parser.parse_args()
    wk_dir_ = args.wk_dir




if __name__ == "__main__":
    main()

