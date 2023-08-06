import autoarray as aa


class FitGalaxy(aa.FitDataset):
    def __init__(self, masked_galaxy_dataset, model_galaxies):
        """Class which fits a set of galaxy-datas to a model galaxy, using either the galaxy's image, \
        surface-density or potential.

        Parameters
        ----------
        masked_galaxy_dataset : GalaxyData
            The galaxy-datas object being fitted.
        model_galaxies : ag.Galaxy
            The model galaxy used to fit the galaxy-datas.
        """
        self.model_galaxies = model_galaxies

        model_data = masked_galaxy_dataset.profile_quantity_from(
            galaxies=model_galaxies
        )

        fit = aa.FitData(
            data=masked_galaxy_dataset.image,
            noise_map=masked_galaxy_dataset.noise_map,
            model_data=model_data.binned,
            mask=masked_galaxy_dataset.mask,
            use_mask_in_fit=False,
        )

        super().__init__(dataset=masked_galaxy_dataset, fit=fit)

    @property
    def masked_galaxy_dataset(self):
        return self.dataset

    @property
    def grid(self):
        return self.masked_galaxy_dataset.grid

    def image(self):
        return self.data

    def model_image(self):
        return self.model_data
