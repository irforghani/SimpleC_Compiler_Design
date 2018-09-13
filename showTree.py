from graphviz import Source
graph = open("graph_table.txt", 'r')
temp = """
digraph G{
edge [dir=forward]
node [shape=plaintext]
program_original -> { program  example open_parantes input kama output clos_parantes semicolon }
}
"""
print(temp)
s = Source(temp, filename="test.gv", format="png")
s.view()