def solve_seating(n, subjects):
    remaining = [s["students"] for s in subjects]
    grid = [[-1 for _ in range(n)] for _ in range(n)]

    def is_safe(row, col, subject):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue

                nr = row + dr
                nc = col + dc

                if 0 <= nr < n and 0 <= nc < n:
                    if grid[nr][nc] == subject:
                        return False

        return True

    def backtrack(position):
        if position == n * n:
            return all(count == 0 for count in remaining)

        if sum(remaining) > n * n - position:
            return False

        row, col = divmod(position, n)

        candidates = sorted(
            range(len(subjects)),
            key=lambda s: remaining[s],
            reverse=True
        )

        for subject in candidates:
            if remaining[subject] <= 0:
                continue

            if is_safe(row, col, subject):
                grid[row][col] = subject
                remaining[subject] -= 1

                if backtrack(position + 1):
                    return True

                remaining[subject] += 1
                grid[row][col] = -1

        grid[row][col] = -1

        if backtrack(position + 1):
            return True

        return False

    if not backtrack(0):
        return None

    codes = []

    for i, subject in enumerate(subjects):
        words = subject["name"].split()
        code = "".join(word[0] for word in words[:3]).upper()

        if not code:
            code = f"S{i + 1}"

        codes.append(code[:5])

    return {
        "grid": grid,
        "subjects": [
            {
                "name": subjects[i]["name"],
                "students": subjects[i]["students"],
                "code": codes[i]
            }
            for i in range(len(subjects))
        ]
    }
