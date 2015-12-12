from math import ceil
import requests

__author__ = 'dbotha'

import json
CM_TO_INCHES_RATIO = 1 / 2.54
PRINT_DPI = 300
API_KEY = "2778e89d274cf8ecbbad3fbba180cc5e62d0997c"

# GROUPS AND PRODUCT ORDERING IN THIS NEXT LIST DRIVES OUTPUT TABLES
PRODUCT_ORDER = [
    # Print Products
    ("OPTIMAL PRINT PRODUCT ASSET DIMENSIONS", [
        "a1_poster",
        "a2_poster",
        "a3_poster",
        "a4_poster",
        "photos_4x6",
        "magnets",
        "squares",
        "squares_mini",
        "polaroids",
        "polaroids_mini",
        "greeting_cards",
        "greeting_cards_a5",
        "greeting_cards_7x5",
        "stickers_square",
        "stickers_circle",
        "frames_50cm",
        "postcard"
        #"a2_poster_24",
        #"a1_poster_70",
        #"frames_50cm_4x4",
        #"frames_50cm_3x3",
        #"a2_poster_54",
        #"a5_flyer_500",
        #"greeting_cards_a5_10pack",
        #"greeting_cards_7x5_10pack",
        #"a2_poster_35",
        #"a1_poster_54",
        #"a1_poster_35",
        #"a5_flyer_1000",
        #"frames_50cm_2x2",
    ]),

    # WOYC
    ("OPTIMAL PHONE CASE ASSET DIMENSIONS", [
        "i6splus_tough_case",
        "i6splus_case",
        "i6s_case",
        "i6s_tough_case",

        "i6plus_tough_case",
        "i6plus_case",
        "i6plus_folio_case",
        "i6_tough_case",
        "i6_case",
        "i6_folio_case",
        "i6_bakpak_1_case",
        "i6_bakpak_3_case",

        "i5_tough_case",
        "i5_case",
        "i5_clik_case",

        "i5c_tough_case",
        "i5c_case",

        "i4_tough_case",
        "i4_case",

        "samsung_s6e_tough_case",
        "samsung_s6e_case",

        "samsung_s6_tough_case",
        "samsung_s6_case",

        "samsung_s5_tough_case",
        "samsung_s5_case",
        "samsung_s5_mini_case",

        "samsung_s4_tough_case",
        "samsung_s4_case",
        "samsung_s4_mini_tough_case",
        "samsung_s4_mini_case",

        "samsung_s3_tough_case",
        "samsung_s3_case",

        "samsung_s3_mini_case",

        "samsung_n4_tough_case",
        "samsung_n4_case",
        "samsung_n3_case",

        "sony_x_z1_case",
        "sony_x_c_case",

        "lg_g2_case",
        "moto_g_case",
        "nexus_5_case",
    ]),

    ("OPTIMAL TABLET CASE DIMENSIONS", [
        "ipad_mini_case",
        "ipad_case",
        "ipad_air_case",
        "nexus_7_case",
    ]),

    # Apparel
    ("OPTIMAL APPAREL ASSET DIMENSIONS", [
        #"gildan_hoodie",
        #"gildan_hoodie_zipped",
        #"gildan_tshirt"
    ]),

    # Photo Books

    # RPI Products
    ("OPTIMAL PHOTOBOOK ASSET DIMENSIONS", [
        # "photobook_small_landscape",
        # "photobook_small_portrait",
        "rpi_wrap_321x270_sm",
        "rpi_wrap_210x280_sm",
        "rpi_wrap_280x210_sm_40pg",
        "rpi_wrap_280x210_sm",
        "rpi_wrap_280x210_sm_100pg",
        "rpi_wrap_300x300_sm",
        "rpi_wrap_210x210_sm",
        "rpi_soft_210x210_s",
        "rpi_wrap_140x140_sm",
        "rpi_soft_280x210_s",
        "rpi_soft_210x280_s"
    ]),

    # Photobox Products
    ("OPTIMAL PHOTOBOX ASSET DIMENSIONS", [
        "i6ptc7",
        "i6cc7",
        "i5c4",
        "iphone5c1",
        "i5ccc1",
        "stickeri5c1",
        "i4c9",
        "i4ccc1",
        "stickeri4c1",
        "sgs5c1",
        "sgs4c3",
        "sgs3c4",
        "sgs2c1",

        "ipad_case_1",
        "ipadminic1",
        "ipadsmartc6",
        "ipadminismartc1",

        "pbx_canvas_20x30",
        "pbx_canvas_30x20",
        "pbx_canvas_30x30",
        "pbx_canvas_40x40",
        "pbx_polaroids_12",
        "pbx_polaroids_24",
        "pbx_polaroids_36",

        "pbx_a3",
        "pbx_6x4",
        "pbx_7x5",
        "pbx_squares_5x5",
        "pbx_squares_8x8",
        "pbx_magnets_8x8",
        "pbx_magnets_13x9",
        "pbx_magnets_15x10",
        "pbx_stickers_13x9",
        "pbx_cards_a6_10pack",

        "mgth10",
        "mug_bone_wrap",

        "pbx_frame_30x30",
        "pbx_canvas_30x40",
        "23540-3mbook_1"
    ]),

    # S9 Products
    ("OPTIMAL STICKY9 ASSET DIMENSIONS", [
        # "s9_polaroids_12",
        # "s9_magnets",
        # "s9_magnets_mini",
        # "s9_squares",
        # "s9_squares_single",
        # "s9_squares_mini_single",
        # "s9_poster",
        # "s9_greetingcard",
        # #"s9_packframe",
        # "s9_jigsaw",
        # "s9_squares_mini"
    ]),

    # Albumprinter Products
    ("OPTIMAL ALBELLI ASSET DIMENSIONS", [
        "ap_aluminium_400x400",
        "ap_aluminium_300x400",
        "ap_aluminium_400x300",
        "ap_mounted_400x400",
        "ap_mounted_400x300",
        "ap_mounted_300x400",
        "ap_canvas_400x300",
        "ap_canvas_300x400",
        "ap_canvas_400x400",
        "ap_wood_400x300",
        "ap_wood_300x400",
        "ap_wood_400x400",
        "ap_acrylic_300x400",
        "ap_acrylic_400x300",
        "ap_acrylic_400x400",
        "ap_album_210x210",
        "metallic_8x8"
    ])
]

