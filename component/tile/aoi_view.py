from sepal_ui.aoi import AoiView
from sepal_ui.scripts import utils as su
from sepal_ui import color as sc
import ee

from component import parameter as cp


class AoiView(AoiView):
    """
    Extend the aoi_view component from sepal_ui.mapping to add
    the extra coloring parameter used in this application. To do so we were
    forced to copy/paste the _update_aoi
    """

    def __init__(self, **kwargs):

        # create the map
        super().__init__(methods=["ADMIN0"], **kwargs)

        # nest the tile
        self.elevation = False

        # change btn color
        self.btn.color = "secondary"

        # preselect country selection and prevent user to change
        self.w_method.readonly = True
        self.w_method.viz = False
        self.w_method.v_model = "ADMIN0"

    @su.loading_button(debug=True)
    def _update_aoi(self, widget, event, data):
        """
        extention of the original method that display information on the map.
        In the ee display we changed the display parameters. We also check if the aoi is the prototyped Uganda
        """

        # update the model
        self.model.set_object()

        if self.model.name.lower() != "uga":
            self.reset()
            self.w_method.v_model = "ADMIN0"
            self.w_admin_0.viz = True
            raise Exception(
                "This module is a prototype, only Uganda can be selected in the list"
            )

        # update the map
        if self.map_:
            [self.map_.remove_layer(lr) for lr in self.map_.layers if lr.name == "aoi"]
            self.map_.zoom_bounds(self.model.total_bounds())

            if self.ee:

                empty = ee.Image().byte()
                outline = empty.paint(
                    featureCollection=self.model.feature_collection, color=1, width=2
                )

                self.map_.addLayer(outline, {"palette": sc.primary}, "aoi")
            else:
                self.map_.add_layer(self.model.get_ipygeojson())

            self.map_.hide_dc()

        # tell the rest of the apps that the aoi have been updated
        self.updated += 1
