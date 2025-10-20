#!/usr/bin/env python3
"""
Configuration module - Language priorities and config management
"""


def get_language_config(choice):
    """
    Returns configuration based on user's language priority choice
    Compatible with both old and new formats
    """
    configs = {
        '1': {
            'name': 'Spanish (Spain)',
            'regions': ['Spain', 'Europe', 'Japan'],
            'language_code': 'Es',
            'languages': ['Es'],
            'language_priority': ['Es', 'En'],
            'region_priority': ['Spain', 'Europe', 'Japan'],
            'priority': {'Spain': 1, 'Europe': 2, 'Japan': 3, 'Es': 4},
            'prefer_spanish': True
        },
        '2': {
            'name': 'English (Europe/USA)',
            'regions': ['Europe', 'USA', 'Japan'],
            'language_code': 'En',
            'languages': ['En'],
            'language_priority': ['En'],
            'region_priority': ['Europe', 'USA', 'Japan'],
            'priority': {'Europe': 1, 'USA': 2, 'Japan': 3, 'En': 4},
            'prefer_spanish': False
        },
        '3': {
            'name': 'French (France)',
            'regions': ['France', 'Europe', 'Japan'],
            'language_code': 'Fr',
            'languages': ['Fr', 'En'],
            'language_priority': ['Fr', 'En'],
            'region_priority': ['France', 'Europe', 'Japan'],
            'priority': {'France': 1, 'Europe': 2, 'Japan': 3, 'Fr': 4},
            'prefer_spanish': False
        },
        '4': {
            'name': 'German (Germany)',
            'regions': ['Germany', 'Europe', 'Japan'],
            'language_code': 'De',
            'languages': ['De', 'En'],
            'language_priority': ['De', 'En'],
            'region_priority': ['Germany', 'Europe', 'Japan'],
            'priority': {'Germany': 1, 'Europe': 2, 'Japan': 3, 'De': 4},
            'prefer_spanish': False
        },
        '5': {
            'name': 'Italian (Italy)',
            'regions': ['Italy', 'Europe', 'Japan'],
            'language_code': 'It',
            'languages': ['It', 'En'],
            'language_priority': ['It', 'En'],
            'region_priority': ['Italy', 'Europe', 'Japan'],
            'priority': {'Italy': 1, 'Europe': 2, 'Japan': 3, 'It': 4},
            'prefer_spanish': False
        },
        '6': {
            'name': 'Japanese (Japan)',
            'regions': ['Japan'],
            'language_code': None,
            'languages': [],
            'language_priority': [],
            'region_priority': ['Japan'],
            'priority': {'Japan': 1},
            'prefer_spanish': False
        }
    }
    
    return configs.get(choice, configs['1'])


def create_custom_config(user_priorities, analysis):
    """
    Creates a custom configuration based on user selections
    
    Args:
        user_priorities: dict with user's selections
        analysis: dict with available options analysis
    
    Returns:
        dict with custom configuration
    """
    config = {
        'name': 'Custom Configuration',
        'regions': user_priorities.get('regions', []),
        'languages': user_priorities.get('languages', []),
        'language_priority': user_priorities.get('language_priority', []),
        'region_priority': user_priorities.get('region_priority', []),
        'prefer_spanish': 'Spain' in user_priorities.get('regions', []),
        'include_demos': user_priorities.get('include_demos', False),
        'exclusive_only': user_priorities.get('exclusive_only', False),
        'priority_games': user_priorities.get('priority_games', {})
    }
    
    return config


def get_all_available_configs():
    """Returns a list of all predefined configurations"""
    return {
        'spain': get_language_config('1'),
        'europe': get_language_config('2'),
        'usa': get_language_config('3'),
        'japan': get_language_config('4'),
        'world': get_language_config('5')
    }
