matrix
======

Pythonic 2D matrix data type. This is a generic data structure with all the operations you would expect:

    m = Matrix(2, 3) # 2 rows, 3 columns, filled with None.
    m = Matrix([[1, 2, 3], [4, 5, 6]]) # Exactly what you expect.
    
    # Access with (row, col) indices.
    m[0,1] # Element at row 0, column 1.
    m[-1,-1] # Element at last row, last column.
    m[(0,1):(2,3)] # Two dimensional slice returns a new Matrix.
    
    # Or by absolute elements, like a list.
    m[5] # Element at index 5, regardless of rows and columns.
    m[2:] # From the element 2 until the end.
    
    7 in m # Searches for elements.
    
    # You can also set values using the techniques above:
    m[1:-1] = list(m[:(2,2)]) # I have no idea what this means, but it works!
    
    # Helper methods are also provided:
    m.addcol(2, [7, 8]) # Adds column at index 2, filling with elements 7 and 8.
    m.addrow(0) # Adds a new first row, with None values.
    m.removerow(0) # Removes the row we added.
    
    m.map(lambda x: x**2) # Returns matrix with squared elements.
    
    # 1 2 7 4
    # 5 5 8 6
    print(m)

This is a simple data structure. It's not supposed to hold large amounts of data or be used in linear math.
