import numpy as np
import pytest

import autogalaxy as ag

grid = np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [2.0, 4.0]])


class TestEllGaussian:
    def test__deflections_correct_values(self):

        gaussian = ag.mp.EllGaussian(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.05263),
            intensity=1.0,
            sigma=3.0,
            mass_to_light_ratio=1.0,
        )

        deflections = gaussian.deflections_2d_from(grid=np.array([[1.0, 0.0]]))

        assert deflections[0, 0] == pytest.approx(1.024423, 1.0e-4)
        assert deflections[0, 1] == pytest.approx(0.0, 1.0e-4)

        gaussian = ag.mp.EllGaussian(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.111111),
            intensity=1.0,
            sigma=5.0,
            mass_to_light_ratio=1.0,
        )

        deflections = gaussian.deflections_2d_from(grid=np.array([[0.5, 0.2]]))

        assert deflections[0, 0] == pytest.approx(0.554062, 1.0e-4)
        assert deflections[0, 1] == pytest.approx(0.177336, 1.0e-4)

        gaussian = ag.mp.EllGaussian(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.111111),
            intensity=1.0,
            sigma=5.0,
            mass_to_light_ratio=2.0,
        )

        deflections = gaussian.deflections_2d_from(grid=np.array([[0.5, 0.2]]))

        assert deflections[0, 0] == pytest.approx(1.108125, 1.0e-4)
        assert deflections[0, 1] == pytest.approx(0.35467, 1.0e-4)

        gaussian = ag.mp.EllGaussian(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.111111),
            intensity=2.0,
            sigma=5.0,
            mass_to_light_ratio=1.0,
        )

        deflections = gaussian.deflections_2d_from(grid=np.array([[0.5, 0.2]]))

        assert deflections[0, 0] == pytest.approx(1.10812, 1.0e-4)
        assert deflections[0, 1] == pytest.approx(0.35467, 1.0e-4)

    def test__deflections_via_integrator_and_analytic_agree(self):

        gaussian = ag.mp.EllGaussian(
            centre=(0.4, 0.2),
            elliptical_comps=(0.0, 0.17647),
            intensity=1.0,
            sigma=10.0,
            mass_to_light_ratio=1.0,
        )

        grid = ag.Grid2D.uniform(
            shape_native=(3, 3), pixel_scales=0.1, origin=(1.0, 1.0)
        )

        deflections_via_analytic = gaussian.deflections_2d_from(grid=grid)
        deflections_via_integrator = gaussian.deflections_2d_via_integrator_from(
            grid=grid
        )

        assert deflections_via_analytic == pytest.approx(
            deflections_via_integrator, 1.0e-2
        )

        gaussian = ag.mp.EllGaussian(
            centre=(-0.7, -0.4),
            elliptical_comps=(0.0, 0.05263),
            intensity=3.0,
            sigma=15.0,
            mass_to_light_ratio=7.0,
        )

        grid = ag.Grid2D.uniform(
            shape_native=(3, 3), pixel_scales=0.1, origin=(1.0, 1.0)
        )

        deflections_via_analytic = gaussian.deflections_2d_from(grid=grid)
        deflections_via_integrator = gaussian.deflections_2d_via_integrator_from(
            grid=grid
        )

        assert deflections_via_analytic == pytest.approx(
            deflections_via_integrator, 1.0e-2
        )

    def test__intensity_and_convergence_match_for_mass_light_ratio_1(self):

        gaussian_light_profile = ag.lp.EllGaussian(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.333333),
            intensity=2.0,
            sigma=3.0,
        )

        gaussian_mass_profile = ag.mp.EllGaussian(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.333333),
            intensity=2.0,
            sigma=3.0,
            mass_to_light_ratio=1.0,
        )

        intensity = gaussian_light_profile.image_2d_from(grid=np.array([[1.0, 0.0]]))
        convergence = gaussian_mass_profile.convergence_2d_from(
            grid=np.array([[1.0, 0.0]])
        )

        print(intensity, convergence)

        assert (intensity == convergence).all()

    def test__image_2d_via_radii_from__correct_value(self):
        gaussian = ag.mp.EllGaussian(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.0), intensity=1.0, sigma=1.0
        )

        intensity = gaussian.image_2d_via_radii_from(grid_radii=1.0)

        assert intensity == pytest.approx(0.60653, 1e-2)

        gaussian = ag.mp.EllGaussian(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.0), intensity=2.0, sigma=1.0
        )

        intensity = gaussian.image_2d_via_radii_from(grid_radii=1.0)

        assert intensity == pytest.approx(2.0 * 0.60653, 1e-2)

        gaussian = ag.mp.EllGaussian(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.0), intensity=1.0, sigma=2.0
        )

        intensity = gaussian.image_2d_via_radii_from(grid_radii=1.0)

        assert intensity == pytest.approx(0.882496, 1e-2)

        gaussian = ag.mp.EllGaussian(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.0), intensity=1.0, sigma=2.0
        )

        intensity = gaussian.image_2d_via_radii_from(grid_radii=3.0)

        assert intensity == pytest.approx(0.32465, 1e-2)

    def test__convergence_2d_from__correct_value(self):
        gaussian = ag.mp.EllGaussian(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.0),
            intensity=1.0,
            sigma=1.0,
            mass_to_light_ratio=1.0,
        )

        convergence = gaussian.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(0.60653, 1e-2)

        gaussian = ag.mp.EllGaussian(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.0),
            intensity=1.0,
            sigma=1.0,
            mass_to_light_ratio=2.0,
        )

        convergence = gaussian.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(2.0 * 0.60653, 1e-2)

        gaussian = ag.mp.EllGaussian(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.333333),
            intensity=2.0,
            sigma=3.0,
            mass_to_light_ratio=4.0,
        )

        convergence = gaussian.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(7.88965, 1e-2)


