from src.controller.ErlekamController import ErlekamController

norm_to_beat = ErlekamController.process_tri_tetra_wiseman()
ErlekamController.process_tri_tetra_q_c(norm_to_beat)

norm_to_beat = ErlekamController.process_deca_bi_wiseman()
ErlekamController.process_deca_bi_q_c(norm_to_beat)
