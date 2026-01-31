
from companies.models import JobOffer

SKILL_WEIGHT = 0.70 
INTEREST_WEIGHT = 0.30 

def get_job_recommendations(profile):
    """
    Calcule un score de compatibilité pondéré pour chaque OFFRE D'EMPLOI
    et retourne une liste d'offres recommandées, triées par score.
    """
    user_skill_evals = {eval.skill.id: eval.level for eval in profile.skill_evaluations.all()}
 
    user_interest_evals = {eval.interest.id: eval.level for eval in profile.interest_evaluations.all()}
    
    if not user_skill_evals:
        return []


    all_offers = JobOffer.objects.filter(is_active=True).prefetch_related('required_skills').all()
    
    offer_scores = []

    for offer in all_offers:

        skill_score = 0
        required_skills = offer.required_skills.all()
        if required_skills:
            total_skill_points = 0
            for r_skill in required_skills:
                total_skill_points += user_skill_evals.get(r_skill.id, 0)
            
            # Normalisation du score sur 100
            skill_score = (total_skill_points / (len(required_skills) * 5)) * 100
        

        interest_score = 0


        final_score = (skill_score * SKILL_WEIGHT) + (interest_score * INTEREST_WEIGHT)
        
        if final_score > 20: 
            offer_scores.append({
                'offer': offer, 
                'score': round(final_score),
                'skill_score': round(skill_score), 
                'interest_score': round(interest_score) 
            })


    sorted_recommendations = sorted(offer_scores, key=lambda x: x['score'], reverse=True)
    
    return sorted_recommendations
