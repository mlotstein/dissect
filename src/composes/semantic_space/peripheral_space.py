'''
Created on Sep 26, 2012

@author: georgianadinu
'''

from space import Space
from composes.utils.space_utils import list2dict
from composes.utils.space_utils import assert_dict_match_list
from composes.utils.space_utils import assert_shape_consistent
from composes.utils.space_utils import add_items_to_dict

class PeripheralSpace(Space):
    '''
    classdocs
    '''


    def __init__(self, core_space, matrix_, id2row, row2id=None):
        '''
        Constructor
        '''
        if row2id is None:
            row2id = list2dict(id2row)
        else:
            assert_dict_match_list(row2id, id2row)    
            
        column2id = core_space.column2id
        id2column = core_space.id2column
            
        self._operations = list(core_space.operations)    
        self._cooccurrence_matrix = self._project_core_operations(matrix_)
        
        assert_shape_consistent(self.cooccurrence_matrix, id2row, id2column, 
                                     row2id, column2id)
        
        self._row2id = row2id
        self._id2row = id2row
        self._column2id = column2id
        self._id2column = id2column

                
    def _project_core_operations(self, matrix_):
       
        for operation in self._operations:
            matrix_ = operation.project(matrix_)
        return matrix_
        
         
    def add_rows(self, matrix_, id2row):
        
        try:
            self._row2id = add_items_to_dict(self.row2id, id2row)
        except ValueError:
            raise ValueError("Found duplicate keys when appending rows to\
                            peripheral space.")
        
        if matrix_.mat.shape[0] != len(id2row):
            raise ValueError("Matrix shape inconsistent with no. of rows:%s %s"
                              % (matrix_.mat.shape, len(id2row)))
       
        self._id2row = self.id2row + id2row
        matrix_ = self._project_core_operations(matrix_)

        #TODO self._cooccurrence_matrix = self._cooccurrence_matrix.vstack(matrix_)
        #TODO assert_shape_consistent(self.cooccurrence_matrix, self.id2row,
        #                         self.id2column, row2id, column2id)        
        
        
        
        
        
        