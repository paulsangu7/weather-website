# utils/geocode.py

def get_lat_lon(location):
    """Return lat, lon for a given city/country."""
    location_map = {
        "Dar es Salaam": (-6.7924, 39.2083),
        "Nairobi": (-1.286389, 36.817223),
        "Tanzania": (-6.369028, 34.888822),
        "Kenya": (0.0236, 37.9062)
    }
    return location_map.get(location.title(), (None, None))
