import folium

class Map:

    GR_COORDS = [46.6651, 9.5705]
    MY_COORDS = [47.0417, 9.4168]
    ALG_COORDS = [46.8493, 9.5147]
    MY_IMAGE = "https://amberg-solutions.ch/static/img/kai_lanz.png"
    ALG_IMGAGE = "https://media.jobs.ch/media/5489689d-2524-4e99-a9db-9a75be8bffbd"
    MY_POPUP = f"""
    <div style="width: 270px; font-family: 'Montserrat', sans-serif; color: #17211b;">
        <img
            src="{MY_IMAGE}"
            alt="Kai Lanz"
            style="width: 50%; height: 100px; object-fit: cover; border-radius: 6px; display: block;"
        >
        <div style="padding: 14px 2px 4px;">
            <h3 style="margin: 0 0 6px; font-size: 20px; font-weight: 700;">Kai Lanz</h3>
            <p style="margin: 0 0 12px; color: #5d6962; font-size: 12px; font-weight: 600;">
                Messmerhölzli 41, 8887 Mels
            </p>
            <p style="margin: 0; font-size: 14px; line-height: 1.5;">
                Hier in Mels neben der Fabrik wohne ich.
            </p>
        </div>
    </div>
    """
    ALG_POPUP = f"""
    <div style="width: 270px; font-family: 'Montserrat', sans-serif; color: #17211b;">
        <img
            src="{ALG_IMGAGE}"
            alt="Amt für Landwirtschaft und Geoinformation"
            style="width: 50%; height: 100px; object-fit: cover; border-radius: 6px; display: block;"
        >
        <div style="padding: 14px 2px 4px;">
            <h3 style="margin: 0 0 6px; font-size: 20px; font-weight: 700;">Amt für Landwirtschaft und Geoinformation</h3>
            <p style="margin: 0 0 12px; color: #5d6962; font-size: 12px; font-weight: 600;">
                Ringstrasse 10, 7001 Chur
            </p>
            <p style="margin: 0; font-size: 14px; line-height: 1.5;">
                Hier sind Sie.
            </p>
        </div>
    </div>
    """

    @staticmethod
    def build_html_map(geo_data: list[dict], region: str = "all") -> str:

        m = folium.Map(location=Map.GR_COORDS, zoom_start=9, width="100%", height="100%")
        folium.Marker(Map.MY_COORDS, popup=Map.MY_POPUP, icon=folium.Icon("blue")).add_to(m)
        folium.Marker(Map.ALG_COORDS, popup=Map.ALG_POPUP, icon=folium.Icon("black")).add_to(m)

        for item in geo_data:
            name = item["name"]
            geometry = folium.GeoJson(
                data=item["geom"],
                tooltip=name
            )
            geometry.add_to(m)
            folium.Marker(item["point"], item["name"]).add_to(m)

        return m.get_root().render()


