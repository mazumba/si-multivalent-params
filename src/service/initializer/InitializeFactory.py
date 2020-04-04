from src.service.initializer.Initialize import Initialize


class InitializeFactory(Initialize):
    tri_tetra = 'tri_tetra'
    deca_bi = 'deca_bi'

    @staticmethod
    def initialize_wiseman_by(dirname):
        if dirname == InitializeFactory.tri_tetra:
            return Initialize.init_wiseman_man1355llbb25(dirname)
        if dirname == InitializeFactory.deca_bi:
            return Initialize.init_wiseman_man1010lacetate2(dirname)
        raise FileNotFoundError(f'The wiseman fitting directory "{dirname}" could not be initialized.')

    @staticmethod
    def initialize_qc_by(dirname):
        if dirname == InitializeFactory.tri_tetra:
            return Initialize.init_qc_man1355llbb25(dirname)
        if dirname == InitializeFactory.deca_bi:
            return Initialize.init_qc_man1010lacetate2(dirname)
        raise FileNotFoundError(f'The qc fitting directory "{dirname}" could not be initialized.')
