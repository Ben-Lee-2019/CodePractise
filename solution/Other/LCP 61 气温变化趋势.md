# LCP 61. 气温变化趋势

URL: https://leetcode.cn/problems/6CE719/
Difficulty: Easy
Notes: 简单题，注意Integer.compare方法
Tag: Other
Best Times/Space: O(n),O(1)
Last edited time: June 21, 2024 10:53 AM

## LCP 61. 气温变化趋势

![Untitled](image/LCP%2061%20%E6%B0%94%E6%B8%A9%E5%8F%98%E5%8C%96%E8%B6%8B%E5%8A%BF/Untitled.png)

python  没有Integer.compare类型函数，但是`(a1 > a2) - (a1 < a2)`的设计比较精妙

```python
class Solution:
    def temperatureTrend(self, temperatureA: List[int], temperatureB: List[int]) -> int:
        ans = same = 0
        for (a1, b1), (a2, b2) in pairwise(zip(temperatureA, temperatureB)):
            if (a1 > a2) - (a1 < a2) == (b1 > b2) - (b1 < b2):
                same += 1
                ans = max(ans, same)
            else:
                same = 0
        return ans
```

```java
class Solution {
    public int temperatureTrend(int[] temperatureA, int[] temperatureB) {
        int ans = 0, count = 0;
        for (int i = 1; i < temperatureA.length; i++) {
            int a = Integer.compare(temperatureA[i] , temperatureA[i - 1]);
            int b = Integer.compare(temperatureB[i] , temperatureB[i - 1]);
            if (a == b) {
                count++;
            } else {
                ans = Math.max(ans, count);
                count = 0;
            }
        }
        ans = Math.max(ans, count);
        return ans;
    }
}
```