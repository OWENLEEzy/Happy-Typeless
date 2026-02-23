# src/repositories/mock_repository.py
import random
import uuid
from datetime import UTC, datetime, timedelta

from src.models.transcription import Transcription, TranscriptionList
from src.repositories.base import TranscriptionRepository

# Realistic content templates for mock data
CONTENT_TEMPLATES = {
    "work": [
        "The API needs to be refactored",
        "Can we schedule a meeting for tomorrow?",
        "I'll fix this bug by the end of the day",
        "The deployment is scheduled for Friday",
        "Need to review the pull requests",
        "Let's sync up about the project roadmap",
        "The database migration is complete",
        "I'm working on the authentication module",
        "The tests are failing on CI",
        "We need to optimize this query",
        "Documentation is outdated",
        "Should we use TypeScript or JavaScript?",
        "The feature branch is ready for review",
        "Let's deploy to staging first",
        "I need more context on this ticket",
    ],
    "casual": [
        "What's for lunch today?",
        "The weather is nice today",
        "I'm feeling tired",
        "Can you believe this happened?",
        "That's interesting",
        "I'm not sure about this",
        "Let me think about it",
        "Sounds good to me",
        "I'll get back to you on this",
        "Thanks for your help",
        "No worries at all",
        "Have a great weekend",
        "See you tomorrow",
        "That makes sense",
        "I appreciate it",
    ],
    "ideas": [
        "Idea for the new feature: add a dark mode",
        "What if we tried a different approach?",
        "We could simplify the architecture",
        "Let's brainstorm about the UI",
        "The user experience could be better",
        "I have a suggestion for the dashboard",
        "We should consider mobile users",
        "The onboarding flow needs improvement",
        "Accessibility is important",
        "Let's add some animations",
    ],
    "negative": [
        "This is so frustrating",
        "I can't believe this is happening again",
        "What a waste of time",
        "This is ridiculous",
        "I'm so done with this",
        "Why does this keep breaking?",
        "This is driving me crazy",
        "I'm so tired of these issues",
        "Are you kidding me?",
        "This is a nightmare",
    ],
    "questions": [
        "Should we use PostgreSQL or MongoDB?",
        "What's the best approach here?",
        "Can you explain this to me?",
        "How did you solve this problem?",
        "What are your thoughts on this?",
        "Is this the right direction?",
        "Have you considered this option?",
        "What's the timeline for this?",
        "Who's working on this?",
        "When can we ship this?",
    ],
    "short": [
        "OK",
        "Sure",
        "Got it",
        "Done",
        "Thanks",
        "Perfect",
        "Noted",
        "Agreed",
        "Sounds good",
        "Will do",
        "Yes",
        "No",
        "Maybe",
        "Hmm",
        "Wait",
    ],
    "long": [
        "I've been thinking about the architecture for a while now, and I believe we need to reconsider our approach to data modeling. The current schema doesn't scale well, and we're seeing performance issues in production.",
        "The user feedback has been incredibly valuable. People love the new interface, but there are some accessibility concerns we should address. The contrast ratio needs improvement, and keyboard navigation isn't working properly in some areas.",
        "After reviewing the codebase, I think we have some technical debt that needs to be addressed. The dependency tree is getting complex, and some packages haven't been updated in a while. We should plan a refactoring sprint.",
        "I wanted to share some thoughts about our development process. I think we could be more efficient if we had better code review practices and automated testing. The current manual testing approach is not scalable.",
        "The meeting yesterday was really productive. We covered a lot of ground regarding the product roadmap. I'll send out the notes later today, but the key takeaway is that we're focusing on user retention for the next quarter.",
    ],
}

# App names with frequencies
APPS = [
    ("VSCode", 25),
    ("Google Chrome", 20),
    ("Terminal", 15),
    ("Slack", 12),
    ("Typeless", 10),
    ("Figma", 8),
    ("Notion", 6),
    ("Discord", 4),
]