class TestSersic:
    def test__convergence_correct_values(self):

        sersic = ag.mp.EllSersic(
            centre=(0.0, 0.0),
            intensity=3.0,
            effective_radius=2.0,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
        )

        convergence = sersic.convergence_2d_from(grid=np.array([[0.0, 1.5]]))

        assert convergence == pytest.approx(4.90657319276, 1e-3)

        sersic = ag.mp.EllSersic(
            centre=(0.0, 0.0),
            intensity=6.0,
            effective_radius=2.0,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
        )

        convergence = sersic.convergence_2d_from(grid=np.array([[0.0, 1.5]]))

        assert convergence == pytest.approx(2.0 * 4.90657319276, 1e-3)

        sersic = ag.mp.EllSersic(
            centre=(0.0, 0.0),
            intensity=3.0,
            effective_radius=2.0,
            sersic_index=2.0,
            mass_to_light_ratio=2.0,
        )

        convergence = sersic.convergence_2d_from(grid=np.array([[0.0, 1.5]]))

        assert convergence == pytest.approx(2.0 * 4.90657319276, 1e-3)

        sersic = ag.mp.EllSersic(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.333333),
            intensity=3.0,
            effective_radius=2.0,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
        )

        convergence = sersic.convergence_2d_from(grid=np.array([[1.0, 0.0]]))

        assert convergence == pytest.approx(5.38066670129, 1e-3)

    def test__convergence_2d_from_gaussians__correct_values(self):
        sersic = ag.mp.EllSersic(
            centre=(0.0, 0.0),
            intensity=3.0,
            effective_radius=2.0,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
        )

        convergence = sersic.convergence_2d_via_gaussians_from(
            grid=np.array([[0.0, 1.5]])
        )

        assert convergence == pytest.approx(4.90657319276, 1e-3)

        sersic = ag.mp.EllSersic(
            centre=(0.0, 0.0),
            intensity=6.0,
            effective_radius=2.0,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
        )

        convergence = sersic.convergence_2d_via_gaussians_from(
            grid=np.array([[0.0, 1.5]])
        )

        assert convergence == pytest.approx(2.0 * 4.90657319276, 1e-3)

        sersic = ag.mp.EllSersic(
            centre=(0.0, 0.0),
            intensity=3.0,
            effective_radius=2.0,
            sersic_index=2.0,
            mass_to_light_ratio=2.0,
        )

        convergence = sersic.convergence_2d_via_gaussians_from(
            grid=np.array([[0.0, 1.5]])
        )

        assert convergence == pytest.approx(2.0 * 4.90657319276, 1e-3)

        sersic = ag.mp.EllSersic(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.333333),
            intensity=3.0,
            effective_radius=2.0,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
        )

        convergence = sersic.convergence_2d_via_gaussians_from(
            grid=np.array([[1.0, 0.0]])
        )

        assert convergence == pytest.approx(5.38066670129, 1e-3)

    def test__deflections_via_integrator__correct_values(self):
        sersic = ag.mp.EllSersic(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=5.0,
            effective_radius=0.2,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
        )

        deflections = sersic.deflections_2d_via_integrator_from(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(1.1446, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.79374, 1e-3)

        sersic = ag.mp.EllSersic(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=5.0,
            effective_radius=0.2,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
        )

        deflections = sersic.deflections_2d_via_integrator_from(
            grid=ag.Grid2DIrregular([(0.1625, 0.1625), (0.1625, 0.1625)])
        )

        assert deflections[0, 0] == pytest.approx(1.1446, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.79374, 1e-3)
        assert deflections[1, 0] == pytest.approx(1.1446, 1e-3)
        assert deflections[1, 1] == pytest.approx(0.79374, 1e-3)

    def test__deflections_2d_from_close_to_integrator__correct_values(self):

        sersic = ag.mp.EllSersic(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=5.0,
            effective_radius=0.2,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
        )

        deflections = sersic.deflections_2d_from(grid=np.array([[0.1625, 0.1625]]))

        assert deflections[0, 0] == pytest.approx(1.1446, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.79374, 1e-3)

        sersic = ag.mp.EllSersic(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=5.0,
            effective_radius=0.2,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
        )

        deflections = sersic.deflections_2d_from(
            grid=ag.Grid2DIrregular([(0.1625, 0.1625), (0.1625, 0.1625)])
        )

        assert deflections[0, 0] == pytest.approx(1.1446, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.79374, 1e-3)
        assert deflections[1, 0] == pytest.approx(1.1446, 1e-3)
        assert deflections[1, 1] == pytest.approx(0.79374, 1e-3)

        sersic = ag.mp.EllSersic(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=10.0,
            effective_radius=0.2,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
        )

        deflections = sersic.deflections_2d_from(
            grid=ag.Grid2DIrregular([(0.1625, 0.1625), (0.1625, 0.1625)])
        )

        assert deflections[0, 0] == pytest.approx(2.0 * 1.1446, 1e-3)
        assert deflections[0, 1] == pytest.approx(2.0 * 0.79374, 1e-3)
        assert deflections[1, 0] == pytest.approx(2.0 * 1.1446, 1e-3)
        assert deflections[1, 1] == pytest.approx(2.0 * 0.79374, 1e-3)

        sersic = ag.mp.EllSersic(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=5.0,
            effective_radius=0.2,
            sersic_index=2.0,
            mass_to_light_ratio=2.0,
        )

        deflections = sersic.deflections_2d_from(
            grid=ag.Grid2DIrregular([(0.1625, 0.1625), (0.1625, 0.1625)])
        )

        assert deflections[0, 0] == pytest.approx(2.0 * 1.1446, 1e-3)
        assert deflections[0, 1] == pytest.approx(2.0 * 0.79374, 1e-3)
        assert deflections[1, 0] == pytest.approx(2.0 * 1.1446, 1e-3)
        assert deflections[1, 1] == pytest.approx(2.0 * 0.79374, 1e-3)

    def test__convergence__change_geometry(self):
        sersic_0 = ag.mp.EllSersic(centre=(0.0, 0.0))
        sersic_1 = ag.mp.EllSersic(centre=(1.0, 1.0))

        convergence_0 = sersic_0.convergence_2d_from(grid=np.array([[1.0, 1.0]]))

        convergence_1 = sersic_1.convergence_2d_from(grid=np.array([[0.0, 0.0]]))

        assert convergence_0 == pytest.approx(convergence_1, 1.0e-6)

        sersic_0 = ag.mp.EllSersic(centre=(0.0, 0.0))
        sersic_1 = ag.mp.EllSersic(centre=(0.0, 0.0))

        convergence_0 = sersic_0.convergence_2d_from(grid=np.array([[1.0, 0.0]]))

        convergence_1 = sersic_1.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence_0 == convergence_1

        sersic_0 = ag.mp.EllSersic(centre=(0.0, 0.0), elliptical_comps=(0.0, 0.111111))
        sersic_1 = ag.mp.EllSersic(centre=(0.0, 0.0), elliptical_comps=(0.0, -0.111111))

        convergence_0 = sersic_0.convergence_2d_from(grid=np.array([[1.0, 0.0]]))

        convergence_1 = sersic_1.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence_0 == convergence_1

    def test__deflections__change_geometry(self):

        sersic_0 = ag.mp.EllSersic(centre=(0.0, 0.0))
        sersic_1 = ag.mp.EllSersic(centre=(1.0, 1.0))

        deflections_0 = sersic_0.deflections_2d_from(grid=np.array([[1.0, 1.0]]))
        deflections_1 = sersic_1.deflections_2d_from(grid=np.array([[0.0, 0.0]]))

        assert deflections_0[0, 0] == pytest.approx(-deflections_1[0, 0], 1e-4)
        assert deflections_0[0, 1] == pytest.approx(-deflections_1[0, 1], 1e-4)

        sersic_0 = ag.mp.EllSersic(centre=(0.0, 0.0))
        sersic_1 = ag.mp.EllSersic(centre=(0.0, 0.0))

        deflections_0 = sersic_0.deflections_2d_from(grid=np.array([[1.0, 0.0]]))
        deflections_1 = sersic_1.deflections_2d_from(grid=np.array([[0.0, 1.0]]))

        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-4)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-4)

        sersic_0 = ag.mp.EllSersic(centre=(0.0, 0.0), elliptical_comps=(0.0, 0.111111))
        sersic_1 = ag.mp.EllSersic(centre=(0.0, 0.0), elliptical_comps=(0.0, -0.111111))

        deflections_0 = sersic_0.deflections_2d_from(grid=np.array([[1.0, 0.0]]))
        deflections_1 = sersic_1.deflections_2d_from(grid=np.array([[0.0, 1.0]]))

        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-4)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-4)

    def test__spherical_and_elliptical_identical(self):
        elliptical = ag.mp.EllSersic(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.0),
            intensity=1.0,
            effective_radius=1.0,
            sersic_index=4.0,
            mass_to_light_ratio=1.0,
        )

        spherical = ag.mp.EllSersic(
            centre=(0.0, 0.0),
            intensity=1.0,
            effective_radius=1.0,
            sersic_index=4.0,
            mass_to_light_ratio=1.0,
        )

        assert (
            elliptical.convergence_2d_from(grid=grid)
            == spherical.convergence_2d_from(grid=grid)
        ).all()
        # assert elliptical.potential_2d_from(grid=grid) == spherical.potential_2d_from(grid=grid)
        np.testing.assert_almost_equal(
            elliptical.deflections_2d_via_integrator_from(grid=grid),
            spherical.deflections_2d_via_integrator_from(grid=grid),
        )

    def test__outputs_are_autoarrays(self):
        grid = ag.Grid2D.uniform(shape_native=(2, 2), pixel_scales=1.0, sub_size=1)

        sersic = ag.mp.EllSersic()

        convergence = sersic.convergence_2d_from(grid=grid)

        assert convergence.shape_native == (2, 2)

        # potential = sersic.potential_2d_from(
        #     grid=grid)
        #
        # assert potential.shape == (2, 2)

        deflections = sersic.deflections_2d_via_integrator_from(grid=grid)

        assert deflections.shape_native == (2, 2)

        sersic = ag.mp.EllSersic()

        convergence = sersic.convergence_2d_from(grid=grid)

        assert convergence.shape_native == (2, 2)

        # potential = sersic.potential_2d_from(
        #     grid=grid)
        #
        # assert potential.shape == (2, 2)

        deflections = sersic.deflections_2d_via_integrator_from(grid=grid)

        assert deflections.shape_native == (2, 2)


