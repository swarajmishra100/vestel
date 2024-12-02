import networkx as nx
import pandas as pd

G = nx.DiGraph()

df = pd.read_csv('nasdaq_clean.csv')
print(df.head())