# Window titles
WINDOW_TITLES = {
    "VSCode": [
        "Typeless Voice Notes - VSCode",
        "main.py - Visual Studio Code",
        "config.py - Typeless Project",
        "README.md - Visual Studio Code",
    ],
    "Google Chrome": [
        "Gmail - Inbox",
        "GitHub - Repository",
        "Stack Overflow - Question",
        "Google Docs - Document",
    ],
    "Terminal": [
        "bash - Terminal",
        "zsh - ~",
        "python - Interactive",
    ],
    "Slack": [
        "Slack - #general",
        "Slack - #development",
        "Slack - DM",
    ],
    "Typeless": [
        "Typeless - Voice Notes",
        "Typeless - Settings",
        "Typeless - History",
    ],
    "Figma": [
        "Figma - Design File",
        "Figma - Prototype",
    ],
    "Notion": [
        "Notion - Documentation",
        "Notion - Meeting Notes",
    ],
    "Discord": [
        "Discord - #general",
        "Discord - Voice Channel",
    ],
}


class MockTranscriptionRepository(TranscriptionRepository):
    """Mock repository for testing with realistic data"""

    def __init__(self):
        self._data: TranscriptionList = TranscriptionList(items=[])

    def set_data(self, data: TranscriptionList | list[Transcription]):
        """Set mock data"""
        if isinstance(data, TranscriptionList):
            self._data = data
        else:
            self._data = TranscriptionList(items=data)

    def get_all(self) -> TranscriptionList:
        """Get all mock data"""
        return self._data

    def generate_mock(self, count: int = 500, days: int = 61):
        """Generate realistic mock transcription data

        Args:
            count: Number of records to generate
            days: Number of days to spread data across
        """
        start_time = datetime.now(UTC) - timedelta(days=days)

        # Hour weights - peak during work hours (9-17)
        hour_weights = [
            1,  # 0: late night
            1,  # 1
            1,  # 2
            1,  # 3
            1,  # 4
            1,  # 5
            2,  # 6: early morning
            3,  # 7
            8,  # 8: start work
            15,  # 9: peak
            20,  # 10
            25,  # 11
            30,  # 12: lunch
            28,  # 13
            25,  # 14
            22,  # 15
            20,  # 16
            18,  # 17
            15,  # 18: end work
            12,  # 19
            8,  # 20
            5,  # 21
            3,  # 22
            2,  # 23
        ]

        # Content category weights - more casual/work, less negative
        category_choices = (
            ["work"] * 30
            + ["casual"] * 35
            + ["ideas"] * 15
            + ["questions"] * 12
            + ["short"] * 5
            + ["long"] * 2
            + ["negative"] * 1
        )

        # Build app list with weights
        app_list = []
        for app, weight in APPS:
            app_list.extend([app] * weight)

        items = []
        for i in range(count):
            # Random time
            hour = random.choices(range(24), weights=hour_weights)[0]
            day_offset = random.randint(0, days - 1)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            random_time = start_time + timedelta(
                days=day_offset, hours=hour, minutes=minute, seconds=second
            )

            # Select content based on category
            category = random.choice(category_choices)
            content = random.choice(CONTENT_TEMPLATES[category])

            # Add some variety - sometimes prepend fillers
            if random.random() < 0.1:  # 10% chance
                fillers = ["Um,", "Uh,", "So,", "Like,", "Actually,", "Basically,"]
                content = f"{random.choice(fillers)} {content}"

            # Select app
            app_name = random.choice(app_list)
            window_title = random.choice(WINDOW_TITLES.get(app_name, [f"{app_name} - Window"]))

            # Duration based on content length with some variance
            base_duration = len(content) * 0.15  # ~150 chars / min speaking rate
            duration = max(1.5, base_duration + random.uniform(-2, 3))

            items.append(
                Transcription(
                    id=str(uuid.uuid4()),
                    timestamp=int(random_time.timestamp()),
                    content=content,
                    duration=round(duration, 3),
                    app_name=app_name,
                    window_title=window_title,
                )
            )

        self._data = TranscriptionList(items=sorted(items, key=lambda x: x.timestamp))
