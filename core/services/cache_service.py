from _helpers import BaseCacheService
from django.conf import settings


class CoreCacheService(BaseCacheService):
    PREFIX = 'CR'
    KEYS = {
        'name': f'{PREFIX}'':NAME_{student_id}',
        'enter_year': f'{PREFIX}'':YEAR_{student_id}'
    }
    EX = settings.REDIS_REGISTER_EX

    def cache_name(self, student_id, name: str):
        return self._set(
            key=self.KEYS['name'].format(
                student_id=student_id
            ),
            val=name
        )

    def get_name(self, student_id) -> str:
        return self._get(
            key=self.KEYS['name'].format(
                student_id=student_id
            )
        )

    def cache_enter_year(self, student_id, enter_year) -> str:
        return self._set(
            key=self.KEYS['enter_year'].format(
                student_id=student_id
            ),
            val=enter_year
        )

    def get_enter_year(self, student_id) -> str:
        return self._get(
            key=self.KEYS['enter_year'].format(
                student_id=student_id
            )
        )
