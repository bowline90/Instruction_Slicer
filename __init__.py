import binaryninja as bn
import Queue 
def slicer(bv, address,direction):
    colorize = []
    colorize.append(address)
    function = bv.get_functions_containing(address)[0]

    ml = function.mlil
    instr = ml[ml.get_instruction_start(address)].ssa_form
    if direction == 'F':
    ### Forward
        var_s = instr.vars_written
        q = Queue.Queue()
        for i in var_s:
            q.put(i)
    ## Also multithreading
        while not q.empty():
            var = q.get()
            temp = ml.get_ssa_var_uses(var)
            for i in temp:
                colorize.append(i.address)
                data = i.ssa_form.vars_written
                for j in data:
                    q.put(j)
    elif direction == 'B':
        var_s = instr.vars_read
        q = Queue.Queue()
        for i in var_s:
            q.put(i)
        while not q.empty():
            var = q.get()
            temp = ml.get_ssa_var_definition(var)
            if temp != None:
                colorize.append(temp.address)
                data = temp.ssa_form.vars_read
                for j in data:
                    q.put(j)
    ##COMPLETED
    bv.begin_undo_actions()
    for i in colorize:
        function.set_user_instr_highlight(i,bn.HighlightStandardColor.BlueHighlightColor)
    bv.commit_undo_actions()
def slicing_back(bv,address):
    slicer(bv,address,'B')
def slicing_forward(bv,address):
    slicer(bv,address,'F')
bn.PluginCommand.register_for_address("Backward slicing", "Perform a backward slicing for this instruction", slicing_back)
bn.PluginCommand.register_for_address("Forward slicing", "Perform a forward slicing for this instruction", slicing_forward)
