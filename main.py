import shutil
from PIL import Image
import requests
from io import BytesIO
import zlib
import gzip
import base64

# http://maps.google.com/cbk?output=tile&panoid=69qCKOuw4y-qzv4Pe3NGMg&zoom=3&x=0&y=0
# http://maps.google.com/cbk?output=xml&ll=48.013928,16.295161&dm=1


class Tile:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img


def main():
    zoom = 1
    cols = int(pow(2, zoom) - 1)
    rows = int(pow(2, zoom))
    url = 'http://maps.google.com/cbk?output=tile&panoid=69qCKOuw4y-qzv4Pe3NGMg'
    tile_array = []

    print("start downloading")
    for i in range(rows):
        for j in range(cols):
            tile_array.append(Tile(i, j, loadPanoTile(i, j, zoom, url)))

    print("start combining")

    combinePano(rows, cols, zoom, tile_array)


def loadPanoTile(row, col, zoom, pano_url):
    response = requests.get(pano_url + "&zoom=" + str(zoom) +
                            "&x=" + str(row) + "&y=" + str(col) + "", stream=True)
    img = Image.open(BytesIO(response.content))
    del response
    return img
    # with open("tmp/" + str(row) + "_" + str(col) + ".png", "wb") as out_file:
    # shutil.copyfileobj(response.raw, out_file)


