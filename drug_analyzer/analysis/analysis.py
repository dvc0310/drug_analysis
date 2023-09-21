import seaborn as sns
import json
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Load the JSON file
with open("../drug_data.json", "r") as file:
    drug_data = json.load(file)

# Extract schedules and ratings
schedules = [attributes['schedule'] for drug, attributes in drug_data.items()]
ratings = [float(attributes['rating']) for drug, attributes in drug_data.items()]

# Create a DataFrame for visualization
df_schedule_rating = pd.DataFrame({
    'Schedule': schedules,
    'Rating': ratings
})

# Filter out the drugs with schedules "5", "M", and "Schedule 1"
filtered_df = df_schedule_rating[~df_schedule_rating['Schedule'].isin(['5', 'M', 'Schedule 1'])]

# Boxplot
plt.figure(figsize=(15, 8))
order = ['Not a controlled drug', 'Schedule 4', 'Schedule 3', 'Schedule 2']
sns.boxplot(x='Schedule', y='Rating', data=filtered_df, palette='pastel', order=order)
plt.title('Boxplot of Ratings by Schedule')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("boxplot_ratings.png")
plt.show()

# Tukey's HSD test
tukey_result = pairwise_tukeyhsd(endog=filtered_df['Rating'], groups=filtered_df['Schedule'], alpha=0.05)
print(tukey_result)
