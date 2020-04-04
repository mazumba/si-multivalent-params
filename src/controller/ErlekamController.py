from src.controller.AbstractController import AbstractController
from src.service import Manager, QService
from src.service.initializer.InitializeFactory import InitializeFactory
import src.importer.ImporterMediator as Importer


class ErlekamController(AbstractController):
    @staticmethod
    def process_tri_tetra_wiseman() -> float:
        dirname = 'tri_tetra'
        return AbstractController.__process_wiseman__(dirname, Importer.__extract_man1355llbb25__(),
                                                      InitializeFactory.initialize_wiseman_by(dirname), 0.3)

    @staticmethod
    def process_tri_tetra_q_c(norm_to_beat: float):
        dirname = 'tri_tetra'
        try:
            params = Manager.load_q_c_ini(dirname)
        except IOError:
            params = InitializeFactory.initialize_qc_by(dirname)
        AbstractController.__process_qc__(dirname, Importer.__extract_man1355llbb25__(), params,
                                          QService.const_trival, norm_to_beat, 0.3)

    @staticmethod
    def process_deca_bi_wiseman() -> float:
        dirname = 'deca_bi'
        return AbstractController.__process_wiseman__(dirname, Importer.__extract_man1010lacetate2__(),
                                                      InitializeFactory.initialize_wiseman_by(dirname), 0.2)

    @staticmethod
    def process_deca_bi_q_c(norm_to_beat: float):
        dirname = 'deca_bi'
        try:
            params = Manager.load_q_c_ini(dirname)
        except IOError:
            params = InitializeFactory.initialize_qc_by(dirname)
        AbstractController.__process_qc__(dirname, Importer.__extract_man1010lacetate2__(), params,
                                          QService.const_bval, norm_to_beat, 0.2)
