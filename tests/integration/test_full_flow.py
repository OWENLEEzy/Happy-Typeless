# tests/integration/test_full_flow.py
from src.factories.repository_factory import RepositoryFactory
from src.services.overview import OverviewService


def test_full_analysis_flow_with_mock():
    """Test complete flow: repository -> service -> result"""
    # Create mock repository
    factory = RepositoryFactory()
    repository = factory.create_mock_repository()
    repository.generate_mock(count=100, days=30)

    # Get data
    data = repository.get_all()
    assert len(data) == 100

    # Analyze with service
    overview_service = OverviewService(data)
    stats = overview_service.get_stats()

    assert stats.total_records == 100
    assert stats.total_words > 0
    assert stats.active_days > 0
