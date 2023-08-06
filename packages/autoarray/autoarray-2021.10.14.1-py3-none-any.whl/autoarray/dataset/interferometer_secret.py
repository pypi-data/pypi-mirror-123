import logging

from autoconf import cached_property

from autoarray.dataset.abstract_dataset import AbstractWTilde
from autoarray.dataset.interferometer import Interferometer

from autoarray.inversion.inversion import inversion_util_secret

logger = logging.getLogger(__name__)


class WTildeInterferometer(AbstractWTilde):
    def __init__(self, curvature_preload, noise_map_value):

        super().__init__(
            curvature_preload=curvature_preload, noise_map_value=noise_map_value
        )


class InterferometerSecret(Interferometer):
    @cached_property
    def w_tilde(self):
        """
        The w_tilde formalism of the linear algebra equations precomputes the Fourier Transform of all the visibilities
        given the `uv_wavelengths` (see `inversion.inversion_util`).

        The `WTilde` object stores these precomputed values in the interferometer dataset ensuring they are only
        computed once per analysis.

        This uses lazy allocation such that the calculation is only performed when the wtilde matrices are used,
        ensuring efficient set up of the `Interferometer` class.

        Returns
        -------
        WTildeInterferometer
            Precomputed values used for the w tilde formalism of linear algebra calculations.
        """

        logger.info("IMAGING - Computing W-Tilde... May take a moment.")

        curvature_preload = inversion_util_secret.w_tilde_curvature_preload_interferometer_from(
            noise_map_real=self.noise_map.real,
            uv_wavelengths=self.uv_wavelengths,
            shape_masked_pixels_2d=self.transformer.grid.mask.shape_native_masked_pixels,
            grid_radians_2d=self.transformer.grid.mask.unmasked_grid_sub_1.in_radians.native,
        )

        return WTildeInterferometer(
            curvature_preload=curvature_preload, noise_map_value=self.noise_map[0]
        )
