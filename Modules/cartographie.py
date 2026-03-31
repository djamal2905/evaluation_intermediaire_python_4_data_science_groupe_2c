from cartiflette import carti_download
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.colors import LinearSegmentedColormap


class Cartographie:
    """
    Classe de gestion et visualisation de cartes électorales
    sur les départements français.

    Attributes
    ----------
    departement_borders : gpd.GeoDataFrame | None
        Contient les frontières des départements.
    """

    def __init__(self) -> None:
        """
        Initialise la classe sans données géographiques chargées.
        """
        self.departement_borders: gpd.GeoDataFrame | None = None

    def does_departement_borders_exist(self) -> bool:
        """
        Vérifie si les frontières des départements sont chargées.

        Returns
        -------
        bool
            True si les données existent, False sinon.
        """
        return self.departement_borders is not None

    def download_departement_borders(
        self,
        values: list[str] | None = None,
        crs: int = 4326,
        borders: str = "DEPARTEMENT",
        vectorfile_format: str = "geojson",
        simplification: int = 50,
        filter_by: str = "FRANCE_ENTIERE_DROM_RAPPROCHES",
        source: str = "EXPRESS-COG-CARTO-TERRITOIRE",
        year: int = 2022,
    ) -> None:
        """
        Télécharge les frontières des départements français.

        Parameters
        ----------
        values : list[str] | None
            Zones à télécharger.
        crs : int
            Système de coordonnées.
        borders : str
            Type de frontière.
        vectorfile_format : str
            Format du fichier.
        simplification : int
            Niveau de simplification géométrique.
        filter_by : str
            Filtre géographique.
        source : str
            Source des données.
        year : int
            Année des données.
        """
        if values is None:
            values = ["France"]

        if self.departement_borders is not None:
            print("Les frontières sont déjà chargées.")
            return

        try:
            self.departement_borders = carti_download(
                values=values,
                crs=crs,
                borders=borders,
                vectorfile_format=vectorfile_format,
                simplification=simplification,
                filter_by=filter_by,
                source=source,
                year=year,
            )
        except Exception as error:
            print(
                "Erreur lors du téléchargement des frontières : "
                f"{error}"
            )

    def afficher_resultats_filtre_candidat(
        self,
        df_score: pd.DataFrame,
        candidat: str = "Marine LE PEN",
        departement_code: str | None = None,
        afficher_carte: bool = False,
        fig_size: tuple[int, int] = (12, 14),
    ) -> None:
        """
        Filtre les résultats d'un candidat et affiche une carte.

        Parameters
        ----------
        df_score : pd.DataFrame
            Doit contenir :
            - code_departement
            - candidat
            - votes_departement
            - surrepresentation
        candidat : str
            Nom du candidat.
        departement_code : str | None
            Filtre sur un département.
        afficher_carte : bool
            Affiche la carte si True.
        fig_size : tuple[int, int]
            Taille de la figure matplotlib.
        """

        required_cols = [
            "code_departement",
            "candidat",
            "votes_departement",
            "surrepresentation",
        ]

        missing = [col for col in required_cols if col not in df_score.columns]
        if missing:
            raise ValueError(f"Colonnes manquantes : {missing}")

        df_candidat = df_score[
            df_score["candidat"].str.lower() == candidat.lower()
        ]

        if departement_code is not None:
            df_candidat = df_candidat[
                df_candidat["code_departement"] == departement_code
            ]

        if self.departement_borders is None:
            raise ValueError("Les frontières départementales ne sont pas chargées.")

        df_plot = self.departement_borders.merge(
            df_candidat,
            left_on="INSEE_DEP",
            right_on="code_departement",
            how="left",
        )

        fig, ax = plt.subplots(1, 1, figsize=fig_size)

        colors = ["#0CA8E6", "#FFFFFF", "#CD1039"]
        cmap = LinearSegmentedColormap.from_list("blue_pink", colors)

        df_plot.plot(
            column="surrepresentation",
            cmap=cmap,
            linewidth=0.8,
            edgecolor="black",
            vmin=df_candidat["surrepresentation"].min(),
            vmax=df_candidat["surrepresentation"].max(),
            legend=True,
            ax=ax,
            legend_kwds={
                "label": "",
                "orientation": "vertical",
                "shrink": 0.5,
            },
        )

        cbar = ax.get_figure().get_axes()[-1]
        cbar.text(
            0.5,
            1,
            "% par rapport à la moyenne nationale",
            ha="center",
            va="bottom",
            transform=cbar.transAxes,
        )

        ax.annotate(
            "N",
            xy=(0.95, 0.98),
            xytext=(0.95, 0.92),
            arrowprops=dict(facecolor="black", width=5, headwidth=15),
            ha="center",
            va="center",
            fontsize=14,
            xycoords=ax.transAxes,
        )

        scalebar = ScaleBar(
            1,
            units="m",
            dimension="si-length",
            location="lower right",
            pad=0.5,
            color="black",
            frameon=False,
        )
        ax.add_artist(scalebar)

        ax.set_axis_off()

        ax.set_title(
            f"Score du candidat {candidat} par département",
            fontsize=16,
        )

        if afficher_carte:
            plt.show()