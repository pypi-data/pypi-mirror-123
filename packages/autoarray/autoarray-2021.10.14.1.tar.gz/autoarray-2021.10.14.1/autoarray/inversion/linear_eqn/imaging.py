import numpy as np
from scipy.linalg import block_diag
from typing import Dict, List, Optional, Union

from autoconf import cached_property
from autoarray.numba_util import profile_func

from autoarray.inversion.linear_eqn.abstract import AbstractLinearEqn
from autoarray.structures.arrays.two_d.array_2d import Array2D
from autoarray.operators.convolver import Convolver
from autoarray.inversion.mappers.rectangular import MapperRectangular
from autoarray.inversion.mappers.voronoi import MapperVoronoi
from autoarray.dataset.imaging import WTildeImaging

from autoarray.inversion.linear_eqn import linear_eqn_util


class AbstractLinearEqnImaging(AbstractLinearEqn):
    def __init__(
        self,
        noise_map: Array2D,
        convolver: Convolver,
        mapper_list: List[Union[MapperRectangular, MapperVoronoi]],
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
        noise_map
            Flattened 1D array of the noise-map used by the inversion during the fit.
        convolver : convolution.Convolver
            The convolver used to blur the mapping matrix with the PSF.
        mapper_list : inversion.Mapper
            The util between the image-pixels (via its / sub-grid) and pixelization pixels.
        regularization : inversion.regularization.Regularization
            The regularization scheme applied to smooth the pixelization used to reconstruct the image for the \
            inversion

        Attributes
        -----------
        regularization_matrix
            The matrix defining how the pixelization's pixels are regularized with one another for smoothing (H).
        curvature_matrix
            The curvature_matrix between each pixelization pixel and all other pixelization pixels (F).
        curvature_reg_matrix
            The curvature_matrix + regularization matrix.
        solution_vector
            The vector containing the reconstructed fit to the hyper_galaxies.
        """

        self.convolver = convolver

        super().__init__(
            noise_map=noise_map, mapper_list=mapper_list, profiling_dict=profiling_dict
        )

    @cached_property
    @profile_func
    def blurred_mapping_matrix(self) -> np.ndarray:
        """
        For a given pixelization pixel on the mapping matrix, we can use it to map it to a set of image-pixels in the
        image  plane. This therefore creates a 'image' of the source pixel (which corresponds to a set of values that
        mostly zeros, but with 1's where mappings occur).

        Before reconstructing the source, we blur every one of these source pixel images with the Point Spread Function
        of our  dataset via 2D convolution. This uses the methods
        in `Convolver.__init__` and `Convolver.convolve_mapping_matrix`:
        """
        return np.hstack(
            [
                self.blurred_mapping_matrix_of_mapper(mapper_index=mapper_index)
                for mapper_index in range(self.total_mappers)
            ]
        )

    def blurred_mapping_matrix_of_mapper(self, mapper_index: int) -> np.ndarray:
        """
        For a given pixelization pixel on the mapping matrix, we can use it to map it to a set of image-pixels in the
        image  plane. This therefore creates a 'image' of the source pixel (which corresponds to a set of values that
        mostly zeros, but with 1's where mappings occur).

        Before reconstructing the source, we blur every one of these source pixel images with the Point Spread Function
        of our  dataset via 2D convolution. This uses the methods
        in `Convolver.__init__` and `Convolver.convolve_mapping_matrix`:
        """
        return self.convolver.convolve_mapping_matrix(
            mapping_matrix=self.mapper_list[mapper_index].mapping_matrix
        )

    @property
    def operated_mapping_matrix(self) -> np.ndarray:
        return self.blurred_mapping_matrix

    def mapped_reconstructed_image_of_mappers_from(
        self, reconstruction: np.ndarray
    ) -> List[Array2D]:
        return self.mapped_reconstructed_data_of_mappers_from(
            reconstruction=reconstruction
        )


class LinearEqnImagingWTilde(AbstractLinearEqnImaging):
    def __init__(
        self,
        noise_map: Array2D,
        convolver: Convolver,
        w_tilde: WTildeImaging,
        mapper_list: List[Union[MapperRectangular, MapperVoronoi]],
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
        """

        self.w_tilde = w_tilde
        self.w_tilde.check_noise_map(noise_map=noise_map)

        super().__init__(
            noise_map=noise_map,
            convolver=convolver,
            mapper_list=mapper_list,
            profiling_dict=profiling_dict,
        )

    @profile_func
    def data_vector_from(self, data: Array2D) -> np.ndarray:
        """
        To solve for the source pixel fluxes we now pose the problem as a linear inversion which we use the NumPy
        linear  algebra libraries to solve. The linear algebra is based on
        the paper https://arxiv.org/pdf/astro-ph/0302587.pdf .

        This requires us to convert `w_tilde_data` into a data vector matrices of dimensions [image_pixels].

        The `data_vector` D is the first such matrix, which is given by equation (4)
        in https://arxiv.org/pdf/astro-ph/0302587.pdf.

        The calculation is performed by the method `w_tilde_data_imaging_from`.
        """

        w_tilde_data = linear_eqn_util.w_tilde_data_imaging_from(
            image_native=data.native,
            noise_map_native=self.noise_map.native,
            kernel_native=self.convolver.kernel.native,
            native_index_for_slim_index=data.mask.native_index_for_slim_index,
        )

        return np.concatenate(
            [
                linear_eqn_util.data_vector_via_w_tilde_data_imaging_from(
                    w_tilde_data=w_tilde_data,
                    data_to_pix_unique=mapper.data_unique_mappings.data_to_pix_unique,
                    data_weights=mapper.data_unique_mappings.data_weights,
                    pix_lengths=mapper.data_unique_mappings.pix_lengths,
                    pix_pixels=mapper.pixels,
                )
                for mapper in self.mapper_list
            ]
        )

    @property
    @profile_func
    def curvature_matrix(self) -> np.ndarray:
        """
        The `curvature_matrix` F is the second matrix, given by equation (4)
        in https://arxiv.org/pdf/astro-ph/0302587.pdf.

        This function computes F using the w_tilde formalism, which is faster as it precomputes the PSF convolution
        of different noise-map pixels (see `curvature_matrix_via_w_tilde_curvature_preload_imaging_from`).

        The `curvature_matrix` computed here is overwritten in memory when the regularization matrix is added to it,
        because for large matrices this avoids overhead. For this reason, `curvature_matrix` is not a cached property
        to ensure if we access it after computing the `curvature_reg_matrix` it is correctly recalculated in a new
        array of memory.
        """
        if len(self.mapper_list) == 1:
            return self.curvature_matrix_diag

        curvature_matrix = self.curvature_matrix_diag

        curvature_matrix_off_diag = self.curvature_matrix_off_diag_from(
            mapper_index_0=0, mapper_index_1=1
        )

        pixels_diag = self.mapper_list[0].pixels

        curvature_matrix[0:pixels_diag, pixels_diag:] = curvature_matrix_off_diag

        for i in range(curvature_matrix.shape[0]):
            for j in range(curvature_matrix.shape[1]):
                curvature_matrix[j, i] = curvature_matrix[i, j]

        return curvature_matrix

    @property
    @profile_func
    def curvature_matrix_diag(self) -> np.ndarray:
        """
        The `curvature_matrix` F is the second matrix, given by equation (4)
        in https://arxiv.org/pdf/astro-ph/0302587.pdf.

        This function computes F using the w_tilde formalism, which is faster as it precomputes the PSF convolution
        of different noise-map pixels (see `curvature_matrix_via_w_tilde_curvature_preload_imaging_from`).

        The `curvature_matrix` computed here is overwritten in memory when the regularization matrix is added to it,
        because for large matrices this avoids overhead. For this reason, `curvature_matrix` is not a cached property
        to ensure if we access it after computing the `curvature_reg_matrix` it is correctly recalculated in a new
        array of memory.

        For multiple mappers, the curvature matrix is computed using the block diagonal of the diagonal curvature
        matrix of each individual mapper. The scipy function `block_diag` has an overhead associated with it and if
        there is only one mapper and regularization it is bypassed.
        """

        if self.has_one_mapper:

            return linear_eqn_util.curvature_matrix_via_w_tilde_curvature_preload_imaging_from(
                curvature_preload=self.w_tilde.curvature_preload,
                curvature_indexes=self.w_tilde.indexes,
                curvature_lengths=self.w_tilde.lengths,
                data_to_pix_unique=self.mapper_list[
                    0
                ].data_unique_mappings.data_to_pix_unique,
                data_weights=self.mapper_list[0].data_unique_mappings.data_weights,
                pix_lengths=self.mapper_list[0].data_unique_mappings.pix_lengths,
                pix_pixels=self.mapper_list[0].pixels,
            )

        return block_diag(
            *[
                linear_eqn_util.curvature_matrix_via_w_tilde_curvature_preload_imaging_from(
                    curvature_preload=self.w_tilde.curvature_preload,
                    curvature_indexes=self.w_tilde.indexes,
                    curvature_lengths=self.w_tilde.lengths,
                    data_to_pix_unique=mapper.data_unique_mappings.data_to_pix_unique,
                    data_weights=mapper.data_unique_mappings.data_weights,
                    pix_lengths=mapper.data_unique_mappings.pix_lengths,
                    pix_pixels=mapper.pixels,
                )
                for mapper in self.mapper_list
            ]
        )

    @profile_func
    def curvature_matrix_off_diag_from(
        self, mapper_index_0, mapper_index_1
    ) -> np.ndarray:
        """
        Returns the off diagonal terms in the curvature matrix `F` (see Warren & Dye 2003) by computing them
        using `w_tilde_preload` (see `w_tilde_preload_interferometer_from`) for an imaging inversion.

        The `curvature_matrix` F is the second matrix, given by equation (4)
        in https://arxiv.org/pdf/astro-ph/0302587.pdf.

        This function computes the off-diagonal terms of F using the w_tilde formalism for the mapper of this
        `LinearEqn` and an input second mapper.
        """

        mapper_0 = self.mapper_list[mapper_index_0]
        mapper_1 = self.mapper_list[mapper_index_1]

        curvature_matrix_off_diag_0 = linear_eqn_util.curvature_matrix_off_diags_via_w_tilde_curvature_preload_imaging_from(
            curvature_preload=self.w_tilde.curvature_preload,
            curvature_indexes=self.w_tilde.indexes,
            curvature_lengths=self.w_tilde.lengths,
            data_to_pix_unique_0=mapper_0.data_unique_mappings.data_to_pix_unique,
            data_weights_0=mapper_0.data_unique_mappings.data_weights,
            pix_lengths_0=mapper_0.data_unique_mappings.pix_lengths,
            pix_pixels_0=mapper_0.pixels,
            data_to_pix_unique_1=mapper_1.data_unique_mappings.data_to_pix_unique,
            data_weights_1=mapper_1.data_unique_mappings.data_weights,
            pix_lengths_1=mapper_1.data_unique_mappings.pix_lengths,
            pix_pixels_1=mapper_1.pixels,
        )

        curvature_matrix_off_diag_1 = linear_eqn_util.curvature_matrix_off_diags_via_w_tilde_curvature_preload_imaging_from(
            curvature_preload=self.w_tilde.curvature_preload,
            curvature_indexes=self.w_tilde.indexes,
            curvature_lengths=self.w_tilde.lengths,
            data_to_pix_unique_0=mapper_1.data_unique_mappings.data_to_pix_unique,
            data_weights_0=mapper_1.data_unique_mappings.data_weights,
            pix_lengths_0=mapper_1.data_unique_mappings.pix_lengths,
            pix_pixels_0=mapper_1.pixels,
            data_to_pix_unique_1=mapper_0.data_unique_mappings.data_to_pix_unique,
            data_weights_1=mapper_0.data_unique_mappings.data_weights,
            pix_lengths_1=mapper_0.data_unique_mappings.pix_lengths,
            pix_pixels_1=mapper_0.pixels,
        )

        return curvature_matrix_off_diag_0 + curvature_matrix_off_diag_1.T

    @profile_func
    def mapped_reconstructed_data_of_mappers_from(
        self, reconstruction: np.ndarray
    ) -> List[Array2D]:
        """
        Using the reconstructed source pixel fluxes we map each source pixel flux back to the image plane and
        reconstruct the image data.

        This uses the unique mappings of every source pixel to image pixels, which is a quantity that is already
        computed when using the w-tilde formalism.

        Returns
        -------
        Array2D
            The reconstructed image data which the inversion fits.
        """

        mapped_reconstructed_image_of_mappers = []

        reconstruction_of_mappers = self.source_quantity_of_mappers_from(
            source_quantity=reconstruction
        )

        for mapper_index in range(self.total_mappers):

            mapper = self.mapper_list[mapper_index]
            reconstruction = reconstruction_of_mappers[mapper_index]

            mapped_reconstructed_image = linear_eqn_util.mapped_reconstructed_data_via_image_to_pix_unique_from(
                data_to_pix_unique=mapper.data_unique_mappings.data_to_pix_unique,
                data_weights=mapper.data_unique_mappings.data_weights,
                pix_lengths=mapper.data_unique_mappings.pix_lengths,
                reconstruction=reconstruction,
            )

            mapped_reconstructed_image = Array2D(
                array=mapped_reconstructed_image,
                mask=mapper.source_grid_slim.mask.mask_sub_1,
            )

            mapped_reconstructed_image = self.convolver.convolve_image_no_blurring(
                image=mapped_reconstructed_image
            )

            mapped_reconstructed_image_of_mappers.append(mapped_reconstructed_image)

        return mapped_reconstructed_image_of_mappers


class LinearEqnImagingMapping(AbstractLinearEqnImaging):
    def __init__(
        self,
        noise_map: Array2D,
        convolver: Convolver,
        mapper_list: List[Union[MapperRectangular, MapperVoronoi]],
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
        """

        super().__init__(
            noise_map=noise_map,
            convolver=convolver,
            mapper_list=mapper_list,
            profiling_dict=profiling_dict,
        )

    @profile_func
    def data_vector_from(self, data: Array2D) -> np.ndarray:
        """
        __Data Vector (D)__

        To solve for the source pixel fluxes we now pose the problem as a linear inversion which we use the NumPy
        linear  algebra libraries to solve. The linear algebra is based on the
        paper https://arxiv.org/pdf/astro-ph/0302587.pdf .

        This requires us to convert the blurred mapping matrix and our data / noise map into matrices of certain
        dimensions.

        The `data_vector` D is the first such matrix, which is given by equation (4)
        in https://arxiv.org/pdf/astro-ph/0302587.pdf.
        """
        return linear_eqn_util.data_vector_via_blurred_mapping_matrix_from(
            blurred_mapping_matrix=self.blurred_mapping_matrix,
            image=data,
            noise_map=self.noise_map,
        )

    @property
    @profile_func
    def curvature_matrix(self):
        """
        The `curvature_matrix` F is the second matrix, given by equation (4)
        in https://arxiv.org/pdf/astro-ph/0302587.pdf.

        This function computes F using the mapping matrix formalism, which is slower but must be used in circumstances
        where the noise-map is varying.

        The `curvature_matrix` computed here is overwritten in memory when the regularization matrix is added to it,
        because for large matrices this avoids overhead. For this reason, `curvature_matrix` is not a cached property
        to ensure if we access it after computing the `curvature_reg_matrix` it is correctly recalculated in a new
        array of memory.
        """
        return linear_eqn_util.curvature_matrix_via_mapping_matrix_from(
            mapping_matrix=self.operated_mapping_matrix, noise_map=self.noise_map
        )

    @profile_func
    def mapped_reconstructed_data_of_mappers_from(
        self, reconstruction: np.ndarray
    ) -> List[Array2D]:
        """
        Using the reconstructed source pixel fluxes we map each source pixel flux back to the image plane (via
        the blurred mapping_matrix) and reconstruct the image data.

        This uses the blurring mapping matrix which describes the PSF convolved mappings of flux between every
        source pixel and image pixels, which is a quantity that is already computed when using the mapping formalism.

        Returns
        -------
        Array2D
            The reconstructed image data which the inversion fits.
        """

        mapped_reconstructed_image_of_mappers = []

        reconstruction_of_mappers = self.source_quantity_of_mappers_from(
            source_quantity=reconstruction
        )

        for mapper_index in range(self.total_mappers):

            reconstruction = reconstruction_of_mappers[mapper_index]
            mapper = self.mapper_list[mapper_index]
            blurred_mapping_matrix = self.blurred_mapping_matrix_of_mapper(
                mapper_index=mapper_index
            )

            mapped_reconstructed_image = linear_eqn_util.mapped_reconstructed_data_via_mapping_matrix_from(
                mapping_matrix=blurred_mapping_matrix, reconstruction=reconstruction
            )

            mapped_reconstructed_image = Array2D(
                array=mapped_reconstructed_image,
                mask=mapper.source_grid_slim.mask.mask_sub_1,
            )

            mapped_reconstructed_image_of_mappers.append(mapped_reconstructed_image)

        return mapped_reconstructed_image_of_mappers
