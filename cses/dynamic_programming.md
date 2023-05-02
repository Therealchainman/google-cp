# Dynamic Programming

## At the top of each script

```cpp
#include <bits/stdc++.h>
using namespace std;

inline int read()
{
	int x = 0, y = 1; char c = getchar();
	while (c < '0' || c > '9') {
		if (c == '-') y = -1;
		c = getchar();
	}
	while (c >= '0' && c <= '9') x = x * 10 + c - '0', c = getchar();
	return x * y;
}

inline long long readll() {
	long long x = 0, y = 1; char c = getchar();
	while (c < '0' || c > '9') {
		if (c == '-') y = -1;
		c = getchar();
	}
	while (c >= '0' && c <= '9') x = x * 10 + c - '0', c = getchar();
	return x * y;
}
```

## Coin Combinations I

### Solution 1:  iterative dp + order doesn't matter + Unordered Coin Change + O(nx) time

This can be solved by having two for loops in a particular order.

Iterate through the sum of the coins first and then through the coins, and add the coins for that sum. This leads to adding up very quicly for example if you have

```py
coins = [2, 3, 5], x = 9
dp = [[], [], [], [], [], [], [], [], [], []]
for when coin_sum = 2 it becomes
dp = [[], [], [2], [], [], [], [], [], [], []]
coin_sum = 3
dp = [[], [], [2], [3], [], [], [], [], [], []]
coin_sum = 4
dp = [[], [], [2], [3], [2, 2], [], [], [], [], []]
coin_sum = 5
dp = [[], [], [2], [3], [2, 2], [[3, 2], [2, 3], [5]], [], [], [], []]
coin_sum = 6
dp = [[], [], [2], [3], [2, 2], [[3, 2], [2, 3], [5]], [[2, 2, 2], [3, 3]], [[3, 2, 2], [2, 3, 2], [5, 2], [2, 2, 3], [2, 5]], [], []]
```

```cpp
int main() {
    int n = read(), x = read();
    int mod = 1e9 + 7;
    vector<int> dp(x + 1, 0);
    dp[0] = 1;
    vector<int> coins;
    for (int i = 0; i < n; i++) {
        int c = read();
        coins.push_back(c);
    }
    for (int coin_sum = 1; coin_sum <= x; coin_sum++) {
        for (int i = 0; i < n; i++) {
            if (coins[i] > coin_sum) continue;
            dp[coin_sum] = (dp[coin_sum] + dp[coin_sum - coins[i]]) % mod;
        }
    }
    cout << dp[x] << endl;
    return 0;
}
```

## Coin Combinations II

### Solution 1: iterative dp + order matters + O(nx) time

For this problem you want to iterate through the coins first and then the coin_sum. This is because you want to add the coins in a particular order. For example if you have

```py
coins = [2, 3, 5], x = 9
dp = [[], [], [], [], [], [], [], [], [], []]
coin = 2
dp = [[], [], [2], [], [[2, 2]], [], [[2, 2, 2]], [], [[2, 2, 2, 2]], []]
coin = 3
dp = [[], [], [2], [[3]], [[2, 2]], [[2, 3]], [[2, 2, 2], [3, 3]], [[2, 2, 3]], [[2, 2, 2, 2], [2, 3, 3]], [[2, 2, 2, 3], [3, 3, 3]]]
coin = 5
dp = [[], [], [2], [[3]], [[2, 2]], [[2, 3], [5]], [[2, 2, 2], [3, 3]], [[2, 2, 3], [2, 5]], [[2, 2, 2, 2], [2, 3, 3], [3, 5]], [[2, 2, 2, 3], [3, 3, 3], [2, 2, 5]]]
```

```cpp
int main() {
    int n = read(), x = read();
    int mod = 1e9 + 7;
    vector<int> dp(x + 1, 0);
    dp[0] = 1;
    vector<int> coins;
    for (int i = 0; i < n; i++) {
        int c = read();
        coins.push_back(c);
    }
    for (int i = 0; i < n; i++) {
        for (int coin_sum = coins[i]; coin_sum <= x; coin_sum++) {
            if (coins[i] > coin_sum) continue;
            dp[coin_sum] = (dp[coin_sum] + dp[coin_sum - coins[i]]) % mod;
        }
    }
    cout << dp[x] << endl;
    return 0;
}
```