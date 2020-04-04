import src.service.Manager as Manager
from src.service.initializer.InitializeFactory import InitializeFactory
from src.service.Processor import QcProcessor, WisemanProcessor
from src.entity.ResultCollection import QcResultCollection
from src.entity.ExtractCollection import ExtractCollection
from src.Exceptions import ComplexError, NegativeValueError, NormValueTooLargeError
from src.service.Wiseman import Wiseman
from src.entity.Parameters import WisemanParameters, QcParameters
import numpy as np


class AbstractController:
    def __init__(self):
        pass

    @staticmethod
    def __get_gaus_pos__(dirname: str):
        if 'tri_tetra' == dirname:
            return 0.3
        if 'deca_bi' == dirname:
            return 0.2

    @staticmethod
    def __process_qc__(dirname: str, extract_collection: ExtractCollection, params: QcParameters, matrix_key: str,
                       norm_to_beat: float, gauss_pos: float):
        try:
            params = Manager.load_q_c_ini(dirname)
        except IOError:
            pass
        processor = QcProcessor(extract_collection, gauss_pos, matrix_key,
                                QcResultCollection(len(extract_collection.heat_per_injection)), norm_to_beat)
        plots_count = 0
        better_plots_count = 0
        norm = 0
        better_params = params
        max_tries = 100000
        for plots in range(0, max_tries):
            try:
                new_n, new_deltah = processor.optimize_n_and_deltah(params.n, params.delta_h, params.k)
                params.n = new_n
                params.delta_h = new_deltah
                result_collection = processor.get_result()

                qc_wiseman = Wiseman(extract_collection, result_collection.k_a, params.n, params.delta_h)
                new_norm = processor.calculate_norm(extract_collection.heat_per_injection, qc_wiseman.get_graph())
                if 0 == norm:
                    norm = new_norm
                    print(f'Initial norm: {norm}')
                    better_params.print()
                if new_norm < norm:
                    norm = new_norm
                    better_params = params
                    better_plots_count = better_plots_count + 1
                    print(f'Found a better one.\n         Current norm: {norm}')
                    print(f'         Current iteration: {plots_count + 1} of {plots}')
                    better_params.print()
                    Manager.save_q_c_params(better_params)
                    if new_norm < norm_to_beat:
                        print('you did it.')
                        break
                plots_count = plots_count + 1
            except ComplexError:
                continue
            except np.linalg.LinAlgError:
                continue
            except NegativeValueError:
                continue
            except NormValueTooLargeError:
                continue
            finally:
                params = InitializeFactory.initialize_qc_by(dirname)
        print(f'valid plots: {plots_count + 1}')
        print(f'better plots: {better_plots_count}')
        print(f'best norm: {norm}')
        better_params.print()

    @staticmethod
    def __process_wiseman__(dirname: str, extract_collection: ExtractCollection, params: WisemanParameters,
                            gauss_pos: float) -> float:
        try:
            params = Manager.load_wiseman_ini(dirname)
            wiseman = Wiseman(extract_collection, params.k, params.n, params.delta_h)
            processor = WisemanProcessor(extract_collection, gauss_pos, wiseman)
            norm = processor.calculate_norm(wiseman.heat_per_inj, wiseman.get_graph())
            print(f'Optimization from file.\n         Current gaussian norm: {norm}')
        except IOError:
            # use given params if not already saved
            wiseman = Wiseman(extract_collection, params.k, params.n, params.delta_h)
            processor = WisemanProcessor(extract_collection, params.n, wiseman)
            processor.fit_to_heat_per_inj()
            better_params = WisemanParameters(wiseman.k, wiseman.n, wiseman.delta_h, dirname)
            Manager.save_wiseman_params(better_params)
            params = better_params
        params.print()
        wiseman_graph = wiseman.get_graph()
        norm = processor.calculate_norm(wiseman.heat_per_inj, wiseman_graph)
        return norm
