from typing import List, Dict

def generate_retro_summary(retro_data) -> List[Dict]:
 summaries = []
 grouped = retro_data.groupby(['Team', 'Sprint'])

 for (team, sprint), group in grouped:
    well_points = group['What Went Well'].dropna().tolist()
    well_votes = group['Votes (Well)'].fillna(0).astype(int).tolist()

    improve_points = group['What Can Be Improved'].dropna().tolist()
    improve_votes = group['Votes (Improve)'].fillna(0).astype(int).tolist()

    actions = group['Action Items'].dropna().tolist()

    summary = {
        "team": team,
        "sprint": sprint,
        "top_well_points": sorted(zip(well_points, well_votes), key=lambda x: x[1], reverse=True),
        "top_improvements": sorted(zip(improve_points, improve_votes), key=lambda x: x[1], reverse=True),
        "action_items": actions
    }

    summaries.append(summary)

 return summaries