#include <stdio.h>

#define MAX 10
#define MAX_SUBJECTS 10

int grid[MAX][MAX];
int n;
int subjectCount;
int students[MAX_SUBJECTS];

int isSafe(int row, int col, int subject)
{
    int dr, dc;
    int nr, nc;

    for (dr = -1; dr <= 1; dr++)
    {
        for (dc = -1; dc <= 1; dc++)
        {
            if (dr == 0 && dc == 0)
                continue;

            nr = row + dr;
            nc = col + dc;

            if (nr >= 0 && nr < n &&
                nc >= 0 && nc < n)
            {
                if (grid[nr][nc] == subject)
                    return 0;
            }
        }
    }

    return 1;
}

int solve(int position)
{
    int row, col;
    int subject;

    if (position == n * n)
    {
        for (subject = 0; subject < subjectCount; subject++)
        {
            if (students[subject] != 0)
                return 0;
        }

        return 1;
    }

    row = position / n;
    col = position % n;

    for (subject = 0; subject < subjectCount; subject++)
    {
        if (students[subject] > 0 &&
            isSafe(row, col, subject + 1))
        {
            grid[row][col] = subject + 1;
            students[subject]--;

            if (solve(position + 1))
                return 1;

            grid[row][col] = 0;
            students[subject]++;
        }
    }

    grid[row][col] = 0;

    if (solve(position + 1))
        return 1;

    return 0;
}

int main()
{
    int i, j;
    int total = 0;

    if (scanf("%d %d", &n, &subjectCount) != 2)
    {
        printf("ERROR\n");
        return 1;
    }

    if (n < 1 || n > MAX ||
        subjectCount < 1 ||
        subjectCount > MAX_SUBJECTS)
    {
        printf("ERROR\n");
        return 1;
    }

    for (i = 0; i < subjectCount; i++)
    {
        if (scanf("%d", &students[i]) != 1 ||
            students[i] < 0)
        {
            printf("ERROR\n");
            return 1;
        }

        total += students[i];
    }

    if (total > n * n)
    {
        printf("NO\n");
        return 0;
    }

    for (i = 0; i < n; i++)
    {
        for (j = 0; j < n; j++)
        {
            grid[i][j] = 0;
        }
    }

    if (solve(0))
    {
        printf("OK\n");

        for (i = 0; i < n; i++)
        {
            for (j = 0; j < n; j++)
            {
                printf("%d ", grid[i][j]);
            }

            printf("\n");
        }
    }
    else
    {
        printf("NO\n");
    }

    return 0;
}
