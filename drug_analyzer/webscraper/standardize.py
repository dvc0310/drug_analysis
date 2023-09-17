import json

def standardize_use_string(use_string, disease_aliases):
    standardized_string = use_string.lower()
    
    for canonical_name, aliases in disease_aliases.items():
        if standardized_string in [alias.lower() for alias in aliases]:
            return canonical_name

    return standardized_string

def remove_duplicates(uses_list):
    seen = set()
    return [x for x in uses_list if x.lower() not in seen and not seen.add(x.lower())]


def standardizer(json_file_path):
    # Read the JSON data from the file
    with open(json_file_path, "r") as file:
        data = json.load(file)

    disease_aliases = {
        'attention deficit hyperactivity disorder': ['adhd', 'attention deficit hyperactivity disorder (adhd)'],
        'major depression disorder' : ['depression','depression.','major depressive disorder (mdd)'],
        'acne' : ['acne vulgaris', 'moderate acne'],
        'panic disorder' : ['panic disorders'],
        'pain' : ['chronic pain', 'pain reliever', 'severe pain'],
        'restless legs syndrome (rls)' : ['restless leg syndrome', 'restless legs syndrome'],
        'paroxysmal nocturnal hemoglobinuria' : ['paroxysmal nocturnal hemoglobinuria (pnh)'],
        'ischemic stroke' : ['ischemic stroke, prophylaxis'],
        'birth control' : ['birth control pill'],
        'influenza virus' : ['influenza a', 'influenza'],
        'hypothyroidism' : ['hypothyroidism (low thyroid hormone)'],
        'hyperparathyroidism': ['hyperphosphatemia of renal failure'],
        'hypercalcemia' : ['hypercalcemia of malignancy'],
        'urinary tract infection' : ['urinary tract infections'],
        'ulcerative colitis (uc)' : ['ulcerative colitis'],
        'hiv' : ['immunodeficiency','hiv infection','hiv or aids','hiv-1', 'human immunodeficiency virus', 'human immunodeficiency virus (hiv)', 'human immunodeficiency virus-1 (hiv-1)' ],
        'benign prostatic hyperplasia' : ['benign prostatic hyperplasia (bph)', 'benign prostatic hypertrophy'],
        'asthma': ['asthma attacks', 'asthma, acute', 'asthma, maintenance', 'severe asthma'],
        'arthritis' : ['enthesitis-related arthritis', 'gouty arthritis', 'non-radiographic axial spondyloarthritis', 'osteoarthritis', 'osteoarthritis pain', 'psoriatic arthritis', 'rheumatoid arthritis'],
        'anxiety' : ['anxiety disorder', 'anxiety disorders', 'general anxiety disorder', 'social anxiety disorder (sad)'],
        'pulmonary embolism' : ['(pulmonary embolism)', 'pulmonary embolism, pe'],
        'angina' : ['(angina)','angina (chest pain)', 'angina attacks', 'angina pectoris prophylaxis'],
        'acquired immunodeficiency syndrome' :['aids'],
        'breast cancer' : ['breast', 'breast cancer, adjuvant', 'breast cancer cancer, adjuvant', 'breast cancer cancer, metastatic'],
        'bipolar disorder': ['bipolar i disorder'],
        'tonic-clonic seizures' : ['tonic-clonic'],
        'fever' : ['fevers'],
        'systemic lupus erythematosus' : ['systemic lupus erythematosus (sle)'],
        'gastroesophageal reflux disease' : ['gastroesophageal reflux disease (gerd)'],
        'fluid retention' : ['fluid retention (edema)'],
        'cough' : ['coughing'],
        'opioid addiction' : ['opiate dependence', 'opiate withdrawal'],
        'obesity' : ['obese'],
        'obsessive compulsive disorder' : ['obsessive-compulsive disorder', 'ocd'],
        'non-hodgkin lymphoma' : ['non-hodgkin\'s lymphoma'],
        'nerves' : ['nerve pain', 'nerve pain (neuralgia)', 'nerve pain (postherpetic neuralgia)'], 
        'weight management' : ['weight loss drug.','weight loss (obesity/overweight)', 'weight loss','fda approved weight loss drug.'  ],
        'excessive daytime sleepiness' : ['excessive sleepiness'],
        'erectile dysfunction (impotence)' : ['erectile dysfunction'],
        'diabetes': ['diabetic macular edema','type 2 diabetes mellitus', 'type 1 diabetes', 'diabetes, type 2', 'diabetes, type 1', 'diabetes mellitus','diabetes medicine','central diabetes insipidus'  ],
        'crohn\'s disease' : ['crohnâ€™s disease'],
        'high blood pressure' : ['high blood pressure (hypertension)'],
        'high blood cholesterol' : ['cholesterol','high cholesterol', 'high cholesterol, familial heterozygous','high cholesterol, familial homozygous' ],
        'hereditary angioedema' : ['hereditary angioedema (hae)'],
        'herpes' : ['herpes simplex, suppression', 'herpes zoster', 'herpes zoster, prophylaxis'],
        'hemophilia' : ['hemophilia b'],
        'deep vein thrombosis' : ['dvt','deep vein thrombosis (dvt)', 'dvt - deep vein thrombosis'],
        'chronic dry eye' :['dry eye disease'],
        'hemolytic uremic syndrome' : ['hemolytic uremic syndrome (ahus)'],
        'heart attack' : ['heart attacks'],
        'conjunctivitis' : ['conjunctivitis, allergic','conjunctivitis, bacterial' ],
        'common cold' :['cold symptoms','cold medicines'],
        'chronic obstructive pulmonary disease (copd)': ['chronic obstructive pulmonary disease','copd','copd (chronic obstructive pulmonary disease','copd (chronic obstructive pulmonary disease)','copd, acute' ],
        'migraine' : ['headache','chronic migraine','migraine headache','migraine headaches','migraine prevention','prevent episodic migraines'],
        'leukemia':['acute lymphoblastic leukemia','acute myeloid leukemia', 'acute myeloid leukemia (aml)', 'acute promyelocytic leukemia', 'chronic lymphocytic leukemia', 'chronic myelogenous leukemia', 'chronic myeloid leukemia' ],
        'kidney disease' : ['chronic kidney disease','kidney failure', 'kidney infections','kidney stones', 'kidneys'],
        'irritable bowel syndrome' : ['ibs','chronic irritable bowel syndrome'],
        'hives' : ['chronic hives','chronic urticaria (hives','chronic urticaria (hives)' ],
        'hepatitis': ['chronic hepatitis c', 'hepatitis b', 'hepatitis c'],
        'bronchitis': ['bronchospasm','chronic bronchitis'],
        'diarrhea' : ['carcinoid syndrome diarrhea', 'traveler\'s diarrhea'],
        'calcitonin gene-related peptide (cgrp) receptor blocker': ['cgrp','calcitonin-gene related peptide antagonist'],
        'shingles': ['"shingles.', 'shingles (herpes zoster)'] ,
        'anemia' : ['iron deficiency anemia', 'aplastic anemia', 'anemia associated with chronic renal failure'],
        'allergies' : ['nasal allergy symptoms','allergies.' 'allergy symptoms','allergic reactions', 'conjunctivitis, allergic','allergic rhinitis']
    }
    

    # Standardize the strings in the "uses list" for each drug and remove duplicates
    keys_to_remove = []
    for drug in data:
        if data[drug].get('link'):
            del data[drug]['link']
            
        if 'uses list' not in data[drug]:
            continue 
        else:
            data[drug]["uses list"] = [standardize_use_string(use, disease_aliases) for use in data[drug]["uses list"]]
            data[drug]["uses list"] = remove_duplicates(data[drug]["uses list"])
        
        # Remove drug entry if it has any missing value, empty "uses list", or empty "drug class list"
        if any(value is None or value == "N/A" for value in data[drug].values()) or \
        (not data[drug]["uses list"] or not data[drug]["drug class list"]):
            keys_to_remove.append(drug)

    # Remove the drug entries with missing values
    for key in keys_to_remove:
        del data[key]


    # Write the updated JSON data back to the file
    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)