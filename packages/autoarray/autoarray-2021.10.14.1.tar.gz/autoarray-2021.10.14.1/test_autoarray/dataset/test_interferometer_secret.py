from os import path

import autoarray as aa

from autoarray.dataset.interferometer_secret import InterferometerSecret

from autoarray.operators import transformer

test_data_dir = path.join(
    "{}".format(path.dirname(path.realpath(__file__))), "files", "interferometer"
)


class TestInterferometer:
    def test__transformer_and_w_tilde(
        self,
        visibilities_7,
        visibilities_noise_map_7,
        uv_wavelengths_7x2,
        sub_mask_2d_7x7,
    ):
        interferometer_7 = InterferometerSecret(
            visibilities=visibilities_7,
            noise_map=visibilities_noise_map_7,
            uv_wavelengths=uv_wavelengths_7x2,
            real_space_mask=sub_mask_2d_7x7,
            settings=aa.SettingsInterferometer(
                transformer_class=transformer.TransformerDFT
            ),
        )

        assert type(interferometer_7.transformer) == transformer.TransformerDFT
        assert interferometer_7.w_tilde.curvature_preload[0][0] == 1.75

        interferometer_7 = aa.Interferometer(
            visibilities=visibilities_7,
            noise_map=visibilities_noise_map_7,
            uv_wavelengths=uv_wavelengths_7x2,
            real_space_mask=sub_mask_2d_7x7,
            settings=aa.SettingsInterferometer(
                transformer_class=transformer.TransformerNUFFT
            ),
        )

        assert type(interferometer_7.transformer) == transformer.TransformerNUFFT
