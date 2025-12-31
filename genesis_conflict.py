import random
import time

# ==========================================================
# Genesis-1: The Internal Friction (内在撕裂变体)
# 模拟“高权重维度的互斥”导致的生命快速耗竭（精神内耗）
# ==========================================================

class LifeKernel:
    def __init__(self):
        self.hp = 1.0
        self.alive = True

    def consume(self, rate):
        if not self.alive: return
        self.hp *= (1 - rate)
        if self.hp <= 0.0001: self.alive = False

class ConflictedPreferenceCore:
    def __init__(self):
        # 【关键修改】强制植入“矛盾人格”
        # 对“秩序”和“新奇”都有极高的渴望，且不可妥协
        self.weights = {
            "symmetry":    random.uniform(0.75, 0.95), # 极度渴望秩序
            "novelty":     random.uniform(0.75, 0.95), # 极度渴望新奇
            "compression": random.uniform(0.1, 0.5),   # 其他维度次要
            "rhythm":      random.uniform(0.1, 0.5),
        }

    def affinity(self, structure):
        return sum(self.weights[k] * structure.get(k, 0) for k in self.weights)

class MutuallyExclusiveEnvironment:
    def generate_structures(self):
        structures = []
        for _ in range(5):
            # 【关键修改】制造“不可能三角”环境
            # 高对称性必然导致低新奇度，反之亦然
            # 现实世界很少提供既完美对称又极度新奇的事物
            sym = random.random()
            
            # 互斥逻辑：Novelty = 1.0 - Symmetry + 随机扰动
            # 这意味着两者之和很难超过 1.0，但实体的期望和是 ~1.7
            nov = 1.0 - sym + random.uniform(-0.1, 0.1)
            nov = max(0.0, min(1.0, nov)) # 截断

            structures.append({
                "symmetry":    sym,
                "novelty":     nov,
                "compression": random.random(),
                "rhythm":      random.random(),
            })
        return structures

class Entity:
    def __init__(self):
        self.life = LifeKernel()
        self.pref = ConflictedPreferenceCore() # 使用矛盾人格
        self.log = []

    def step(self, environment):
        if not self.life.alive: return
        
        options = environment.generate_structures()
        scored = sorted([(self.pref.affinity(opt), opt) for opt in options], reverse=True)
        best_score, _ = scored[0]

        # 计算痛苦指数
        # 由于环境互斥，best_score 很难达到高分
        # mismatch_penalty 将长期居高不下
        base_cost = 0.01
        mismatch_penalty = (1 - best_score / 2.0) * 0.03 # 稍微调整系数以放大感知
        cost = base_cost + mismatch_penalty

        self.life.consume(cost)
        self.log.append({
            "step": len(self.log) + 1,
            "hp": round(self.life.hp, 6),
            "score": round(best_score, 4),
            "cost": round(cost, 4)
        })

if __name__ == "__main__":
    env = MutuallyExclusiveEnvironment()
    entity = Entity()

    print(f"--- Genesis-1: Internal Friction Entity Born ---")
    print(f"矛盾偏好: Symmetry={entity.pref.weights['symmetry']:.2f}, Novelty={entity.pref.weights['novelty']:.2f}")
    print(f"注定悲剧：渴望的总和 (~1.7) 远超环境允许的极限 (~1.0)\n")

    for _ in range(1000):
        entity.step(env)
        if not entity.life.alive: break

    print(f"实体于第 {len(entity.log)} 步耗尽（死于内耗）。")
    print(f"最终 HP: {entity.life.hp:.8f}")
    if len(entity.log) > 0:
        avg_score = sum(i['score'] for i in entity.log) / len(entity.log)
        print(f"一生平均满意度: {avg_score:.4f} (长期低迷)")