class TestExponential:
    def test__convergence_correct_values(self):
        exponential = ag.mp.EllExponential(
            elliptical_comps=(0.0, 0.333333),
            intensity=3.0,
            effective_radius=2.0,
            mass_to_light_ratio=1.0,
        )

        convergence = exponential.convergence_2d_from(grid=np.array([[1.0, 0.0]]))

        assert convergence == pytest.approx(4.9047, 1e-3)

        exponential = ag.mp.EllExponential(
            elliptical_comps=(0.0, -0.333333),
            intensity=2.0,
            effective_radius=3.0,
            mass_to_light_ratio=1.0,
        )

        convergence = exponential.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(4.8566, 1e-3)

        exponential = ag.mp.EllExponential(
            elliptical_comps=(0.0, -0.333333),
            intensity=4.0,
            effective_radius=3.0,
            mass_to_light_ratio=1.0,
        )
        convergence = exponential.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(2.0 * 4.8566, 1e-3)

        exponential = ag.mp.EllExponential(
            elliptical_comps=(0.0, -0.333333),
            intensity=2.0,
            effective_radius=3.0,
            mass_to_light_ratio=2.0,
        )

        convergence = exponential.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(2.0 * 4.8566, 1e-3)

        exponential = ag.mp.EllExponential(
            elliptical_comps=(0.0, -0.333333),
            intensity=2.0,
            effective_radius=3.0,
            mass_to_light_ratio=1.0,
        )

        convergence = exponential.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(4.8566, 1e-3)

    def test__convergence_2d_via_gaussians_from__correct_values(self):
        exponential = ag.mp.EllExponential(
            elliptical_comps=(0.0, 0.333333),
            intensity=3.0,
            effective_radius=2.0,
            mass_to_light_ratio=1.0,
        )

        convergence = exponential.convergence_2d_via_gaussians_from(
            grid=np.array([[1.0, 0.0]])
        )

        assert convergence == pytest.approx(4.9047, 1e-3)

        exponential = ag.mp.EllExponential(
            elliptical_comps=(0.0, -0.333333),
            intensity=2.0,
            effective_radius=3.0,
            mass_to_light_ratio=1.0,
        )

        convergence = exponential.convergence_2d_via_gaussians_from(
            grid=np.array([[0.0, 1.0]])
        )

        assert convergence == pytest.approx(4.8566, 1e-3)

        exponential = ag.mp.EllExponential(
            elliptical_comps=(0.0, -0.333333),
            intensity=4.0,
            effective_radius=3.0,
            mass_to_light_ratio=1.0,
        )
        convergence = exponential.convergence_2d_via_gaussians_from(
            grid=np.array([[0.0, 1.0]])
        )

        assert convergence == pytest.approx(2.0 * 4.8566, 1e-3)

        exponential = ag.mp.EllExponential(
            elliptical_comps=(0.0, -0.333333),
            intensity=2.0,
            effective_radius=3.0,
            mass_to_light_ratio=2.0,
        )

        convergence = exponential.convergence_2d_via_gaussians_from(
            grid=np.array([[0.0, 1.0]])
        )

        assert convergence == pytest.approx(2.0 * 4.8566, 1e-3)

        exponential = ag.mp.EllExponential(
            elliptical_comps=(0.0, -0.333333),
            intensity=2.0,
            effective_radius=3.0,
            mass_to_light_ratio=1.0,
        )

        convergence = exponential.convergence_2d_via_gaussians_from(
            grid=np.array([[0.0, 1.0]])
        )

        assert convergence == pytest.approx(4.8566, 1e-3)

    def test__deflections_via_integrator__correct_values(self):
        exponential = ag.mp.EllExponential(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=5.0,
            effective_radius=0.2,
            mass_to_light_ratio=1.0,
        )

        deflections = exponential.deflections_2d_via_integrator_from(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(0.90493, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.62569, 1e-3)

        exponential = ag.mp.EllExponential(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=5.0,
            effective_radius=0.2,
            mass_to_light_ratio=1.0,
        )

        deflections = exponential.deflections_2d_via_integrator_from(
            grid=ag.Grid2DIrregular([(0.1625, 0.1625)])
        )

        assert deflections[0, 0] == pytest.approx(0.90493, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.62569, 1e-3)

    def test__deflections_2d_from_close_to_integrator_correct_values(self):
        exponential = ag.mp.EllExponential(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=5.0,
            effective_radius=0.2,
            mass_to_light_ratio=1.0,
        )

        deflections = exponential.deflections_2d_from(grid=np.array([[0.1625, 0.1625]]))

        assert deflections[0, 0] == pytest.approx(0.90493, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.62569, 1e-3)

        exponential = ag.mp.EllExponential(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=5.0,
            effective_radius=0.2,
            mass_to_light_ratio=1.0,
        )

        deflections = exponential.deflections_2d_from(
            grid=ag.Grid2DIrregular([(0.1625, 0.1625)])
        )

        assert deflections[0, 0] == pytest.approx(0.90493, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.62569, 1e-3)

    def test__spherical_and_elliptical_identical(self):
        elliptical = ag.mp.EllExponential(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.0),
            intensity=1.0,
            effective_radius=1.0,
            mass_to_light_ratio=1.0,
        )

        spherical = ag.mp.EllExponential(
            centre=(0.0, 0.0),
            intensity=1.0,
            effective_radius=1.0,
            mass_to_light_ratio=1.0,
        )

        assert (
            elliptical.convergence_2d_from(grid=grid)
            == spherical.convergence_2d_from(grid=grid)
        ).all()

    def test__outputs_are_autoarrays(self):
        grid = ag.Grid2D.uniform(shape_native=(2, 2), pixel_scales=1.0, sub_size=1)

        exponential = ag.mp.EllExponential()

        convergence = exponential.convergence_2d_from(grid=grid)

        assert convergence.shape_native == (2, 2)

        # potential = exponential.potential_2d_from(
        #     grid=grid)
        #
        # assert potential.shape == (2, 2)

        deflections = exponential.deflections_2d_via_integrator_from(grid=grid)

        assert deflections.shape_native == (2, 2)

        exponential = ag.mp.EllExponential()

        convergence = exponential.convergence_2d_from(grid=grid)

        assert convergence.shape_native == (2, 2)

        # potential = exponential.potential_2d_from(
        #     grid=grid)
        #
        # assert potential.shape == (2, 2)

        deflections = exponential.deflections_2d_via_integrator_from(grid=grid)

        assert deflections.shape_native == (2, 2)


