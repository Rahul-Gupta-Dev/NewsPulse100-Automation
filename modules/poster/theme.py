"""
NewsPulse100 Theme Engine
"""

THEMES = {

    "Politics": {
        "primary": (225, 0, 0),
        "secondary": (255, 205, 0),
        "headline": (255, 255, 255),
        "summary": (235, 235, 235),
        "footer": (12, 12, 12),
        "gradient": 0.72,
        "accent": (255, 0, 0),
        "badge": "BREAKING NEWS"
    },

    "Business": {
        "primary": (0, 82, 204),
        "secondary": (255, 205, 0),
        "headline": (255,255,255),
        "summary": (240,240,240),
        "footer": (10,18,35),
        "gradient": 0.68,
        "accent": (0,140,255),
        "badge": "BUSINESS"
    },

    "Jobs": {
        "primary": (0,140,70),
        "secondary": (255,220,0),
        "headline": (255,255,255),
        "summary": (235,235,235),
        "footer": (10,30,15),
        "gradient": 0.70,
        "accent": (0,255,120),
        "badge": "JOB ALERT"
    },

    "Students": {
        "primary": (115,45,180),
        "secondary": (255,220,0),
        "headline": (255,255,255),
        "summary": (235,235,235),
        "footer": (30,15,45),
        "gradient": 0.70,
        "accent": (180,100,255),
        "badge": "STUDENT NEWS"
    },

    "Agriculture": {
        "primary": (34,120,34),
        "secondary": (255,220,0),
        "headline": (255,255,255),
        "summary": (235,235,235),
        "footer": (12,40,12),
        "gradient": 0.72,
        "accent": (40,220,40),
        "badge": "AGRICULTURE"
    }

}


def get_theme(category):

    return THEMES.get(
        category,
        THEMES["Politics"]
    )