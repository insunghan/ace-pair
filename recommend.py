import itertools
import json

# Load data
with open("data/players.json") as f:
    players = json.load(f)

def synergy_score(p1, p2):
    score = 0

    # 스타일 상보성
    if p1["style"] != p2["style"]:
        score += 2

    # 포핸드 사이드 다름
    if p1["forehand_side"] != p2["forehand_side"]:
        score += 1

    # 평균 네트/발리/스피드
    for attr in ["net_play", "volley", "speed"]:
        score += (p1[attr] + p2[attr]) / 2

    # 서브 안정성
    score += ((p1["first_serve_pct"] - p1["double_fault_pct"]) +
              (p2["first_serve_pct"] - p2["double_fault_pct"])) * 10  # 가중치 부여

    return round(score, 2)

def recommend_best_doubles(players):
    best_score = -1
    best_combination = None

    # 4명을 뽑아 가능한 모든 2 vs 2 조합을 생성
    for four_players in itertools.combinations(players, 4):
        for team1 in itertools.combinations(four_players, 2):
            team2 = [p for p in four_players if p not in team1]

            team1_score = synergy_score(team1[0], team1[1])
            team2_score = synergy_score(team2[0], team2[1])
            total_score = team1_score + team2_score

            if total_score > best_score:
                best_score = total_score
                best_combination = {
                    "team1": [team1[0]["name"], team1[1]["name"]],
                    "team2": [team2[0]["name"], team2[1]["name"]],
                    "team1_score": team1_score,
                    "team2_score": team2_score,
                    "total_score": total_score
                }

    return best_combination

result = recommend_best_doubles(players)
print("🏆 Best Doubles Recommendation:")
print(result)