class TestDevVaucouleurs:
    def test__convergence_correct_values(self):
        dev = ag.mp.EllDevVaucouleurs(
            elliptical_comps=(0.0, 0.333333),
            intensity=3.0,
            effective_radius=2.0,
            mass_to_light_ratio=1.0,
        )

        convergence = dev.convergence_2d_from(grid=np.array([[1.0, 0.0]]))

        assert convergence == pytest.approx(5.6697, 1e-3)

        dev = ag.mp.EllDevVaucouleurs(
            elliptical_comps=(0.0, -0.333333),
            intensity=2.0,
            effective_radius=3.0,
            mass_to_light_ratio=1.0,
        )

        convergence = dev.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(7.4455, 1e-3)

        dev = ag.mp.EllDevVaucouleurs(
            elliptical_comps=(0.0, -0.333333),
            intensity=4.0,
            effective_radius=3.0,
            mass_to_light_ratio=1.0,
        )

        convergence = dev.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(2.0 * 7.4455, 1e-3)

        dev = ag.mp.EllDevVaucouleurs(
            elliptical_comps=(0.0, -0.333333),
            intensity=2.0,
            effective_radius=3.0,
            mass_to_light_ratio=2.0,
        )

        convergence = dev.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(2.0 * 7.4455, 1e-3)

        dev = ag.mp.EllDevVaucouleurs(
            centre=(0.0, 0.0),
            intensity=1.0,
            effective_radius=0.6,
            mass_to_light_ratio=1.0,
        )

        convergence = dev.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(0.351797, 1e-3)

    def test__convergence_2d_via_gaussians_from__correct_values(self):
        dev = ag.mp.EllDevVaucouleurs(
            elliptical_comps=(0.0, 0.333333),
            intensity=3.0,
            effective_radius=2.0,
            mass_to_light_ratio=1.0,
        )

        convergence = dev.convergence_2d_via_gaussians_from(grid=np.array([[1.0, 0.0]]))

        assert convergence == pytest.approx(5.6697, 1e-3)

        dev = ag.mp.EllDevVaucouleurs(
            elliptical_comps=(0.0, -0.333333),
            intensity=2.0,
            effective_radius=3.0,
            mass_to_light_ratio=1.0,
        )

        convergence = dev.convergence_2d_via_gaussians_from(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(7.4455, 1e-3)

        dev = ag.mp.EllDevVaucouleurs(
            elliptical_comps=(0.0, -0.333333),
            intensity=4.0,
            effective_radius=3.0,
            mass_to_light_ratio=1.0,
        )

        convergence = dev.convergence_2d_via_gaussians_from(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(2.0 * 7.4455, 1e-3)

        dev = ag.mp.EllDevVaucouleurs(
            elliptical_comps=(0.0, -0.333333),
            intensity=2.0,
            effective_radius=3.0,
            mass_to_light_ratio=2.0,
        )

        convergence = dev.convergence_2d_via_gaussians_from(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(2.0 * 7.4455, 1e-3)

        dev = ag.mp.EllDevVaucouleurs(
            centre=(0.0, 0.0),
            intensity=1.0,
            effective_radius=0.6,
            mass_to_light_ratio=1.0,
        )

        convergence = dev.convergence_2d_via_gaussians_from(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(0.351797, 1e-3)

    def test__deflections_via_integrator__correct_values(self):
        dev = ag.mp.EllDevVaucouleurs(
            centre=(0.4, 0.2),
            elliptical_comps=(0.0180010, 0.0494575),
            intensity=2.0,
            effective_radius=0.8,
            mass_to_light_ratio=3.0,
        )

        deflections = dev.deflections_2d_via_integrator_from(
            grid=ag.Grid2DIrregular([(0.1625, 0.1625)])
        )

        assert deflections[0, 0] == pytest.approx(-24.528, 1e-3)
        assert deflections[0, 1] == pytest.approx(-3.37605, 1e-3)

    def test__deflections_2d_from_close_to_integrator__correct_values(self):
        dev = ag.mp.EllDevVaucouleurs(
            centre=(0.4, 0.2),
            elliptical_comps=(0.0180010, 0.0494575),
            intensity=2.0,
            effective_radius=0.8,
            mass_to_light_ratio=3.0,
        )

        deflections = dev.deflections_2d_from(
            grid=ag.Grid2DIrregular([(0.1625, 0.1625)])
        )

        # assert deflections[0, 0] == pytest.approx(-24.528, 1e-3)
        # assert deflections[0, 1] == pytest.approx(-3.37605, 1e-3)

    def test__spherical_and_elliptical_identical(self):
        elliptical = ag.mp.EllDevVaucouleurs(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.0),
            intensity=1.0,
            effective_radius=1.0,
            mass_to_light_ratio=1.0,
        )

        spherical = ag.mp.EllDevVaucouleurs(
            centre=(0.0, 0.0),
            intensity=1.0,
            effective_radius=1.0,
            mass_to_light_ratio=1.0,
        )

        assert (
            elliptical.convergence_2d_from(grid=grid)
            == spherical.convergence_2d_from(grid=grid)
        ).all()

    def test__outputs_are_autoarrays(self):
        grid = ag.Grid2D.uniform(shape_native=(2, 2), pixel_scales=1.0, sub_size=1)

        dev_vaucouleurs = ag.mp.EllDevVaucouleurs()

        convergence = dev_vaucouleurs.convergence_2d_from(grid=grid)

        assert convergence.shape_native == (2, 2)

        # potential = dev_vaucouleurs.potential_2d_from(
        #     grid=grid)
        #
        # assert potential.shape == (2, 2)

        deflections = dev_vaucouleurs.deflections_2d_via_integrator_from(grid=grid)

        assert deflections.shape_native == (2, 2)

        dev_vaucouleurs = ag.mp.EllDevVaucouleurs()

        convergence = dev_vaucouleurs.convergence_2d_from(grid=grid)

        assert convergence.shape_native == (2, 2)

        # potential = dev_vaucouleurs.potential_2d_from(
        #     grid=grid)
        #
        # assert potential.shape == (2, 2)

        deflections = dev_vaucouleurs.deflections_2d_via_integrator_from(grid=grid)

        assert deflections.shape_native == (2, 2)


class TestSersicMassRadialGradient:
    def test__convergence_correct_values(self):
        # ((axis_ratio*radius/effective_radius)**-mass_to_light_gradient) = (1/0.6)**-1.0 = 0.6
        sersic = ag.mp.EllSersicRadialGradient(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.0),
            intensity=1.0,
            effective_radius=0.6,
            sersic_index=4.0,
            mass_to_light_ratio=1.0,
            mass_to_light_gradient=1.0,
        )

        convergence = sersic.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(0.6 * 0.351797, 1e-3)

        # ((axis_ratio*radius/effective_radius)**-mass_to_light_gradient) = (1.5/2.0)**1.0 = 0.75

        sersic = ag.mp.EllSersicRadialGradient(
            elliptical_comps=(0.0, 0.0),
            intensity=3.0,
            effective_radius=2.0,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
            mass_to_light_gradient=-1.0,
        )

        convergence = sersic.convergence_2d_from(grid=np.array([[1.5, 0.0]]))

        assert convergence == pytest.approx(0.75 * 4.90657319276, 1e-3)

        sersic = ag.mp.EllSersicRadialGradient(
            elliptical_comps=(0.0, 0.0),
            intensity=6.0,
            effective_radius=2.0,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
            mass_to_light_gradient=-1.0,
        )

        convergence = sersic.convergence_2d_from(grid=np.array([[1.5, 0.0]]))

        assert convergence == pytest.approx(2.0 * 0.75 * 4.90657319276, 1e-3)

        sersic = ag.mp.EllSersicRadialGradient(
            elliptical_comps=(0.0, 0.0),
            intensity=3.0,
            effective_radius=2.0,
            sersic_index=2.0,
            mass_to_light_ratio=2.0,
            mass_to_light_gradient=-1.0,
        )

        convergence = sersic.convergence_2d_from(grid=np.array([[1.5, 0.0]]))

        assert convergence == pytest.approx(2.0 * 0.75 * 4.90657319276, 1e-3)

        # ((axis_ratio*radius/effective_radius)**-mass_to_light_gradient) = ((0.5*1.41)/2.0)**-1.0 = 2.836
        sersic = ag.mp.EllSersicRadialGradient(
            elliptical_comps=(0.0, 0.333333),
            intensity=3.0,
            effective_radius=2.0,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
            mass_to_light_gradient=1.0,
        )

        convergence = sersic.convergence_2d_from(grid=np.array([[1.0, 0.0]]))

        assert convergence == pytest.approx(2.836879 * 5.38066670129, abs=2e-01)

    def test__deflections_via_integrator__correct_values(self):
        sersic = ag.mp.EllSersicRadialGradient(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=5.0,
            effective_radius=0.2,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
            mass_to_light_gradient=1.0,
        )

        deflections = sersic.deflections_2d_via_integrator_from(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert deflections[0, 0] == pytest.approx(3.60324873535244, 1e-3)
        assert deflections[0, 1] == pytest.approx(2.3638898009652, 1e-3)

        sersic = ag.mp.EllSersicRadialGradient(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=5.0,
            effective_radius=0.2,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
            mass_to_light_gradient=-1.0,
        )

        deflections = sersic.deflections_2d_via_integrator_from(
            grid=ag.Grid2DIrregular([(0.1625, 0.1625)])
        )

        assert deflections[0, 0] == pytest.approx(0.97806399756448, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.725459334118341, 1e-3)

    def test__deflections_2d_from_using_mge__same_as_integrator__correct_values(self):

        # sersic = ag.mp.EllSersicRadialGradient(
        #     centre=(-0.4, -0.2),
        #     elliptical_comps=(-0.07142, -0.085116),
        #     intensity=5.0,
        #     effective_radius=0.2,
        #     sersic_index=2.0,
        #     mass_to_light_ratio=1.0,
        #     mass_to_light_gradient=1.0,
        # )
        #
        # deflections = sersic.deflections_2d_from(grid=np.array([[0.1625, 0.1625]]))
        #
        # assert deflections[0, 0] == pytest.approx(3.60324873535244, 1e-3)
        # assert deflections[0, 1] == pytest.approx(2.3638898009652, 1e-3)

        sersic = ag.mp.EllSersicRadialGradient(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=5.0,
            effective_radius=0.2,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
            mass_to_light_gradient=-1.0,
        )

        deflections = sersic.deflections_2d_from(
            grid=ag.Grid2DIrregular([(0.1625, 0.1625)])
        )

        assert deflections[0, 0] == pytest.approx(0.97806399756448, 1e-3)
        assert deflections[0, 1] == pytest.approx(0.725459334118341, 1e-3)

    def test__compare_to_sersic(self):
        sersic = ag.mp.EllSersicRadialGradient(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=5.0,
            effective_radius=0.2,
            sersic_index=1.0,
            mass_to_light_ratio=1.0,
            mass_to_light_gradient=0.0,
        )

        sersic_deflections = sersic.deflections_2d_from(
            grid=np.array([[0.1625, 0.1625]])
        )

        exponential = ag.mp.EllExponential(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=5.0,
            effective_radius=0.2,
            mass_to_light_ratio=1.0,
        )
        exponential_deflections = exponential.deflections_2d_from(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert sersic_deflections[0, 0] == pytest.approx(
            exponential_deflections[0, 0], 1e-3
        )
        assert sersic_deflections[0, 0] == pytest.approx(0.90493, 1e-3)
        assert sersic_deflections[0, 1] == pytest.approx(
            exponential_deflections[0, 1], 1e-3
        )
        assert sersic_deflections[0, 1] == pytest.approx(0.62569, 1e-3)

        sersic = ag.mp.EllSersicRadialGradient(
            centre=(0.4, 0.2),
            elliptical_comps=(0.0180010, 0.0494575),
            intensity=2.0,
            effective_radius=0.8,
            sersic_index=4.0,
            mass_to_light_ratio=3.0,
            mass_to_light_gradient=0.0,
        )
        sersic_deflections = sersic.deflections_2d_from(
            grid=np.array([[0.1625, 0.1625]])
        )

        dev = ag.mp.EllDevVaucouleurs(
            centre=(0.4, 0.2),
            elliptical_comps=(0.0180010, 0.0494575),
            intensity=2.0,
            effective_radius=0.8,
            mass_to_light_ratio=3.0,
        )

        dev_deflections = dev.deflections_2d_from(grid=np.array([[0.1625, 0.1625]]))

        # assert sersic_deflections[0, 0] == pytest.approx(dev_deflections[0, 0], 1e-3)
        # assert sersic_deflections[0, 0] == pytest.approx(-24.528, 1e-3)
        # assert sersic_deflections[0, 1] == pytest.approx(dev_deflections[0, 1], 1e-3)
        # assert sersic_deflections[0, 1] == pytest.approx(-3.37605, 1e-3)

        sersic_grad = ag.mp.EllSersicRadialGradient(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=5.0,
            effective_radius=0.2,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
            mass_to_light_gradient=0.0,
        )
        sersic_grad_deflections = sersic_grad.deflections_2d_from(
            grid=np.array([[0.1625, 0.1625]])
        )

        sersic = ag.mp.EllSersic(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=5.0,
            effective_radius=0.2,
            sersic_index=2.0,
            mass_to_light_ratio=1.0,
        )
        sersic_deflections = sersic.deflections_2d_from(
            grid=np.array([[0.1625, 0.1625]])
        )

        assert sersic_deflections[0, 0] == pytest.approx(
            sersic_grad_deflections[0, 0], 1e-3
        )
        assert sersic_deflections[0, 0] == pytest.approx(1.1446, 1e-3)
        assert sersic_deflections[0, 1] == pytest.approx(
            sersic_grad_deflections[0, 1], 1e-3
        )
        assert sersic_deflections[0, 1] == pytest.approx(0.79374, 1e-3)

    def test__spherical_and_elliptical_identical(self):
        elliptical = ag.mp.EllSersicRadialGradient(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.0),
            intensity=1.0,
            effective_radius=1.0,
            sersic_index=4.0,
            mass_to_light_ratio=1.0,
            mass_to_light_gradient=1.0,
        )

        spherical = ag.mp.EllSersicRadialGradient(
            centre=(0.0, 0.0),
            intensity=1.0,
            effective_radius=1.0,
            sersic_index=4.0,
            mass_to_light_ratio=1.0,
            mass_to_light_gradient=1.0,
        )

        assert (
            elliptical.convergence_2d_from(grid=grid)
            == spherical.convergence_2d_from(grid=grid)
        ).all()
        # assert elliptical.potential_2d_from(grid=grid) == spherical.potential_2d_from(grid=grid)
        assert (
            elliptical.deflections_2d_from(grid=grid)
            == spherical.deflections_2d_from(grid=grid)
        ).all()

    def test__outputs_are_autoarrays(self):
        grid = ag.Grid2D.uniform(shape_native=(2, 2), pixel_scales=1.0, sub_size=1)

        sersic = ag.mp.EllSersicRadialGradient()

        convergence = sersic.convergence_2d_from(grid=grid)

        assert convergence.shape_native == (2, 2)

        # potential = sersic.potential_2d_from(
        #     grid=grid)
        #
        # assert potential.shape == (2, 2)

        deflections = sersic.deflections_2d_from(grid=grid)

        assert deflections.shape_native == (2, 2)

        sersic = ag.mp.EllSersicRadialGradient()

        convergence = sersic.convergence_2d_from(grid=grid)

        assert convergence.shape_native == (2, 2)

        # potential = sersic.potential_2d_from(
        #     grid=grid)
        #
        # assert potential.shape == (2, 2)

        deflections = sersic.deflections_2d_from(grid=grid)

        assert deflections.shape_native == (2, 2)


class TestSersicCore:
    def test__convergence_correct_values(self):

        core_sersic = ag.mp.EllSersicCore(
            elliptical_comps=(0.0, 0.0),
            effective_radius=5.0,
            sersic_index=4.0,
            radius_break=0.01,
            intensity_break=0.1,
            gamma=1.0,
            alpha=1.0,
            mass_to_light_ratio=1.0,
        )

        convergence = core_sersic.convergence_2d_from(grid=np.array([[0.0, 0.01]]))

        assert convergence == pytest.approx(0.1, 1e-3)

        core_sersic = ag.mp.EllSersicCore(
            elliptical_comps=(0.0, 0.0),
            effective_radius=5.0,
            sersic_index=4.0,
            radius_break=0.01,
            intensity_break=0.1,
            gamma=1.0,
            alpha=1.0,
            mass_to_light_ratio=2.0,
        )

        convergence = core_sersic.convergence_2d_from(grid=np.array([[0.0, 0.01]]))

        assert convergence == pytest.approx(0.2, 1e-3)

    def test__convergence_2d_via_gaussians_from__same_as_convergence_2d_from(self):

        core_sersic = ag.mp.EllSersicCore(
            elliptical_comps=(0.2, 0.4),
            effective_radius=5.0,
            sersic_index=4.0,
            radius_break=0.01,
            intensity_break=0.1,
            gamma=1.0,
            alpha=1.0,
            mass_to_light_ratio=1.0,
        )

        convergence = core_sersic.convergence_2d_from(grid=np.array([[0.0, 1.0]]))
        convergence_via_gaussians = core_sersic.convergence_2d_via_gaussians_from(
            grid=np.array([[0.0, 1.0]])
        )

        assert convergence == pytest.approx(convergence_via_gaussians, 1e-3)

    def test__deflections_2d_from__correct_values(self):

        sersic = ag.mp.EllSersicCore(
            centre=(1.0, 2.0),
            elliptical_comps=ag.convert.elliptical_comps_from(
                axis_ratio=0.5, angle=70.0
            ),
            intensity_break=0.45,
            effective_radius=0.5,
            radius_break=0.01,
            gamma=0.0,
            alpha=2.0,
            sersic_index=2.2,
        )

        deflections = sersic.deflections_2d_from(grid=np.array([[2.5, -2.5]]))

        assert deflections[0, 0] == pytest.approx(0.0015047, 1e-4)
        assert deflections[0, 1] == pytest.approx(-0.004493, 1e-4)

        sersic = ag.mp.EllSersicCore(
            centre=(1.0, 2.0),
            elliptical_comps=ag.convert.elliptical_comps_from(
                axis_ratio=0.5, angle=70.0
            ),
            intensity_break=2.0 * 0.45,
            effective_radius=0.5,
            radius_break=0.01,
            gamma=0.0,
            alpha=2.0,
            sersic_index=2.2,
        )

        deflections = sersic.deflections_2d_from(grid=np.array([[2.5, -2.5]]))

        assert deflections[0, 0] == pytest.approx(2.0 * 0.0015047, 1e-4)
        assert deflections[0, 1] == pytest.approx(2.0 * -0.004493, 1e-4)

        sersic = ag.mp.EllSersicCore(
            centre=(1.0, 2.0),
            elliptical_comps=ag.convert.elliptical_comps_from(
                axis_ratio=0.5, angle=70.0
            ),
            intensity_break=0.45,
            effective_radius=0.5,
            radius_break=0.01,
            gamma=0.0,
            alpha=2.0,
            sersic_index=2.2,
            mass_to_light_ratio=2.0,
        )

        deflections = sersic.deflections_2d_from(grid=np.array([[2.5, -2.5]]))

        assert deflections[0, 0] == pytest.approx(2.0 * 0.0015047, 1e-4)
        assert deflections[0, 1] == pytest.approx(2.0 * -0.004493, 1e-4)

    def test__convergence__change_geometry(self):

        sersic_0 = ag.mp.EllSersicCore(centre=(0.0, 0.0))
        sersic_1 = ag.mp.EllSersicCore(centre=(1.0, 1.0))

        convergence_0 = sersic_0.convergence_2d_from(grid=np.array([[1.0, 1.0]]))

        convergence_1 = sersic_1.convergence_2d_from(grid=np.array([[0.0, 0.0]]))

        assert convergence_0 == convergence_1

        sersic_0 = ag.mp.EllSersicCore(centre=(0.0, 0.0))
        sersic_1 = ag.mp.EllSersicCore(centre=(0.0, 0.0))

        convergence_0 = sersic_0.convergence_2d_from(grid=np.array([[1.0, 0.0]]))

        convergence_1 = sersic_1.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence_0 == convergence_1

        sersic_0 = ag.mp.EllSersicCore(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.111111)
        )
        sersic_1 = ag.mp.EllSersicCore(
            centre=(0.0, 0.0), elliptical_comps=(0.0, -0.111111)
        )

        convergence_0 = sersic_0.convergence_2d_from(grid=np.array([[1.0, 0.0]]))

        convergence_1 = sersic_1.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence_0 == convergence_1

    def test__deflections__change_geometry(self):

        sersic_0 = ag.mp.EllSersicCore(centre=(0.0, 0.0))
        sersic_1 = ag.mp.EllSersicCore(centre=(1.0, 1.0))

        deflections_0 = sersic_0.deflections_2d_from(grid=np.array([[1.0, 1.0]]))
        deflections_1 = sersic_1.deflections_2d_from(grid=np.array([[0.0, 0.0]]))

        assert deflections_0[0, 0] == pytest.approx(-deflections_1[0, 0], 1e-4)
        assert deflections_0[0, 1] == pytest.approx(-deflections_1[0, 1], 1e-4)

        sersic_0 = ag.mp.EllSersicCore(centre=(0.0, 0.0))
        sersic_1 = ag.mp.EllSersicCore(centre=(0.0, 0.0))

        deflections_0 = sersic_0.deflections_2d_from(grid=np.array([[1.0, 0.0]]))
        deflections_1 = sersic_1.deflections_2d_from(grid=np.array([[0.0, 1.0]]))

        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-4)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-4)

        sersic_0 = ag.mp.EllSersicCore(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.111111)
        )
        sersic_1 = ag.mp.EllSersicCore(
            centre=(0.0, 0.0), elliptical_comps=(0.0, -0.111111)
        )

        deflections_0 = sersic_0.deflections_2d_from(grid=np.array([[1.0, 0.0]]))
        deflections_1 = sersic_1.deflections_2d_from(grid=np.array([[0.0, 1.0]]))

        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-4)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-4)

    def test__spherical_and_elliptical_identical(self):

        elliptical = ag.mp.EllSersicCore(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.0),
            effective_radius=1.0,
            sersic_index=4.0,
            mass_to_light_ratio=1.0,
        )

        spherical = ag.mp.EllSersicCore(
            centre=(0.0, 0.0),
            effective_radius=1.0,
            sersic_index=4.0,
            mass_to_light_ratio=1.0,
        )

        assert (
            elliptical.convergence_2d_from(grid=grid)
            == spherical.convergence_2d_from(grid=grid)
        ).all()
        # assert elliptical.potential_2d_from(grid=grid) == spherical.potential_2d_from(grid=grid)
        np.testing.assert_almost_equal(
            elliptical.deflections_2d_via_integrator_from(grid=grid),
            spherical.deflections_2d_via_integrator_from(grid=grid),
        )

    def test__outputs_are_autoarrays(self):

        grid = ag.Grid2D.uniform(shape_native=(2, 2), pixel_scales=1.0, sub_size=1)

        sersic = ag.mp.EllSersicCore()

        convergence = sersic.convergence_2d_from(grid=grid)

        assert convergence.shape_native == (2, 2)

        # potential = sersic.potential_2d_from(
        #     grid=grid)
        #
        # assert potential.shape == (2, 2)

        deflections = sersic.deflections_2d_via_integrator_from(grid=grid)

        assert deflections.shape_native == (2, 2)

        sersic = ag.mp.EllSersicCore()

        convergence = sersic.convergence_2d_from(grid=grid)

        assert convergence.shape_native == (2, 2)

        # potential = sersic.potential_2d_from(
        #     grid=grid)
        #
        # assert potential.shape == (2, 2)

        deflections = sersic.deflections_2d_via_integrator_from(grid=grid)

        assert deflections.shape_native == (2, 2)


