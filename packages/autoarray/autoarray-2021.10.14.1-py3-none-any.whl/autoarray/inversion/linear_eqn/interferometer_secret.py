import logging
import numpy as np

from typing import Dict, List, Optional, Union

from autoarray.dataset.interferometer_secret import WTildeInterferometer
from autoarray.inversion.linear_eqn.interferometer import (
    AbstractLinearEqnInterferometer,
)
from autoarray.inversion.inversion.settings import SettingsInversion
from autoarray.inversion.mappers.rectangular import MapperRectangular
from autoarray.inversion.mappers.voronoi import MapperVoronoi
from autoarray.inversion.regularization.abstract import AbstractRegularization
from autoarray.operators.transformer import TransformerNUFFT
from autoarray.structures.visibilities import Visibilities
from autoarray.structures.visibilities import VisibilitiesNoiseMap

from autoarray.inversion.inversion import inversion_util_secret
from autoarray.numba_util import profile_func

logger = logging.getLogger(__name__)


class LinearEqnInterferometerWTilde(AbstractLinearEqnInterferometer):
    def __init__(
        self,
        noise_map: VisibilitiesNoiseMap,
        transformer: TransformerNUFFT,
        w_tilde: WTildeInterferometer,
        mapper_list: List[Union[MapperRectangular, MapperVoronoi]],
        settings: SettingsInversion = SettingsInversion(),
        profiling_dict: Optional[Dict] = None,
    ):
        """
        An inversion, which given an input image and noise-map reconstructs the image using a linear inversion, \
        including a convolution that accounts for blurring.

        The inversion uses a 2D pixelization to perform the reconstruction by util each pixelization pixel to a \
        set of image pixels via a mapper. The reconstructed pixelization is smoothed via a regularization scheme to \
        prevent over-fitting noise.

        Parameters
        -----------
        image_1d
            Flattened 1D array of the observed image the inversion is fitting.
        noise_map
            Flattened 1D array of the noise-map used by the inversion during the fit.
        convolver : convolution.Convolver
            The convolver used to blur the mapping matrix with the PSF.
        mapper_list : inversion.Mapper
            The util between the image-pixels (via its / sub-grid) and pixelization pixels.
        regularization : inversion.regularization.Regularization
            The regularization scheme applied to smooth the pixelization used to reconstruct the image for the \
            inversion
        """

        self.w_tilde = w_tilde
        self.w_tilde.check_noise_map(noise_map=noise_map)

        super().__init__(
            noise_map=noise_map,
            transformer=transformer,
            mapper_list=mapper_list,
            profiling_dict=profiling_dict,
        )

    @profile_func
    def data_vector_from(self, data: Visibilities) -> np.ndarray:
        """
        To solve for the source pixel fluxes we now pose the problem as a linear inversion which we use the NumPy
        linear algebra libraries to solve. The linear algebra is based on
        the paper https://arxiv.org/pdf/astro-ph/0302587.pdf .

        This requires us to convert `w_tilde_data` into a data vector matrices of dimensions [image_pixels].

        The `data_vector` D is the first such matrix, which is given by equation (4)
        in https://arxiv.org/pdf/astro-ph/0302587.pdf.

        The calculation is performed by the method `w_tilde_data_interferometer_from`.
        """
        return None

    @property
    @profile_func
    def curvature_matrix_diag(self) -> np.ndarray:
        """
        The `curvature_matrix` F is the second matrix, given by equation (4)
        in https://arxiv.org/pdf/astro-ph/0302587.pdf.

        This function computes F using the w_tilde formalism, which is faster as it precomputes the Fourier Transform
        of different visibilities noise-map (see `curvature_matrix_via_w_tilde_curvature_preload_interferometer_from`).

        The `curvature_matrix` computed here is overwritten in memory when the regularization matrix is added to it,
        because for large matrices this avoids overhead. For this reason, `curvature_matrix` is not a cached property
        to ensure if we access it after computing the `curvature_reg_matrix` it is correctly recalculated in a new
        array of memory.
        """
        return inversion_util_secret.curvature_matrix_via_w_tilde_curvature_preload_interferometer_from(
            curvature_preload=self.w_tilde.curvature_preload,
            pixelization_index_for_sub_slim_index=self.mapper_list[
                0
            ].pixelization_index_for_sub_slim_index,
            native_index_for_slim_index=self.transformer.real_space_mask.mask.native_index_for_slim_index,
            pixelization_pixels=self.mapper_list[0].pixels,
        )

    @profile_func
    def mapped_reconstructed_data_of_mappers_from(
        self, reconstruction: np.ndarray
    ) -> Visibilities:
        """
        Using the reconstructed source pixel fluxes we map each source pixel flux back to the image plane to
        reconstruct the image in real-space. We then apply the Fourier Transform to map this to the reconstructed
        visibilities.

        Returns
        -------
        Visibilities
            The reconstructed visibilities which the inversion fits.
        """
        return self.transformer.visibilities_from(
            image=self.mapped_reconstructed_data_of_mappers_from(
                reconstruction=reconstruction
            )
        )
