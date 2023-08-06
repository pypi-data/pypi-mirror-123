def transform_sqlstring_to_vector(ls):
    return '( '+ ','.join(list(map(lambda x: "'"+x+"'",ls))) + ')'