import automata_toolkit
from visual_automata.fa.dfa import VisualDFA

commentsDFA = VisualDFA(

    states={"q0", "q1"},
    input_symbols={";", "Anything Else"},
    transitions={
        "q0": {";": "q0", "Anything Else": "q1"},
        "q1": {";": "q1", "Anything Else": "q1"},

    },
    initial_state="q0",
    final_states={"q1"}
)

stringDFA = VisualDFA(
    states={"q0", "q1", "q2", "q3", "Dead"},
    input_symbols={"Space", "\"", "\\\\", "All except [\"]"},
    transitions={
        "q0": {"Space": "q0", "\"": "q1", "\\\\": "Dead", "All except [\"]": "Dead"},
        "q1": {"Space": "q1", "\"": "q3", "\\\\": "q2", "All except [\"]": "q1"},
        "q2": {"Space": "q2", "\"": "q1", "\\\\": "q1", "All except [\"]": "q1"},
        "q3": {"Space": "q3", "\"": "Dead", "\\\\": "Dead", "All except [\"]": "Dead"},
        "Dead": {"Space": "Dead", "\"": "Dead", "\\\\": "Dead", "All except [\"]": "Dead"}

    },
    initial_state="q0",
    final_states={"q3"}
)

numbersDFA = VisualDFA(
    states={"q0", "q1", "q2", "q3", "Dead"},
    input_symbols={"Space", "[0-9]", "Dot(.)"},
    transitions={
        "q0": {"Space": "q0", "[0-9]": "q1", "Dot(.)": "q3"},
        "q1": {"Space": "q1", "[0-9]": "q1", "Dot(.)": "Dead"},
        "q2": {"Space": "q2", "[0-9]": "q2", "Dot(.)": "Dead"},
        "q3": {"Space": "q3", "[0-9]": "q1", "Dot(.)": "Dead"},
        "Dead": {"Space": "Dead", "[0-9]": "Dead", "Dot(.)": "Dead"}
    },
    initial_state="q0",
    final_states={"q1", "q2"}
)

relationalOperatorsDFA = VisualDFA(
    states={"q0", "q1", "q2", "q3", "q4", "q5", "q6", "Dead"},
    input_symbols={"<= | >= | = | <>", "[0-9]", "Dot(.)", "Space"},
    transitions={
        "q0": {"<= | >= | = | <>": "q1", "[0-9]": "Dead", "Dot(.)": "Dead", "Space": "Dead"},
        "q1": {"<= | >= | = | <>": "Dead", "[0-9]": "Dead", "Dot(.)": "Dead", "Space": "q2"},
        "q2": {"<= | >= | = | <>": "Dead", "[0-9]": "q3", "Dot(.)": "Dead", "Space": "q2"},
        "q3": {"<= | >= | = | <>": "Dead", "[0-9]": "q3", "Dot(.)": "q6", "Space": "q4"},
        "q4": {"<= | >= | = | <>": "Dead", "[0-9]": "q5", "Dot(.)": "Dead", "Space": "q4"},
        "q5": {"<= | >= | = | <>": "Dead", "[0-9]": "q5", "Dot(.)": "Dead", "Space": "q5"},
        "q6": {"<= | >= | = | <>": "Dead", "[0-9]": "q3", "Dot(.)": "Dead", "Space": "q6"},
        "Dead": {"<= | >= | = | <>": "Dead", "[0-9]": "Dead", "Dot(.)": "Dead", "Space": "Dead"},

    },
    initial_state="q0",
    final_states={"q5"}

)

arithmeticOperatorsDFA = VisualDFA(
    states={"q0", "q1", "q2", "q3", "q4", "q5", "q6", "Dead"},
    input_symbols={"+ | - | * | / | mod | rem | incf | decf", "[0-9]", "Dot(.)", "Space"},
    transitions={
        "q0": {"+ | - | * | / | mod | rem | incf | decf": "q1", "[0-9]": "Dead", "Dot(.)": "Dead", "Space": "Dead"},
        "q1": {"+ | - | * | / | mod | rem | incf | decf": "Dead", "[0-9]": "Dead", "Dot(.)": "Dead", "Space": "q2"},
        "q2": {"+ | - | * | / | mod | rem | incf | decf": "Dead", "[0-9]": "q3", "Dot(.)": "Dead", "Space": "q2"},
        "q3": {"+ | - | * | / | mod | rem | incf | decf": "Dead", "[0-9]": "q3", "Dot(.)": "q6", "Space": "q4"},
        "q4": {"+ | - | * | / | mod | rem | incf | decf": "Dead", "[0-9]": "q5", "Dot(.)": "Dead", "Space": "q4"},
        "q5": {"+ | - | * | / | mod | rem | incf | decf": "Dead", "[0-9]": "q5", "Dot(.)": "Dead", "Space": "q5"},
        "q6": {"+ | - | * | / | mod | rem | incf | decf": "Dead", "[0-9]": "q3", "Dot(.)": "Dead", "Space": "q6"},
        "Dead": {"+ | - | * | / | mod | rem | incf | decf": "Dead", "[0-9]": "Dead", "Dot(.)": "Dead", "Space": "Dead"},

    },
    initial_state="q0",
    final_states={"q5"}

)

