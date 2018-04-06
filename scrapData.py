from bs4 import BeautifulSoup
import requests
import re
import os
from copy import deepcopy

dlink = re.compile(r'(.*)\"(.*)\"(.*)')
nline = re.compile(r'(.*)\n')

diseaseList = ["Rubella", "Shoulder Pain", "Foodborne Diseases", "Dermatitis, Exfoliative", "Milk Hypersensitivity", "Central Nervous System Protozoal Infections", "Arterio-Arterial Fistula", "46, XY Disorders of Sex Development", "Shaken Baby Syndrome", "Dientamoebiasis", "Blepharitis", "Cestode Infections", "Mouth Breathing", "Peste-des-Petits-Ruminants", "Porphyria Cutanea Tarda", "Self Mutilation", "Brain Death", "Decerebrate State", "Autolysis", "Heart Aneurysm", "Facial Pain", "Pseudomyxoma Peritonei", "Pasteurellosis, Pneumonic", "Bronchogenic Cyst", "Carcinoma, Brown-Pearce", "Pelvic Organ Prolapse", "Causalgia", "Marburg Virus Disease", "Amebiasis", "Polyradiculopathy", "Maxillary Sinus Neoplasms", "Keratosis, Actinic", "Bone Cysts, Aneurysmal", "Pleural Effusion, Malignant", "Hepatitis D, Chronic", "Tracheal Diseases", "Afferent Loop Syndrome", "Rheumatic Nodule", "Taeniasis", "Neoplasms, Neuroepithelial", "Nephrosclerosis", "Gram-Positive Bacterial Infections", "Encephalomyelitis", "Hydrocephalus, Normal Pressure", "Murine Acquired Immunodeficiency Syndrome", "Empyema", "Hepatopulmonary Syndrome", "Pulmonary Atresia", "Frostbite", "Endolymphatic Hydrops", "Skin Diseases, Metabolic", "Erythroblastosis, Fetal", "Pemphigus", "Oligohydramnios", "Pycnodysostosis", "Hyperkeratosis, Epidermolytic", "Pregnancy, Prolonged", "Lichenoid Eruptions", "Chickenpox", "Epstein-Barr Virus Infections", "Delirium", "Mucopolysaccharidosis VII", "Osteolysis, Essential", "Factitious Disorders", "Reye Syndrome", "Sprue, Tropical", "Schistosomiasis haematobia", "Ornithine Carbamoyltransferase Deficiency Disease", "Metrorrhagia", "Meige Syndrome", "Post-Concussion Syndrome", "Chondromatosis", "Embryo Loss", "Lymphatic Abnormalities", "Oligodendroglioma", "Scleromyxedema", "Limbic Encephalitis", "Pancreatitis, Alcoholic", "Brain Hemorrhage, Traumatic", "Hearing Loss, Central", "Sensation Disorders", "Encephalitis, California", "Subclavian Steal Syndrome", "Odontoma", "Odontogenic Cysts", "Chagas Disease", "Sialic Acid Storage Disease", "Lateral Medullary Syndrome", "Retinopathy of Prematurity", "Systemic Inflammatory Response Syndrome", "Protein-Energy Malnutrition", "Subphrenic Abscess", "Hyperostosis, Sternocostoclavicular", "Foot Injuries", "Discrete Subaortic Stenosis", "Hermanski-Pudlak Syndrome", "Leprosy, Borderline", "Toothache", "Mucormycosis", "Hyperphosphatemia", "Binge-Eating Disorder", "Vulvar Vestibulitis", "Critical Illness", "Uveitis, Suppurative", "Opportunistic Infections", "Heart Septal Defects", "Central Nervous System Infections", "Cystinuria", "Marijuana Abuse", "Cicatrix, Hypertrophic", "Hepatitis D", "Lymphangioma", "Gait Apraxia", "Glossopharyngeal Nerve Diseases", "Border Disease", "Endomyocardial Fibrosis", "Bile Reflux", "Common Bile Duct Neoplasms", "Croup", "Dyspareunia", "Schistosomiasis japonica", "Urethral Neoplasms", "Arbovirus Infections", "Polyradiculoneuropathy", "Histiocytic Sarcoma", "Steatorrhea", "Hydroa Vacciniforme", "Giardiasis", "Whiplash Injuries", "Laboratory Infection", "Fractures, Ununited", "Intestinal Obstruction", "Meningitis, Pneumococcal", "Intracranial Hemorrhage, Traumatic", "Biliary Tract Neoplasms", "Vulvitis", "Agraphia", "Encephalitis, Tick-Borne", "Gastroenteritis", "Hemostatic Disorders", "Placenta, Retained", "Uterine Cervical Dysplasia", "Hand, Foot and Mouth Disease", "Tracheal Stenosis", "Mycotoxicosis", "Mercury Poisoning", "Ainhum", "Takayasu Arteritis", "Ganglioneuroma", "Lymphangiomyoma", "Panniculitis, Lupus Erythematosus", "Tinea Versicolor", "Primary Progressive Nonfluent Aphasia", "Eosinophilic Esophagitis", "Hernia, Ventral", "Otitis Media, Suppurative", "Tachycardia, Paroxysmal", "Mongolian Spot", "Jaundice, Neonatal", "Coma", "Rare Diseases", "Neoplasms, Complex and Mixed", "Colloid Cysts", "Abortion, Threatened", "Landau-Kleffner Syndrome", "Heavy Metal Poisoning, Nervous System", "Carcinoma, Lobular", "Hyperglycemic Hyperosmolar Nonketotic Coma", "Equinus Deformity", "Iris Neoplasms", "Lichen Sclerosus et Atrophicus", "Gastric Fistula", "Adenoma, Acidophil", "Enzootic Bovine Leukosis", "Ureterolithiasis", "Infant Nutrition Disorders", "Sleep Deprivation", "Tracheobronchomalacia", "Cat-Scratch Disease", "Peliosis Hepatis", "Pemphigoid, Bullous", "Jaundice, Chronic Idiopathic", "Pneumonia, Lipid", "Hematoma, Epidural, Cranial", "Elephantiasis", "Trench Fever", "Trichomonas Vaginitis", "Leukemia P388", "Breech Presentation", "Chylous Ascites", "Epidermodysplasia Verruciformis", "Phimosis", "Peripheral Nervous System Neoplasms", "Common Cold", "Reflex Sympathetic Dystrophy", "Ephemeral Fever", "Emergencies", "Brain Stem Neoplasms", "Catastrophic Illness", "Posterior Tibial Tendon Dysfunction", "Ecthyma", "Pain, Referred", "Hematoma, Subdural, Acute", "Echovirus Infections", "Pregnancy, Tubal", "Cholesteatoma, Middle Ear", "Thyroid Nodule", "Jaundice", "Biliary Dyskinesia", "Hepatitis, Autoimmune", "Wallerian Degeneration", "Arterivirus Infections", "Bacteroides Infections", "Endocarditis", "Fibrous Dysplasia, Monostotic", "Piriformis Muscle Syndrome", "Cryptogenic Organizing Pneumonia", "Sweat Gland Neoplasms", "Leber Congenital Amaurosis", "Trisomy", "Neuroaspergillosis", "Melena", "Activated Protein C Resistance", "Erythrokeratodermia Variabilis", "Insulin Coma", "Actinomycosis", "Abdominal Abscess", "Trigeminal Neuralgia", "Fractures, Compression", "Sarcoma, Yoshida", "Inappropriate ADH Syndrome", "Coronavirus Infections", "Prehypertension", "Epidermolysis Bullosa, Junctional", "Mitral Valve Stenosis", "Radiation Injuries, Experimental", "Thymus Hyperplasia", "Corneal Neovascularization", "Complex Regional Pain Syndromes", "Extravasation of Diagnostic and Therapeutic Materials", "Prosopagnosia", "Coronary Vessel Anomalies", "Lead Poisoning, Nervous System, Adult", "Consciousness Disorders", "Bovine Virus Diarrhea-Mucosal Disease", "Scleroderma, Diffuse", "Melkersson-Rosenthal Syndrome", "Herpes Zoster", "Hematoma, Subdural, Intracranial", "Turner Syndrome", "Uterine Perforation", "Dumping Syndrome", "Rupture, Spontaneous", "Aniseikonia", "Lupus Erythematosus, Discoid", "Hookworm Infections", "Abortion, Veterinary", "Scabies", "Cholesteatoma", "Foot Ulcer", "Neoplasms, Post-Traumatic", "Paraneoplastic Syndromes", "Cerebral Ventricle Neoplasms", "Hydranencephaly", "Kearns-Sayre Syndrome", "Neck Injuries", "Mixed Tumor, Mesodermal", "Postpericardiotomy Syndrome", "Oral Manifestations", "Abortion, Septic", "Ascorbic Acid Deficiency", "Panniculitis", "Borrelia Infections", "Bladder Exstrophy", "Hypertension, Renovascular", "Intussusception", "Pericarditis, Constrictive", "Graft Occlusion, Vascular", "Penile Induration", "Leukocyte-Adhesion Deficiency Syndrome", "Meningitis, Listeria", "Bronchiolitis, Viral", "Lung Diseases, Parasitic", "Vulvovaginitis", "Osteopoikilosis", "Carcinoma, Adenosquamous", "Plague", "Lipodystrophy, Congenital Generalized", "Lacrimal Duct Obstruction", "Adenoma, Bile Duct", "Erythema Induratum", "Mesenteric Lymphadenitis", "Central Nervous System Fungal Infections", "Jaw Abnormalities", "Schizophrenia, Paranoid", "Labyrinth Diseases", "Hemorrhagic Fever, American", "Intermittent Claudication", "Muscular Disorders, Atrophic", "Postphlebitic Syndrome", "Paralysis, Hyperkalemic Periodic", "Ascaridiasis", "Optic Disk Drusen", "Microscopic Polyangiitis", "Carbamoyl-Phosphate Synthase I Deficiency Disease", "Hyperlysinemias", "Spina Bifida Occulta", "Sarcopenia", "Duodenitis", "Wheat Hypersensitivity", "Conjunctivitis, Allergic", "Liver Abscess", "Rectocele", "Reflex, Babinski", "Hypothalamic Neoplasms", "Pharyngeal Diseases", "Lymphangitis", "Glaucoma, Angle-Closure", "Gingival Neoplasms", "Trichostrongylosis", "Pulmonary Heart Disease", "Periodontal Attachment Loss", "Demyelinating Autoimmune Diseases, CNS", "Choriocarcinoma", "Coronary Stenosis", "Thrombocytopenia, Neonatal Alloimmune", "Morphine Dependence", "Hemorrhagic Fevers, Viral", "Skull Fractures", "Neoplasms, Multiple Primary", "Pulmonary Subvalvular Stenosis", "Facial Neuralgia", "Thalamic Diseases", "Central Nervous System Helminthiasis", "Varicocele", "Lymphocele", "Massive Hepatic Necrosis", "Nephroma, Mesoblastic", "Macroglossia", "Ectodermal Dysplasia 3, Anhidrotic", "Hypertensive Encephalopathy", "Tangier Disease", "Lipoid Proteinosis of Urbach and Wiethe", "Peroneal Neuropathies", "Encephalomyelitis, Eastern Equine", "MeSH Disease Term", "Urethral Stricture", "Silicosis", "Lens Diseases", "Nevus of Ota", "Abortion, Incomplete", "Scleredema Adultorum", "Encopresis", "Birnaviridae Infections", "Wound Infection", "Carcinoma, Giant Cell", "Gingival Recession", "alpha 1-Antitrypsin Deficiency", "Perceptual Disorders", "Fractures, Cartilage", "Myocardial Bridging", "Papilloma, Intraductal", "Retrobulbar Hemorrhage", "Prune Belly Syndrome", "Filoviridae Infections", "Neurocytoma", "Borderline Personality Disorder", "Orbital Diseases", "Fascioloidiasis", "Polyradiculoneuropathy, Chronic Inflammatory Demyelinating", "Keratosis, Seborrheic", "Nocturnal Paroxysmal Dystonia", "Lymphangiectasis", "Sex Cord-Gonadal Stromal Tumors", "Ergotism", "Glucose Metabolism Disorders", "Uveal Neoplasms", "Vein of Galen Malformations", "Hypodermyiasis", "Aneurysm, False", "Retroperitoneal Fibrosis", "Skull Fracture, Basilar", "Esophageal Achalasia", "Pulmonary Valve Insufficiency", "Hematoma, Subdural, Spinal", "Intracranial Arteriosclerosis", "Adenomatoid Tumor", "Uterine Cervicitis", "Poliomyelitis, Bulbar", "Cystic Adenomatoid Malformation of Lung, Congenital", "Embolism, Air", "Endocardial Cushion Defects", "Ehrlichiosis", "Vulvar Lichen Sclerosus", "Chondroma", "Melanosis", "Acinetobacter Infections", "Leukemia, Eosinophilic, Acute", "Chondrocalcinosis", "Hypervitaminosis A", "Pharyngitis", "Adenoma, Sweat Gland", "Sick Building Syndrome", "Leukemia, Hairy Cell", "Fasciitis, Necrotizing", "Herpes Zoster Ophthalmicus", "Granuloma, Lethal Midline", "Respiratory Paralysis", "Mushroom Poisoning", "Conduct Disorder", "Rickettsia Infections", "Spinal Cord Ischemia", "Brain Abscess", "Arthus Reaction", "Corynebacterium Infections", "Pregnancy, Ectopic", "Ochronosis", "Chylothorax", "Glomus Tympanicum Tumor", "Bulbar Palsy, Progressive", "Sinus Pericranii", "Head Injuries, Penetrating", "Orchitis", "Tuberculoma", "Tuberculoma, Intracranial", "Abducens Nerve Injury", "Still's Disease, Adult-Onset", "Hernia, Diaphragmatic, Traumatic", "Unconsciousness", "Pulmonary Eosinophilia", "Facial Hemiatrophy", "Sertoli-Leydig Cell Tumor", "Open Bite", "Myelitis, Transverse", "Cysticercosis", "Brachial Plexus Neuropathies", "Retroviridae Infections", "Paranasal Sinus Neoplasms", "Malocclusion, Angle Class II", "Lecithin Acyltransferase Deficiency", "Growth Hormone-Secreting Pituitary Adenoma", "Leprosy, Multibacillary", "Mumps", "DNA Repair-Deficiency Disorders", "Dermatitis, Phototoxic", "Fox-Fordyce Disease", "Encephalitis, Viral", "Conjunctivitis, Acute Hemorrhagic", "Pyloric Stenosis", "Paraneoplastic Syndromes, Nervous System", "Anastomotic Leak", "Toxoplasmosis", "Hepatitis E", "Paraparesis, Tropical Spastic", "Central Nervous System Viral Diseases", "Cryoglobulinemia", "Scrapie", "Fascioliasis", "Angiomyolipoma", "Tumor Lysis Syndrome", "Schizotypal Personality Disorder", "Lymphoma, T-Cell, Peripheral", "Myelolipoma", "Chorioretinitis", "Anemia, Refractory", "Keratoacanthoma", "Yersinia Infections", "Jaw Neoplasms", "Hyper-IgM Immunodeficiency Syndrome, Type 1", "Trichomonas Infections", "X-Linked Combined Immunodeficiency Diseases", "Hepatitis, Alcoholic", "Acidosis, Respiratory", "Protozoan Infections", "Sclerema Neonatorum", "Lutembacher Syndrome", "Staphylococcal Scalded Skin Syndrome", "Birth Injuries", "Chondroblastoma", "Myofascial Pain Syndromes", "Keratoconjunctivitis Sicca", "Jaw Fractures", "Varicose Ulcer", "Eye Neoplasms", "Subarachnoid Hemorrhage", "Carcinoma, Krebs 2", "Gastritis, Hypertrophic", "Venereal Tumors, Veterinary", "Nevus, Intradermal", "Chordoma", "Pseudolymphoma", "Fissure in Ano", "Infarction, Posterior Cerebral Artery", "Vaginal Fistula", "Erythema Chronicum Migrans", "Medullary Sponge Kidney", "Propionic Acidemia", "Intertrigo", "Metatarsalgia", "Dracunculiasis", "Chiari-Frommel Syndrome", "Salpingitis", "Buruli Ulcer", "Giant Cell Tumors", "Dental Fistula", "Pedophilia", "Hemoptysis", "Tennis Elbow", "Diffuse Neurofibrillary Tangles with Calcification", "Channelopathies", "Fatty Liver, Alcoholic", "Hyperpituitarism", "Hypoaldosteronism", "Aleutian Mink Disease", "Hypersomnolence, Idiopathic", "Colles' Fracture", "Electric Injuries", "Angioedemas, Hereditary", "Esophageal Fistula", "Tuberculosis, Oral", "Syringoma", "Elephantiasis, Filarial", "Nail-Patella Syndrome", "Paresis", "Candidiasis", "Tetanus", "Bone Malalignment", "Dent Disease", "Stupor", "Subdural Effusion", "Leptospirosis", "Paramyxoviridae Infections", "Esophageal Cyst", "Coccidiosis", "Bronchial Neoplasms", "Graves Ophthalmopathy", "Plant Poisoning", "Dupuytren Contracture", "Dendritic Cell Sarcoma, Follicular", "Hereditary Angioedema Type III", "Attention Deficit and Disruptive Behavior Disorders", "Dysphonia", "Menopause, Premature", "Tuberculosis, Osteoarticular", "Chromoblastomycosis", "Hallucinations", "Swine Erysipelas", "Nephritis", "Thyroiditis, Subacute", "Digestive System Fistula", "Paraparesis, Spastic", "Tuberculosis, Male Genital", "Hypolipoproteinemias", "Compartment Syndromes", "Bronchial Spasm", "IgG Deficiency", "Neurocysticercosis", "Whooping Cough", "Hematemesis", "Xerostomia", "Heat Stroke", "Atrial Premature Complexes", "Multicystic Dysplastic Kidney", "Hematoma, Subdural, Chronic", "Parotid Diseases", "Carotid Artery Injuries", "Paronychia", "Echinococcosis", "Premenstrual Syndrome", "Paranoid Disorders", "Urethral Diseases", "Abdominal Injuries", "Cytomegalovirus Retinitis", "Togaviridae Infections", "Pneumatosis Cystoides Intestinalis", "Albinism, Ocular", "Splenosis", "Menorrhagia", "Dysthymic Disorder", "Chondromatosis, Synovial", "Streptococcal Infections", "Penile Neoplasms", "Rib Fractures", "Yellow Fever", "Pyomyositis", "Andersen Syndrome", "Metaplasia", "Auditory Diseases, Central", "Livedo Reticularis", "Paget Disease, Extramammary", "Central Nervous System Vascular Malformations", "Lip Neoplasms", "Hyperamylasemia", "Femoracetabular Impingement", "Meningeal Carcinomatosis", "Trichostrongyloidiasis", "Glycogen Storage Disease Type VII", "Clonorchiasis", "Lichen Nitidus", "Gastroenteritis, Transmissible, of Swine", "Bacteriuria", "Shoulder Impingement Syndrome", "Osteochondritis", "Crush Syndrome", "Meningitis", "XYY Karyotype", "Angiolymphoid Hyperplasia with Eosinophilia", "Salmonella Food Poisoning", "Orbital Cellulitis", "Capillary Leak Syndrome", "Mesothelioma, Cystic", "Precursor T-Cell Lymphoblastic Leukemia-Lymphoma", "Neoplasms, Basal Cell", "Pregnancy Complications, Parasitic", "Fetal Nutrition Disorders", "Neurodermatitis", "Central Cord Syndrome", "Alcohol-Induced Disorders", "Sarcocystosis", "Iritis", "Hemorrhagic Fever, Crimean", "Classical Swine Fever", "Scotoma", "Burns, Chemical", "Anovulation", "Immunoblastic Lymphadenopathy", "Neurocirculatory Asthenia", "Sporotrichosis", "Urinary Bladder Calculi", "Dentigerous Cyst", "Teratocarcinoma", "Biliary Fistula", "Postgastrectomy Syndromes", "Nocturnal Enuresis", "Exotropia", "Otitis", "Myelitis", "Asphyxia Neonatorum", "Vitamin B Deficiency", "Brenner Tumor", "Aphasia, Conduction", "Palatal Neoplasms", "Dyslexia, Acquired", "Lymphoma, Primary Effusion", "MPTP Poisoning", "Calcium Metabolism Disorders", "Elimination Disorders", "Neuromuscular Junction Diseases", "Tumor Virus Infections", "Stomatitis", "Paratuberculosis", "Dermatitis, Photoallergic", "Night Terrors", "Retinal Telangiectasis", "Cystadenocarcinoma, Mucinous", "Gastroparesis", "Mixed Tumor, Malignant", "Sunburn", "Osteochondroma", "Hallux Rigidus", "Brain Damage, Chronic", "Pericarditis, Tuberculous", "Keratitis, Herpetic", "Equine Infectious Anemia", "Superinfection", "Sertoli Cell Tumor", "Failed Back Surgery Syndrome", "Headache Disorders, Primary", "Prosthesis-Related Infections", "Skin Diseases, Infectious", "Carcinoma, Acinar Cell", "Cadmium Poisoning", "Funnel Chest", "Alveolar Bone Loss", "Neoplasms, Adnexal and Skin Appendage", "Blind Loop Syndrome", "Malignant Atrophic Papulosis", "Prenatal Injuries", "Epilepsy, Partial, Sensory", "Biliary Tract Diseases", "Coronary Thrombosis", "Encephalitis, Varicella Zoster", "Fractures, Stress", "Ophthalmia Neonatorum", "Dentin, Secondary", "Herpangina", "Leukemia L5178", "Perivascular Epithelioid Cell Neoplasms", "Systemic Vasculitis", "Ovarian Cysts", "Abducens Nerve Diseases", "Marchiafava-Bignami Disease", "Ventricular Premature Complexes", "Rhinophyma", "Microsporidiosis", "von Willebrand Disease, Type 2", "Neuronal Migration Disorders", "Histrionic Personality Disorder", "Pleuropneumonia", "Tracheal Neoplasms", "Dental Caries", "Shock", "Heart Failure, Diastolic", "Adrenocortical Adenoma", "Erythema Nodosum", "Xanthogranuloma, Juvenile", "Ulnar Neuropathies", "Urinary Incontinence, Urge", "Serum Sickness", "Synovial Cyst", "Mediastinal Emphysema", "Trematode Infections", "Bernard-Soulier Syndrome", "Pica", "Polyomavirus Infections", "Teratoma", "Urinary Bladder Fistula", "Furunculosis", "Tonsillitis", "Nerve Compression Syndromes", "Orbital Pseudotumor", "Decalcification, Pathologic", "Nuchal Cord", "Pityriasis Rubra Pilaris", "Fibromyalgia", "Sialometaplasia, Necrotizing", "Dacryocystitis", "Parasitemia", "Gonadal Disorders", "Mastocytosis", "Pulpitis", "Parasystole", "Giant Lymph Node Hyperplasia", "Fecal Impaction", "Peanut Hypersensitivity", "Yang Deficiency", "Reoviridae Infections", "Tonsillar Neoplasms", "Puberty, Delayed", "Scimitar Syndrome", "Chromosome Fragility", "Arcus Senilis", "Compulsive Personality Disorder", "Latent Tuberculosis", "Leukemia, Myeloid, Chronic, Atypical, BCR-ABL Negative", "Brain Edema", "Dens in Dente", "Actinomycetales Infections", "Retrognathism", "Pellagra", "Fat Necrosis", "Adenocarcinoma, Mucinous", "Knee Injuries", "Tongue Diseases", "Trichiasis", "Mutism", "Fasciitis, Plantar", "Phlebotomus Fever", "Pneumonia, Atypical Interstitial, of Cattle", "Acute Disease", "Confusion", "Shellfish Poisoning", "Vascular Malformations", "Phagocyte Bactericidal Dysfunction", "Respiratory Tract Fistula", "Malignant Catarrh", "Dyspnea, Paroxysmal", "Renal Aminoacidurias", "Tooth Migration", "Zollinger-Ellison Syndrome", "Pleurisy", "Ureteral Obstruction", "Thrombophlebitis", "Holocarboxylase Synthetase Deficiency", "Menstruation Disturbances", "Cystadenocarcinoma", "Chorioamnionitis", "Wounds, Stab", "Tuberculosis, Hepatic", "Cor Triatriatum", "Meningeal Neoplasms", "Infectious Bovine Rhinotracheitis", "Heart Neoplasms", "Urinary Bladder, Neurogenic", "Obstetric Labor, Premature", "Cardiac Output, Low", "Dysentery, Amebic", "Lymphoma, AIDS-Related", "Eye Infections, Fungal", "Tooth Resorption", "Oculomotor Nerve Diseases", "Neuroacanthocytosis", "Akinetic Mutism", "Chagas Cardiomyopathy", "Passive-Aggressive Personality Disorder", "Waldenstrom Macroglobulinemia", "Gliosis", "Dermatitis, Irritant", "Myokymia", "Insect Bites and Stings", "Wasting Syndrome", "Anaplasia", "Pregnancy Complications, Infectious", "Alexia, Pure", "Tendon Entrapment", "Herpesviridae Infections", "Cerebrospinal Fluid Otorrhea", "Multiple Sulfatase Deficiency Disease", "Borna Disease", "Malacoplakia", "Femoral Neuropathy", "Bronchial Fistula", "Urethritis", "Pregnancy Complications, Neoplastic", "Crigler-Najjar Syndrome", "Poland Syndrome", "Brain Concussion", "Pain, Postoperative", "Follicular Cyst", "Erythema Multiforme", "Neuroectodermal Tumors, Primitive, Peripheral", "Anthrax", "Spinal Stenosis", "Double Outlet Right Ventricle", "Enterobiasis", "Sialadenitis", "Hemoglobinuria", "Diabetic Coma", "Fibromuscular Dysplasia", "Epididymitis", "Uveitis, Posterior", "Granuloma Annulare", "Shoulder Fractures", "Leukemia, B-Cell", "Coronary Restenosis", "Psittacosis", "Anthracosis", "Spondylosis", "Eye Injuries, Penetrating", "Spinal Fractures", "Polymyositis", "Dermatitis Herpetiformis", "Sexually Transmitted Diseases", "Taste Disorders", "Dysplastic Nevus Syndrome", "Dental Pulp Necrosis", "Heel Spur", "Acne Keloid", "Hip Injuries", "Invasive Pulmonary Aspergillosis", "Retroperitoneal Neoplasms", "Erythromelalgia", "Milk Sickness", "Thyroid Hormone Resistance Syndrome", "Middle Lobe Syndrome", "Tooth Attrition", "Out-of-Hospital Cardiac Arrest", "Multiple Personality Disorder", "Zygomycosis", "Lentigo", "Duodenal Neoplasms", "Jaw, Edentulous, Partially", "Neoplasms, Adipose Tissue", "Scleritis", "Embolism, Amniotic Fluid", "Infant, Newborn, Diseases", "Ureteral Calculi", "Pelvic Neoplasms", "Trypanosomiasis", "Anaplasmosis", "Gas Gangrene", "Neuromyelitis Optica", "Contusions", "Rinderpest", "Sciatica", "Enterovirus Infections", "Dicrocoeliasis", "Solitary Fibrous Tumors", "Ureterocele", "Hydronephrosis", "Pyonephrosis", "Urination Disorders", "Mycoses", "Callosities", "Postpoliomyelitis Syndrome", "Pseudotumor Cerebri", "Aortic Valve Insufficiency", "Arterial Occlusive Diseases", "Adenoma, Chromophobe", "Thyroid Crisis", "Status Epilepticus", "Meniere Disease", "Hantavirus Pulmonary Syndrome", "Herpes Labialis", "Macular Edema", "Accessory Nerve Diseases", "Gingival Pocket", "Keratitis, Dendritic", "Fused Teeth", "Encephalitis, Japanese", "Myotonia", "Struma Ovarii", "Hepatitis, Viral, Human", "Aphakia, Postcataract", "Uterine Inversion", "Sickle Cell Trait", "Granuloma, Foreign-Body", "Cystadenoma", "Yaws", "Paresthesia", "Tooth, Supernumerary", "Gonadal Dysgenesis, 46,XX", "Genomic Instability", "Berylliosis", "Cystitis", "Tuberculosis, Cutaneous", "Legionellosis", "Yin Deficiency", "Synkinesis", "Syphilis, Cardiovascular", "Hearing Loss, Functional", "Necrolytic Migratory Erythema", "Neurofibroma", "Hemobilia", "Postoperative Complications", "Blastomycosis", "Intra-Articular Fractures", "Viremia", "Delayed Graft Function", "Trypanosomiasis, African", "Osteosarcoma, Juxtacortical", "Gastroschisis", "Lymphocytic Choriomeningitis", "Maxillofacial Abnormalities", "Angiomyoma", "Urinary Bladder, Overactive", "Tooth Loss", "Tuberculosis, Laryngeal", "Alcoholic Neuropathy", "Niemann-Pick Disease, Type B", "Hypertension, Malignant", "Sarcoma, Clear Cell"]

