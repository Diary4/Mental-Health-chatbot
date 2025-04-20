# services/chat_service.py
import os
import random
from typing import Optional, List, Dict, Tuple

class ChatService:
    def __init__(self):
        # Load responses directly into the class
        self.responses = self._load_responses()
        self.advice = self._load_advice()
        self.conversation_history = []
        print("Chat service initialized successfully")
        
    def _load_responses(self) -> Dict[str, List[str]]:
        """Load all responses"""
        responses = {
            "default": [
                "I understand this is difficult. What specific part is most challenging for you?",
                "Thank you for sharing that with me. How long have you been feeling this way?",
                "I'm here to support you. Could you tell me more about what's on your mind?",
                "Your feelings are valid. What strategies have helped you cope in the past?",
                "It sounds like you're going through a lot. What would be most helpful to focus on right now?",
                "I appreciate you opening up about this. Would you like to explore some coping strategies together?",
                "That sounds challenging. What aspect of this situation is affecting you the most?",
                "I'm listening and here to support you. How can I be most helpful right now?",
                "It takes courage to share these feelings. Is there a particular area you'd like guidance with?"
            ],
            "stress": [
                "Dealing with stress can be overwhelming. Let's break this down into smaller, manageable parts.",
                "For immediate stress relief, try taking 5 deep breaths. Inhale for 4 counts, hold for 2, exhale for 6.",
                "When we're stressed, our thinking can become clouded. What's one small step you could take right now?",
                "Stress often builds up when we feel overwhelmed. Would it help to prioritize what needs to be done first?",
                "Sometimes stress comes from trying to do everything perfectly. Could you identify what's 'good enough' for now?",
                "Physical activity can help reduce stress hormones. Even a short 5-minute walk might help clear your mind.",
                "Mindfulness practices can help center you when stress feels overwhelming. Would you like to try a quick grounding exercise?",
                "Stress can affect our sleep, which then increases stress further. How has your sleep been lately?",
                "When we're under pressure, we often forget to take care of our basic needs. Have you been able to eat, hydrate, and rest today?"
            ],
            "depression": [
                "Depression can make even small tasks feel overwhelming. What's one tiny step that might feel manageable?",
                "I hear how difficult this is. Depression affects many people and there are pathways forward.",
                "When we're feeling low, self-care becomes even more important. Have you been able to meet your basic needs today?",
                "Depression often distorts our thinking. Could we try to challenge some of these thoughts together?",
                "It takes courage to talk about depression. What support systems do you have in place right now?",
                "Sometimes depression can make everything feel meaningless. Are there any activities, however small, that still bring you some sense of purpose?",
                "Depression often involves negative self-talk. Would you speak to a friend the way you speak to yourself?",
                "Many find it helpful to create a small routine when dealing with depression. Even just getting out of bed and brushing your teeth can be a victory.",
                "Have you noticed any specific patterns or triggers that seem to deepen your depression?"
            ],
            "anxiety": [
                "Anxiety can make threats seem larger than they really are. Let's examine your concerns together.",
                "When anxiety rises, try the 5-4-3-2-1 technique: notice 5 things you see, 4 things you can touch, 3 things you hear, 2 things you smell, and 1 thing you taste.",
                "Our minds often jump to worst-case scenarios when we're anxious. What's a more balanced perspective we could consider?",
                "Anxiety is often about future uncertainties. Can we focus on what you know and can control right now?",
                "Physical symptoms often accompany anxiety. Have you noticed any changes in your breathing or muscle tension?",
                "Anxiety can feel like your mind is racing. Would writing down your thoughts help externalize them?",
                "Some find it helpful to schedule 'worry time' - a specific 15 minutes each day dedicated to worrying, then trying to let it go at other times.",
                "Challenging anxious thoughts can help. What evidence supports your worry, and what evidence contradicts it?",
                "Regular mindfulness practice can help reduce anxiety over time. Have you tried any meditation or mindfulness techniques?"
            ],
            "overthinking": [
                "Overthinking often involves getting stuck in repetitive thought loops. What helps you break out of these patterns?",
                "When we overthink, we're often trying to solve problems that haven't happened yet. Can we focus on what's actually happening right now?",
                "Overthinking can be exhausting. Have you tried setting aside specific 'worry time' to contain these thoughts?",
                "Sometimes writing down our thoughts can help get them out of our heads. Would you like to try that?",
                "Overthinking often involves 'what if' scenarios. What evidence do you have that supports or contradicts these worries?",
                "The mind can create endless possibilities when we overthink. What's one small, concrete action you could take right now?",
                "When you notice yourself overthinking, try asking: 'Is this thought helpful right now?'",
                "Overthinking can make problems seem bigger than they are. Could we shrink this down to just the facts?",
                "Physical movement can sometimes interrupt overthinking. Would taking a short walk or stretching help?"
            ],
            "deadline": [
                "Project deadlines can be stressful. Let's create a simple plan to tackle this step by step.",
                "When facing a tight deadline, breaking the work into small chunks can make it feel more manageable. What's the first tiny step?",
                "It's common to feel overwhelmed when deadlines approach. What resources or support might help you meet this deadline?",
                "Time pressure can be intense. Would it help to set some short work intervals with brief breaks in between?",
                "Sometimes we need to negotiate deadlines. Is there any flexibility with this submission date?",
                "The Pomodoro technique - working for 25 minutes, then taking a 5-minute break - can help with focus when deadlines loom.",
                "Perfectionism can slow us down when we're on a deadline. What would 'good enough' look like for this project?",
                "Sometimes we need to make trade-offs when time is limited. What are the most essential elements to focus on?",
                "Have you tried creating a visual timeline for your project? Seeing the steps laid out can make the process clearer."
            ],
            "project": [
                "Projects can sometimes feel overwhelming. What specific part seems most challenging right now?",
                "Let's break down your project into smaller steps. What would be the very first action to take?",
                "Sometimes starting is the hardest part of a project. What's one small task you could complete in the next 30 minutes?",
                "Is there anyone who could offer support or collaborate with you on this project?",
                "Would it help to set some specific goals or milestones for your project?",
                "Creating a mental health app is meaningful work. What inspired you to focus on this area?",
                "For tech projects, starting with a simple prototype or MVP can help build momentum. Could you create a basic version first?",
                "What's the core value your mental health app will provide to users? Focusing on this can help prioritize features.",
                "Have you done any user research to understand what potential users might need from a mental health app?"
            ],
            "help": [
                "I'm here to support you. What specific kind of help would be most useful right now?",
                "I'd like to understand how I can best assist you. Could you share more about what you're going through?",
                "Thank you for reaching out for help - that takes courage. What's the most pressing concern you'd like to address?",
                "I'm listening and want to help. What would make the biggest difference for you right now?",
                "Different situations call for different kinds of support. What would be most helpful in this moment?",
                "Sometimes it helps to prioritize our concerns. What's the most immediate issue you'd like help with?",
                "I appreciate you reaching out. Would you like practical advice, emotional support, or maybe just someone to listen?",
                "Help comes in many forms. Would you like to explore some coping strategies, discuss resources, or just talk through your feelings?",
                "I'm here for you. What aspect of your situation feels most important to address first?"
            ],
            "mental_health": [
                "Mental health is just as important as physical health. What aspects of your mental wellbeing are you most concerned about?",
                "Taking care of our mental health often involves building small daily habits. What practices have you found helpful?",
                "Creating a mental health app is a wonderful way to support others. What features do you think would be most beneficial?",
                "Mental health exists on a spectrum and fluctuates over time. How would you describe your mental health journey?",
                "Many factors contribute to mental wellbeing - sleep, nutrition, movement, social connection, and meaning. Which of these areas feels most relevant for you right now?",
                "Digital mental health tools can provide valuable support. What kinds of support are you hoping to offer through your app?",
                "User experience is particularly important for mental health apps. How are you thinking about making your app accessible during difficult moments?",
                "Peer support can be a powerful element in mental health apps. Are you considering any community features?",
                "Mental health resources vary greatly in different regions. Are you designing your app for a specific location or globally?"
            ],
            "app": [
                "Developing an app requires balancing different priorities. What's your vision for this mental health application?",
                "User experience is crucial for mental health apps. How are you approaching the design to make it accessible during difficult moments?",
                "What features are you planning to include in your mental health app?",
                "Have you conducted user research to understand what potential users might need from your app?",
                "Privacy and security are especially important for mental health applications. How are you addressing these concerns?",
                "Are you incorporating any evidence-based therapeutic approaches in your app design?",
                "What makes your mental health app unique compared to others available?",
                "Are you considering accessibility features to make your app usable for people with different abilities?",
                "Testing with real users can provide valuable insights. Do you have plans for getting feedback on your app?"
            ],
            "time": [
                "Time management can be challenging. Would creating a schedule or timeline help you organize your remaining time?",
                "When time is limited, focusing on the most critical elements first can help. What's absolutely essential for your project?",
                "Sometimes we need to adjust our expectations when time is short. What would a realistic outcome look like given your timeframe?",
                "Breaking down the remaining time into specific work blocks might help. How many hours do you have available?",
                "The pressure of time constraints can sometimes spark creativity. What's the most efficient approach you could take?",
                "When working with limited time, eliminating distractions becomes even more important. How's your work environment?",
                "Sometimes we need external motivation when racing against time. Would working alongside someone else help?",
                "Have you tried time-boxing techniques like setting a timer for focused work periods?",
                "What specific aspects of your project are most time-consuming? Could any of these be simplified?"
            ],
            "crisis": [
                "I'm concerned about what you're sharing. Please consider contacting a crisis line immediately at 988 (US) or your local emergency services.",
                "Your safety is the priority. I strongly encourage you to reach out to a mental health professional or crisis support service right away.",
                "This sounds serious. Please consider calling a crisis helpline or going to your nearest emergency room for immediate support."
            ],
            "sleep": [
                "Sleep problems can significantly impact mental health. What aspects of sleep are challenging for you right now?",
                "Creating a consistent sleep routine can help train your body and mind for better rest. Would you like to explore some bedtime routine strategies?",
                "Many find that limiting screen time an hour before bed helps improve sleep quality. How do screens currently fit into your evening routine?",
                "Sleep environment matters - darkness, quiet, and comfortable temperature can all impact rest. How would you describe your sleep space?",
                "Trouble falling asleep often connects to racing thoughts. Would you like to try some techniques to quiet your mind before bedtime?",
                "Sleep difficulties can both cause and result from anxiety and depression. Have you noticed any patterns in how your mood affects your sleep?",
                "Short-term sleep problems are common during stressful periods. How long have you been experiencing sleep difficulties?",
                "Some find sleep tracking helpful to identify patterns. Have you tried monitoring your sleep habits?",
                "Certain foods and drinks like caffeine and alcohol can disrupt sleep patterns. How do these fit into your daily routine?"
            ],
            "grief": [
                "Grief is a deeply personal experience that unfolds differently for everyone. How have you been processing your loss?",
                "It's common for grief to come in waves, feeling manageable one moment and overwhelming the next. Does that resonate with your experience?",
                "Many people find comfort in honoring their loved one's memory in tangible ways. Have you thought about or created any remembrance rituals?",
                "There's no timeline for grief, despite what others might suggest. How have others' expectations affected your grieving process?",
                "Supporting your basic needs becomes especially important while grieving. How have you been caring for yourself physically?",
                "Some find that expressing feelings through creative outlets like writing or art helps process grief. Have you explored any expressive activities?",
                "Grief can sometimes feel isolating. Do you have people in your life who understand what you're going through?",
                "Anniversary dates and special occasions can often trigger stronger grief responses. Are there any significant dates approaching?",
                "It's normal for grief to affect concentration, memory, and decision-making. Have you noticed changes in your cognitive functioning?"
            ],
            "trauma": [
                "Processing trauma takes time and safety. What helps you feel grounded when difficult memories arise?",
                "Many trauma survivors find that physical sensations can be triggers. Have you identified any specific triggers in your daily life?",
                "Establishing routines can help create a sense of safety after trauma. What parts of your daily routine feel supportive?",
                "Self-compassion is particularly important when healing from trauma. How do you speak to yourself when trauma responses surface?",
                "Many find that trauma affects their sense of safety in the world. Has this been part of your experience?",
                "Trauma responses like hypervigilance serve a protective function. Have you noticed yourself being on high alert?",
                "Connecting with others who understand trauma can be validating. Do you have support people who understand what you've experienced?",
                "Trauma can live in the body. Have you explored any body-based approaches to processing your experiences?",
                "Recovery isn't linear, and healing from trauma often involves setbacks along with progress. How have you navigated the ups and downs of your healing journey?"
            ],
            "self_esteem": [
                "Our self-talk significantly impacts how we feel about ourselves. What's your internal dialogue like when you face challenges?",
                "Self-esteem often develops from early experiences. Can you identify when you first began to question your worth?",
                "Building self-esteem involves recognizing your strengths. What are some qualities or abilities you value in yourself?",
                "Comparing ourselves to others can undermine self-esteem. How does social comparison affect your self-perception?",
                "Sometimes we hold ourselves to impossible standards. What expectations do you find hardest to meet?",
                "Small successes can gradually build confidence. What's something small you've accomplished recently?",
                "Our relationships can either strengthen or weaken our self-esteem. Are there people in your life who help you feel valued?",
                "Self-compassion practices can help counter harsh self-criticism. How do you respond to yourself when you make mistakes?",
                "Body image often connects to overall self-esteem. How does your relationship with your body affect how you feel about yourself?"
            ],
            "relationships": [
                "Healthy relationships require clear communication. What aspects of communication feel challenging in your relationships?",
                "Boundaries help create safety and respect in relationships. How comfortable do you feel setting boundaries with others?",
                "Conflict is inevitable in relationships, but how we handle it matters. What's your typical approach to disagreements?",
                "Trust develops gradually through consistent experiences. Has trust been a concern in your current relationships?",
                "Different attachment styles can affect how we connect with others. Have you noticed patterns in how you relate to important people in your life?",
                "Loneliness and social isolation can significantly impact mental health. How connected do you feel to others right now?",
                "Relationships often mirror early life experiences. Do you notice any themes from your past appearing in current relationships?",
                "Finding balance between self-care and caring for others can be challenging. How do you maintain your own wellbeing while supporting others?",
                "Digital communication has changed how we connect. How do online interactions compare to in-person relationships for you?"
            ],
            "burnout": [
                "Burnout often develops gradually, with warning signs we might miss. What changes have you noticed in yourself recently?",
                "Chronic stress without recovery periods frequently leads to burnout. How often do you take breaks from work or responsibilities?",
                "Burnout often involves emotional exhaustion, cynicism, and reduced efficacy. Which of these resonates most with your experience?",
                "Values misalignment at work or school can contribute to burnout. How well does your current situation reflect what matters to you?",
                "Recovering from burnout requires addressing root causes, not just symptoms. What factors might be driving your exhaustion?",
                "Physical symptoms like headaches, digestive issues, or sleep problems often accompany burnout. Have you noticed physical changes?",
                "Setting limits becomes especially important when addressing burnout. What boundaries might help protect your wellbeing?",
                "Many find that burnout affects their sense of meaning and purpose. Has your motivation or sense of accomplishment changed?",
                "Burnout recovery takes time and often requires support. What resources might help you rebuild your energy reserves?"
            ],
            "mindfulness": [
                "Mindfulness involves bringing gentle awareness to the present moment. What helps you feel connected to the here and now?",
                "Starting with brief mindfulness practices can build the skill gradually. Would a short breathing exercise feel manageable?",
                "Many find mindfulness challenging because our minds naturally wander. What has your experience been with present-moment awareness?",
                "Mindfulness can be practiced in everyday activities like eating, walking, or washing dishes. Have you tried incorporating awareness into daily tasks?",
                "Some prefer movement-based mindfulness like yoga or tai chi. Have you explored any mindful movement practices?",
                "Mindfulness isn't about clearing the mind, but noticing thoughts without attachment. How do you relate to your thinking patterns?",
                "Regular practice helps build the mindfulness muscle. What might help you incorporate brief moments of awareness throughout your day?",
                "Body scan meditations help reconnect with physical sensations. Would you like to try a simple body awareness practice?",
                "Mindfulness can help create space between triggers and reactions. Have you noticed how awareness affects your response to challenges?"
            ]
        }
        return responses
        
    def _load_advice(self) -> Dict[str, Dict[str, str]]:
        """Load specific advice for different topics"""
        advice = {
            "stress_reduction": {
                "physical": "Physical techniques to reduce stress include:\n1. Deep breathing: Inhale slowly for 4 counts, hold for 2, exhale for 6\n2. Progressive muscle relaxation: Tense and then release each muscle group\n3. Brief exercise: Even a 5-minute walk can reduce stress hormones\n4. Stretching: Simple stretches can release physical tension\n5. Cold water: Splashing your face with cold water can activate your parasympathetic nervous system",
                
                "mental": "Mental techniques for stress reduction include:\n1. Mindfulness meditation: Focus on your breath or bodily sensations\n2. Grounding exercises: The 5-4-3-2-1 technique helps reconnect with your senses\n3. Thought challenging: Identify and question stress-inducing thoughts\n4. Visualization: Imagine a peaceful place in detail\n5. Cognitive reframing: Look for alternative perspectives on stressful situations",
                
                "practical": "Practical strategies to manage stress include:\n1. Time management: Break tasks into smaller steps with specific timeframes\n2. Boundary setting: Practice saying no to additional commitments\n3. Delegation: Identify tasks that others could help with\n4. Prioritization: Use techniques like the Eisenhower matrix to focus on what matters most\n5. Environment optimization: Create a calming workspace free of distractions",
                
                "lifestyle": "Lifestyle changes that reduce stress include:\n1. Regular sleep schedule: Aim for 7-9 hours of quality sleep\n2. Balanced nutrition: Reduce caffeine and sugar, increase whole foods\n3. Hydration: Drink water consistently throughout the day\n4. Social connection: Talk with supportive friends or family\n5. Media consumption: Limit exposure to negative news and social media",
                
                "long_term": "Long-term stress management strategies include:\n1. Regular exercise routine: 30 minutes of moderate activity most days\n2. Consistent mindfulness practice: Even 5-10 minutes daily builds resilience\n3. Journaling: Processing thoughts and feelings in writing\n4. Creative expression: Art, music, or other creative outlets\n5. Professional support: Consider therapy or counseling for ongoing stress"
            },
            
            "project_management": {
                "planning": "Effective project planning techniques:\n1. Define clear objectives and success criteria\n2. Break the project into manageable tasks and subtasks\n3. Create a visual timeline or Gantt chart\n4. Identify dependencies between tasks\n5. Build in buffer time for unexpected challenges",
                
                "prioritization": "Methods for prioritizing project tasks:\n1. MoSCoW method: Must have, Should have, Could have, Won't have\n2. Eisenhower matrix: Urgent/Important grid for decision making\n3. Value vs. Effort: Focus on high-value, low-effort tasks first\n4. Critical path: Identify the sequence of dependent tasks\n5. MVP approach: Define the minimal viable product to deliver first",
                
                "focus": "Techniques to maintain focus during project work:\n1. Pomodoro technique: 25 minutes of work, 5 minute break\n2. Time blocking: Schedule specific time for specific tasks\n3. Environment optimization: Minimize distractions in your workspace\n4. Clear start/end rituals: Signal to your brain when work begins and ends\n5. Single-tasking: Focus on one specific task at a time",
                
                "tools": "Useful tools for project management:\n1. Trello or Asana for task tracking\n2. Google Calendar for time management\n3. Forest app for focus sessions\n4. Notion for documentation and planning\n5. Time tracking apps like Toggl to understand where time goes",
                
                "deadline": "Strategies for tight deadlines:\n1. Scope reduction: Identify what's truly essential\n2. Timeboxing: Allocate fixed time periods for each task\n3. Quick feedback cycles: Check progress frequently\n4. Elimination: Remove unnecessary steps or perfectionism\n5. Parallel work: Identify tasks that can be done simultaneously"
            },
            
            "mental_health_app": {
                "features": "Key features to consider for a mental health app:\n1. Mood tracking and journaling tools\n2. Guided meditation and breathing exercises\n3. Cognitive behavioral therapy (CBT) techniques\n4. Crisis resources and emergency contacts\n5. Community support or peer connection options\n6. Sleep tracking and improvement tools\n7. Goal setting and habit building features\n8. Educational content about mental health\n9. Personalized recommendations\n10. Professional support connections",
                
                "design": "Design considerations for mental health apps:\n1. Simple, intuitive interface that works during distress\n2. Calming color scheme and visual elements\n3. Accessible design for various abilities\n4. Minimal steps required for core functions\n5. Positive, encouraging language and tone\n6. Customizable experience based on user needs\n7. Clear typography and readable text\n8. Considerate notification strategy\n9. Privacy-focused design elements\n10. Trauma-informed approach to all interactions",
                
                "technical": "Technical considerations for mental health apps:\n1. Data security and encryption for sensitive information\n2. Offline functionality for consistent access\n3. Efficient battery usage for regular engagement\n4. Cross-platform compatibility if possible\n5. Scalable architecture for growing user base\n6. Compliance with healthcare privacy regulations\n7. Accessible coding practices for screen readers\n8. Optimized performance for various devices\n9. Simple onboarding with minimal friction\n10. Regular backups and data protection",
                
                "research": "Research approaches for mental health apps:\n1. User interviews with potential app users\n2. Consultation with mental health professionals\n3. Competitive analysis of existing applications\n4. Literature review of digital mental health interventions\n5. Usability testing with diverse participants\n6. Analysis of app store reviews for similar apps\n7. Surveys about desired features and pain points\n8. Participatory design sessions with target users\n9. Prototype testing with think-aloud protocols\n10. Beta testing with feedback collection"
            },
            
            "time_management": {
                "techniques": "Effective time management techniques:\n1. Pomodoro method: 25 minutes of focused work followed by 5-minute breaks\n2. Time blocking: Scheduling specific activities for specific time periods\n3. Eisenhower matrix: Categorizing tasks by urgency and importance\n4. 2-minute rule: If a task takes less than 2 minutes, do it immediately\n5. Time batching: Grouping similar tasks together to reduce context switching",
                
                "prioritization": "Methods for prioritizing when time is limited:\n1. ABC method: Categorizing tasks as A (critical), B (important), or C (nice to have)\n2. MoSCoW method: Must have, Should have, Could have, Won't have\n3. Value vs. Effort analysis: Focus on high-value, low-effort tasks\n4. Pareto Principle: Identify the 20% of tasks that deliver 80% of results\n5. Opportunity cost consideration: What must be sacrificed for each choice?",
                
                "productivity": "Productivity enhancers for limited time:\n1. Elimination: Identify and cut unnecessary tasks or features\n2. Delegation: Determine what tasks others could help with\n3. Automation: Find repetitive tasks that could be automated\n4. Templates: Use or create templates rather than starting from scratch\n5. Focus tools: Utilize website blockers and do-not-disturb modes",
                
                "planning": "Planning strategies for tight deadlines:\n1. Backward planning: Start from the deadline and work backwards\n2. Buffer scheduling: Build in extra time for unexpected challenges\n3. Critical path analysis: Identify the sequence of dependent tasks\n4. Visual timeline creation: Map out the entire project with milestones\n5. Decision trees: Plan for different scenarios and contingencies"
            },
            "mental_health_basics": {
                "warning_signs": "Common mental health warning signs to monitor:\n1. Persistent changes in sleep patterns (insomnia or oversleeping)\n2. Significant mood changes lasting two weeks or longer\n3. Withdrawal from activities and relationships previously enjoyed\n4. Difficulty concentrating or completing familiar tasks\n5. Changes in appetite or weight (significant increase or decrease)\n6. Feelings of hopelessness or overwhelming worry\n7. Physical symptoms without clear causes (headaches, digestive issues)\n8. Increased use of substances to cope with emotions\n9. Thoughts of death or self-harm\n10. Decreased performance at work or school",
                
                "self_care_foundations": "Core elements of mental health self-care:\n1. Sleep hygiene: Consistent schedule, calming bedtime routine, screen limits\n2. Nutrition: Regular meals, hydration, limited alcohol and caffeine\n3. Physical activity: Regular movement, even brief walks can help\n4. Social connection: Maintaining supportive relationships\n5. Stress management: Regular relaxation practices and breaks\n6. Time in nature: Even brief outdoor exposure improves wellbeing\n7. Digital boundaries: Limiting news and social media consumption\n8. Meaningful activities: Engaging in purposeful actions aligned with values\n9. Help-seeking: Knowing when and how to access professional support\n10. Compassionate self-talk: Speaking to yourself with kindness",
                
                "crisis_resources": "Mental health crisis resources:\n1. National Suicide Prevention Lifeline: 988 (call or text)\n2. Crisis Text Line: Text HOME to 741741\n3. Veterans Crisis Line: 988, press 1\n4. Trevor Project (LGBTQ+): 866-488-7386\n5. Trans Lifeline: 877-565-8860\n6. SAMHSA Helpline: 800-662-4357\n7. Local emergency room or urgent care mental health services\n8. College/university counseling centers (for students)\n9. Employee Assistance Programs (for employed individuals)\n10. Local crisis intervention teams (available in many communities)",
                
                "therapy_types": "Common therapeutic approaches:\n1. Cognitive Behavioral Therapy (CBT): Addresses thought patterns and behaviors\n2. Dialectical Behavior Therapy (DBT): Skills for emotion regulation and distress tolerance\n3. Acceptance and Commitment Therapy (ACT): Psychological flexibility and values-aligned action\n4. Mindfulness-Based Cognitive Therapy: Combines mindfulness with traditional CBT\n5. Psychodynamic therapy: Explores unconscious patterns from past experiences\n6. EMDR: Processing traumatic memories through bilateral stimulation\n7. Interpersonal therapy: Focuses on relationship patterns and social functioning\n8. Solution-focused therapy: Brief approach emphasizing strengths and solutions\n9. Group therapy: Peer support facilitated by professionals\n10. Family systems therapy: Addresses patterns within family relationships",
                
                "stigma_facts": "Facts to counter mental health stigma:\n1. Mental health conditions affect 1 in 5 adults annually\n2. Mental health disorders are medical conditions, not character flaws\n3. Treatment success rates for mental health conditions compare favorably to those for physical conditions\n4. Recovery and management are possible with proper support\n5. Mental health exists on a spectrum - everyone has mental health\n6. Seeking help is a sign of strength, not weakness\n7. Many successful public figures manage mental health conditions\n8. Most people with mental illness never become violent\n9. Mental health conditions have biological, psychological, and social causes\n10. Supporting someone with a mental health condition makes a significant difference"
            },

            "digital_wellbeing": {
                "healthy_habits": "Healthy digital habits for mental wellbeing:\n1. Screen-free zones: Designate certain spaces as technology-free\n2. Tech curfew: Set a time to disconnect from devices before sleep\n3. Notification management: Customize alerts to reduce interruptions\n4. App time limits: Use built-in tools to monitor and restrict usage\n5. Content curation: Follow accounts that contribute positively to wellbeing\n6. Regular digital detox periods: Schedule brief breaks from technology\n7. Mindful consumption: Check in with how content makes you feel\n8. Physical posture: Maintain ergonomic positioning to reduce strain\n9. 20-20-20 rule: Every 20 minutes, look at something 20 feet away for 20 seconds\n10. Technology boundaries: Communicate limits with others in your life",
                
                "social_media": "Managing social media for better mental health:\n1. Comparison awareness: Remember feeds show curated highlights\n2. Content filtering: Unfollow or mute accounts that trigger negative emotions\n3. Engagement intention: Decide purpose before browsing (connection, inspiration, information)\n4. Active vs. passive use: Creating and connecting improves wellbeing more than scrolling\n5. Reality check: Remember filters, angles, and editing affect perception\n6. Time boundaries: Set specific times for checking platforms\n7. Physical prompts: Move phone farther away to reduce automatic checking\n8. Alternative activities: List non-digital activities that bring joy\n9. Designated periods: Consider scheduled social media breaks\n10. Values alignment: Ensure online time reflects personal values",
                
                "online_communities": "Finding supportive online mental health communities:\n1. Moderated spaces provide safer environments with community guidelines\n2. Peer support groups focus on shared experiences and mutual aid\n3. Professional oversight indicates evidence-informed approaches\n4. Privacy policies protect sensitive information sharing\n5. Content warnings help members prepare for potentially triggering material\n6. Resources sections offer additional support options\n7. Focus on specific conditions or experiences can provide targeted support\n8. Clear community values and guidelines establish expectations\n9. Multiple engagement options accommodate different comfort levels\n10. Regular community check-ins maintain supportive atmosphere",
                
                "app_evaluation": "Evaluating mental health apps:\n1. Evidence base: Research support for approaches used\n2. Developer credibility: Created by qualified health professionals or organizations\n3. Transparent privacy policy: Clear information about data collection and use\n4. Regular updates: Maintained and improved over time\n5. User reviews: Feedback from actual users about helpfulness\n6. Crisis support: Clear protocols for emergency situations\n7. Accessible design: Usable during mental health difficulties\n8. Customization options: Adaptable to individual needs\n9. Offline functionality: Available without constant internet connection\n10. Reasonable claims: Avoids promises of quick fixes or miracle results"
            },
             "overthinking": {
                "cognitive": "Cognitive techniques to manage overthinking:\n1. Thought stopping: Say 'stop' aloud when you notice rumination\n2. Scheduled worry time: Designate 15 minutes daily for worries, then let them go\n3. Reality testing: Ask 'What evidence supports this thought?'\n4. Worst-case scenario: Imagine the worst outcome and how you'd cope\n5. Probability estimation: Rate how likely feared outcomes actually are",
                
                "behavioral": "Behavioral strategies for overthinking:\n1. Distraction activities: Engage in absorbing tasks to interrupt rumination\n2. Physical movement: Exercise or stretching to shift mental state\n3. Delaying worry: Tell yourself 'I'll think about this later'\n4. Problem-solving: Convert worries into actionable steps\n5. Time limits: Set a timer for productive worry periods",
                
                "mindfulness": "Mindfulness approaches to overthinking:\n1. Observing thoughts: Imagine thoughts as clouds passing by\n2. Grounding exercises: Use the 5-4-3-2-1 technique\n3. Breathing focus: Count breaths to anchor in the present\n4. Body scans: Notice physical sensations to interrupt thoughts\n5. Labeling: Name thought patterns ('worrying', 'catastrophizing')",
                
                "long_term": "Long-term strategies to reduce overthinking:\n1. Journaling: Process thoughts in writing to get them out of your head\n2. CBT techniques: Work with a therapist on cognitive restructuring\n3. Values clarification: Focus on what matters rather than what worries\n4. Sleep hygiene: Ensure adequate rest to reduce rumination\n5. Medication: Consider SSRIs if overthinking is part of anxiety/depression"
            },
            
            "ocd_management": {
                "erp": "Exposure and Response Prevention (ERP) basics:\n1. Create hierarchy: List feared situations from least to most anxiety-provoking\n2. Start small: Begin with mildly challenging exposures\n3. Resist compulsions: Gradually increase time between obsession and compulsion\n4. Tolerate discomfort: Anxiety will decrease naturally with time\n5. Build up: Progress to more challenging exposures as you gain confidence",
                
                "cognitive": "Cognitive techniques for OCD:\n1. Thought labeling: 'This is just an OCD thought, not reality'\n2. Probability testing: Examine actual likelihood of feared outcomes\n3. Cost-benefit analysis: Weigh pros/cons of performing compulsions\n4. Uncertainty tolerance: Practice accepting 'maybe' instead of certainty\n5. Cognitive restructuring: Challenge exaggerated responsibility beliefs",
                
                "self_help": "Self-help strategies for OCD:\n1. Delay rituals: Gradually increase time before performing compulsions\n2. Modify compulsions: Change rituals to make them less satisfying\n3. Mindfulness: Observe intrusive thoughts without reacting\n4. Habit reversal: Replace compulsions with alternative behaviors\n5. Support groups: Connect with others facing similar challenges"
            },
            
            "ptsd_recovery": {
                "grounding": "Grounding techniques for PTSD:\n1. 5-4-3-2-1 method: Notice 5 things you see, 4 you can touch, etc.\n2. Anchoring objects: Carry something tangible to remind you of safety\n3. Temperature changes: Hold something cold or warm to shift focus\n4. Scent grounding: Use familiar, comforting smells\n5. Movement grounding: Gentle rocking or tapping",
                
                "processing": "Trauma processing approaches:\n1. Narrative exposure: Gradually recount trauma in safe setting\n2. EMDR: Use bilateral stimulation while recalling memories\n3. Body-based: Yoga or somatic experiencing to release tension\n4. Art therapy: Express experiences creatively\n5. Integration: Find meaning or growth from trauma experience",
                
                "safety": "Creating safety with PTSD:\n1. Safety plan: List coping strategies and emergency contacts\n2. Triggers map: Identify and prepare for known triggers\n3. Sleep hygiene: Ensure restful environment to reduce nightmares\n4. Boundaries: Communicate needs clearly to others\n5. Self-compassion: Practice kindness toward trauma responses"
            }
        }
        return advice
    
    def check_for_question(self, text: str) -> Tuple[bool, str]:
        """Check if the input is a question about a specific topic"""
        text = text.lower()
        
        # Check for phrases that indicate specific advice requests
        advice_requests = {
            "stress_reduction": ["how to reduce stress", "ways to reduce stress", "stress reduction", "manage stress", "dealing with stress", "cope with stress"],
            "project_management": ["manage my project", "project management", "organize my project", "project planning", "project tips"],
            "mental_health_app": ["mental health app", "app features", "design my app", "build an app", "app development"],
            "time_management": ["manage my time", "time management", "use time efficiently", "save time", "better use of time"],
            "mental_health_basics": ["mental health basics", "mental health information", "mental health facts", "mental health signs", "mental illness"],
            "digital_wellbeing": ["digital wellbeing", "screen time", "technology and mental health", "social media mental health", "digital health"],
            "overthinking": ["how to stop overthinking", "reduce rumination", "stop obsessive thoughts", "manage overthinking", "control my thoughts"],
            "ocd_management": ["manage ocd", "ocd help", "ocd strategies", "deal with intrusive thoughts", "stop compulsions"],
            "ptsd_recovery": ["ptsd recovery", "heal from trauma", "manage flashbacks", "deal with triggers", "cope with ptsd"]
        }
        
        for topic, phrases in advice_requests.items():
            if any(phrase in text for phrase in phrases):
                # Check for specific subtopics
                if topic == "stress_reduction":
                    if any(word in text for word in ["body", "physical", "breathing", "exercise"]):
                        return True, f"{topic}.physical"
                    elif any(word in text for word in ["mind", "mental", "thinking", "thoughts"]):
                        return True, f"{topic}.mental"
                    elif any(word in text for word in ["practical", "organize", "manage", "steps"]):
                        return True, f"{topic}.practical"
                    elif any(word in text for word in ["lifestyle", "habits", "daily", "routine"]):
                        return True, f"{topic}.lifestyle"
                    elif any(word in text for word in ["long term", "future", "ongoing"]):
                        return True, f"{topic}.long_term"
                    else:
                        # If no specific subtopic is detected, return all subtopics
                        return True, topic
                        
                elif topic == "project_management":
                    if any(word in text for word in ["plan", "planning", "organize"]):
                        return True, f"{topic}.planning"
                    elif any(word in text for word in ["prioritize", "important", "first"]):
                        return True, f"{topic}.prioritization"
                    elif any(word in text for word in ["focus", "concentrate", "distraction"]):
                        return True, f"{topic}.focus"
                    elif any(word in text for word in ["tools", "apps", "software"]):
                        return True, f"{topic}.tools"
                    elif any(word in text for word in ["deadline", "time", "quick"]):
                        return True, f"{topic}.deadline"
                    else:
                        return True, topic
                        
                elif topic == "mental_health_app":
                    if any(word in text for word in ["features", "functionality", "capabilities"]):
                        return True, f"{topic}.features"
                    elif any(word in text for word in ["design", "interface", "ui", "ux"]):
                        return True, f"{topic}.design"
                    elif any(word in text for word in ["technical", "code", "develop", "programming"]):
                        return True, f"{topic}.technical"
                    elif any(word in text for word in ["research", "study", "interview", "test"]):
                        return True, f"{topic}.research"
                    else:
                        return True, topic
                        
                elif topic == "time_management":
                    if any(word in text for word in ["techniques", "methods", "how to"]):
                        return True, f"{topic}.techniques"
                    elif any(word in text for word in ["prioritize", "important", "first"]):
                        return True, f"{topic}.prioritization"
                    elif any(word in text for word in ["productive", "efficiency", "effective"]):
                        return True, f"{topic}.productivity"
                    elif any(word in text for word in ["plan", "schedule", "organize"]):
                        return True, f"{topic}.planning"
                    else:
                        return True, topic
                        
                elif topic == "overthinking":
                    if any(word in text for word in ["mind", "thought", "cognitive", "thinking"]):
                        return True, f"{topic}.cognitive"
                    elif any(word in text for word in ["behavior", "action", "do", "activity"]):
                        return True, f"{topic}.behavioral"
                    elif any(word in text for word in ["present", "mindful", "awareness", "grounding"]):
                        return True, f"{topic}.mindfulness"
                    elif any(word in text for word in ["long term", "future", "ongoing"]):
                        return True, f"{topic}.long_term"
                    else:
                        return True, topic
                
                elif topic == "ocd_management":
                    if any(word in text for word in ["exposure", "erp", "face fear"]):
                        return True, f"{topic}.erp"
                    elif any(word in text for word in ["thought", "cognitive", "mind", "belief"]):
                        return True, f"{topic}.cognitive"
                    elif any(word in text for word in ["self help", "myself", "on my own"]):
                        return True, f"{topic}.self_help"
                    else:
                        return True, topic
                
                elif topic == "ptsd_recovery":
                    if any(word in text for word in ["ground", "present", "here and now", "calm"]):
                        return True, f"{topic}.grounding"
                    elif any(word in text for word in ["process", "memory", "trauma", "past"]):
                        return True, f"{topic}.processing"
                    elif any(word in text for word in ["safe", "protection", "environment"]):
                        return True, f"{topic}.safety"
                    else:
                        return True, topic
        
        return False, ""

    def detect_keywords(self, text: str) -> List[str]:
        """Simple keyword detection instead of emotion detection"""
        text = text.lower()
        keywords = []
        
        keyword_mapping = {
            "stress": ["stress", "overwhelm", "pressure", "tense", "burnout", "anxious"],
            "depression": ["depress", "sad", "hopeless", "low", "down", "meaningless"],
            "anxiety": ["anxi", "worry", "nervous", "fear", "panic", "afraid"],
            "deadline": ["deadline", "due date", "running out of time", "submit", "submission"],
            "project": ["project", "assignment", "work", "task", "homework"],
            "help": ["help", "support", "advice", "guidance", "assist"],
            "mental_health": ["mental health", "wellbeing", "emotional", "psychological", "therapy"],
            "app": ["app", "application", "software", "program", "development", "coding"],
            "time": ["time", "quick", "fast", "hurry", "rush", "soon"],
            "crisis": ["suicide", "kill myself", "end it all", "don't want to live", "better off dead"],
            "sleep": ["sleep", "insomnia", "tired", "rest", "fatigue", "bed", "awake"],
            "grief": ["grief", "loss", "death", "bereavement", "mourning", "died", "passed away"],
            "trauma": ["trauma", "ptsd", "traumatic", "abuse", "assault", "flashback", "trigger"],
            "self_esteem": ["self esteem", "confidence", "worth", "value", "self image", "self worth", "self doubt"],
            "relationships": ["relationship", "friend", "partner", "family", "social", "connection", "interpersonal"],
            "burnout": ["burnout", "exhausted", "drained", "overworked", "overwhelmed", "can't keep going"],
            "mindfulness": ["mindful", "meditation", "present", "awareness", "breath", "attention", "focus"],
            "overthinking": ["overthink", "ruminat", "dwell on", "can't stop thinking", "obsess", "fixat"],
            "ocd": ["ocd", "obsessive", "compulsive", "ritual", "intrusive thought"],
            "ptsd": ["ptsd", "trauma", "flashback", "triggered", "nightmare"],
            "bipolar": ["bipolar", "manic", "hypomanic", "mood swing", "depression and euphoria"],
            "eating_disorder": ["eating disorder", "anorexia", "bulimia", "binge eating", "purge", "body dysmorphia", "diet", "nutrition"],
            "addiction": ["addiction", "drug", "alcohol", "substance abuse", "addicted", "addiction recovery"],
            "depression": ["depression", "sad", "hopeless", "depressed", "depression symptoms", "depression treatment"],
            "anxiety": ["anxiety", "worry", "nervous", "fear", "panic", "afraid"],
            "addiction": ["addiction", "drug", "alcohol", "substance abuse", "addicted", "addiction recovery"],
            "depression": ["depression", "sad", "hopeless", "depressed", "depression symptoms", "depression treatment"],
            
        }
        
        for category, terms in keyword_mapping.items():
            if any(term in text for term in terms):
                keywords.append(category)
                
        return keywords

    def provide_specific_advice(self, topic_path: str) -> str:
        """Provide specific advice based on the topic path"""
        # Check if the topic has specific advice
        parts = topic_path.split('.')
        main_topic = parts[0]
        
        if main_topic not in self.advice:
            return ""
            
        # If there's a subtopic specified
        if len(parts) > 1 and parts[1] in self.advice[main_topic]:
            return self.advice[main_topic][parts[1]]
            
        # If just the main topic is specified, provide all subtopics
        full_advice = f"Here are some strategies for {main_topic.replace('_', ' ')}:\n\n"
        for subtopic, content in self.advice[main_topic].items():
            full_advice += f"--- {subtopic.capitalize()} ---\n{content}\n\n"
            
        return full_advice

    def generate_response(self, user_input: str) -> str:
        """Generate a response to user input"""
        
        self.conversation_history.append({"role": "user", "content": user_input})
        
        
        is_question, topic_path = self.check_for_question(user_input)
        
        if is_question:
            
            specific_advice = self.provide_specific_advice(topic_path)
            if specific_advice:
                
                self.conversation_history.append({"role": "assistant", "content": specific_advice})
                return specific_advice
        
        
        keywords = self.detect_keywords(user_input)
        print(f"Detected keywords: {keywords}")
        
       
        if "crisis" in keywords:
            response = random.choice(self.responses["crisis"])
        
        elif keywords:
            
            response = random.choice(self.responses[keywords[0]])
        
        else:
            response = random.choice(self.responses["default"])
            
        
        connectors = [
            "I understand that's difficult. ",
            "Thank you for sharing that with me. ",
            "I'm here to support you. ",
            "",  
            "It's okay to feel this way. "
        ]
        
        
        if random.random() < 0.4:
            response = random.choice(connectors) + response
            
       
        self.conversation_history.append({"role": "assistant", "content": response})
        
        
        return response