class TestChameleon:
    def test__convergence_correct_values(self):

        chameleon = ag.mp.EllChameleon(
            elliptical_comps=(0.0, 0.0),
            intensity=1.0,
            core_radius_0=0.1,
            core_radius_1=0.3,
            mass_to_light_ratio=2.0,
        )

        convergence = chameleon.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence == pytest.approx(2.0 * 0.018605, 1e-3)

        chameleon = ag.mp.EllChameleon(
            elliptical_comps=(0.5, 0.0),
            intensity=3.0,
            core_radius_0=0.2,
            core_radius_1=0.4,
            mass_to_light_ratio=1.0,
        )

        convergence = chameleon.convergence_2d_from(grid=np.array([[0.0, 1.5]]))

        assert convergence == pytest.approx(0.007814, 1e-3)

    def test__deflections_correct_values(self):
        chameleon = ag.mp.EllChameleon(
            centre=(-0.4, -0.2),
            elliptical_comps=(-0.07142, -0.085116),
            intensity=5.0,
            core_radius_0=0.2,
            core_radius_1=0.4,
            mass_to_light_ratio=3.0,
        )

        deflections = chameleon.deflections_2d_from(grid=np.array([[0.1625, 0.1625]]))

        assert deflections[0, 0] == pytest.approx(2.12608, 1e-3)
        assert deflections[0, 1] == pytest.approx(1.55252, 1e-3)

    def test__convergence__change_geometry(self):
        chameleon_0 = ag.mp.EllChameleon(
            centre=(0.0, 0.0), intensity=3.0, core_radius_0=0.2, core_radius_1=0.4
        )
        chameleon_1 = ag.mp.EllChameleon(
            centre=(1.0, 1.0), intensity=3.0, core_radius_0=0.2, core_radius_1=0.4
        )

        convergence_0 = chameleon_0.convergence_2d_from(grid=np.array([[1.0, 1.0]]))

        convergence_1 = chameleon_1.convergence_2d_from(grid=np.array([[0.0, 0.0]]))

        assert convergence_0 == pytest.approx(convergence_1, 1.0e-6)

        chameleon_0 = ag.mp.EllChameleon(
            centre=(0.0, 0.0), intensity=3.0, core_radius_0=0.2, core_radius_1=0.4
        )
        chameleon_1 = ag.mp.EllChameleon(
            centre=(0.0, 0.0), intensity=3.0, core_radius_0=0.2, core_radius_1=0.4
        )

        convergence_0 = chameleon_0.convergence_2d_from(grid=np.array([[1.0, 0.0]]))

        convergence_1 = chameleon_1.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

        chameleon_0 = ag.mp.EllChameleon(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.111111)
        )
        chameleon_1 = ag.mp.EllChameleon(
            centre=(0.0, 0.0), elliptical_comps=(0.0, -0.111111)
        )

        convergence_0 = chameleon_0.convergence_2d_from(grid=np.array([[1.0, 0.0]]))

        convergence_1 = chameleon_1.convergence_2d_from(grid=np.array([[0.0, 1.0]]))

        assert convergence_0 == pytest.approx(convergence_1, 1.0e-4)

    def test__deflections__change_geometry(self):
        chameleon_0 = ag.mp.EllChameleon(centre=(0.0, 0.0))
        chameleon_1 = ag.mp.EllChameleon(centre=(1.0, 1.0))

        deflections_0 = chameleon_0.deflections_2d_from(grid=np.array([[1.0, 1.0]]))
        deflections_1 = chameleon_1.deflections_2d_from(grid=np.array([[0.0, 0.0]]))

        assert deflections_0[0, 0] == pytest.approx(-deflections_1[0, 0], 1e-4)
        assert deflections_0[0, 1] == pytest.approx(-deflections_1[0, 1], 1e-4)

        chameleon_0 = ag.mp.EllChameleon(centre=(0.0, 0.0))
        chameleon_1 = ag.mp.EllChameleon(centre=(0.0, 0.0))

        deflections_0 = chameleon_0.deflections_2d_from(grid=np.array([[1.0, 0.0]]))
        deflections_1 = chameleon_1.deflections_2d_from(grid=np.array([[0.0, 1.0]]))

        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-4)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-4)

        chameleon_0 = ag.mp.EllChameleon(
            centre=(0.0, 0.0), elliptical_comps=(0.0, 0.111111)
        )
        chameleon_1 = ag.mp.EllChameleon(
            centre=(0.0, 0.0), elliptical_comps=(0.0, -0.111111)
        )

        deflections_0 = chameleon_0.deflections_2d_from(grid=np.array([[1.0, 0.0]]))
        deflections_1 = chameleon_1.deflections_2d_from(grid=np.array([[0.0, 1.0]]))

        assert deflections_0[0, 0] == pytest.approx(deflections_1[0, 1], 1e-4)
        assert deflections_0[0, 1] == pytest.approx(deflections_1[0, 0], 1e-4)

    def test__spherical_and_elliptical_identical(self):
        elliptical = ag.mp.EllChameleon(
            centre=(0.0, 0.0),
            elliptical_comps=(0.0, 0.0),
            intensity=1.0,
            mass_to_light_ratio=1.0,
        )

        spherical = ag.mp.EllChameleon(
            centre=(0.0, 0.0), intensity=1.0, mass_to_light_ratio=1.0
        )

        assert (
            elliptical.convergence_2d_from(grid=grid)
            == spherical.convergence_2d_from(grid=grid)
        ).all()
        # assert elliptical.potential_2d_from(grid=grid) == spherical.potential_2d_from(grid=grid)
        np.testing.assert_almost_equal(
            elliptical.deflections_2d_from(grid=grid),
            spherical.deflections_2d_from(grid=grid),
        )

    def test__outputs_are_autoarrays(self):
        grid = ag.Grid2D.uniform(shape_native=(2, 2), pixel_scales=1.0, sub_size=1)

        chameleon = ag.mp.EllChameleon()

        convergence = chameleon.convergence_2d_from(grid=grid)

        assert convergence.shape_native == (2, 2)

        # potential = chameleon.potential_2d_from(
        #     grid=grid)
        #
        # assert potential.shape == (2, 2)

        deflections = chameleon.deflections_2d_from(grid=grid)

        assert deflections.shape_native == (2, 2)

        chameleon = ag.mp.EllChameleon()

        convergence = chameleon.convergence_2d_from(grid=grid)

        assert convergence.shape_native == (2, 2)

        # potential = chameleon.potential_2d_from(
        #     grid=grid)
        #
        # assert potential.shape == (2, 2)

        deflections = chameleon.deflections_2d_from(grid=grid)

        assert deflections.shape_native == (2, 2)
