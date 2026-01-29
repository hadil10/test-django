from .models import Job
SKILL_WEIGHT = 0.70  # 70% du score final vient des compétences
INTEREST_WEIGHT = 0.30 # 30% du score final vient des intérêts

def get_job_recommendations(profile):
    """
    Calcule un score de compatibilité pondéré (compétences + intérêts) pour chaque métier
    et retourne une liste de métiers recommandés, triés par score.
    """
    
    # 1. Récupérer les évaluations de l'utilisateur dans des dictionnaires pour un accès rapide
    user_skill_evals = {eval.skill.id: eval.level for eval in profile.skill_evaluations.all()}
    user_interest_evals = {eval.interest.id: eval.level for eval in profile.interest_evaluations.all()}
    
    # Si l'utilisateur n'a rien rempli, on ne peut rien recommander.
    if not user_skill_evals and not user_interest_evals:
        return []

    # 2. Récupérer tous les métiers avec leurs compétences et intérêts pré-chargés
    all_jobs = Job.objects.prefetch_related('required_skills', 'relevant_interests').all()
    
    job_scores = []

    # 3. Calculer le score pour chaque métier
    for job in all_jobs:
        # --- Calcul du score de compétences ---
        skill_score = 0
        required_skills = job.required_skills.all()
        if required_skills:
            total_skill_points = 0
            for r_skill in required_skills:
                total_skill_points += user_skill_evals.get(r_skill.id, 0)
            
            # Score moyen des compétences, normalisé sur 100
            skill_score = (total_skill_points / (len(required_skills) * 5)) * 100
        
        # --- Calcul du score d'intérêts ---
        interest_score = 0
        relevant_interests = job.relevant_interests.all()
        if relevant_interests:
            total_interest_points = 0
            for r_interest in relevant_interests:
                total_interest_points += user_interest_evals.get(r_interest.id, 0)
            
            # Score moyen des intérêts, normalisé sur 100
            interest_score = (total_interest_points / (len(relevant_interests) * 5)) * 100

        # --- Calcul du score final pondéré ---
        final_score = (skill_score * SKILL_WEIGHT) + (interest_score * INTEREST_WEIGHT)
        
        # On n'ajoute le métier que si son score est supérieur à zéro
        if final_score > 0:
            job_scores.append({
                'job': job,
                'score': round(final_score),
                'skill_score': round(skill_score), # Bonus: on garde les sous-scores
                'interest_score': round(interest_score) # Bonus: on garde les sous-scores
            })

    # 4. Trier les métiers par score final, du plus élevé au plus bas
    sorted_recommendations = sorted(job_scores, key=lambda x: x['score'], reverse=True)
    
    return sorted_recommendations