identifiersDFA = VisualDFA(
    states={"q0", "q1", "q2", "Dead"},
    input_symbols={"[a-z]", "[A-Z]", "$ | ! | % | & | * | / | : | < | = | > | ? | _ | ^ | ~", "[0-9]", "Space"},
    transitions={
        "q0": {"[a-z]": "q1", "[A-Z]": "q1", "$ | ! | % | & | * | / | : | < | = | > | ? | _ | ^ | ~": "q1",
               "[0-9]": "q1", "Space": "q1"},
        "q1": {"[a-z]": "q1", "[A-Z]": "q1", "$ | ! | % | & | * | / | : | < | = | > | ? | _ | ^ | ~": "q1",
               "[0-9]": "q1", "Space": "q2"},
        "q2": {"[a-z]": "Dead", "[A-Z]": "Dead", "$ | ! | % | & | * | / | : | < | = | > | ? | _ | ^ | ~": "Dead",
               "[0-9]": "Dead", "Space": "q2"},
        "Dead": {"[a-z]": "Dead", "[A-Z]": "Dead", "$ | ! | % | & | * | / | : | < | = | > | ? | _ | ^ | ~": "Dead",
                 "[0-9]": "Dead", "Space": "Dead"}

    },
    initial_state="q0",
    final_states={"q1", "q2"}
)

semiStandardCharactersDFA = VisualDFA(
    states={"q0", "q1", "q2", "q3", "Dead"},
    input_symbols={"#", "\\\\", "space", "Backspace | Tab | Linefeed | Page | Return | Rubout"},
    transitions={
        "q0": {"#": "q1", "\\\\": "Dead", "space": "q0", "Backspace | Tab | Linefeed | Page | Return | Rubout": "Dead"},
        "q1": {"#": "Dead", "\\\\": "q2", "space": "Dead",
               "Backspace | Tab | Linefeed | Page | Return | Rubout": "Dead"},
        "q2": {"#": "Dead", "\\\\": "q2", "space": "Dead",
               "Backspace | Tab | Linefeed | Page | Return | Rubout": "q3"},
        "q3": {"#": "Dead", "\\\\": "Dead", "space": "Dead",
               "Backspace | Tab | Linefeed | Page | Return | Rubout": "Dead"},
        "Dead": {"#": "Dead", "\\\\": "Dead", "space": "Dead",
                 "Backspace | Tab | Linefeed | Page | Return | Rubout": "Dead"},

    },
    initial_state="q0",
    final_states={"q3"}
)

charactersDFA = VisualDFA(
    states={"q0", "q1", "q2", "q3", "Dead"},
    input_symbols={"#", "\\\\", "Anything except \\\\", "Anything except #", "Anything"},
    transitions={
        "q0": {"#": "q1", "\\\\": "Dead", "Anything except \\\\": "Dead", "Anything except #": "Dead",
               "Anything": "Dead"},
        "q1": {"#": "Dead", "\\\\": "q2", "Anything except \\\\": "Dead", "Anything except #": "Dead",
               "Anything": "Dead"},
        "q2": {"#": "q3", "\\\\": "q3", "Anything except \\\\": "q3", "Anything except #": "q3", "Anything": "q3"},
        "q3": {"#": "Dead", "\\\\": "Dead", "Anything except \\\\": "Dead", "Anything except #": "Dead",
               "Anything": "Dead"},
        "Dead": {"#": "q1", "\\\\": "Dead", "Anything except \\\\": "Dead", "Anything except #": "Dead",
                 "Anything": "Dead"},

    },
    initial_state="q0",
    final_states={"q3"}
)

commentsDFA.show_diagram(input_str="", path="Test-DFAs", filename='commentsDFA', format_type="png", view=False)
stringDFA.show_diagram(input_str="", path="Test-DFAs", filename="stringsDFA", format_type="png", view=False)
numbersDFA.show_diagram(input_str="", path="Test-DFAs", filename="numbersDFA", format_type="svg", view=False)
relationalOperatorsDFA.show_diagram(input_str="", path="Test-DFAs", filename="relationalOperatorsDFA",
                                    format_type="png", view=False)
arithmeticOperatorsDFA.show_diagram(input_str="", path="Test-DFAs", filename="arithmeticOperatorsDFA",
                                    format_type="png", view=False)
identifiersDFA.show_diagram(input_str="", path="Test-DFAs", filename="identifiersDFA",
                            format_type="png", view=False)
semiStandardCharactersDFA.show_diagram(input_str="", path="Test-DFAs", filename="semiStandardCharactersDFA",
                                       format_type="png", view=False)
charactersDFA.show_diagram(input_str="", path="Test-DFAs", filename="charactersDFA",
                                       format_type="svg", view=False)
