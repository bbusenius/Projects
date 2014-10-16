

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Creates a scoring matrix. Dashes '-' are hardcoded in.
    Returns a dictionary of dictionaries whose entries are indexed 
    by pairs of characters in alphabet plus '-'.
    """
    test = {}
    for row in alphabet:
        row_dict = {}
        for col in alphabet:
            
            if row == '-':
                row_dict[col] = dash_score
            elif row == col and col != '-':
                row_dict[col] = diag_score
            elif col in alphabet and col != '-':
                row_dict[col] = off_diag_score
            else: 
                row_dict[col] = dash_score
        test[row] = row_dict

    return test


print build_scoring_matrix(set(['A', 'C', '-', 'T', 'G']), 6, 2, -4)

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Ugh...
    """
    pass 
