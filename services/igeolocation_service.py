class IGeoLocationService:
    def get_city_name_by_coordinates(self, lat, lng):
        """Método para obtener el nombre de la ciudad a partir de latitud y longitud."""
        raise NotImplementedError("Este método debe ser implementado por subclases.")
