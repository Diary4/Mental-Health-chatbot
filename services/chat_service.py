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
            "time_management": ["manage my time", "time management", "use time efficiently", "save time", "better use of time"]
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
            "crisis": ["suicide", "kill myself", "end it all", "don't want to live", "better off dead"]
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
        # Store user input in conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Check if this is a specific question about a topic
        is_question, topic_path = self.check_for_question(user_input)
        
        if is_question:
            # Get specific advice for this topic
            specific_advice = self.provide_specific_advice(topic_path)
            if specific_advice:
                # Store response in conversation history
                self.conversation_history.append({"role": "assistant", "content": specific_advice})
                return specific_advice
        
        # If not a specific question, detect keywords
        keywords = self.detect_keywords(user_input)
        print(f"Detected keywords: {keywords}")
        
        # Handle crisis situation first
        if "crisis" in keywords:
            response = random.choice(self.responses["crisis"])
        # Then check for specific keywords
        elif keywords:
            # Use the first detected keyword category
            response = random.choice(self.responses[keywords[0]])
        # Fall back to default responses
        else:
            response = random.choice(self.responses["default"])
            
        # Add variety with connectors occasionally
        connectors = [
            "I understand that's difficult. ",
            "Thank you for sharing that with me. ",
            "I'm here to support you. ",
            "",  # Empty connector for variety
            "It's okay to feel this way. "
        ]
        
        # 40% chance to add a connector
        if random.random() < 0.4:
            response = random.choice(connectors) + response
            
        # Store response in conversation history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Return the response
        return response