def combinePano(rows, cols, zoom, tile_array):
    panowidth = 416 * pow(2, zoom)
    panoheight = (416 * pow(2, zoom - 1))
    out_img = Image.new('RGB', (panowidth, panoheight))

    for i in range(len(tile_array)):
        out_img.paste(tile_array[i].img,
                      (tile_array[i].x * 512, tile_array[i].y * 512))

    print("finished combining")
    # out_img.show()

    raw_depth = "eJzt2n1wFPUdx_FE4EgJCSEQkqAQE6AhEBJIQhByyd0FeTLj1CIoolShPFiUwWiLPMkKIwyg7ThYS3kuxYJTSAGdUkk2t-Ag0vJkpwwIwoAowhQqoAxgeLCXu0u4h9293dvH2-_n_QczXI65_d3rk83DkDAwLu6-uPiEOIQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIIYQQQgghhBBCCCGEEEIIySvZ6AtAhpaMAZDKZgv-ezIGQCdbY2lBDyVjAESy-UsLGgD8SWS7V1rQAJIxAOtnswX7Nw8gKSkZA7B6NluYv3cASY0lYwBWj88_Lckf_C1Ym8BsfP5JIf4YgJWKwh8DsFBR-KenN_3jlBQjLx2pkJh_mpC_dwEpjRl9-UhhUfqnp6TA3wpF9E-Cv5WDP-3gTzv40w7-tIM_7eBPO_jTDv60gz_tLO_fqZPRV2DqRPgt4d-zEwYgFgV_LEA4Gv6duhp9HWZNoX-20dcfqSb_rlgAb9L90-FvwZT6m30A8BdPsb-5B9Ab_uJJ90-GvwWDP-3gTzqxX__C3_rB3yz9hD-NXxX-ZknAX-MlwN_gWjUV0V-TFajgn5io8jWpmXn9W4UUJt3Cl7YrUMXfxAswpX8ovacWMlJzBir5m3YBZvOPXp3PX_kIFPpnN_ubdAEm8lcOz--vaAQq-ptyASbxV0le2D_aEajqb8IFGO-vKr3fv60vFTagsr_pFmCsv_r2Qf5CM5Bxhcr9H0pMNPECDPRX4Ts9af68K5B4kVH4pwf7h_KbawAG-Sv6-S46__ARSLlQLfzNtAAj_Hl-vDfEX8oEtPE3zwJ09-fDV3kAMvwjTkArf7MsQF9_IXwj_T116-a_vvZNNV9xtP6hv_4zZgBJrT2JPkOJ_wNNdfAl_mwRe-P9_QNoH5aG_joswOvvLTOT_xlq-t8r7KkR8I339w1AZ__ExCL_-5N6r9aiyRMK9Pelj3-HDg96ko5vAv_23YzwT0xMDc0Plpqa01iov-ehPt5iwN-bJHzC_kVFYQvwx-sfmG8IfQRkzeEvlZ-wf2Eh321Agr9_BE20meFfJeBP078p-MNfsn-XoHqFBX9L-AczB_h37hz4gc6heRbQt29f-GviH9X3f9H4e2S7e_Orwp-Wf_em4A9_-JvAv1DAPwf-8Ic__OEPf_jDX8A_E_5h_oIDgD_8hfxLS0tjz78P_GPeP1F3_7zm4N_sX1BQYH3_ODH_wAUI-Bdn3Qv-seAfxxOvv_9jPcLLzy_2lhWcoH_GvWLHv4DPvyCW_FsGltCUZH8e-EZ6AfzAMoSLFf-SAv6U-ncMLDc3N9w_NTVq_5biJQQl2z_fl7i9CH0M-ZcEFqA_YIBC_yB7T_cFFc8Tz___DXlGBHWRCTQPIYJ_fnNi9pHo5S3ASP9-PPnZIvonSfDnsxfyl5KcBfBOwF9ejx6h_vn5gfjK5GVtwBj__s3x6qvgL2SvxF_eAEQnEOCfHxw_vmx6T_6XMtw_SP6nIgV8yRbzT4vsL2yvyF_2AgQnEOAf8Gi-KvIhL9XOkwH-YXd7MXm1_YXtFfrLXwD_BPj9w4uevYk-IO39w5LzznZU5u-75WvuL38AfBOQ6h9xBIL_qJ1gevhH88Z2FMpm8_0Z4O99PNA_6I4v7q-MP7oFhG5Aln_QBiQ8V5j-Xvd7UnkIUbJH9g_egs2v35TPX_wzXl3_KBcQOAHZ_hKTQu-1D8t_MlmLiP5znTdJAwjMe8eXh6-Of5QDCNiA-v6S6Pnxxc-q6Iu6nOTK-274MvXV8VewgJaB_nrKR4WvZ9Ll5ZJr4K9kAZ4N9FQDXzq8AL5ab4U6SZBXBK-yv7IFiP56SF34WLBvTIReDXf1_RUOIOoNKMZX8S1QMeHPezX51fRXYQFRbcB69o1pcrfX2F-VBcgfQXT2Kp9c7bTh1tpfrQXIG4Fce9UPrUWxyR-v4gIkj8Bq9L5i1V_dBUiagRR6bY6qZTHrr8ECIsxAhF6rI-pQ7PprtQDBIYTJa3cyPYtdf40XEJaWJzGwGPbXdwHansS4YtlfzwVofRLDiml__Rag_UmMKrb99VqAHicxqBj3j9dlAjqdxJBinT9ehwXodxQjinn_eK0noOtR9M8C_vGaTkDvo-idJfw1XID-R9E3i_jHazUBQ46iY9bxbwz-crOWf7zqEzDyKLpkNf94dSdg8FG0z3r83uAvMYv6e4N_5Kzs7w3-olne3xfwBSLi7w_wodHyD4sad1jE_ckHf9qBn3bwpx38aQd_2sGfdvCnHfxpB37awZ928Kcd_GkHf9qBn3bwpx38aQd_2sGfdvCnHfhpB3_awZ928Kcd-GkHf9rBn3bwpx34aQd_4sGfdvCnHfhpB3_awZ924Kcd_GkHf9qBn3bwpx34aQd_2sGfduCnHfxpB37agZ948Kcd-GkHf9qBn3bgpx34aQd-2oGfeOCnHfhpB37agZ920Kcd-IkHfdpBn3bQJx70aQd82sGeeMCnHeiJB3niAZ52UEcIIYQQQgghhBBCyMLFhfToWzkbx9a_wU65wXCzl5U5d7bbUnfxL23ZrbcZ7mJ5mbPhydccJctS3bvGPmpfPPMZV9rRdXUXV6WUjzvKcAdujHBeHDjXkbu5wD18-Gj7qEPTXTuWFXCt7GXcS5Mul7W_Ve5ifj2bq_r6cXd-bW1dxuz_unpvWcTeKj5em-x5vQ2TKpwHbjOOK4cWDsw6n21_-dMXXdvZg3Uffsdwnxxabd-5bKHrdJsybvC-Am5I3O6yM_O_d1XNZxx9Fs-uz_pfif3yl6-43s0bwq0f3o2beWl52bDbVa52Df0d5xqKuaNF79vz8z5wbjj8IVs4_Xht1hWG-8fycufkMbO4J7-Z4n7eVlN3-m6567F-VyvGc-O52gvb7EVvpla-7Dn3p-ceKTtzLYcdN--U6_C7d-vTr7_mOJO3kV27Ja_yN-t-x75YsI9lzjLcDycGO48tGOGYfLgL9-ddf7KnP3vSWd2b4a7nbigfvmQQu7DhkrPL1n9XVM35FfdezTZ7Wm4f16vc5-yakr_aL5xguPMvjHF2W8Vwm4c8V79vQQpbeqJl5bGMCe4T62Y5ej62mX14z9TK5d_msjWXl9Yvm8RwY2ff7_xycoJj75oxjlk3i9kD9sLK9a1z2QlXGMfFnLXsMwOervzx2vPctC5HKqZ9vZQd_l5fV-mxlQMH17cpO_Ejw12Z6HK-MXqbe_XQlxwZv9_KbvmoZeUj5dmOBXuGchMLa-zu7XecR1Y-zX31dgtuSa8dg7ILTrrutp3h2Dr6txWLNi4p6_fVKef766rKF2xgHPMyV7Apa6oq90zIKL9x6Vbd9s8Y7nRelnPt68-xtmPL2T9-63l_ztqduW8trlj_fRY36osy7uyEjq6d50Y6rj3Q3vEztrju2TU3Kma805k7dafKUTPib-yxO3ddrz41zT3t5kxH5sHN7MFF0ypXrJjLTfmsR0X_AyPZcfPzXJ90_dj--oLddTMuMdwH2fnOxTmTuScePuN-54ebO1dlnXYV7v_IfvV6XP1_DjFc6aFxzjkr53DHZ9krarKfYvP21rqm7r_qzv3DeMee89vYkyMmVZ4_coB1TN3LDvuc4V75wuHcsYHh_rl1VPnSzkXsm7_Y57rQ-_FyR8PJurGbPHuv7ur8-dAJ7He_7O7euGkuN2j5cefRQfvZWZuesJd8w3DF1QnOef9aZ69_Ibt-9S6G6zW92jnzobfZ89W76_5-jeE-XpnldLebx1WPbChfO2gYO6nfRNf_Abx8Gdo"

    decoded = base64_decode(raw_depth)
    length = 512 * 512 + 5000

    try:
        json = zlib.decompress(decoded)
    except Exception as e:
        raise BadPayload('Could not zlib decompress the payload before '
                         'decoding the payload', original_error=e)
    print(json)


def base64_decode(string):
    """base64 decodes a single bytestring (and is tolerant to getting
    called with a unicode string).
    The result is also a bytestring.
    """
    string = want_bytes(string, encoding='ascii', errors='ignore')
    return base64.urlsafe_b64decode(string + b'=' * (-len(string) % 4))


def want_bytes(s, encoding='utf-8', errors='strict'):
    if isinstance(s, str):
        s = s.encode(encoding, errors)
    return s


if __name__ == '__main__':
    main()
