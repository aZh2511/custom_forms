from core.domain.repositories import IRepository
from core.domain.entities import Form


class MockedRepository(IRepository):
    def get_all_forms(self) -> set[Form]:
        return {
            Form.create('Mocked Form #1'),
            Form.create('Mocked Form #2'),
        }

