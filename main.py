import sqlite3

def analyze_domains(domains):
    # A simple function to identify frequent patterns in domains
    patterns = {}
    for domain in domains:
        parts = domain.split('.')
        if len(parts) > 2:
            pattern = parts[-3]
            if pattern in patterns:
                patterns[pattern] += 1
            else:
                patterns[pattern] = 1

    frequent_patterns = [pattern for pattern, count in patterns.items() if count > 5]  # Adjust the threshold
    return frequent_patterns


def create_regex(frequent_patterns):
    # A simple function to convert patterns to regex
    regex_patterns = ["*." + pattern + ".*" for pattern in frequent_patterns]
    return '|'.join(regex_patterns)


def main():
    conn = sqlite3.connect('domains.db')
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT project_id FROM domains")
    project_ids = cursor.fetchall()

    for project_id in project_ids:
        cursor.execute("SELECT name FROM domains WHERE project_id=?", (project_id[0],))
        domains = cursor.fetchall()
        domains = [domain[0] for domain in domains]

        frequent_patterns = analyze_domains(domains)

        if frequent_patterns:
            regex = create_regex(frequent_patterns)
            cursor.execute("INSERT INTO rules (regexp, project_id) VALUES (?, ?)", (regex, project_id[0]))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
