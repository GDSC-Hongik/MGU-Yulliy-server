import re
import sys

# 커밋 메시지 형식을 정의합니다.
COMMIT_MSG_REGEX = r"^(feat|fix|docs|style|refactor|test|chore):\s.+"


def validate_commit_message(commit_msg_file):
    with open(commit_msg_file, "r") as file:
        commit_msg = file.read().strip()

    if not re.match(COMMIT_MSG_REGEX, commit_msg):
        print("Error: Invalid commit message format.")
        print("Commit message should start with one of the following types:")
        print("feat, fix, docs, style, refactor, test, chore")
        print('Example: "feat: add new user login feature"')
        sys.exit(1)


if __name__ == "__main__":
    validate_commit_message(sys.argv[1])
