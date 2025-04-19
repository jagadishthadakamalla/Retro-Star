import json
import pandas as pd

def load_data(filepath):
    """
    Load retrospective data from an Excel file
    """
    data = pd.read_excel(filepath)
    return data

def generate_summary(data):
    """
    Generate a structured summary from retrospective data
    """
    summary = {}

    # Create a summary for each team
    for team in data['Team Name'].unique():
        team_data = data[data['Team Name'] == team]
        team_summary = {
            "What Went Well": team_data['What went well'].tolist(),
            "Votes (Well)": team_data['Votes (Well)'].sum(),
            "What Can Be Improved": team_data['What can be improved'].tolist(),
            "Votes (Improve)": team_data['Votes (Improve)'].sum(),
            "Action Items": team_data['Action Items'].tolist()
        }
        summary[team] = team_summary

    # Sort action items for each team (optional)
    for team in summary:
        action_items = summary[team]["Action Items"]
        action_items_sorted = sorted(action_items, key=lambda x: len(x), reverse=True) # Example: Sort by length of action items
        summary[team]["Sorted Action Items"] = action_items_sorted
    return summary

def save_summary(summary, output_filepath):
    """
    Save the structured summary to a JSON file
    """
    with open(output_filepath, 'w') as f:
        json.dump(summary, f, indent=4)

# Example usage
if __name__ == "__main__":
    data = load_data('retrospectives_data.xlsx')
    summary = generate_summary(data)
    save_summary(summary, 'summary.json')