from utils.generate import generate_output_content


def main() -> int:
    print("Hello from ares!")
    print(
        generate_output_content("BFS", 16, 695, 4321, 58.12, 12.56, "uLulDrrRRRRRRurD")
    )
    return 0
