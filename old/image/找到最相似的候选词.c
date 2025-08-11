#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <limits.h>

// 计算两个字符串的编辑距离
int levenshtein(const char *s1, const char *s2) {
    int len1 = strlen(s1);
    int len2 = strlen(s2);
    int dp[len1 + 1][len2 + 1];

    for (int i = 0; i <= len1; i++) dp[i][0] = i;
    for (int j = 0; j <= len2; j++) dp[0][j] = j;

    for (int i = 1; i <= len1; i++) {
        for (int j = 1; j <= len2; j++) {
            int cost = (s1[i-1] == s2[j-1]) ? 0 : 1;
            dp[i][j] = fmin(dp[i-1][j] + 1, fmin(dp[i][j-1] + 1, dp[i-1][j-1] + cost));
        }
    }

    return dp[len1][len2];
}

// 找到最相似的候选词
const char* find_closest(const char *word, const char *candidates[], int count) {
    int min_distance = INT_MAX;
    const char *best_match = NULL;

    for (int i = 0; i < count; i++) {
        int dist = levenshtein(word, candidates[i]);
        if (dist < min_distance) {
            min_distance = dist;
            best_match = candidates[i];
        }
    }

    return best_match;
}

int main() {
    const char *candidates[] = {"螺丝", "螺母", "垫片", "弹簧", "钢圈"};
    const char *ocr_result[] = {"裸丝", "锣母", "电片", "弹黄", "刚圈"};
    int num_candidates = sizeof(candidates) / sizeof(candidates[0]);
    int num_ocr = sizeof(ocr_result) / sizeof(ocr_result[0]);

    for (int i = 0; i < num_ocr; i++) {
        const char *closest = find_closest(ocr_result[i], candidates, num_candidates);
        printf("OCR识别: %s → 匹配: %s\n", ocr_result[i], closest);
    }

    return 0;
}
