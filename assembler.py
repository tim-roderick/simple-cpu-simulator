def assemble(file):
    instructions = [line.rstrip('\n') for line in open(file)]
    instructions = list(filter(None, instructions))
    instructions = list(filter(lambda line: not line.startswith(";"), instructions))
    labels = list(filter(lambda line: line.startswith("-"), instructions))
    for instr in instructions:
        for label in labels:
            if label == instr:
                labels[labels.index(label)] = [str(label), instructions.index(instr)]
                instructions.remove(instr)

    for instr in instructions:
        for label in labels:
            if label[0] in instr:
                instructions[instructions.index(instr)] = instr.replace(label[0], str(label[1]))

    return instructions, labels
