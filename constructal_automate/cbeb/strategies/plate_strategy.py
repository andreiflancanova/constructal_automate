from abc import ABC, abstractmethod

class PlateStrategy(ABC):

    @abstractmethod
    def define_element_type_section_and_material(self, mapdl, E, poisson_ratio, t_1, t_s):
        pass

    @abstractmethod
    def define_geometry(self, mapdl, a, b, t_1, N_ts, N_ls, h_s):
        pass

    @abstractmethod
    def define_discretization(self, mapdl, mesh_size, stiffened_plate_analysis):
        pass

    @abstractmethod
    def define_components_and_apply_boundary_conditions(self, mapdl, a, b, t_1):
        pass

    @abstractmethod
    def apply_load_for_elastic_buckling(self, mapdl, buckling_load_type):
        pass

    @abstractmethod
    def apply_load_for_elasto_plastic_buckling(self, mapdl, buckling_load_type, material, t_1):
    # def apply_load_for_elasto_plastic_buckling(self, mapdl, buckling_load_type, material, t_eq_ts, t_eq_ls):
        pass