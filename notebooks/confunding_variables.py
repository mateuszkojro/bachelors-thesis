# %%
import pandas as pd
import dataset
from dataset import split_validation_training, FFT_COLS
from scipy.stats import kruskal

dataset.VALIDATION_SET = []

# %%
metadata = pd.read_json("../results/metadata.json", orient='index')
measurements = pd.read_csv('../results/dataset.csv')
measurements, nothing = split_validation_training(measurements)
# %%
# for t, person in metadata.groupby('email'):
#     print(person.to_markdown())

metadata["id"] = metadata.index
# %%

combined = pd.merge(measurements, metadata, on='id')
combined

# %%
index = ~(combined[FFT_COLS(combined)].isna().T.any())
# %%

combined = combined[index].copy()
combined[FFT_COLS(combined)]
# %%
combined["sleep_less_than_8"] = combined["hours_of_sleep"][combined["hours_of_sleep"].replace('', 0).astype(int) < 8]
combined["computer_less_than_8"] = combined["hours_in_front_of_computer"][combined["hours_in_front_of_computer"].replace('', 0).astype(int) < 8]
combined["exhaustion_less_than_3"] = combined["exhaustion_level"][combined["exhaustion_level"].replace('', 0).astype(int) < 3]
combined["psychoactive_substances"].fillna('brak', inplace=True)
combined["mental_arithemtic_high"] = 1;
combined["mental_arithemtic_high"] =  combined["mental_arithemtic_high"].where((combined["mental_calculations"]=="1_to_10_times_a_day") | (combined["mental_calculations"]=="more_than_10_times_a_day"), 0)
combined["battery_high"] = combined["EEG.BatteryPercent"][combined["EEG.BatteryPercent"] < 20]
#%%
def anova(df, grouper):
    df = df[df["label"] == "waiting"]
    grouped = list(df.groupby(grouper))
    groups = [group[FFT_COLS(combined)].mean().to_numpy() for _, group in grouped]
    return kruskal(*groups)

# %%
confunding_variables = [
                        "gender", 
                        "sleep_less_than_8",
                        "computer_less_than_8",
                        "exhaustion_less_than_3",
                        "psychoactive_substances",
                        "mental_arithemtic_high",
                        "battery_high"
                        # "hours_of_sleep", 
                        # "exhaustion_level", 
                        # "hours_in_front_of_computer", 
                        # "mental_calculations", 
                        ]
for variable in confunding_variables:
    k = anova(combined, variable)
    print(f"{variable=}: {k}")
# %%
combined["EEG.BatteryPercent"].hist()
# %%
