from django import template

register = template.Library()

@register.filter(name='level_to_color')
def level_to_color(level):
    """
    Retourne une classe de couleur Bootstrap en fonction du niveau (1-5).
    """
    if level == 1:
        return 'danger'  # Rouge
    elif level == 2:
        return 'warning' # Orange
    elif level == 3:
        return 'info'    # Bleu clair
    elif level == 4:
        return 'primary' # Bleu
    elif level == 5:
        return 'success' # Vert
    return 'secondary' # Gris par défaut
