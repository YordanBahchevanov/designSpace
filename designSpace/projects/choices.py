from django.db import models

class ProjectTypeChoice(models.TextChoices):
    RESIDENTIAL = 'residential', 'Residential Architecture'
    COMMERCIAL = 'commercial', 'Commercial Architecture'
    INSTITUTIONAL = 'institutional', 'Institutional Architecture'
    RELIGIOUS = 'religious', 'Religious Architecture'
    CULTURAL = 'cultural', 'Cultural Architecture'
    LANDSCAPE = 'landscape', 'Landscape Architecture'
    URBAN_DESIGN = 'urban_design', 'Urban Design'
    SUSTAINABLE = 'sustainable', 'Sustainable Architecture'
    TRANSPORTATION = 'transportation', 'Transportation Architecture'
    INTERIOR = 'interior', 'Interior Design'
    MODELING = 'modeling', '3D Modeling and Visualization'
    OTHER = "other", "Other"


