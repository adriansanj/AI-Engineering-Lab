import os
import kagglehub
import pandas as pd
from datasets import Dataset

def load_dataset():
    path = kagglehub.dataset_download("nasirkhalid24/the-office-us-complete-dialoguetranscript")
    file_path = os.path.join(path, "The-Office-Lines-V4.csv")
    df = pd.read_csv(file_path)
    return df

def format_dataset(row):
    return [
        {"role": "user", "content": row["line"]},
        {"role": "assistant", "content": row["michael_response"]},
    ]

def create_conversation_pairs(df):
    df["previous_speaker"] = df.groupby(["season", "episode", "scene"])["speaker"].shift(1)
    df["next_speaker"] = df.groupby(["season", "episode", "scene"])["speaker"].shift(-1)
    michael_responses = df[(df["speaker"] == "Michael") & (df["previous_speaker"].notna()) & (df["previous_speaker"] != "Michael")]
    character_lines = df[(df["speaker"] != "Michael") & (df["next_speaker"].notna()) & (df["next_speaker"] == "Michael")]
    final_df = character_lines[["speaker", "line"]].copy()
    final_df["michael_response"] = michael_responses["line"].values

    final_df["messages"] = final_df.apply(format_dataset, axis=1)
    
    dataset = Dataset.from_pandas(final_df[["messages"]], preserve_index=False)

    return dataset


def main():
    
    print("Loading dataset...")
    df = load_dataset()
    print("Dataset loaded. Creating conversation pairs...")
    dataset = create_conversation_pairs(df)
    print("Conversation pairs created.")

    print(len(dataset), "conversation pairs created. Pushing to Hugging Face Hub...")
    dataset.push_to_hub(
        "adrianse/the-office-michael-scott-conversations", 
        token=os.getenv("HUGGING_FACE_HUB_TOKEN")
    )
    print("Dataset pushed to Hugging Face Hub.")


if __name__ == "__main__":
    main()