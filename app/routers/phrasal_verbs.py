import os
import pandas as pd
from fastapi import APIRouter

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSLATED_CSV = os.path.join(BASE_DIR, "..", "data", "Mamka 50 translated.csv")
EXAMPLES_CSV = os.path.join(BASE_DIR, "..", "data", "Mamka 50.csv")

df_translated = pd.read_csv(TRANSLATED_CSV)
df_examples = pd.read_csv(EXAMPLES_CSV)
df = pd.merge(df_translated, df_examples, on="phrasal_verb", how="inner")

# Обратный словарь: перевод → фразовый глагол
reverse_lookup = {}
for _, row in df.iterrows():
    for meaning in [row["meaning_1"], row["meaning_2"], row["meaning_3"]]:
        if pd.notna(meaning):
            reverse_lookup[meaning.strip().lower()] = row["phrasal_verb"]

@router.get("/lookup")
def lookup(query: str):
    query = query.strip().lower()
    row = None

    if query in df['phrasal_verb'].str.lower().values:
        row = df[df['phrasal_verb'].str.lower() == query].iloc[0]
    elif query in reverse_lookup:
        pv = reverse_lookup[query]
        row = df[df['phrasal_verb'] == pv].iloc[0]
    else:
        return {
            "phrasal_verb": query,
            "translations": [],
            "example_en": "",
            "example_ru": ""
        }

    translations = [row['meaning_1']]
    if pd.notna(row['meaning_2']):
        translations.append(row['meaning_2'])
    if pd.notna(row['meaning_3']):
        translations.append(row['meaning_3'])

    return {
        "phrasal_verb": row['phrasal_verb'],
        "translations": translations,
        "example_en": row['example_en'],
        "example_ru": row['example_ru']
    }