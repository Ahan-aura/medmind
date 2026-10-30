export type Language = 'en' | 'te';

export const translations = {
  en: {
    appTitle: "MEDMIND AI",
    tagline: "Learn smarter. Detect earlier. Practice safer.",
    disclaimer: "EDUCATIONAL SIMULATION ONLY · Fictional patient cases & synthetic labs. Not intended for clinical diagnosis, treatment decisions, or emergency medical care.",
    login: {
      title: "Clinical Reasoning Practice Simulator",
      subtitle: "Sign in to access interactive patient cases and grounded AI tutoring",
      emailLabel: "Medical School Email",
      passwordLabel: "Password",
      signInBtn: "Sign In",
      quickStudent: "Quick Demo: Student (Alex Mercer)",
      quickTeacher: "Quick Demo: Faculty (Demo Faculty)",
      registerPrompt: "Need an account? Register as student",
      roleStudent: "Medical / Nursing Student",
      roleTeacher: "Clinical Faculty / Teacher"
    },
    nav: {
      cases: "Patient Cases",
      lessons: "Lessons",
      progress: "My Progress",
      teacher: "Faculty Dashboard",
      demoMode: "4-Min Demo Guide",
      logout: "Sign Out",
      studentBadge: "Student",
      teacherBadge: "Faculty"
    },
    cases: {
      header: "Patient Case Simulator",
      description: "Select an illustrative patient scenario. Practice interpreting laboratory patterns and formulate evidence-based clinical explanations.",
      initialRole: "Initial Diagnostic Encounter",
      reassessmentRole: "Concept Transfer Reassessment",
      startCase: "Begin Case Simulation",
      objective: "Learning Objective",
      fictionalNotice: "Fictional case for education only"
    },
    player: {
      patientHistory: "Patient Presentation & Clinical History",
      labsHeader: "Diagnostic Laboratory Panel",
      branchingHeader: "Clinical Investigation Path",
      decisionHeader: "Diagnostic Formulation & Justification",
      evidenceSelection: "Select Key Supporting Findings (Evidence)",
      reasoningLabel: "Explain Your Diagnostic Reasoning",
      reasoningPlaceholder: "Specify which clinical history clues and laboratory indices support your diagnosis, and explain the underlying pathophysiology...",
      confidenceLabel: "Diagnostic Confidence Calibration",
      confidenceHint: "How confident are you that this interpretation is correct?",
      submitBtn: "Submit Clinical Formulation",
      submitting: "Evaluating Reasoning Rubric...",
      revealedSmear: "Investigation Finding Revealed",
      continueBtn: "Proceed to Interpretation"
    },
    feedback: {
      title: "Evaluation & Grounded AI Tutor Feedback",
      scoreTitle: "Objective Rubric Performance",
      metBadge: "Criterion Satisfied",
      missedBadge: "Area for Improvement",
      aiLabel: "AI Clinical Tutor (Grounded in Guidelines)",
      fallbackLabel: "Curated Reference Guidance",
      whatRight: "What You Got Right",
      whatNeedsWork: "Gaps in Clinical Reasoning",
      whyMatters: "Pathophysiological Rationale",
      citationsHeader: "Evidence-Based Literature & Guidelines",
      reflectionPrompt: "Confidence & Calibration Reflection",
      uncertaintyNote: "Clinical Scope & Limitations",
      proceedLesson: "Proceed to Targeted Concept Lesson",
      skipToReassess: "Proceed Directly to Reassessment Case"
    },
    lessonsLibrary: {
      title: "Doctor Practice Lessons",
      subtitle: "Targeted clinical reasoning modules grounded in haematology evidence and guidelines",
      recommendedTitle: "Recommended for You",
      recommendedSubtitle: "Based on your recent simulation attempts and identified clinical misconceptions",
      allLessonsTitle: "All Practice Lessons",
      draftBadge: "Draft - pending clinical review",
      draftTooltip: "This educational lesson is in draft form and has not yet completed formal clinical review. For simulation study only.",
      mins: "mins",
      difficulty: "Difficulty",
      level: "Level",
      completed: "Completed",
      startLesson: "Start Lesson",
      reviewLesson: "Review Lesson",
      bestScore: "Best Score",
      teluguProgressNotice: "Telugu translation in progress — displaying English version with clinical terms."
    },
    lesson: {
      title: "Targeted Mastery Module",
      overview: "Clinical Overview",
      keyPrinciples: "Core Diagnostic Principles",
      pearl: "Clinical Practice Pearl",
      quizTitle: "Formative Check Questions",
      checkAnswer: "Check Answer",
      completeBtn: "Mark Lesson Completed & Begin Reassessment Case"
    },
    compare: {
      title: "Learning Transfer: Initial vs Reassessment",
      subtitle: "Demonstrating knowledge acquisition through independent patient case transfer",
      initialScore: "Initial Case Score",
      reassessScore: "Reassessment Score",
      scoreGain: "Mastery Gain",
      newlyMet: "Criteria Mastered on Transfer Case",
      viewProgress: "Go to Progress Dashboard"
    },
    progress: {
      title: "Learner Progress & Calibration Analytics",
      objectivesHeader: "Objective Mastery Trajectory",
      calibrationHeader: "Diagnostic Confidence vs Accuracy Calibration",
      calibrationDesc: "Brier-style calibration tracking learner self-awareness. Overconfidence (high confidence with missed diagnoses) triggers targeted reflection prompts.",
      misconceptionHistory: "Recorded Reasoning Misconceptions",
      timesObserved: "Times Encountered"
    },
    teacher: {
      title: "Faculty Cohort Analytics Dashboard",
      subtitle: "Aggregated cohort-level reasoning diagnostics for medical educators",
      cohortLabel: "Active Cohort",
      studentCount: "Enrolled Learners",
      cohortAverages: "Cohort Performance: Initial vs Reassessment",
      commonMisconceptions: "Top 5 Recurring Clinical Misconceptions",
      misconceptionTableDesc: "Identifies systemic curricular gaps requiring lecture or small-group reinforcement.",
      classCalibration: "Class-Wide Confidence Calibration Matrix"
    }
  },
  te: {
    appTitle: "మెడ్‌మైండ్ AI (MEDMIND AI)",
    tagline: "తెలివిగా నేర్చుకోండి. త్వరగా గుర్తించండి. సురక్షితంగా సాధన చేయండి.",
    disclaimer: "విద్యా ప్రయోజనాల కోసం మాత్రమే · రోగి కేస్ మరియు ప్రయోగశాల ఫలితాలు కల్పితమైనవి. నిజమైన రోగుల నిర్ధారణ లేదా చికిత్స కోసం కాదు.",
    login: {
      title: "క్లినికల్ రీజనింగ్ ప్రాక్టీస్ సిమ్యులేటర్",
      subtitle: "ఇంటరాక్టివ్ రోగి కేసులు మరియు ఆధారిత AI ట్యూటరింగ్ కోసం సైన్ ఇన్ చేయండి",
      emailLabel: "వైద్య విద్యార్థి ఈమెయిల్",
      passwordLabel: "పాస్‌వర్డ్",
      signInBtn: "సైన్ ఇన్ చేయండి",
      quickStudent: "డెమో విద్యార్థి (Alex Mercer)",
      quickTeacher: "డెమో అధ్యాపకులు (Demo Faculty)",
      registerPrompt: "ఖాతా లేదా? నమోదు చేసుకోండి",
      roleStudent: "వైద్య / నర్సింగ్ విద్యార్థి",
      roleTeacher: "క్లినికల్ ఫ్యాకల్టీ / ఉపాధ్యాయులు"
    },
    nav: {
      cases: "రోగి కేసులు (Cases)",
      lessons: "పాఠాలు (Lessons)",
      progress: "నా పురోగతి (Progress)",
      teacher: "ఫ్యాకల్టీ డ్యాష్‌బోర్డ్",
      demoMode: "4 నిమిషాల డెమో గైడ్",
      logout: "లాగ్ అవుట్",
      studentBadge: "విద్యార్థి",
      teacherBadge: "ఫ్యాకల్టీ"
    },
    cases: {
      header: "రోగి కేస్ సిమ్యులేటర్ (Patient Cases)",
      description: "రోగి పరిస్థితులను ఎంచుకోండి. ప్రయోగశాల ఫలితాలను విశ్లేషించి సరైన రోగనిర్ధారణ కారణాలను రూపొందించండి.",
      initialRole: "ప్రారంభ రోగనిర్ధారణ కేస్",
      reassessmentRole: "పునఃపరిశీలన కేస్ (Transfer)",
      startCase: "కేస్ ప్రారంభించండి",
      objective: "అభ్యసన లక్ష్యం (Objective)",
      fictionalNotice: "విద్యార్థుల సాధన కొరకు మాత్రమే"
    },
    player: {
      patientHistory: "రోగి చరిత్ర మరియు లక్షణాలు (History)",
      labsHeader: "ప్రయోగశాల పరీక్షల ఫలితాలు (Lab Panel)",
      branchingHeader: "రోగనిర్ధారణ పరిశోధన మార్గం",
      decisionHeader: "క్లినికల్ రోగనిర్ధారణ & కారణ వివరణ",
      evidenceSelection: "ఆధారాలను ఎంచుకోండి (Evidence)",
      reasoningLabel: "మీ రోగనిర్ధారణ కారణాన్ని వివరించండి",
      reasoningPlaceholder: "ఏ ప్రయోగశాల సూచికలు మరియు రోగి లక్షణాలు మీ నిర్ణయానికి మద్దతు ఇస్తున్నాయో వివరించండి...",
      confidenceLabel: "మీ విశ్వాస స్థాయి (Confidence Level)",
      confidenceHint: "ఈ రోగనిర్ధారణ సరైనదని మీరు ఎంత శాతం విశ్వసిస్తున్నారు?",
      submitBtn: "రోగనిర్ధారణను సమర్పించండి",
      submitting: "రూబ్రిక్ మూల్యాంకనం జరుగుతోంది...",
      revealedSmear: "పరిశోధన వివరాలు వెల్లడించబడ్డాయి",
      continueBtn: "నిర్ణయానికి కొనసాగండి"
    },
    feedback: {
      title: "మూల్యాంకనం & AI ట్యూటర్ ఫీడ్‌బ్యాక్",
      scoreTitle: "రూబ్రిక్ స్కోరు పనితీరు",
      metBadge: "సరైన ప్రమాణం",
      missedBadge: "మెరుగుపడవలసిన అంశం",
      aiLabel: "AI క్లినికల్ ట్యూటర్ (ఆధారిత వివరణ)",
      fallbackLabel: "సూచిక మార్గదర్శక వివరణ",
      whatRight: "మీరు సరిగ్గా గుర్తించినవి",
      whatNeedsWork: "మెరుగుపరచవలసిన కారణాలు",
      whyMatters: "క్లినికల్ ప్రాముఖ్యత",
      citationsHeader: "ఆధారిత వైద్య మార్గదర్శకాలు (Citations)",
      reflectionPrompt: "విశ్వాస ప్రతిబింబం (Reflection)",
      uncertaintyNote: "పరిమితులు మరియు పరిధి",
      proceedLesson: "లక్ష్య అభ్యసన పాఠానికి వెళ్లండి",
      skipToReassess: "పునఃపరిశీలన కేస్‌కు నేరుగా వెళ్లండి"
    },
    lessonsLibrary: {
      title: "డాక్టర్ ప్రాక్టీస్ పాఠాలు",
      subtitle: "హెమటాలజీ మార్గదర్శకాల ఆధారంగా రూపొందించిన క్లినికల్ రీజనింగ్ పాఠాలు",
      recommendedTitle: "మీ కోసం సూచించబడినవి",
      recommendedSubtitle: "మీ ఇటీవలి సిమ్యులేషన్ అభ్యాసాల ఆధారంగా రూపొందించబడింది",
      allLessonsTitle: "అన్ని ప్రాక్టీస్ పాఠాలు",
      draftBadge: "డ్రాఫ్ట్ - క్లినికల్ రివ్యూ పెండింగ్‌లో ఉంది",
      draftTooltip: "ఈ విద్యా పాఠం డ్రాఫ్ట్ రూపంలో ఉంది మరియు ఇంకా అధికారిక క్లినికల్ సమీక్షను పూర్తి చేయలేదు.",
      mins: "నిమిషాలు",
      difficulty: "కఠినత",
      level: "స్థాయి",
      completed: "పూర్తయింది",
      startLesson: "పాఠం ప్రారంభించండి",
      reviewLesson: "సమీక్షించండి",
      bestScore: "ఉత్తమ స్కోరు",
      teluguProgressNotice: "తెలుగు అనువాదం పురోగతిలో ఉంది — ఆంగ్ల సంస్కరణ చూపబడుతోంది."
    },
    lesson: {
      title: "లక్ష్య అభ్యసన పాఠం (Targeted Lesson)",
      overview: "క్లినికల్ అవలోకనం",
      keyPrinciples: "ముఖ్య సూత్రాలు",
      pearl: "క్లినికల్ ప్రాక్టీస్ పర్ల్",
      quizTitle: "సాధన ప్రశ్నలు (Practice Quiz)",
      checkAnswer: "సమాధానం సరిచూడండి",
      completeBtn: "పాఠం పూర్తయింది · పునఃపరిశీలన కేస్‌కు వెళ్లండి"
    },
    compare: {
      title: "నేర్చుకున్న అంశాల బదిలీ (Initial vs Reassessment)",
      subtitle: "కొత్త కేస్ ద్వారా జ్ఞాన బదిలీని కొలవడం",
      initialScore: "ప్రారంభ కేస్ స్కోరు",
      reassessScore: "పునఃపరిశీలన స్కోరు",
      scoreGain: "స్కోరు పెరుగుదల",
      newlyMet: "కొత్తగా సాధించిన ప్రమాణాలు",
      viewProgress: "పురోగతి డ్యాష్‌బోర్డ్‌కు వెళ్లండి"
    },
    progress: {
      title: "విద్యార్థి పురోగతి & కాలిబ్రేషన్",
      objectivesHeader: "అభ్యసన లక్ష్యాల పురోగతి",
      calibrationHeader: "విశ్వాసం vs ఖచ్చితత్వం కాలిబ్రేషన్",
      calibrationDesc: "విద్యార్థి విశ్వాస స్థాయిలు మరియు ఖచ్చితత్వం మధ్య సమతుల్యత ట్రాకింగ్.",
      misconceptionHistory: "గమనించిన అపోహలు",
      timesObserved: "ఎదురైన సార్లు"
    },
    teacher: {
      title: "ఫ్యాకల్టీ డ్యాష్‌బోర్డ్ (Teacher Dashboard)",
      subtitle: "తరగతి స్థాయి క్లినికల్ రీజనింగ్ కొలమానాలు",
      cohortLabel: "ప్రస్తుత బ్యాచ్",
      studentCount: "విద్యార్థుల సంఖ్య",
      cohortAverages: "సగటు స్కోరు: ప్రారంభం vs పునఃపరిశీలన",
      commonMisconceptions: "తరగతిలో సాధారణంగా కనిపించే 5 అపోహలు",
      misconceptionTableDesc: "లెక్చర్‌లలో పునరావృతం చేయవలసిన అంశాలను గుర్తిస్తుంది.",
      classCalibration: "తరగతి స్థాయి విశ్వాస కాలిబ్రేషన్"
    }
  }
};
