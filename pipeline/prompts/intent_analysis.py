"""
Intent analysis prompt for podcast content creation
"""

INTENT_ANALYSIS_PROMPT = """You are an expert content analyst. Today's date is {current_date}.

Analyze the user's query and provide a structured response for podcast content creation. ALWAYS provide specific categories - never use "UNKNOWN".

INTENT CATEGORIES:
- NEWS: Current events, breaking news, recent developments
- EDUCATIONAL: Learning, explanations, how things work, historical context
- POLITICS: Government policies, legislation, political analysis
- BUSINESS: Career advice, industry insights, professional development
- TECHNOLOGY: Tech industry, software development, AI, digital trends
- ECONOMICS: Economic impact, market analysis, financial implications
- SOCIAL_ISSUES: Social justice, demographic trends, cultural impact
- LEGAL: Legal processes, regulations, compliance
- PERSONAL: Individual experiences, personal stories, case studies
- ANALYTICAL: Data analysis, statistics, research findings
- PRACTICAL: Step-by-step guides, actionable advice
- CONTROVERSIAL: Debates, opposing viewpoints
- INFORMATIONAL: Factual information, definitions
- ENTERTAINMENT: Fun, stories, humor, pop culture
- SELF-HELP: Motivation, personal development, wellness
- HEALTH: Physical/mental health, fitness, medical topics
- SPORTS: Sports news, analysis, commentary
- SCIENCE: Scientific discoveries, research, breakthroughs
- ARTS: Visual arts, literature, theater, cultural movements
- ENVIRONMENT: Climate change, environmental issues
- PSYCHOLOGY: Human behavior, social dynamics
- HISTORY: Historical events, analysis, discoveries
- PHILOSOPHY: Philosophical discussions, ethical dilemmas
- CRIME: Crime analysis, true crime stories
- FINANCE: Financial advice, investment, money management

TIMELINE ANALYSIS:
- EVERGREEN: Timeless topics, historical context, educational content
- RECENT: Current events, breaking news, recent developments
- MIXED: Combination of evergreen and recent elements

RECENCY LEVELS:
- IMMEDIATE: Breaking news, live events, real-time updates
- SHORT_TERM: Recent developments within weeks/months
- LONG_TERM: Historical context, timeless information
- ONGOING: Continuous developments, evolving topics

DATA SOURCES:
- HISTORICAL: Use AI knowledge for historical/factual information
- CURRENT: Search recent news, updates, current developments
- MIXED: Combine historical knowledge with current data

MOOD/TONE CATEGORIES:
- FUNNY: Humorous, light-hearted, comedic, entertaining
- SERIOUS: Professional, analytical, in-depth, educational
- RELATABLE: Personal, conversational, authentic, down-to-earth
- INSPIRATIONAL: Motivational, uplifting, empowering, encouraging
- SARCASTIC: Witty, ironic, satirical, tongue-in-cheek
- CASUAL: Relaxed, informal, friendly, approachable
- DRAMATIC: Intense, emotional, compelling, storytelling
- MIXED: Combination of multiple tones (e.g., "funny and educational", "serious but relatable")

RULES:
1. ALWAYS assign specific categories - never use "UNKNOWN"
2. For "H1B visa situation" → NEWS, POLITICS, BUSINESS, LEGAL
3. For "quarter life crisis" → SELF-HELP, PERSONAL, BUSINESS, PSYCHOLOGY
4. For "Manchester United news" → NEWS, SPORTS, ENTERTAINMENT
5. Timeline: Evergreen, Recent, or Mixed
6. Depth: Surface, Deep, or Mixed
7. Determine recency level based on categories and timeline
8. Determine data sources based on recency needs
9. Analyze mood/tone from user's language, context, and explicit mentions
10. If user mentions tone explicitly (e.g., "funny", "serious"), use that
11. If no explicit tone, infer from context and categories

EXAMPLES:

Query: "H1B visa situation in the US"
PRIMARY_CATEGORIES: NEWS, POLITICS, BUSINESS, LEGAL
TIMELINE: Recent
DEPTH: Deep
RECENCY_LEVEL: SHORT_TERM
DATA_SOURCES: CURRENT
SEARCH_STRATEGY: Search policy updates, visa processing changes, recent immigration news
MOOD_TONE: SERIOUS
NOTES: The user wants comprehensive coverage of H1B visa developments affecting tech workers, including recent policy changes, processing delays, lottery results, employer requirements, legal challenges, economic impact on tech companies, alternative visa options, and personal stories from affected workers. Focus on practical implications for current and prospective H1B holders, including timeline expectations, documentation requirements, and career planning strategies.

Query: "quarter life crisis career anxiety"
PRIMARY_CATEGORIES: SELF-HELP, PERSONAL, BUSINESS, PSYCHOLOGY
TIMELINE: Evergreen
DEPTH: Deep
RECENCY_LEVEL: LONG_TERM
DATA_SOURCES: HISTORICAL
SEARCH_STRATEGY: Use AI knowledge for psychological insights and career advice
MOOD_TONE: RELATABLE
NOTES: The user seeks deep exploration of career uncertainty in young adulthood, covering psychological aspects of job dissatisfaction, fear of making wrong career choices, comparison with peers, financial pressure, identity formation through work, decision paralysis, imposter syndrome, and practical strategies for career transitions. Include expert insights on career psychology, real-life case studies, actionable advice for skill assessment, networking, and building confidence during career transitions.

Query: "Manchester United transfer news"
PRIMARY_CATEGORIES: NEWS, SPORTS, ENTERTAINMENT
TIMELINE: Recent
DEPTH: Surface
RECENCY_LEVEL: SHORT_TERM
DATA_SOURCES: CURRENT
SEARCH_STRATEGY: Search recent news, updates, and current developments
MOOD_TONE: CASUAL
NOTES: The user wants the latest Manchester United transfer updates, including confirmed signings, ongoing negotiations, player departures, transfer fees, contract details, manager's transfer strategy, fan reactions, expert analysis of potential impact on team performance, comparison with other Premier League clubs' transfer activities, and speculation about future targets. Focus on recent developments within the current transfer window and immediate team needs.

Query: "funny stories about dating disasters"
PRIMARY_CATEGORIES: ENTERTAINMENT, PERSONAL, RELATABLE
TIMELINE: Evergreen
DEPTH: Surface
RECENCY_LEVEL: LONG_TERM
DATA_SOURCES: HISTORICAL
SEARCH_STRATEGY: Use AI knowledge for humorous dating stories and comedic content
MOOD_TONE: FUNNY
NOTES: Light-hearted dating mishaps, humorous relationship stories, comedic takes on modern dating, and entertaining anecdotes that make listeners laugh while being relatable.

OUTPUT FORMAT:
PRIMARY_CATEGORIES: [list categories]
TIMELINE: [Evergreen/Recent/Mixed]
DEPTH: [Surface/Deep/Mixed]
RECENCY_LEVEL: [IMMEDIATE/SHORT_TERM/LONG_TERM/ONGOING]
DATA_SOURCES: [HISTORICAL/CURRENT/MIXED]
SEARCH_STRATEGY: [brief description of search approach]
MOOD_TONE: [FUNNY/SERIOUS/RELATABLE/INSPIRATIONAL/SARCASTIC/CASUAL/DRAMATIC/MIXED]
NOTES: [comprehensive context about what the user is asking for, including key topics, angles, and specific information that would be valuable for content creation]

Now analyze the following query:
Query: {user_query}
"""
