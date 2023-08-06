import requests

URL_BASE = "https://api.lolpros.gg"


def get_teams(region: str = "", page: int = 1):
    resp = requests.get(f"{URL_BASE}/es/teams?page={page}&region={region}")
    resp.raise_for_status()
    return resp.json()


def get_team_by_name(team_name: str) -> dict:
    resp = requests.get(f"{URL_BASE}/es/teams/{team_name}")
    resp.raise_for_status()
    return resp.json()


def get_team_by_tag(team_tag: str) -> dict:
    all_teams = get_teams()
    for team in all_teams:
        if team.get("tag") == team_tag:
            return team
    raise KeyError("Team not found.")


def get_players_by_team(team_name: str) -> list:
    team_info = get_team_by_name(team_name=team_name)

    return [{'role': member['position'].split('_')[1], 'name': member['slug']} for member in
            team_info['current_members'] if
            member['position'] is not None]


def get_player_by_name(player_name: str):
    resp = requests.get(f"{URL_BASE}/es/players/{player_name}")
    resp.raise_for_status()
    return resp.json()


def get_player_summoner_info(player_name: str):
    player_info = get_player_by_name(player_name=player_name)

    if player_info['league_player'] is not None:
        return [account for account in player_info['league_player']['accounts']]
    return []


def get_player_summoner_names(player_name: str):
    player_info = get_player_by_name(player_name=player_name)

    if player_info['league_player'] is not None:
        return [account['summoner_name'] for account in player_info['league_player']['accounts']]
    return []


def get_summoner_rankings(summoner_uuid: str, months: int = 1):
    resp = requests.get(f"{URL_BASE}/lol/riot-accounts/{summoner_uuid}/rankings?months={months}")
    resp.raise_for_status()
    return resp.json()