for disease in diseaseList :
	diseaseId = diseaseList.index(disease)
	page = requests.get("https://www.drugbank.ca/unearth/q?utf8=%E2%9C%93&query="+disease+"&searcher=drugs")
	soup = BeautifulSoup(page.content, 'html.parser')
	drugList = list(soup.select("h2 a"))
	drugCount = 0
	f = open("disease_dataset/" + str(disease + ".txt"), "w")
	for drugLink in drugList :
		drugCount += 1
		print("DrugId: ", drugCount, file=f)
		j = re.match(dlink, str(drugLink))
		page1 = requests.get("https://www.drugbank.ca" + str(j.group(2)))
		soup1 = BeautifulSoup(page1.content, 'html.parser')
		drug = soup1.find(class_ = "card-content px-md-4 px-sm-2 pb-md-4 pb-sm-2")
		drug_items = drug.find_all(class_="section-header")
		cl = drug.find_all(class_ = "col-md-2 col-sm-4")
		ob = drug.find_all(class_ = "col-md-10 col-sm-8")
		flag = 0
		for i in cl:
			if i.get_text() == "Name":
				j = ob[cl.index(i)]
				j_text = j.get_text()
				if re.match(nline, j_text):
					j_text = re.sub(nline, "\\1", j_text)
				print("1. Name: ", j_text, file=f)
			if i.get_text() == "Groups":
				j = ob[cl.index(i)]
				j_text = j.get_text()
				if re.match(nline, j_text):
					j_text = re.sub(nline, "\\1", j_text)
				print("2. Groups: ", j_text, file=f)
			if i.get_text() == "Description" and flag == 0:
				j = ob[cl.index(i)]
				j_text = j.get_text()
				if re.match(nline, j_text):
					j_text = re.sub(nline, "\\1", j_text)
				print("3. Description: ", j_text, file=f)
				flag = 1
			if i.get_text() == "Indication":
				j = ob[cl.index(i)]
				j_text = j.get_text()
				if re.match(nline, j_text):
					j_text = re.sub(nline, "\\1", j_text)
				print("4. Indication: ", j_text, file=f)
	f.close()
	if diseaseId == 0:
		print("Done for one disease!", diseaseId)
	elif diseaseId < len(diseaseList) - 1:
		print("Done for another disease!", diseaseId)
	else:
		print("Done for the last disease! Yayyyy!!", diseaseId)