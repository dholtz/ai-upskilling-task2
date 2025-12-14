# Models module for data structures and ML models
from .database import db, init_db
from .tables import PresentationFile, PresentationSlide, SlideUrl

__all__ = ['db', 'init_db', 'PresentationFile', 'PresentationSlide', 'SlideUrl']
