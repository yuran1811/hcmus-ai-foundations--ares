from utils import generate_output_content


def test_generate_output_content():
    assert (
        generate_output_content("BFS", 16, 695, 4321, 58.12, 12.56, "uLulDrrRRRRRRurD")
        == "BFS\nSteps: 16, Weight: 695, Node: 4321, Time (ms): 58.12, Memory (MB): 12.56\nuLulDrrRRRRRRurD\n"
    )
