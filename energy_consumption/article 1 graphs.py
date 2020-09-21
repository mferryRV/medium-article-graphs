import matplotlib.pyplot as pyplot
import squarify
import pandas

# Create pie chart from this data: https://www.epa.gov/ghgemissions/global-greenhouse-gas-emissions-data#Sector
title = "Global Greenhouse Gas Emissions\nby Economic Sector"
sizes = [24, 25, 21, 14, 6, 10]
titles = ["Agriculture, Forestry,\nand Other Land Use",
  "Electricity and Heat Production",
  "Industry",
  "Transportation",
  "Buildings",
  "Other Energy"]
colors = ["#bfdcae", "#fa7d09", "#9cada4", "#e8ded2", "#fa1616", "#e0ece4"]
labels = [x + "\n(" + str(sizes[i]) + "%)" for i, x in enumerate(titles)]
squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.85, bar_kwargs=dict(linewidth=3, edgecolor="#F0F0F0"))
pyplot.title(title, fontsize=18, fontweight="bold")
pyplot.axis("off")
pyplot.show()

# Show growth in emissions from this graph: https://ourworldindata.org/co2-and-other-greenhouse-gas-emissions#how-have-global-co2-emissions-changed-over-time
input_df = pandas.read_csv('annual-co-emissions-by-region.csv')
included_entities = list(reversed([
  "United States",
  "EU-28",
  "Europe (excl. EU-28)",
  "China",
  "India",
  "Asia (excl. China & India)",
  "Africa",
  "South America",
  "North America (excl. USA)",
  "Oceania",
  "International transport"
]))
# Only since 1900
input_df = input_df[input_df["Year"].ge(1900)]

# Get a dataframe for each entity (year, emissions) named for the entity
def get_entity_df(entity):
  source_df = input_df.copy(deep=True)
  df = source_df[source_df["Entity"].eq(entity)].filter(items=["Year", "Annual CO2 emissions"])
  df.columns = ["Year", entity]
  return df

entity_dataframes = list(map(get_entity_df, included_entities))

# Join them all to create a single dataframe
emissions_df = pandas.DataFrame(index=pandas.Series(name="Year", data=sorted(input_df["Year"].unique())))
for entity in entity_dataframes:
  emissions_df = emissions_df.merge(entity, on="Year", how="left")

# Add labels and order legend
ax = emissions_df.plot(x="Year", kind="area", stacked=True)
pyplot.title("Annual CO$_2$ Emissions by World Region", fontsize=18, fontweight="bold")
pyplot.ylabel("CO$_2$ emissions (megatons)")
handles, labels = ax.get_legend_handles_labels()
ax.legend(reversed(handles), reversed(labels), loc='upper left')

pyplot.show(block=True)
