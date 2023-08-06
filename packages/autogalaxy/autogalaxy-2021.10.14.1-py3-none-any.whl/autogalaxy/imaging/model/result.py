from autogalaxy.analysis.result import ResultDataset


class ResultImaging(ResultDataset):
    @property
    def max_log_likelihood_fit(self):

        hyper_image_sky = self.analysis.hyper_image_sky_for_instance(
            instance=self.instance
        )

        hyper_background_noise = self.analysis.hyper_background_noise_for_instance(
            instance=self.instance
        )

        return self.analysis.fit_imaging_for_plane(
            plane=self.max_log_likelihood_plane,
            hyper_image_sky=hyper_image_sky,
            hyper_background_noise=hyper_background_noise,
        )

    @property
    def unmasked_model_image(self):
        return self.max_log_likelihood_fit.unmasked_blurred_image

    @property
    def unmasked_model_image_of_galaxies(self):
        return self.max_log_likelihood_fit.unmasked_blurred_image_of_galaxies
