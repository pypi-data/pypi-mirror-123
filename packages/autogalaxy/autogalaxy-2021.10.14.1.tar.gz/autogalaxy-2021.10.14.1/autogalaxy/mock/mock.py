from astropy import constants
import math

import autofit as af
import autoarray as aa
import autogalaxy as ag
from autoarray.mock.mock import *
from autofit.mock.mock import MockSearch, MockSamples

# MockProfiles #


class MockLightProfile(ag.lp.LightProfile):
    def __init__(self, image_2d=None, value=None, value1=None):

        super().__init__()

        self.image_2d = image_2d
        self.value = value
        self.value1 = value1

    def image_2d_from(self, grid):
        return self.image_2d


class MockMassProfile(ag.mp.MassProfile):
    def __init__(self, value, value1=None):

        self.value = value
        self.value1 = value1

    def convergence_from(self, grid):
        return np.array([self.value])

    def potential_2d_from(self, grid):
        return np.array([self.value])

    def deflections_2d_from(self, grid):
        return np.array([self.value, self.value])


# Mock Galaxy #


class MockGalaxy:
    def __init__(self, value, shape=1):
        self.value = value
        self.shape = shape

    @aa.grid_dec.grid_2d_to_structure
    def image_2d_from(self, grid):
        return np.full(shape=self.shape, fill_value=self.value)

    @aa.grid_dec.grid_2d_to_structure
    def convergence_2d_from(self, grid):
        return np.full(shape=self.shape, fill_value=self.value)

    @aa.grid_dec.grid_2d_to_structure
    def potential_2d_from(self, grid):
        return np.full(shape=self.shape, fill_value=self.value)

    @aa.grid_dec.grid_2d_to_structure
    def deflections_2d_from(self, grid):
        return np.full(shape=(self.shape, 2), fill_value=self.value)


# Mock Cosmology #


class Value:
    def __init__(self, value):
        self.value = value

    def to(self, *args, **kwargs):
        return Value(value=self.value)


class MockCosmology:
    def __init__(
        self,
        arcsec_per_kpc=0.5,
        kpc_per_arcsec=2.0,
        critical_surface_density=2.0,
        cosmic_average_density=2.0,
    ):
        self.arcsec_per_kpc = arcsec_per_kpc
        self.kpc_per_arcsec = kpc_per_arcsec
        self.critical_surface_density = critical_surface_density
        self.cosmic_average_density = cosmic_average_density

    def arcsec_per_kpc_proper(self, z):
        return Value(value=self.arcsec_per_kpc)

    def kpc_per_arcsec_proper(self, z):
        return Value(value=self.kpc_per_arcsec)

    def angular_diameter_distance(self, z):
        return Value(value=1.0)

    def angular_diameter_distance_z1z2(self, z1, z2):
        const = constants.c.to("kpc / s") ** 2.0 / (
            4 * math.pi * constants.G.to("kpc3 / (solMass s2)")
        )
        return Value(value=self.critical_surface_density * const.value)

    def critical_density(self, z):
        return Value(value=self.cosmic_average_density)


# Mock Model-Fitting #


class MockResult(af.MockResult):
    def __init__(
        self,
        samples=None,
        instance=None,
        model=None,
        analysis=None,
        search=None,
        mask=None,
        model_image=None,
        path_galaxy_tuples=None,
        hyper_galaxy_image_path_dict=None,
        hyper_model_image=None,
        hyper_galaxy_visibilities_path_dict=None,
        hyper_model_visibilities=None,
        pixelization=None,
    ):
        super().__init__(
            samples=samples,
            instance=instance,
            model=model,
            analysis=analysis,
            search=search,
        )

        self.mask = mask
        self.hyper_galaxy_image_path_dict = hyper_galaxy_image_path_dict
        self.hyper_model_image = hyper_model_image
        self.path_galaxy_tuples = path_galaxy_tuples
        self.hyper_galaxy_visibilities_path_dict = hyper_galaxy_visibilities_path_dict
        self.hyper_model_visibilities = hyper_model_visibilities
        self.model_image = model_image
        self.unmasked_model_image = model_image
        self.pixelization = pixelization

        self.max_log_likelihood_plane = ag.Plane(galaxies=[ag.Galaxy(redshift=0.5)])

    @property
    def last(self):
        return self


class MockResults(af.ResultsCollection):
    def __init__(
        self,
        samples=None,
        instance=None,
        model=None,
        analysis=None,
        search=None,
        mask=None,
        model_image=None,
        hyper_galaxy_image_path_dict=None,
        hyper_model_image=None,
        hyper_galaxy_visibilities_path_dict=None,
        hyper_model_visibilities=None,
        pixelization=None,
    ):
        """
        A collection of results from previous searchs. Results can be obtained using an index or the name of the search
        from whence they came.
        """

        super().__init__()

        result = MockResult(
            samples=samples,
            instance=instance,
            model=model,
            analysis=analysis,
            search=search,
            mask=mask,
            model_image=model_image,
            hyper_galaxy_image_path_dict=hyper_galaxy_image_path_dict,
            hyper_model_image=hyper_model_image,
            hyper_galaxy_visibilities_path_dict=hyper_galaxy_visibilities_path_dict,
            hyper_model_visibilities=hyper_model_visibilities,
            pixelization=pixelization,
        )

        self.__result_list = [result]

    @property
    def last(self):
        """
        The result of the last search
        """
        if len(self.__result_list) > 0:
            return self.__result_list[-1]
        return None

    def __getitem__(self, item):
        """
        Get the result of a previous search by index

        Parameters
        ----------
        item: int
            The index of the result

        Returns
        -------
        result: Result
            The result of a previous search
        """
        return self.__result_list[item]

    def __len__(self):
        return len(self.__result_list)