url = 'https://api.kite.ly/v2.0/template/?limit=200'
headers = {'Authorization': ('ApiKey %s:' % API_KEY)}

r = requests.get(url, headers=headers)
r_json = r.json()

def get_dimension_safe(size, unit, side, default):
    if not size.get(unit, False):
        return default

    return size.get(unit).get(side, default)

def calculate_sensible_sizes(size):
    width_px = get_dimension_safe(size, "px", "width", 0)
    height_px = get_dimension_safe(size, "px", "height", 0)
    width_cm = get_dimension_safe(size, "cm", "width", 0)
    height_cm = get_dimension_safe(size, "cm", "height", 0)
    width_inch = get_dimension_safe(size, "inch", "width", 0)
    height_inch = get_dimension_safe(size, "inch", "height", 0)

    # convert cm & inches into px @ 300dpi then go with the largest
    width_cm_in_px = width_cm * CM_TO_INCHES_RATIO * PRINT_DPI
    height_cm_in_px = height_cm * CM_TO_INCHES_RATIO * PRINT_DPI
    width_inch_in_px = width_inch * PRINT_DPI
    height_inch_in_px = height_inch * PRINT_DPI

    base_width_px = width_inch_in_px
    base_height_px = height_inch_in_px
    base_area_px = base_width_px * base_height_px

    ROUNDING_ERROR_FUDGE_FACTOR_PX = 2 # Favour using pixels as they're likely "pretty" as rounding errors may have bumped inch_px or cm_px slightly larger
    if (width_px + ROUNDING_ERROR_FUDGE_FACTOR_PX) * (height_px + ROUNDING_ERROR_FUDGE_FACTOR_PX) > base_area_px:
        base_width_px = width_px
        base_height_px = height_px
        base_area_px = (width_px + ROUNDING_ERROR_FUDGE_FACTOR_PX) * (height_px + ROUNDING_ERROR_FUDGE_FACTOR_PX)

    if width_cm_in_px * height_inch_in_px > base_area_px:
        base_width_px = width_cm_in_px
        base_height_px = height_cm_in_px

    if base_width_px < 500 or base_height_px < 500:
        return 0, 0, 0, 0, 0, 0

    base_width_px = ceil(base_width_px)
    base_height_px = ceil(base_height_px)

    return (base_width_px, base_height_px,
            (base_width_px / PRINT_DPI) / CM_TO_INCHES_RATIO, (base_height_px / PRINT_DPI) / CM_TO_INCHES_RATIO,
            base_width_px / PRINT_DPI, base_height_px / PRINT_DPI)

def fn(num):
    return format(num, '.1f').rstrip('0').rstrip('.')

def find_product_with_template_id(products, template_id):
    for product in products:
        if product["template_id"] == template_id:
            return product

for (group_name, templates) in PRODUCT_ORDER:
    if len(templates) == 0:
        continue

    print("### %s" % group_name)
    print('<table class="apparel-positions"><thead><tr><th>product</th><th>pixels</th><th>cm</th><th>inches</th></tr></thead><tbody>')
    for template_id in templates:
        product = find_product_with_template_id(r_json["objects"], template_id)
        name = product["name"]
        template_id = product["template_id"]

        size = product["product"]["size"]
        (width_px, height_px, width_cm, height_cm, width_inch, height_inch) = calculate_sensible_sizes(size)

        print('<tr><td>%s<span class="optional-argument">%s</span></td><td><code class="prettyprint">%s&times;%s</code></td><td><code class="prettyprint">%s&times;%s</code></td><td><code class="prettyprint">%s&times;%s</code></td></tr>' % (name, template_id, fn(width_px), fn(height_px), fn(width_cm), fn(height_cm), fn(width_inch), fn(height_inch)))

    print("</tbody></table>")
    print("")

