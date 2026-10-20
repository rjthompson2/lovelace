from team.engineering.main import main
import sys

if __name__ == "__main__":
    task = " ".join(sys.argv[1:])
    main(task=task)