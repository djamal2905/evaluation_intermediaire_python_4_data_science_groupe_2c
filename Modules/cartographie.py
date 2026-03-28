from cartiflette import carti_download
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.colors import LinearSegmentedColormap


class Cartographie:
    """
    Classe pour gérer la cartographie des départements français et la visualisation
    des scores par candidat.

    Attributs
    ---------
    departement_borders : GeoDataFrame | None
        Contient les frontières des départements téléchargées.
    """

    def __init__(self) -> None:
        """Initialise une instance de Cartographie sans frontières de départements."""
        self.departement_borders: gpd.GeoDataFrame | None = None

    def does_departement_borders_exist(self) -> bool:
        """
        Vérifie si les frontières des départements ont été téléchargées.

        Returns
        -------
        bool
            True si les frontières existent, False sinon.
        """
        return self.departement_borders is not None

    def download_departement_borders(
        self,
        values: list[str] = ["France"],
        crs: int = 4326,
        borders: str = "DEPARTEMENT",
        vectorfile_format: str = "geojson",
        simplification: int = 50,
        filter_by: str = "FRANCE_ENTIERE_DROM_RAPPROCHES",
        source: str = "EXPRESS-COG-CARTO-TERRITOIRE",
        year: int = 2022,
    ) -> None:
        """
        Télécharge les frontières des départements français via Cartiflette.

        Paramètres
        ----------
        values : list[str], optional
            Liste de valeurs géographiques à télécharger (défaut ["France"]).
        crs : int, optional
            Système de coordonnées (défaut 4326).
        borders : str, optional
            Type de frontière à récupérer (défaut "DEPARTEMENT").
        vectorfile_format : str, optional
            Format du fichier vectoriel (défaut "geojson").
        simplification : int, optional
            Pourcentage de simplification géométrique (défaut 50).
        filter_by : str, optional
            Filtre sur la zone géographique (défaut "FRANCE_ENTIERE_DROM_RAPPROCHES").
        source : str, optional
            Source du téléchargement (défaut "EXPRESS-COG-CARTO-TERRITOIRE").
        year : int, optional
            Année des données (défaut 2022).

        Returns
        -------
        None
        """
        if not self.does_departement_borders_exist():
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
            except Exception as e:
                print(
                    "Une erreur s'est produite lors du téléchargement "
                    f"des frontières des départements: {e}"
                )
        else:
            print("Les frontières des départements ont déjà été téléchargées.")

    def afficher_resultats_filtre_score_candidat(
        self,
        df_score: pd.DataFrame,
        candidat: str = "Marine LE PEN",
        departement_code: str | None = None,
        afficher_carte: bool = False,
        figSize: tuple[int, int] = (12, 14),
    ):
        """
        Filtre les scores d'un candidat par département et trace la carte.

        Paramètres
        ----------
        df_score : pd.DataFrame
            DataFrame contenant les colonnes ['code_departement', 'candidat',
            'votes_departement', 'score_departement'].
        candidat : str, optional
            Nom du candidat à filtrer (défaut "Marine LE PEN").
        departement_code : str | None, optional
            Code département à filtrer, None pour tous les départements (défaut None).
        afficher_carte : bool, optional
            True pour afficher la carte après génération (défaut False).
        figSize : tuple[int, int], optional
            Taille de la figure matplotlib (défaut (12, 14)).
        """
        # Vérifier que toutes les colonnes nécessaires sont présentes
        required_cols = [
            "code_departement",
            "candidat",
            "votes_departement",
            "score_departement",
        ]
        if not all(col in df_score.columns for col in required_cols):
            raise ValueError(
                f"Le DataFrame df_score doit contenir les colonnes {required_cols}"
            )

        # Filtrer par candidat (insensible à la casse)
        df_candidat = df_score[df_score["candidat"].str.lower() == candidat.lower()]

        # Filtrer par département si fourni
        if departement_code is not None:
            df_candidat = df_candidat[
                df_candidat["code_departement"] == departement_code
            ]

        # Merge avec les frontières
        df_plot = self.departement_borders.merge(
            df_candidat, right_on="code_departement", left_on="INSEE_DEP", how="left"
        )

        # Création figure
        fig, ax = plt.subplots(1, 1, figsize=figSize)

        # Colormap bleu ciel -> blanc -> rose foncé
        colors = ["#0CA8E6", "#FFFFFF", "#CD1039"]
        cmap = LinearSegmentedColormap.from_list("blue_pink", colors)

        # Tracé
        df_plot.plot(
            column="score_departement",
            cmap=cmap,
            linewidth=0.8,
            edgecolor="black",
            legend=True,
            ax=ax,
            legend_kwds={"label": "", "orientation": "vertical", "shrink": 0.5},
        )

        # Colorbar
        cbar = ax.get_figure().get_axes()[-1]
        cbar.text(
            x=0.5,
            y=1,
            s="% par rapport à la moyenne nationale",
            ha="center",
            va="bottom",
            transform=cbar.transAxes,
        )

        # Flèche du Nord
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

        # Échelle
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

        # Supprimer axes
        ax.set_axis_off()

        # Titre
        ax.set_title(
            f"Score obtenu par le.a candidat.e {candidat} par département", fontsize=16
        )

        # Afficher la carte si demandé
        if afficher_carte:
            plt.show()
