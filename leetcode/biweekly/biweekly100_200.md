# Leetcode Biweekly Contest 135

## Minimum Array Changes to Make Differences Equal

### Solution 1:  sort, multiset, greedy

```cpp
class Solution {
public:
    int minChanges(vector<int>& nums, int k) {
        int N = nums.size();
        vector<pair<int, int>> data;
        for (int i = 0; i < N / 2; i++) {
            int a = nums[i], b = nums[N - i - 1];
            if (a > b) swap(a, b);
            int p = max(k - a, b);
            data.emplace_back(b - a, p);
        }
        sort(data.begin(), data.end());
        multiset<int> pool;
        int ans = N / 2, ptr = 0, cur = N / 2;
        for (int x = 0; x <= k; x++) {
            int cnt_equal = 0;
            for (auto it = pool.begin(); it != pool.end(); it++) {
                if (x <= *it) break;
                pool.erase(it);
                cur++;
            }
            while (ptr < N / 2 && data[ptr].first == x) {
                pool.insert(data[ptr++].second);
                cnt_equal++;
            }
            ans = min(ans, cur - cnt_equal);
        }
        return ans;
    }
};
```

## Maximum Score From Grid Operations

### Solution 1:  dynamic programming with 3 states, prefix sums, dp on matrix

```cpp

```

# Leetcode Biweekly Contest 136

## Minimum Number of Flips to Make Binary Grid Palindromic II

### Solution 1:  connected components, counting, greedy

```cpp
class Solution {
public:
    int minFlips(vector<vector<int>>& grid) {
        int R = grid.size(), C = grid[0].size();
        int ans = 0;
        for (int r = 0; r < R / 2; r++) {
            for (int c = 0; c < C / 2; c++) {
                int cnt1 = grid[r][c] + grid[r][C - c - 1] + grid[R - r - 1][c] + grid[R - r - 1][C - c - 1];
                ans += min(cnt1, 4 - cnt1);
            }
        }
        int freq[3];
        memset(freq, 0, sizeof(freq));
        if (R & 1) {
            for (int c = 0; c < C / 2; c++) {
                int cnt = grid[R / 2][c] + grid[R / 2][C - c - 1];
                freq[cnt]++;
            }
        }
        if (C & 1) {
            for (int r = 0; r < R / 2; r++) {
                int cnt = grid[r][C / 2] + grid[R - r - 1][C / 2];
                freq[cnt]++;
            }
        }
        if ((freq[2] & 1) && freq[1] == 0) freq[1] += 2;
        ans += freq[1];
        if ((R & 1) && (C & 1)) {
            ans += grid[R / 2][C / 2];
        }
        return ans;
    }
};
```

## 3241. Time Taken to Mark All Nodes

### Solution 1:  reroot dp on tree, dfs

```cpp
class Solution {
public:
    int N;
    vector<vector<int>> adj;
    vector<int> ans, max_d1, max_d2, max_c1, max_c2, max_p;
    void dfs1(int u, int p = -1) {
        for (int v : adj[u]) {
            if (v == p) continue;
            dfs1(v, u);
            int cd = max_d1[v] + (v % 2 == 0 ? 2 : 1);
            if (cd > max_d1[u]) {
                max_d2[u] = max_d1[u];
                max_c2[u] = max_c1[u];
                max_d1[u] = cd;
                max_c1[u] = v;
            } else if (cd > max_d2[u]) {
                max_d2[u] = cd;
                max_c2[u] = v;
            }
        }
    }
    void dfs2(int u, int p = -1) {
        ans[u] = max(max_p[u], max_d1[u]);
        for (int v : adj[u]) {
            if (v == p) continue;
            if (v != max_c1[u]) {
                max_p[v] = max(max_p[u], max_d1[u]) + (u % 2 == 0 ? 2 : 1);
            } else {
                max_p[v] = max(max_p[u], max_d2[u]) + (u % 2 == 0 ? 2 : 1);
            }
            dfs2(v, u);
        }
    }
    vector<int> timeTaken(vector<vector<int>>& edges) {
        N = edges.size() + 1;
        adj.assign(N, {});
        for (const auto &edge : edges) {
            int u = edge[0], v = edge[1];
            adj[u].push_back(v);
            adj[v].push_back(u);
        }
        max_d1.assign(N, 0);
        max_d2.assign(N, 0);
        max_c1.assign(N, -1);
        max_c2.assign(N, -1);
        dfs1(0);
        ans.resize(N);
        max_p.assign(N, 0);
        dfs2(0);
        return ans;
    }
};
```

# Leetcode Biweekly Contest 137

## 

### Solution 1: 

```cpp

```

## 

### Solution 1: 

```cpp

```

# Leetcode Biweekly Contest 138

## 

### Solution 1: 

```cpp

```

## 3273. Minimum Amount of Damage Dealt to Bob

### Solution 1:  greedy, sorting, exchange argument

```cpp
int ceil(int x, int y) {
    return (x + y - 1) / y;
}
struct Monster {
    long long dmg, turns;
    Monster() {}
    Monster(long long dmg, long long turns) : dmg(dmg), turns(turns) {}
    bool operator<(const Monster &other) const {
        long long cost1 = turns * (dmg + other.dmg) + other.dmg * other.turns;
        long long cost2 = other.turns * (dmg + other.dmg) + dmg * turns;
        return cost1 < cost2;
    }
};
class Solution {
public:
    long long minDamage(int power, vector<int>& damage, vector<int>& health) {
        int N = damage.size();
        long long ans = 0, dmg = 0;
        vector<Monster> arr(N);
        for (int i = 0; i < N; i++) {
            dmg += damage[i];
            arr[i] = Monster(damage[i], ceil(health[i], power));
        }
        sort(arr.begin(), arr.end());
        for (const Monster &m : arr) {
            ans += dmg * m.turns;
            dmg -= m.dmg;
        }
        return ans;
    }
};
```

# Leetcode Biweekly Contest 139

## 

### Solution 1: 

```cpp

```

## 

### Solution 1: 

```cpp

```